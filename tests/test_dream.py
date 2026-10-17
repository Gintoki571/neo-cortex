"""neo dream: one test per step, plus idempotence and dry_run. Memories get controlled vectors: each group owns two
dimensions and an angle, so cosine = cos(angle difference) and groups never interact."""
import math

import numpy as np

from neo_cortex import dream as D

DAY = 86_400_000
NOW = 1_800_000_000_000


def vec(deg, g):
    v = np.zeros(768, dtype=np.float32)
    v[2 * g], v[2 * g + 1] = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return v.tolist()


def _q(store, c, /, **p):
    return store.query(c, p)


def mem(store, mid, text, kind="episodic", deg=0, g=0, created=NOW - 40 * DAY, uses=0, last_used=NOW - DAY, conf=0.9):
    _q(store, "CREATE (:Memory {id:$id, text:$text, kind:$kind, status:'active', confidence:$conf, created_ms:$c, "
              "valid_from_ms:$c, uses:$u, last_used_ms:$l, emb:vecf32($e)})",
       id=mid, text=text, kind=kind, conf=conf, c=created, u=uses, l=last_used, e=vec(deg, g))


def session(store, sid):
    _q(store, "CREATE (:Session {id:$s, agent:'claude-code', project:'p', started_ms:0, path:'x'})", s=sid)


def entity(store, eid):
    _q(store, "CREATE (:Entity {id:$i, key:$i, name:$i, type:'service', mentions:0})", i=eid)


def link(store, a, b, typ, props=""):
    _q(store, f"MATCH (a {{id:$a}}), (b {{id:$b}}) CREATE (a)-[:{typ} {props}]->(b)", a=a, b=b)


def _merge_world(store):
    mem(store, "a", "Run pytest with NEO_TEST_PORT set", deg=0, uses=2, created=NOW - 30 * DAY)
    mem(store, "b", "Always run pytest with NEO_TEST_PORT set", deg=10, uses=3, created=NOW - 20 * DAY)
    mem(store, "c", "Deploys happen on Tuesdays", deg=60, created=NOW - 5 * DAY)
    mem(store, "d", "Run pytest with NEO_TEST_PORT set", kind="semantic", deg=0, created=NOW - 40 * DAY)  # other kind
    session(store, "s0")
    session(store, "s1")
    entity(store, "e1")
    link(store, "a", "s0", "DERIVED_FROM")
    link(store, "b", "s1", "DERIVED_FROM")
    link(store, "b", "e1", "MENTIONS", "{conf:1.0}")


def _promote_world(store):
    for i in (1, 2, 3):
        session(store, f"ps{i}")
    mem(store, "p1", "Deploy freezes start on Fridays", deg=0, g=1, created=NOW - 40 * DAY)
    mem(store, "p2", "Freeze the deploys on Fridays at noon", deg=30, g=1, created=NOW - 30 * DAY, uses=4)
    mem(store, "p3", "Friday deploy freeze is enforced", deg=-30, g=1, created=NOW - 20 * DAY)
    for pid, sid in (("p1", "ps1"), ("p2", "ps2"), ("p3", "ps3")):
        link(store, pid, sid, "DERIVED_FROM")
    # two sessions only (s1 twice): must not promote
    session(store, "qs1")
    session(store, "qs2")
    mem(store, "q1", "Use feature flags for rollout", deg=90, g=2, created=NOW - 15 * DAY)
    mem(store, "q2", "Feature flags drive rollout", deg=120, g=2, created=NOW - 14 * DAY)
    mem(store, "q3", "Rollout uses feature flags", deg=60, g=2, created=NOW - 13 * DAY)
    link(store, "q1", "qs1", "DERIVED_FROM")
    link(store, "q2", "qs1", "DERIVED_FROM")
    link(store, "q3", "qs2", "DERIVED_FROM")


def _decay_world(store):
    mem(store, "x1", "Old fact about queues", deg=0, g=3, last_used=NOW - 65 * DAY)                 # 2 periods
    mem(store, "x2", "Old preference about tabs", kind="preference", deg=100, g=3, last_used=NOW - 200 * DAY)
    mem(store, "x3", "Recent fact about caches", deg=200, g=3, last_used=NOW - 10 * DAY)
    mem(store, "x4", "Ancient fact about logs", deg=300, g=3, last_used=NOW - 400 * DAY, conf=0.2)  # hits the floor
    mem(store, "x5", "Old decision about hosting", kind="decision", deg=45, g=3, last_used=NOW - 400 * DAY)


