import os

import pytest

from neo_cortex import models
from neo_cortex.retrieve import channels as ch
from neo_cortex.retrieve import parse_query, recall

pytestmark = pytest.mark.skipif(os.environ.get("NEO_SLOW") != "1", reason="set NEO_SLOW=1")

TEXTS = {
    "c_ck": ("Checkout failures began right after Tuesday's deploy.", "e_ck"),
    "c_auth": ("Token issuance latency is graphed on the shared dashboard.", "e_auth"),
    "c_plat": ("Dana Okafor is the lead engineer and carries the pager rotation.", "e_plat"),
    "c_pizza": ("Pizza lunch is booked for Friday at noon.", None),
    "c_roadmap": ("The Q3 roadmap prioritises the mobile app redesign.", None),
    "c_hr": ("New hires receive their laptops in the first week.", None),
}


def test_multihop_question_answered_by_graph(store):
    q = "Who should be paged about the checkout failures?"
    pq = parse_query(q)
    assert "checkout" in " ".join(e["name"].lower() for e in pq["entities"])
    assert set(pq["intent"]) == {"fact", "connection", "temporal", "owner", "howto"}
    ents = [("e_ck", "Checkout", "service"), ("e_auth", "Auth Service", "service"), ("e_plat", "Platform Team", "team")]
    for (i, n, t), e in zip(ents, models.embed_docs([n for _, n, _ in ents])):
        store.query("CREATE (:Entity {id:$i, name:$n, key:$k, type:$t, emb:vecf32($e)})",
                    {"i": i, "n": n, "k": ch.key_of(n), "t": t, "e": e.tolist()})
    store.query("MATCH (a:Entity {id:'e_ck'}),(b:Entity {id:'e_auth'}),(c:Entity {id:'e_plat'}) "
                "CREATE (a)-[:REL {type:'DEPENDS_ON', conf:0.9}]->(b), (c)-[:REL {type:'OWNS', conf:0.9}]->(b)")
    embs = models.embed_docs([t for t, _ in TEXTS.values()])
    for (i, (text, e)), emb in zip(TEXTS.items(), embs):
        store.query("CREATE (:Chunk {id:$i, text:$t, kind:'doc', date_ms:1767225600000, emb:vecf32($v)})",
                    {"i": i, "t": text, "v": emb.tolist()})
        if e:
            store.query("MATCH (c:Chunk {id:$i}),(e:Entity {id:$e}) CREATE (c)-[:MENTIONS {conf:1.0}]->(e)", {"i": i, "e": e})
    only_graph = recall(store, q, k=3, channels=["graph"])
    assert [r["id"] for r in only_graph] == ["c_ck", "c_auth", "c_plat"]  # seed, hop 1, hop 2
    assert only_graph[2]["paths"][0].startswith("Checkout -[DEPENDS_ON]-> Auth Service <-[OWNS]- Platform Team")
    full = recall(store, q, k=3)
    assert "c_plat" in [r["id"] for r in full] and "graph" in next(r for r in full if r["id"] == "c_plat")["channels"]
