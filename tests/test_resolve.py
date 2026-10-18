"""Entity resolution: spelling variants merge into one entity with aliases; different products never merge."""
import pytest

from neo_cortex import resolve


def _count(store):
    return store.query("MATCH (e:Entity) RETURN count(e)")[0][0]


def test_variant_key_drops_spacing_case_punctuation_and_size_or_version():
    vk = resolve.variant_key
    assert vk("gliner2 5") == vk("gliner2 5 base") == vk("gliner2 5 base v1") == vk("gliner 2 5") == "gliner 2 5"
    assert vk("gliner 2 5 hf") == "gliner 2 5" and vk("api v1") == "api" and vk("api v2") != vk("api")
    # different products or versions stay apart
    assert len({vk("gliner2"), vk("gliner2 5"), vk("gliner2 5 decide"), vk("gliner 25"), vk("gliner2 pypi")}) == 5
    assert vk("auth service") != vk("auth gateway") and vk("database") == "database" and vk("base") == "base"


def test_spelling_variants_merge_into_one_entity(store, fake_models):
    first = resolve.resolve_entity(store, "GLiNER2.5", "tool")
    for name in ["GLiNER2.5 base", "gliner2.5-base-v1", "GLiNER 2.5", "gliner-2.5-hf", "GLiNER2.5 Base"]:
        assert resolve.resolve_entity(store, name, "tool") == first, name
    assert _count(store) == 1
    aliases = store.query("MATCH (e:Entity {id:$i}) RETURN e.aliases", {"i": first})[0][0]
    assert {"gliner2 5 base", "gliner 2 5"} <= set(aliases)


def test_different_products_do_not_merge(store, fake_models):
    names = [("GLiNER2", "tool"), ("GLiNER2.5", "tool"), ("GLiNER2.5-Decide", "product"), ("GLiNER", "tool"),
             ("gliner2-pypi", "file"), ("auth-service", "service"), ("auth-gateway", "service"),
             ("Noor Haddad", "person"), ("Samir Haddad", "person")]
    ids = [resolve.resolve_entity(store, n, t) for n, t in names]
    assert len(set(ids)) == len(names) and _count(store) == len(names)


def test_same_key_still_merges(store, fake_models):
    gw = resolve.resolve_entity(store, "auth-gateway", "service")
    assert resolve.resolve_entity(store, "Auth Gateway", "service") == gw


def test_code_identifiers_never_merge_by_similarity(store, fake_models):
    import numpy as np
    v = np.ones(768, dtype=np.float32) / np.sqrt(768)   # identical embeddings: only the lexical guard could merge them
    a = resolve.resolve_entity(store, "_sentences", "component", emb=v)
    assert resolve.resolve_entity(store, "_sentence", "component", emb=v) != a
    b = resolve.resolve_entity(store, "_hard_split", "component", emb=v)
    assert resolve.resolve_entity(store, "_split", "component", emb=v) != b
    assert resolve.resolve_entity(store, "_sentences", "component", emb=v) == a   # exact key still merges


def test_similarity_still_merges_plain_names(store, fake_models):
    import numpy as np
    v = np.ones(768, dtype=np.float32) / np.sqrt(768)   # control for the test above: plain names do merge on similarity
    g = resolve.resolve_entity(store, "api-gateway", "service", emb=v)
    assert resolve.resolve_entity(store, "api-gateways", "service", emb=v) == g


def _types(store, eid):
    return store.query("MATCH (e:Entity {id:$i}) RETURN e.type", {"i": eid})[0][0]


def test_majority_vote_beats_one_higher_ranked_mention(store, fake_models):
    # 50 GLiNER tool votes against one team vote: the type is tool (the old rank rule made it team)
    eid = resolve.resolve_entity(store, "FalkorDB", "team", weight=0.85)
    for _ in range(50):
        assert resolve.resolve_entity(store, "FalkorDB", "tool", weight=0.8) == eid
    assert _types(store, eid) == "tool"


def test_pins_explicit_beats_regex_beats_vote(store, fake_models):
    eid = resolve.resolve_entity(store, "IDN-212", "tool", weight=5.0)       # many confident GLiNER votes
    resolve.resolve_entity(store, "IDN-212", "ticket", weight=1.0, pin=resolve.PIN_REGEX)
    assert _types(store, eid) == "ticket"
    resolve.resolve_entity(store, "IDN-212", "decision", weight=0.1, pin=resolve.PIN_EXPLICIT)
    assert _types(store, eid) == "decision"
    resolve.resolve_entity(store, "IDN-212", "tool", weight=50.0)           # a vote never overrides a pin
    assert _types(store, eid) == "decision"


