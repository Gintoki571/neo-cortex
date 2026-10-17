"""Write path: documents (markdown + YAML frontmatter, other formats via anydoc), agent memories, session transcripts."""
import ast
from html.parser import HTMLParser
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

from . import extract as X
from .models import embed_docs
from .resolve import PIN_EXPLICIT, PIN_REGEX, resolve_many
from .session_mem import read_transcript, select
from .util import content_hash, new_id, normalize_key, now_ms

CHUNK_MIN, CHUNK_MAX = 120, 250  # words
MAX_CHARS = 2500                 # a code block or URL soup can be few words but many tokens
DEDUPE, CONFLICT = 0.92, 0.75    # memory cosine similarity: at or above DEDUPE reinforce; CONFLICT..DEDUPE flag
_TEXT_EXT = {".md", ".markdown", ".txt"}
_CODE_EXT = {".py"}                # one chunk per top-level def/class, see _code_chunks
_SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}  # images are not ingested (embed_images is available)
_KINDS = {"doc", "adr", "ticket", "chat", "meeting", "session", "file"}
_NUM = re.compile(r"\d+(?:\.\d+)?")
_NEG = re.compile(r"\b(?:not|no|never|none|nothing|cannot|without)\b|n't\b", re.I)


def _differ(a: str, b: str) -> bool:
    """Two near-identical statements that differ in a number or a negation contradict each other: never a duplicate."""
    return set(_NUM.findall(a)) != set(_NUM.findall(b)) or bool(_NEG.search(a)) != bool(_NEG.search(b))


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


def _code_chunks(src: str) -> list[tuple[str, str, str | None]]:
    """(code, prose, name) per chunk: the header (module docstring, imports, top-level statements), then one chunk per
    top-level def/class (decorators included), long ones split. prose = docstrings and comments, the only text GLiNER reads."""
    tree = ast.parse(src)
    lines = src.splitlines()
    defs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    taken = {i for n in defs for i in range(min([n.lineno] + [d.lineno for d in n.decorator_list]) - 1, n.end_lineno)}
    header = "\n".join(l for i, l in enumerate(lines) if i not in taken).strip()
    pieces = [(piece, ast.get_docstring(tree), None) for piece in _hard_split(header)] if header else []
    for n in defs:
        s = min([n.lineno] + [d.lineno for d in n.decorator_list]) - 1
        for j, piece in enumerate(_hard_split("\n".join(lines[s:n.end_lineno]))):
            pieces.append((piece, ast.get_docstring(n) if j == 0 else None, n.name if j == 0 else None))
    out = []
    for piece, doc, name in pieces:
        comments = [l.strip().lstrip("#").strip() for l in piece.splitlines() if l.strip().startswith("#")]
        out.append((piece, "\n".join(([doc] if doc else []) + comments), name))
    return out


def _module_title(path: Path) -> str:
    """Module path from the top of the package: src/neo_cortex/tools.py -> neo_cortex/tools.py (a loose file: its name)."""
    p = path.resolve()
    rel, d = [p.name], p.parent
    while d != d.parent and (d / "__init__.py").exists():
        rel.insert(0, d.name)
        d = d.parent
    return "/".join(rel)


def _title(path: Path, fm: dict, body: str) -> str:
    """Frontmatter title, else the first `#` (then `##`) heading outside code fences, else "<parent dir>/<stem>"."""
    if fm.get("title"):
        return str(fm["title"])
    body = re.sub(r"(?s)```.*?```", "", body)
    # a level-1 heading wins; converted slides and sheets (anydoc) often start at level 2
    m = re.search(r"^#[ \t]+(\S.*?)\s*$", body, re.M) or re.search(r"^##[ \t]+(\S.*?)\s*$", body, re.M)
    return m.group(1) if m else f"{path.parent.name}/{path.stem}"


def _strs(v) -> list[str]:
    if isinstance(v, str):
        return [x.strip() for x in v.split(",") if x.strip()]
    return [str(x) for x in (v or [])]


