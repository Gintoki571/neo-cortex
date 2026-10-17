import json
import threading

import pytest

from neo_cortex import extract as X
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


def _rels(spec, wins, title="", gl=(), kind=""):
    """Relations from the pattern rules alone (GLiNER output is an explicit argument): spec = [(name, type)]."""
    from neo_cortex.util import normalize_key
    ents = {normalize_key(n): {"name": n, "type": t, "conf": 0.9} for n, t in spec}
    return {(r["head"], r["type"], r["tail"]) for r in X._relations(ents, wins, list(gl), title, kind=kind)}


def _ms(y, m, d):
    from datetime import datetime, timezone
    return int(datetime(y, m, d, tzinfo=timezone.utc).timestamp() * 1000)


SVC = [("orders-service", "service"), ("ledger-cache", "service"), ("quota-store", "service"),
       ("billing-api", "service"), ("fraud-check", "service")]


def test_depends_on_phrasings():
    got = _rels(SVC, ["orders-service relies on ledger-cache.", "orders-service reads from quota-store.",
                      "orders-service needs billing-api.", "quota-store is downstream of billing-api.",
                      "orders-service uses fraud-check.",
                      "fraud-check feeds the scoring model that billing-api consults before each payment."])
    assert got == {("orders-service", "DEPENDS_ON", "ledger-cache"), ("orders-service", "DEPENDS_ON", "quota-store"),
                   ("orders-service", "DEPENDS_ON", "billing-api"), ("quota-store", "DEPENDS_ON", "billing-api"),
                   ("orders-service", "DEPENDS_ON", "fraud-check"), ("billing-api", "DEPENDS_ON", "fraud-check")}


def test_depends_on_implicit_subject_is_the_chunk_service():
    # "It" is the most-mentioned service of the chunk; a passive or subject-less sentence takes it as head too
    assert ("orders-service", "DEPENDS_ON", "ledger-cache") in _rels(
        SVC, ["orders-service handles payouts.", "orders-service is busy.", "It relies on ledger-cache."])
    assert _rels(SVC[:2], ["ledger-cache is the cache.", "orders-service is busy.", "orders-service is busy."]) == set()
    got = _rels(SVC, ["ledger-cache is the public API.", "The payment goes to fraud-check for a risk decision.",
                      "The approved payment is then written into quota-store."])
    assert got == {("ledger-cache", "DEPENDS_ON", "fraud-check"), ("ledger-cache", "DEPENDS_ON", "quota-store")}


def test_broker_role_and_publish_to_broker():
    got = _rels([("event-pipeline", "service"), ("ledger-service", "service")],
                ["event-pipeline is the message broker.", "ledger-service is the main producer.",
                 "It publishes its events through a publisher, which hands them to the broker."])
    assert got == {("ledger-service", "DEPENDS_ON", "event-pipeline")}


def test_owns_phrasings():
    assert ("Platform", "OWNS", "orders-service") in _rels(
        [("Platform", "team"), ("orders-service", "service")], ["Platform owns orders-service."])
    assert ("Lukas Brandt", "OWNS", "orders-service") in _rels(
        [("Lukas Brandt", "person"), ("orders-service", "service")], ["orders-service handles payouts.", "Owner: Lukas Brandt."])
    assert ("Mateo Alvarez", "OWNS", "orders-service") in _rels(
        [("Mateo Alvarez", "person"), ("orders-service", "service")], ["Mateo Alvarez is on-call for orders-service."])
    assert ("Mateo Alvarez", "OWNS", "orders-service") in _rels(
        [("Mateo Alvarez", "person"), ("orders-service", "service")], ["Mateo Alvarez is responsible for orders-service."])


def test_owner_line_is_the_task_owner_in_tickets_and_meetings():
    spec = [("Olivia Hartmann", "person"), ("ledger-service", "service")]
    text = ["ledger-service publishes events.", "Owner: Olivia Hartmann."]
    assert _rels(spec, text, kind="ticket") == set()  # DATA-325: the assignee of a task, not ledger-service's owner
    assert _rels(spec, text, kind="meeting") == set()
    assert ("Olivia Hartmann", "OWNS", "ledger-service") in _rels(spec, text, kind="doc")  # a doc describing the service
    assert ("Olivia Hartmann", "OWNS", "ledger-service") in _rels(spec, ["Owner: Olivia Hartmann (ledger-service)."], kind="ticket")


