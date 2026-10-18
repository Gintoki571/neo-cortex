"""Hybrid retrieval: vector + BM25 + graph + temporal channels fused with weighted RRF."""
import os

from ..util import now_ms as _now
from . import channels as ch
from .fuse import BASE, boost_factor, channel_weights, kind_factor, rrf
from .query import parse_query, parse_time

__all__ = ["recall", "rrf", "parse_query", "parse_time"]
CHANNELS = ("vector", "bm25", "graph", "temporal")
ANCHORS = 5  # top dense/BM25 hits whose entities seed the graph channel
POOL = 20  # top candidates per channel handed to the temporal re-rank


def _trim(t, n=400):
    t = t or ""
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


def _proof_counts(store, ids, tenant):
    """id -> evidence count: Memory.uses, else the number of MENTIONS edges out of the item."""
    rows = store.query("MATCH (n) WHERE (n:Chunk OR n:Memory) AND n.id IN $ids "
                       "OPTIONAL MATCH (n)-[m:MENTIONS]->() RETURN n.id, n.uses, count(m)",
                       {"ids": list(ids)}, tenant)
    return {r[0]: max(r[1] or 0, r[2]) for r in rows}


def recall(store, query, k=8, since_ms=None, until_ms=None, kinds=None, weights=None, channels=None, tenant=None, now_ms=None, info=None, _relax=False):
    """Top-k Chunks/Memories as {id, label, text, score, channels: {name: rank}, paths, source, date_ms, kind, status}.
    since_ms/until_ms: window [since, until), explicit values beat time words in the query. kinds: Chunk or Memory
    `kind` values and/or the lowercase labels "chunk"/"memory". weights: absolute per-channel weights (no intent
    boosts); channels: subset of vector, bm25, graph, temporal (ablations). A window parsed from the query that matches nothing
    is dropped and the search repeated unfiltered with the temporal (recency) channel. info (optional dict) receives the graph
    channel's "seeds" and PPR-related "entities"."""
    now = now_ms if now_ms is not None else _now()
    chans = list(channels) if channels else None
    need_nlp = chans is None or "graph" in chans or "temporal" in chans
    pq = parse_query(query, now, nlp=need_nlp)
    since = since_ms if since_ms is not None else (None if _relax else pq["since_ms"])
    until = until_ms if until_ms is not None else (None if _relax else pq["until_ms"])
    intent = pq["intent"]
    top = max(intent, key=intent.get) if intent else None
    temporal_q = top == "temporal" and intent[top] >= 0.4
    f = ch.Filt(since, until, tuple(kinds) if kinds else None, superseded=temporal_q)
    parsed_window = since_ms is None and until_ms is None and (since is not None or until is not None)
    if chans is None:
        cue = since is not None or until is not None or temporal_q or ch.RECENT_RE.search(query)
        chans = ["vector", "bm25", "graph"] + (["temporal"] if cue else [])
    bad = set(chans) - set(CHANNELS)
    if bad:
        raise ValueError(f"unknown channels {sorted(bad)}")
    lists, paths, gi = {}, {}, {}  # gi: the graph channel's own report (strength), copied to info
    if "vector" in chans:
        lists["vector"] = ch.vector(store, query, f, tenant)
    if "bm25" in chans:
        lists["bm25"] = ch.bm25(store, query, f, tenant)
    if "graph" in chans:
        anchors = [i for i, _, _ in rrf({c: lists[c] for c in ("vector", "bm25") if c in lists})[:ANCHORS]]
        lists["graph"] = ch.graph(store, pq["entities"], query, f, tenant, paths=paths, anchors=anchors, now=now,
                                  current=not temporal_q, info=gi)
        if info is not None:
            info.update(gi)
    if "temporal" in chans:
        pool = {i for l in lists.values() for i, _ in l[:POOL]} or None
        asc = temporal_q and bool(ch.CHANGE_RE.search(query))
        lists["temporal"] = ch.temporal(store, f, tenant, pool, asc, q=query) if pool is not None or not lists else []
    if os.environ.get("NEO_WHY_TIER") == "1" and intent.get("decision"):  # graphify idea #8: why/frontmatter tier
        lists["why"] = ch._why_list(store, query, tenant)
    w = channel_weights(intent) if weights is None else {**BASE, **weights}
    if os.environ.get("NEO_WHY_TIER") == "1" and intent.get("decision"):
        w = {**w, "why": 0.2}  # low weight: supplementary, never a filter
    if "graph" in lists:  # a weak or hub seed scales the graph's rank contribution down
        w = {**w, "graph": w["graph"] * gi.get("strength", 1.0)}
    if _relax:
        w = {**w, "temporal": 2.0}  # recency boost: the user's time words found nothing
    fused = rrf(lists, w, norm=os.environ.get("NEO_FUSE_NORM") == "1")
    meta_rows = ch.meta(store, [i for i, _, _ in fused], tenant)
    kind = {i: m[1] for i, m in meta_rows.items()}  # kind routing: decision nodes
    if fused and os.environ.get("NEO_FUSE_BOOST") == "1":  # bounded secondary boosts (recency/window/proof)
        proof = _proof_counts(store, [i for i, _, _ in fused], tenant)
        fused = [(i, s * boost_factor(meta_rows.get(i, (None, None, None, None))[2], now, since, until, proof.get(i, 0)), r)
                 for i, s, r in fused]
    fused = sorted(((i, s * kind_factor(intent, kind.get(i)), r) for i, s, r in fused), key=lambda x: -x[1])[:k]
    if not fused:
        if parsed_window:  # the time words matched nothing: search everything, newest first
            return recall(store, query, k, None, None, kinds, weights, chans if "temporal" in chans else chans + ["temporal"],
                          tenant, now, info, _relax=True)
        return []
    ids = [i for i, _, _ in fused]
    rows = {r[0]: r for r in store.query(
        "MATCH (n) WHERE (n:Chunk OR n:Memory) AND n.id IN $ids OPTIONAL MATCH (d:Document)-[:HAS_CHUNK]->(n) "
        "RETURN n.id, labels(n)[0], n.text, coalesce(n.date_ms, n.valid_from_ms, n.created_ms), n.kind, n.status, "
        "n.source_id, n.agent, n.project, d.id, d.title, d.kind, d.uri, d.author", {"ids": ids}, tenant)}
    doc_rows = {r[0]: r for r in store.query(
        "MATCH (d:Document) WHERE d.id IN $ids "
        "RETURN d.id, d.title, d.kind, d.uri, d.author, d.date_ms, d.description, d.doc_type", {"ids": ids}, tenant)}
    out = []
    for i, s, ranks in fused:
        if i in doc_rows:  # why-tier hit: a Document surfaced by title / doc_type / description
            _, dtitle, dkind, duri, dauthor, date, description, doctype = doc_rows[i]
            out.append({"id": i, "label": "Document", "text": _trim(description or dtitle or ""), "score": s,
                        "channels": ranks, "paths": paths.get(i, []),
                        "source": {"doc_id": i, "title": dtitle, "kind": dkind, "uri": duri, "author": dauthor,
                                   "doc_type": doctype},
                        "date_ms": date, "kind": dkind, "status": None})
            continue
        _, label, text, date, kind, status, sid, agent, project, did, dtitle, dkind, duri, dauthor = rows[i]
        src = ({"doc_id": did, "title": dtitle, "kind": dkind, "uri": duri, "author": dauthor} if label == "Chunk"
               else {"source_id": sid, "agent": agent, "project": project, "kind": kind})
        out.append({"id": i, "label": label, "text": _trim(text), "score": s, "channels": ranks, "paths": paths.get(i, []),
                    "source": src, "date_ms": date, "kind": kind, "status": status})
    return out
