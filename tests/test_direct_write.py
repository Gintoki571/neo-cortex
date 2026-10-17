"""Direct writes: the calling agent passes entities and relations it already knows, so GLiNER never runs."""
import pytest
from conftest import _fake_embed

from neo_cortex import extract, resolve, tools, write


@pytest.fixture
def offline(monkeypatch):
    """Embeddings are faked; every GLiNER entry point raises, so a test fails if extraction still runs."""
    monkeypatch.setattr(write, "embed_docs", _fake_embed)
    monkeypatch.setattr(resolve, "embed_docs", _fake_embed)

    def boom(*a, **k):
        raise AssertionError("GLiNER must not run for a structured remember")
    for name in ("extract", "classify_memory", "extract_batch", "_softmax_labels"):
        monkeypatch.setattr(extract, name, boom)


def _mem(store, mid):
    return store.query("MATCH (m:Memory {id:$i}) RETURN m.kind, m.text", {"i": mid})


def test_structured_remember_writes_typed_entities_mentions_and_edges(store, offline):
    out = tools.remember(store, "Checkout depends on Auth Service, and Priya Shah owns Checkout", kind="decision",
                         entities=[{"name": "Checkout", "type": "service"}, {"name": "Auth Service", "type": "service"},
                                   {"name": "Priya Shah", "type": "person"}],
                         relations=[["Checkout", "DEPENDS_ON", "Auth Service"], ["Priya Shah", "OWNS", "Checkout"]])
    mid = out.split("[", 1)[1].split("]", 1)[0]
    assert out.startswith("created [mem_") and mid.startswith("mem_")
    assert store.query("MATCH (e:Entity) RETURN e.key, e.type ORDER BY e.key") == [
        ["auth service", "service"], ["checkout", "service"], ["priya shah", "person"]]
    assert sorted(r[0] for r in store.query("MATCH (m:Memory {id:$m})-[:MENTIONS]->(e:Entity) RETURN e.key", {"m": mid})) == [
        "auth service", "checkout", "priya shah"]
    edges = store.query("MATCH (a:Entity)-[r:REL]->(b:Entity) RETURN a.key, r.type, b.key, r.source_id, r.conf ORDER BY r.type")
    assert edges == [["checkout", "DEPENDS_ON", "auth service", mid, 1.0], ["priya shah", "OWNS", "checkout", mid, 1.0]]
    assert "Checkout -[DEPENDS_ON]-> " in out and "Priya Shah -[OWNS]-> " in out
    assert _mem(store, mid) == [["decision", "Checkout depends on Auth Service, and Priya Shah owns Checkout"]]


def test_unknown_relation_type_reported_per_triple(store, offline):
    out = tools.remember(store, "Checkout depends on Auth Service", kind="semantic",
                         entities=[{"name": "Checkout", "type": "service"}],
                         relations=[["Checkout", "LOVES", "Auth Service"], ["Checkout", "DEPENDS_ON", "Auth Service"],
                                    ["Checkout", "DEPENDS_ON"]])
    assert out.startswith("created [mem_")
    assert "type must be one of" in out and "relation ['Checkout', 'DEPENDS_ON'] is not [head, TYPE, tail]" in out
    assert store.query("MATCH ()-[r:REL]->() RETURN r.type") == [["DEPENDS_ON"]]  # the valid triple still lands


def test_unknown_entity_type_becomes_other(store, offline):
    tools.remember(store, "Ops runs a weekly drill", kind="procedural", entities=[{"name": "Drill Night", "type": "ritual"}])
    assert store.query("MATCH (e:Entity {key:'drill night'}) RETURN e.type") == [["other"]]


def test_about_names_stay_other_without_extraction(store, offline):
    tools.remember(store, "Use the Atlas board", kind="procedural", about=["Atlas"])
    assert store.query("MATCH (e:Entity {key:'atlas'}) RETURN e.type") == [["other"]]


def test_relate_end_closes_edge_and_impact_forgets_it(store, offline):
    tools.remember(store, "Checkout depends on Auth Service", kind="semantic",
                   relations=[["Checkout", "DEPENDS_ON", "Auth Service"]])
    assert "Checkout" in tools.impact(store, "Auth Service")
    out = tools.relate(store, "Checkout", "DEPENDS_ON", "Auth Service", end=True, agent="codex")
    assert out.startswith("ended 1 current edge(s)")
    rows = store.query("MATCH ()-[r:REL {type:'DEPENDS_ON'}]->() RETURN r.valid_to_ms")
    assert len(rows) == 1 and rows[0][0] is not None  # kept for history
    assert "nothing depends on it" in tools.impact(store, "Auth Service")
    assert "ended" in tools.explore(store, "Checkout")
    assert tools.relate(store, "Checkout", "DEPENDS_ON", "Auth Service", end=True).startswith("no current edge")
    assert "no replacement" in tools.relate(store, "Checkout", "DEPENDS_ON", "Auth Service", end=True, supersede=True)


def test_plain_remember_still_extracts(store, monkeypatch):
    calls = []
    monkeypatch.setattr(write, "embed_docs", _fake_embed)
    monkeypatch.setattr(resolve, "embed_docs", _fake_embed)
    monkeypatch.setattr(extract, "extract", lambda t: calls.append("extract") or {"entities": [], "relations": []})
    monkeypatch.setattr(extract, "classify_memory", lambda t: calls.append("classify") or ("semantic", 0.9))
    tools.remember(store, "Always run tests with uv")  # no kind: classify + extract
    tools.remember(store, "Deploy the Atlas board on Fridays", kind="procedural")  # kind but nothing structured: extract
    assert calls == ["classify", "extract", "extract"]


def test_relate_end_never_creates_entities(store, offline):
    tools.remember(store, "Checkout depends on Auth Service", kind="semantic",
                   relations=[["Checkout", "DEPENDS_ON", "Auth Service"]])
    before = store.query("MATCH (e:Entity) RETURN count(e)")[0][0]
    out = tools.relate(store, "Zed Service", "DEPENDS_ON", "Quux Gateway", end=True)
    assert out.startswith("no current edge") and "nothing written" in out
    out = tools.relate(store, "Checkout", "DEPENDS_ON", "Quux Gateway", end=True)  # one known end is not enough
    assert out.startswith("no current edge") and "Quux Gateway" in out
    assert store.query("MATCH (e:Entity) RETURN count(e)")[0][0] == before
    assert store.query("MATCH ()-[r:REL {type:'DEPENDS_ON'}]->() WHERE r.valid_to_ms IS NULL RETURN count(r)")[0][0] == 1
