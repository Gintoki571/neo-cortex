"""Agent-facing tools: plain functions over a Store that return compact markdown text.

Every line carries ids (pass them back as arguments), kind, date, source and why it matched. Every tool takes
`max_chars` and truncates with a "narrow with" hint. No LLM here: the calling agent reasons over this evidence.
"""
import math
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import write
from .config import settings
from .dream import dream as _dream
from .retrieve import channels as ch
from .retrieve import parse_query
from .retrieve import recall as _recall
from .util import content_hash, new_id, normalize_key, now_ms

MAX = 4000
DAY = 86400000
OWN_TYPES = ["OWNS", "MEMBER_OF", "WORKS_ON", "APPROVED", "DECIDED", "PART_OF"]
KINDS = ("episodic", "semantic", "procedural", "preference", "decision")
DOC_KINDS = ("doc", "adr", "ticket", "chat", "meeting", "session", "file")


# ---------------------------------------------------------------- formatting helpers

def _d(ms) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d") if ms else "undated"


def _ms(v: str | None, end=False) -> int | None:
    """ISO date or datetime to epoch-ms. A date-only `until` includes that whole day."""
    if not v:
        return None
    dt = datetime.fromisoformat(v.strip().replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000) + (DAY if end and len(v.strip()) == 10 else 0)


def _t(s, n=240) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def _cap(lines, max_chars, hint, tail=False) -> str:
    """Join lines within max_chars; the dropped remainder (from the end, or the oldest with tail=True) becomes a hint."""
    lines = list(lines)
    if sum(len(x) + 1 for x in lines) <= max_chars:
        return "\n".join(lines)
    note = lambda n: f"…{n} more, narrow with {hint}"  # noqa: E731
    budget, out = max_chars - len(note(len(lines))) - 1, []
    for x in (reversed(lines) if tail else lines):
        if len(x) + 1 > budget:
            break
        out.append(x)
        budget -= len(x) + 1
    if tail:
        out.reverse()
    dropped = len(lines) - len(out)
    return "\n".join(([note(dropped)] + out) if tail else (out + [note(dropped)]))


def _mem_line(r) -> str:
    i, kind, date, agent, project, conf, text, uses, status = r
    meta = ", ".join(x for x in (agent, project, f"conf {conf:.2f}" if conf is not None else None,
                                 f"used {uses}x" if uses else None, "SUPERSEDED" if status == "superseded" else None) if x)
    return f"- [{i}] {kind} {_d(date)} ({meta}) {_t(text)}"


def _item(n, r) -> str:
    s = r["source"]
    src = (f'doc "{_t(s.get("title"), 60)}" ({s.get("kind")}) [{s.get("doc_id")}]' + (f' by {s["author"]}' if s.get("author") else "") if r["label"] == "Chunk"
           else "memory " + "/".join(x for x in (s.get("agent"), s.get("project")) if x) + (f" session {s['source_id']}" if s.get("source_id") else ""))
    why = ",".join(f"{c}#{k}" for c, k in r["channels"].items())
    out = f"{n}. [{r['id']}] {r['kind'] or r['label'].lower()} {_d(r['date_ms'])}" + (" SUPERSEDED" if r["status"] == "superseded" else "")
    out += f" | {src} | via {why}\n   {_t(r['text'])}"
    return out + "".join(f"\n   path: {p}" for p in r["paths"][:1])


def _resolve(store, name, tenant):
    """Entity (id, name, type) by id, key or alias, else fuzzy full-text / vector. None when nothing is close."""
    k = normalize_key(name)
    r = store.query("MATCH (e:Entity) WHERE e.id=$n OR e.key=$k OR $k IN e.aliases RETURN e.id, e.name, e.type "
                    "ORDER BY e.mentions DESC LIMIT 1", {"n": name, "k": k}, tenant)
    if r:
        return tuple(r[0])
    hit = ch.link_entities(store, [{"name": name, "type": "other"}], name, tenant)
    for eid in hit:
        return tuple(store.query("MATCH (e:Entity {id:$i}) RETURN e.id, e.name, e.type", {"i": eid}, tenant)[0])
    return None


def _src_names(store, ids, tenant) -> dict:
    ids = [i for i in set(ids) if i]
    if not ids:
        return {}
    out = {r[0]: f'"{_t(r[1], 50)}" [{r[2]}] {_d(r[3])}' for r in store.query(
        "MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk) WHERE c.id IN $i RETURN c.id, d.title, d.id, d.date_ms", {"i": ids}, tenant)}
    out.update({r[0]: f"memory [{r[0]}]" for r in store.query("MATCH (m:Memory) WHERE m.id IN $i RETURN m.id", {"i": ids}, tenant)})
    return out


def _trail(nodes, rels) -> str:
    s = nodes[0][1]
    for i, r in enumerate(rels):
        s += f" -[{r[0]}]-> {nodes[i + 1][1]}" if r[1] == nodes[i][0] else f" <-[{r[0]}]- {nodes[i + 1][1]}"
    return s


def _paths(store, a, b, max_hops, tenant, count=3):
    """Shortest REL paths between entity ids a and b (both directions): [(nodes [[id,name]], rels [[type,start,src,date,conf]])]."""
    return store.query(
        "MATCH (a:Entity {id:$a}), (b:Entity {id:$b}) CALL algo.SPpaths({sourceNode:a, targetNode:b, relTypes:['REL'], "
        f"maxLen:{int(max_hops)}, relDirection:'both', pathCount:{int(count)}}}) YIELD path "
        "RETURN [x IN nodes(path) | [x.id, x.name]], [r IN relationships(path) | [r.type, startNode(r).id, r.source_id, r.valid_from_ms, r.conf]]",
        {"a": a, "b": b}, tenant)


def _path_lines(store, paths, tenant, lead="") -> list[str]:
    src = _src_names(store, [r[2] for _, rels in paths for r in rels], tenant)
    out = []
    for nodes, rels in paths:
        out.append(f"{lead}{_trail(nodes, rels)}")
        out.append("    src: " + "; ".join(f"{r[0]} {src.get(r[2], r[2] or '?')}" for r in rels))
    return out


