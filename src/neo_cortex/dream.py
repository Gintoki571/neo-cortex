"""`neo dream`: deterministic memory consolidation. No LLM; the rules and thresholds live here.

Planning reads the graph once and works on a Python copy, so `dry_run` reports exactly what a real run writes.
Writes are batched UNWIND statements. A second run right after a first one changes no Memory or edge."""
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations

import numpy as np

from . import util
from . import write as W

PROMOTE_SIM = 0.80            # episodic cluster radius (merge uses write.DEDUPE, conflicts use write.CONFLICT)
PROMOTE_SESSIONS = 3
PROMOTE_CAP = 0.95
DECAY_PERIOD_MS = 30 * 86_400_000
DECAY_FACTOR, DECAY_FLOOR = 0.9, 0.1
EXEMPT_KINDS = {"preference", "decision"}   # never decay
CONFLICT_KINDS = {"semantic", "decision"}


@dataclass
class M:
    id: str
    kind: str
    status: str
    text: str
    conf: float
    created: int
    uses: int
    last_used: int
    decayed: int | None
    emb: np.ndarray
    ents: dict = field(default_factory=dict)      # entity id -> MENTIONS conf
    srcs: set = field(default_factory=set)        # DERIVED_FROM targets (Chunk, Session or Memory)
    sessions: set = field(default_factory=set)    # DERIVED_FROM targets that are Sessions
    derived_by: set = field(default_factory=set)  # Memories that DERIVED_FROM this one


def _cos(a, b) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def _load(store, tenant):
    q = lambda c: store.query(c, {}, tenant)  # noqa: E731
    sids = {r[0] for r in q("MATCH (s:Session) RETURN s.id")}
    mems = {r[0]: M(r[0], r[1], r[2], r[3], r[4] or 0.0, r[5] or 0, r[6] or 0, r[7] or 0, r[8],
                    np.asarray(r[9], dtype=np.float32))
            for r in q("MATCH (m:Memory) RETURN m.id, m.kind, m.status, m.text, m.confidence, m.created_ms, m.uses, "
                       "m.last_used_ms, m.decayed_ms, m.emb")}
    for mid, eid, conf in q("MATCH (m:Memory)-[x:MENTIONS]->(e:Entity) RETURN m.id, e.id, x.conf"):
        mems[mid].ents[eid] = conf
    for mid, tid in q("MATCH (m:Memory)-[:DERIVED_FROM]->(t) RETURN m.id, t.id"):
        mems[mid].srcs.add(tid)
        if tid in sids:
            mems[mid].sessions.add(tid)
    for sid, mid in q("MATCH (s:Memory)-[:DERIVED_FROM]->(m:Memory) RETURN s.id, m.id"):
        mems[mid].derived_by.add(sid)
    existing = {(r[0], r[1]) for r in q("MATCH (a:Memory)-[:CONFLICTS_WITH]->(b:Memory) RETURN a.id, b.id")}
    return mems, existing


def _neighbours(store, mems, tenant):
    """id -> [(other id, cosine)] over every Memory.
    shortcut: exact top-N per memory with N = all Memory nodes, O(N^2) index reads; batch the queries when N grows."""
    out = {}
    for m in mems.values():
        rows = store.query("CALL db.idx.vector.queryNodes('Memory','emb',$k,vecf32($e)) YIELD node, score "
                           "RETURN node.id, score", {"k": len(mems), "e": W._vec(m.emb)}, tenant)
        out[m.id] = [(i, 1 - s) for i, s in rows if i != m.id]  # the index score is a distance
    return out


