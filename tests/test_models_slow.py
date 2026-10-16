import os

import numpy as np
import pytest

pytestmark = pytest.mark.skipif(os.environ.get("NEO_SLOW") != "1", reason="set NEO_SLOW=1")


def test_gliner_entities():
    from neo_cortex.models import gliner
    r = gliner().extract_entities("Priya approved the SESSION_TTL change in Redis.",
                                  {"person": "a person's name", "software component": "a service, library or cache"})
    assert "Priya" in str(r)


def test_embed_shapes_and_norm():
    from neo_cortex.models import embed_docs, embed_query
    d = embed_docs(["redis session cache", "pizza on friday"], titles=["ci", None])
    assert d.shape == (2, 768) and d.dtype == np.float32
    assert np.allclose(np.linalg.norm(d, axis=1), 1, atol=1e-3)
    q = embed_query("why did the login test fail?")
    assert q.shape == (768,) and abs(np.linalg.norm(q) - 1) < 1e-3
