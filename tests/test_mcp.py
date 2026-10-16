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

TOOLS = {"brief", "recall", "remember", "ask", "explore", "connect", "who", "timeline", "ingest", "handoff", "cypher", "dream"}


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
