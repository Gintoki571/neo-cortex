import datetime as dt
import re
import zlib

import numpy as np
import pytest

from neo_cortex import models
from neo_cortex.retrieve import channels as ch
from neo_cortex.retrieve import parse_time, recall, rrf
from neo_cortex.retrieve.fuse import channel_weights


def ms(s):
    return int(dt.datetime.fromisoformat(s).replace(tzinfo=dt.timezone.utc).timestamp() * 1000)


NOW = ms("2026-10-16T12:00:00")


def vec(text):  # bag-of-words hash embedding: shared words give cosine similarity
    v = np.zeros(768, dtype=np.float32)
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        v[zlib.crc32(w.encode()) % 768] += 1
    return v / (np.linalg.norm(v) or 1)


class FakeGliner:
    calls = 0
    NAMES = {"checkout": "service", "platform team": "team", "session_ttl": "config setting", "priya": "person"}

    def extract_entities(self, q, labels, threshold=0.5, include_confidence=False):
        FakeGliner.calls += 1
        out = {}
        for name, t in self.NAMES.items():
            if name in q.lower():
                out.setdefault(t, []).append({"text": name.upper() if "_" in name else name.title(), "confidence": 0.9})
        return {"entities": out}

    def classify_text(self, q, tasks, include_confidence=False):
        FakeGliner.calls += 1
        spec = tasks["intent"]["labels"]
        ql = q.lower()
        hot = {"temporal": bool(re.search(r"chang|when|latest", ql)), "owner": bool(re.search(r"\bwho\b|owns", ql)),
               "connection": "connected" in ql, "howto": "how do" in ql}
        return {"intent": [{"label": l, "confidence": 0.9 if hot.get(k) else 0.05}
                           for (k, _), l in zip(__import__("neo_cortex.retrieve.query", fromlist=["x"]).INTENT_LABELS.items(), spec)]}


@pytest.fixture(autouse=True)
def fakes(monkeypatch):
    monkeypatch.setattr(models, "embed_query", vec)
    monkeypatch.setattr(models, "embed_docs", lambda texts, titles=None: np.stack([vec(t) for t in texts]))
    monkeypatch.setattr(models, "gliner", lambda: FakeGliner())
    FakeGliner.calls = 0


@pytest.fixture
def g(store):
    q = store.query
    ents = [("e_ck", "Checkout", "service"), ("e_auth", "Auth Service", "service"), ("e_plat", "Platform Team", "team"),
            ("e_ttl", "SESSION_TTL", "config_setting")]
    for i, n, t in ents:
        q("CREATE (:Entity {id:$i, name:$n, key:$k, type:$t, emb:vecf32($e)})",
          {"i": i, "n": n, "k": ch.key_of(n), "t": t, "e": vec(n).tolist()})
    q("MATCH (a:Entity {id:'e_ck'}),(b:Entity {id:'e_auth'}),(c:Entity {id:'e_plat'}) "
      "CREATE (a)-[:REL {type:'DEPENDS_ON', conf:0.9}]->(b), (c)-[:REL {type:'OWNS', conf:0.8}]->(b)")
    q("CREATE (:Document {id:'d1', kind:'doc', title:'Platform runbook', uri:'runbook.md'})")
    chunks = [("c_ttl_old", "SESSION_TTL was 60 seconds in config", "2026-01-10", "e_ttl"),
              ("c_ttl_new", "SESSION_TTL raised to 300 seconds in config", "2026-03-05", "e_ttl"),
              ("c_ck", "Checkout errors spiked after the deploy", "2026-02-01", "e_ck"),
              ("c_plat", "On-call rota and escalation contacts for platform engineers", "2026-02-02", "e_plat"),
              ("c_auth", "Latency dashboards and alerts live here", "2026-02-03", "e_auth"),
              ("c_pizza", "Pizza lunch on Friday", "2026-02-04", None)]
    for i, text, d, e in chunks:
        q("MATCH (d:Document {id:'d1'}) CREATE (d)-[:HAS_CHUNK]->(c:Chunk {id:$i, doc_id:'d1', text:$t, kind:'doc', date_ms:$d, emb:vecf32($v)})",
          {"i": i, "t": text, "d": ms(d), "v": vec(text).tolist()})
        if e:
            q("MATCH (c:Chunk {id:$i}),(e:Entity {id:$e}) CREATE (c)-[:MENTIONS {conf:1.0}]->(e)", {"i": i, "e": e})
    for i, text, st, d in [("m_old", "Sessions expire after 60 seconds", "superseded", "2026-01-11"),
                           ("m_new", "Sessions expire after 300 seconds", "active", "2026-03-06")]:
        q("CREATE (:Memory {id:$i, text:$t, kind:'semantic', status:$s, created_ms:$d, source_id:'sess_1', agent:'claude-code', emb:vecf32($v)})",
          {"i": i, "t": text, "s": st, "d": ms(d), "v": vec(text).tolist()})
    q("MATCH (a:Memory {id:'m_new'}),(b:Memory {id:'m_old'}) CREATE (a)-[:SUPERSEDES]->(b)")
    return store