def test_renamed_formerly_and_now_called():
    assert _rels(SVC[1:3], ["ledger-cache is now called quota-store."]) == {("ledger-cache", "RENAMED_TO", "quota-store")}
    assert _rels(SVC[1:3], ["quota-store (formerly ledger-cache) is live."]) == {("ledger-cache", "RENAMED_TO", "quota-store")}


def test_caused_by_and_fixed_phrasings():
    spec = [("INC-07", "incident"), ("cache-pool", "component")]
    assert ("INC-07", "CAUSED_BY", "cache-pool") in _rels(spec, ["The root cause was memory pressure in cache-pool."])
    assert ("INC-07", "CAUSED_BY", "cache-pool") in _rels(spec, ["INC-07 was caused by cache-pool."])
    assert ("INC-07", "CAUSED_BY", "cache-pool") in _rels(spec, ["INC-07 was triggered by cache-pool."])


def test_decided_and_approved_by():
    spec = [("ADR-005", "decision"), ("Sofia Marchetti", "person"), ("Tobias Wren", "person")]
    assert _rels(spec, ["ADR-005 was decided by Sofia Marchetti.", "ADR-005 was approved by Tobias Wren."]) == {
        ("Sofia Marchetti", "DECIDED", "ADR-005"), ("Tobias Wren", "APPROVED", "ADR-005")}
    assert ("Tobias Wren", "APPROVED", "ADR-005") in _rels(spec, ["Tobias Wren signed off on ADR-005."])


def test_table_rows_are_read_row_by_row():
    text = ("| Service | Owner | Depends on |\n|---|---|---|\n"
            "| orders-service | Mateo Alvarez | ledger-cache, quota-store |\n"
            "| billing-api | Lukas Brandt | ledger-cache |\n")
    facts = {(h, r, t) for h, r, t, _, _ in X._table_facts(text)}
    assert facts == {("Mateo Alvarez", "OWNS", "orders-service"), ("orders-service", "DEPENDS_ON", "ledger-cache"),
                     ("orders-service", "DEPENDS_ON", "quota-store"), ("Lukas Brandt", "OWNS", "billing-api"),
                     ("billing-api", "DEPENDS_ON", "ledger-cache")}


def test_former_owner_passing_mention_is_not_ownership():
    spec = [("Lukas Brandt", "person"), ("session-cache", "service"), ("Mateo Alvarez", "person")]
    gl = [{"relation_extraction": {"owns": [{"head": {"text": "Lukas Brandt"}, "tail": {"text": "session-cache"},
                                             "confidence": 0.9}]}}]
    assert _rels(spec, ["Lukas Brandt was the former owner of session-cache, and reviewed the change."], gl=gl) == set()
    assert _rels(spec, ["Lukas Brandt is the former owner of session-cache."]) == set()
    assert _rels(spec, ["Lukas Brandt, who used to own session-cache, reviewed the change."]) == set()
    # positive controls: the same shapes without the former-state cue assert ownership
    assert ("Lukas Brandt", "OWNS", "session-cache") in _rels(spec, ["Lukas Brandt owns session-cache."], gl=gl)
    assert ("Mateo Alvarez", "OWNS", "session-cache") in _rels(spec, ["Mateo Alvarez is the owner of session-cache."])


def test_effective_date_is_the_validity_start():
    spec = [("Mateo Alvarez", "person"), ("session-cache", "service")]
    for sen in ["Mateo Alvarez owns session-cache, effective 2026-08-15.", "Mateo Alvarez owns session-cache from 15 August 2026.",
                "Mateo Alvarez owns session-cache starting Aug 15, 2026."]:
        rels = X._relations({"mateo alvarez": {"name": "Mateo Alvarez", "type": "person", "conf": 0.9},
                             "session cache": {"name": "session-cache", "type": "service", "conf": 0.9}}, [sen], [], "")
        owns = [r for r in rels if r["type"] == "OWNS"]
        assert owns and owns[0]["valid_from_ms"] == _ms(2026, 8, 15), sen


