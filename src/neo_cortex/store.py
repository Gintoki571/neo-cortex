"""FalkorDB access: embedded falkordblite (TCP on 127.0.0.1 only) or an external server via NEO_FALKORDB_URL."""
import os
import threading
import time

from .config import settings
from .schema import ensure_schema


def _graph_name(tenant: str) -> str:
    return "neo_" + "".join(c if c.isalnum() or c in "_-" else "_" for c in tenant)


class Store:
    def __init__(self):
        s = settings()
        self.default_tenant = s.tenant
        self._embedded = s.falkordb_url is None
        self._ready: set[str] = set()
        self._lock = threading.Lock()
        if self._embedded:
            from redislite.falkordb_client import FalkorDB
            s.home.mkdir(parents=True, exist_ok=True)
            # bind explicitly: redislite otherwise listens on 0.0.0.0 with no password
            self.db = FalkorDB(str(s.home / "neo.rdb"),
                               serverconfig={"port": str(s.port), "bind": "127.0.0.1"})
        else:
            from falkordb import FalkorDB
            self.db = FalkorDB.from_url(s.falkordb_url)

    def graph(self, tenant: str | None = None):
        name = _graph_name(tenant or self.default_tenant)
        g = self.db.select_graph(name)
        if name not in self._ready:
            with self._lock:
                if name not in self._ready:
                    ensure_schema(g)
                    self._ready.add(name)
        return g

    def query(self, cypher: str, params: dict | None = None, tenant: str | None = None):
        return self.graph(tenant).query(cypher, params).result_set

    def close(self):
        if self._embedded:
            r = self.db.client
            pid = r.pid
            try:
                # redislite's own close() skips shutdown while any other client (e.g. FalkorDB Browser) is
                # attached, leaving an orphan redis-server; we own the server, so stop it unconditionally.
                r.shutdown(save=True, now=True, force=True)
            except Exception:
                pass
            for _ in range(100):
                try:
                    os.kill(pid, 0)
                except OSError:
                    break
                time.sleep(0.05)
            else:
                os.kill(pid, 9)
            try:
                r.close()
            except Exception:
                pass
        else:
            self.db.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
