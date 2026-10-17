"""Real-text check of RAG and the knowledge graph on this repository's own docs (tenant "real").

    NEO_HOME=<dir> NEO_PORT=<port> uv run --no-sync python eval/real_check.py [--ingest] [--out eval/real_check.md]

--ingest wipes tenant "real" and ingests real_files() (README, AGENTS files, docs/, eval reports, demo script, the
Claude Code integration README and knowledge/ except knowledge/references/). Without it the existing graph is checked as is.
Questions and entity/relation checks: eval/real_gold.jsonl (answers and evidence must be verbatim in their gold files;
load_gold() asserts that on every start). Writes Markdown to --out: RAG (rank, answer containment, Hit@1/5, MRR,
latency), graph health, entity and relation checks, and 15 random REL edges with their source text (random seed 0).
NEO_HOME and NEO_PORT are required (never the default ~/.neo-cortex). Use NEO_DEVICE=cpu for a baseline on a shared GPU.
"""
import argparse
import json
import os
import random
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics as M  # noqa: E402  (eval/metrics.py, shared with run_eval.py)

TENANT = "real"
K = 20
QTYPES = ["fact", "why", "how", "number", "where"]
GOLD = ROOT / "eval" / "real_gold.jsonl"
FIXED = ["README.md", "AGENTS.md", "src/neo_cortex/AGENTS.md", "eval/README.md", "eval/results.md", "eval/answers.md",
         "eval/stress.md", "demo/SCRIPT.md", "integrations/claude-code/README.md"]
GENERIC_FALLBACK = set("entity graph node edge module function class file team service tool model agent user system component".split())


def real_files() -> list[Path]:
    """The real corpus: FIXED, docs/*.md and knowledge/**/*.md. Never data/synthetic, never knowledge/references/."""
    rel = set(FIXED)
    rel |= {p.relative_to(ROOT).as_posix() for p in (ROOT / "docs").glob("*.md")}
    rel |= {p.relative_to(ROOT).as_posix() for p in (ROOT / "knowledge").glob("**/*.md")}
    rel = {r for r in rel if not r.startswith("knowledge/references/")}
    assert not any(r.startswith("data/") for r in rel), "data/ must not be in the real corpus"
    files = [ROOT / r for r in sorted(rel)]
    missing = [str(f) for f in files if not f.is_file()]
    assert not missing, f"missing corpus files: {missing}"
    return files


def load_gold() -> list[dict]:
    gold = [json.loads(l) for l in GOLD.read_text().splitlines() if l.strip()]
    ids = [q["id"] for q in gold]
    assert len(ids) == len(set(ids)), "duplicate ids in real_gold.jsonl"
    for q in gold:  # self-check: every gold file exists and the answer / evidence / entity string is verbatim in it
        for p in q["gold_paths"]:
            assert (ROOT / p).is_file(), f"{q['id']}: no gold file {p}"
        text = " ".join(" ".join((ROOT / p).read_text().split()) for p in q["gold_paths"])
        key = q.get("answer") or q.get("evidence") or q.get("entity")
        assert " ".join(key.split()) in text, f"{q['id']}: '{key}' is not verbatim in {q['gold_paths']}"
    return gold


def ingest(store, files):
    """Wipe the tenant first (the hash skip would keep documents that left the list), then ingest each file."""
    from neo_cortex.write import ingest_path
    store.query("MATCH (n) DETACH DELETE n", tenant=TENANT)
    tot, t = Counter(), time.time()
    for i, f in enumerate(files, 1):
        print(f"ingest {i}/{len(files)} {f.relative_to(ROOT).as_posix()}", flush=True)  # progress: a killed run shows where
        for k, v in ingest_path(store, f, tenant=TENANT).items():
            tot[k] += v
    return {**tot, "seconds": round(time.time() - t, 1)}


def rel_path(p) -> str:
    p = str(p)
    return Path(p).relative_to(ROOT).as_posix() if p.startswith(str(ROOT) + os.sep) else p