def test_effective_owner_change_closes_the_old_edge(store, fake_models, tmp_path, monkeypatch):
    eff = _ms(2026, 8, 15)

    def fake(texts, titles=None, authors=None, teams=(), kind=""):
        out = []
        for t in texts:
            ents = [{"name": n, "type": "person", "conf": 0.9} for n in ("Lukas Brandt", "Mateo Alvarez")]
            ents.append({"name": "session-cache", "type": "service", "conf": 0.9})
            rel = {"head": "Mateo Alvarez", "type": "OWNS", "tail": "session-cache", "conf": 0.9, "valid_from_ms": eff} \
                if "effective" in t else {"head": "Lukas Brandt", "type": "OWNS", "tail": "session-cache", "conf": 0.9}
            out.append({"entities": ents, "relations": [rel]})
        return out
    monkeypatch.setattr(X, "extract_batch", fake)
    d = tmp_path / "docs"
    d.mkdir()
    (d / "a.md").write_text(_doc("a", "2026-06-01T09:00:00Z", "Lukas Brandt owns session-cache."))
    (d / "b.md").write_text(_doc("b", "2026-09-01T09:00:00Z", "Mateo Alvarez takes over session-cache, effective 2026-08-15."))
    write.ingest_path(store, d)
    rows = _q(store, "MATCH (a:Entity)-[r:REL {type:'OWNS'}]->(:Entity) RETURN a.name, r.valid_from_ms, r.valid_to_ms ORDER BY r.valid_from_ms")
    # the old edge ends where the new one starts (the stated date, not the document date 2026-09-01); the new one is open
    assert [r[0] for r in rows] == ["Lukas Brandt", "Mateo Alvarez"] and rows[1][1] == eff and rows[0][2] == eff and rows[1][2] is None


def test_number_or_negation_difference_is_a_conflict(store, fake_models, monkeypatch):
    import numpy as np
    # the embedder sees the two sentences as the same vector: only the number or negation can tell them apart
    monkeypatch.setattr(write, "embed_docs", lambda texts, titles=None: np.tile(np.eye(768, dtype=np.float32)[0], (len(texts), 1)))
    a = write.remember(store, "keep window at 24 hours")
    b = write.remember(store, "keep window at 48 hours")
    assert b["status"] == "created" and [c["id"] for c in b["conflicts"]] == [a["id"]]
    assert _q(store, "MATCH (m:Memory {id:$m}) RETURN m.uses", m=a["id"]) == [[0]]
    c = write.remember(store, "keep window at 48 hours")
    assert c["status"] == "reinforced" and c["id"] == b["id"]
    n = write.remember(store, "Sessions may expire after 24 hours")
    m = write.remember(store, "Sessions may not expire after 24 hours")
    assert m["status"] == "created" and n["id"] in [x["id"] for x in m["conflicts"]]


def test_unicode_names_keep_their_key():
    from neo_cortex.util import normalize_key
    assert normalize_key("田中") == "田中" and normalize_key("Ékó") == "ékó"
    assert normalize_key("Auth_Service!") == "auth service"


def test_empty_key_creates_no_entity(store, fake_models):
    assert resolve.resolve_entity(store, "!!!", "other") is None
    assert store.query("MATCH (e:Entity) WHERE e.key = '' RETURN count(e)") == [[0]]


def test_find_tolerates_an_empty_key():
    from neo_cortex.extract import _find
    ents = {"": {"name": "!!!", "type": "person", "conf": 0.9}, "bob ross": {"name": "Bob Ross", "type": "person", "conf": 0.9}}
    assert _find(ents, "Ross") == "bob ross"
    assert _find(ents, "Alice") is None


def test_frontmatter_id_collision_skips_the_second_file(store, fake_models, tmp_path, capsys):
    d = tmp_path / "docs"  # the store home is tmp_path itself, so keep the ingested tree apart from it
    d.mkdir()
    a, b = d / "a.md", d / "b.md"
    a.write_text("---\nid: same\n---\n\nNoor Haddad owns auth-service.\n")
    b.write_text("---\nid: same\n---\n\nSamir Haddad owns billing-service.\n")
    r = write.ingest_path(store, d)
    assert r["documents"] == 1 and r["errors"] == 1
    assert "id collision with" in capsys.readouterr().err
    assert store.query("MATCH (d:Document {id:'same'}) RETURN d.path") == [[str(a)]]


