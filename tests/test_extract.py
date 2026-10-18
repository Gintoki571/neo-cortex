"""Entity and relation quality in extract.py: generic words, type sanity, relation type constraints, new patterns."""
from neo_cortex import extract as X
from neo_cortex.resolve import PIN_REGEX
from neo_cortex.util import normalize_key


def _rels(spec, wins, gl=(), title="", kind=""):
    """Relations from the pattern rules alone (GLiNER output is an explicit argument): spec = [(name, type)]."""
    ents = {normalize_key(n): {"name": n, "type": t, "conf": 0.9} for n, t in spec}
    return {(r["head"], r["type"], r["tail"]) for r in X._relations(ents, wins, list(gl), title, kind=kind)}


def test_is_generic_single_words_only():
    for w in ["Entity", "graph", "MODULE", "Teams", "classes", "file", "Node", "agents"]:
        assert X.is_generic(w), w
    for w in ["Data", "Platform", "Payments", "Graph database", "auth-service", "Noor Haddad", ""]:
        assert not X.is_generic(w), w


def test_generic_words_are_junk_for_every_type():
    assert X._junk("Entity", "other") and X._junk("MODULE", "component") and X._junk("Team", "team")
    assert X._junk("graph", "tool") and X._junk("file", "file")
    assert not X._junk("Payments", "team") and not X._junk("Data", "team")
    assert not X._junk("auth-service", "service") and not X._junk("Graph database", "tool")


def test_sane_type_files_persons_customers():
    st = X._sane_type
    assert st("config/ci.yaml", "component") == "file" and st("gliner2.5-readme.txt", "tool") == "file"
    assert st("cfgctl.py", "tool") == "file" and st("src/app", "other") == "file"
    assert st("falkordblite", "customer") == "other" and st("acme-bank", "customer") == "other"
    assert st("gliner25-hf-card", "person") == "other" and st("Read-only Cypher", "person") == "other"
    assert st("Noor Haddad", "person") == "person" and st("Lukas J. Brandt", "person") == "person"
    assert st("O'Brien", "person") == "person" and st("田中", "person") == "person"
    assert st("Acme Bank", "customer") == "customer" and st("session-cache", "service") == "service"


def test_entities_apply_type_sanity_and_generic_filter():
    raw = {"entities": {
        "person": [{"text": "gliner25-hf-card", "confidence": 0.95}, {"text": "Noor Haddad", "confidence": 0.9}],
        "file": [{"text": "gliner2_readme.txt", "confidence": 0.9}, {"text": "config/ci.yaml", "confidence": 0.9}],
        "customer": [{"text": "falkordblite", "confidence": 0.95}],
        "component": [{"text": "Entity", "confidence": 0.95}, {"text": "MODULE", "confidence": 0.95}],
    }}
    ents = X._entities(raw, "Noor Haddad reads gliner2_readme.txt and config/ci.yaml. The Entity and MODULE are listed.")
    got = {k: v["type"] for k, v in ents.items()}
    # a data dump (.txt) is not an entity; a repo path is
    assert got == {"noor haddad": "person", "config ci yaml": "file", "gliner25 hf card": "other"}
    assert "entity" not in ents and "module" not in ents and "falkordblite" not in ents
    assert "gliner25 hf card" in ents and ents["gliner25 hf card"]["type"] == "other"


def test_relations_respect_head_and_tail_types():
    # a service cannot own a team; a team can own a service; a person cannot be a DEPENDS_ON endpoint
    got = _rels([("Payments", "team"), ("auth-service", "service"), ("Noor Haddad", "person")],
                ["Payments owns auth-service.", "auth-service owns Payments.", "Noor Haddad depends on auth-service."])
    assert ("Payments", "OWNS", "auth-service") in got
    assert not any(h == "auth-service" and t == "OWNS" for h, t, _ in got)
    assert not any(t == "DEPENDS_ON" for _, t, _ in got)


def test_rel_ok_covers_every_type():
    for rtype in X.REL_TYPES:
        heads, tails = X.REL_TYPES[rtype]
        assert all(X.rel_ok(rtype, h, t) for h in heads for t in tails)
    assert not X.rel_ok("OWNS", "tool", "service") and X.rel_ok("OWNS", "team", "service")
    assert not X.rel_ok("DEPENDS_ON", "person", "service") and X.rel_ok("DEPENDS_ON", "product", "tool")


def test_new_patterns_replaced_and_stored_in():
    got = _rels([("auth-gateway", "service"), ("session-cache", "service"), ("ledger-cache", "service"),
                 ("ledger-db", "tool")],
                ["auth-gateway replaced session-cache.", "ledger-cache is stored in ledger-db."])
    assert ("session-cache", "REPLACED_BY", "auth-gateway") in got
    assert ("ledger-cache", "DEPENDS_ON", "ledger-db") in got
    # no entity placeholders, or the replacement is passive: nothing new
    assert _rels([("auth-gateway", "service"), ("session-cache", "service")],
                 ["The old one was replaced by the new one.", "session-cache was replaced by auth-gateway."]) == {
        ("session-cache", "REPLACED_BY", "auth-gateway")}


def test_table_header_needs_a_separator_line_and_names_are_typed():
    # a chunk that starts mid-table: its first row is data, not a header, so "Owners" in a cell is not an owner column
    mid = ("| `who(topic)` | Owners and experts for a topic |\n| `cypher(query, limit?)` | Read-only Cypher, the escape hatch |")
    assert X._table_facts(mid) == []
    ok = "| Service | Owner |\n|---|---|\n| auth-service | Noor Haddad |"
    assert X._table_facts(ok) == [("Noor Haddad", "OWNS", "auth-service", "person", "service")]
    # an owner cell that is not a person is typed other, so no OWNS edge can come from it
    bad = "| Service | Owner |\n|---|---|\n| auth-service | Read-only Cypher |"
    assert [r for r in X._table_facts(bad) if r[1] == "OWNS" and r[3] == "person"] == []