def _plan_merge(mems, nb):
    """Oldest active memory of a same-kind group (cosine >= DEDUPE) is canonical; the rest merge into it,
    unless the two differ in a number or negation (write._differ): that is a new fact, not a duplicate."""
    order = sorted((m for m in mems.values() if m.status == "active"), key=lambda m: (m.created, m.id))
    merged: dict[str, str] = {}   # duplicate id -> canonical id
    for m in order:
        if m.id in merged:
            continue
        for nid, sim in nb[m.id]:
            n = mems[nid]
            if (sim >= W.DEDUPE and n.status == "active" and n.kind == m.kind and nid not in merged
                    and (n.created, n.id) > (m.created, m.id) and not W._differ(m.text, n.text)):
                merged[nid] = m.id
    uses_add: dict[str, int] = defaultdict(int)
    ent_new, src_new, ent_touch = [], [], set()
    for dup_id, can_id in merged.items():
        d, c = mems[dup_id], mems[can_id]
        d.status = "merged"
        c.uses += d.uses
        uses_add[can_id] += d.uses
        c.derived_by |= d.derived_by
        c.sessions |= d.sessions
        ent_touch |= set(d.ents)
        for e, conf in d.ents.items():
            if e not in c.ents:
                c.ents[e] = conf
                ent_new.append((can_id, e, conf))
        for t in d.srcs - c.srcs:
            c.srcs.add(t)
            src_new.append((can_id, t))
    return merged, uses_add, ent_new, src_new, ent_touch


def _plan_promote(mems, nb, now):
    """Episodic clusters (cosine >= PROMOTE_SIM around a seed) seen in >= PROMOTE_SESSIONS sessions become one semantic memory."""
    cand = {m.id for m in mems.values() if m.status == "active" and m.kind == "episodic"}
    order = sorted((mems[i] for i in cand), key=lambda m: (m.created, m.id))
    sem = [m for m in mems.values() if m.status == "active" and m.kind == "semantic"]
    claimed, out = set(), []
    for seed in order:
        if seed.id in claimed:
            continue
        ids = [seed.id] + [i for i, sim in nb[seed.id] if sim >= PROMOTE_SIM and i in cand and i not in claimed]
        members = [mems[i] for i in ids]
        n = len({s for x in members for s in x.sessions})
        if n < PROMOTE_SESSIONS or any(x.derived_by for x in members):  # too few sessions, or already promoted
            continue
        best = max(members, key=lambda x: (x.uses, -x.created, x.id))
        if any(_cos(s.emb, best.emb) >= W.DEDUPE for s in sem):         # would duplicate an existing semantic memory
            continue
        new = M(util.new_id("mem"), "semantic", "active", best.text, min(PROMOTE_CAP, 0.5 + 0.1 * n), now, 0, now, None,
                best.emb, ents={e: 1.0 for x in members for e in x.ents}, srcs=set(ids))
        sem.append(new)
        claimed |= set(ids)
        out.append((new, ids))
    return out


def _plan_decay(mems, now):
    """(memory, new confidence, new decayed_ms) for active memories unused for whole 30-day periods."""
    rows = []
    for m in mems.values():
        if m.status != "active" or m.kind in EXEMPT_KINDS:
            continue
        anchor = max(m.last_used, m.decayed or 0)
        periods = (now - anchor) // DECAY_PERIOD_MS
        if periods < 1:
            continue
        conf = min(m.conf, max(DECAY_FLOOR, m.conf * DECAY_FACTOR ** periods))  # never raised, never below the floor
        rows.append((m, conf, anchor + periods * DECAY_PERIOD_MS))
    return rows


def _plan_conflicts(mems, existing):
    """Pairs of active semantic/decision memories sharing an entity that differ in a number or negation and have
    cosine >= CONFLICT (a near-duplicate that differs is a conflict, not a merge)."""
    pool = [m for m in mems.values() if m.status == "active" and m.kind in CONFLICT_KINDS]
    by_ent = defaultdict(list)
    for m in pool:
        for e in m.ents:
            by_ent[e].append(m)
    seen, out = set(), []
    for group in by_ent.values():
        for a, b in combinations(sorted(group, key=lambda m: m.id), 2):
            key = (a.id, b.id)
            if key in seen or key in existing or (b.id, a.id) in existing:
                continue
            seen.add(key)
            if _cos(a.emb, b.emb) >= W.CONFLICT and W._differ(a.text, b.text):
                out.append(key)
    return out


