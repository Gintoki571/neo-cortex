"""Assertion gate on extracted REL edges (pg-jev idea): denial drops, hedges are tagged and low-conf, facts and agent edges are untouched.
The GLiNER calls are faked: relations come from the deterministic patterns (`payments-service depends on ledger-service`)."""
import numpy as np
import pytest

from neo_cortex import extract as X
from neo_cortex import models, resolve, tools, write
from neo_cortex.retrieve import channels as ch
from test_retrieve import vec


class FakeExtractor:
    """Entity and relation passes return nothing, so only the sentence patterns (and the modality gate) decide the edges."""

    def create_schema(self):
        return self

    def entities(self, *a, **k):
        return self

    def relations(self, *a, **k):
        return self

    def batch_extract_long(self, texts, schema, **k):
        return [{} for _ in texts]


def probs(text):
    """Fake modality distribution keyed by a marker word: [deny] denial, [hedge] possibility, [plan] plan, else fact."""
    if "[deny]" in text:
        p = {"fact": 0.02, "possibility": 0.03, "denial": 0.9, "plan or forecast": 0.05}
    elif "[hedge]" in text:
        p = {"fact": 0.2, "possibility": 0.7, "denial": 0.04, "plan or forecast": 0.06}
    elif "[plan]" in text:
        p = {"fact": 0.3, "possibility": 0.1, "denial": 0.05, "plan or forecast": 0.55}
    else:
        p = {"fact": 0.97, "possibility": 0.01, "denial": 0.01, "plan or forecast": 0.01}
    return p


@pytest.fixture(autouse=True)
def _model_gate(monkeypatch):
    """Most tests here exercise the model-denial path; test_rule_gate... covers the default rule gate."""
    monkeypatch.setenv("NEO_GATE_MODEL", "model")


@pytest.fixture
def calls(monkeypatch):
    """Fake classifier that records each call (one list of texts per call)."""
    seen = []

    def fake(texts, task, labels):
        assert task == "modality" and set(labels) == {"fact", "possibility", "denial", "plan or forecast"}
        seen.append(list(texts))
        return [probs(t) for t in texts]

    monkeypatch.setattr(X, "_softmax_batch", fake)
    monkeypatch.setattr(X, "gliner", lambda: FakeExtractor())
    return seen


@pytest.fixture(autouse=True)
def fakes(monkeypatch):
    monkeypatch.setattr(models, "embed_query", vec)
    monkeypatch.setattr(models, "embed_docs", lambda texts, titles=None: np.stack([vec(t) for t in texts]))
    monkeypatch.setattr(resolve, "embed_docs", lambda texts, titles=None: np.stack([vec(t) for t in texts]))


def rel(head, tail, win, conf=0.9, typ="DEPENDS_ON"):
    return {"head": head, "type": typ, "tail": tail, "conf": conf, "win": win}


def test_gate_drops_denial_and_tags_hedges(calls):
    rels = [rel("A", "B", "payments-service depends on ledger-service [deny]"),
            rel("A", "C", "payments-service depends on fraud-service [hedge]"),
            rel("A", "D", "payments-service depends on vault-service [plan]"),
            rel("A", "E", "payments-service depends on card-service.")]
    got = {r["tail"]: r for r in X._gate(rels)}
    assert set(got) == {"C", "D", "E"}  # the denial is not written
    assert got["C"]["modality"] == "possibility" and got["C"]["p_fact"] == 0.2 and got["C"]["conf"] == round(0.9 * 0.2, 4)
    assert got["D"]["modality"] == "plan" and got["D"]["conf"] == round(0.9 * 0.3, 4)
    assert got["E"]["modality"] == "fact" and got["E"]["p_fact"] == 0.97 and got["E"]["conf"] == 0.9  # facts keep their conf
    assert all("win" not in r for r in got.values())
    assert len(calls) == 1 and len(calls[0]) == 4  # one classifier call for the whole document's windows


def test_the_classifier_reads_the_edge_sentence_not_the_window(calls):
    win = "auth-service reads its settings from config-service. Nothing is compiled in, so a change needs no release [deny]."
    got = X._gate([rel("auth-service", "config-service", win)])
    assert got and got[0]["modality"] == "fact"  # the denial is about another sentence
    assert calls[-1] == ["auth-service reads its settings from config-service."]


def test_table_facts_and_no_relations_skip_the_classifier(calls):
    table = {"head": "Ops", "type": "OWNS", "tail": "vault-service", "conf": 0.9}  # no window: a table row is a fact
    assert X._gate([table]) == [{**table, "modality": "fact", "p_fact": 1.0}]
    assert X._gate([]) == [] and calls == []


