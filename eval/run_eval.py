"""Retrieval ablation over data/synthetic with eval/gold.jsonl. Writes eval/results.md and eval/results.json.

    uv run --no-sync python eval/run_eval.py [--setting clean|distract] [--reingest] [--configs full,vector] [--k 20]

--setting distract: the same synthetic tenant plus data/public/falkordb (docs + tickets) as distractors (HotpotQA-distractor style).
clean writes results.json, distract results_distract.json; results.md always holds the clean tables and, when both exist, a side-by-side section.
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
_pre = argparse.ArgumentParser(add_help=False)
_pre.add_argument("--setting", choices=["clean", "distract"], default="clean")
SETTING = _pre.parse_known_args()[0].setting
os.environ.setdefault("NEO_HOME", str(ROOT / ".neo" / ("eval-new" if SETTING == "clean" else "eval-distract")))
os.environ.setdefault("NEO_PORT", os.environ.get("NEO_TEST_PORT", "6395") if SETTING == "clean" else "6376")
import metrics as M  # noqa: E402

TENANT = "eval"
NOW_MS = int(datetime(2026, 10, 16, tzinfo=timezone.utc).timestamp() * 1000)
KINDS = ["doc", "adr", "ticket", "chat", "meeting", "session"]
ALL4 = ["vector", "bm25", "graph", "temporal"]
CONFIGS = {  # name -> channels (None = the product default: graph on, temporal only when the query has a time cue)
    "vector": ["vector"],
    "bm25": ["bm25"],
    "vector+bm25": ["vector", "bm25"],
    "vector+bm25+graph": ["vector", "bm25", "graph"],
    "vector+bm25+temporal": ["vector", "bm25", "temporal"],
    "full": ALL4,
    "full-graph": ["vector", "bm25", "temporal"],
    "auto": None,
}
N_DOCS = sum(1 for _ in open(ROOT / "data" / "synthetic" / "manifest.jsonl"))
N_PUBLIC = sum(1 for k in ("doc", "ticket") for f in (ROOT / "data" / "public" / "falkordb" / k).rglob("*") if f.is_file())
STATS = Path(os.environ["NEO_HOME"]) / "eval_ingest.json"
TYPES = ["single", "multi", "temporal", "ownership", "procedural"]
SHOW = ["recall@10", "fullcover@10", "answerin@10", "mrr@10", "hit@10", "recall@5", "fullcover@5", "answerin@5", "mrr@5", "hit@5"]


def ingest(store, reingest):
    """Synthetic corpus once; in the distract setting also data/public/falkordb/{doc,ticket} (resumable: unchanged docs are skipped)."""
    from neo_cortex.write import ingest_path
    have = store.query("MATCH (d:Document) RETURN count(d)", tenant=TENANT)[0][0]
    stats = json.loads(STATS.read_text() if STATS.exists() else "{}")
    done = have >= N_DOCS + (N_PUBLIC if SETTING == "distract" else 0) and (SETTING == "clean" or "public_ingest" in stats)
    if done and not reingest:
        return {"skipped": True, "documents_in_graph": have, **stats}
    if reingest and have:  # hash-skip would keep old documents, so start from an empty tenant
        store.query("MATCH (n) DETACH DELETE n", tenant=TENANT)
    t = time.time()
    tot = {}
    for kind in KINDS:
        for k, v in ingest_path(store, ROOT / "data" / "synthetic" / kind, tenant=TENANT).items():
            tot[k] = tot.get(k, 0) + v
    tot["seconds"] = round(time.time() - t, 1)
    if "first_ingest" not in stats or reingest:
        stats["first_ingest"] = tot
    if SETTING == "distract":
        t = time.time()
        pub = {}
        for kind in ("doc", "ticket"):
            for k, v in ingest_path(store, ROOT / "data" / "public" / "falkordb" / kind, tenant=TENANT).items():
                pub[k] = pub.get(k, 0) + v
        pub["seconds"] = round(time.time() - t, 1)
        if not (pub["errors"] or pub["unsupported"]):
            stats["public_ingest"] = pub
        tot["public"] = pub
    STATS.parent.mkdir(parents=True, exist_ok=True)
    STATS.write_text(json.dumps(stats))
    return tot | {"documents_in_graph": store.query("MATCH (d:Document) RETURN count(d)", tenant=TENANT)[0][0]}


def run_config(store, name, channels, gold):
    from neo_cortex.retrieve import recall
    rows, ms = [], []
    for q in gold:
        t = time.perf_counter()
        items = recall(store, q["question"], k=K, channels=channels, tenant=TENANT, now_ms=NOW_MS)
        ms.append((time.perf_counter() - t) * 1000)
        ranked = M.unique_docs(items)
        full = dict(store.query("MATCH (c:Chunk) WHERE c.id IN $i RETURN c.id, c.text", {"i": [it["id"] for it in items]}, TENANT))
        texts = {}  # full chunk text (recall() trims to 400 chars) joined per doc
        for it in items:
            d = (it.get("source") or {}).get("doc_id")
            if d:
                texts[d] = texts.get(d, "") + " " + full.get(it["id"], it["text"])
        rows.append({"id": q["id"], "type": q["type"], "ranked": ranked, "ms": ms[-1],
                     **M.question_metrics(ranked, q["gold_docs"], texts, q["answer"])})
    return rows


def by_type(rows):
    out = {"overall": M.aggregate([{k: v for k, v in r.items() if isinstance(v, float) and k != "ms"} for r in rows])}
    for t in TYPES:
        sub = [{k: v for k, v in r.items() if isinstance(v, float) and k != "ms"} for r in rows if r["type"] == t]
        out[t] = M.aggregate(sub)
    return out


def doc_people():
    """doc id -> participants parsed from the frontmatter of the corpus files (author is always a participant)."""
    out = {}
    for f in (ROOT / "data" / "synthetic").glob("*/*.md"):
        m = re.search(r"^participants: \[(.*)\]\s*$", f.read_text(), re.M)
        out[f.stem] = [p.strip() for p in m[1].split(",")] if m else []
    return out


def vector_who(ranked, people_of, n=10):
    """Baseline for `who`: people of the top-n vector-only docs, scored sum(1/rank), ties by earliest doc rank."""
    sc, first = {}, {}
    for r, d in enumerate(ranked[:n], 1):
        for p in people_of.get(d, []):
            sc[p] = sc.get(p, 0) + 1 / r
            first.setdefault(p, r)
    return [p for p in sorted(sc, key=lambda p: (-sc[p], first[p], p))]


def tool_eval(store, gold):
    from neo_cortex import tools
    from neo_cortex.retrieve import recall
    people_of = doc_people()
    ask_rows, who_rows = [], []
    for q in gold:
        if q["type"] in ("multi", "ownership"):
            t = time.perf_counter()
            out = tools.ask(store, q["question"], tenant=TENANT)
            ms = (time.perf_counter() - t) * 1000
            items = recall(store, q["question"], k=8, channels=["vector"], tenant=TENANT, now_ms=NOW_MS)  # baseline: top-8 vector chunks
            full = dict(store.query("MATCH (c:Chunk) WHERE c.id IN $i RETURN c.id, c.text", {"i": [it["id"] for it in items]}, TENANT))
            vtext = " ".join(full.get(it["id"], it["text"]) for it in items)
            ask_rows.append({"id": q["id"], "type": q["type"], "answer_in_ask": M.hit_answer(out, q), "answer_in_vec": M.hit_answer(vtext, q),
                             "chars_ask": len(out), "chars_vec": len(vtext), "ms": ms})
        if q["type"] == "ownership":
            gold_people = M.people(q["answer"])
            row = {"id": q["id"], "gold": gold_people}
            vec = M.unique_docs(recall(store, q["question"], k=K, channels=["vector"], tenant=TENANT, now_ms=NOW_MS))
            vtop = [M.norm(p) for p in vector_who(vec, people_of)][:3]
            got = [M.norm(p) in vtop for p in gold_people]
            row["vector"] = {"top3": vtop, "any": float(any(got)), "all": float(all(got))}
            # variants: the whole question as topic (what a lazy agent passes) and the gold non-person entity (linking ceiling)
            ents = [e for e in q["gold_entities"] if e not in gold_people]
            for tag, topic in (("question", q["question"]), ("entity", ents[0] if ents else q["question"])):
                out = tools.who(store, topic, tenant=TENANT)
                top = [norm_name for norm_name in (M.norm(m) for m in re.findall(r"^\d+\. \[[^\]]+\] (.+?) score", out, re.M))][:3]
                got = [M.norm(p) in top for p in gold_people]
                row[tag] = {"topic": topic, "top3": top, "any": float(any(got)), "all": float(all(got))}
            who_rows.append(row)
    return ask_rows, who_rows


def timeline_eval(store, gold):
    """Temporal answer check: does tools.timeline(topic) hold both the old and the new value, old line first, each line dated?
    Baseline: top-8 vector chunk text holds both values and at least two ISO dates (order is not recoverable from it)."""
    from neo_cortex import tools
    from neo_cortex.retrieve import recall
    tg = {k: v for k, v in json.load(open(ROOT / "eval" / "timeline_gold.json")).items() if not k.startswith("_")}
    rows = []
    for q in gold:
        if q["id"] not in tg:
            continue
        old, new = (M.norm(v) for v in tg[q["id"]]["values"])
        out = tools.timeline(store, tg[q["id"]]["topic"], tenant=TENANT)
        lines = [M.norm(l) for l in out.splitlines()[1:]]
        pos = lambda v: next((i for i, l in enumerate(lines) if f" {v} " in f" {l} "), None)  # noqa: E731
        po, pn = pos(old), pos(new)
        if po is not None and pn is not None and po > pn:  # "from OLD to NEW" on one line is ordered even if NEW appears on an earlier line
            po = pn if any(re.search(rf"\b{re.escape(old)}\b.*\b{re.escape(new)}\b", l) for l in lines) else po
        items = recall(store, q["question"], k=8, channels=["vector"], tenant=TENANT, now_ms=NOW_MS)
        full = dict(store.query("MATCH (c:Chunk) WHERE c.id IN $i RETURN c.id, c.text", {"i": [it["id"] for it in items]}, TENANT))
        vt = " ".join(full.get(it["id"], it["text"]) for it in items)
        vboth = f" {old} " in f" {M.norm(vt)} " and f" {new} " in f" {M.norm(vt)} "
        rows.append({"id": q["id"], "topic": tg[q["id"]]["topic"], "both": float(po is not None and pn is not None),
                     "ordered": float(po is not None and pn is not None and po <= pn),
                     "dated": float(all(re.match(r"\d{4} \d{2} \d{2}", lines[i]) for i in (po, pn) if i is not None) and po is not None and pn is not None),
                     "vec_both": float(vboth), "vec_both_dated": float(vboth and len(set(re.findall(r"\d{4}-\d{2}-\d{2}", vt))) >= 2)})
    return rows


def tool_boots(ask_rows, who_rows):
    """Paired bootstrap of the graph tools against their vector-only baselines (delta = tool - baseline)."""
    boots = []
    if ask_rows:
        for sub, ok in (("multi+ownership", lambda r: True), ("multi", lambda r: r["type"] == "multi"), ("ownership", lambda r: r["type"] == "ownership")):
            rs = [r for r in ask_rows if ok(r)]
            boots.append({"subset": sub, "metric": "answer-in-output", "a": "tools.ask", "b": "vector top-8 text",
                          **M.paired_bootstrap([r["answer_in_ask"] for r in rs], [r["answer_in_vec"] for r in rs])})
    for tag in ("question", "entity"):
        for m in ("any", "all"):
            if who_rows:
                boots.append({"subset": "ownership", "metric": f"who top3 {m} ({tag} topic)", "a": "tools.who", "b": "vector top-10 people",
                              **M.paired_bootstrap([r[tag][m] for r in who_rows], [r["vector"][m] for r in who_rows])})
    return boots


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def table(header, rows):
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(r) + " |" for r in rows])


def render(res):
    cfgs, agg = res["configs"], res["aggregate"]
    L = ["# Retrieval evaluation", "",
         f"Synthetic Pellucid Pay corpus, setting {res.get('setting', 'clean')} ({res['ingest'].get('documents_in_graph', res['ingest'].get('documents', '?'))} docs in the graph, AI-generated, fictional), "
         f"{res['n_questions']} gold questions, k={K} chunks collapsed to unique documents, fixed now = 2026-10-16T00:00Z. "
         "Hit/Recall/FullCover/MRR are against `gold_docs`; AnswerIn = normalised gold answer found in the retrieved chunk text "
         "(full chunk text of the first k unique documents, so it only checks that the answer string was retrieved, not that it is easy to extract).", "",
         f"Ingest: {res['ingest']}", ""]
    for m in SHOW:
        L += [f"## {m}", "", table(["config"] + ["overall"] + TYPES, [[c] + [f"{agg[c][t][m]:.2f}" for t in ["overall"] + TYPES] for c in cfgs]), ""]
    L += ["## Latency (ms per query, recall k=20)", "", table(["config", "mean", "p95"], [[c, f"{res['latency'][c]['mean']:.0f}", f"{res['latency'][c]['p95']:.0f}"] for c in cfgs]), ""]
    L += ["## Paired bootstrap (1000 resamples, seed 0, 95% CI of mean delta)", ""]
    for b in res["bootstrap"]:
        L.append(f"- {b['subset']}, {b['metric']}: `{b['a']}` vs `{b['b']}`: delta {b['delta']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}] "
                 f"(n={b['n']}, {'significant' if b['significant'] else 'inside noise'})")
    if res["tools"]:
        L += ["", "## Tools vs vector-only baselines", ""]
        a, w = res["tools"]["ask"], res["tools"]["who"]
        L.append(f"- `ask` evidence pack vs top-8 vector chunk text, gold answer keys present: tools.ask multi {a['multi']:.2f} / ownership {a['ownership']:.2f} "
                 f"(n={a['n_multi']}/{a['n_ownership']}); baseline multi {a['vec_multi']:.2f} / ownership {a['vec_ownership']:.2f}; "
                 f"mean size {a['chars_ask']:.0f} vs {a['chars_vec']:.0f} chars; ask {a['ms']:.0f} ms")
        for tag, desc in (("question", "topic = whole question"), ("entity", "topic = gold non-person entity")):
            L.append(f"- `who` ({desc}): gold person in top 3 (any) {w[tag]['any']:.2f}, all gold people {w[tag]['all']:.2f} (n={w['n']})")
        t = res["tools"].get("timeline")
        if t:
            L.append(f"- `timeline` on the gold entity (n={t['n']} temporal questions with an old to new value): both values listed {t['both']:.2f}, "
                     f"old before new {t['ordered']:.2f}, both on dated lines {t['dated']:.2f}; baseline top-8 vector text: both values {t['vec_both']:.2f}, "
                     f"both values and at least two ISO dates {t['vec_both_dated']:.2f}")
        L.append(f"- `who` baseline (people of the top-10 vector-only docs, scored by 1/rank): any {w['vector']['any']:.2f}, all {w['vector']['all']:.2f} (n={w['n']})")
        L += ["", "### Paired bootstrap, tool minus baseline", ""]
        for b in res["tool_bootstrap"]:
            L.append(f"- {b['subset']}, {b['metric']}: `{b['a']}` vs `{b['b']}`: delta {b['delta']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}] "
                     f"(n={b['n']}, {'significant' if b['significant'] else 'inside noise'})")
    return "\n".join(L) + "\n"


def mo(res, c, m):
    rs = [r[m] for r in res["per_question"][c] if r["type"] in ("multi", "ownership")]
    return mean(rs)


def blines(boots, subsets=("all questions", "multi+ownership")):
    return [f"  - {b['subset']}, {b['metric']}: `{b['a']}` vs `{b['b']}`: delta {b['delta']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}] "
            f"({'significant' if b['significant'] else 'inside noise'})" for b in boots if b["subset"] in subsets]


def compare(cl, di):
    """Side-by-side section from the two results files."""
    names = [c for c in cl["configs"] if c in di["configs"]]
    rows = []
    for c in names:
        rows.append([c] + [f"{x:.2f}" for r in (cl, di) for x in (r["aggregate"][c]["overall"]["recall@10"], r["aggregate"][c]["overall"]["fullcover@10"],
                                                                  mo(r, c, "recall@10"), mo(r, c, "fullcover@10"))]
                    + [f"{cl['latency'][c]['mean']:.0f} / {di['latency'][c]['mean']:.0f}"])
    ing = di["ingest"]
    L = ["## Clean vs distract", "",
         f"Distract = the synthetic tenant plus data/public/falkordb docs and tickets in the same tenant "
         f"({ing.get('documents_in_graph', '?')} documents in the graph vs {cl['ingest'].get('documents_in_graph', '?')} clean). "
         "Same 80 questions, same gold docs. R = Recall@10, FC = FullCover@10, M+O = multi + ownership questions (n=43).", "",
         table(["config", "clean R", "clean FC", "clean M+O R", "clean M+O FC", "distract R", "distract FC", "distract M+O R", "distract M+O FC", "ms/q clean / distract"], rows), ""]
    for tag, r in (("clean", cl), ("distract", di)):
        L += [f"- Bootstrap, {tag} (paired, 95% CI of mean delta vs the best non-graph config):"] + blines(r["bootstrap"])
    L += [""]
    for tag, r in (("clean", cl), ("distract", di)):
        t = r["tools"]
        if not t:
            continue
        a, w, tl = t["ask"], t["who"], t.get("timeline")
        L.append(f"- Tools, {tag}: ask answer-in-output multi {a['multi']:.2f} / ownership {a['ownership']:.2f} vs vector top-8 text {a['vec_multi']:.2f} / {a['vec_ownership']:.2f}; "
                 f"who top-3 (question topic) any {w['question']['any']:.2f} / all {w['question']['all']:.2f}, (entity topic) {w['entity']['any']:.2f} / {w['entity']['all']:.2f}, "
                 f"vector baseline {w['vector']['any']:.2f} / {w['vector']['all']:.2f}"
                 + (f"; timeline both values {tl['both']:.2f}, ordered {tl['ordered']:.2f}, dated {tl['dated']:.2f} vs vector both {tl['vec_both']:.2f} / with dates {tl['vec_both_dated']:.2f} (n={tl['n']})" if tl else ""))
        L += blines(r["tool_bootstrap"], ("multi+ownership", "ownership", "temporal"))
    return "\n".join(L) + "\n"


def write_md(out):
    rs = {s: json.loads(f.read_text()) for s, n in (("clean", "results.json"), ("distract", "results_distract.json")) if (f := out / n).exists()}
    base = rs.get("clean") or rs["distract"]
    (out / "results.md").write_text(render(base) + ("\n" + compare(rs["clean"], rs["distract"]) if len(rs) == 2 else ""))


def main():
    global K
    ap = argparse.ArgumentParser()
    ap.add_argument("--setting", choices=["clean", "distract"], default="clean")
    ap.add_argument("--ingest-only", action="store_true")
    ap.add_argument("--reingest", action="store_true")
    ap.add_argument("--configs", default=",".join(CONFIGS))
    ap.add_argument("--k", type=int, default=20)
    ap.add_argument("--no-tools", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "eval"))
    a = ap.parse_args()
    K = a.k
    names = a.configs.split(",")
    bad = [n for n in names if n not in CONFIGS]
    if bad:
        sys.exit(f"unknown configs {bad}; choose from {list(CONFIGS)}")
    gold = [json.loads(l) for l in open(ROOT / "eval" / "gold.jsonl") if l.strip()]
    from neo_cortex.store import Store
    t0 = time.time()
    with Store() as store:
        ing = ingest(store, a.reingest)
        print("ingest:", ing, flush=True)
        if ing.get("errors") or ing.get("unsupported"):
            sys.exit("ingest had errors (see stderr; GPU OOM from another process?); rerun to resume (unchanged docs are skipped)")
        if a.ingest_only:
            return
        per_q, agg, lat = {}, {}, {}
        for n in names:
            per_q[n] = run_config(store, n, CONFIGS[n], gold)
            agg[n] = by_type(per_q[n])
            ms = sorted(r["ms"] for r in per_q[n])
            lat[n] = {"mean": mean(ms), "p95": ms[int(0.95 * (len(ms) - 1))]}
            print(f"{n:24s} recall@10 {agg[n]['overall']['recall@10']:.3f} fullcover@10 {agg[n]['overall']['fullcover@10']:.3f} "
                  f"answerin@10 {agg[n]['overall']['answerin@10']:.3f}  {lat[n]['mean']:.0f} ms/q", flush=True)
        tools_res, tboots = {}, []
        if not a.no_tools:
            ask_rows, who_rows = tool_eval(store, gold)
            tl_rows = timeline_eval(store, gold)
            sub = lambda t, k="answer_in_ask": [r[k] for r in ask_rows if r["type"] == t]  # noqa: E731
            tools_res = {"ask": {"multi": mean(sub("multi")), "ownership": mean(sub("ownership")), "n_multi": len(sub("multi")),
                                 "n_ownership": len(sub("ownership")), "vec_multi": mean(sub("multi", "answer_in_vec")),
                                 "vec_ownership": mean(sub("ownership", "answer_in_vec")), "chars_ask": mean([r["chars_ask"] for r in ask_rows]),
                                 "chars_vec": mean([r["chars_vec"] for r in ask_rows]), "ms": mean([r["ms"] for r in ask_rows]), "rows": ask_rows},
                         "who": {tag: {"any": mean([r[tag]["any"] for r in who_rows]), "all": mean([r[tag]["all"] for r in who_rows])}
                                 for tag in ("question", "entity", "vector")} | {"n": len(who_rows), "rows": who_rows},
                         "timeline": {**{k: mean([r[k] for r in tl_rows]) for k in ("both", "ordered", "dated", "vec_both", "vec_both_dated")},
                                      "n": len(tl_rows), "rows": tl_rows}}
            tboots = tool_boots(ask_rows, who_rows)
            tboots.append({"subset": "temporal", "metric": "both old+new value present", "a": "tools.timeline", "b": "vector top-8 text",
                           **M.paired_bootstrap([r["both"] for r in tl_rows], [r["vec_both"] for r in tl_rows])})
    # bootstrap: full and auto vs the best config that has no graph channel
    boots = []
    nog = [n for n in names if CONFIGS[n] is not None and "graph" not in CONFIGS[n] and n in per_q]
    for cfg in ("full", "auto"):
        if cfg not in per_q or not nog:
            continue
        best = max(nog, key=lambda n: (agg[n]["overall"]["recall@10"], agg[n]["overall"]["fullcover@10"]))
        odd = lambda i: int(gold[i]["id"][1:]) % 2 == 1  # noqa: E731
        for subset, ok in (("all questions", lambda i: True), ("odd questions", odd), ("even questions", lambda i: not odd(i)),
                           ("multi+ownership", lambda i: gold[i]["type"] in ("multi", "ownership"))):
            idx = [i for i in range(len(gold)) if ok(i)]
            for m in ("recall@10", "fullcover@10"):
                r = M.paired_bootstrap([per_q[cfg][i][m] for i in idx], [per_q[best][i][m] for i in idx])
                boots.append({"subset": subset, "metric": m, "a": cfg, "b": best, **r})
    res = {"setting": SETTING, "now_ms": NOW_MS, "k": K, "n_questions": len(gold), "ingest": ing, "configs": names, "aggregate": agg, "latency": lat,
           "bootstrap": boots, "tools": tools_res, "tool_bootstrap": tboots, "per_question": per_q, "gold": {q["id"]: q["gold_docs"] for q in gold},
           "total_seconds": round(time.time() - t0, 1)}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / ("results.json" if SETTING == "clean" else "results_distract.json")).write_text(json.dumps(res, indent=1))
    write_md(out)
    for b in boots + tboots:
        print(f"bootstrap {b['subset']} {b['metric']}: {b['a']} vs {b['b']} delta {b['delta']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}]")
    print(f"total {res['total_seconds']} s; wrote {out}/results.md and the {SETTING} json")


K = 20
if __name__ == "__main__":
    main()