def doc_paths(store) -> dict:
    """Document id -> repo-relative path."""
    return {i: rel_path(p) for i, p in store.query("MATCH (d:Document) RETURN d.id, d.path", tenant=TENANT)}


def doc_of(item, docs):
    d = (item.get("source") or {}).get("doc_id")
    return docs.get(d)


def rag(store, gold, docs):
    from neo_cortex import tools
    from neo_cortex.retrieve import recall
    rows = []
    for q in gold:
        if q["type"] not in QTYPES:
            continue
        t = time.perf_counter()
        items = recall(store, q["question"], k=K, tenant=TENANT)
        ms_r = (time.perf_counter() - t) * 1000
        first, ranked = {}, []  # unique documents in rank order, with the channels of their best chunk
        for it in items:
            d = doc_of(it, docs)
            if d and d not in first:
                first[d] = it["channels"]
                ranked.append(d)
        ranks = [ranked.index(g) + 1 for g in q["gold_paths"] if g in ranked]
        rank = min(ranks) if ranks else None
        full = dict(store.query("MATCH (c:Chunk) WHERE c.id IN $i RETURN c.id, c.text", {"i": [it["id"] for it in items]}, TENANT))
        chunk5 = " ".join(full.get(it["id"], it["text"]) for it in items if doc_of(it, docs) in ranked[:5])
        t = time.perf_counter()
        ask_out = tools.ask(store, q["question"], tenant=TENANT)
        ms_a = (time.perf_counter() - t) * 1000
        recall5 = tools.recall(store, q["question"], k=5, tenant=TENANT)
        ans = q["answer"]
        rows.append({"id": q["id"], "type": q["type"], "question": q["question"], "answer": ans, "gold": q["gold_paths"],
                     "rank": rank, "hit@1": float(rank == 1), "hit@5": float(bool(rank and rank <= 5)),
                     "mrr": 1 / rank if rank else 0.0, "out5": M.answer_in(recall5, ans), "chunk5": M.answer_in(chunk5, ans),
                     "ask": M.answer_in(ask_out, ans), "ms_recall": ms_r, "ms_ask": ms_a,
                     "above": [(d, first[d]) for d in (ranked[:rank - 1] if rank else ranked)[:3]], "top1": ranked[0] if ranked else None})
    return rows


def agg(rows):
    n = len(rows)
    mean = lambda k: sum(r[k] for r in rows) / n if n else 0.0  # noqa: E731
    return {"n": n, "hit@1": mean("hit@1"), "hit@5": mean("hit@5"), "mrr": mean("mrr"), "out5": mean("out5"),
            "chunk5": mean("chunk5"), "ask": mean("ask")}


def pct(xs, p):
    s = sorted(xs)
    return s[int(round(p * (len(s) - 1)))] if s else 0.0


def stems(key: str) -> set:
    """Grouping stems for name variants: every letter run of 4+ and the letters-only key ("gliner2.5-base" -> gliner, glinerbase)."""
    runs = set(re.findall(r"[a-z]{4,}", key))
    letters = re.sub(r"[^a-z]", "", key)
    return runs | ({letters} if len(letters) >= 4 else set())


