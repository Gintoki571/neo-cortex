"""Non-text documents through the real write path: anydoc converts, fake models extract and embed."""
from pathlib import Path

import pytest

from neo_cortex import write

FIX = Path(__file__).parent / "fixtures" / "docs"
SENT = "Noor Haddad owns session-cache."
# converted by anydoc: format -> (has a Markdown table, expected title or None for "any non-empty title")
CONVERTED = {
    "sample.docx": (True, "Session cache ownership"),
    "sample.xlsx": (True, None),
    "sample.pptx": (True, "Session cache ownership"),  # slide title is a level-2 heading
    "sample.pdf": (False, "Session cache ownership"),
    "sample.rtf": (True, None),
    "sample.csv": (True, None),
}
UNSUPPORTED = ["sample.html", "sample.json", "sample.eml"]  # anydoc has no reader for these
FAILS = ["scanned.pdf", "encrypted.pdf"]                   # anydoc raises NeedsOcr / Encrypted


def _text(store) -> str:
    return "\n".join(r[0] for r in store.query("MATCH (c:Chunk) RETURN c.text ORDER BY c.id"))


@pytest.mark.parametrize("name", list(CONVERTED))
def test_converted_format_becomes_one_document(store, fake_models, name):
    table, title = CONVERTED[name]
    r = write.ingest_path(store, FIX / name)
    assert (r["documents"], r["unsupported"], r["errors"]) == (1, 0, 0), r
    [(kind, doc_title, path)] = store.query("MATCH (d:Document) RETURN d.kind, d.title, d.path")
    assert kind == "file" and doc_title and path.endswith(name)
    if title:
        assert doc_title == title
    text = _text(store)
    assert SENT in text
    assert ("| session-cache |" in text) == table
    if table:
        assert "| --- |" in text  # GFM table separator row


def test_reingest_unchanged_docx_is_skipped(store, fake_models):
    write.ingest_path(store, FIX / "sample.docx")
    r = write.ingest_path(store, FIX / "sample.docx")
    assert r["skipped"] == 1 and r["documents"] == 0


@pytest.mark.parametrize("name", UNSUPPORTED)
def test_unsupported_format_is_counted_not_raised(store, fake_models, name):
    r = write.ingest_path(store, FIX / name)
    assert (r["unsupported"], r["errors"], r["documents"]) == (1, 0, 0), r
    assert store.query("MATCH (d:Document) RETURN count(d)")[0][0] == 0


@pytest.mark.parametrize("name", FAILS)
def test_needs_ocr_or_encrypted_is_counted_as_error(store, fake_models, name):
    r = write.ingest_path(store, FIX / name)
    assert (r["errors"], r["unsupported"], r["documents"]) == (1, 0, 0), r
    assert store.query("MATCH (d:Document) RETURN count(d)")[0][0] == 0


def test_directory_batch_survives_every_bad_file(store, fake_models):
    r = write.ingest_path(store, FIX)
    assert r["documents"] == len(CONVERTED)
    assert r["unsupported"] == len(UNSUPPORTED)
    assert r["errors"] == len(FAILS)
    assert store.query("MATCH (d:Document) RETURN count(d)")[0][0] == len(CONVERTED)
