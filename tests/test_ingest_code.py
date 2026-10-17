"""Ingest of .py files (one chunk per top-level def/class), document titles and frontmatter fields (fake models)."""
import pytest

from neo_cortex import write

MOD = '''"""Tools for the graph.

Second line of the module docstring.
"""
import re

LIMIT = 5  # a top-level constant stays in the header


def new_id(prefix: str) -> str:
    """Make an id. The docstring is prose for extraction."""
    return f"{prefix}_{re.sub('x', 'y', prefix)}"


@staticmethod
def decorated():
    return 1


class Store:
    """A store. Owns the write lock."""

    def close(self):
        pass
'''


def _names(store):
    return sorted(r[0] for r in store.query("MATCH (e:Entity {type:'component'}) RETURN e.name"))


def test_code_chunks_header_and_one_chunk_per_def(tmp_path):
    parts = write._code_chunks(MOD)
    names = [n for _, _, n in parts]
    assert names == [None, "new_id", "decorated", "Store"]  # header first, then each top-level def/class in order
    header, new_id, dec, cls = parts
    assert '"""Tools for the graph.' in header[0] and "import re" in header[0] and "LIMIT = 5" in header[0]
    assert "def new_id" not in header[0]
    assert header[1] == "Tools for the graph.\n\nSecond line of the module docstring."
    assert new_id[1] == "Make an id. The docstring is prose for extraction."
    assert dec[0].startswith("@staticmethod") and "def decorated" in dec[0]  # decorators travel with the def
    assert "def close" in cls[0] and cls[1] == "A store. Owns the write lock."


def test_code_chunks_split_a_long_function_and_handle_empty_source():
    long_body = "\n".join(f"    value_{i} = compute_something_long({i}, 'padding words to make the line count grow')" for i in range(400))
    parts = write._code_chunks(f"def big():\n{long_body}\n")
    assert len(parts) > 1 and parts[0][2] == "big" and all(p[2] is None for p in parts[1:])
    assert all(len(p[0].split()) <= write.CHUNK_MAX or p[0].count("\n") == 0 for p in parts)
    assert write._code_chunks("") == []
    with pytest.raises(SyntaxError):
        write._code_chunks("def broken(:\n")


def test_module_title_is_the_path_from_the_package_top(tmp_path):
    pkg = tmp_path / "src" / "pkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    (pkg / "mod.py").write_text("x = 1\n")
    (tmp_path / "loose.py").write_text("x = 1\n")
    assert write._module_title(pkg / "mod.py") == "pkg/mod.py"
    assert write._module_title(tmp_path / "loose.py") == "loose.py"


def test_ingest_py_file_one_document_with_components(store, fake_models, tmp_path):
    pkg = tmp_path / "src" / "pkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    (pkg / "mod.py").write_text(MOD)
    r = write.ingest_path(store, pkg / "mod.py")
    assert (r["documents"], r["errors"], r["unsupported"]) == (1, 0, 0)
    doc = store.query("MATCH (d:Document) RETURN d.kind, d.title, d.doc_type, d.description, d.tags")
    assert doc == [["code", "pkg/mod.py", None, None, []]]
    assert store.query("MATCH (c:Chunk) RETURN count(c)") == [[4]]
    assert _names(store) == ["Store", "decorated", "new_id"]
    # the component entity is mentioned from its own chunk, the header chunk has none of the defs
    linked = store.query("MATCH (c:Chunk)-[:MENTIONS]->(e:Entity {type:'component'}) RETURN e.name, c.pos ORDER BY c.pos")
    assert linked == [["new_id", 1], ["decorated", 2], ["Store", 3]]


def test_syntax_error_in_py_is_an_error_not_unsupported(store, fake_models, tmp_path):
    (tmp_path / "src").mkdir()  # the store fixture keeps its own files in tmp_path
    (tmp_path / "src" / "bad.py").write_text("def broken(:\n")
    r = write.ingest_path(store, tmp_path / "src")
    assert r["errors"] == 1 and r["unsupported"] == 0 and r["documents"] == 0
    assert store.query("MATCH (d:Document) RETURN count(d)") == [[0]]
