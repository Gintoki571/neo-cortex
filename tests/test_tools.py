import numpy as np
import pytest
from test_retrieve import FakeGliner, ms, vec

from neo_cortex import models, resolve, tools, write
from neo_cortex.retrieve import channels as ch

NOW = ms("2026-10-16T12:00:00")


class G(FakeGliner):
    NAMES = {"checkout": "service", "platform team": "team", "payments team": "team", "auth service": "service",
             "priya shah": "person", "session_ttl": "config setting"}


@pytest.fixture(autouse=True)
def fakes(monkeypatch):
    monkeypatch.setattr(models, "embed_query", vec)
    monkeypatch.setattr(models, "embed_docs", lambda texts, titles=None: np.stack([vec(t) for t in texts]))
    monkeypatch.setattr(models, "gliner", lambda: G())
    monkeypatch.setattr(resolve, "embed_docs", lambda texts, titles=None: np.stack([vec(t) for t in texts]))


@pytest.fixture
def g(store):
    q = store.query
    for i, n, t in [("e_priya", "Priya Shah", "person"), ("e_plat", "Platform Team", "team"), ("e_pay", "Payments Team", "team"),
                    ("e_auth", "Auth Service", "service"), ("e_ck", "Checkout", "service"), ("e_ttl", "SESSION_TTL", "config_setting")]:
        q("CREATE (:Entity {id:$i, name:$n, key:$k, type:$t, mentions:1, emb:vecf32($e)})",
          {"i": i, "n": n, "k": ch.key_of(n), "t": t, "e": vec(n).tolist()})
    q("CREATE (:Document {id:'d1', kind:'doc', title:'Platform runbook', author:'Priya Shah', date_ms:$d}), "
      "(:Document {id:'d2', kind:'adr', title:'ADR-7 auth ownership', date_ms:$e})", {"d": ms("2026-03-05T00:00:00"), "e": ms("2026-02-01T00:00:00")})
    for cid, did, text, d, e in [("d1#0", "d1", "Auth Service ownership moved to the Platform Team runbook", "2026-03-05", "e_auth"),
                                 ("d2#0", "d2", "Payments Team handed Auth Service to Platform Team", "2026-02-01", "e_auth"),
                                 ("d1#1", "d1", "SESSION_TTL is 300 seconds", "2026-03-05", "e_ttl")]:
        q("MATCH (d:Document {id:$d}) CREATE (d)-[:HAS_CHUNK]->(c:Chunk {id:$i, doc_id:$d, pos:$p, text:$t, kind:d.kind, date_ms:$m, emb:vecf32($v)}) "
          "WITH c MATCH (e:Entity {id:$e}) CREATE (c)-[:MENTIONS {conf:1.0}]->(e)",
          {"d": did, "i": cid, "p": int(cid.split("#")[1]), "t": text, "m": ms(d + "T00:00:00"), "v": vec(text).tolist(), "e": e})
    q("MATCH (p:Entity {id:'e_priya'}), (d:Document {id:'d1'}) CREATE (p)-[:AUTHORED]->(d)")
    for a, t, b, d, src in [("e_priya", "MEMBER_OF", "e_plat", "2026-01-01", "d1#0"), ("e_pay", "OWNS", "e_auth", "2025-06-01", "d2#0"),
                            ("e_plat", "OWNS", "e_auth", "2026-02-01", "d2#0"), ("e_ck", "DEPENDS_ON", "e_auth", "2025-09-01", "d1#0")]:
        q("MATCH (a:Entity {id:$a}), (b:Entity {id:$b}) CREATE (a)-[:REL {type:$t, conf:0.9, source_id:$s, valid_from_ms:$d}]->(b)",
          {"a": a, "b": b, "t": t, "s": src, "d": ms(d + "T00:00:00")})
    for i, kind, text, st, d in [("m_pref", "preference", "Always run tests with uv run --no-sync", "active", "2026-09-01"),
                                 ("m_dec", "decision", "Use RS256 for Auth Service tokens", "active", "2026-09-10"),
                                 ("m_old", "semantic", "Auth Service sessions expire after 60 seconds", "superseded", "2026-01-11"),
                                 ("m_new", "semantic", "Auth Service sessions expire after 300 seconds", "active", "2026-03-06")]:
        q("CREATE (:Memory {id:$i, kind:$k, text:$t, status:$s, confidence:0.9, created_ms:$d, valid_from_ms:$d, uses:2, agent:'claude-code', emb:vecf32($v)})",
          {"i": i, "k": kind, "t": text, "s": st, "d": ms(d + "T00:00:00"), "v": vec(text).tolist()})
    q("MATCH (a:Memory {id:'m_new'}),(b:Memory {id:'m_old'}) CREATE (a)-[:SUPERSEDES]->(b)")
    q("MATCH (m:Memory {id:'m_new'}),(e:Entity {id:'e_auth'}) CREATE (m)-[:MENTIONS {conf:1.0}]->(e)")
    q("MATCH (m:Memory {id:'m_old'}),(e:Entity {id:'e_auth'}) CREATE (m)-[:MENTIONS {conf:1.0}]->(e)")
    return store


