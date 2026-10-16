"""Retrieval channels. Each returns [(node_id, score)] over Chunk/Memory nodes, best first (higher is better)."""
import difflib
import re
import threading
from dataclasses import dataclass

import bm25s
import Stemmer

from .. import models
from ..util import normalize_key

N = 50  # candidates per channel
DECAY = 0.5  # graph weight per REL hop
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
        if status == "superseded" and not f.superseded:
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
def link_entities(store, ents, q, tenant=None) -> dict:
    """Query entities -> {entity_id: (name, conf)}. Exact key (GLiNER entity 1.0, query n-gram 0.7), else fuzzy
    full-text on Entity.name (0.8 x similarity), else nearest Entity.emb (0.6)."""
    words = key_of(q).split()
    grams = {" ".join(words[i:i + n]) for n in (1, 2, 3) for i in range(len(words) - n + 1)}
    grams = {g for g in grams if len(g) >= 3 and not all(w in _STOP for w in g.split())}
    want = {key_of(e["name"]): 1.0 for e in ents}
    for g in grams:
        want.setdefault(g, 0.7)
    out, hit = {}, set()
    for kk, eid, name in store.query("MATCH (e:Entity) WHERE e.key IN $k RETURN e.key, e.id, e.name", {"k": list(want)}, tenant):
        hit.add(kk)
        out[eid] = (name, max(want[kk], out.get(eid, ("", 0))[1]))
    for e in ents:
        k = key_of(e["name"])
        if k in hit or not k:
            continue
        toks = [t for t in k.split() if len(t) >= 3] or [k]
        for eid, name, ek in store.query("CALL db.idx.fulltext.queryNodes('Entity',$q) YIELD node RETURN node.id, node.name, node.key",
                                         {"q": "|".join(f"%{t}%" for t in toks)}, tenant):
            c = 0.8 * difflib.SequenceMatcher(None, k, ek or key_of(name)).ratio()
            if c >= 0.6 and c > out.get(eid, ("", 0))[1]:
                out[eid] = (name, c)
                hit.add(k)
        if k not in hit:
            v = models.embed_docs([e["name"]], [e["type"]])[0].tolist()
            for eid, name, d in store.query("CALL db.idx.vector.queryNodes('Entity','emb',3,vecf32($v)) YIELD node, score RETURN node.id, node.name, score",
                                            {"v": v}, tenant):
                if 1 - d >= 0.8 and 0.6 > out.get(eid, ("", 0))[1]:
                    out[eid] = (name, 0.6)
    return dict(sorted(out.items(), key=lambda kv: -kv[1][1])[:8])


def _render(trail):
    s = trail[0]
    for rel, fwd, name in trail[1:]:
        s += f" -[{rel}]-> {name}" if fwd else f" <-[{rel}]- {name}"
    return s


def graph(store, ents, q: str, f: Filt, tenant=None, n=N, paths: dict | None = None):
    """Seeds -> entities within 2 REL hops (weight x conf x DECAY per hop) -> Chunks/Memories that MENTION them.
    Entities on SPpaths between seed pairs get a bridging weight and evidence touching two of them a 1.5x bonus.
    `paths` (optional dict) is filled with {node_id: ["A -[OWNS]-> B <-[MENTIONS]- node", ...]}."""
    seeds = link_entities(store, ents, q, tenant)
    if not seeds:
        return []
    W = {e: (c, [nm]) for e, (nm, c) in seeds.items()}  # entity -> (weight, trail)
    names = {e: nm for e, (nm, _) in seeds.items()}
    front = set(W)
    for _ in range(2):
        new = {}
        for a, b, bn, t, c, st in store.query(
                "MATCH (a:Entity)-[r:REL]-(b:Entity) WHERE a.id IN $ids RETURN a.id, b.id, b.name, r.type, coalesce(r.conf, 0.5), startNode(r).id",
                {"ids": list(front)}, tenant):
            w = W[a][0] * c * DECAY
            names[b] = bn
            if w > W.get(b, (0,))[0] and w > new.get(b, (0,))[0]:
                new[b] = (w, W[a][1] + [(t, st == a, bn)])
        W.update(new)
        front = set(new)
    core = set(seeds)
    sl = list(seeds)[:6]
    for i, a in enumerate(sl):
        for b in sl[i + 1:]:
            for ids, rels in store.query(
                    "MATCH (a:Entity {id:$a}), (b:Entity {id:$b}) CALL algo.SPpaths({sourceNode:a, targetNode:b, relTypes:['REL'], maxLen:3, "
                    "relDirection:'both', pathCount:1}) YIELD path RETURN [x IN nodes(path) | [x.id, x.name]], "
                    "[r IN relationships(path) | [r.type, startNode(r).id]]", {"a": a, "b": b}, tenant):
                bw = 0.8 * min(seeds[a][1], seeds[b][1])
                trail = [ids[0][1]]
                for j, (rel, st) in enumerate(rels):
                    trail.append((rel, st == ids[j][0], ids[j + 1][1]))
                    e = ids[j + 1][0]
                    core.add(e)
                    if bw > W.get(e, (0,))[0]:
                        W[e] = (bw, list(trail))
    top = sorted(W, key=lambda e: -W[e][0])[:40]
    score, why = {}, {}
    for nid, e, mc in store.query("MATCH (n)-[m:MENTIONS]->(e:Entity) WHERE e.id IN $ids AND (n:Chunk OR n:Memory) "
                                  "RETURN n.id, e.id, coalesce(m.conf, 1.0)", {"ids": top}, tenant):
        s = W[e][0] * mc
        score[nid] = score.get(nid, 0) + s
        why.setdefault(nid, []).append((s, e))
    for nid, ws in why.items():
        if len({e for _, e in ws} & core) >= 2:
            score[nid] *= 1.5
    ranked = keep(store, sorted(score.items(), key=lambda kv: -kv[1])[:n * 2], f, tenant)[:n]
    if paths is not None:
        for nid, _ in ranked:
            paths[nid] = [f"{_render(W[e][1])} <-[MENTIONS]- {nid}" for _, e in sorted(why[nid], reverse=True)[:2]]
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
