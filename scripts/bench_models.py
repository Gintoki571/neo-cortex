"""Latency of GLiNER (entities/relations/classify) and embed_docs on the configured device."""
import time

import torch

from neo_cortex import models
from neo_cortex.config import settings

PARA = ("Yesterday Priya approved raising SESSION_TTL to 300 in config/ci.yaml after Claude traced the flaky "
        "login test in auth/login_test.py to the Redis session cache expiring too early. The payments team owns "
        "the auth service, and Marcus will review the change on Monday. The lesson learned is to always mock "
        "time in session tests, because real clocks made the CI run fail twice last week on the shared runners.")
ENT = {"person": "a person's name", "config file": "path to a configuration file",
       "software component": "a service, library, cache or module", "config setting": "an UPPER_CASE setting name"}
REL = {"approved": "person approved a change", "owns": "team or person owns a component"}
CLS = {"memory_type": ["something that happened in a session (episode)", "a general fact about the system",
                       "step-by-step procedure", "a user preference", "a decision that was made"]}


def timed(fn, n=10):
    fn()  # warmup
    ts = []
    for _ in range(n):
        t = time.perf_counter(); fn(); ts.append(time.perf_counter() - t)
        if torch.cuda.is_available(): torch.cuda.synchronize()
    return sorted(ts)[len(ts) // 2] * 1000


if __name__ == "__main__":
    print("device:", settings().device, torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")
    t = time.perf_counter(); g = models.gliner(); print(f"gliner load {time.perf_counter()-t:.1f}s")
    print(f"entities  {timed(lambda: g.extract_entities(PARA, ENT)):.0f} ms")
    print(f"relations {timed(lambda: g.extract_relations(PARA, REL)):.0f} ms")
    print(f"classify  {timed(lambda: g.classify_text(PARA, CLS)):.0f} ms")
    t = time.perf_counter(); models.embed_query("warm"); print(f"embed load {time.perf_counter()-t:.1f}s")
    docs = [f"memory {i}: the redis session cache expires after {i} seconds in CI " * 3 for i in range(64)]
    print(f"embed_docs x64 {timed(lambda: models.embed_docs(docs), 5):.0f} ms")
    print(f"embed_query {timed(lambda: models.embed_query('why did the login test fail in CI?')):.0f} ms")
    if torch.cuda.is_available(): print("peak gpu MB", torch.cuda.max_memory_allocated() // 2**20)