def test_who_two_hop_owner(g):
    out = tools.who(g, "Auth Service")
    print(out)
    assert out.index("Priya Shah") < 400 and "Priya Shah -[MEMBER_OF]-> Platform Team -[OWNS]-> Auth Service" in out
    assert "[d1]" in out  # authored evidence id


def test_connect_path_and_sources(g):
    out = tools.connect(g, "Priya Shah", "Checkout")
    print(out)
    assert "Priya Shah -[MEMBER_OF]-> Platform Team -[OWNS]-> Auth Service <-[DEPENDS_ON]- Checkout" in out
    assert "Platform runbook" in out
    assert "No path" in tools.connect(g, "Priya Shah", "SESSION_TTL")


def test_timeline_owner_change_in_order(g):
    out = tools.timeline(g, "Auth Service")
    print(out)
    assert out.index("Payments Team -[OWNS]-> Auth Service") < out.index("Platform Team -[OWNS]-> Auth Service")
    assert "REPLACED on 2026-02-01 by Platform Team" in out and "(was Payments Team)" in out
    assert "SUPERSEDED on 2026-03-06 by [m_new]" in out
    dates = [l[:10] for l in out.split("Events:")[1].splitlines() if l[:2] == "20"]
    assert dates == sorted(dates)
    assert "2025-06-01" not in tools.timeline(g, "Auth Service", since="2026-01-01")


def test_cypher_readonly_and_cap(g):
    assert tools.cypher(g, "CREATE (:X {id:'x'})").startswith("rejected")
    assert g.query("MATCH (x:X) RETURN count(x)")[0][0] == 0
    out = tools.cypher(g, "MATCH (e:Entity) RETURN e LIMIT 100", limit=3)
    assert out.startswith("3 rows (capped at 3)") and "emb" not in out
    assert tools.cypher(g, "MATCH (e:Entity) RETURN e.name LIMIT 2").startswith("2 rows")


def test_handoff_in_brief(g):
    out = tools.handoff(g, to="codex", summary="Finish the auth migration", tasks=["rotate keys", "update runbook"], from_agent="claude-code")
    hid = out.split("[")[1].split("]")[0]
    assert "Finish the auth migration" in tools.brief(g, agent="codex")
    assert "Finish the auth migration" not in tools.brief(g, agent="someone-else")
    tools.handoff(g, done=hid)
    assert "Finish the auth migration" not in tools.brief(g, agent="codex")


def test_brief_sections(g):
    out = tools.brief(g)
    print(out)
    for s in ("Preferences", "Active decisions", "Recent documents", "[m_pref]", "[m_dec]"):
        assert s in out
    assert "[m_old]" not in out  # superseded stays hidden


def test_brief_excludes_noise_and_raw_quotes(g):
    g.query(
        "CREATE (:Memory {id:'m_sentiment', kind:'episodic', text:'The user felt frustrated about the failed demo.', "
        "status:'active', confidence:0.9, created_ms:$d, uses:1})",
        {"d": ms("2026-10-01T00:00:00")},
    )
    g.query(
        "CREATE (:Memory {id:'m_quote', kind:'semantic', text:'\"This is a raw user quote that should not enter the brief.\"', "
        "status:'active', confidence:0.9, created_ms:$d, uses:1})",
        {"d": ms("2026-10-02T00:00:00")},
    )
    out = tools.brief(g)
    assert "[m_sentiment]" not in out
    assert "[m_quote]" not in out


def test_ask_expands_evidence_budget(g, monkeypatch):
    def result(i):
        return {
            "id": f"m_ask_{i}",
            "label": "Memory",
            "kind": "semantic",
            "date_ms": NOW,
            "status": "active",
            "text": f"Evidence item {i} records the hackathon submission requirements and deadline.",
            "source": {"agent": "codex", "project": "neo-cortex", "source_id": None},
            "channels": {"dense": i + 1},
            "paths": [],
        }

    seen = []

    def recall(*args, **kwargs):
        seen.append(kwargs["k"])
        return [result(i) for i in range(kwargs["k"])]

    monkeypatch.setattr(tools, "_recall", recall)
    out = tools.ask(g, "hackathon submission requirements", max_chars=12000)
    assert seen[0] > 8
    assert 4200 < len(out) <= 12000


