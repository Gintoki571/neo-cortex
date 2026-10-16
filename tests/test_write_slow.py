import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(os.environ.get("NEO_SLOW") != "1", reason="set NEO_SLOW=1")
ROOT = Path(__file__).resolve().parents[1]


def test_extract_real():
    from neo_cortex.extract import extract
    r = extract("Noor Haddad owns auth-service, which depends on config-service. See IDN-212 and ADR-006.")
    ents = {(e["name"], e["type"]) for e in r["entities"]}
    assert ("Noor Haddad", "person") in ents and ("auth-service", "service") in ents
    assert ("IDN-212", "ticket") in ents and ("ADR-006", "decision") in ents
    assert any(x["head"] == "Noor Haddad" and x["type"] == "OWNS" and x["tail"] == "auth-service" for x in r["relations"])


def test_worth_and_kind_real():
    from neo_cortex.extract import classify_memory, worth_keeping
    assert worth_keeping("Never deploy on Fridays because the freeze starts at 15:00.") > 0.6
    assert worth_keeping("ok thanks, can you run it again?") < 0.4
    assert classify_memory("User prefers short answers without emojis.")[0] == "preference"


def test_ingest_real_owner_table(store):
    from neo_cortex.write import ingest_path
    ingest_path(store, ROOT / "data/synthetic/doc/doc-01.md")
    owns = {(r[0], r[1]) for r in store.query("MATCH (a:Entity)-[r:REL {type:'OWNS'}]->(b:Entity) RETURN a.name, b.name")}
    assert ("Arjun Malhotra", "web-dashboard") in owns and ("Viktor Sokolov", "api-gateway") in owns
