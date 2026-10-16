"""Retrieval ablation over data/synthetic with eval/gold.jsonl. Writes eval/results.md and eval/results.json.

    uv run --no-sync python eval/run_eval.py [--reingest] [--configs full,vector] [--k 20]
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
os.environ.setdefault("NEO_HOME", str(ROOT / ".neo" / "eval"))
os.environ.setdefault("NEO_PORT", os.environ.get("NEO_TEST_PORT", "6395"))
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
STATS = Path(os.environ["NEO_HOME"]) / "eval_ingest.json"
TYPES = ["single", "multi", "temporal", "ownership", "procedural"]
SHOW = ["recall@10", "fullcover@10", "answerin@10", "mrr@10", "hit@10", "recall@5", "fullcover@5", "answerin@5", "mrr@5", "hit@5"]


def ingest(store, reingest):
    from neo_cortex.write import ingest_path
    have = store.query("MATCH (d:Document) RETURN count(d)", tenant=TENANT)[0][0]
    if have >= N_DOCS and not reingest:
        return {"skipped": True, "documents_in_graph": have, **json.loads(STATS.read_text() if STATS.exists() else "{}")}
    if reingest and have:  # hash-skip would keep old documents, so start from an empty tenant
        store.query("MATCH (n) DETACH DELETE n", tenant=TENANT)
    t = time.time()
    tot = {}
    for kind in KINDS:
        for k, v in ingest_path(store, ROOT / "data" / "synthetic" / kind, tenant=TENANT).items():
            tot[k] = tot.get(k, 0) + v
    tot["seconds"] = round(time.time() - t, 1)
    STATS.parent.mkdir(parents=True, exist_ok=True)
    STATS.write_text(json.dumps({"first_ingest": tot}))
    return tot


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


def tool_eval(store, gold):
    from neo_cortex import tools
    ask_rows, who_rows = [], []
    for q in gold:
        if q["type"] in ("multi", "ownership"):
            t = time.perf_counter()
            out = tools.ask(store, q["question"], tenant=TENANT)
            ask_rows.append({"id": q["id"], "type": q["type"], "answer_in_ask": M.answer_in(out, q["answer"]),
                             "ms": (time.perf_counter() - t) * 1000})
        if q["type"] == "ownership":
            gold_people = M.people(q["answer"])
            row = {"id": q["id"], "gold": gold_people}
            # variants: the whole question as topic (what a lazy agent passes) and the gold non-person entity (linking ceiling)
            ents = [e for e in q["gold_entities"] if e not in gold_people]
            for tag, topic in (("question", q["question"]), ("entity", ents[0] if ents else q["question"])):
                out = tools.who(store, topic, tenant=TENANT)
                top = [norm_name for norm_name in (M.norm(m) for m in re.findall(r"^\d+\. \[[^\]]+\] (.+?) score", out, re.M))][:3]
                got = [M.norm(p) in top for p in gold_people]
                row[tag] = {"topic": topic, "top3": top, "any": float(any(got)), "all": float(all(got))}
            who_rows.append(row)
    return ask_rows, who_rows


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def table(header, rows):
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(r) + " |" for r in rows])


def render(res):
    cfgs, agg = res["configs"], res["aggregate"]
    L = ["# Retrieval evaluation", "",
         f"Synthetic Pellucid Pay corpus ({res['ingest'].get('documents', res['ingest'].get('documents_in_graph', '?'))} docs, AI-generated, fictional), "
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
    L += ["", "## Tools", ""]
    a = res["tools"]["ask"]
    L.append(f"- `ask` evidence pack, gold answer string present: multi {a['multi']:.2f} (n={a['n_multi']}), ownership {a['ownership']:.2f} (n={a['n_ownership']}); mean {a['ms']:.0f} ms")
    for tag, desc in (("question", "topic = whole question"), ("entity", "topic = gold non-person entity")):
        w = res["tools"]["who"][tag]
        L.append(f"- `who` ({desc}): gold person in top 3 (any) {w['any']:.2f}, all gold people {w['all']:.2f} (n={w['n']})")
    return "\n".join(L) + "\n"


def main():
    global K
    ap = argparse.ArgumentParser()
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
        per_q, agg, lat = {}, {}, {}
        for n in names:
            per_q[n] = run_config(store, n, CONFIGS[n], gold)
            agg[n] = by_type(per_q[n])
            ms = sorted(r["ms"] for r in per_q[n])
            lat[n] = {"mean": mean(ms), "p95": ms[int(0.95 * (len(ms) - 1))]}
            print(f"{n:24s} recall@10 {agg[n]['overall']['recall@10']:.3f} fullcover@10 {agg[n]['overall']['fullcover@10']:.3f} "
                  f"answerin@10 {agg[n]['overall']['answerin@10']:.3f}  {lat[n]['mean']:.0f} ms/q", flush=True)
        tools_res = {}
        if not a.no_tools:
            ask_rows, who_rows = tool_eval(store, gold)
            sub = lambda t: [r["answer_in_ask"] for r in ask_rows if r["type"] == t]  # noqa: E731
            tools_res = {"ask": {"multi": mean(sub("multi")), "ownership": mean(sub("ownership")), "n_multi": len(sub("multi")),
                                 "n_ownership": len(sub("ownership")), "ms": mean([r["ms"] for r in ask_rows]), "rows": ask_rows},
                         "who": {tag: {"any": mean([r[tag]["any"] for r in who_rows]), "all": mean([r[tag]["all"] for r in who_rows]),
                                       "n": len(who_rows)} for tag in ("question", "entity")} | {"rows": who_rows}}
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
    res = {"now_ms": NOW_MS, "k": K, "n_questions": len(gold), "ingest": ing, "configs": names, "aggregate": agg, "latency": lat,
           "bootstrap": boots, "tools": tools_res, "per_question": per_q, "gold": {q["id"]: q["gold_docs"] for q in gold},
           "total_seconds": round(time.time() - t0, 1)}
    out = Path(a.out)
    (out / "results.json").write_text(json.dumps(res, indent=1))
    if tools_res:
        (out / "results.md").write_text(render(res))
    for b in boots:
        print(f"bootstrap {b['subset']} {b['metric']}: {b['a']} vs {b['b']} delta {b['delta']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}]")
    print(f"total {res['total_seconds']} s; wrote {out}/results.md, results.json")


K = 20
if __name__ == "__main__":
    main()