def ids(rs):
    return [r["id"] for r in rs]


def test_parse_time():
    d = lambda s: ms(s + "T00:00:00")
    assert parse_time("what happened in March", NOW) == (d("2026-03-01"), d("2026-04-01"))
    assert parse_time("changes in December 2025", NOW) == (d("2025-12-01"), d("2026-01-01"))
    assert parse_time("in november", NOW) == (d("2025-11-01"), d("2025-12-01"))  # future month -> last year
    assert parse_time("since 2026-03-01", NOW) == (d("2026-03-01"), None)
    assert parse_time("before 2026-03-01", NOW) == (None, d("2026-03-01"))
    assert parse_time("after 2026-03-01", NOW) == (d("2026-03-02"), None)
    assert parse_time("on 2026-03-01", NOW) == (d("2026-03-01"), d("2026-03-02"))
    assert parse_time("between 2026-03-01 and 2026-03-10", NOW) == (d("2026-03-01"), d("2026-03-11"))
    assert parse_time("since 2026-01-01 and before 2026-02-01", NOW) == (d("2026-01-01"), d("2026-02-01"))
    assert parse_time("yesterday", NOW) == (d("2026-10-15"), d("2026-10-16"))
    assert parse_time("errors today", NOW) == (None, None)  # recency cues are not windows
    assert parse_time("the current and latest value now", NOW) == (None, None)
    assert parse_time("last week", NOW) == (NOW - 7 * 86400000, NOW)
    assert parse_time("since last month", NOW) == (NOW - 30 * 86400000, None)
    assert parse_time("past 3 days", NOW) == (NOW - 3 * 86400000, NOW)
    assert parse_time("you may like the setting", NOW) == (None, None)  # "may" alone is not a date
    assert parse_time("what port does it use", NOW) == (None, None)


def test_rrf_math():
    r = rrf({"a": [("x", 9), ("y", 8)], "b": [("y", 1), ("x", 0)]}, {"a": 2.0, "b": 1.0})
    sc = {i: s for i, s, _ in r}
    assert sc["x"] == pytest.approx(2 / 61 + 1 / 62) and sc["y"] == pytest.approx(2 / 62 + 1 / 61)
    assert r[0][0] == "x" and r[0][2] == {"a": 1, "b": 2}
    w = channel_weights({"owner": 1.0})
    assert w["graph"] == 2.0 and w["vector"] == 1.0
    assert channel_weights({"temporal": 0.5})["temporal"] == pytest.approx(0.5 * 2.0)


def test_vector_channel(g):
    r = ch.vector(g, "session ttl seconds config", ch.Filt())
    assert r[0][0] in ("c_ttl_old", "c_ttl_new") and r[0][1] > 0.3
    assert "m_old" not in [i for i, _ in r]  # superseded hidden


def test_bm25_channel_and_rebuild(g):
    assert ch.bm25(g, "pizza friday", ch.Filt())[0][0] == "c_pizza"
    assert ch.bm25(g, "session ttl", ch.Filt())[0][0] in ("c_ttl_old", "c_ttl_new")  # identifier SESSION_TTL is split
    assert ch.bm25(g, "xyzzy", ch.Filt()) == []
    g.query("CREATE (:Chunk {id:'c_new', text:'quokka migration plan', date_ms:$d})", {"d": ms("2026-05-01")})
    assert ch.bm25(g, "quokka", ch.Filt())[0][0] == "c_new"  # cache noticed the new chunk