def test_extract_batch_gates_pattern_relations(calls):
    text = ("payments-service depends on ledger-service.\npayments-service depends on fraud-service [hedge].\n"
            "payments-service depends on vault-service [deny].")  # one window per line
    out = X.extract_batch([text], ["Payments design"], [""], kind="doc")
    rels = {r["tail"]: r for r in out[0]["relations"]}
    assert "payments-service" in [r["head"] for r in out[0]["relations"]]
    assert set(rels) == {"ledger-service", "fraud-service"}  # denial dropped, hedge kept as possibility
    assert rels["fraud-service"]["modality"] == "possibility" and rels["fraud-service"]["conf"] < 0.9
    assert rels["ledger-service"]["modality"] == "fact" and rels["ledger-service"]["conf"] == 0.9
    assert all("win" not in r for r in out[0]["relations"])
    assert len(calls) == 1  # one classifier call per document


def test_ingest_writes_modality_and_hedge_is_not_current(store, calls, tmp_path):
    p = tmp_path / "design.md"
    p.write_text("# Payments design\n\npayments-service depends on fraud-service [hedge].\n\n"
                 "payments-service depends on ledger-service.\n", encoding="utf-8")
    write.ingest_path(store, p)
    rows = {b: (mod, pf, conf) for b, mod, pf, conf in store.query(
        "MATCH (a:Entity {key:'payments service'})-[r:REL]->(b:Entity) RETURN b.key, r.modality, r.p_fact, r.conf")}
    assert rows["fraud service"][0] == "possibility" and rows["fraud service"][1] == 0.2
    assert rows["ledger service"][0] == "fact" and rows["ledger service"][1] == 0.97
    # the hedge is a stored edge, but impact does not count it as a current dependency
    out = tools.impact(store, "fraud-service")
    assert "1 depend on it" not in out and "nothing depends on it" in out
    assert "payments-service" in tools.impact(store, "ledger-service")  # the fact dependency counts
    assert "(possibility, not a current fact)" in tools.explore(store, "payments-service")


def test_read_side_treats_non_fact_edges_as_not_current(store, monkeypatch):
    q = store.query
    for i, n, t in [("e_p", "Payments Service", "service"), ("e_l", "Ledger Service", "service"), ("e_f", "Fraud Service", "service"),
                    ("e_s", "SESSION_TTL", "config_setting"), ("e_pri", "Priya Shah", "person")]:
        q("CREATE (:Entity {id:$i, name:$n, key:$k, type:$t, mentions:1, emb:vecf32($e)})",
          {"i": i, "n": n, "k": ch.key_of(n), "t": t, "e": vec(n).tolist()})
    q("CREATE (:Document {id:'d1', kind:'doc', title:'Runbook', date_ms:1767225600000})")
    # chunk d1#1 is the only place Fraud Service is mentioned, so the PPR walk reaches it through the REL edge alone
    for cid, text, ents in (("d1#0", "Payments Service keeps SESSION_TTL", ("e_p", "e_s")), ("d1#1", "Fraud Service", ("e_f",))):
        q("CREATE (:Chunk {id:$i, doc_id:'d1', pos:$p, text:$t, kind:'doc', date_ms:1767225600000, emb:vecf32($e)})",
          {"i": cid, "p": int(cid[-1]), "t": text, "e": vec(text).tolist()})
        q("MATCH (d:Document {id:'d1'}), (c:Chunk {id:$i}) CREATE (d)-[:HAS_CHUNK]->(c)", {"i": cid})
        for e in ents:
            q("MATCH (c:Chunk {id:$i}), (e:Entity {id:$e}) CREATE (c)-[:MENTIONS {conf:1.0}]->(e)", {"i": cid, "e": e})
    # a hedge (possibility, low conf) and a fact on the same pair; and a hedged owner of SESSION_TTL
    q("MATCH (a:Entity {id:'e_p'}), (b:Entity {id:'e_f'}) CREATE (a)-[:REL {type:'DEPENDS_ON', conf:0.18, source_id:'d1#0', "
      "valid_from_ms:1767225600000, modality:'possibility', p_fact:0.2}]->(b)")
    q("MATCH (a:Entity {id:'e_pri'}), (b:Entity {id:'e_s'}) CREATE (a)-[:REL {type:'OWNS', conf:0.54, source_id:'d1#0', "
      "valid_from_ms:1767225600000, modality:'plan', p_fact:0.6}]->(b)")
    out = tools.impact(store, "Fraud Service")
    assert "nothing depends on it" in out and "Payments" not in out
    assert "Priya" not in tools.who(store, "SESSION_TTL")
    assert ", plan, not a current fact)" in tools.read(store, "d1#0")
    assert "DEPENDS_ON" not in tools.timeline(store, "Fraud Service")  # hedged edges are not dated events
    assert "No path" in tools.connect(store, "Payments Service", "Fraud Service")  # the hedge is not a path
    names = ch.ppr(store, {"e_p": 1.0}, {}, tenant=None, now=0, current=True)[1]
    assert "e_f" not in names  # the PPR walk does not cross the hedge
    names_temporal = ch.ppr(store, {"e_p": 1.0}, {}, tenant=None, now=0, current=False)[1]
    assert "e_f" not in names_temporal