def graph_health(store, docs):
    from neo_cortex.util import normalize_key
    try:
        from neo_cortex.extract import is_generic
    except ImportError:  # shortcut: extract.is_generic is missing, so use a small local list
        is_generic = lambda name: normalize_key(name) in GENERIC_FALLBACK  # noqa: E731

    def q(cypher, params=None):
        return store.query(cypher, params, TENANT)

    G = {}
    dk = q("MATCH (d:Document) RETURN d.kind, d.doc_type")
    G["docs_kind"] = Counter(r[0] for r in dk)
    G["docs_doc_type"] = Counter(r[1] or "(none)" for r in dk)
    G["chunks"] = q("MATCH (c:Chunk) RETURN count(c)")[0][0]
    ents = q("MATCH (e:Entity) RETURN e.key, e.name, e.type, e.mentions")
    G["entities_by_type"] = Counter(r[2] for r in ents)
    G["entities"] = len(ents)
    G["rels_by_type"] = Counter(r[0] for r in q("MATCH ()-[r:REL]->() RETURN r.type"))
    G["mentions"] = q("MATCH ()-[m:MENTIONS]->() RETURN count(m)")[0][0]
    G["single_word"] = sum(1 for r in ents if " " not in (r[0] or ""))
    G["generic"] = sorted({r[1] for r in ents if is_generic(r[1] or "")})
    G["file_entities"] = sorted(r[1] for r in ents if r[2] == "file")
    groups = defaultdict(dict)  # stem -> {entity key: mentions}
    for key, _, _, m in ents:
        for s in stems(key or ""):
            groups[s][key] = m or 0
    G["variant_groups"] = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]
    edges = sorted(q("MATCH (h:Entity)-[r:REL]->(t:Entity) RETURN h.name, r.type, t.name, r.source_id, r.conf"),
                   key=lambda r: tuple(str(x) for x in r))
    sample = random.Random(0).sample(edges, min(15, len(edges)))
    cids = [e[3] for e in sample if e[3]]
    ctext = {r[0]: (r[1] or "", r[2]) for r in q("MATCH (c:Chunk) WHERE c.id IN $i RETURN c.id, c.text, c.doc_id", {"i": cids})} if cids else {}
    G["sample_edges"] = [(e, *ctext.get(e[3], ("(no source chunk)", None))) for e in sample]  # (edge, chunk text, doc id)
    G["sample_edges"] = [(e, t, docs.get(d)) for e, t, d in G["sample_edges"]]
    return G, normalize_key


def entity_checks(store, gold, normalize_key):
    out = []
    for e in gold:
        k = normalize_key(e["entity"])
        found = store.query("MATCH (e:Entity) WHERE e.key = $k OR $k IN e.aliases RETURN e.name, e.type, e.mentions", {"k": k}, TENANT)
        near = [] if found else store.query("MATCH (e:Entity) WHERE e.key CONTAINS $k RETURN e.name, e.type LIMIT 5", {"k": k}, TENANT)
        ok = any(r[1] in e["entity_types"] for r in found)
        out.append({"id": e["id"], "entity": e["entity"], "expected": e["entity_types"], "found": found, "near": near, "pass": ok})
    return out


def relation_checks(store, gold, normalize_key):
    out = []
    for r in gold:
        h, t = normalize_key(r["head"]), normalize_key(r["tail"])
        q = "MATCH (h:Entity)-[r:REL]->(t:Entity) WHERE (h.key = $h OR $h IN h.aliases) AND (t.key = $t OR $t IN t.aliases) AND r.type = $ty RETURN h.name, t.name, r.conf, r.source_id"
        fwd = store.query(q, {"h": h, "t": t, "ty": r["rel"]}, TENANT)
        rev = [] if fwd else store.query(q, {"h": t, "t": h, "ty": r["rel"]}, TENANT)
        heads = store.query("MATCH (e:Entity) WHERE e.key = $h OR $h IN e.aliases RETURN e.type", {"h": h}, TENANT)
        tails = store.query("MATCH (e:Entity) WHERE e.key = $t OR $t IN e.aliases RETURN e.type", {"t": t}, TENANT)
        own = store.query("MATCH (h:Entity)-[r:REL]->(t:Entity) WHERE h.key = $h OR $h IN h.aliases RETURN r.type, t.name LIMIT 5", {"h": h}, TENANT)
        out.append({"id": r["id"], "head": r["head"], "rel": r["rel"], "tail": r["tail"], "pass": bool(fwd), "edge": fwd[:2],
                    "reversed": bool(rev), "head_found": bool(heads), "tail_found": bool(tails), "head_edges": own})
    return out


def esc(s) -> str:
    return str(s).replace("|", "/").replace("\n", " ")


def table(header, rows):
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows])