def test_graph_multihop_answers_what_text_channels_miss(g):
    q = "who owns the service behind checkout"
    paths = {}
    seeds = ch.link_entities(g, [{"name": "Checkout", "type": "service", "conf": 0.9}], q)
    assert seeds["e_ck"][1] == 1.0
    gr = ch.graph(g, [{"name": "Checkout", "type": "service", "conf": 0.9}], q, ch.Filt(), paths=paths)
    assert [i for i, _ in gr][:2] == ["c_ck", "c_plat"] or "c_plat" in [i for i, _ in gr]
    assert paths["c_plat"][0] == "Checkout -[DEPENDS_ON]-> Auth Service <-[OWNS]- Platform Team <-[MENTIONS]- c_plat"
    text_only = recall(g, q, k=3, channels=["vector", "bm25"])
    assert "c_plat" not in ids(text_only)
    res = recall(g, q, k=5)  # the toy corpus is tiny, so the text channels' top-5 anchors also pull in unrelated entities
    hit = next(r for r in res if r["id"] == "c_plat")
    assert "graph" in hit["channels"] and hit["paths"]  # vector only sees it as a low-similarity tail
    assert hit["source"]["title"] == "Platform runbook"


def test_graph_bridging_between_seeds(g):
    q = "how is checkout connected to the platform team"
    paths = {}
    gr = ch.graph(g, [{"name": "Checkout", "type": "service", "conf": 0.9}, {"name": "Platform Team", "type": "team", "conf": 0.9}],
                  q, ch.Filt(), paths=paths)
    got = [i for i, _ in gr]
    assert "c_auth" in got  # mentions only the bridging entity (Auth Service), which sits on the seeds' shortest path
    assert "Checkout -[DEPENDS_ON]-> Auth Service" in paths["c_auth"][0]
    # evidence for either seed outranks pure-hop neighbours
    assert set(got[:3]) == {"c_ck", "c_plat", "c_auth"}


def test_superseded_hidden_unless_temporal(g):
    assert "m_old" not in ids(recall(g, "sessions expire after seconds", k=10, now_ms=NOW))
    rs = recall(g, "what changed about how long sessions expire", k=10, now_ms=NOW)
    assert "m_old" in ids(rs) and "m_new" in ids(rs)
    assert next(r for r in rs if r["id"] == "m_old")["status"] == "superseded"


def test_window_and_kinds(g):
    rs = recall(g, "session ttl seconds", k=10, since_ms=ms("2026-03-01T00:00:00"), until_ms=ms("2026-04-01T00:00:00"), now_ms=NOW)
    assert set(ids(rs)) == {"c_ttl_new", "m_new"}
    rs = recall(g, "session ttl in January 2026 seconds", k=10, now_ms=NOW)  # window parsed from the query
    assert set(ids(rs)) == {"c_ttl_old"}  # m_old is superseded and the question is not temporal
    assert set(r["label"] for r in recall(g, "session ttl seconds", k=10, kinds=["memory"])) == {"Memory"}
    assert set(r["kind"] for r in recall(g, "session ttl seconds", k=10, kinds=["semantic"])) == {"semantic"}


def test_temporal_ordering(g):
    f = ch.Filt(superseded=True)
    pool = {"c_ttl_old", "c_ttl_new", "m_old", "m_new"}
    assert [i for i, _ in ch.temporal(g, f, pool=pool)] == ["m_new", "c_ttl_new", "m_old", "c_ttl_old"]
    assert [i for i, _ in ch.temporal(g, f, pool=pool, asc=True)] == ["c_ttl_old", "m_old", "c_ttl_new", "m_new"]
    rs = recall(g, "what is the latest ttl for sessions", k=3, now_ms=NOW)
    assert "temporal" in rs[0]["channels"]


def test_channels_ablation(g):
    rs = recall(g, "session ttl seconds", k=5, channels=["vector"])
    assert rs and all(set(r["channels"]) == {"vector"} for r in rs)
    assert FakeGliner.calls == 0  # nothing needs GLiNER when only vector runs
    rs = recall(g, "pizza friday", k=5, channels=["bm25"])
    assert ids(rs) == ["c_pizza"]
    rs = recall(g, "session ttl seconds", k=5, weights={"vector": 0.0, "bm25": 1.0, "graph": 1.0})
    assert rs[0]["channels"].get("bm25") == 1
    with pytest.raises(ValueError):
        recall(g, "x", channels=["nope"])