def test_other_votes_abstain_and_ties_fall_back_to_rank(store, fake_models):
    eid = resolve.resolve_entity(store, "auth gateway", "other", weight=3.0)
    assert _types(store, eid) == "other"
    resolve.resolve_entity(store, "auth gateway", "service", weight=0.5)
    assert _types(store, eid) == "service"                                  # one real vote beats any number of "other"
    a = resolve.resolve_entity(store, "api edge", "component", weight=1.0)
    resolve.resolve_entity(store, "api edge", "service", weight=1.0)
    assert _types(store, a) == "service"                                     # equal votes: _RANK decides


def test_resolve_many_accepts_weighted_items(store, fake_models):
    ids = resolve.resolve_many(store, [("session cache", "service", 0.9, resolve.PIN_VOTE),
                                       ("session cache", "tool", 0.2, resolve.PIN_VOTE), ("Session Cache", "tool")])
    assert len(set(ids)) == 1 and _types(store, ids[0]) == "tool"           # 0.9 service vs 0.2 + 1.0 tool


@pytest.fixture
def same_vec(monkeypatch):
    """Every text gets one identical embedding: the vector path would merge any pair the lexical guard lets through."""
    import numpy as np

    from neo_cortex import write
    v = np.ones(768, dtype=np.float32) / np.sqrt(768)
    f = lambda texts, titles=None: np.stack([v] * len(texts))  # noqa: E731
    monkeypatch.setattr(resolve, "embed_docs", f)
    monkeypatch.setattr(write, "embed_docs", f)


def test_plural_s_after_a_digit_is_not_a_plural():
    assert resolve._stem("bm25s") == ["bm25s"] and resolve._stem("k8s") == ["k8s"]
    assert resolve._stem("services") == ["service"] and resolve._stem("auth services") == ["auth", "service"]
    assert not resolve._guard("bm25s", "bm25", "tool", "tool") and not resolve._guard("k8s", "k8", "tool", "tool")
    assert resolve._guard("services", "service", "service", "service")


def test_explicit_remember_entity_does_not_merge_into_a_similar_name(store, fake_models, same_vec):
    from neo_cortex import tools
    bm25 = resolve.resolve_entity(store, "BM25", "tool")
    out = tools.remember(store, "The agent indexes chunks with bm25s", kind="semantic", entities=[{"name": "bm25s", "type": "tool"}])
    assert out.startswith("created"), out
    assert _count(store) == 2
    assert store.query("MATCH (m:Memory)-[:MENTIONS]->(e:Entity) RETURN e.key") == [["bm25s"]]
    assert store.query("MATCH (e:Entity {id:$i}) RETURN e.aliases", {"i": bm25})[0][0] == []


def test_explicit_relation_endpoint_does_not_merge_into_a_similar_name(store, fake_models, same_vec):
    from neo_cortex import tools
    resolve.resolve_entity(store, "BM25", "tool")
    tools.remember(store, "The agent depends on bm25s", kind="semantic", relations=[["bm25s", "DEPENDS_ON", "checkout"]])
    assert store.query("MATCH (a:Entity)-[r:REL]->(b:Entity) RETURN a.key, r.type, b.key") == [["bm25s", "DEPENDS_ON", "checkout"]]
    assert _count(store) == 3
    tools.relate(store, "bm25s", "DEPENDS_ON", "checkout")  # relate resolves the same way: exact key or alias, else new
    assert _count(store) == 3


def test_plural_still_merges_through_ingest_resolution(store, fake_models, same_vec):
    # default pin (a GLiNER or document vote): "services" merges with "service" by the plural rule
    a, b = resolve.resolve_many(store, [("auth service", "service"), ("auth services", "service")])
    assert a == b and _count(store) == 1


def test_caller_named_lone_surname_stays_ambiguous_and_never_merges(store, fake_models):
    resolve.resolve_entity(store, "Noor Haddad", "person")
    resolve.resolve_entity(store, "Samir Haddad", "person")
    assert resolve.resolve_entity(store, "Haddad", "person", pin=resolve.PIN_EXPLICIT) is None  # refuse, never guess
    assert resolve.resolve_entity(store, "Haddad", "person") is None
    assert resolve.resolve_entity(store, "Noor", "person", pin=resolve.PIN_EXPLICIT) not in (None, store.query(
        "MATCH (e:Entity {key:'noor haddad'}) RETURN e.id")[0][0])  # a caller-named "Noor" is its own entity, not Noor Haddad


# --- NEO_RESOLVE_JW -----------------------------------------------------------------------------------------------


def test_jaro_winkler_math():
    jw = resolve.jaro_winkler
    assert jw("falkordb", "falkordb") == 1.0
    assert jw("", "x") == 0.0 and jw("abc", "xyz") == 0.0
    assert 0.9 <= jw("falkordb", "falkordblite") <= 1.0        # the merge case the flag is for
    assert jw("api v2", "api v3") >= 0.9                        # high JW, but blocked by the numeric rule instead
    assert jw("checkout", "outcheck") < 0.9                     # transposed words: low JW despite shared letters