# ---------------------------------------------------------------- brief

def brief(store, project=None, agent=None, max_chars=MAX, tenant=None) -> str:
    """Session-start context: open handoffs, preferences, decisions, lessons, facts, recent episodes, recent documents."""
    p = {"p": project}
    lines = []

    def mems(title, kind, n):
        order = "m.created_ms DESC" if kind == "episodic" else "coalesce(m.uses,0) DESC, coalesce(m.created_ms,0) DESC"
        rows = store.query(
            "MATCH (m:Memory {kind:$k}) WHERE m.status='active' AND ($p IS NULL OR m.project IS NULL OR m.project=$p) "
            "RETURN m.id, m.kind, coalesce(m.valid_from_ms, m.created_ms), m.agent, m.project, m.confidence, m.text, m.uses, m.status "
            f"ORDER BY {order} LIMIT {n}", {**p, "k": kind}, tenant)
        if rows:
            lines.append(f"## {title}")
            lines.extend(_mem_line(r) for r in rows)

    hs = store.query(
        "MATCH (h:Handoff {status:'open'}) OPTIONAL MATCH (h)-[:FROM]->(f:Agent) OPTIONAL MATCH (h)-[:TO]->(t:Agent) "
        "WITH h, f, t WHERE $a IS NULL OR t.id=$a OR t.name=$an RETURN h.id, f.name, t.name, h.created_ms, h.summary, h.tasks "
        "ORDER BY h.created_ms DESC LIMIT 10", {"a": "agent:" + normalize_key(agent) if agent else None, "an": agent}, tenant)
    if hs:
        lines.append("## Open handoffs (finish, then handoff(done=<id>))")
        for i, f, t, d, s, tasks in hs:
            lines.append(f"- [{i}] {_d(d)} from {f or '?'} to {t or '?'}: {_t(s)}" + (f" | tasks: {_t('; '.join(tasks), 200)}" if tasks else ""))
    mems("Preferences", "preference", 8)
    mems("Active decisions", "decision", 8)
    mems("Lessons (procedural)", "procedural", 6)
    mems("Facts", "semantic", 5)
    mems("Recent episodes", "episodic", 5)
    docs = store.query("MATCH (d:Document) WHERE d.date_ms IS NOT NULL RETURN d.id, d.kind, d.date_ms, d.title ORDER BY d.date_ms DESC LIMIT 5",
                       None, tenant)
    if docs:
        lines.append("## Recent documents")
        lines.extend(f'- [{i}] {k} {_d(d)} "{_t(t, 80)}"' for i, k, d, t in docs)
    if not lines:
        return "Memory is empty. Use remember(text) to record preferences, decisions and lessons; ingest(path) for documents."
    scope = " ".join(x for x in (f"project={project}" if project else "", f"agent={agent}" if agent else "") if x)
    head = f"# Neo-Cortex brief{' (' + scope + ')' if scope else ''}"
    return _cap([head, *lines], max_chars, "project=/agent=, or recall(query)")


# ---------------------------------------------------------------- recall / remember

def recall(store, query, k=8, since=None, until=None, kinds=None, max_chars=MAX, tenant=None) -> str:
    rs = _recall(store, query, k=k, since_ms=_ms(since), until_ms=_ms(until, end=True), kinds=kinds, tenant=tenant)
    if not rs:
        return f'No results for "{_t(query, 80)}". Try other words, drop since/until/kinds, or ask(question).'
    return _cap([f'# recall "{_t(query, 80)}": {len(rs)} results (id | source | channels#rank)']
                + [_item(i, r) for i, r in enumerate(rs, 1)], max_chars, "kinds=, since=, or a smaller k")


def remember(store, text, kind=None, about=None, supersedes=None, agent=None, project=None, max_chars=MAX, tenant=None) -> str:
    if kind is not None and kind not in KINDS:
        return f"kind must be one of {', '.join(KINDS)}"
    old = None
    if supersedes:
        old = store.query("MATCH (m:Memory {id:$i}) RETURN m.text", {"i": supersedes}, tenant)
        if not old:
            return f"supersedes id {supersedes} not found; use recall to find the memory id"
    r = write.remember(store, text, kind=kind, about=about, supersedes=supersedes, agent=agent, project=project, tenant=tenant)
    out = [f"{r['status']} [{r['id']}] {r['kind']}" + (f" about: {', '.join(r['entities'][:8])}" if r["entities"] else "")]
    if r["status"] == "reinforced":
        out.append("an equivalent memory already existed; its use count went up (nothing new written)")
    if old:
        out.append(f"superseded {supersedes}: {_t(old[0][0], 120)}")
    if r["conflicts"]:
        out.append("conflicts: similar active memories that may be stale; call remember again with supersedes=<id> to replace one:")
        out += [f"- [{c['id']}] sim {c['sim']:.2f} {_t(c['text'], 160)}" for c in r["conflicts"]]
    return _cap(out, max_chars, "shorter text")


# ---------------------------------------------------------------- ask / explore / connect