# ---------------------------------------------------------------- documents

class _HTMLMarkdown(HTMLParser):
    _DROP = {"script", "style", "nav", "footer"}
    _BLOCKS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.buffer, self.title, self.rows = [], [], None, []
        self.row, self.cell = None, None
        self.heading = False
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._DROP:
            self.skip += 1
        elif not self.skip and tag == "title":
            self.title = []
        elif not self.skip and tag == "tr":
            self.row = []
        elif not self.skip and tag in {"th", "td"}:
            self.cell = []

    def handle_endtag(self, tag):
        if tag in self._DROP:
            self.skip -= 1
        elif self.skip:
            return
        elif tag == "title":
            self.title = "".join(self.title).strip()
        elif tag in {"th", "td"} and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row:
                self.rows.append(self.row)
            self.row = None
        elif tag in self._BLOCKS:
            text = " ".join("".join(self.buffer).split())
            if text:
                prefix = "#" * int(tag[1:]) + " " if tag.startswith("h") else "- " if tag == "li" else ""
                self.lines.append(prefix + text)
                self.heading |= tag == "h1"
            self.buffer = []

    def handle_data(self, data):
        if self.skip:
            return
        if self.cell is not None:
            self.cell.append(data)
        elif isinstance(self.title, list):
            self.title.append(data)
        else:
            self.buffer.append(data)

    def markdown(self):
        if self.rows:
            table = ["| " + " | ".join(self.rows[0]) + " |",
                     "| " + " | ".join("---" for _ in self.rows[0]) + " |"]
            table += ["| " + " | ".join(row) + " |" for row in self.rows[1:]]
            self.lines.extend(table)
        return "\n\n".join(self.lines).strip(), (self.title if not self.heading else None)


def _html_to_markdown(path: Path) -> tuple[dict, str]:
    parser = _HTMLMarkdown()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    body, title = parser.markdown()
    return ({"title": title} if title else {}), body


