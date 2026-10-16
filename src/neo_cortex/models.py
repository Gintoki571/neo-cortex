"""Lazy, thread-safe model singletons. GLiNER extracts/classifies; EmbeddingGemma embeds (float32: sm_75 has no bf16)."""
import threading

import numpy as np
import torch

from .config import settings

_lock = threading.RLock()
_cache: dict = {}


def _once(key, build):
    with _lock:
        if key not in _cache:
            _cache[key] = build()
        return _cache[key]


def gliner():
    def build():
        from gliner2 import AutoExtractor
        return AutoExtractor.from_pretrained(settings().gliner, map_location=settings().device)
    return _once("gliner", build)


def _embedder():
    def build():
        from sentence_transformers import SentenceTransformer
        # text-only: skip vision/audio encoders (pillow+torchvision still must be installed for the processor import)
        return SentenceTransformer(settings().embed, device=settings().device,
                                   config_kwargs={"vision_config": None, "audio_config": None},
                                   model_kwargs={"dtype": torch.float32})
    return _once("embed", build)


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
    def build():
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(settings().embed, device=settings().device, model_kwargs={"dtype": torch.float32})
    return _once("embed_full", build)


def embed_images(paths) -> np.ndarray:
    from PIL import Image
    imgs = [Image.open(p).convert("RGB") for p in paths]
    with _lock:
        e = _full_embedder().encode(imgs, batch_size=8, normalize_embeddings=True)
    return np.asarray(e, dtype=np.float32)
