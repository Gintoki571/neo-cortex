import asyncio
import os
import signal
import socket
import subprocess
import sys
import time

import pytest
from mcp.client import Client
from test_tools import fakes, g  # noqa: F401  (fixtures)

from neo_cortex.mcp_server import make_server

TOOLS = {"brief", "recall", "remember", "ask", "explore", "connect", "who", "timeline", "impact", "relate", "read", "ingest", "handoff", "cypher", "dream"}


def test_inprocess_list_and_call(g):  # noqa: F811
    async def run():
        async with Client(make_server(g)) as c:
            tl = {t.name: t for t in (await c.list_tools()).tools}
            assert set(tl) == TOOLS
            assert tl["connect"].input_schema["required"] == ["a", "b"]
            assert tl["recall"].input_schema["properties"]["k"]["type"] == "integer"
            assert sum(len(t.description or "") for t in tl.values()) < 2500  # descriptions cost context in every session
            r = await c.call_tool("who", {"topic": "Auth Service"})
            assert "Priya Shah -[MEMBER_OF]-> Platform Team -[OWNS]-> Auth Service" in r.content[0].text
            r = await c.call_tool("cypher", {"query": "CREATE (:X)"})
            assert "rejected" in r.content[0].text
    asyncio.run(run())


def test_ingest_dir_background_job(g, tmp_path):  # noqa: F811
    from starlette.testclient import TestClient
    (tmp_path / "note.md").write_text("---\nkind: doc\ntitle: Session note\n---\nAuth Service sessions expire after 300 seconds.\n")
    http = TestClient(make_server(g).streamable_http_app(), base_url="http://127.0.0.1")  # loopback Host passes the API guard
    r = http.post("/api/ingest", json={"path_or_text": str(tmp_path), "background": True})
    job = r.json()["job"]  # returned at once, before the ingest has run
    assert r.status_code == 200 and job.startswith("job_")
    for _ in range(300):
        j = http.get(f"/api/jobs?id={job}").json()[0]
        if j["status"] in ("done", "error"):
            break
        time.sleep(0.1)
    assert j["status"] == "done" and j["result"].startswith("ingested "), j
    assert "documents 1" in j["result"]


def _redis_pids(db_port):
    return subprocess.run(["pgrep", "-f", f"redis-server 127.0.0.1:{db_port}"], capture_output=True, text=True).stdout.split()


@pytest.mark.parametrize("sig", [signal.SIGTERM, signal.SIGINT])
def test_http_subprocess_no_orphan(tmp_path, sig):
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    db_port = int(os.environ.get("NEO_TEST_PORT", "6391")) + 20 + (sig == signal.SIGINT)
    env = {**os.environ, "NEO_HOME": str(tmp_path), "NEO_PORT": str(db_port), "NEO_DEVICE": "cpu"}
    p = subprocess.Popen([sys.executable, "-m", "neo_cortex.mcp_server", "--transport", "http", "--port", str(port)], env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        async def run():
            async with Client(f"http://127.0.0.1:{port}/mcp") as c:
                assert {t.name for t in (await c.list_tools()).tools} == TOOLS
                r = await c.call_tool("cypher", {"query": "MATCH (n) RETURN count(n)"})
                assert r.content[0].text.startswith("1 rows")
        for _ in range(100):  # wait for the daemon (embedded DB start + imports)
            try:
                socket.create_connection(("127.0.0.1", port), 0.2).close()
                break
            except OSError:
                time.sleep(0.3)
        asyncio.run(run())
        assert _redis_pids(db_port), "positive control: the daemon's redis-server should be running"
    finally:
        p.send_signal(sig)
        try:
            p.wait(30)
        except subprocess.TimeoutExpired:
            p.kill()
            raise
    time.sleep(0.5)
    assert not _redis_pids(db_port), "orphan redis-server after shutdown"


def test_api_type_error_inside_tool_is_500(g):  # noqa: F811
    from starlette.testclient import TestClient
    http = TestClient(make_server(g).streamable_http_app(), base_url="http://127.0.0.1")
    r = http.post("/api/handoff", json={"to": "codex", "summary": "x", "tasks": 5})  # the tool itself raises TypeError
    assert r.status_code == 500 and "failed" in r.text
    r = http.post("/api/handoff", json={"to": "codex", "summary": "x", "tsks": ["a"]})  # a wrong argument name is the caller's fault
    assert r.status_code == 400 and "bad arguments" in r.text


def test_remote_host_needs_opt_in(monkeypatch, capsys, tmp_path):
    from neo_cortex import mcp_server, store
    monkeypatch.setenv("NEO_HOME", str(tmp_path))  # never the user's default DB
    monkeypatch.delenv("NEO_ALLOW_REMOTE", raising=False)
    with pytest.raises(SystemExit, match="NEO_ALLOW_REMOTE"):  # refused before the store is opened
        mcp_server.main(["--host", "0.0.0.0"])
    monkeypatch.setenv("NEO_ALLOW_REMOTE", "1")
    monkeypatch.setattr(store, "Store", lambda: (_ for _ in ()).throw(RuntimeError("store reached")))
    with pytest.raises(RuntimeError, match="store reached"):
        mcp_server.main(["--host", "0.0.0.0"])
    assert "no authentication" in capsys.readouterr().err  # the opt-in is announced


def test_api_body_over_1mb_is_413(g):  # noqa: F811
    from starlette.testclient import TestClient
    http = TestClient(make_server(g).streamable_http_app(), base_url="http://127.0.0.1")
    assert http.post("/api/recall", json={"query": "auth"}).status_code == 200
    assert http.post("/api/recall", json={"query": "x" * 1_100_000}).status_code == 413


def test_jobs_evict_only_finished():
    import threading as th
    from neo_cortex.mcp_server import Jobs
    j, block = Jobs(), th.Event()
    ids = [j.submit("x", "t", lambda: block.wait(5))]  # holds the single worker
    ids += [j.submit("x", "t", lambda: "ok") for _ in range(105)]  # queued, unfinished
    assert all(i in j.byid for i in ids)  # an unfinished job is never evicted
    block.set()
    for _ in range(100):
        if j.stats["done"] + j.stats["errors"] == 106:
            break
        time.sleep(0.05)
    j.submit("x", "t", lambda: "ok")
    assert len(j.byid) <= 101 and ids[-1] in j.byid  # finished ones beyond the newest 100 go


def test_worker_survives_base_exception():
    from neo_cortex.mcp_server import Jobs
    j = Jobs()

    def boom():
        raise SystemExit(3)  # a BaseException, not an Exception: must not kill the worker
    bad = j.submit("x", "t", boom)
    good = j.submit("x", "t", lambda: "ok")
    for _ in range(100):
        if j.byid[good]["status"] == "done":
            break
        time.sleep(0.05)
    assert j.byid[bad]["status"] == "error" and j.byid[good]["status"] == "done"
