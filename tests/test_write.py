import json

from neo_cortex import resolve, write
from neo_cortex.cli import main

DOC = """---
id: tkt-1
kind: ticket
title: "IDN-1: remember device"
date: 2026-06-12T09:30:00Z
author: Lukas Brandt
participants: [Lukas Brandt, Noor Haddad]
status: closed
labels: [identity]
---

# IDN-1: remember device

Noor Haddad owns auth-service and reviewed the change.

## Comments

**Noor Haddad (2026-06-12):** looks fine.
"""
CHAT = """---
id: chat-1
kind: chat
title: "#identity"
date: 2026-06-04T09:00:00Z
author: Ravi Chandrasekar
participants: [Ravi Chandrasekar, Noor Haddad]
---

# #identity

**[2026-06-04 09:00] Ravi Chandrasekar:** morning
**[2026-06-04 09:03] Noor Haddad:** hi, session-cache is fine
"""


def _q(s, c, **p):
    return s.query(c, p)


def test_chunking():
    assert len(write.chunk_text("a b c\n\nd e f")) == 1
    long = "\n\n".join("word " * 100 for _ in range(6))
    cs = write.chunk_text(long)
    assert len(cs) >= 2 and all(len(c.split()) <= write.CHUNK_MAX for c in cs)
    chat = "\n".join(f"**[2026-01-01 09:{i:02d}] A B:** " + "word " * 30 for i in range(12))
    assert all(c.count("**[") >= 2 for c in write.chunk_text(chat, "chat"))


def test_ingest_two_docs_and_idempotence(store, fake_models, tmp_path):
    d = tmp_path / "docs"
    d.mkdir()
    (d / "a.md").write_text(DOC)
    (d / "b.md").write_text(CHAT)
    r = write.ingest_path(store, d)
    assert r["documents"] == 2 and r["errors"] == 0 and r["chunks"] >= 2
    assert _q(store, "MATCH (d:Document) RETURN count(d)") == [[2]]
    # tickets keep the document date on chunks, REL carries chunk source and document date
    date = _q(store, "MATCH (d:Document {id:'tkt-1'}) RETURN d.date_ms")[0][0]
    assert date == 1781256600000
    assert _q(store, "MATCH (c:Chunk {doc_id:'tkt-1'}) RETURN DISTINCT c.date_ms") == [[date]]
    rel = _q(store, "MATCH (a:Entity)-[r:REL]->(b:Entity) RETURN a.name, r.type, b.name, r.source_id, r.valid_from_ms")
    assert rel[0][:3] == ["Noor Haddad", "OWNS", "auth-service"] and rel[0][3].startswith("tkt-1#") and rel[0][4] == date
    assert _q(store, "MATCH (e:Entity {key:'lukas brandt'})-[:AUTHORED]->(d) RETURN d.id") == [["tkt-1"]]
    assert sorted(x[0] for x in _q(store, "MATCH (e:Entity {key:'noor haddad'})-[:PARTICIPATED]->(d) RETURN d.id")) == ["chat-1", "tkt-1"]
    assert _q(store, "MATCH (e:Entity {key:'noor haddad'}) RETURN e.mentions")[0][0] == 2
    counts = _q(store, "MATCH (n) RETURN count(n)")
    # unchanged: skipped, nothing added
    r2 = write.ingest_path(store, d)
    assert r2["skipped"] == 2 and r2["documents"] == 0 and _q(store, "MATCH (n) RETURN count(n)") == counts
    # changed: chunks replaced, no duplicates
    (d / "a.md").write_text(DOC.replace("looks fine", "needs another pass"))
    r3 = write.ingest_path(store, d)
    assert r3["documents"] == 1 and r3["skipped"] == 1
    assert _q(store, "MATCH (d:Document {id:'tkt-1'}) RETURN count(d)") == [[1]]
    assert _q(store, "MATCH (c:Chunk {doc_id:'tkt-1'}) WHERE c.text CONTAINS 'looks fine' RETURN count(c)") == [[0]]
    assert _q(store, "MATCH ()-[r:REL]->() RETURN count(r)") == [[1]]


def test_remember_dedupe_reinforce(store, fake_models):
    a = write.remember(store, "Always run pytest with NEO_TEST_PORT set to avoid port collisions")
    b = write.remember(store, "Always run pytest with NEO_TEST_PORT set to avoid port collisions")
    assert a["status"] == "created" and b["status"] == "reinforced" and b["id"] == a["id"]
    assert _q(store, "MATCH (m:Memory) RETURN count(m), max(m.uses)") == [[1, 1]]


