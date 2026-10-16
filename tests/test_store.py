import subprocess

import numpy as np

from neo_cortex.schema import ensure_schema
from neo_cortex.store import Store


def _servers(home):
    out = subprocess.run(["pgrep", "-af", "redis-server"], capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if str(home) in l or ":6391" in l]


def test_open_close_no_orphan(tmp_path, monkeypatch):
    monkeypatch.setenv("NEO_HOME", str(tmp_path))
    monkeypatch.setenv("NEO_PORT", "6391")
    s = Store()
    assert s.query("RETURN 1") == [[1]]
    assert _servers(tmp_path)
    s.close()
    assert not _servers(tmp_path)


def test_bound_to_loopback(store):
    out = subprocess.run(["ss", "-ltn"], capture_output=True, text=True).stdout
    line = [l for l in out.splitlines() if ":6391" in l]
    assert line and all("127.0.0.1:6391" in l for l in line)


def test_schema_idempotent(store):
    g = store.graph()
    ensure_schema(g)
    ensure_schema(g)
    have = {(r[0], p, t) for r in g.query("CALL db.indexes()").result_set for p, ts in r[2].items() for t in ts}
    for want in [("Memory", "emb", "VECTOR"), ("Chunk", "emb", "VECTOR"), ("Entity", "emb", "VECTOR"),
                 ("Entity", "name", "FULLTEXT"), ("Memory", "valid_from", "RANGE"), ("Person", "id", "RANGE"),
                 ("Entity", "key", "RANGE")]:
        assert want in have, want


def test_vector_roundtrip_score_is_distance(store):
    rng = np.random.default_rng(0)
    v = rng.normal(size=(5, 768)).astype("float32")
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    for i in range(5):
        store.query("CREATE (:Memory {id:$i, emb: vecf32($e)})", {"i": f"m{i}", "e": v[i].tolist()})
    rows = store.query("CALL db.idx.vector.queryNodes('Memory','emb',3,vecf32($q)) "
                       "YIELD node, score RETURN node.id, score ORDER BY score", {"q": v[2].tolist()})
    assert rows[0][0] == "m2" and rows[0][1] < 1e-3          # self is nearest: distance ~0
    assert rows[1][1] > rows[0][1]


def test_tenants_isolated(store):
    store.query("CREATE (:Memory {id:'a'})", tenant="t1")
    store.query("CREATE (:Memory {id:'b'})", tenant="t2")
    assert store.query("MATCH (m:Memory) RETURN m.id", tenant="t1") == [["a"]]
    assert store.query("MATCH (m:Memory) RETURN m.id", tenant="t2") == [["b"]]