def _write(store, tenant, now, plan):
    merged, uses_add, ent_new, src_new, ent_touch, promos, decays, conflicts = plan
    q = lambda c, rows: store.query(c, {"rows": rows}, tenant)  # noqa: E731
    if merged:
        q("UNWIND $rows AS r MATCH (d:Memory {id:r.d}), (c:Memory {id:r.c}) SET d.status='merged' "
          "CREATE (d)-[:MERGED_INTO]->(c)", [{"d": d, "c": c} for d, c in merged.items()])
        q("UNWIND $rows AS r MATCH (c:Memory {id:r.c}) SET c.uses = c.uses + r.n",
          [{"c": c, "n": n} for c, n in uses_add.items()])
        q("UNWIND $rows AS r MATCH (c:Memory {id:r.c}), (e:Entity {id:r.e}) CREATE (c)-[:MENTIONS {conf:r.conf}]->(e)",
          [{"c": c, "e": e, "conf": v} for c, e, v in ent_new])
        q("UNWIND $rows AS r MATCH (d:Memory {id:r})-[x:MENTIONS]->() DELETE x", list(merged))
        q("UNWIND $rows AS r MATCH (c:Memory {id:r.c}), (t {id:r.t}) CREATE (c)-[:DERIVED_FROM]->(t)",
          [{"c": c, "t": t} for c, t in src_new])
        q("UNWIND $rows AS r MATCH (d:Memory {id:r})-[x:DERIVED_FROM]->() DELETE x", list(merged))
    for new, members in promos:
        store.query("CREATE (:Memory {id:$id, text:$text, kind:'semantic', confidence:$conf, created_ms:$t, "
                    "valid_from_ms:$t, status:'active', uses:0, last_used_ms:$t, emb:vecf32($e)})",
                    {"id": new.id, "text": new.text, "conf": new.conf, "t": now, "e": W._vec(new.emb)}, tenant)
        q("UNWIND $rows AS r MATCH (c:Memory {id:r.c}), (e:Entity {id:r.e}) CREATE (c)-[:MENTIONS {conf:r.conf}]->(e)",
          [{"c": new.id, "e": e, "conf": 1.0} for e in new.ents])
        q("UNWIND $rows AS r MATCH (s:Memory {id:r.s}), (m:Memory {id:r.m}) CREATE (s)-[:DERIVED_FROM]->(m)",
          [{"s": new.id, "m": m} for m in members])
    if decays:
        q("UNWIND $rows AS r MATCH (m:Memory {id:r.id}) SET m.confidence=r.conf, m.decayed_ms=r.d",
          [{"id": m.id, "conf": c, "d": d} for m, c, d in decays])
    if conflicts:
        store.query("UNWIND $rows AS r MATCH (a:Memory {id:r.a}), (b:Memory {id:r.b}) "
                    "CREATE (a)-[:CONFLICTS_WITH {found_ms:$t}]->(b)",
                    {"rows": [{"a": a, "b": b} for a, b in conflicts], "t": now}, tenant)
    W._refresh_entities(store, sorted(ent_touch | {e for _, e, _ in ent_new} | {e for n, _ in promos for e in n.ents}),
                        tenant)


def dream(store, tenant=None, now_ms=None, dry_run=False) -> dict:
    with store.write_lock:  # plan from one snapshot and write before any other writer runs
        now = util.now_ms() if now_ms is None else now_ms
        mems, existing = _load(store, tenant)
        nb = _neighbours(store, mems, tenant) if mems else {}
        merged, uses_add, ent_new, src_new, ent_touch = _plan_merge(mems, nb)
        promos = _plan_promote(mems, nb, now)
        decays = _plan_decay(mems, now)
        conflicts = _plan_conflicts(mems, existing)
        counts = {"merged": len(merged), "promoted": len(promos),
                  "decayed": sum(1 for m, c, _ in decays if c < m.conf), "conflicts": len(conflicts)}
        run_id = None if dry_run else util.new_id("dream")
        if not dry_run:
            plan = (merged, uses_add, ent_new, src_new, ent_touch, promos, decays, conflicts)
            _write(store, tenant, now, plan)
            store.query("CREATE (:DreamRun {id:$id, at_ms:$t, merged:$merged, promoted:$promoted, decayed:$decayed, "
                        "conflicts:$conflicts})", {"id": run_id, "t": now, **counts}, tenant)
        return {"id": run_id, "at_ms": now, "dry_run": dry_run, **counts}