def test_remember_conflict_and_supersedes(store, fake_models):
    a = write.remember(store, "The session TTL is 900 seconds for auth-service", kind="semantic", agent="claude-code")
    b = write.remember(store, "The session TTL is 3600 seconds for auth-service")
    assert b["status"] == "created" and [c["id"] for c in b["conflicts"]] == [a["id"]]
    assert 0.75 <= b["conflicts"][0]["sim"] < 0.92
    c = write.remember(store, "Session TTL moved to 300 seconds on auth-service", supersedes=a["id"])
    assert c["status"] == "created"
    assert _q(store, "MATCH (n:Memory {id:$n})-[:SUPERSEDES]->(o:Memory) RETURN o.id, o.status, o.valid_to_ms IS NOT NULL", n=c["id"]) == [[a["id"], "superseded", True]]
    assert _q(store, "MATCH (:Agent {name:'claude-code'})-[:WROTE]->(m:Memory) RETURN count(m)") == [[1]]


def test_resolve(store, fake_models):
    p = resolve.resolve_many(store, [("Viktor Sokolov", "person"), ("api-gateway", "component")])
    assert resolve.resolve_entity(store, "Viktor", "person") == p[0]            # lone first name, unique person
    assert resolve.resolve_entity(store, "Api Gateway", "service") == p[1]       # same key
    assert _q(store, "MATCH (e:Entity {id:$i}) RETURN e.type", i=p[1]) == [["service"]]  # type upgraded
    n = resolve.resolve_entity(store, "Noor Haddad", "person")
    s = resolve.resolve_entity(store, "Samir Haddad", "person")
    assert n != s
    j1 = resolve.judge(store, "q", "a = b ?", ["same", "different"])
    j2 = resolve.judge(store, "q", "a = b ?", ["same", "different"])
    assert j1 == j2 and _q(store, "MATCH (j:Judgment) RETURN count(j)") == [[1]]


def test_cli_version(capsys):
    assert main(["--version"]) == 0 and capsys.readouterr().out.strip()


def test_chunk_tail_fold():
    cs = write.chunk_text("\n\n".join(["w " * 130, "x " * 130, "tiny tail"]))
    assert len(cs) == 2 and cs[-1].endswith("tiny tail")


def test_chunk_hard_split():
    code = "\n".join(f"line_{i} = compute(a, b, c, d)" for i in range(600))   # one paragraph, no sentences
    cs = write.chunk_text(code)
    assert len(cs) > 1 and all(len(c.split()) <= write.CHUNK_MAX and len(c) <= write.MAX_CHARS for c in cs)
    assert len(write.chunk_text("x" * 20000)) > 1


def _doc(i, date, body, labels="[]"):
    return f"---\nid: {i}\nkind: doc\ntitle: {i}\ndate: {date}\nauthor: Ann Lee\nlabels: {labels}\n---\n\n{body}\n"


def test_single_valued_owner_is_closed_by_a_later_one(store, fake_models, tmp_path):
    (tmp_path / "a.md").write_text(_doc("a", "2026-06-01T09:00:00Z", "Lukas Brandt owns session-cache."))
    (tmp_path / "b.md").write_text(_doc("b", "2026-09-01T09:00:00Z", "Mateo Alvarez owns session-cache.", "[session-cache]"))
    write.ingest_path(store, tmp_path)
    rows = _q(store, "MATCH (a:Entity)-[r:REL {type:'OWNS'}]->(:Entity) RETURN a.name, r.valid_from_ms, r.valid_to_ms ORDER BY r.valid_from_ms")
    assert rows[0][0] == "Lukas Brandt" and rows[0][2] == rows[1][1] and rows[1][2] is None
    # label session-cache on doc b: its chunk mentions the entity once
    assert _q(store, "MATCH (:Chunk {doc_id:'b'})-[m:MENTIONS]->(e:Entity {key:'session cache'}) RETURN count(m)") == [[1]]


def test_patterns_and_generic_filter():
    from neo_cortex import extract as X
    ents = {k: {"name": n, "type": t, "conf": 0.9} for k, n, t in [
        ("viktor sokolov", "Viktor Sokolov", "person"), ("api gateway", "api-gateway", "service"),
        ("auth service", "auth-service", "service"), ("bankbridge", "bankbridge", "service"),
        ("bank connector", "bank-connector", "service"), ("tobias wren", "Tobias Wren", "person"),
        ("adr 005", "ADR-005", "decision")]}
    wins = ["Viktor owns the gateway.", "The gateway calls auth-service on every request.",
            "bank-connector (formerly bankbridge) is live.", "Decided by: Tobias Wren (CTO)"]
    got = {(r["head"], r["type"], r["tail"]) for r in X._relations(ents, wins, [], "ADR-005: rename")}
    assert got == {("Viktor Sokolov", "OWNS", "api-gateway"), ("api-gateway", "DEPENDS_ON", "auth-service"),
                   ("bankbridge", "RENAMED_TO", "bank-connector"), ("Tobias Wren", "DECIDED", "ADR-005")}
    assert all(X._junk(n, "component") for n in ["other services", "Platform engineer", "new file", "config file"])
    assert not X._junk("Noor Haddad", "person") and not X._junk("session-cache", "service")