def ask(store, question, max_chars=MAX, tenant=None) -> str:
    """Multi-hop evidence pack. It does not answer: the caller reasons over seeds, paths, facts and cited evidence."""
    pq = parse_query(question)
    ginfo = {}
    rs = _recall(store, question, k=8, weights={"graph": 2.0}, info=ginfo, tenant=tenant)
    seeds = ginfo["seeds"] if "seeds" in ginfo else ch.link_entities(store, pq["entities"], question, tenant)  # seeds the walk actually used
    out = ["# ask: evidence pack"]
    if seeds:
        out.append("## Seeds (linked entities)")
        out += [f"- [{e}] {n} (match {c:.2f})" for e, (n, c) in seeds.items()]
    paths, ids = [], list(seeds)
    sl = ids[:5]
    for i, a in enumerate(sl):
        for b in sl[i + 1:]:
            paths += _paths(store, a, b, 3, tenant, count=1)
    if paths:
        out.append("## Bridging paths")
        out += _path_lines(store, paths, tenant, "- ")
        ids = list({*ids, *(n[0] for nodes, _ in paths for n in nodes)})
    rel_ents = [e for e, *_ in ginfo.get("entities", [])[:6]]
    ids = list({*ids, *rel_ents})
    if ids:
        facts = store.query(
            "MATCH (a:Entity)-[r:REL]->(b:Entity) WHERE (a.id IN $i AND b.id IN $i) OR ((a.id IN $r OR b.id IN $r) AND r.type IN $ty) "
            "RETURN a.name, r.type, b.name, r.conf, r.valid_from_ms, r.source_id "
            "ORDER BY r.conf DESC LIMIT 15", {"i": ids, "r": rel_ents, "ty": OWN_TYPES}, tenant)  # reached entities: show who owns/approves/works on them
        if facts:
            src = _src_names(store, [f[5] for f in facts], tenant)
            out.append("## Facts among them")
            out += [f"- {a} -[{t}]-> {b} ({_d(d)}, conf {c or 0:.2f}) src {src.get(s, s or '?')}" for a, t, b, c, d, s in facts]
    if ginfo.get("entities"):  # reached by the Personalized PageRank walk: bridging answers (people, owners) show up here
        out.append("## Related entities (graph walk from the seeds, strongest first)")
        out += [f"- [{e}] {n}: {tr}" for e, n, _, tr in ginfo["entities"][:6]]
    if rs:
        out.append("## Evidence (cite ids)")
        out += [_item(i, r) for i, r in enumerate(rs, 1)]
    top = max(pq["intent"], key=pq["intent"].get) if pq["intent"] else None
    first = next(iter(seeds.values()))[0] if seeds else None
    if not seeds:
        nxt = "no entity linked; try recall(query) with the exact terms, or cypher"
    elif top == "temporal" and pq["intent"][top] >= 0.4:
        nxt = f'timeline("{first}")'
    elif top == "owner" and pq["intent"][top] >= 0.4:
        nxt = f'who("{first}")'
    elif len(seeds) > 1 and not paths:
        nxt = f'connect("{first}", "{list(seeds.values())[1][0]}", max_hops=5): no short path found'
    else:
        nxt = f'explore("{first}")'
    out.append(f"## Suggested next\n{nxt}")
    return _cap(out, max_chars, "a narrower question")


def explore(store, entity, hops=1, since=None, max_chars=MAX, tenant=None) -> str:
    e = _resolve(store, entity, tenant)
    if not e:
        return f'No entity matching "{entity}". Try recall("{entity}") or cypher.'
    eid, name, typ = e
    t0 = _ms(since)
    seen, front, rows = {eid}, [eid], []
    for h in range(1, max(1, min(int(hops), 3)) + 1):
        got = store.query(
            "MATCH (a:Entity)-[r:REL]-(b:Entity) WHERE a.id IN $f RETURN a.name, b.id, b.name, b.type, r.type, startNode(r).id = a.id, "
            "r.conf, r.valid_from_ms, r.source_id", {"f": front}, tenant)
        front = []
        for an, bid, bn, bt, rt, fwd, c, d, s in got:
            if (t0 and (d or 0) < t0) or bid in seen:
                continue
            front.append(bid)
            rows.append((h, an, bid, bn, bt, rt, fwd, c, d, s))
        seen |= set(front)
    src = _src_names(store, [r[9] for r in rows], tenant)
    out = [f"# [{eid}] {name} ({typ})"]
    if rows:
        out.append("## Neighbours")
        for h, an, bid, bn, bt, rt, fwd, c, d, s in rows:
            arrow = f"-[{rt}]->" if fwd else f"<-[{rt}]-"
            out.append(f"- {'  ' * (h - 1)}{an} {arrow} [{bid}] {bn} ({bt}) {_d(d)} conf {c or 0:.2f} src {src.get(s, s or '?')}")
    docs = store.query("MATCH (d:Document)-[:HAS_CHUNK]->(c)-[:MENTIONS]->(e:Entity {id:$i}) RETURN d.id, d.kind, d.date_ms, d.title, count(c) "
                       "ORDER BY count(c) DESC, d.date_ms DESC LIMIT 6", {"i": eid}, tenant)
    if docs:
        out.append("## Most-mentioning documents")
        out += [f'- [{i}] {k} {_d(d)} "{_t(t, 70)}" ({n} chunks)' for i, k, d, t, n in docs]
    ms_ = store.query("MATCH (m:Memory)-[:MENTIONS]->(e:Entity {id:$i}) WHERE m.status='active' RETURN m.id, m.kind, coalesce(m.valid_from_ms, m.created_ms), "
                      "m.agent, m.project, m.confidence, m.text, m.uses, m.status ORDER BY m.created_ms DESC LIMIT 4", {"i": eid}, tenant)
    if ms_:
        out.append("## Memories")
        out += [_mem_line(r) for r in ms_]
    return _cap(out, max_chars, "hops=1 or since=")


def connect(store, a, b, max_hops=4, max_chars=MAX, tenant=None) -> str:
    ra, rb = _resolve(store, a, tenant), _resolve(store, b, tenant)
    if not ra or not rb:
        return f'No entity matching "{a if not ra else b}". Try explore/recall first.'
    ps = _paths(store, ra[0], rb[0], max_hops, tenant, count=5)
    if not ps:
        return f"No path between [{ra[0]}] {ra[1]} and [{rb[0]}] {rb[1]} within {max_hops} hops. Try a larger max_hops or ask(question)."
    return _cap([f"# connect [{ra[0]}] {ra[1]} <-> [{rb[0]}] {rb[1]}: {len(ps)} paths", *_path_lines(store, ps, tenant, "- ")],
                max_chars, "a smaller max_hops")


# ---------------------------------------------------------------- impact / relate / read