def test_crash_mid_ingest_leaves_no_partial_document(store, fake_models, tmp_path, monkeypatch):
    f = tmp_path / "a.md"
    f.write_text("Noor Haddad owns auth-service.\n")
    real = write._refresh_entities

    def boom(*a, **k):
        raise RuntimeError("crash")

    monkeypatch.setattr(write, "_refresh_entities", boom)
    with pytest.raises(RuntimeError, match="crash"):
        write._ingest_doc(store, f, None)
    assert store.query("MATCH (d:Document) RETURN count(d)") == [[0]]
    assert store.query("MATCH (c:Chunk) RETURN count(c)") == [[0]]
    monkeypatch.setattr(write, "_refresh_entities", real)
    assert write._ingest_doc(store, f, None)["documents"] == 1  # retried, not skipped


@pytest.mark.parametrize("op", ["remember", "ingest_path"])
def test_writes_wait_for_the_store_write_lock(store, fake_models, tmp_path, monkeypatch, op):
    f = tmp_path / "a.md"
    f.write_text("Noor Haddad owns auth-service.\n")
    reached = threading.Event()
    real_embed = write.embed_docs

    def spy(*a, **k):  # both writers embed before they create anything: that must wait for the lock
        reached.set()
        return real_embed(*a, **k)

    monkeypatch.setattr(write, "embed_docs", spy)
    call = {"remember": lambda: write.remember(store, "Deploys happen on Tuesdays"),
            "ingest_path": lambda: write.ingest_path(store, f)}[op]
    store.write_lock.acquire()
    try:
        out = {}
        t = threading.Thread(target=lambda: out.update(r=call()))
        t.start()
        assert not reached.wait(0.5)
    finally:
        store.write_lock.release()
    t.join(60)
    assert reached.is_set() and "r" in out


def test_titles_from_heading_or_parent_dir(store, fake_models, tmp_path):
    d = tmp_path / "wiki"
    d.mkdir()
    (d / "index.md").write_text("Intro text.\n\n## Not a title\n\n```\n# shell comment\n```\n\n# Design notes\n\nBody text here.\n")
    (d / "log.md").write_text("Only prose, no heading at all.\n")
    (d / "README.md").write_text("---\ntitle: Real Title\n---\n\n# Ignored heading\n\nBody.\n")
    write.ingest_path(store, d)
    titles = dict(_q(store, "MATCH (d:Document) RETURN d.path, d.title"))
    assert titles[str(d / "index.md")] == "Design notes"
    assert titles[str(d / "log.md")] == "wiki/log"
    assert titles[str(d / "README.md")] == "Real Title"


def test_frontmatter_type_description_tags_are_stored_and_searchable(store, fake_models, tmp_path):
    f = tmp_path / "decision.md"
    f.write_text("---\ntype: Decision\ntitle: Queue choice\ndescription: Picked the outbox pattern over direct sends.\n"
                 "tags: [messaging, outbox]\nstatus: draft\n---\n\n# Queue choice\n\nWe write events to a table first.\n")
    write.ingest_path(store, f)
    row = _q(store, "MATCH (d:Document) RETURN d.kind, d.doc_type, d.description, d.tags, d.status")[0]
    assert row == ["doc", "Decision", "Picked the outbox pattern over direct sends.", ["messaging", "outbox"], "draft"]
    text = _q(store, "MATCH (c:Chunk) RETURN c.text ORDER BY c.pos LIMIT 1")[0][0]
    assert text.startswith("Picked the outbox pattern over direct sends.")  # the description is in the first chunk text


def test_tags_as_comma_string_and_missing_fields(store, fake_models, tmp_path):
    f = tmp_path / "plain.md"
    f.write_text("---\ntags: alpha, beta\n---\n\nJust a body with no heading.\n")
    write.ingest_path(store, f)
    assert _q(store, "MATCH (d:Document) RETURN d.tags, d.doc_type, d.description") == [[["alpha", "beta"], None, None]]
