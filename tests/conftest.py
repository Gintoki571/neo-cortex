import re
import os
import pytest

from neo_cortex.store import Store

# parallel test runs (several agents) pick distinct ports via NEO_TEST_PORT
PORT = os.environ.get("NEO_TEST_PORT", "6391")


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("NEO_HOME", str(tmp_path))
    monkeypatch.setenv("NEO_PORT", PORT)
    monkeypatch.setenv("NEO_DEVICE", "cpu")
    with Store() as s:
        yield s


def _fake_embed(texts, titles=None):
    """Bag-of-words hash embedding: texts sharing words are close, so dedupe/conflict thresholds are testable offline."""
    import re
    import zlib

    import numpy as np
    out = np.zeros((len(texts), 768), dtype=np.float32)
    for i, t in enumerate(texts):
        for w in re.findall(r"[a-z0-9-]+", t.lower()):
            out[i, zlib.crc32(w.encode()) % 768] += 1
        out[i] /= max(np.linalg.norm(out[i]), 1e-9)
    return out


def _fake_extract_batch(texts, titles=None):
    import re
    res = []
    for t in texts:
        ents = [{"name": n, "type": "person", "conf": 0.9} for n in dict.fromkeys(re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", t))]
        ents += [{"name": n, "type": "service", "conf": 0.9} for n in dict.fromkeys(re.findall(r"\b[a-z]+-[a-z]+\b", t))]
        rels = [{"head": ents[0]["name"], "type": "OWNS", "tail": ents[-1]["name"], "conf": 0.8}] if "owns" in t and len(ents) > 1 else []
        res.append({"entities": ents, "relations": rels})
    return res


@pytest.fixture
def fake_models(monkeypatch):
    from neo_cortex import extract, resolve, write
    monkeypatch.setattr(write, "embed_docs", _fake_embed)
    monkeypatch.setattr(resolve, "embed_docs", _fake_embed)
    monkeypatch.setattr(extract, "extract_batch", _fake_extract_batch)
    monkeypatch.setattr(extract, "extract", lambda t: _fake_extract_batch([t])[0])
    monkeypatch.setattr(extract, "classify_memory", lambda t: ("semantic", 0.9))
    monkeypatch.setattr(extract, "classify_memory_batch", lambda ts: [("semantic", 0.9)] * len(ts))
    monkeypatch.setattr(extract, "worth_keeping_batch",
                        lambda ts: [0.9 if re.search(r"always|decided|never", t, re.I) else 0.1 for t in ts])
    monkeypatch.setattr(extract, "_softmax_labels", lambda text, task, labels: {labels[0]: 0.99, labels[1]: 0.01})