def _depends(store, ids, n, up, tenant) -> dict:
    """Transitive DEPENDS_ON over currently valid edges. up=False: entities that depend on `ids`; up=True: what `ids` depend on.
    Returns {entity id: (hops, [[id, name], ...] chain from that entity toward the start (down) or from the start (up), [source ids])}."""
    pat = ("p=(s:Entity)-[:REL*1..%d]->(a:Entity)" if up else "p=(a:Entity)-[:REL*1..%d]->(s:Entity)") % int(n)
    rows = store.query(f"MATCH {pat} WHERE s.id IN $s AND all(r IN relationships(p) WHERE r.type='DEPENDS_ON' AND r.valid_to_ms IS NULL) "
                       "RETURN a.id, [x IN nodes(p) | [x.id, x.name]], [r IN relationships(p) | r.source_id] LIMIT 500", {"s": list(ids)}, tenant)
    best = {}
    for aid, nodes, srcs in rows:
        if aid not in ids and (aid not in best or len(nodes) < len(best[aid][1])):
            best[aid] = (len(nodes) - 1, nodes, srcs)
    return best


def impact(store, entity, max_hops=3, max_chars=MAX, tenant=None) -> str:
    """Blast radius of `entity` failing: who depends on it (transitively, current DEPENDS_ON edges), what it needs, the current owners of each
    affected component, and the customers and incidents recorded near them. Every edge carries its source."""
    e = _resolve(store, entity, tenant)
    if not e:
        return f'No entity matching "{entity}". Try recall("{entity}") or explore.'
    eid, name, typ = e
    n = max(1, min(int(max_hops), 5))
    same = {eid, *(r[0] for r in store.query("MATCH (x:Entity {id:$i})-[r:REL]-(y:Entity) WHERE r.type IN ['RENAMED_TO','REPLACED_BY'] RETURN y.id", {"i": eid}, tenant))}
    down, up = _depends(store, same, n, False, tenant), _depends(store, same, n, True, tenant)
    src = _src_names(store, [s for d in (down, up) for *_, ss in d.values() for s in ss], tenant)

    def chain(nodes, srcs, rev):
        names = [x[1] for x in nodes]
        return " -> ".join(names[::-1] if rev else names) + "  src: " + "; ".join(src.get(s, s or "?") for s in srcs)

    out = [f"# impact [{eid}] {name} ({typ}): {len(down)} depend on it, it needs {len(up)} (DEPENDS_ON, current, max_hops {n}; A -> B = A depends on B)"]
    if same - {eid}:
        out.append("(also counting its other names: " + ", ".join(r[0] for r in store.query("MATCH (x:Entity) WHERE x.id IN $i RETURN x.name", {"i": list(same - {eid})}, tenant)) + ")")
    out.append("## Breaks if it fails (nearest first)" if down else "## Breaks if it fails\n- nothing depends on it in the graph")
    out += [f"- hop {h} [{a}] {nodes[0][1]}: {chain(nodes, srcs, False)}" for a, (h, nodes, srcs) in sorted(down.items(), key=lambda kv: (kv[1][0], kv[1][1][0][1]))]
    if up:
        out.append("## It needs (if these fail, it fails)")
        out += [f"- hop {h} [{a}] {nodes[-1][1]}: {chain(nodes, srcs, False)}" for a, (h, nodes, srcs) in sorted(up.items(), key=lambda kv: (kv[1][0], kv[1][1][-1][1]))]
    comps = {**{eid: name}, **{a: v[1][0][1] for a, v in down.items()}}
    owners = {}
    for cid, oid, on, ot, d, s in store.query(
            "MATCH (o:Entity)-[r:REL {type:'OWNS'}]->(c:Entity) WHERE c.id IN $c AND r.valid_to_ms IS NULL RETURN c.id, o.id, o.name, o.type, r.valid_from_ms, r.source_id",
            {"c": list(comps) + list(same)}, tenant):
        owners.setdefault(cid, []).append((oid, on, ot, d, s))
    teams = [o[0] for os_ in owners.values() for o in os_ if o[2] == "team"]
    members = {}
    if teams:
        for tid, pn in store.query("MATCH (p:Entity)-[r:REL {type:'MEMBER_OF'}]->(t:Entity) WHERE t.id IN $t AND r.valid_to_ms IS NULL RETURN t.id, p.name", {"t": teams}, tenant):
            members.setdefault(tid, []).append(pn)
    osrc = _src_names(store, [o[4] for os_ in owners.values() for o in os_], tenant)
    out.append("## Owners to tell (current OWNS)")
    for cid, cn in comps.items():
        os_ = owners.get(cid) or next((owners[s] for s in same if s in owners and cid == eid), None)
        out.append(f"- {cn}: " + ("; ".join(f"[{o[0]}] {o[1]}{' (' + ', '.join(members[o[0]][:6]) + ')' if o[0] in members else ''} since {_d(o[3])} src {osrc.get(o[4], o[4] or '?')}" for o in os_)
                                  if os_ else "no current owner recorded"))
    near = {}
    for kid, kn, kt, an, cnt, cids in store.query(
            "MATCH (c:Chunk)-[:MENTIONS]->(a:Entity), (c)-[:MENTIONS]->(k:Entity) WHERE a.id IN $a AND k.type IN ['customer','incident'] AND k.id <> a.id "
            "RETURN k.id, k.name, k.type, a.name, count(DISTINCT c), collect(DISTINCT c.id)", {"a": list(comps) + list(same)}, tenant):
        k = near.setdefault(kid, [kn, kt, 0, []])
        k[2] += cnt
        k[3].append(f"{an} {cnt}x [{cids[0]}]")
    for kid, kn, kt, an, how in store.query(
            "MATCH (a:Entity)-[r:REL]-(k:Entity) WHERE a.id IN $a AND k.type IN ['customer','incident'] AND r.valid_to_ms IS NULL RETURN k.id, k.name, k.type, a.name, r.type",
            {"a": list(comps) + list(same)}, tenant):
        k = near.setdefault(kid, [kn, kt, 0, []])
        k[2] += 2
        k[3].append(f"{an} {how}")
    for kind in ("customer", "incident"):
        top = sorted((v for v in near.values() if v[1] == kind), key=lambda v: -v[2])[:6]
        if top:
            out.append(f"## {kind.capitalize()}s linked to these components (co-mentioned in a chunk, or a REL edge)")
            out += [f"- {v[0]}: " + "; ".join(v[3][:3]) for v in top]
    return _cap(out, max_chars, "a smaller max_hops")


