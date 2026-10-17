"""CUDA OOM fallback in models.py, with fake model classes (no GPU, no model downloads)."""
import sys
import types

import numpy as np
import pytest
import torch

from neo_cortex import models


def oom():
    return torch.OutOfMemoryError("CUDA out of memory")


@pytest.fixture
def gpu(monkeypatch):
    """A pretend CUDA card: settings() resolves auto to cuda, cache clears are counted, the model cache is fresh."""
    monkeypatch.delenv("NEO_DEVICE", raising=False)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    clears = []
    monkeypatch.setattr(torch.cuda, "empty_cache", lambda: clears.append(1))
    monkeypatch.setattr(models, "_cache", {})
    monkeypatch.setattr(models, "_cpu", set())
    return clears


@pytest.fixture
def st(monkeypatch):
    """Fake sentence_transformers: `load_fails` / `encode_fails` are OOMs still to raise on cuda."""
    ctl = types.SimpleNamespace(load_fails=0, encode_fails=0, made=[])

    class FakeST:
        def __init__(self, name, device=None, **kw):
            if device == "cuda" and ctl.load_fails:
                ctl.load_fails -= 1
                raise oom()
            self.device = device
            ctl.made.append(self)

        def to(self, device):
            self.device = device
            return self

        def encode(self, docs, **kw):
            if self.device == "cuda" and ctl.encode_fails:
                ctl.encode_fails -= 1
                raise oom()
            return np.ones((len(docs), 4), dtype=np.float32)

    monkeypatch.setitem(sys.modules, "sentence_transformers", types.SimpleNamespace(SentenceTransformer=FakeST))
    return ctl


@pytest.fixture
def gl(monkeypatch):
    """Fake gliner2: `encode_fails` OOMs on cuda for extract_entities."""
    ctl = types.SimpleNamespace(encode_fails=0)

    class FakeExtractor:
        def __init__(self, device):
            self.device = device

        def to(self, device):
            self.device = device
            return self

        def extract_entities(self, text, labels, **kw):
            if self.device == "cuda" and ctl.encode_fails:
                ctl.encode_fails -= 1
                raise oom()
            return {"entities": {"person": [{"text": "Priya", "confidence": 0.9}]}}

    class AutoExtractor:
        @staticmethod
        def from_pretrained(path, map_location=None, **kw):
            return FakeExtractor(map_location)

    monkeypatch.setitem(sys.modules, "gliner2", types.SimpleNamespace(AutoExtractor=AutoExtractor))
    return ctl


def test_load_oom_under_auto_loads_on_cpu(gpu, st, capsys):
    st.load_fails = 1
    assert models.embed_docs(["a", "b"]).shape == (2, 4)
    assert st.made[-1].device == "cpu"
    assert len(gpu) == 1  # cache freed before the CPU load
    assert capsys.readouterr().err.count("warning") == 1


def test_load_oom_with_explicit_cuda_raises(gpu, st, monkeypatch):
    monkeypatch.setenv("NEO_DEVICE", "cuda")
    st.load_fails = 1
    with pytest.raises(torch.OutOfMemoryError):
        models.embed_docs(["a"])


def test_encode_oom_once_retries_on_cuda(gpu, st, capsys):
    models.embed_docs(["a"])
    st.encode_fails = 1
    models.embed_docs(["b"])
    assert st.made[0].device == "cuda"
    assert len(gpu) == 1
    assert capsys.readouterr().err == ""


def test_encode_oom_twice_moves_model_to_cpu(gpu, st, capsys):
    models.embed_docs(["a"])
    st.encode_fails = 2
    assert models.embed_docs(["a"]).shape == (1, 4)
    assert st.made[0].device == "cpu"
    assert models.embed_docs(["b"]).shape == (1, 4)  # later calls stay on CPU
    assert capsys.readouterr().err.count("warning") == 1


def test_encode_oom_with_explicit_cuda_raises(gpu, st, monkeypatch):
    monkeypatch.setenv("NEO_DEVICE", "cuda")
    models.embed_docs(["a"])
    st.encode_fails = 1
    with pytest.raises(torch.OutOfMemoryError):
        models.embed_docs(["b"])
    assert st.made[0].device == "cuda"


def test_gliner_extract_oom_falls_back_to_cpu(gpu, gl, capsys):
    m = models.gliner()
    gl.encode_fails = 2
    assert m.extract_entities("Priya", {})["entities"]["person"][0]["text"] == "Priya"
    assert models._cache["gliner"].device == "cpu"
    assert capsys.readouterr().err.count("warning") == 1
