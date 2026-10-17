"""Retrieval channels. Each returns [(node_id, score)] over Chunk/Memory nodes, best first (higher is better)."""
import difflib
import math
import re
import threading
from dataclasses import dataclass

import bm25s
import numpy as np
import Stemmer

from .. import models
from ..util import normalize_key

N = 50  # candidates per channel
_STOP = set("a an the of to in on at for and or is are was were be been do does did what which who whom whose when where why how "
            "with by from as that this these those it its i we you they he she our your their my me us about has have had not "
            "can could should would will than then there into over any all".split())


@dataclass
class Filt:
    since: int | None = None
    until: int | None = None  # exclusive
    kinds: tuple | None = None
    superseded: bool = False


key_of = normalize_key  # must match the write path's Entity.key


def meta(store, ids, tenant):
    """id -> (label, kind, date_ms, status) for Chunk/Memory; ids=None means all. Memory date = valid_from, else created."""
    cy = ("MATCH (n) WHERE (n:Chunk OR n:Memory)" + ("" if ids is None else " AND n.id IN $ids") +
          " RETURN n.id, labels(n)[0], n.kind, coalesce(n.date_ms, n.valid_from_ms, n.created_ms), n.status")
    return {r[0]: tuple(r[1:]) for r in store.query(cy, None if ids is None else {"ids": list(ids)}, tenant)}


def keep(store, ranked, f: Filt, tenant, m=None):
    m = m or meta(store, [i for i, _ in ranked], tenant)
    out = []
    for i, s in ranked:
        if i not in m:
            continue
        label, kind, d, status = m[i]
        if status == "merged" or (status == "superseded" and not f.superseded):  # merged: dream's duplicate, never shown
            continue
        if f.kinds and kind not in f.kinds and label.lower() not in f.kinds:
            continue
        if (f.since is not None or f.until is not None) and d is None:
            continue
        if (f.since is not None and d < f.since) or (f.until is not None and d >= f.until):
            continue
        out.append((i, s))
    return out


def vector(store, q: str, f: Filt, tenant=None, n=N):
    e = models.embed_query(q).tolist()
    rows = []
    for label in ("Chunk", "Memory"):
        rows += store.query(f"CALL db.idx.vector.queryNodes('{label}','emb',{n},vecf32($v)) YIELD node, score RETURN node.id, score",
                            {"v": e}, tenant)
    rows.sort(key=lambda r: r[1])  # score is a distance
    return keep(store, [(i, 1 - d) for i, d in rows[:n]], f, tenant)


# --- BM25 -------------------------------------------------------------------------------------------------------
_lock = threading.Lock()
_stem = None


def _tok(texts, ids=False):
    global _stem
    _stem = _stem or Stemmer.Stemmer("english")
    # split identifiers (SESSION_TTL, config/ci.yaml) so a query word can hit them
    return bm25s.tokenize([re.sub(r"[_\-./:\\]+", " ", t) for t in texts], stopwords="en", stemmer=_stem,
                          return_ids=ids, show_progress=False)


def _bm25_index(store, tenant):
    cache = store.__dict__.setdefault("_bm25", {})
    t = tenant or store.default_tenant
    sig = store.query("MATCH (n) WHERE n:Chunk OR n:Memory RETURN count(n), sum(size(n.text)), max(coalesce(n.date_ms, n.created_ms, 0))", None, tenant)[0]
    with _lock:
        c = cache.get(t)
        if c is None or c[0] != sig:
            # shortcut: full rebuild whenever count/text-size/max-date changes (O(corpus)); fine to ~10k chunks,
            # switch to incremental indexing or a persisted index beyond that
            rows = [r for r in store.query("MATCH (n) WHERE n:Chunk OR n:Memory RETURN n.id, n.text", None, tenant) if r[1]]
            r = None
            if rows:
                r = bm25s.BM25()
                r.index(_tok([x[1] for x in rows], ids=True), show_progress=False)
            cache[t] = c = (sig, [x[0] for x in rows], r)
        return c


