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
