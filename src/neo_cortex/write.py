"""Write path: documents (markdown + YAML frontmatter, other formats via anydoc), agent memories, session transcripts."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

from . import extract as X
from .models import embed_docs
from .resolve import _RANK, resolve_many
from .util import content_hash, new_id, normalize_key, now_ms

CHUNK_MIN, CHUNK_MAX = 120, 250  # words
MAX_CHARS = 2500                 # a code block or URL soup can be few words but many tokens
DEDUPE, CONFLICT = 0.92, 0.75    # memory cosine similarity: at or above DEDUPE reinforce; CONFLICT..DEDUPE flag
MAX_SESSION_MEMORIES = 15
SESSION_WORTH = 0.6
_TEXT_EXT = {".md", ".markdown", ".txt"}
_SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}  # images are not ingested (embed_images is available)
_KINDS = {"doc", "adr", "ticket", "chat", "meeting", "session", "file"}


def _vec(a) -> list:
    return np.asarray(a, dtype=np.float32).tolist()


def _ms(v) -> int | None:
    if v is None:
        return None
    if isinstance(v, str):
        v = datetime.fromisoformat(v.strip().replace("Z", "+00:00"))
    if not isinstance(v, datetime):  # yaml parses a bare date to datetime.date
        v = datetime(v.year, v.month, v.day)
    return int((v if v.tzinfo else v.replace(tzinfo=timezone.utc)).timestamp() * 1000)


# ---------------------------------------------------------------- chunking

def split_frontmatter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            try:
                fm = yaml.safe_load(parts[1])
            except yaml.YAMLError:
                return {}, text
            return (fm if isinstance(fm, dict) else {}), parts[2].lstrip("\n")
    return {}, text


def _sentences(par: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", par) if s]


def _hard_split(p: str) -> list[str]:
    """Halve text (by lines, else by words, else by characters) until every piece fits the word and character caps."""
    if len(p.split()) <= CHUNK_MAX and len(p) <= MAX_CHARS:
        return [p]
    lines = p.splitlines(keepends=True)
    if len(lines) > 1:
        a, b = "".join(lines[:len(lines) // 2]), "".join(lines[len(lines) // 2:])
    else:
        w = p.split(" ")
        a, b = (" ".join(w[:len(w) // 2]), " ".join(w[len(w) // 2:])) if len(w) > 1 else (p[:len(p) // 2], p[len(p) // 2:])
    return _hard_split(a) + _hard_split(b)


def chunk_text(body: str, kind: str = "doc") -> list[str]:
    """Paragraph groups of CHUNK_MIN..CHUNK_MAX words; chat messages stay whole and consecutive."""
    if kind == "chat":
        units = [u for u in re.split(r"\n(?=\*\*\[)", body.strip()) if u.strip()]
    else:
        units = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    flat = []
    for u in units:
        parts = _sentences(u) if len(u.split()) > CHUNK_MAX and not u.lstrip().startswith("|") else [u]
        for p in parts:
            flat += _hard_split(p)
    chunks, cur, n, c = [], [], 0, 0
    for u in flat:
        w = len(u.split())
        if cur and ((n >= CHUNK_MIN and n + w > CHUNK_MAX) or c + len(u) > MAX_CHARS):
            chunks.append("\n\n".join(cur) if kind != "chat" else "\n".join(cur))
            cur, n, c = [], 0, 0
        cur.append(u)
        n += w
        c += len(u)
    if cur:
        chunks.append("\n\n".join(cur) if kind != "chat" else "\n".join(cur))
    if len(chunks) > 1 and len(chunks[-1].split()) < CHUNK_MIN // 3:  # fold a tiny tail into its neighbour
        tail = chunks.pop()
        chunks[-1] += "\n\n" + tail
    return chunks


# ---------------------------------------------------------------- documents

def _load(path: Path) -> tuple[dict, str, str]:
    """(frontmatter, body, raw text) for a file; non-text formats go through anydoc."""
    if path.suffix.lower() in _TEXT_EXT:
        raw = path.read_text(encoding="utf-8", errors="replace")
        fm, body = split_frontmatter(raw)
        return fm, body, raw
    import anydoc
    body = anydoc.to_markdown(str(path))
    return {}, body, body


def _replace_old(store, doc_id: str, tenant) -> list[str]:
    """Drop a changed document with its chunks and their REL edges; return the entity ids that lose mentions."""
    q = lambda c, p=None: store.query(c, p or {"d": doc_id}, tenant)  # noqa: E731
    cids = [r[0] for r in q("MATCH (:Document {id:$d})-[:HAS_CHUNK]->(c) RETURN c.id")]
    eids = [r[0] for r in q("MATCH (:Document {id:$d})-[:HAS_CHUNK]->(c)-[:MENTIONS]->(e) RETURN DISTINCT e.id")]
    if cids:
        q("MATCH ()-[r:REL]->() WHERE r.source_id IN $c DELETE r", {"c": cids})
        q("MATCH (c:Chunk) WHERE c.id IN $c DETACH DELETE c", {"c": cids})
    q("MATCH (d:Document {id:$d}) DETACH DELETE d")
    return eids


def _refresh_entities(store, eids: list[str], tenant) -> None:
    if eids:
        store.query("MATCH (e:Entity) WHERE e.id IN $ids OPTIONAL MATCH (e)<-[:MENTIONS]-(x) "
                    "WITH e, count(x) AS n, min(x.date_ms) AS f, max(x.date_ms) AS l "
                    "SET e.mentions = n, e.first_seen_ms = coalesce(f, e.first_seen_ms), "
                    "e.last_seen_ms = coalesce(l, e.last_seen_ms)", {"ids": eids}, tenant)


_SINGLE = (("OWNS", "tail"), ("MEMBER_OF", "head"))  # one current owner per thing, one current team per person


def _supersede(store, eids: list[str], tenant) -> None:
    """Close the validity of single-valued relations: an edge ends when a later document names a different counterpart."""
    for rtype, side in _SINGLE:
        key, other = ("b", "a") if side == "tail" else ("a", "b")
        rows = store.query(f"MATCH (a:Entity)-[r:REL {{type:$t}}]->(b:Entity) WHERE {key}.id IN $e "
                           f"RETURN id(r), {key}.id, {other}.id, r.valid_from_ms, r.valid_to_ms", {"t": rtype, "e": eids}, tenant)
        groups: dict[str, list] = {}
        for rid, k, o, vf, vt in rows:
            groups.setdefault(k, []).append((vf or 0, o, rid, vt))
        upd = []
        for edges in groups.values():
            edges.sort()
            for vf, o, rid, vt in edges:
                nxt = next((e[0] for e in edges if e[0] > vf and e[1] != o), None)
                if nxt != vt:
                    upd.append({"i": rid, "v": nxt})
        if upd:
            store.query("UNWIND $r AS x MATCH ()-[r:REL]->() WHERE id(r) = x.i SET r.valid_to_ms = x.v", {"r": upd}, tenant)


def _ingest_doc(store, path: Path, tenant) -> dict:
    fm, body, raw = _load(path)
    kind = fm.get("kind") if fm.get("kind") in _KINDS else ("doc" if path.suffix.lower() in _TEXT_EXT else "file")
    doc_id = str(fm.get("id") or "doc_" + content_hash(str(path.resolve())))
    h = content_hash(raw)
    old = store.query("MATCH (d:Document {id:$d}) RETURN d.hash", {"d": doc_id}, tenant)
    if old and old[0][0] == h:
        return {"skipped": 1}
    stale = _replace_old(store, doc_id, tenant) if old else []
    date_ms = _ms(fm.get("date")) or int(path.stat().st_mtime * 1000)
    title = str(fm.get("title") or path.stem)
    labels = [str(x) for x in (fm.get("labels") or [])]
    people = [str(p) for p in (fm.get("participants") or [])]
    author = str(fm["author"]) if fm.get("author") else None

    chunks = chunk_text(body, kind) or [body.strip() or title]
    ex = X.extract_batch(chunks, [title] * len(chunks))
    embs = embed_docs(chunks, [title] * len(chunks))

    # one (name -> type, conf) map for the document, then a single resolution pass
    seen: dict[str, tuple[str, str, float]] = {}  # key -> (name, type, conf)

    def note(name, typ, conf):
        k = normalize_key(name)
        if k and (k not in seen or _RANK.get(typ, 0) > _RANK.get(seen[k][1], 0)):
            seen[k] = (name, typ, conf)

    for name in ([author] if author else []) + people:
        note(name, "person", 1.0)
    for e in ex:
        for x in e["entities"]:
            note(x["name"], x["type"], x["conf"])
    keys = list(seen)
    ids = {k: i for k, i in zip(keys, resolve_many(store, [(seen[k][0], seen[k][1]) for k in keys], tenant)) if i}

    cid = [f"{doc_id}#{i}" for i in range(len(chunks))]
    store.query("CREATE (:Document {id:$id, kind:$kind, title:$title, uri:$uri, path:$path, author:$author, "
                "date_ms:$date, status:$status, labels:$labels, hash:$hash})",
                {"id": doc_id, "kind": kind, "title": title, "uri": fm.get("uri"), "path": str(path),
                 "author": author, "date": date_ms, "status": fm.get("status"), "labels": labels, "hash": h}, tenant)
    store.query("UNWIND $rows AS r CREATE (c:Chunk {id:r.id, doc_id:$d, pos:r.pos, text:r.text, kind:$k, date_ms:$t, "
                "emb:vecf32(r.emb)}) WITH c MATCH (d:Document {id:$d}) CREATE (d)-[:HAS_CHUNK]->(c)",
                {"d": doc_id, "k": kind, "t": date_ms,
                 "rows": [{"id": cid[i], "pos": i, "text": chunks[i], "emb": _vec(embs[i])} for i in range(len(chunks))]},
                tenant)
    men, rels = [], []
    for i, e in enumerate(ex):
        best: dict[str, float] = {}
        for x in e["entities"]:
            k = normalize_key(x["name"])
            best[k] = max(best.get(k, 0), x["conf"])
        men += [{"c": cid[i], "e": ids[k], "conf": c} for k, c in best.items() if k in ids]
        for r in e["relations"]:
            hk, tk = normalize_key(r["head"]), normalize_key(r["tail"])
            if hk in ids and tk in ids:
                rels.append({"h": ids[hk], "t": ids[tk], "type": r["type"], "conf": r["conf"], "src": cid[i]})
    lab = {normalize_key(x) for x in labels}  # frontmatter labels that name known entities (auth-service, identity)
    if lab:
        known = store.query("MATCH (e:Entity) WHERE e.key IN $k RETURN e.id", {"k": list(lab)}, tenant)
        have = {(m["c"], m["e"]) for m in men}
        men += [{"c": c, "e": r[0], "conf": 1.0} for r in known for c in cid if (c, r[0]) not in have]
        ids.update({f"label:{i}": r[0] for i, r in enumerate(known)})
    if men:
        store.query("UNWIND $rows AS r MATCH (c:Chunk {id:r.c}), (e:Entity {id:r.e}) "
                    "CREATE (c)-[:MENTIONS {conf:r.conf}]->(e)", {"rows": men}, tenant)
    if rels:
        store.query("UNWIND $rows AS r MATCH (a:Entity {id:r.h}), (b:Entity {id:r.t}) CREATE (a)-[:REL {type:r.type, "
                    "conf:r.conf, source_id:r.src, valid_from_ms:$t}]->(b)", {"rows": rels, "t": date_ms}, tenant)
    for who, edge in ([(author, "AUTHORED")] if author else []) + [(p, "PARTICIPATED") for p in people if p != author]:
        if normalize_key(who) in ids:
            store.query(f"MATCH (e:Entity {{id:$e}}), (d:Document {{id:$d}}) MERGE (e)-[:{edge}]->(d)",
                        {"e": ids[normalize_key(who)], "d": doc_id}, tenant)
    touched = list({*ids.values(), *stale})
    _refresh_entities(store, touched, tenant)
    _supersede(store, touched, tenant)
    return {"documents": 1, "chunks": len(chunks), "mentions": len(men), "rels": len(rels)}


def ingest_path(store, path, tenant=None) -> dict:
    """Ingest a file or a directory tree. Unchanged documents (same hash) are skipped; changed ones are replaced."""
    p = Path(path)
    files = sorted(f for f in ([p] if p.is_file() else p.rglob("*")) if f.is_file() and f.suffix.lower() not in _SKIP_EXT
                   and not any(part.startswith(".") for part in f.relative_to(p if p.is_dir() else p.parent).parts))
    before = store.query("MATCH (e:Entity) RETURN count(e)", tenant=tenant)[0][0]
    tot = {"documents": 0, "skipped": 0, "chunks": 0, "mentions": 0, "rels": 0, "errors": 0, "unsupported": 0}
    for f in files:
        try:
            for k, v in _ingest_doc(store, f, tenant).items():
                tot[k] += v
        except Exception as e:  # one unreadable file must not abort a directory ingest
            tot["unsupported" if type(e).__name__ == "UnsupportedError" else "errors"] += 1
            print(f"neo: skipped {f}: {type(e).__name__}: {e}", file=__import__("sys").stderr)
    tot["new_entities"] = store.query("MATCH (e:Entity) RETURN count(e)", tenant=tenant)[0][0] - before
    return tot


# ---------------------------------------------------------------- memories

def _agent_edge(store, agent: str, mid: str, tenant):
    store.query("MERGE (a:Agent {id:$i}) SET a.name=$n WITH a MATCH (m:Memory {id:$m}) MERGE (a)-[:WROTE]->(m)",
                {"i": "agent:" + normalize_key(agent), "n": agent, "m": mid}, tenant)


def remember(store, text: str, kind: str | None = None, about=None, supersedes: str | None = None,
             agent: str | None = None, project: str | None = None, source_id: str | None = None, tenant=None,
             confidence: float | None = None) -> dict:
    """Write a memory. Near-duplicates (cosine >= 0.92) reinforce the existing one; similar memories that share an
    entity come back as `conflicts` (0.75..0.92); `supersedes` retires an older memory and links SUPERSEDES."""
    q = lambda c, p=None: store.query(c, p or {}, tenant)  # noqa: E731
    text = text.strip()
    emb = embed_docs([text])[0]
    if kind is None:
        kind, kconf = X.classify_memory(text)
    else:
        kconf = 1.0 if confidence is None else confidence
    ex = X.extract(text)["entities"]
    names = {normalize_key(x["name"]): (x["name"], x["type"]) for x in ex}
    for a in ([about] if isinstance(about, str) else about or []):
        names.setdefault(normalize_key(a), (a, "other"))
    eids = [i for i in resolve_many(store, list(names.values()), tenant) if i]

    cands = [(r[0], r[1], 1 - r[2], r[3]) for r in q(
        "CALL db.idx.vector.queryNodes('Memory','emb',8,vecf32($e)) YIELD node, score "
        "RETURN node.id, node.text, score, node.status ORDER BY score", {"e": _vec(emb)})
        if r[3] == "active" and r[0] != supersedes]
    if cands and cands[0][2] >= DEDUPE and not supersedes:
        mid = cands[0][0]
        same_src = source_id and q("MATCH (m:Memory {id:$m})-[:DERIVED_FROM]->(s {id:$s}) RETURN 1", {"m": mid, "s": source_id})
        if not same_src:  # re-ingesting the same session must not count as another use
            q("MATCH (m:Memory {id:$m}) SET m.uses = m.uses + 1, m.last_used_ms = $t", {"m": mid, "t": now_ms()})
        return {"id": mid, "status": "reinforced", "kind": kind, "entities": [n for n, _ in names.values()], "conflicts": []}
    conflicts = []
    if eids:
        shared = {r[0] for r in q("MATCH (m:Memory)-[:MENTIONS]->(e:Entity) WHERE e.id IN $e AND m.status='active' "
                                  "RETURN DISTINCT m.id", {"e": eids})}
        conflicts = [{"id": i, "text": t, "sim": round(s, 4)} for i, t, s, _ in cands
                     if CONFLICT <= s < DEDUPE and i in shared]
    mid, t = new_id("mem"), now_ms()
    q("CREATE (:Memory {id:$id, text:$text, kind:$kind, confidence:$conf, created_ms:$t, valid_from_ms:$t, "
      "status:'active', uses:0, last_used_ms:$t, source_id:$src, agent:$agent, project:$project, emb:vecf32($e)})",
      {"id": mid, "text": text, "kind": kind, "conf": kconf, "t": t, "src": source_id, "agent": agent,
       "project": project, "e": _vec(emb)})
    if eids:
        q("UNWIND $e AS i MATCH (m:Memory {id:$m}), (e:Entity {id:i}) CREATE (m)-[:MENTIONS {conf:1.0}]->(e)",
          {"m": mid, "e": eids})
        _refresh_entities(store, eids, tenant)
    if supersedes:
        q("MATCH (n:Memory {id:$n}), (o:Memory {id:$o}) CREATE (n)-[:SUPERSEDES]->(o) "
          "SET o.status='superseded', o.valid_to_ms=$t", {"n": mid, "o": supersedes, "t": t})
    if source_id:
        q("MATCH (m:Memory {id:$m}) OPTIONAL MATCH (s:Session {id:$s}) OPTIONAL MATCH (c:Chunk {id:$s}) "
          "WITH m, coalesce(s, c) AS src WHERE src IS NOT NULL CREATE (m)-[:DERIVED_FROM]->(src)", {"m": mid, "s": source_id})
    if agent:
        _agent_edge(store, agent, mid, tenant)
    return {"id": mid, "status": "created", "kind": kind, "entities": [n for n, _ in names.values()], "conflicts": conflicts}


# ---------------------------------------------------------------- sessions

_NOISE = re.compile(r"<(system-reminder|local-command-[a-z]+|command-[a-z]+|task-notification)[^>]*>.*?</\1>", re.S)
_CODE = re.compile(r"```.*?```", re.S)


def _transcript_segments(path: Path) -> tuple[dict, list[tuple[str, str]]]:
    """(meta, [(role, segment)]) from a Claude Code JSONL transcript: user/assistant text only, tool traffic skipped."""
    meta, segs = {}, []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        for k, f in (("session_id", "sessionId"), ("cwd", "cwd")):
            if d.get(f) and k not in meta:
                meta[k] = d[f]
        if d.get("timestamp") and "started" not in meta:
            meta["started"] = d["timestamp"]
        m = d.get("message")
        if d.get("type") not in ("user", "assistant") or d.get("isMeta") or d.get("isSidechain") or not isinstance(m, dict):
            continue
        c = m.get("content")
        blocks = [c] if isinstance(c, str) else [b.get("text", "") for b in c or [] if isinstance(b, dict) and b.get("type") == "text"]
        for b in blocks:
            b = _CODE.sub(" ", _NOISE.sub(" ", b))
            for par in re.split(r"\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)", b):
                par = re.sub(r"\s+", " ", par).strip(" -*#>|")
                if par.startswith(("|", "http")) or len(par.split()) < 6:
                    continue
                segs += [(d["type"], s) for s in (_sentences(par) if len(par.split()) > 60 else [par])]
    return meta, segs


def ingest_session(store, transcript_path, agent: str = "claude-code", project: str | None = None, tenant=None) -> dict:
    """Session node + up to 15 auto-extracted Memories. Idempotent per session id and transcript hash."""
    p = Path(transcript_path)
    raw = p.read_bytes().decode("utf-8", errors="replace")
    meta, segs = _transcript_segments(p)
    sid = str(meta.get("session_id") or p.stem)
    h = content_hash(raw)
    old = store.query("MATCH (s:Session {id:$s}) RETURN s.hash", {"s": sid}, tenant)
    if old and old[0][0] == h:
        return {"session": sid, "skipped": 1, "memories": 0}
    project = project or (Path(meta["cwd"]).name if meta.get("cwd") else None)
    store.query("MERGE (s:Session {id:$s}) SET s.agent=$a, s.project=$p, s.started_ms=$t, s.path=$path, s.hash=$h "
                "WITH s MERGE (g:Agent {id:$gid}) SET g.name=$a MERGE (s)-[:BY]->(g)",
                {"s": sid, "a": agent, "p": project, "t": _ms(meta.get("started")) or now_ms(), "path": str(p), "h": h,
                 "gid": "agent:" + normalize_key(agent)}, tenant)
    uniq = list(dict.fromkeys(s for _, s in segs))[:600]  # shortcut: first 600 unique segments, raise for very long sessions
    kept = []
    if uniq:
        scores = X.worth_keeping_batch(uniq)
        kept = sorted([(s, t) for s, t in zip(scores, uniq) if s >= SESSION_WORTH], reverse=True)[:MAX_SESSION_MEMORIES]
    kinds = X.classify_memory_batch([t for _, t in kept]) if kept else []
    created = reinforced = 0
    for (score, text), (kind, kconf) in zip(kept, kinds):
        r = remember(store, text, kind=kind, agent=agent, project=project, source_id=sid, tenant=tenant,
                     confidence=kconf)
        created += r["status"] == "created"
        reinforced += r["status"] == "reinforced"
    return {"session": sid, "skipped": 0, "segments": len(uniq), "memories": created, "reinforced": reinforced}
