"""Settings from env, read at call time so tests can monkeypatch."""
import os
from dataclasses import dataclass
from pathlib import Path


def _local_or(name: str, hub_id: str) -> str:
    p = Path(name).resolve()
    return str(p) if p.exists() else hub_id


@dataclass(frozen=True)
class Settings:
    home: Path
    falkordb_url: str | None
    port: int
    tenant: str
    device: str
    gliner: str
    embed: str


def settings() -> Settings:
    e = os.environ.get
    device = e("NEO_DEVICE", "auto")
    if device == "auto":
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
    return Settings(
        home=Path(e("NEO_HOME", "~/.neo-cortex")).expanduser(),
        falkordb_url=e("NEO_FALKORDB_URL") or None,
        port=int(e("NEO_PORT", "6390")),
        tenant=e("NEO_TENANT", "default"),
        device=device,
        gliner=e("NEO_GLINER") or _local_or("gliner2.5-base-v1", "fastino/gliner2.5-base-v1"),
        embed=e("NEO_EMBED") or _local_or("embeddinggemma-2", "google/embeddinggemma-2"),
    )