def bm25(store, q: str, f: Filt, tenant=None, n=N):
    _, ids, r = _bm25_index(store, tenant)
    if r is None:
        return []
    docs, scores = r.retrieve(_tok([q]), k=min(len(ids), 4 * n), show_progress=False)
    ranked = [(ids[d], float(s)) for d, s in zip(docs[0], scores[0]) if s > 0]
    return keep(store, ranked, f, tenant)[:n]


# --- graph ------------------------------------------------------------------------------------------------------
# Query words that name a role or a kind of thing, never one specific entity: such phrases are not linked fuzzily.
_GENERIC = set("engineer developer manager executive owner reviewer person people team group service system component incident outage "
               "failure issue change edit config configuration setting feature code path flow store tool company customer user "
               "thing bug error problem rule decision file module library project work month year week day".split())
ALPHA, BETA, LAMBDA = 0.5, 0.5, 0.5  # PPR restart prob.; share of an entity's mass sent along REL; weight of anchor seeds
SPEC_POW = 2.0  # idf-like weight squared: hub entities (people on every ticket) must not carry mass
HOPS, MAX_NODES, PER_ENT, SEEDS, REL_LIMIT = 3, 500, 25, 5, 1000  # REL_LIMIT: strongest neighbour edges read per hop


def _content(name):
    """Content tokens of a phrase: lowercase, no stop/generic words, plural 's' stripped."""
    out = []
    for t in key_of(name).split():
        t = t[:-1] if len(t) > 3 and t.endswith("s") else t
        if t not in _STOP and t not in _GENERIC and (len(t) >= 3 or t.isdigit()):
            out.append(t)
    return out


def _spec(m):
    """Entity specificity (idf-like): entities named in many chunks say little about any one of them."""
    return (1 / math.log(1 + max(m or 1, 1))) ** SPEC_POW


SEED_FLOOR = 0.2  # the graph channel stays off when its best linked seed scores below this (conf x idf)


def _idf(m, n):
    """Corpus-relative rarity in (0, 1]: 1 for an entity named in one node of n, about 0.4 for one in 40 of 370."""
    return math.log(1 + n / max(m or 1, 1)) / math.log(1 + n)


def link_entities(store, ents, q, tenant=None, cap=SEEDS) -> dict:
    """Query entities -> {entity_id: (name, conf)}, at most `cap`. Exact key (GLiNER entity 1.0, query n-gram 0.7), fuzzy
    full-text on Entity.name (0.8 x similarity), a rare content word shared with an entity name (0.35-0.5), else the nearest
    Entity.emb (0.6) when it is very close (>= 0.9) or close (>= 0.8) and shares a content word. Generic phrases ("the
    executive", "configuration edit") only link by exact key."""
    rows = store.query("MATCH (e:Entity) RETURN e.id, e.key, e.name", None, tenant)  # shortcut: O(entities) per call, fine to ~10k
    bykey = {r[1]: r for r in rows}
    words = key_of(q).split()
    grams = {" ".join(words[i:i + n]) for n in (1, 2, 3) for i in range(len(words) - n + 1)}
    grams = {g for g in grams if len(g) >= 3 and not all(w in _STOP for w in g.split())}
    want = {key_of(e["name"]): 1.0 for e in ents}
    for g in grams:
        want.setdefault(g, 0.7)
    out, hit = {}, set()

    def put(eid, name, c):
        if c > out.get(eid, ("", 0))[1]:
            out[eid] = (name, c)

    for kk, c in want.items():
        if kk in bykey:
            hit.add(kk)
            put(bykey[kk][0], bykey[kk][2], c)
    toks = {}  # content word -> entities whose name has it
    for eid, ek, name in rows:
        for t in set(_content(ek or "")):
            toks.setdefault(t, []).append((eid, name, ek))
    for t in set(_content(q)):
        if 1 <= len(toks.get(t, [])) <= 2:
            for eid, name, ek in toks[t]:
                put(eid, name, 0.35 + 0.15 / max(len(_content(ek)), 1))
    for e in ents:
        k = key_of(e["name"])
        ct = set(_content(e["name"]))
        if k in hit or not k or not ct:
            continue
        ft = [t for t in k.split() if len(t) >= 3] or [k]
        for eid, name, ek in store.query("CALL db.idx.fulltext.queryNodes('Entity',$q) YIELD node RETURN node.id, node.name, node.key",
                                         {"q": "|".join(f"%{t}%" for t in ft)}, tenant):
            c = 0.8 * difflib.SequenceMatcher(None, k, ek or key_of(name)).ratio()
            if c >= 0.6:
                put(eid, name, c)
                hit.add(k)
        if k not in hit:
            v = models.embed_docs([e["name"]], [e["type"]])[0].tolist()
            for eid, name, d in store.query("CALL db.idx.vector.queryNodes('Entity','emb',3,vecf32($v)) YIELD node, score RETURN node.id, node.name, score",
                                            {"v": v}, tenant):
                if (1 - d >= 0.9) or (1 - d >= 0.8 and ct & set(_content(name))):
                    put(eid, name, 0.6)
    return dict(sorted(out.items(), key=lambda kv: -kv[1][1])[:cap])


