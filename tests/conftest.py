import pytest

from neo_cortex.store import Store


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("NEO_HOME", str(tmp_path))
    monkeypatch.setenv("NEO_PORT", "6391")
    monkeypatch.setenv("NEO_DEVICE", "cpu")
    with Store() as s:
        yield s