def _conflict_world(store):
    entity(store, "e2")
    mem(store, "cA", "The session TTL is 900 seconds for auth-service", kind="semantic", deg=0, g=4)
    mem(store, "cB", "The session TTL is 3600 seconds for auth-service", kind="semantic", deg=30, g=4)
    mem(store, "cC", "The session TTL is 900 seconds for auth-service", kind="semantic", deg=-30, g=4)
    mem(store, "cD", "Auth-service never caches sessions", kind="decision", deg=60, g=4)
    mem(store, "cE", "The session TTL is 3600 seconds for auth-service", deg=30, g=4)  # episodic: same rule as remember
    mem(store, "cF", "The session TTL is 3600 seconds", kind="semantic", deg=60, g=4)  # no entity: a near-duplicate still conflicts
    for m in ("cA", "cB", "cC", "cD", "cE"):
        link(store, m, "e2", "MENTIONS", "{conf:1.0}")


def _world(store):
    _merge_world(store)
    _promote_world(store)
    _decay_world(store)
    _conflict_world(store)


def _state(store):
    return (_q(store, "MATCH (m:Memory) RETURN m.id, m.status, m.confidence, m.uses, m.decayed_ms ORDER BY m.id"),
            _q(store, "MATCH ()-[r]->() RETURN type(r), count(r) ORDER BY type(r)"),
            _q(store, "MATCH (n) WHERE NOT n:DreamRun RETURN labels(n)[0], count(n) ORDER BY labels(n)[0]"))


def test_merge_near_duplicates(store):
    _merge_world(store)
    r = D.dream(store, now_ms=NOW)
    assert r["merged"] == 1 and r["promoted"] == 0
    assert _q(store, "MATCH (b:Memory {id:'b'}) RETURN b.status") == [["merged"]]
    assert _q(store, "MATCH (:Memory {id:'b'})-[:MERGED_INTO]->(a:Memory {id:'a'}) RETURN count(*)") == [[1]]
    assert _q(store, "MATCH (a:Memory {id:'a'}) RETURN a.uses") == [[5]]              # 2 + 3
    assert _q(store, "MATCH (:Memory {id:'a'})-[:MENTIONS]->(e) RETURN e.id") == [["e1"]]   # re-pointed
    assert _q(store, "MATCH (:Memory {id:'b'})-[:MENTIONS|DERIVED_FROM]->() RETURN count(*)") == [[0]]
    assert _q(store, "MATCH (:Memory {id:'a'})-[:DERIVED_FROM]->(s) RETURN s.id ORDER BY s.id") == [["s0"], ["s1"]]
    assert _q(store, "MATCH (m:Memory) WHERE m.id IN ['c','d'] RETURN m.status ORDER BY m.id") == [["active"], ["active"]]


def test_promote_recurring_episodes(store):
    _promote_world(store)
    r = D.dream(store, now_ms=NOW)
    assert r["promoted"] == 1 and r["merged"] == 0
    rows = _q(store, "MATCH (s:Memory {kind:'semantic'})-[:DERIVED_FROM]->(m:Memory) RETURN s.text, s.confidence, "
                     "m.id ORDER BY m.id")
    assert {x[2] for x in rows} == {"p1", "p2", "p3"}
    assert rows[0][0] == "Freeze the deploys on Fridays at noon"                      # most-used member's text
    assert abs(rows[0][1] - 0.8) < 1e-6                                              # min(0.95, 0.5 + 0.1 * 3)
    assert _q(store, "MATCH (m:Memory) WHERE m.id IN ['q1','q2','q3'] AND m.status='active' RETURN count(m)") == [[3]]


def test_decay_unused_memories(store):
    _decay_world(store)
    r = D.dream(store, now_ms=NOW)
    assert r["decayed"] == 2                                                         # x1 and x4
    conf = dict(_q(store, "MATCH (m:Memory) RETURN m.id, m.confidence"))
    assert abs(conf["x1"] - 0.9 * 0.9 ** 2) < 1e-6                                   # 65 days = 2 whole periods
    assert conf["x2"] == 0.9 and conf["x3"] == 0.9 and conf["x5"] == 0.9            # preference, recent, decision
    assert conf["x4"] == 0.1                                                         # floor, never deleted
    assert _q(store, "MATCH (m:Memory {id:'x1'}) RETURN m.decayed_ms") == [[NOW - 5 * DAY]]
    assert _q(store, "MATCH (m:Memory) RETURN count(m)") == [[5]]


def test_conflicts_surface_but_do_not_resolve(store):
    _conflict_world(store)
    r = D.dream(store, now_ms=NOW)
    assert r["conflicts"] == 5
    pairs = {tuple(sorted(x)) for x in _q(store, "MATCH (a:Memory)-[:CONFLICTS_WITH]->(b:Memory) RETURN a.id, b.id")}
    # number or negation differs, cosine >= 0.75 with a shared entity (cA-cB, cA-cE, cB-cD, cD-cE) or >= 0.92 (cD-cF);
    # cB-cF is 0.87 with no shared entity, and cA-cC are identical texts
    assert pairs == {("cA", "cB"), ("cA", "cE"), ("cB", "cD"), ("cD", "cE"), ("cD", "cF")}
    assert _q(store, "MATCH (:Memory)-[c:CONFLICTS_WITH]->(:Memory) RETURN c.found_ms LIMIT 1") == [[NOW]]
    assert _q(store, "MATCH (m:Memory) WHERE m.id IN ['cA','cB','cD'] RETURN m.status ORDER BY m.id") == \
        [["active"], ["active"], ["active"]]