def _load(path: Path) -> tuple[dict, str, str]:
    """(frontmatter, body, raw text) for a file; non-text formats go through anydoc."""
    if path.suffix.lower() in {".html", ".htm"}:
        raw = path.read_text(encoding="utf-8", errors="replace")
        fm, body = _html_to_markdown(path)
        return fm, body, raw
    if path.suffix.lower() in _CODE_EXT:
        raw = path.read_text(encoding="utf-8", errors="replace")
        return {}, raw, raw
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
        rows = store.query(f"MATCH (a:Entity)-[r:REL {{type:$t}}]->(b:Entity) WHERE {key}.id IN $e AND coalesce(r.modality,'fact')='fact' "
                           f"RETURN id(r), {key}.id, {other}.id, r.valid_from_ms, r.valid_to_ms, a.type = 'person'",
                           {"t": rtype, "e": eids}, tenant)
        groups: dict[tuple, list] = {}
        for rid, k, o, vf, vt, person in rows:  # a team and a person can both own a thing: one current owner of each kind
            groups.setdefault((k, person if rtype == "OWNS" else None), []).append((vf or 0, o, rid, vt))
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
    code = path.suffix.lower() in _CODE_EXT
    kind = "code" if code else (fm.get("kind") if fm.get("kind") in _KINDS else ("doc" if path.suffix.lower() in _TEXT_EXT else "file"))
    doc_id = str(fm.get("id") or "doc_" + content_hash(str(path.resolve())))
    h = content_hash(raw)
    old = store.query("MATCH (d:Document {id:$d}) RETURN d.hash, d.path", {"d": doc_id}, tenant)
    if old and Path(old[0][1]).resolve() != path.resolve():  # frontmatter id owned by another file
        raise ValueError(f"id collision with {old[0][1]}")
    if old and old[0][0] == h:
        return {"skipped": 1}
    try:
        stale = _replace_old(store, doc_id, tenant) if old else []
        date_ms = _ms(fm.get("date")) or int(path.stat().st_mtime * 1000)
        title = _module_title(path) if code else _title(path, fm, body)
        labels = [str(x) for x in (fm.get("labels") or [])]
        people = [str(p) for p in (fm.get("participants") or [])]
        author = str(fm["author"]) if fm.get("author") else None
        desc = str(fm.get("description") or "").strip() or None
        tags = _strs(fm.get("tags"))

        if code:
            parts = _code_chunks(raw) or [(title, "", None)]
            chunks, prose, names = [c for c, _, _ in parts], [p for _, p, _ in parts], [n for _, _, n in parts]
        else:
            chunks = chunk_text(body, kind) or [body.strip() or title]
            if desc:  # searchable: the description rides in the first chunk (vector and BM25 both read chunk text)
                chunks[0] = desc + "\n\n" + chunks[0]
            prose, names = chunks, [None] * len(chunks)
        teams = [r[0] for r in store.query("MATCH (e:Entity {type:'team'}) RETURN e.name", tenant=tenant)]
        ex = X.extract_batch(prose, [title] * len(chunks), [author or ""] * len(chunks), teams, kind=kind)
        for e, n in zip(ex, names):  # a def/class name is a component entity in its own chunk
            if n:
                e["entities"].append({"name": n, "type": "component", "conf": 1.0, "pin": PIN_REGEX})
        embs = embed_docs(chunks, [title] * len(chunks))

        # one vote per (name, type) for the document: confidences summed over its chunks, then a single resolution pass
        seen: dict[str, dict] = {}  # key -> {"name": first spelling, "votes": {type: [weight, pin]}}

        def note(name, typ, weight, pin):
            k = normalize_key(name)
            if k:
                v = seen.setdefault(k, {"name": name, "votes": {}})["votes"]
                w, p = v.get(typ, [0.0, 0])
                v[typ] = [w + weight, max(p, pin)]

        for name in ([author] if author else []) + people:
            note(name, "person", 1.0, PIN_EXPLICIT)
        for e in ex:
            for x in e["entities"]:
                note(x["name"], x["type"], x["conf"], x.get("pin", 0))
        keys = [k for k in seen for _ in seen[k]["votes"]]
        items = [(seen[k]["name"], t, w, p) for k in seen for t, (w, p) in seen[k]["votes"].items()]
        ids = {k: i for k, i in zip(keys, resolve_many(store, items, tenant)) if i}

        cid = [f"{doc_id}#{i}" for i in range(len(chunks))]
        store.query("CREATE (:Document {id:$id, kind:$kind, title:$title, uri:$uri, path:$path, author:$author, "
                    "date_ms:$date, status:$status, labels:$labels, doc_type:$dt, description:$desc, tags:$tags})",
                    {"id": doc_id, "kind": kind, "title": title, "uri": fm.get("uri"), "path": str(path),
                     "author": author, "date": date_ms, "status": fm.get("status"), "labels": labels,
                     "dt": str(fm["type"]) if fm.get("type") else None, "desc": desc, "tags": tags}, tenant)
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
                    rels.append({"h": ids[hk], "t": ids[tk], "type": r["type"], "conf": r["conf"], "src": cid[i],
                                 "vf": r.get("valid_from_ms") or date_ms, "mod": r.get("modality", "fact"), "pf": r.get("p_fact", 1.0)})
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
                        "conf:r.conf, source_id:r.src, valid_from_ms:r.vf, modality:r.mod, p_fact:r.pf}]->(b)", {"rows": rels}, tenant)
        for who, edge in ([(author, "AUTHORED")] if author else []) + [(p, "PARTICIPATED") for p in people if p != author]:
            if normalize_key(who) in ids:
                store.query(f"MATCH (e:Entity {{id:$e}}), (d:Document {{id:$d}}) MERGE (e)-[:{edge}]->(d)",
                            {"e": ids[normalize_key(who)], "d": doc_id}, tenant)
        touched = list({*ids.values(), *stale})
        _refresh_entities(store, touched, tenant)
        _supersede(store, touched, tenant)
        store.query("MATCH (d:Document {id:$d}) SET d.hash=$h", {"d": doc_id, "h": h}, tenant)  # last: a crash leaves no hash
        return {"documents": 1, "chunks": len(chunks), "mentions": len(men), "rels": len(rels)}
    except Exception:
        _replace_old(store, doc_id, tenant)  # no half-written document may survive: the next run would skip it
        raise


