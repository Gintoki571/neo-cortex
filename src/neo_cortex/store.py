"""FalkorDB access: embedded falkordblite (TCP on 127.0.0.1 only) or an external server via NEO_FALKORDB_URL."""
import fcntl  # shortcut: POSIX flock (Linux only); switch to a portable lock if Windows support is ever needed
import os
import threading
import time
from pathlib import Path

from .config import settings
from .schema import ensure_schema

# Per process and per embedded home: the flock'd lock fd, a refcount and the one FalkorDB handle.
# flock is per open file description, so a second open() of the lock file in this process would
# block on itself; nested Stores on one home share the handle instead.
_homes: dict[str, dict] = {}
_homes_guard = threading.Lock()


def _graph_name(tenant: str) -> str:
    return "neo_" + "".join(c if c.isalnum() or c in "_-" else "_" for c in tenant)


def _open_home(home: Path, port: int):
    """Take the exclusive OS lock on `<home>/.lock` (or reuse this process's handle) and return (key, FalkorDB)."""
    home.mkdir(parents=True, exist_ok=True)
    key = str(home.resolve())
    with _homes_guard:
        h = _homes.get(key)
        if h is None:
            fd = os.open(home / ".lock", os.O_RDWR | os.O_CREAT, 0o644)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                os.close(fd)
                raise RuntimeError(
                    f"NEO_HOME {key} is already in use: a daemon already owns it. Send commands through the "
                    "daemon (NEO_DAEMON_URL), or set NEO_HOME to another directory.") from None
            from redislite.falkordb_client import FalkorDB
            try:
                # bind explicitly: redislite otherwise listens on 0.0.0.0 with no password
                db = FalkorDB(str(home / "neo.rdb"), serverconfig={"port": str(port), "bind": "127.0.0.1"})
            except BaseException:
                os.close(fd)
                raise
            h = _homes[key] = {"fd": fd, "refs": 0, "db": db}
        h["refs"] += 1
        return key, h["db"]


def _stop_server(r):
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


class Store:
    def __init__(self):
        s = settings()
        self.default_tenant = s.tenant
        self._embedded = s.falkordb_url is None
        self._home: str | None = None  # key into _homes while this Store holds a reference
        self._ready: set[str] = set()
        self._lock = threading.Lock()
        # process-wide: every check-then-create writer (ingest, remember, dream, relate) holds it
        self.write_lock = threading.RLock()
        if self._embedded:
            self._home, self.db = _open_home(s.home, s.port)
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
        if not self._embedded:
            self.db.connection.close()
            return
        if self._home is None:  # already closed
            return
        key, self._home = self._home, None
        with _homes_guard:
            h = _homes[key]
            h["refs"] -= 1
            if h["refs"] > 0:  # a nested Store on this home is still open: the server stays up
                return
            del _homes[key]
        _stop_server(h["db"].client)
        os.close(h["fd"])  # releases the flock only after the server has saved and stopped

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