def test_ask_keeps_more_evidence_within_default_budget(g, monkeypatch):
    def result(i):
        return {
            "id": f"m_budget_{i}",
            "label": "Memory",
            "kind": "semantic",
            "date_ms": NOW,
            "status": "active",
            "text": f"Evidence item {i} records the hackathon submission requirements and deadline. "
                    "The supporting document also describes the review process and the final submission window.",
            "source": {"agent": "documentation-agent", "project": "neo-cortex-research", "source_id": None},
            "channels": {"dense": i + 1},
            "paths": [],
        }

    monkeypatch.setattr(tools, "_recall", lambda *args, **kwargs: [result(i) for i in range(kwargs["k"])])
    out = tools.ask(g, "hackathon submission requirements", max_chars=4000)
    assert out.count("semantic | memory |") >= 12


def test_ask_compacts_path_sources(g):
    paths = [([["e_priya", "Priya Shah"], ["e_plat", "Platform Team"]],
              [["MEMBER_OF", "e_priya", "d1#0", NOW, 0.9, None, "fact"]])]
    full = tools._path_lines(g, paths, None)
    compact = tools._path_lines(g, paths, None, compact=True)
    assert len(compact[1]) < len(full[1])
    assert "d1#0" in compact[1]


def test_max_chars_respected(g):
    for fn, args in [(tools.brief, ()), (tools.timeline, ("Auth Service",)), (tools.recall, ("auth service",)), (tools.ask, ("who owns Auth Service",)),
                     (tools.explore, ("Auth Service",)), (tools.cypher, ("MATCH (e:Entity) RETURN e",))]:
        full = fn(g, *args, max_chars=100000)
        small = fn(g, *args, max_chars=300)
        assert len(small) <= 300 and len(full) > 300, fn.__name__
        assert "more, narrow with" in small, fn.__name__


def test_recall_and_ask_and_explore(g):
    out = tools.recall(g, "auth service sessions expire", k=3)
    print(out)
    assert "[m_new]" in out and "via" in out
    out = tools.ask(g, "who owns Auth Service and how does Checkout connect to it")
    print(out)
    assert "Seeds" in out and "Suggested next" in out and "Evidence" in out
    out = tools.explore(g, "Auth Service", hops=2)
    print(out)
    assert "Checkout" in out and "Platform runbook" in out and "Priya Shah" in out
    assert "No entity" in tools.explore(g, "zzqx unknown")


def test_remember_wraps_write(g, monkeypatch):
    monkeypatch.setattr(write, "remember", lambda store, text, **kw: {"id": "mem_1", "status": "created", "kind": "decision", "entities": ["Auth Service"],
                                                                      "conflicts": [{"id": "m_new", "text": "Auth Service sessions expire after 300 seconds", "sim": 0.8}]})
    out = tools.remember(g, "Auth Service sessions expire after 600 seconds", supersedes="m_new")
    assert "created [mem_1]" in out and "superseded m_new" in out and "supersedes=<id>" in out and "[m_new] sim 0.80" in out
    assert "not found" in tools.remember(g, "x", supersedes="nope")


