"""Lazy, thread-safe model singletons. GLiNER extracts/classifies; EmbeddingGemma embeds (float32: sm_75 has no bf16).
Under NEO_DEVICE=auto a CUDA OOM degrades to CPU (`_load`, `_Guarded`); an explicit NEO_DEVICE=cuda raises."""
import inspect
import os
import sys
import threading

import numpy as np
import torch

from .config import settings

_lock = threading.RLock()
_cache: dict = {}
_cpu: set = set()  # keys whose model is on CPU because of a CUDA OOM


def _once(key, build):
    with _lock:
        if key not in _cache:
            _cache[key] = build()
        return _cache[key]


def _auto() -> bool:
    return os.environ.get("NEO_DEVICE", "auto") == "auto"


def _warn(msg: str):
    print(f"neo: warning: {msg}", file=sys.stderr)


def _load(key, build):
    """build(device) on the configured device; under auto an OOM while loading falls back to CPU."""
    def load():
        dev = settings().device
        try:
            return build(dev)
        except torch.OutOfMemoryError:
            if not _auto() or dev == "cpu":
                raise
            torch.cuda.empty_cache()
            _cpu.add(key)
            _warn(f"{key} did not fit on CUDA, loaded it on CPU")
            return build("cpu")
    return _once(key, load)


class _Guarded:
    """Model handle: each method call runs through _guard, so callers keep the model's own API."""

    def __init__(self, key, m):
        self._key, self._m = key, m

    def __getattr__(self, name):
        attr = getattr(self._m, name)
        if not inspect.ismethod(attr):
            return attr
        return lambda *a, **k: _guard(self._key, self._m, lambda: attr(*a, **k))


def _guard(key, m, fn):
    """fn() on model m. Under auto, a CUDA OOM frees the cache and retries once, then moves m to CPU for good."""
    try:
        return fn()
    except torch.OutOfMemoryError:
        if not _auto() or key in _cpu:
            raise
    torch.cuda.empty_cache()
    try:
        return fn()
    except torch.OutOfMemoryError:
        m.to("cpu")
        torch.cuda.empty_cache()
        _cpu.add(key)
        _warn(f"{key} ran out of CUDA memory, moved it to CPU for the rest of the process")
        return fn()


def gliner():
    def build(device):
        from gliner2 import AutoExtractor
        return AutoExtractor.from_pretrained(settings().gliner, map_location=device)
    return _Guarded("gliner", _load("gliner", build))


def _embedder():
    def build(device):
        from sentence_transformers import SentenceTransformer
        # text-only: skip vision/audio encoders (pillow+torchvision still must be installed for the processor import)
        return SentenceTransformer(settings().embed, device=device,
                                   config_kwargs={"vision_config": None, "audio_config": None},
                                   model_kwargs={"dtype": torch.float32})
    return _Guarded("embed", _load("embed", build))


def embed_docs(texts, titles=None) -> np.ndarray:
    titles = titles or [None] * len(texts)
    docs = [f"title: {t or 'none'} | text: {x}" for t, x in zip(titles, texts)]
    with _lock:  # one forward pass at a time on the shared GPU
        e = _embedder().encode(docs, batch_size=32, normalize_embeddings=True)
    return np.asarray(e, dtype=np.float32)


def embed_query(text: str) -> np.ndarray:
    with _lock:
        e = _embedder().encode(text, prompt_name="SearchQuery", normalize_embeddings=True)
    return np.asarray(e, dtype=np.float32)


def _full_embedder():
    def build(device):
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(settings().embed, device=device, model_kwargs={"dtype": torch.float32})
    return _Guarded("embed_full", _load("embed_full", build))


def embed_images(paths) -> np.ndarray:
    from PIL import Image
    imgs = [Image.open(p).convert("RGB") for p in paths]
    with _lock:
        e = _full_embedder().encode(imgs, batch_size=8, normalize_embeddings=True)
    return np.asarray(e, dtype=np.float32)