REL_NAMES = ("OWNS", "MEMBER_OF", "DEPENDS_ON", "CAUSED_BY", "FIXED_BY", "APPROVED", "DECIDED", "PART_OF", "WORKS_ON", "REPORTED", "REPLACED_BY", "RENAMED_TO", "RELATED_TO")
_ENDS = {"OWNS": ("person", "service"), "MEMBER_OF": ("person", "team"), "DEPENDS_ON": ("service", "service"), "CAUSED_BY": ("incident", "other"),
         "FIXED_BY": ("incident", "other"), "APPROVED": ("person", "decision"), "DECIDED": ("person", "decision"), "PART_OF": ("service", "service"),
         "WORKS_ON": ("person", "ticket"), "REPORTED": ("person", "incident"), "REPLACED_BY": ("service", "service"), "RENAMED_TO": ("service", "service")}


def relate(store, head, type, tail, source=None, supersede=False, agent=None, max_chars=MAX, tenant=None) -> str:
    """Write (or correct) one typed edge head -[type]-> tail from now on. Names or ids; unknown names become new entities. supersede=True first
    closes the current same-type edge it replaces (OWNS: other owners of `tail`; other types: other `type` edges from `head`)."""
    t = re.sub(r"\W+", "_", type.strip()).upper()
    if t not in REL_NAMES:
        return f"type must be one of {', '.join(REL_NAMES)}"
    from .resolve import resolve_entity
    ids = []
    for n, ty in zip((head, tail), _ENDS.get(t, ("other", "other"))):
        i = store.query("MATCH (e:Entity {id:$i}) RETURN e.id", {"i": n}, tenant)
        i = i[0][0] if i else resolve_entity(store, n, ty, tenant=tenant)
        if not i:
            return f'"{n}" is ambiguous (a lone surname matching several people); use the entity id from explore/who'
        ids.append(i)
    a, b = ids
    if a == b:
        return "head and tail are the same entity"
    names = {r[0]: r[1] for r in store.query("MATCH (e:Entity) WHERE e.id IN $i RETURN e.id, e.name", {"i": ids}, tenant)}
    cur = store.query("MATCH (a:Entity {id:$a})-[r:REL {type:$t}]->(b:Entity {id:$b}) WHERE r.valid_to_ms IS NULL RETURN r.valid_from_ms, r.source_id", {"a": a, "b": b, "t": t}, tenant)
    line = f"[{a}] {names[a]} -[{t}]-> [{b}] {names[b]}"
    if cur:
        return f"already current since {_d(cur[0][0])}: {line} (nothing written)"
    now, closed = now_ms(), []
    if supersede:
        pat = ("(x:Entity)-[r:REL {type:$t}]->(b:Entity {id:$b}) WHERE x.id <> $a" if t == "OWNS" else "(x:Entity {id:$a})-[r:REL {type:$t}]->(y:Entity) WHERE y.id <> $b")
        for xn, yn, vf in store.query(f"MATCH {pat} AND r.valid_to_ms IS NULL SET r.valid_to_ms=$n RETURN {'x.name, b.name' if t == 'OWNS' else 'x.name, y.name'}, r.valid_from_ms",
                                      {"a": a, "b": b, "t": t, "n": now}, tenant):
            closed.append(f"closed {xn} -[{t}]-> {yn} (valid since {_d(vf)}, ended {_d(now)})")
    store.query("MATCH (a:Entity {id:$a}), (b:Entity {id:$b}) CREATE (a)-[:REL {type:$t, conf:1.0, source_id:$s, valid_from_ms:$n, agent:$g, created_ms:$n}]->(b)",
                {"a": a, "b": b, "t": t, "s": source, "n": now, "g": agent}, tenant)
    src = _src_names(store, [source], tenant).get(source, source) if source else "none given"
    return _cap([f"created {line} valid from {_d(now)} by {agent or 'unknown agent'}, src {src}", *closed], max_chars, "a smaller max_chars")


