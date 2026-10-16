"""Test launcher: the real daemon with offline fake models (run as `python tests/_fake_daemon.py <args>`)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from conftest import _fake_embed, _fake_extract_batch  # noqa: E402

from neo_cortex import extract, mcp_server, resolve, write  # noqa: E402

write.embed_docs = resolve.embed_docs = _fake_embed
extract.extract_batch = _fake_extract_batch
extract.extract = lambda t: _fake_extract_batch([t])[0]
extract.classify_memory = lambda t: ("semantic", 0.9)
extract.classify_memory_batch = lambda ts: [("semantic", 0.9)] * len(ts)
extract.worth_keeping_batch = lambda ts: [0.9 if re.search(r"always|decided|never", t, re.I) else 0.1 for t in ts]
extract._softmax_labels = lambda text, task, labels: {labels[0]: 0.99, labels[1]: 0.01}
mcp_server.main(sys.argv[1:])
