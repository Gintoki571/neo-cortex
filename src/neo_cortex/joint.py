"""Alternative GLiNER extraction paths, chosen by NEO_EXTRACT (read per call; `split` stays in extract.py):
- combined: one create_schema() with entities and relations, one batch_extract_long call over the sentence windows.
- joint: JointIE over the same windows; relation endpoints are REL_TYPES' head/tail sets, decoded greedily under those constraints.
Both map their output to the batch_extract_long shape and reuse the split path's post-processing, so extract_batch's output is the same.
"""
import os
import re
import sys

import torch

from . import extract as X
from .config import settings
from .models import gliner
from .util import normalize_key

MODES = ("split", "combined", "joint")
_THRESHOLD = 0.4  # the split path's GLiNER threshold for both entities and relations


def mode() -> str:
    m = os.environ.get("NEO_EXTRACT", "split")
    if m not in MODES:
        raise ValueError(f"NEO_EXTRACT must be one of {MODES}, not {m!r}")
    return m


def _run(m, texts, schema, bs):
    """batch_extract_long; a CUDA OOM retries one text at a time, as extract.extract_batch does."""
    kw = dict(threshold=_THRESHOLD, include_confidence=True, chunk_size=X.MAX_WORDS)
    try:
        return m.batch_extract_long(texts, schema, batch_size=bs, **kw)
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        return [m.batch_extract_long([t], schema, batch_size=1, **kw)[0] for t in texts]


def _combined(flat: list[str]) -> list[dict]:
    m = gliner()
    sch = m.create_schema().entities({k: d for k, (_, d) in X.ENTITY_LABELS.items()}).relations(
        {k: d for k, (_, d) in X.REL_LABELS.items()})
    return _run(m, flat, sch, 4)  # 16 ran the 6 GB card out of memory (GLiNER moved to CPU); 4 as the split entity pass


def _joint_schema():
    from gliner2.joint_ie import JointSchema
    label_of = {ct: lbl for lbl, (ct, _) in X.ENTITY_LABELS.items()}
    js = JointSchema().entities({k: d for k, (_, d) in X.ENTITY_LABELS.items()})
    for lbl, (rt, desc) in X.REL_LABELS.items():  # the endpoint sets are rel_ok's, mapped from contract types to GLiNER labels
        heads, tails = X.REL_TYPES[rt]
        js.relation(lbl, head=[label_of[t] for t in heads if t in label_of],
                    tail=[label_of[t] for t in tails if t in label_of], description=desc, threshold=_THRESHOLD)
    return js.no_self_loops()


def _raw(r) -> dict:
    """JointResult -> the batch_extract_long shape ("entities" by label, "relation_extraction" by label)."""
    ents, byid, rels = {}, {}, {}
    for e in r.entities:
        byid[e.id] = e
        ents.setdefault(e.type, []).append({"text": e.text, "confidence": e.confidence or 0.0})
    for rel in r.relations:
        h, t = byid.get(rel.head), byid.get(rel.tail)
        if h and t:
            rels.setdefault(rel.type, []).append({
                "head": {"text": h.text, "confidence": h.confidence or 0.0},
                "tail": {"text": t.text, "confidence": t.confidence or 0.0},
                "confidence": rel.confidence or 0.0})
    return {"entities": ents, "relation_extraction": rels}


def _joint(flat: list[str]) -> list[dict]:
    from gliner2.joint_ie import JointIE, JointIEConfig
    m = gliner()
    cfg = JointIEConfig(optimizer="greedy", candidate_threshold=0.05, relation_role_threshold=0.05,
                        entity_threshold=_THRESHOLD, include_confidence=True)
    eng = JointIE(m, device=settings().device)
    try:
        res = eng.batch_extract(flat, _joint_schema(), config=cfg)
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        res = [eng.batch_extract([t], _joint_schema(), config=cfg)[0] for t in flat]
    bad = sum(1 for r in res if not r.feasible)
    if bad:  # an infeasible window decodes to nothing, which is not the same as "no entities"
        print(f"neo: warning: {bad} of {len(res)} JointIE windows were infeasible under their constraints", file=sys.stderr)
    return [_raw(r) for r in res]


def extract_alt(texts, titles, authors, teams, kind: str, how: str) -> list[dict]:
    """extract_batch for NEO_EXTRACT=combined|joint: the same output shape and post-processing as the split path.
    shortcut: entities come only from the sentence windows (tables and lines under 3 words are left to _table_facts), upgrade if recall drops."""
    titles = titles or [""] * len(texts)
    authors = authors or [""] * len(texts)
    wins = [X._windows(t) for t in texts]
    flat = [w for ws, _ in wins for w in ws]
    raw = (_joint if how == "joint" else _combined)(flat) if flat else []
    per_text, i = [], 0
    for ws, _ in wins:  # a text's entities are the union over its windows
        ents: dict[str, list] = {}
        for r in raw[i:i + len(ws)]:
            for lbl, items in r["entities"].items():
                ents.setdefault(lbl, []).extend(items)
        per_text.append({"entities": ents})
        i += len(ws)
    known = set(teams or ()) | set().union(*(X.team_names(t) for t in texts))
    known |= {it["text"] for r in per_text for it in r["entities"].get("team", [])
              if it["confidence"] >= X.ENTITY_CONF["team"] and re.fullmatch(r"[A-Z][a-z]+", it["text"])} - X._NOT_TEAM
    ents = [X._entities(r, t, ti, a, known) for r, t, ti, a in zip(per_text, texts, titles, authors)]
    for e in ents:  # "Kofi" alone is a first name, whatever else the model made of it
        names = {w for k, x in e.items() if x["type"] == "person" for w in k.split()}
        for k in [k for k, x in e.items() if x["type"] == "team" and k in names]:
            del e[k]
    out, i = [], 0
    for e, (ws, sp), t, ti, a in zip(ents, wins, texts, titles, authors):
        rels = X._relations(e, ws, raw[i:i + len(ws)], ti, a, sp, kind=kind)
        i += len(ws)
        seen = {(normalize_key(r["head"]), r["type"], normalize_key(r["tail"])) for r in rels}
        for who, rt, thing, wt, tt in X._table_facts(t):
            if (normalize_key(who), rt, normalize_key(thing)) not in seen and X.rel_ok(rt, wt, tt):
                rels.append({"head": who, "type": rt, "tail": thing, "conf": 0.9})
        out.append({"entities": list(e.values()), "relations": rels})
    return out