def read(store, id, max_chars=MAX, tenant=None) -> str:
    """Full text of a Chunk, Memory or Document by id, with metadata and neighbours (recall/ask cut evidence at 240 characters)."""
    q = lambda c: store.query(c, {"i": id}, tenant)  # noqa: E731
    ents = lambda label: ", ".join(f"[{i}] {n} ({t})" for i, n, t in q(f"MATCH (:{label} {{id:$i}})-[m:MENTIONS]->(e:Entity) RETURN e.id, e.name, e.type ORDER BY m.conf DESC LIMIT 12"))  # noqa: E731
    r = q("MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk {id:$i}) RETURN c.text, c.pos, c.kind, c.date_ms, d.id, d.title, d.uri, d.author, d.status")
    if r:
        text, pos, kind, dt, did, title, uri, author, status = r[0]
        n = store.query("MATCH (:Document {id:$d})-[:HAS_CHUNK]->(c) RETURN count(c)", {"d": did}, tenant)[0][0]
        rels = [f"{a} -[{ty}]-> {b} ({_d(vf)}{', ended ' + _d(vt) if vt else ''})" for a, ty, b, vf, vt in q(
            "MATCH (a:Entity)-[r:REL {source_id:$i}]->(b:Entity) RETURN a.name, r.type, b.name, r.valid_from_ms, r.valid_to_ms LIMIT 12")]
        meta = [f'# chunk [{id}] {kind} {_d(dt)} | doc "{_t(title, 80)}" [{did}]' + (f" by {author}" if author else "") + (f" status {status}" if status else "") + f" | chunk {pos + 1} of {n}" + (f" | {uri}" if uri else ""),
                f"prev: {'[' + did + '#' + str(pos - 1) + ']' if pos else 'none'}  next: {'[' + did + '#' + str(pos + 1) + ']' if pos + 1 < n else 'none'}"]
        if ents("Chunk"):
            meta.append("mentions: " + ents("Chunk"))
        if rels:
            meta.append("relations sourced here: " + "; ".join(rels))
        body = [text]
    elif (r := q("MATCH (m:Memory {id:$i}) RETURN m.text, m.kind, m.status, coalesce(m.valid_from_ms, m.created_ms), m.valid_to_ms, m.confidence, m.agent, m.project, m.uses, m.source_id")):
        text, kind, st, d, vt, conf, ag, pr, uses, sid = r[0]
        links = [f"{rel} [{o}] {_t(tx, 80)}" for rel, qy in (("supersedes", "MATCH (:Memory {id:$i})-[:SUPERSEDES]->(o:Memory) RETURN o.id, o.text"),
                                                         ("superseded by", "MATCH (o:Memory)-[:SUPERSEDES]->(:Memory {id:$i}) RETURN o.id, o.text")) for o, tx in q(qy)]
        meta = [f"# memory [{id}] {kind} {st} {_d(d)}" + (f", ended {_d(vt)}" if vt else "") + f" | " + ", ".join(x for x in (ag, pr, f"conf {conf:.2f}" if conf is not None else None, f"used {uses}x" if uses else None, f"from [{sid}]" if sid else None) if x)]
        if ents("Memory"):
            meta.append("mentions: " + ents("Memory"))
        meta += links
        body = [text]
    elif (r := q("MATCH (d:Document {id:$i}) RETURN d.kind, d.title, d.date_ms, d.author, d.status, d.uri")):
        kind, title, dt, author, status, uri = r[0]
        cs = q("MATCH (:Document {id:$i})-[:HAS_CHUNK]->(c:Chunk) RETURN c.id, c.text ORDER BY c.pos")
        meta = [f'# document [{id}] {kind} {_d(dt)} "{_t(title, 100)}"' + (f" by {author}" if author else "") + (f" status {status}" if status else "") + (f" | {uri}" if uri else "") + f" | {len(cs)} chunks"]
        body = [f"[{c}] {t}" for c, t in cs]
    else:
        return f"No chunk, memory or document with id {id}. Ids come from recall/ask results ([doc-01#0], [mem_..]); entity ids go to explore."
    head = "\n".join(meta) + "\n---\n"
    text = "\n".join(body)
    room = max(200, max_chars - len(head) - 80)
    if len(text) > room:
        text = text[:room].rsplit(" ", 1)[0] + f"…\n…{len(text) - room} more chars, narrow with read({id!r}, max_chars={len(head) + len(text) + 80})"
    return head + text


# ---------------------------------------------------------------- who / timeline

def who(store, topic, max_chars=MAX, tenant=None) -> str:
    seeds = ch.link_entities(store, [{"name": topic, "type": "other"}], topic, tenant)
    tids = list(seeds)[:3]
    score, why = {}, {}
    names = {}

    def add(pid, pname, s, reason):
        names[pid] = pname
        score[pid] = score.get(pid, 0) + s
        why.setdefault(pid, []).append(reason)

    if tids:
        rows = store.query(
            "MATCH p=(x:Entity {type:'person'})-[:REL*1..2]->(t:Entity) WHERE t.id IN $t AND all(r IN relationships(p) WHERE r.type IN $ty) "
            "RETURN x.id, x.name, [n IN nodes(p) | [n.id, n.name]], [r IN relationships(p) | [r.type, startNode(r).id, r.source_id, r.valid_from_ms, r.conf, r.valid_to_ms]]",
            {"t": tids, "ty": OWN_TYPES}, tenant)
        src = _src_names(store, [r[2] for *_, rels in rows for r in rels], tenant)
        best = {}
        for pid, pname, nodes, rels in rows:
            s = math.prod((r[4] or 0.5) for r in rels) * 0.7 ** (len(rels) - 1) * (1.0 if any(r[0] == "OWNS" for r in rels) else 0.8)
            if s > best.get(pid, (0,))[0]:
                ended = next((r[5] for r in rels if r[5]), None)  # a relation that ended: former owner, not current
                best[pid] = (s, pname, f"{_trail(nodes, rels)} (src {src.get(rels[-1][2], rels[-1][2] or '?')})" + (f" FORMER, ended {_d(ended)}" if ended else ""))
        for pid, (s, pname, reason) in best.items():
            add(pid, pname, s, reason)
        docs = {r[0]: r[1] for r in store.query("MATCH (d:Document)-[:HAS_CHUNK]->(c)-[:MENTIONS]->(t:Entity) WHERE t.id IN $t RETURN d.id, count(c)",
                                                {"t": tids}, tenant)}
    else:
        docs = {}
        for r in _recall(store, topic, k=10, channels=["vector", "bm25"], tenant=tenant):
            if r["label"] == "Chunk" and r["source"].get("doc_id"):
                docs[r["source"]["doc_id"]] = 1
    if docs:
        now = now_ms()
        per = {}
        for pid, pname, rel, did, title, d in store.query(
                "MATCH (x:Entity {type:'person'})-[a:AUTHORED|PARTICIPATED]->(d:Document) WHERE d.id IN $d RETURN x.id, x.name, type(a), d.id, d.title, d.date_ms",
                {"d": list(docs)}, tenant):
            w = (0.3 if rel == "AUTHORED" else 0.15) * (1 + math.log(docs[did])) * 0.5 ** (max(0, now - (d or now)) / DAY / 365)
            p = per.setdefault(pid, [pname, 0.0, []])
            p[1] += w
            p[2].append((d or 0, rel.lower(), did))
        for pid, (pname, w, ev) in per.items():
            ev.sort(reverse=True)
            add(pid, pname, w, f"{len(ev)} docs on topic ({', '.join(sorted({e[1] for e in ev}))}), latest {_d(ev[0][0])}: " + ", ".join(f"[{e[2]}]" for e in ev[:3]))
    if not score:
        return f'No people found for "{topic}". Try explore("{topic}") or recall.'
    top = sorted(score, key=lambda p: -score[p])[:8]
    out = [f'# who: "{_t(topic, 60)}"' + (f" (entities: {', '.join(n for n, _ in seeds.values())})" if seeds else "") + ", ranked, with evidence"]
    out += [f"{i}. [{p}] {names[p]} score {score[p]:.2f}\n   " + "\n   ".join(why[p]) for i, p in enumerate(top, 1)]
    return _cap(out, max_chars, "a more specific topic")