def test_result_shape(g):
    g.query("MATCH (c:Chunk {id:'c_pizza'}) SET c.text = $t", {"t": "pizza " * 200})
    r = recall(g, "pizza", k=1, channels=["bm25"])[0]
    assert r["label"] == "Chunk" and len(r["text"]) <= 401 and r["source"]["doc_id"] == "d1" and r["date_ms"] == ms("2026-02-04")
    m = recall(g, "sessions expire seconds", k=1, channels=["bm25"])[0]
    assert m["id"] == "m_new" and m["source"]["source_id"] == "sess_1" and m["source"]["agent"] == "claude-code"


def test_entity_linking_fuzzy_and_vector(g):
    e = lambda n: [{"name": n, "type": "service", "conf": 0.9}]
    fz = ch.link_entities(g, e("Chekout"), "zzz")  # typo: full-text fuzzy
    assert 0.6 <= fz["e_ck"][1] < 0.8
    vc = ch.link_entities(g, e("team platform"), "zzz")  # word order: fuzzy ratio too low, embedding NN
    assert vc["e_plat"][1] == 0.6
    assert ch.link_entities(g, e("kubernetes"), "zzz") == {}



def test_empty_window_falls_back_to_recency(g):
    rs = recall(g, "session ttl seconds in March 2020", k=5, now_ms=NOW)  # nothing dated 2020: window dropped, newest first
    assert ids(rs).index("c_ttl_new") < ids(rs).index("c_ttl_old") and "temporal" in rs[0]["channels"]
    assert recall(g, "session ttl seconds today", k=3, now_ms=NOW)  # "today" is a recency cue, not a one-day window
    assert recall(g, "session ttl seconds", k=5, since_ms=ms("2020-01-01T00:00:00"), until_ms=ms("2020-02-01T00:00:00"), now_ms=NOW) == []  # explicit args stay hard


def test_ppr_specificity_bridge_and_current(g):
    q = g.query
    q("CREATE (:Entity {id:'e_hub', name:'Hub Person', key:'hub person', type:'person', mentions:40}), (:Entity {id:'e_rare', name:'Rare Person', key:'rare person', type:'person', mentions:1})")
    for i in range(6):  # the hub is on six chunks, the rare person on one chunk that also mentions Checkout
        q("CREATE (:Chunk {id:$i, doc_id:'d1', text:'x', kind:'doc', date_ms:1})", {"i": f"h{i}"})
        q("MATCH (c:Chunk {id:$i}),(e:Entity {id:'e_hub'}) CREATE (c)-[:MENTIONS {conf:1.0}]->(e)", {"i": f"h{i}"})
    q("CREATE (:Chunk {id:'r0', doc_id:'d1', text:'y', kind:'doc', date_ms:1})")
    q("MATCH (c:Chunk {id:'r0'}),(e:Entity) WHERE e.id IN ['e_rare','e_ck'] CREATE (c)-[:MENTIONS {conf:1.0}]->(e)")
    mass, names, trail = ch.ppr(g, {"e_ck": 1.0}, {})
    assert abs(sum(mass.values()) - 1) < 1e-6 and mass["e_ck"] > mass["e_auth"] > 0  # a probability distribution, decaying with distance
    assert mass["r0"] > mass["c_ck"] * 0 and mass["e_rare"] > 0 and "e_hub" not in mass  # r0 bridges Checkout to Rare Person
    assert trail("e_rare") == ["Checkout", ("MENTIONS", False, "r0"), ("MENTIONS", True, "Rare Person")]
    # mass reaching a hub through a shared chunk is divided over all of its chunks, so each one stays small
    q("MATCH (c:Chunk {id:'r0'}),(e:Entity {id:'e_hub'}) CREATE (c)-[:MENTIONS {conf:1.0}]->(e)")
    mass, _, _ = ch.ppr(g, {"e_ck": 1.0}, {})
    assert max(mass[f"h{i}"] for i in range(6)) < mass["r0"] / 4
    # REL edges that ended are ignored unless the question is about change
    q("MATCH (:Entity {id:'e_ck'})-[r:REL]->(:Entity {id:'e_auth'}) SET r.valid_to_ms = 5")
    cur, _, _ = ch.ppr(g, {"e_ck": 1.0}, {}, now=10, current=True)
    old, _, _ = ch.ppr(g, {"e_ck": 1.0}, {}, now=10, current=False)
    assert "e_auth" not in cur and old["e_auth"] > 0