def test_agent_edges_are_facts_and_skip_the_classifier(store, calls, monkeypatch):
    q = store.query
    for i, n, t in [("e_pri", "Priya Shah", "person"), ("e_s", "SESSION_TTL", "config_setting")]:
        q("CREATE (:Entity {id:$i, name:$n, key:$k, type:$t, mentions:1, emb:vecf32($e)})",
          {"i": i, "n": n, "k": ch.key_of(n), "t": t, "e": vec(n).tolist()})
    # a hedge already stored on the pair: a caller's fact is written beside it, not refused as already current
    q("MATCH (a:Entity {id:'e_pri'}), (b:Entity {id:'e_s'}) CREATE (a)-[:REL {type:'OWNS', conf:0.5, source_id:'x', "
      "valid_from_ms:1, modality:'possibility', p_fact:0.5}]->(b)")
    monkeypatch.setattr(X, "_softmax_batch", lambda *a, **k: pytest.fail("classifier must not run on agent edges"))
    out = tools.relate(store, "Priya Shah", "OWNS", "SESSION_TTL", source="memo", agent="tester")
    assert out.startswith("created"), out
    rows = q("MATCH (a:Entity {id:'e_pri'})-[r:REL {type:'OWNS'}]->(b:Entity {id:'e_s'}) RETURN r.modality, r.p_fact ORDER BY r.modality")
    assert rows == [["fact", 1.0], ["possibility", 0.5]]
    assert "Priya Shah" in tools.who(store, "SESSION_TTL")
    assert "already current" in tools.relate(store, "Priya Shah", "OWNS", "SESSION_TTL", source="memo", agent="tester")


def test_supersede_closes_only_fact_owners(store):
    q = store.query
    for i, n in [("e_a", "Team A"), ("e_b", "Team B"), ("e_x", "Ledger Service")]:
        q("CREATE (:Entity {id:$i, name:$n, key:$k, type:$t, mentions:1, emb:vecf32($e)})",
          {"i": i, "n": n, "k": ch.key_of(n), "t": "team" if i != "e_x" else "service", "e": vec(n).tolist()})
    q("MATCH (a:Entity {id:'e_a'}), (x:Entity {id:'e_x'}) CREATE (a)-[:REL {type:'OWNS', conf:0.9, source_id:'s1', valid_from_ms:100}]->(x)")
    q("MATCH (b:Entity {id:'e_b'}), (x:Entity {id:'e_x'}) CREATE (b)-[:REL {type:'OWNS', conf:0.2, source_id:'s2', valid_from_ms:200, "
      "modality:'possibility', p_fact:0.2}]->(x)")
    write._supersede(store, ["e_x"], None)
    assert q("MATCH (:Entity {id:'e_a'})-[r:REL]->(:Entity {id:'e_x'}) RETURN r.valid_to_ms")[0][0] is None  # a hedge does not end a fact
    q("MATCH (b:Entity {id:'e_b'}), (x:Entity {id:'e_x'}) CREATE (b)-[:REL {type:'OWNS', conf:0.9, source_id:'s3', valid_from_ms:300}]->(x)")
    write._supersede(store, ["e_x"], None)
    assert q("MATCH (:Entity {id:'e_a'})-[r:REL]->(:Entity {id:'e_x'}) RETURN r.valid_to_ms")[0][0] == 300  # a later fact ends it


def test_rule_gate_drops_negated_edges_and_keeps_conditionals(calls, monkeypatch):
    monkeypatch.delenv("NEO_GATE_MODEL")  # default rule: the model's denial is not trusted, a cue decides, and conditionals stay facts
    rels = [rel("Payments-service", "fraud-service", "Payments-service no longer calls fraud-service [deny]."),  # cue, model says fact
            rel("auth-service", "session-cache", "If auth-service cannot reach session-cache, new logins fail [deny]."),
            rel("Payments-service", "ledger-service", "Payments-service depends on ledger-service [hedge].")]
    got = {r["tail"]: r for r in X._gate(rels)}
    assert set(got) == {"session-cache", "ledger-service"}
    assert got["session-cache"]["modality"] == "fact" and got["session-cache"]["conf"] == 0.9  # denial mass counts as fact
    assert got["ledger-service"]["modality"] == "possibility" and got["ledger-service"]["p_fact"] == 0.24  # fact 0.2 + denial 0.04
    assert len(calls) == 1 and len(calls[0]) == 3  # still one classifier call per document