def render(meta, ingest_stats, rows, G, ent, rel, files):
    L = ["# Real-text check: RAG and graph on this repository's docs", "",
         f"Generated {datetime.now(timezone.utc).isoformat(timespec='minutes')} UTC. Tenant `{TENANT}`, corpus {len(files)} files "
         f"(README, AGENTS files, docs/, eval reports, demo script, Claude Code integration README, knowledge/ without references/). "
         f"Gold: `eval/real_gold.jsonl`, {len(rows)} questions and {len(ent)} entity and {len(rel)} relation checks. "
         f"Settings: {meta}.", "",
         "Matching: `AnswerIn` is a whole-word, case- and punctuation-insensitive containment of the gold answer string. "
         "`out5` = `tools.recall(k=5)` text (each item is cut to 240 chars); `chunk5` = full chunk text of the top-5 documents; "
         "`ask` = `tools.ask` output. Rank = first gold document among unique documents of `recall(k=20)` (none = not in the top 20).", ""]
    if ingest_stats:
        L += [f"Ingest: {ingest_stats}", ""]
    L += ["## a. RAG", "", "### Summary (overall and per type)", ""]
    cols = ["group", "n", "Hit@1", "Hit@5", "MRR", "AnswerIn@5 out5", "AnswerIn chunk5", "AnswerIn ask"]
    lines = []
    for name, sub in [("overall", rows)] + [(t, [r for r in rows if r["type"] == t]) for t in QTYPES]:
        a = agg(sub)
        lines.append([name, a["n"], f"{a['hit@1']:.2f}", f"{a['hit@5']:.2f}", f"{a['mrr']:.2f}", f"{a['out5']:.2f}", f"{a['chunk5']:.2f}", f"{a['ask']:.2f}"])
    L += [table(cols, lines), ""]
    L += ["### Latency (ms)", "", table(["call", "p50", "p95", "mean"],
          [["recall k=20", f"{statistics.median([r['ms_recall'] for r in rows]):.0f}", f"{pct([r['ms_recall'] for r in rows], .95):.0f}",
            f"{statistics.mean([r['ms_recall'] for r in rows]):.0f}"],
           ["ask", f"{statistics.median([r['ms_ask'] for r in rows]):.0f}", f"{pct([r['ms_ask'] for r in rows], .95):.0f}",
            f"{statistics.mean([r['ms_ask'] for r in rows]):.0f}"]]), ""]
    L += ["### Per question", "", table(["id", "type", "rank", "out5", "chunk5", "ask", "ms recall", "ms ask", "gold", "question"],
          [[r["id"], r["type"], r["rank"] or "none", r["out5"], r["chunk5"], r["ask"], f"{r['ms_recall']:.0f}", f"{r['ms_ask']:.0f}",
            ", ".join(r["gold"]), r["question"]] for r in rows]), ""]
    worst = sorted(rows, key=lambda r: (-(r["rank"] or 99), r["out5"] + r["chunk5"]))[:5]
    L += ["### Five worst questions: which documents beat the gold one", ""]
    for r in worst:
        beats = "; ".join(f"`{d}` via {', '.join(f'{c}#{k}' for c, k in ch.items()) or '-'}" for d, ch in r["above"]) or "(none above it)"
        L.append(f"- **{r['id']}** ({r['type']}, rank {r['rank'] or 'none'}, answer `{r['answer']}`): {r['question']} "
                 f"Gold `{', '.join(r['gold'])}`. Above it: {beats}.")
    L += [""]
    L += ["## b. Graph health", "", "### Counts", "",
          f"- Documents by kind: {dict(G['docs_kind'])}",
          f"- Documents by doc_type (frontmatter `type`): {dict(G['docs_doc_type'])}",
          f"- Chunks: {G['chunks']}; MENTIONS: {G['mentions']}; Entities: {G['entities']}",
          f"- Entities by type: {dict(G['entities_by_type'])}",
          f"- REL edges by type: {dict(G['rels_by_type'])}", "",
          f"- Single-word entity names: {G['single_word']}; generic single words (`is_generic`): {len(G['generic'])}: "
          f"{', '.join(G['generic'][:40]) or '(none)'}",
          f"- Entities typed `file`: {len(G['file_entities'])}: {', '.join(G['file_entities'][:40]) or '(none)'}", "",
          "### Name variants per stem (10 biggest groups)", "",
          "A stem is each letter run of 4+ and the letters-only key; a group is every entity key that contains the stem.", ""]
    L += [table(["stem", "variant keys", "examples (mentions)"],
                [[s, len(keys), ", ".join(f"{k} ({m})" for k, m in sorted(keys.items(), key=lambda kv: -kv[1])[:6])] for s, keys in G["variant_groups"]]), ""]
    L += ["### Entity checks", "", table(["id", "entity", "expected types", "found (name, type, mentions)", "pass"],
          [[e["id"], e["entity"], "/".join(e["expected"]), "; ".join(f"{n} ({t}, {m})" for n, t, m in e["found"]) or
            ("near: " + "; ".join(f"{n} ({t})" for n, t in e["near"]) if e["near"] else "not found"), "PASS" if e["pass"] else "FAIL"] for e in ent]), ""]
    L += ["### Relation checks", "", table(["id", "head -REL->tail", "edge found", "reversed", "head/tail in graph", "other REL edges from head"],
          [[r["id"], f"{r['head']} -{r['rel']}-> {r['tail']}", "PASS" if r["pass"] else "FAIL", "yes" if r["reversed"] else "no",
            f"{'yes' if r['head_found'] else 'no'} / {'yes' if r['tail_found'] else 'no'}",
            "; ".join(f"{t} -> {n}" for t, n in r["head_edges"]) or "-"] for r in rel]), ""]
    L += ["### Random REL edges for human judgement (random seed 0)", ""]
    for i, (e, text, path) in enumerate(G["sample_edges"], 1):
        L.append(f"{i}. `{e[0]}` -{e[1]}-> `{e[2]}` (conf {e[4]}, chunk `{e[3]}` in `{path}`): \"{' '.join((text or '').split())[:160]}\"")
    L += ["", "## Corpus files", ""] + [f"- `{f.relative_to(ROOT).as_posix()}`" for f in files]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ingest", action="store_true", help="wipe tenant 'real' and ingest the real corpus first")
    ap.add_argument("--out", default=str(ROOT / "eval" / "real_check.md"))
    a = ap.parse_args()
    missing = [k for k in ("NEO_HOME", "NEO_PORT") if k not in os.environ]
    if missing:
        sys.exit(f"set {' and '.join(missing)} (scratch home and port; never the default ~/.neo-cortex)")
    from neo_cortex.store import Store
    gold = load_gold()
    files = real_files()
    qs = [q for q in gold if "question" in q]
    ent = [q for q in gold if q["type"] == "entity"]
    rel = [q for q in gold if q["type"] == "relation"]
    print(f"gold: {len(qs)} questions {dict(Counter(q['type'] for q in qs))}, {len(ent)} entity, {len(rel)} relation checks; {len(files)} corpus files", flush=True)
    meta = f"NEO_HOME={os.environ['NEO_HOME']} NEO_PORT={os.environ['NEO_PORT']} NEO_DEVICE={os.environ.get('NEO_DEVICE', 'auto')}"
    with Store() as store:
        stats = ingest(store, files) if a.ingest else None
        print("ingest:", stats, flush=True)
        docs = doc_paths(store)
        rows = rag(store, qs, docs)
        G, normalize_key = graph_health(store, docs)
        ent_rows = entity_checks(store, ent, normalize_key)
        rel_rows = relation_checks(store, rel, normalize_key)
    md = render(meta, stats, rows, G, ent_rows, rel_rows, files)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    o = agg(rows)
    print(f"RAG overall n={o['n']} Hit@1 {o['hit@1']:.2f} Hit@5 {o['hit@5']:.2f} MRR {o['mrr']:.2f} AnswerIn@5 out5 {o['out5']:.2f} "
          f"chunk5 {o['chunk5']:.2f} ask {o['ask']:.2f}")
    print(f"entity checks {sum(e['pass'] for e in ent_rows)}/{len(ent_rows)}, relation checks {sum(r['pass'] for r in rel_rows)}/{len(rel_rows)}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