def test_jw_extra_merge_path(store, fake_models, monkeypatch):
    monkeypatch.setenv("NEO_RESOLVE_JW", "1")
    a = resolve.resolve_entity(store, "FalkorDB", "tool")
    assert resolve.resolve_entity(store, "falkordblite", "tool") == a   # guard keeps them apart, JW merges
    assert _count(store) == 1
    b = resolve.resolve_entity(store, "FalkorDB Lite", "person")        # wrong type family: never merges
    assert b != a and _count(store) == 2


def test_jw_path_off_by_default(store, fake_models, monkeypatch):
    monkeypatch.delenv("NEO_RESOLVE_JW", raising=False)
    a = resolve.resolve_entity(store, "FalkorDB", "tool")
    assert resolve.resolve_entity(store, "falkordblite", "tool") != a and _count(store) == 2


def test_jw_numeric_tokens_hard_block(store, fake_models, monkeypatch):
    monkeypatch.setenv("NEO_RESOLVE_JW", "1")
    a = resolve.resolve_entity(store, "API v2", "service")
    assert resolve.resolve_entity(store, "API v3", "service") != a      # JW >= 0.9 but v2 != v3
    c = resolve.resolve_entity(store, "GLiNER2.5", "tool")
    assert resolve.resolve_entity(store, "GLiNER2", "tool") != c        # 2.5 is not 2
    assert _count(store) == 4


def test_jw_never_merges_persons_or_explicit(store, fake_models, monkeypatch):
    monkeypatch.setenv("NEO_RESOLVE_JW", "1")
    p = resolve.resolve_entity(store, "Noor Haddad", "person")
    assert resolve.resolve_entity(store, "Noor Haddadi", "person") != p  # person names never merge fuzzily
    g = resolve.resolve_entity(store, "auth gateway", "service")
    assert resolve.resolve_entity(store, "auth gateways", "service", pin=resolve.PIN_EXPLICIT) != g  # explicit: exact only
    assert _count(store) == 4  # explicit names are never merged away: "auth gateways" is its own entity


def _boost_graph(store):
    """e_x co-mentioned with e_h1/e_h2 in one chunk; a query at cosine 0.88 to e_x sees all three as candidates."""
    import numpy as np
    q = store.query
    e = [np.zeros(768, dtype=np.float32) for _ in range(3)]
    for v, i in zip(e, range(3)):
        v[i] = 1.0
    vq = 0.88 * e[0] + 0.33 * e[1] + 0.33 * e[2]
    vq = vq / np.linalg.norm(vq)          # cos to e0 = 0.883: SOFT band, judge decides without the boost
    for eid, k, n, t, v in [("e_x", "report engine", "Report Engine", "service", e[0]),
                            ("e_h1", "helper alpha", "Helper Alpha", "tool", e[1]),
                            ("e_h2", "helper beta", "Helper Beta", "tool", e[2])]:
        q("CREATE (:Entity {id:$i, key:$k, name:$n, type:$t, type_votes:'{}', aliases:[], emb:vecf32($e), "
          "first_seen_ms:1, last_seen_ms:1, mentions:2})", {"i": eid, "k": k, "n": n, "t": t, "e": v.tolist()})
    q("CREATE (:Chunk {id:'c1', doc_id:'d1', text:'x', kind:'doc'})")
    q("MATCH (c:Chunk {id:'c1'}),(a:Entity),(b:Entity),(d:Entity) WHERE a.id='e_x' AND b.id='e_h1' AND d.id='e_h2' "
      "CREATE (c)-[:MENTIONS {conf:1.0}]->(a),(c)-[:MENTIONS {conf:1.0}]->(b),(c)-[:MENTIONS {conf:1.0}]->(d)")
    return vq


def test_shared_neighbour_boost_pushes_guarded_pair_over_hard(store, fake_models, monkeypatch):
    monkeypatch.setenv("NEO_RESOLVE_JW", "1")
    vq = _boost_graph(store)
    assert resolve.resolve_entity(store, "report engines", "service", emb=vq) == "e_x"  # 0.883 + 2 neighbours = 0.923
    assert _count(store) == 3


def test_without_boost_the_judge_vetoes_the_same_pair(store, fake_models, monkeypatch):
    from neo_cortex import extract
    monkeypatch.delenv("NEO_RESOLVE_JW", raising=False)
    monkeypatch.setattr(extract, "_softmax_labels", lambda text, task, labels: {"same": 0.01, "different": 0.99})
    vq = _boost_graph(store)
    assert resolve.resolve_entity(store, "report engines", "service", emb=vq) != "e_x"  # judge veto at 0.883
    assert _count(store) == 4
