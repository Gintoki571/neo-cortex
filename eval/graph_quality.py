"""Graph-quality yardstick: REL edges of an ingested graph vs the ground-truth edges in data/synthetic/WORLD.md.

    NEO_HOME=.neo/gq NEO_PORT=6374 NEO_DEVICE=cuda uv run --no-sync python eval/graph_quality.py [--ingest] [--tenant eval] [--show 40]

--ingest wipes the tenant and ingests the synthetic corpus first (same order as run_eval.py); without it the existing graph is
scored. Names are compared by util.normalize_key; the old name bankbridge counts as bank-connector everywhere except in the
RENAMED_TO truth edge itself. WORLD.md is the answer key: only this script reads it, never the product.

Graded types: OWNS (person -> service; team -> service edges that match the Team column are accepted but neither required nor counted), MEMBER_OF, DEPENDS_ON, RENAMED_TO, DECIDED, APPROVED. Other REL types are only
counted (their truth is not fully listed in WORLD.md). CAUSED_BY is scored for recall against a short list of root causes.
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("NEO_HOME", str(ROOT / ".neo" / "gq"))
os.environ.setdefault("NEO_PORT", "6374")
sys.path.insert(0, str(ROOT / "src"))
from neo_cortex.util import normalize_key as nk  # noqa: E402

WORLD = ROOT / "data" / "synthetic" / "WORLD.md"
ALIAS = {"bankbridge": "bank-connector"}
GRADED = ["OWNS", "MEMBER_OF", "DEPENDS_ON", "RENAMED_TO", "DECIDED", "APPROVED"]
# root causes stated in WORLD.md F061, F076, F082, F086-F088 (free text there, so listed by hand): incident -> causes
CAUSED_BY = [("INC-01", "session-cache"), ("INC-02", "config-service"), ("INC-03", "CFG-4411"), ("INC-04", "ledger-service"),
             ("INC-04", "event-pipeline")]


def canon(name: str, rename=False) -> str:
    k = nk(name)
    return k if rename else nk(ALIAS.get(k.replace(" ", "-"), k))


def _ms(s: str) -> int:
    return int(datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp() * 1000)


def _cells(line: str) -> list[str]:
    return [c.strip(" `*") for c in line.strip().strip("|").split("|")]


def _table(text: str, start: str) -> list[list[str]]:
    """Rows (cells) of the first markdown table after the heading that starts with `start`."""
    after = text[text.index(start):].splitlines()[1:]
    rows = [_cells(l) for l in after if l.startswith("|")]
    # stop at the first non-table line after the table began
    out, began = [], False
    for l in after:
        if l.startswith("|"):
            began = True
            out.append(_cells(l))
        elif began:
            break
    return [r for r in out[2:]] if rows else []


def truth(text: str | None = None) -> dict[str, set[tuple]]:
    """type -> set of (head, tail[, extra]) normalised tuples. OWNS tuples are (head, tail, current?)."""
    text = text or WORLD.read_text()
    t: dict[str, set] = defaultdict(set)
    people = {r[0]: r[2] for r in _table(text, "## 3. People")}
    for p, team in people.items():
        t["MEMBER_OF"].add((canon(p), canon(team)))
    for svc, team, owner, _ in _table(text, "## 4. Services"):
        svc = re.sub(r"\s*\(.*", "", svc)
        if "until" in owner:  # session-cache: "Lukas Brandt until 2026-08-31, Mateo Alvarez from 2026-09-01"
            old, new = re.match(r"(.+?) until", owner).group(1), re.search(r",\s*(.+?) from", owner).group(1)
            t["OWNS"] |= {(canon(old), canon(svc), False), (canon(new), canon(svc), True)}
            t["OWNS_TEAM"] |= {(canon("Identity"), canon(svc)), (canon("Platform"), canon(svc))}
        else:
            t["OWNS"].add((canon(owner), canon(svc), True))
            t["OWNS_TEAM"].add((canon(team), canon(svc)))
    sec = text[text.index("Edges (`A -> B`"):]
    for line in sec.split("\n", 1)[0].split(";"):
        for m in re.finditer(r"([a-z-]+)->([a-z-]+(?:, [a-z-]+)*)", line):
            for b in m.group(2).split(", "):
                t["DEPENDS_ON"].add((canon(m.group(1)), canon(b)))
    t["RENAMED_TO"].add((canon("bankbridge", True), canon("bank-connector", True)))
    for m in re.finditer(r"\*\*F\d+\*\* (ADR-\d+) was ([^\n]*)", text):
        adr = nk(m.group(1))
        parts = re.split(r"\b(proposed|decided|approved) by\b", m.group(2))
        for verb, chunk in zip(parts[1::2], parts[2::2]):
            if verb == "proposed":
                continue
            for n in re.split(r",| and ", re.sub(r"(?:[,.\s]|\band)+$", "", chunk.split(";")[0])):
                n = n.strip()
                if n in people:
                    t["DECIDED" if verb == "decided" else "APPROVED"].add((canon(n), adr))
    return t


def graph_edges(store, tenant) -> list[dict]:
    rows = store.query("MATCH (a:Entity)-[r:REL]->(b:Entity) RETURN a.key, a.type, r.type, b.key, b.type, r.conf, "
                       "r.valid_from_ms, r.valid_to_ms, r.source_id", tenant=tenant)
    return [dict(h=h, ht=ht, type=ty, t=t, tt=tt, conf=c, vf=vf, vt=vt, src=s) for h, ht, ty, t, tt, c, vf, vt, s in rows]


def score(edges: list[dict], tr: dict[str, set]) -> dict:
    res = {}
    for ty in GRADED:
        rn = ty == "RENAMED_TO"
        opt = {k[:2] for k in tr["OWNS_TEAM"]} if ty == "OWNS" else set()  # team ownership: accepted, not required
        pred = {(canon(e["h"], rn), canon(e["t"], rn)) for e in edges if e["type"] == ty} - opt
        want = {k[:2] for k in tr[ty]}
        cur = {k[:2] for k in tr[ty] if len(k) < 3 or k[2]}
        good = pred & want
        res[ty] = dict(truth=len(want), pred=len(pred), tp=len(good), wrong=sorted(pred - want), missing=sorted(want - pred),
                       precision=len(good) / len(pred) if pred else None, recall=len(good) / len(want),
                       cur_recall=len(good & cur) / len(cur) if ty == "OWNS" else None)
    return res


def caused_by_recall(edges) -> tuple[int, int]:
    pred = {(canon(e["h"]), canon(e["t"])) for e in edges if e["type"] == "CAUSED_BY"}
    want = {(nk(a), canon(b)) for a, b in CAUSED_BY}
    return len(pred & want), len(want)


def supersession_ok(edges, tr) -> list[str]:
    """session-cache: Lukas's OWNS edge must be closed, Mateo's open."""
    out = []
    for e in edges:
        if e["type"] == "OWNS" and canon(e["t"]) == "session cache" and e["ht"] == "person":
            if e["h"] == "lukas brandt" and e["vt"] is None:
                out.append("Lukas Brandt OWNS session-cache is still open")
            if e["h"] == "mateo alvarez" and e["vt"] is not None:
                out.append("Mateo Alvarez OWNS session-cache is closed")
    return out


def report(edges, show=40) -> dict:
    tr = truth()
    res = score(edges, tr)
    print(f"REL edges: {len(edges)}  ({len({(e['h'], e['type'], e['t']) for e in edges})} distinct)")
    print(f"{'type':<11}{'truth':>6}{'pred':>6}{'tp':>5}{'prec':>7}{'recall':>8}")
    tp = pred = 0
    for ty in GRADED:
        r = res[ty]
        f = lambda v: "  -  " if v is None else f"{v:.2f}"  # noqa: E731
        extra = f"  current-recall {r['cur_recall']:.2f}" if r["cur_recall"] is not None else ""
        print(f"{ty:<11}{r['truth']:>6}{r['pred']:>6}{r['tp']:>5}{f(r['precision']):>7}{f(r['recall']):>8}{extra}")
        tp += r["tp"]
        pred += r["pred"]
    print(f"overall graded precision {tp / max(pred, 1):.3f}  ({tp}/{pred}), recall {tp / sum(r['truth'] for r in res.values()):.3f}")
    a, b = caused_by_recall(edges)
    print(f"CAUSED_BY recall {a}/{b}")
    others = defaultdict(int)
    for e in edges:
        if e["type"] not in GRADED:
            others[e["type"]] += 1
    print("ungraded:", dict(others))
    for msg in supersession_ok(edges, tr):
        print("SUPERSESSION:", msg)
    for ty in GRADED:
        r = res[ty]
        if r["missing"]:
            print(f"\nMISSING {ty} ({len(r['missing'])}):", "; ".join(" -> ".join(m) for m in r["missing"][:show]))
        if r["wrong"]:
            print(f"WRONG {ty} ({len(r['wrong'])}):", "; ".join(" -> ".join(m) for m in r["wrong"][:show]))
    return res


def ingest(store, tenant):
    from neo_cortex.write import ingest_path
    store.query("MATCH (n) DETACH DELETE n", tenant=tenant)
    for kind in ["doc", "adr", "ticket", "chat", "meeting", "session"]:
        r = ingest_path(store, ROOT / "data" / "synthetic" / kind, tenant=tenant)
        print(kind, r, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ingest", action="store_true")
    ap.add_argument("--tenant", default="eval")
    ap.add_argument("--show", type=int, default=40)
    a = ap.parse_args()
    from neo_cortex.store import Store
    with Store() as store:
        if a.ingest:
            ingest(store, a.tenant)
        report(graph_edges(store, a.tenant), a.show)


if __name__ == "__main__":
    main()
