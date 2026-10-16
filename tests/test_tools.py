import numpy as np
import pytest
from test_retrieve import FakeGliner, ms, vec

from neo_cortex import models, tools, write
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
        q("MATCH (d:Document {id:$d}) CREATE (d)-[:HAS_CHUNK]->(c:Chunk {id:$i, doc_id:$d, text:$t, kind:d.kind, date_ms:$m, emb:vecf32($v)}) "
          "WITH c MATCH (e:Entity {id:$e}) CREATE (c)-[:MENTIONS {conf:1.0}]->(e)",
          {"d": did, "i": cid, "t": text, "m": ms(d + "T00:00:00"), "v": vec(text).tolist(), "e": e})
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
    dates = [l[:10] for l in out.splitlines()[1:] if l[:2] == "20"]
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