def test_idempotent_second_run_changes_nothing(store):
    _world(store)
    first = D.dream(store, now_ms=NOW)
    assert first["merged"] == 1 and first["promoted"] == 1 and first["decayed"] == 2 and first["conflicts"] == 5
    before = _state(store)
    second = D.dream(store, now_ms=NOW + 60_000)                                     # right after the first
    assert second["merged"] == second["promoted"] == second["decayed"] == second["conflicts"] == 0
    assert _state(store) == before
    assert _q(store, "MATCH (r:DreamRun) RETURN count(r)") == [[2]]                  # each run logs itself


def test_dry_run_reports_without_writing(store):
    _world(store)
    before = _state(store)
    dry = D.dream(store, now_ms=NOW, dry_run=True)
    assert dry["id"] is None and dry["dry_run"] is True
    assert _state(store) == before
    assert _q(store, "MATCH (r:DreamRun) RETURN count(r)") == [[0]]
    real = D.dream(store, now_ms=NOW)
    assert {k: dry[k] for k in ("merged", "promoted", "decayed", "conflicts")} == \
        {k: real[k] for k in ("merged", "promoted", "decayed", "conflicts")}
    assert _q(store, "MATCH (r:DreamRun) RETURN r.merged, r.promoted, r.decayed, r.conflicts") == \
        [[real["merged"], real["promoted"], real["decayed"], real["conflicts"]]]


def test_differing_numbers_are_never_merged(store):
    # "200" arrives after "100": a near-identical sentence with another number is a new fact, not a duplicate
    mem(store, "r1", "Rate limit is 100 requests per minute", kind="semantic", deg=0, g=5)
    mem(store, "r2", "Rate limit is 200 requests per minute", kind="semantic", deg=5, g=5, created=NOW - 2 * DAY)
    r = D.dream(store, now_ms=NOW)
    assert r["merged"] == 0
    assert _q(store, "MATCH (m:Memory) RETURN m.id, m.status ORDER BY m.id") == [["r1", "active"], ["r2", "active"]]


def test_differing_numbers_conflict_even_when_near_duplicate(store):
    entity(store, "e5")
    mem(store, "n1", "Rate limit is 100 requests per minute", kind="semantic", deg=0, g=6)
    mem(store, "n2", "Rate limit is 200 requests per minute", kind="semantic", deg=5, g=6, created=NOW - 2 * DAY)
    link(store, "n1", "e5", "MENTIONS", "{conf:1.0}")
    link(store, "n2", "e5", "MENTIONS", "{conf:1.0}")
    r = D.dream(store, now_ms=NOW)
    assert r["merged"] == 0 and r["conflicts"] == 1
    assert _q(store, "MATCH (:Memory {id:'n1'})-[:CONFLICTS_WITH]->(:Memory {id:'n2'}) RETURN count(*)") == [[1]]


def test_near_duplicate_that_differs_conflicts_without_entities(store):
    # the remember() case: "deadline is ...18" vs "...19" at cosine 0.99, no entities; remember flags it, so dream must too
    mem(store, "dl1", "The release deadline is 2026-10-18", kind="decision", deg=0, g=7)
    mem(store, "dl2", "The release deadline is 2026-10-19", kind="decision", deg=2, g=7, created=NOW - 2 * DAY)
    r = D.dream(store, now_ms=NOW)
    assert r["merged"] == 0 and r["conflicts"] == 1
    assert _q(store, "MATCH (:Memory {id:'dl1'})-[:CONFLICTS_WITH]->(:Memory {id:'dl2'}) RETURN count(*)") == [[1]]


def test_dream_waits_for_the_store_write_lock(store, monkeypatch):
    import threading
    _merge_world(store)
    reached = threading.Event()
    real_load = D._load

    def spy(*a, **k):  # planning reads the graph first; it must not start while another writer holds the lock
        reached.set()
        return real_load(*a, **k)

    monkeypatch.setattr(D, "_load", spy)
    store.write_lock.acquire()
    try:
        out = {}
        t = threading.Thread(target=lambda: out.update(r=D.dream(store, now_ms=NOW)))
        t.start()
        assert not reached.wait(0.5)
    finally:
        store.write_lock.release()
    t.join(60)
    assert reached.is_set() and out["r"]["merged"] == 1