_STOP = set("the a an of in on to for and or is was were what when how did does do who which that this these those it its by with from as at be been are has have had about over time changed change history".split())
_CUE = re.compile(r"\b(from|to|now|lowered|raised|changed|renamed|replaced|moved|reverted|instead|until|since|effective|increased|decreased|switched|dropped|lifted|set|reversal|replaces|owns|owner)\b", re.I)


def _facts(text, terms, n=2, width=220) -> list[str]:
    """Up to n sentences of `text` that mention one of `terms` (normalised phrases) and carry a number or a change word, in text order."""
    cands = []
    for i, s in enumerate(re.split(r"(?<=[.!?])\s+|\n+", re.sub(r"[*#|`]+", " ", text or ""))):
        s = re.sub(r"\s+", " ", s).strip(" -_:")
        if len(s) < 20:
            continue
        ns = f" {normalize_key(s)} "
        hits = sum(f" {t} " in ns for t in terms)
        num, cue = bool(re.search(r"\d", s)), bool(_CUE.search(s))
        if hits and (num or cue):
            cands.append((-(2 * hits + num + cue), i, _t(s, width)))
    return [c[2] for c in sorted(sorted(cands)[:n], key=lambda c: c[1])]


def timeline(store, topic, since=None, until=None, max_chars=MAX, tenant=None) -> str:
    """Dated events about an entity or topic, oldest first, with the values: relation changes (effective dates), the sentences of each
    document that mention it with numbers or changes, superseded memories. Over the budget, events without values are dropped first."""
    e = _resolve(store, topic, tenant)
    t0, t1 = _ms(since), _ms(until, end=True)
    ev = []  # (date_ms, text, keep-priority)
    tterms = {w for w in normalize_key(topic).split() if len(w) > 2 and w not in _STOP}
    if e:
        eid, name, typ = e
        exact = normalize_key(topic) == normalize_key(name) or topic == eid
        edges = store.query("MATCH (a:Entity)-[r:REL]-(b:Entity {id:$i}) RETURN a.id, a.name, r.type, startNode(r).id = a.id, r.valid_from_ms, r.source_id, r.conf, r.valid_to_ms",
                            {"i": eid}, tenant)
        # same relation type from the same side: a change of the other end is a change of value, not a new fact
        groups = {}
        for o, on, t, fwd, d, s, c, vt in edges:
            groups.setdefault((t, fwd), []).append((d or 0, o, on, s, c, vt))
        src = _src_names(store, [x[5] for x in edges], tenant)
        for (t, fwd), g in groups.items():
            g.sort()
            for i, (d, o, on, s, c, vt) in enumerate(g):
                line = (f"{on} -[{t}]-> {name}" if fwd else f"{on} <-[{t}]- {name}")
                note = ""
                if i and g[i - 1][1] != o:
                    note += f" (was {g[i - 1][2]})"
                if i + 1 < len(g) and g[i + 1][1] != o:
                    note += f" REPLACED on {_d(g[i + 1][0])} by {g[i + 1][2]}"
                ev.append((d, f"{_d(d)} REL {line}{note} (effective {_d(d)}{', ended ' + _d(vt) if vt else ''}) src {src.get(s, s or '?')}", 3))
        terms = {normalize_key(x) for x in (name, *[a for a in (store.query("MATCH (e:Entity {id:$i}) RETURN e.aliases", {"i": eid}, tenant)[0][0] or [])])} | tterms
        docs = {}
        for did, kind, dt, title, cid, text in store.query(
                "MATCH (d:Document)-[:HAS_CHUNK]->(c)-[:MENTIONS]->(e:Entity {id:$i}) RETURN d.id, d.kind, d.date_ms, d.title, c.id, c.text ORDER BY c.id", {"i": eid}, tenant):
            docs.setdefault(did, [kind, dt, title, [], []])
            docs[did][3].append(cid)
            docs[did][4].append(text)
        seen = {c for v in docs.values() for c in v[3]}
        for did, (kind, dt, title, cids, texts) in docs.items():
            fs = _facts("\n".join(texts), terms, 2)
            head = f'{_d(dt)} {kind} [{cids[0]}] "{_t(title, 60)}"'
            ev.append((dt or 0, head + (": " + " | ".join(fs) if fs else f" ({len(cids)} chunks mention it)"), 1.5 if fs else 0))
        for mid, kind, d, text, st, by, bd in store.query(
                "MATCH (m:Memory)-[:MENTIONS]->(e:Entity {id:$i}) WHERE m.status <> 'merged' "
                "OPTIONAL MATCH (n:Memory)-[:SUPERSEDES]->(m) WHERE n.status <> 'merged' "
                "RETURN m.id, m.kind, coalesce(m.valid_from_ms, m.created_ms), m.text, m.status, n.id, coalesce(m.valid_to_ms, n.valid_from_ms, n.created_ms)",
                {"i": eid}, tenant):
            tag = f" SUPERSEDED on {_d(bd)} by [{by}]" if st == "superseded" else ""
            ev.append((d or 0, f"{_d(d)} memory [{mid}] {kind}{tag}: {_t(text, 200)}", 2))
        head = f"# timeline [{eid}] {name} ({typ})"
        extra = not exact  # topic is a phrase that only fuzzily matched an entity: add the dated passages about the phrase itself
    else:
        seen, extra, head = set(), True, f'# timeline "{_t(topic, 60)}" (no entity match; dated recall hits)'
    if extra:
        for r in _recall(store, topic, k=12, since_ms=t0, until_ms=t1, tenant=tenant):
            if r["id"] in seen:
                continue
            fs = _facts(r["text"], tterms, 2) or [_t(r["text"], 160)]
            ev.append((r["date_ms"] or 0, f"{_d(r['date_ms'])} [{r['id']}] {r['kind']}{' SUPERSEDED' if r['status'] == 'superseded' else ''}: " + " | ".join(fs), 1))
    ev = [x for x in sorted(ev, key=lambda x: (x[0], x[1])) if (t0 is None or x[0] >= t0) and (t1 is None or x[0] < t1)]
    if not ev:
        return f'No dated events for "{topic}" in that window.'
    lines = [x[1] for x in ev]
    if sum(len(x) + 1 for x in lines) + len(head) + 20 > max_chars:  # drop the least informative events first, keep chronological order
        keep = set(range(len(ev)))
        for i in sorted(range(len(ev)), key=lambda i: (ev[i][2], i)):
            if sum(len(lines[j]) + 1 for j in keep) + len(head) + 60 <= max_chars:
                break
            keep.discard(i)
        lines = [lines[i] for i in sorted(keep)] + [f"…{len(ev) - len(keep)} more, narrow with since=/until="]
    return _cap([head + ", oldest first", *lines], max_chars, "since=/until=", tail=True)