def _render(trail):
    s = trail[0]
    for rel, fwd, name in trail[1:]:
        s += f" -[{rel}]-> {name}" if fwd else f" <-[{rel}]- {name}"
    return s


def ppr(store, qseeds, aseeds, tenant=None, now=None, current=True):
    """HippoRAG-style Personalized PageRank over the local Entity/Chunk/Memory graph around the seeds.
    qseeds/aseeds: {entity_id: weight} (query-linked; mentioned by the top dense/BM25 hits), scaled by specificity.
    Walk: entity -> REL neighbours (conf, undirected; BETA of its mass) or the chunks mentioning it (the rest, uniform);
    chunk -> its entities (conf x specificity). `current` skips REL edges already ended; every mode skips non-fact edges. Returns (mass {node_id: float},
    names {entity_id: name}, trail(node_id) -> [name, (rel, forward, name), ...] along a shortest hop path from a seed).
    numpy, not algo.pageRank: FalkorDB's PageRank has no personalization vector, and the subgraph is capped at MAX_NODES."""
    seeds = {**aseeds, **qseeds}
    ents = {r[0]: (r[1], r[2]) for r in store.query("MATCH (e:Entity) WHERE e.id IN $i RETURN e.id, e.name, e.mentions",
                                                    {"i": list(seeds)}, tenant)}
    seeds = {e: w for e, w in seeds.items() if e in ents}
    nb, ch_of, ent_of = {}, {}, {}  # entity -> {entity: [w, type, fwd]}, entity -> {chunk: conf}, chunk -> {entity: conf}
    front, done = set(ents), set()
    cond = "AND coalesce(r.modality,'fact')='fact' " + ("AND (r.valid_to_ms IS NULL OR r.valid_to_ms > $now)" if current else "")  # non-fact edges never walk
    new_c = set()  # chunks admitted this hop, counted before their entities are added
    room = lambda: MAX_NODES - len(ents) - len(ent_of) - len(new_c)  # noqa: E731  nodes still allowed; the matrix is this size squared
    for _ in range(HOPS):
        if not front or room() <= 0:
            break
        done |= front
        fe, new_c = set(), set()
        for a, b, bn, bm, t, c, st in store.query(
                f"MATCH (a:Entity)-[r:REL]-(b:Entity) WHERE a.id IN $ids {cond} RETURN a.id, b.id, b.name, b.mentions, r.type, "
                f"coalesce(r.conf, 0.5), startNode(r).id ORDER BY coalesce(r.conf, 0.5) DESC LIMIT {REL_LIMIT}",
                {"ids": list(front), "now": now or 0}, tenant):
            if b not in ents and room() <= 0:
                continue
            ents.setdefault(b, (bn, bm))
            cur = nb.setdefault(a, {}).get(b)
            nb[a][b] = [1 - (1 - (cur[0] if cur else 0)) * (1 - c), t if not cur or c > cur[0] else cur[1], st == a]  # corroborated
            fe.add(b)
        for n, e, mc in store.query(
                "MATCH (n)-[m:MENTIONS]->(e:Entity) WHERE e.id IN $ids AND (n:Chunk OR n:Memory) RETURN n.id, e.id, coalesce(m.conf, 1.0) "
                "ORDER BY m.conf DESC LIMIT 3000", {"ids": list(front)}, tenant):  # shortcut: hub entities keep their PER_ENT best chunks
            if len(ch_of.setdefault(e, {})) >= PER_ENT:
                continue
            if n not in ent_of and n not in new_c:
                if room() <= 0:
                    continue
                new_c.add(n)
            ch_of[e][n] = mc
        if new_c:
            for n, e, en, em, mc in store.query(
                    "MATCH (n)-[m:MENTIONS]->(e:Entity) WHERE n.id IN $ids RETURN n.id, e.id, e.name, e.mentions, coalesce(m.conf, 1.0)",
                    {"ids": list(new_c)}, tenant):
                if e not in ents:
                    if room() <= 0:  # the admitted chunks' slots are already reserved in room()
                        continue
                    ents[e] = (en, em)
                    fe.add(e)
                ent_of.setdefault(n, {})[e] = mc
        front = fe - done
    idx = {k: i for i, k in enumerate([*ents, *ent_of])}  # a chunk or edge that lost the node budget is dropped here
    P = np.zeros((len(idx), len(idx)))
    for e in ents:
        r_ = {b: v for b, v in nb.get(e, {}).items() if b in idx}
        m_ = {c: mc for c, mc in ch_of.get(e, {}).items() if c in idx}
        wr, wm = sum(v[0] for v in r_.values()), sum(m_.values())
        for b, v in r_.items():
            P[idx[e], idx[b]] += (BETA if wm else 1) * v[0] / wr
        for c, mc in m_.items():
            P[idx[e], idx[c]] += (1 - BETA if wr else 1) * mc / wm
    for c, m_ in ent_of.items():
        tot = sum(mc * _spec(ents[e][1]) for e, mc in m_.items())
        for e, mc in m_.items():
            P[idx[c], idx[e]] += mc * _spec(ents[e][1]) / tot

    def vec(sd):
        v = np.zeros(len(idx))
        for e, w in sd.items():
            if e in ents:
                v[idx[e]] += w * _spec(ents[e][1])
        return v / v.sum() if v.any() else v

    rq, ra = vec(qseeds), vec(aseeds)
    r = ra if not rq.any() else rq if not ra.any() else (1 - LAMBDA) * rq + LAMBDA * ra
    p = r.copy()
    for _ in range(40):
        q = (1 - ALPHA) * (p @ P)
        p = q + (1 - q.sum()) * r  # mass lost at dead ends restarts at the seeds
    mass = {k: float(p[i]) for k, i in idx.items()}
    # BFS parents over the same edges, seeds first by weight (ties go to the stronger seed)
    adj = {}
    for a, d in nb.items():
        for b, (_, t, fwd) in d.items():
            adj.setdefault(a, []).append((b, t, fwd))
    for e, d in ch_of.items():
        for c in d:
            adj.setdefault(e, []).append((c, "MENTIONS", False))
    for c, d in ent_of.items():
        for e in d:
            adj.setdefault(c, []).append((e, "MENTIONS", True))
    par = {s: None for s in sorted(seeds, key=lambda e: -seeds[e])}
    queue = list(par)
    for u in queue:
        for v, t, fwd in adj.get(u, []):
            if v not in par:
                par[v] = (u, t, fwd)
                queue.append(v)
    name = lambda k: ents[k][0] if k in ents else k  # noqa: E731

    def trail(k):
        out = []
        while par.get(k):
            u, t, fwd = par[k]
            out.append((t, fwd, name(k)))
            k = u
        return [name(k), *reversed(out)] if k in par else [name(k)]
    return mass, {e: v[0] for e, v in ents.items()}, trail