def test_known_team_names_skip_generic_words():
    # the graph's team list can hold a generic word from an earlier ingest; it must not come back as a team
    ents = X._entities({"entities": {}}, "The Entity team and the Payments team.", teams=["Entity", "Payments"])
    assert "entity" not in ents and ents["payments"]["type"] == "team"


def test_file_entities_are_repo_paths_not_data_dumps():
    keep = ["eval/results.md", "retrieve/channels.py", "pyproject.toml", "docker-compose.yml", "README.md", "Makefile"]
    drop = ["wemakedevs-falkordb-hackathon.txt", "gh repo json", "okf-commits-all.json", "NEO_HOME/neo.rdb", "xlsx", "md",
            "GoogleCloudPlatform/knowledge-catalog repo", "/tmp/falkordb.db", "LICENSE.txt"]
    assert all(X._repo_file(n) for n in keep) and not any(X._repo_file(n) for n in drop)
    raw = {"entities": {"file": [{"text": n, "confidence": 0.95} for n in keep + drop]}}
    got = {v["name"] for v in X._entities(raw, "").values()}
    assert got == set(keep)


def test_regex_ids_keep_their_type_over_gliner():
    raw = {"entities": {"tool": [{"text": "ADR-006", "confidence": 0.95}]}}
    ents = X._entities(raw, "We follow ADR-006 and IDN-212.")
    assert ents["adr 006"]["type"] == "decision" and ents["adr 006"]["pin"] == PIN_REGEX
    assert ents["idn 212"]["type"] == "ticket"


def test_dotted_config_key_typed_as_file_becomes_config_setting():
    from neo_cortex import extract as X
    raw = {"entities": {"file": [{"text": "session.ttl_seconds", "confidence": 0.85},
                                 {"text": "gh-repo.json", "confidence": 0.9}]}}
    raw["entities"]["file"].append({"text": "algo.SPpaths", "confidence": 0.9})
    got = {v["name"]: v["type"] for v in X._entities(raw, "Set session.ttl_seconds to 300; see gh-repo.json; algo.SPpaths.").values()}
    assert got == {"session.ttl_seconds": "config_setting", "algo.SPpaths": "component"}


def _rels_text(spec, text):
    """Relations from the pattern rules over the windows of `text` (what extract_batch feeds _relations)."""
    return _rels(spec, X._windows(text)[0])


_OWNS_SPEC = [("Alice", "person"), ("auth-service", "service")]


def test_fenced_code_block_yields_no_relation_but_prose_does():
    fenced = "Setup:\n\n```bash\nAlice owns auth-service\n```\n\nDone."
    assert _rels_text(_OWNS_SPEC, fenced) == set()
    assert ("Alice", "OWNS", "auth-service") in _rels_text(_OWNS_SPEC, "Alice owns auth-service.")
    assert _rels_text(_OWNS_SPEC, "~~~\nAlice owns auth-service\n~~~") == set()


def test_unclosed_fence_runs_to_the_end_and_a_closer_only_chunk_is_code():
    # a chunk that starts inside a block: its leading ``` closes the block that the previous chunk opened
    prev, cur = X._prose_texts(["```bash\nneo output", "Alice owns auth-service\n```\n\nBob owns billing."])
    assert "Alice" not in cur and "Bob owns billing." in cur
    assert X._windows(prev)[0] == []


def test_shell_prompt_and_cli_lines_yield_no_relation():
    for line in ["$ neo relate \"Alice\" \"OWNS\" auth-service", "neo impact auth-service", "- `neo ask` Alice owns auth-service",
                 "git log Alice owns auth-service", "uv run neo ingest Alice owns auth-service", "curl x Alice owns auth-service"]:
        assert X._windows(line)[0] == [], line
    assert X._windows("Alice owns auth-service.")[0] != []


def test_indented_code_block_after_blank_line_is_code_but_list_continuation_is_not():
    code = "Intro.\n\n    Alice owns auth-service\n\nAfter."
    assert _rels_text(_OWNS_SPEC, code) == set()
    cont = "- Step one:\n\n    Alice owns auth-service, see the doc.\n"
    assert ("Alice", "OWNS", "auth-service") in _rels_text(_OWNS_SPEC, cont)
    # an indented line that continues a paragraph is prose
    assert ("Alice", "OWNS", "auth-service") in _rels_text(_OWNS_SPEC, "Intro line\n    Alice owns auth-service.")


def test_data_table_with_owner_column_still_yields_owns_outside_code():
    table = "| Service | Owner |\n|---|---|\n| auth-service | Noor Haddad |"
    assert X._table_facts(table) == [("Noor Haddad", "OWNS", "auth-service", "person", "service")]
    assert X._table_facts("```\n" + table + "\n```") == []
    assert X._table_facts("Intro.\n\n" + table) == [("Noor Haddad", "OWNS", "auth-service", "person", "service")]


def test_code_is_blanked_but_line_count_and_windows_of_prose_are_kept():
    text = "Alice owns auth-service.\n```\nBob owns billing.\n```\nCarol owns billing."
    assert X._prose_texts([text])[0].count("\n") == text.count("\n")
    wins = X._windows(text)[0]
    assert wins == ["Alice owns auth-service.", "Carol owns billing."]