# ---------------------------------------------------------------- ingest / handoff / cypher

def ingest(store, path_or_text, kind=None, max_chars=MAX, tenant=None) -> str:
    if kind is not None and kind not in DOC_KINDS:
        return f"kind must be one of {', '.join(DOC_KINDS)}"
    p = Path(path_or_text.strip()).expanduser() if len(path_or_text) < 1024 and "\n" not in path_or_text else None
    if p is None or not p.exists():
        # raw text: keep it under NEO_HOME/inbox, named by content hash so re-ingesting the same text is a no-op
        title = _t(path_or_text.strip().splitlines()[0] if path_or_text.strip() else "note", 60).replace('"', "'")
        p = settings().home / "inbox" / f"{content_hash(path_or_text)}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f'---\nkind: {kind or "doc"}\ntitle: "{title}"\ndate: {datetime.now(timezone.utc).date()}\n---\n{path_or_text}\n', encoding="utf-8")
    elif kind:
        return "kind applies to raw text only; for files set `kind:` in the frontmatter"
    c = write.ingest_path(store, p, tenant=tenant)
    return _cap([f"ingested {p}: " + ", ".join(f"{k} {v}" for k, v in c.items())], max_chars, "a smaller path")


def handoff(store, to=None, summary=None, tasks=None, from_agent=None, done=None, max_chars=MAX, tenant=None) -> str:
    """Create a Handoff for agent `to` (shown in its brief), or mark handoff `done` complete."""
    if done:
        r = store.query("MATCH (h:Handoff {id:$i}) SET h.status='done' RETURN h.summary", {"i": done}, tenant)
        return f"handoff [{done}] marked done: {_t(r[0][0], 120)}" if r else f"handoff {done} not found"
    if not to or not summary:
        return "handoff needs `to` and `summary` (or `done=<id>`)"
    hid = new_id("hand")
    store.query("CREATE (:Handoff {id:$i, summary:$s, tasks:$t, status:'open', created_ms:$c})",
                {"i": hid, "s": summary, "t": list(tasks or []), "c": now_ms()}, tenant)
    for who_, edge in ((to, "TO"), (from_agent, "FROM")):
        if who_:
            store.query(f"MERGE (a:Agent {{id:$a}}) ON CREATE SET a.name=$n WITH a MATCH (h:Handoff {{id:$h}}) CREATE (h)-[:{edge}]->(a)",
                        {"a": "agent:" + normalize_key(who_), "n": who_, "h": hid}, tenant)
    return f"handoff [{hid}] open for {to}: it appears in their brief. Mark finished with handoff(done=\"{hid}\")."


def _val(v) -> str:
    if hasattr(v, "labels") and hasattr(v, "properties"):
        props = {k: x for k, x in v.properties.items() if k != "emb"}
        return f"({':'.join(v.labels)} {_t(str(props), 200)})"
    if hasattr(v, "relation"):
        return f"[:{v.relation} {_t(str({k: x for k, x in v.properties.items() if k != 'emb'}), 120)}]"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_val(x) for x in v[:20]) + "]"
    return _t(str(v), 200)


def cypher(store, query, limit=50, max_chars=MAX, tenant=None) -> str:
    """Read-only Cypher via GRAPH.RO_QUERY; adds LIMIT when missing, caps rows and characters."""
    q = query.strip().rstrip(";")
    limit = max(1, min(int(limit), 500))
    if not re.search(r"\blimit\s+\d+\s*$", q, re.I):
        q += f" LIMIT {limit}"
    try:
        res = store.graph(tenant).ro_query(q, timeout=10000)
    except Exception as e:
        return f"rejected or failed (read-only): {_t(str(e), 300)}"
    rows = res.result_set[:limit]
    out = [f"{len(rows)} rows" + (f" (capped at {limit})" if len(res.result_set) > limit else "") + ": " + " | ".join(str(h[1] if isinstance(h, (list, tuple)) else h) for h in res.header)]
    out += [" | ".join(_val(c) for c in r) for r in rows]
    return _cap(out, max_chars, "RETURN fewer columns or a smaller LIMIT")


# ---------------------------------------------------------------- dream

def dream(store, dry_run=False, max_chars=MAX, tenant=None) -> str:
    """Memory consolidation (merge duplicates, promote recurring episodes, decay, flag conflicts). dry_run writes nothing."""
    r = _dream(store, tenant=tenant, dry_run=dry_run)
    what = "dry run, nothing written" if dry_run else r["id"]
    return _cap([f"# dream ({what}): merged {r['merged']}, promoted {r['promoted']}, decayed {r['decayed']}, conflicts {r['conflicts']}"],
                max_chars, "a larger max_chars")