def test_linking_drops_generic_and_junk(g):
    e = lambda n: [{"name": n, "type": "other", "conf": 0.9}]
    assert ch.link_entities(g, e("platform engineer"), "zzz") == {}  # role word only
    assert ch.link_entities(g, e("configuration edit"), "zzz") == {}
    assert "e_auth" in ch.link_entities(g, e("auth"), "how does the auth flow work")  # a rare content word of the entity name
    assert len(ch.link_entities(g, e("checkout"), "checkout auth platform team session ttl", cap=2)) <= 2


def test_ppr_bounds_nodes_within_a_hop(g):
    """A hub with 1500 REL neighbours must not grow the dense matrix past MAX_NODES inside one hop."""
    g.query("CREATE (:Entity {id:'e_big', name:'Big Hub', key:'big hub', type:'service', mentions:1})")
    ids = [f"n{i}" for i in range(1500)]
    g.query("UNWIND $ids AS i CREATE (:Entity {id:i, name:i, key:i, type:'service', mentions:1})", {"ids": ids})
    g.query("UNWIND $ids AS i MATCH (a:Entity {id:'e_big'}), (b:Entity {id:i}) "
            "CREATE (a)-[:REL {type:'RELATED_TO', conf:0.5, source_id:'x', valid_from_ms:1}]->(b)", {"ids": ids})
    mass, _, _ = ch.ppr(g, {"e_big": 1.0}, {})
    assert 0 < len(mass) <= ch.MAX_NODES
    assert abs(sum(mass.values()) - 1) < 1e-6


def test_invalid_calendar_dates_skipped():
    assert parse_time("between 2026-02-30 and 2026-03-02") == (None, None)  # not a date: no window, no exception
    assert parse_time("events in 2026-02-31") == (None, None)
    assert parse_time("December 9999") == (None, None)  # the month after December 9999 is out of range
    assert parse_time("since December 9999") == (None, None)
    assert parse_time("between 2026-03-01 and 2026-03-02")[0] is not None  # valid ranges still work


def test_graph_off_without_a_strong_seed(g):
    """Anchors alone (what the top text hits mention) never start the walk; a hub seed walks too little to count."""
    info = {}
    assert ch.graph(g, [], "pizza friday", ch.Filt(), anchors=["c_pizza"], info=info) == []
    assert all("graph" not in r["channels"] for r in recall(g, "pizza friday", k=5))
    g.query("MATCH (e:Entity {id:'e_ck'}) SET e.mentions = 500")  # named in hundreds of nodes: little to say about one
    info = {}
    assert ch.graph(g, [{"name": "Checkout", "type": "service", "conf": 0.9}], "checkout", ch.Filt(), info=info) == []
    assert info["strength"] < ch.SEED_FLOOR


def test_decision_cue_routes_to_decision_records(g):
    """A "why" question boosts decision memories (soft: through the fused score, never a filter)."""
    text = "We dropped the queue for checkout because of latency"
    g.query("CREATE (:Memory {id:'m_dec', text:$t, kind:'decision', status:'active', created_ms:$d, source_id:'sess_1', "
            "agent:'claude-code', emb:vecf32($v)})", {"t": text, "d": ms("2026-02-10"), "v": vec(text).tolist()})
    assert recall(g, "why did we drop the checkout queue?", k=3)[0]["id"] == "m_dec"
    assert "m_dec" in ids(recall(g, "checkout queue latency", k=8))  # no cue: still found, not boosted by kind


def test_decision_cue_and_kind_factor():
    from neo_cortex.retrieve import parse_query as pqy
    from neo_cortex.retrieve.fuse import kind_factor
    assert pqy("why was graphrag-sdk dropped?", nlp=False)["intent"] == {"decision": 0.6}
    assert pqy("what port does the daemon use?", nlp=False)["intent"] == {}
    assert kind_factor({"decision": 0.5}, "decision") == 1.5 and kind_factor({"decision": 0.5}, "adr") == 1.5
    assert kind_factor({"decision": 0.5}, "semantic") == 1.0 and kind_factor({}, "decision") == 1.0


def test_bm25_keeps_numbers_and_flags(g):
    """Numbers and --flags are tokens: "port 8765" finds the chunk that says `neo serve --port 8765`."""
    g.query("CREATE (:Chunk {id:'c_port', text:'Start the daemon with neo serve --port 8765 --warm', kind:'doc', date_ms:1})")
    assert ch.bm25(g, "port 8765", ch.Filt())[0][0] == "c_port"
    assert ch.bm25(g, "daemon port", ch.Filt())[0][0] == "c_port"