def test_ingest_text_and_path(g, monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(write, "ingest_path", lambda store, p, tenant=None: calls.append(p) or {"documents": 1})
    f = tmp_path / "a.md"
    f.write_text("hello")
    assert "documents 1" in tools.ingest(g, str(f))
    assert "documents 1" in tools.ingest(g, "A decision note\nwe use RS256", kind="adr")
    assert calls[0] == f and calls[1].read_text().startswith("---\nkind: adr")
    assert tools.ingest(g, "A decision note\nwe use RS256", kind="adr") and calls[2] == calls[1]  # same text, same file


def test_merged_memory_never_surfaces(g):
    from neo_cortex.retrieve import recall
    t = "Auth Service sessions expire after 900 seconds"  # a dream duplicate: same topic, so every channel would rank it
    g.query("CREATE (:Memory {id:'m_merged', kind:'semantic', text:$t, status:'merged', confidence:0.9, created_ms:$d, valid_from_ms:$d, uses:0, emb:vecf32($v)})",
            {"t": t, "d": ms("2026-03-07T00:00:00"), "v": vec(t).tolist()})
    g.query("MATCH (m:Memory {id:'m_merged'}),(e:Entity {id:'e_auth'}) CREATE (m)-[:MENTIONS {conf:1.0}]->(e)")
    for q in ("auth service sessions expire", "what changed about how long auth service sessions expire"):
        assert "m_merged" not in [r["id"] for r in recall(g, q, k=10)], q  # superseded may come back for temporal intent, merged never
    assert "m_merged" not in tools.brief(g)


def _chain(g):
    """Web -> Checkout -> Auth Service, a customer and an incident co-mentioned with Checkout, an owner for Web."""
    q = g.query
    for i, n, t in [("e_web", "Web Dashboard", "service"), ("e_acme", "Acme Corp", "customer"), ("e_inc", "INC-9", "incident"), ("e_zoe", "Zoe Park", "person")]:
        q("CREATE (:Entity {id:$i, name:$n, key:$k, type:$t, mentions:1, emb:vecf32($e)})", {"i": i, "n": n, "k": ch.key_of(n), "t": t, "e": vec(n).tolist()})
    q("MATCH (a:Entity {id:'e_web'}), (b:Entity {id:'e_ck'}), (z:Entity {id:'e_zoe'}) "
      "CREATE (a)-[:REL {type:'DEPENDS_ON', conf:0.9, source_id:'d1#1', valid_from_ms:$d}]->(b), (z)-[:REL {type:'OWNS', conf:0.9, source_id:'d1#1', valid_from_ms:$d}]->(a)", {"d": ms("2026-04-01T00:00:00")})
    q("MATCH (c:Chunk {id:'d1#0'}), (k:Entity {id:'e_ck'}), (a:Entity {id:'e_acme'}), (i:Entity {id:'e_inc'}) "
      "CREATE (c)-[:MENTIONS {conf:1.0}]->(k), (c)-[:MENTIONS {conf:1.0}]->(a), (c)-[:MENTIONS {conf:1.0}]->(i)")
    q("MATCH (a:Entity {id:'e_acme'}), (i:Entity {id:'e_inc'}), (c:Entity {id:'e_ck'}) "
      "CREATE (a)-[:REL {type:'RELATED_TO', conf:0.9, source_id:'d1#0', valid_from_ms:$d}]->(c), "
      "(i)-[:REL {type:'REPORTED', conf:0.9, source_id:'d1#0', valid_from_ms:$d}]->(c)",
      {"d": ms("2026-04-01T00:00:00")})


def test_impact_blast_radius(g):
    _chain(g)
    out = tools.impact(g, "Auth Service")
    print(out)
    assert "Checkout -> Auth Service" in out and "Web Dashboard -> Checkout -> Auth Service" in out and "hop 2" in out
    assert "src:" in out and "Platform runbook" in out  # each edge carries its source
    assert "Platform Team" in out and "Priya Shah" in out and "Zoe Park" in out  # owners of the target and of an affected component (team members listed)
    assert "Acme Corp" in out and "INC-9" in out
    assert "Web Dashboard" not in tools.impact(g, "Auth Service", max_hops=1)
    assert "needs 1" in tools.impact(g, "Checkout") and "Auth Service" in tools.impact(g, "Checkout").split("It needs")[1]
    g.query("MATCH (:Entity {id:'e_ck'})-[r:REL {type:'DEPENDS_ON'}]->(:Entity {id:'e_auth'}) SET r.valid_to_ms = 1")  # an ended edge is not a dependency
    out = tools.impact(g, "Auth Service")
    assert "nothing depends on it" in out and "Checkout ->" not in out
    assert "No entity" in tools.impact(g, "zzqx unknown")


def test_impact_ignores_co_mentioned_customers(g):
    _chain(g)
    q = g.query
    q("CREATE (:Entity {id:'e_noise_customer', name:'Noise Customer', key:'noise customer', type:'customer', mentions:1})")
    q("MATCH (c:Chunk {id:'d1#0'}), (n:Entity {id:'e_noise_customer'}) CREATE (c)-[:MENTIONS {conf:1.0}]->(n)")
    out = tools.impact(g, "Auth Service")
    assert "Acme Corp" in out
    assert "Noise Customer" not in out


def test_timeline_marks_conflicting_memories(g):
    q = g.query
    for i, text, d in [
        ("m_deadline_a", "Hackathon deadline is 2026-10-18", "2026-10-10"),
        ("m_deadline_b", "Hackathon deadline is 2026-10-19", "2026-10-11"),
    ]:
        q(
            "CREATE (:Memory {id:$i, kind:'decision', text:$t, status:'active', confidence:0.9, "
            "created_ms:$d, valid_from_ms:$d, uses:1, emb:vecf32($v)})",
            {"i": i, "t": text, "d": ms(d + "T00:00:00"), "v": vec(text).tolist()},
        )
        q(
            "MATCH (m:Memory {id:$i}), (e:Entity {id:'e_auth'}) "
            "CREATE (m)-[:MENTIONS {conf:1.0}]->(e)",
            {"i": i},
        )
    q(
        "MATCH (a:Memory {id:'m_deadline_a'}), (b:Memory {id:'m_deadline_b'}) "
        "CREATE (a)-[:CONFLICTS_WITH {found_ms:$d}]->(b)",
        {"d": NOW},
    )
    out = tools.timeline(g, "Auth Service")
    lines = [line for line in out.splitlines() if "m_deadline_" in line]
    assert len(lines) == 2
    assert all("CONFLICT" in line for line in lines)


def test_relate_creates_supersedes_and_validates(g):
    out = tools.relate(g, "Priya Shah", "owns", "Checkout", source="d1#0", agent="codex")
    assert out.startswith("created") and "Priya Shah -[OWNS]-> [e_ck] Checkout" in out and "codex" in out and "Platform runbook" in out
    assert tools.relate(g, "Priya Shah", "OWNS", "Checkout").startswith("already current")
    e = g.query("MATCH (:Entity {id:'e_priya'})-[r:REL {type:'OWNS'}]->(:Entity {id:'e_ck'}) RETURN r.agent, r.source_id, r.valid_to_ms, r.conf")
    assert e == [["codex", "d1#0", None, 1.0]]
    # supersede: both current owners of Auth Service end, the new one starts
    out = tools.relate(g, "Priya Shah", "OWNS", "Auth Service", supersede=True, agent="codex")
    print(out)
    assert out.count("closed") == 2 and "Payments Team -[OWNS]-> Auth Service" in out
    cur = g.query("MATCH (x:Entity)-[r:REL {type:'OWNS'}]->(:Entity {id:'e_auth'}) WHERE r.valid_to_ms IS NULL RETURN x.name")
    assert cur == [["Priya Shah"]]
    assert "Priya Shah -[OWNS]-> Auth Service" in tools.who(g, "Auth Service")
    # unknown names become entities; an unsupported type is refused
    assert tools.relate(g, "Zed Service", "DEPENDS_ON", "Checkout").startswith("created")
    assert g.query("MATCH (e:Entity {key:'zed service'}) RETURN e.type") == [["service"]]
    assert tools.relate(g, "Zed Service", "LOVES", "Checkout").startswith("type must be")
    assert "same entity" in tools.relate(g, "Checkout", "PART_OF", "e_ck")
    assert "Zed Service" in tools.impact(g, "Auth Service")  # a written edge is immediately part of the graph


def test_read_chunk_memory_document(g):
    out = tools.read(g, "d1#0")
    assert "Auth Service ownership moved to the Platform Team runbook" in out and "chunk 1 of 2" in out and "next: [d1#1]" in out and "prev: none" in out
    assert "[e_auth] Auth Service (service)" in out and "Checkout -[DEPENDS_ON]-> Auth Service" in out  # relation sourced from this chunk
    assert "prev: [d1#0]" in tools.read(g, "d1#1")
    out = tools.read(g, "m_new")
    assert out.startswith("# memory [m_new]") and "300 seconds" in out and "supersedes [m_old]" in out
    assert "superseded by [m_new]" in tools.read(g, "m_old")
    out = tools.read(g, "d1")
    assert "[d1#0]" in out and "[d1#1] SESSION_TTL is 300 seconds" in out
    long = "word " * 3000
    g.query("MATCH (c:Chunk {id:'d1#1'}) SET c.text=$t", {"t": long})
    out = tools.read(g, "d1#1", max_chars=1000)
    assert len(out) <= 1100 and "more chars" in out and len(tools.read(g, "d1#1", max_chars=20000)) > 10000
    assert tools.read(g, "nope").startswith("No chunk, memory or document")


def test_timeline_shows_values_and_drops_valueless_events_first(g):
    out = tools.timeline(g, "SESSION_TTL")
    print(out)
    assert "Changes:\n2026-03-05 [d1] SESSION_TTL is 300 seconds" in out
    out = tools.timeline(g, "Auth Service")
    assert "(effective 2025-06-01)" in out and "Auth Service ownership moved to the Platform Team runbook" in out
    full = tools.timeline(g, "Auth Service", max_chars=100000)
    small = tools.timeline(g, "Auth Service", max_chars=len(full) - 40)  # just short: only the cheapest events go
    assert len(small) <= len(full) - 40 and "more, narrow with" in small
    assert "REPLACED on 2026-02-01" in small and "[d2#0]" not in small.replace("REL", "") or "ADR-7" not in small
    # a phrase that only fuzzily matches an entity also gets the dated passages about the phrase itself
    g.query("MATCH (c:Chunk {id:'d2#0'}) SET c.text='Auth Service sessions were lowered from 60 to 300 seconds on the platform'")
    assert "lowered from 60 to 300 seconds" in tools.timeline(g, "auth sessions lowered")


def test_timeline_changes_cover_values_in_date_order(g):
    """Config value changes come from chunks that mention the entity; the change sentence leads, dated, once, and in date order."""
    q = g.query
    q("CREATE (:Entity {id:'e_intro', name:'auth.introspection_timeout_ms', key:$k, type:'config_setting', mentions:3, emb:vecf32($e)})",
      {"k": ch.key_of("auth.introspection_timeout_ms"), "e": vec("auth.introspection_timeout_ms").tolist()})
    q("CREATE (:Document {id:'d3', kind:'ticket', title:'CFG-4411 timeout change', date_ms:$d}), "
      "(:Document {id:'d4', kind:'ticket', title:'CFG-4411 rollback', date_ms:$e}), (:Document {id:'d5', kind:'ticket', title:'copy', date_ms:$f})",
      {"d": ms("2026-04-10T00:00:00"), "e": ms("2026-06-01T00:00:00"), "f": ms("2026-04-12T00:00:00")})
    for cid, did, text, d in [("d3#0", "d3", "CFG-4411 lowered auth.introspection_timeout_ms from 800 to 80 ms for the mesh.", "2026-04-10"),
                              ("d3#1", "d3", "The lint team reviews auth.introspection_timeout_ms each sprint.", "2026-04-10"),
                              ("d4#0", "d4", "The auth.introspection_timeout_ms change from CFG-4411 was rolled back to 800 ms.", "2026-06-01"),
                              ("d5#0", "d5", "CFG-4411 lowered auth.introspection_timeout_ms from 800 to 80 ms for the mesh.", "2026-04-12")]:
        q("MATCH (d:Document {id:$d}) CREATE (d)-[:HAS_CHUNK]->(c:Chunk {id:$i, doc_id:$d, pos:0, text:$t, kind:d.kind, date_ms:$m, emb:vecf32($v)}) "
          "WITH c MATCH (e:Entity {id:'e_intro'}) CREATE (c)-[:MENTIONS {conf:1.0}]->(e)",
          {"d": did, "i": cid, "t": text, "m": ms(d + "T00:00:00"), "v": vec(text).tolist()})
    out = tools.timeline(g, "auth.introspection_timeout_ms")
    print(out)
    changes = [l for l in out.split("Changes:")[1].split("Events:")[0].splitlines() if l[:2] == "20"]
    assert changes[0] == "2026-04-10 [d3] CFG-4411 lowered auth.introspection_timeout_ms from 800 to 80 ms for the mesh."
    assert any(l.startswith("2026-06-01 [d4]") and "rolled back to 800 ms" in l for l in changes)
    assert [l[:10] for l in changes] == sorted(l[:10] for l in changes)
    assert out.count("from 800 to 80 ms") == 1 and "lint team" not in out  # duplicate sentence once, no value means not a change
    assert len(tools.timeline(g, "auth.introspection_timeout_ms", max_chars=260)) <= 260


def test_who_exact_entity_beats_fuzzy_neighbour(g):
    """'payment-gateway' is an exact key; 'api-gateway' is a fuzzy neighbour whose owner (heavy on documents) must not rank first."""
    q = g.query
    for i, n, t in [("e_pg", "payment-gateway", "service"), ("e_gw", "api-gateway", "service"),
                    ("e_dan", "Daniel Kwon", "person"), ("e_vik", "Viktor Sokolov", "person")]:
        q("CREATE (:Entity {id:$i, name:$n, key:$k, type:$t, mentions:1, emb:vecf32($e)})", {"i": i, "n": n, "k": ch.key_of(n), "t": t, "e": vec(n).tolist()})
    q("MATCH (d:Entity {id:'e_dan'}), (s:Entity {id:'e_pg'}) CREATE (d)-[:REL {type:'OWNS', conf:0.5, source_id:'d1#0', valid_from_ms:$d}]->(s)",
      {"d": ms("2026-01-01T00:00:00")})
    q("MATCH (v:Entity {id:'e_vik'}), (s:Entity {id:'e_gw'}) CREATE (v)-[:REL {type:'OWNS', conf:0.9, source_id:'d1#0', valid_from_ms:$d}]->(s)",
      {"d": ms("2026-01-01T00:00:00")})
    for n in range(3):  # Viktor authors three documents about payment-gateway: documentary evidence outweighs Daniel's 0.5-confidence OWNS
        did = f"pg{n}"
        q("CREATE (:Document {id:$d, kind:'doc', title:$d, date_ms:$t})", {"d": did, "t": ms("2026-05-01T00:00:00")})
        q("MATCH (v:Entity {id:'e_vik'}), (d:Document {id:$d}) CREATE (v)-[:AUTHORED]->(d) "
          "WITH d CREATE (d)-[:HAS_CHUNK]->(c:Chunk {id:$d+'#0', doc_id:$d, pos:0, text:'payment-gateway retries', kind:'doc', date_ms:$t}) "
          "WITH c MATCH (p:Entity {id:'e_pg'}) CREATE (c)-[:MENTIONS {conf:1.0}]->(p)", {"d": did, "t": ms("2026-05-01T00:00:00")})
    out = tools.who(g, "payment-gateway")
    print(out)
    assert out.splitlines()[0].endswith("(entities: payment-gateway), ranked, with evidence")  # the fuzzy neighbour is not a seed
    assert out.splitlines()[1].startswith("1. [e_dan] Daniel Kwon")  # direct current owner first
    assert out.index("Daniel Kwon") < out.index("Viktor Sokolov")  # Viktor's document score alone is higher than Daniel's 0.5 path


def test_ask_marks_ended_edges_and_skips_ended_paths(g):
    g.query("MATCH (:Entity {id:'e_ck'})-[r:REL {type:'DEPENDS_ON'}]->(:Entity {id:'e_auth'}) SET r.valid_to_ms=$d", {"d": ms("2026-09-01T00:00:00")})
    out = tools.ask(g, "who owns Auth Service and how does Checkout connect to it")
    print(out)
    assert "Checkout -[DEPENDS_ON]-> Auth Service (2025-09-01, ended 2026-09-01, conf" in out  # ended, not presented as current
    assert "## Bridging paths" not in out  # the only Checkout-Auth path is an ended edge
    assert "ended 2026-09-01" in tools.explore(g, "Checkout")  # explore marks ended neighbours like read does
    assert "No path" in tools.connect(g, "Priya Shah", "Checkout")


def test_impact_bfs_caps_dedupes_owners_and_customers(g):
    _chain(g)
    q = g.query
    q("CREATE (:Entity {id:'e_y1', name:'Ledger Export', key:'ledger export', type:'service', mentions:1}), "
      "(:Entity {id:'e_y2', name:'Ledger Sync', key:'ledger sync', type:'service', mentions:1}), "
      "(:Entity {id:'e_y3', name:'Ledger Store', key:'ledger store', type:'service', mentions:1}), "
      "(:Entity {id:'e_wid', name:'Widget Works', key:'widget works', type:'product', mentions:1})")
    q("MATCH (a:Entity {id:'e_y1'}), (b:Entity {id:'e_y2'}), (c:Entity {id:'e_y3'}), (s:Entity {id:'e_auth'}) "
      "CREATE (a)-[:REL {type:'DEPENDS_ON', conf:0.9, source_id:'d1#0', valid_from_ms:$d}]->(b), "
      "(b)-[:REL {type:'DEPENDS_ON', conf:0.9, source_id:'d1#0', valid_from_ms:$d}]->(c), "
      "(c)-[:REL {type:'DEPENDS_ON', conf:0.9, source_id:'d1#0', valid_from_ms:$d}]->(s)", {"d": ms("2026-04-01T00:00:00")})
    q("MATCH (w:Entity {id:'e_wid'}), (c:Chunk {id:'d1#0'}) CREATE (c)-[:MENTIONS {conf:1.0}]->(w)")
    for src in ("d1#0", "d1#1", "d2#0"):  # Zoe's ownership of Web recorded three times
        q("MATCH (z:Entity {id:'e_zoe'}), (a:Entity {id:'e_web'}) CREATE (z)-[:REL {type:'OWNS', conf:0.9, source_id:$s, valid_from_ms:$d}]->(a)",
          {"s": src, "d": ms("2026-04-01T00:00:00")})
    out = tools.impact(g, "Auth Service", max_hops=2)
    print(out)
    assert "Ledger Export" not in out and "Ledger Sync" in out  # hop 3 is beyond max_hops 2
    assert "cut at max_hops 2" in out  # the cap is reported, not silent
    assert out.split("## Owners to tell")[1].count("[e_zoe] Zoe Park") == 1  # one line per owner, however many OWNS edges
    assert "Widget Works" not in out  # only entities typed customer are listed as customers
    assert "Acme Corp" in out
    full = tools.impact(g, "Auth Service", max_hops=3)
    assert "Ledger Export" in full and "cut at" not in full


def test_relate_supersede_only_single_valued(g):
    out = tools.relate(g, "Zed Service", "DEPENDS_ON", "Auth Service", supersede=True)
    assert out.startswith("supersede only applies to single-valued types") and "DEPENDS_ON" in out
    assert g.query("MATCH (e:Entity {key:'zed service'}) RETURN count(e)") == [[0]]  # refused before anything is written
    assert tools.relate(g, "Auth Service", "RENAMED_TO", "Checkout", supersede=True).startswith("created")  # single-valued: allowed


def test_handoff_coerces_fields(g):
    out = tools.handoff(g, to=7, summary=42, tasks=[1, "x"], from_agent=None)
    assert out.startswith("handoff [")  # non-string fields from the JSON API are stored as strings
    brief = tools.brief(g, agent="7")
    assert "42" in brief and "tasks: 1; x" in brief  # and brief still renders them


def test_tenant_name_validated(g):
    out = tools.brief(g, tenant="acme.eu")  # "acme.eu" and "acme_eu" would share a graph name: refused, not coerced
    assert out.startswith('tenant "acme.eu" is invalid')
    assert tools.recall(g, "auth", tenant="acme eu").startswith("tenant")
    assert not tools.brief(g, tenant="acme-eu").startswith("tenant")


def test_bad_since_is_text(g):
    assert tools.recall(g, "auth", since="2026-02-31") == 'bad date "2026-02-31": use ISO YYYY-MM-DD (or YYYY-MM-DDTHH:MM)'
    assert tools.timeline(g, "Auth Service", until="soon").startswith('bad date "soon"')
    assert tools.explore(g, "Auth Service", since="next week").startswith("bad date")


def test_timeline_caps_to_newest_events(g):
    rows = [{"id": f"mx{i:03d}", "t": "Auth Service note was recorded", "d": ms("2025-01-01T00:00:00") + i * 86400000} for i in range(260)]  # no digits: not a change record
    g.query("UNWIND $r AS x CREATE (:Memory {id:x.id, kind:'semantic', text:x.t, status:'active', confidence:0.9, created_ms:x.d, valid_from_ms:x.d, uses:0})",
            {"r": rows})
    g.query("UNWIND $r AS x MATCH (m:Memory {id:x.id}), (e:Entity {id:'e_auth'}) CREATE (m)-[:MENTIONS {conf:1.0}]->(e)", {"r": rows})
    out = tools.timeline(g, "Auth Service", max_chars=100000)
    assert "[mx259]" in out and "[mx000]" not in out  # the newest 200 events are queried, not the whole history
    assert len(out) <= 100000


def test_cypher_limit_in_query(g, monkeypatch):
    seen, real = [], g.graph

    class Spy:
        def __init__(self, graph):
            self.graph = graph

        def ro_query(self, q, **kw):
            seen.append(q)
            return self.graph.ro_query(q, **kw)
    monkeypatch.setattr(g, "graph", lambda tenant=None: Spy(real(tenant)))
    out = tools.cypher(g, "MATCH (e:Entity) RETURN e.name LIMIT 100000", limit=3)
    assert seen[-1].endswith("LIMIT 4") and "100000" not in seen[-1]  # the cap is in the query, not applied after fetching everything
    assert out.startswith("3 rows (capped at 3)")


def test_relate_check_and_create_hold_the_write_lock(g):
    class Spy:
        def __init__(self):
            self.entered = 0

        def __enter__(self):
            self.entered += 1

        def __exit__(self, *exc):
            return False
    spy = g.write_lock = Spy()  # the lock Store exposes for the write path
    out = tools.relate(g, "Priya Shah", "OWNS", "Checkout", source="d1#0")
    assert out.startswith("created") and spy.entered == 1  # the check and the create run under one lock acquisition


def _long_chunk(g):
    """A chunk whose answer sentence sits past the first 400 chars (retrieval trims text there)."""
    text = "The team reviews dashboards each sprint and keeps notes on alerting noise. " * 7 + "Signing keys are rotated every 45 days."
    g.query("MATCH (d:Document {id:'d1'}) CREATE (d)-[:HAS_CHUNK]->(c:Chunk {id:'d1#2', doc_id:'d1', pos:2, text:$t, kind:d.kind, "
            "date_ms:$m, emb:vecf32($v)})", {"t": text, "m": ms("2026-03-06T00:00:00"), "v": vec(text).tolist()})


def test_recall_shows_answer_sentence_past_the_head(g):
    _long_chunk(g)
    out = tools.recall(g, "how often are signing keys rotated", k=3)
    print(out)
    assert "d1#2" in out and "Signing keys are rotated every 45 days." in out
    assert "alerting noise" not in out  # the sentences without query terms are not shown


def test_ask_shows_answer_sentence_past_the_head(g):
    _long_chunk(g)
    out = tools.ask(g, "how often are signing keys rotated")
    print(out)
    assert "Signing keys are rotated every 45 days." in out


def test_snippets_stay_within_max_chars(g):
    _long_chunk(g)
    for n in (300, 600):
        assert len(tools.recall(g, "how often are signing keys rotated", k=3, max_chars=n)) <= n
        assert len(tools.ask(g, "how often are signing keys rotated", max_chars=n * 4)) <= n * 4


def test_snip_picks_best_sentences_in_document_order():
    text = "Intro about nothing. " + "Filler words here. " * 20 + "Refunds take 5 days. " + "More filler. " * 20 + "Refund limit is 500 USD. Closing remark."
    out = tools._snip(text, "refund days limit", 240)
    print(out)
    assert out == "Refunds take 5 days. … Refund limit is 500 USD."
    assert tools._snip("Short text.", "anything", 240) == "Short text."
    assert tools._snip("A" * 300, "zzz", 50).endswith("…")  # no sentence matches: the head, as before


def test_snip_skips_an_over_long_match_for_a_shorter_one():
    s = "a very long bullet of words " * 12 + "The local subgraph is capped at 500 nodes in total. Node count is 500."
    out = tools._snip(s, "node count", 240)
    print(out)
    assert out == "Node count is 500." and len(tools._snip(s, "local subgraph node", 240)) <= 240