def ingest_path(store, path, tenant=None) -> dict:
    """Ingest a file or a directory tree. Unchanged documents (same hash) are skipped; changed ones are replaced."""
    p = Path(path)
    files = sorted(f for f in ([p] if p.is_file() else p.rglob("*")) if f.is_file() and f.suffix.lower() not in _SKIP_EXT
                   and not any(part.startswith(".") or part == "__pycache__" for part in f.relative_to(p if p.is_dir() else p.parent).parts))
    before = store.query("MATCH (e:Entity) RETURN count(e)", tenant=tenant)[0][0]
    tot = {"documents": 0, "skipped": 0, "chunks": 0, "mentions": 0, "rels": 0, "errors": 0, "unsupported": 0}
    for f in files:
        try:
            with store.write_lock:  # check-then-create per document
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
             confidence: float | None = None, valid_from_ms: int | None = None, entities=None, relations=None) -> dict:
    """Write a memory. Near-duplicates (cosine >= 0.92) reinforce the existing one; similar memories that share an
    entity come back as `conflicts` (0.75..0.92); `supersedes` retires an older memory and links SUPERSEDES.
    `entities` ([{name, type}]; unknown types become other) and `relations` ([head, TYPE, tail], only their names are
    linked here; tools.remember writes the edges) are what the caller knows: with `kind` and any of about/entities/
    relations, GLiNER does not run."""
    with store.write_lock:  # dedupe check and create must not interleave
        q = lambda c, p=None: store.query(c, p or {}, tenant)  # noqa: E731
        text = text.strip()
        emb = embed_docs([text])[0]
        structured = kind is not None and bool(about or entities or relations)
        if kind is None:
            kind, kconf = X.classify_memory(text)
        else:
            kconf = 1.0 if confidence is None else confidence
        # name -> (name, type, weight, pin): GLiNER's confidence, the caller's own type (explicit), or no type ("other")
        names = {} if structured else {normalize_key(x["name"]): (x["name"], x["type"], x["conf"], 0)
                                       for x in X.extract(text)["entities"]}
        etypes = {t for t, _ in X.ENTITY_LABELS.values()}
        for e in entities or []:
            names[normalize_key(e["name"])] = (e["name"], e["type"] if e.get("type") in etypes else "other", 1.0, PIN_EXPLICIT)
        for a in ([about] if isinstance(about, str) else about or []):
            names.setdefault(normalize_key(a), (a, "other", 1.0, 0))
        for h, _, tl in relations or []:  # caller-named endpoints resolve by exact key or alias only
            for n in (h, tl):
                nm, t, w, _ = names.get(normalize_key(n), (n, "other", 1.0, PIN_EXPLICIT))
                names[normalize_key(n)] = (nm, t, w, PIN_EXPLICIT)
        resolved = resolve_many(store, list(names.values()), tenant)
        eids = [i for i in resolved if i]
        ids = {n: i for (n, *_), i in zip(names.values(), resolved) if i}

        cands = [(r[0], r[1], 1 - r[2], r[3]) for r in q(
            "CALL db.idx.vector.queryNodes('Memory','emb',8,vecf32($e)) YIELD node, score "
            "RETURN node.id, node.text, score, node.status ORDER BY score", {"e": _vec(emb)})
            if r[3] == "active" and r[0] != supersedes]
        dup = next((c for c in cands if c[2] >= DEDUPE and not _differ(text, c[1])), None)
        if dup and not supersedes:
            mid = dup[0]
            same_src = source_id and q("MATCH (m:Memory {id:$m})-[:DERIVED_FROM]->(s {id:$s}) RETURN 1", {"m": mid, "s": source_id})
            if not same_src:  # re-ingesting the same session must not count as another use
                q("MATCH (m:Memory {id:$m}) SET m.uses = m.uses + 1, m.last_used_ms = $t", {"m": mid, "t": now_ms()})
            return {"id": mid, "status": "reinforced", "kind": kind, "entities": [n for n, *_ in names.values()], "entity_ids": ids, "conflicts": []}
        shared = {r[0] for r in q("MATCH (m:Memory)-[:MENTIONS]->(e:Entity) WHERE e.id IN $e AND m.status='active' "
                                  "RETURN DISTINCT m.id", {"e": eids})} if eids else set()
        # a near-duplicate that differs in a number or negation ("24 hours" vs "48 hours") is a conflict, shared entity or not
        conflicts = [{"id": i, "text": t, "sim": round(s, 4)} for i, t, s, _ in cands if s >= CONFLICT and (s >= DEDUPE or i in shared)]
        mid, t = new_id("mem"), now_ms()
        q("CREATE (:Memory {id:$id, text:$text, kind:$kind, confidence:$conf, created_ms:$t, valid_from_ms:$vf, "
          "status:'active', uses:0, last_used_ms:$t, source_id:$src, agent:$agent, project:$project, emb:vecf32($e)})",
          {"id": mid, "text": text, "kind": kind, "conf": kconf, "t": t, "vf": valid_from_ms or t, "src": source_id, "agent": agent,
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
        return {"id": mid, "status": "created", "kind": kind, "entities": [n for n, *_ in names.values()], "entity_ids": ids, "conflicts": conflicts}


# ---------------------------------------------------------------- sessions

def ingest_session(store, transcript_path, agent: str = "claude-code", project: str | None = None, tenant=None) -> dict:
    """Session node + up to 15 memories from `session_mem.select` (preferences, decisions, lessons, outcomes), each stored
    through `remember` with valid_from = its message time. Idempotent per session id and transcript hash."""
    with store.write_lock:  # check-then-create: one writer at a time
        p = Path(transcript_path)
        raw = p.read_bytes().decode("utf-8", errors="replace")
        meta, ev = read_transcript(p)
        sid = str(meta.get("session_id") or p.stem)
        h = content_hash(raw)
        old = store.query("MATCH (s:Session {id:$s}) RETURN s.hash", {"s": sid}, tenant)
        if old and old[0][0] == h:
            return {"session": sid, "skipped": 1, "memories": 0}
        project = project or (Path(meta["cwd"]).name if meta.get("cwd") else None)
        store.query("MERGE (s:Session {id:$s}) SET s.agent=$a, s.project=$p, s.started_ms=$t, s.path=$path "
                    "WITH s MERGE (g:Agent {id:$gid}) SET g.name=$a MERGE (s)-[:BY]->(g)",
                    {"s": sid, "a": agent, "p": project, "t": _ms(meta.get("started")) or now_ms(), "path": str(p),
                     "gid": "agent:" + normalize_key(agent)}, tenant)
        kept = select(ev)
        created = reinforced = 0
        for c in kept:
            r = remember(store, c["text"], kind=c["kind"], agent=agent, project=project, source_id=sid, tenant=tenant,
                         confidence=c["conf"], valid_from_ms=c["ts"])
            created += r["status"] == "created"
            reinforced += r["status"] == "reinforced"
        store.query("MATCH (s:Session {id:$s}) SET s.hash=$h", {"s": sid, "h": h}, tenant)  # last: a crash leaves no hash
        return {"session": sid, "skipped": 0, "segments": len(ev), "memories": created, "reinforced": reinforced,
                "kinds": dict(Counter(c["kind"] for c in kept))}
