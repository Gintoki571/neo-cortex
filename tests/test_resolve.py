"""Entity resolution: spelling variants merge into one entity with aliases; different products never merge."""
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