def graph(store, ents, q: str, f: Filt, tenant=None, n=N, paths: dict | None = None, anchors=(), now=None, current=True, info: dict | None = None):
    """Seeds (linked query entities, plus the entities mentioned by `anchors`, the top dense/BM25 hits, at lower weight)
    -> Personalized PageRank (see `ppr`) -> Chunks/Memories ranked by mass. `paths` is filled with
    {node_id: ["A -[OWNS]-> B <-[MENTIONS]- node"]}; `info` with {"seeds": {id: (name, conf)}, "entities": [(id, name, mass, trail)]}."""
    seeds = link_entities(store, ents, q, tenant)
    a = {}
    rank = {x: i for i, x in enumerate(anchors)}
    for nid, e, mc in store.query("MATCH (n)-[m:MENTIONS]->(e:Entity) WHERE n.id IN $ids RETURN n.id, e.id, coalesce(m.conf, 1.0)",
                                  {"ids": list(anchors)}, tenant) if anchors else []:
        a[e] = max(a.get(e, 0), mc / (1 + rank[nid]))
    seeds = {e: v for e, v in seeds.items() if v[1] >= 0.65 or e in a or not anchors}  # weak links need support from the retrieved hits
    if not seeds:  # anchors alone never start the walk: their entities are whatever the top hits happen to mention
        return []
    men = dict(store.query("MATCH (e:Entity) WHERE e.id IN $i RETURN e.id, e.mentions", {"i": list(seeds)}, tenant))
    nodes = store.query("MATCH (n) WHERE n:Chunk OR n:Memory RETURN count(n)", None, tenant)[0][0]
    strength = max(c * _idf(men.get(e), nodes) for e, (_, c) in seeds.items())  # hub or weakly linked seeds walk little
    if info is not None:
        info["strength"] = strength
    if strength < SEED_FLOOR:
        return []
    mass, names, trail = ppr(store, {e: c for e, (_, c) in seeds.items()}, a, tenant, now, current)
    m = meta(store, [k for k in mass if k not in names], tenant)
    ranked = keep(store, sorted(((k, v) for k, v in mass.items() if k in m), key=lambda kv: -kv[1])[:n * 2], f, tenant, m)[:n]
    if paths is not None:
        for k, _ in ranked:
            paths[k] = [_render(trail(k))]
    if info is not None:
        info["seeds"] = seeds
        info["entities"] = [(e, names[e], v, _render(trail(e)) if len(trail(e)) > 1 else "named by a top hit")
                            for e, v in sorted(((e, mass[e]) for e in names if e not in seeds), key=lambda kv: -kv[1])[:10]]
    return ranked


# --- temporal ---------------------------------------------------------------------------------------------------
CHANGE_RE = re.compile(r"\b(chang\w*|histor\w*|timeline|over time|evol\w*|when|before|origin\w*|first|previous\w*|used to)\b", re.I)
RECENT_RE = re.compile(r"\b(current\w*|latest|now|recent\w*|newest|today|yesterday|last|this week)\b", re.I)


def temporal(store, f: Filt, tenant=None, pool=None, asc=False, n=N):
    """Rank by date inside the window: newest first (current/latest questions) or oldest first (what changed).
    `pool` restricts to candidate ids from the other channels; without it every node in the window is ranked."""
    m = meta(store, None if pool is None else list(pool), tenant)
    ranked = keep(store, [(i, v[2] or 0) for i, v in m.items()], f, tenant, m)
    ranked.sort(key=lambda x: (x[1], x[0]) if asc else (-x[1], x[0]))
    return ranked[:n]  # shortcut: pool=None scans every Chunk/Memory; fine to ~10k nodes
