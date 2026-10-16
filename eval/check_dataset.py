#!/usr/bin/env python3
"""Consistency check for the synthetic dataset (stdlib only). Run: python3 eval/check_dataset.py"""
import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KINDS = {"doc", "adr", "ticket", "chat", "meeting", "session"}
TYPES = {"single": 12, "multi": 26, "temporal": 16, "ownership": 17, "procedural": 9}
errors, warns = [], []
err = errors.append

# WORLD facts; [T] facts must carry an ISO date
world = {}
for line in (ROOT / "data/synthetic/WORLD.md").read_text().splitlines():
    m = re.match(r"- \*\*(F\d{3})\*\*(.*)", line)
    if m:
        world[m[1]] = m[2]
        if "[T]" in m[2] and not re.search(r"\d{4}-\d{2}-\d{2}", m[2]):
            err(f"temporal fact {m[1]} has no date")

# manifest
docs = {}
for n, line in enumerate((ROOT / "data/synthetic/manifest.jsonl").read_text().splitlines(), 1):
    try:
        d = json.loads(line)
    except json.JSONDecodeError as e:
        err(f"manifest line {n}: invalid JSON ({e})"); continue
    for k in ("id", "kind", "path", "title", "date", "author", "participants", "facts", "brief"):
        if k not in d: err(f"manifest {d.get('id', n)}: missing {k}")
    if d.get("id") in docs: err(f"duplicate doc id {d['id']}")
    docs[d.get("id")] = d
    if d.get("kind") not in KINDS: err(f"{d['id']}: bad kind {d.get('kind')}")
    if d.get("path") != f"data/synthetic/{d.get('kind')}/{d.get('id')}.md": err(f"{d['id']}: path mismatch")
    if not re.fullmatch(r"2026-\d\d-\d\dT\d\d:\d\d:\d\dZ", d.get("date", "")): err(f"{d['id']}: bad date")
    if not ("2026-06-01" <= d.get("date", "")[:10] <= "2026-10-15"): err(f"{d['id']}: date outside window")
    if d.get("author") not in d.get("participants", []): err(f"{d['id']}: author not in participants")
    for f in d.get("facts", []):
        if f not in world: err(f"{d['id']}: unknown fact {f}")
    p = ROOT / d.get("path", "")
    if p.exists():  # written docs: frontmatter id/kind/date must match
        fm = p.read_text().split("---")[1] if p.read_text().startswith("---") else ""
        for k in ("id", "kind", "date"):
            if not re.search(rf"^{k}: *\"?{re.escape(str(d.get(k)))}\"?\s*$", fm, re.M): err(f"{d['id']}: frontmatter {k} mismatch")
used = {f for d in docs.values() for f in d.get("facts", [])}
for f in sorted(set(world) - used): warns.append(f"orphan fact (in no manifest doc): {f}")

# gold
qids, types = set(), Counter()
for n, line in enumerate((ROOT / "eval/gold.jsonl").read_text().splitlines(), 1):
    try:
        q = json.loads(line)
    except json.JSONDecodeError as e:
        err(f"gold line {n}: invalid JSON ({e})"); continue
    qid = q.get("id", f"line{n}")
    if qid in qids: err(f"duplicate question id {qid}")
    qids.add(qid); types[q.get("type")] += 1
    for k in ("type", "question", "answer", "gold_docs", "gold_entities", "facts", "hops"):
        if k not in q: err(f"{qid}: missing {k}")
    gd = q.get("gold_docs", [])
    for g in gd:
        if g not in docs: err(f"{qid}: gold doc {g} not in manifest")
    covered = set()
    for g in gd: covered |= set(docs.get(g, {}).get("facts", []))
    for f in q.get("facts", []):
        if f not in world: err(f"{qid}: unknown fact {f}")
        elif f not in used: err(f"{qid}: fact {f} appears in no manifest doc")
        elif f not in covered: err(f"{qid}: fact {f} not covered by its gold_docs")
    if q.get("type") in ("multi", "ownership"):
        ks = q.get("keys")  # short strings that must all appear in a retrieved text / `ask` output (the verbose `answer` rarely matches verbatim)
        if not (isinstance(ks, list) and ks and all(isinstance(k, str) and k.strip() for k in ks)): err(f"{qid}: needs non-empty `keys` list")
        if len(gd) < 2: err(f"{qid}: needs >=2 gold docs")
        for g, dd in docs.items():  # any doc in the corpus, not only gold ones
            if set(q.get("facts", [])) <= set(dd.get("facts", [])):
                err(f"{qid}: single doc {g} answers alone (graph channel would not be needed)")
        if len({docs[g]["kind"] for g in gd if g in docs}) < 2 and q["type"] == "multi":
            warns.append(f"{qid}: multi-hop gold docs are all of one kind")
for t, c in TYPES.items():
    if types[t] != c: err(f"type {t}: {types[t]} questions, expected {c}")

print("docs by kind:", dict(Counter(d["kind"] for d in docs.values())), "total", len(docs))
print("questions by type:", dict(types), "total", sum(types.values()))
print(f"facts: {len(world)} defined, {len(used)} used")
for w in warns: print("WARN", w)
for e in errors: print("ERROR", e)
print("OK" if not errors else f"FAILED ({len(errors)} errors)")
sys.exit(1 if errors else 0)
