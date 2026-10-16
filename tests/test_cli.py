import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

from neo_cortex import cli

HERE = Path(__file__).parent
DB_PORT = int(os.environ.get("NEO_TEST_PORT", "6391"))


def test_parse_args():
    ap = cli.parser()
    a = ap.parse_args(["recall", "who owns auth", "-k", "3", "--tenant", "t"])
    assert (a.cmd, a.query, a.k, a.tenant) == ("recall", "who owns auth", 3, "t")
    a = ap.parse_args(["remember", "x y", "--kind", "decision", "--about", "A", "--about", "B", "--supersedes", "mem_1"])
    assert (a.about, a.kind, a.supersedes) == (["A", "B"], "decision", "mem_1")
    a = ap.parse_args(["handoff", "--to", "bob", "--task", "t1", "--task", "t2", "do it"])
    assert (a.to, a.task, a.summary) == ("bob", ["t1", "t2"], "do it")
    assert ap.parse_args(["serve", "--port", "9", "--warm"]).warm
    assert ap.parse_args(["install-claude", "--scope", "project"]).scope == "project"
    assert ap.parse_args(["hook", "session-end"]).event == "session-end"
    with pytest.raises(SystemExit):
        ap.parse_args(["hook", "bogus"])
    for c in ("status", "brief", "ask q", "who t", "timeline t", "ingest p", "ingest-session f", "cypher q"):
        assert ap.parse_args(c.split()).cmd == c.split()[0]


def test_install_claude_prints_and_merges(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert cli.install_claude("user", False) == 0
    out = capsys.readouterr().out
    assert "claude mcp add --transport http --scope user neo-cortex http://127.0.0.1:8765/mcp" in out
    assert not (tmp_path / ".claude").exists()  # nothing written without --yes
    f = tmp_path / ".claude" / "settings.json"
    f.parent.mkdir()
    f.write_text(json.dumps({"model": "x", "hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "other"}]}]}}))
    cli.install_claude("user", True)
    cli.install_claude("user", True)  # idempotent
    cur = json.loads(f.read_text())
    assert cur["model"] == "x" and set(cur["hooks"]) == {"SessionStart", "SessionEnd", "PreCompact"}
    ss = cur["hooks"]["SessionStart"]
    assert len(ss) == 2 and ss[0]["hooks"][0]["command"] == "other" and ss[1]["hooks"][0]["command"].endswith("hook session-start")
    assert len(cur["hooks"]["SessionEnd"]) == 1


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _redis_pids():
    return subprocess.run(["pgrep", "-f", f"redis-server 127.0.0.1:{DB_PORT}"], capture_output=True, text=True).stdout.split()


@pytest.fixture(scope="module")
def daemon(tmp_path_factory):
    home, port = tmp_path_factory.mktemp("neo"), _free_port()
    env = {**os.environ, "NEO_HOME": str(home), "NEO_PORT": str(DB_PORT), "NEO_DEVICE": "cpu",
           "NEO_DAEMON_URL": f"http://127.0.0.1:{port}", "NEO_AGENT": ""}
    p = subprocess.Popen([sys.executable, str(HERE / "_fake_daemon.py"), "--transport", "http", "--port", str(port)], env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for _ in range(150):
        try:
            socket.create_connection(("127.0.0.1", port), 0.2).close()
            break
        except OSError:
            time.sleep(0.3)
    yield env, p
    p.send_signal(signal.SIGTERM)
    try:
        p.wait(30)
    except subprocess.TimeoutExpired:
        p.kill()
        raise
    time.sleep(0.5)
    assert not _redis_pids(), "orphan redis-server after the daemon stopped"


def neo(env, *args, stdin=None):
    t = time.time()
    r = subprocess.run([sys.executable, "-m", "neo_cortex.cli", *args], env=env, input=stdin, capture_output=True, text=True, timeout=60)
    return r, time.time() - t


def test_hooks_against_daemon(daemon, tmp_path):
    env, _ = daemon
    assert _redis_pids(), "positive control: the daemon owns the DB"
    r, _ = neo(env, "remember", "Always mock the clock in session-cache tests.", "--kind", "procedural", "--project", "proj")
    assert r.returncode == 0 and "created" in r.stdout, r.stderr
    r, _ = neo(env, "hook", "session-start", stdin=json.dumps({"session_id": "abcdef123456", "cwd": "/x/proj", "source": "startup"}))
    ctx = json.loads(r.stdout)["hookSpecificOutput"]
    assert r.returncode == 0 and ctx["hookEventName"] == "SessionStart" and "mock the clock" in ctx["additionalContext"]
    r, _ = neo(env, "hook", "session-start", stdin=json.dumps({"cwd": "/x/other"}))  # the brief is scoped to the project
    assert "mock the clock" not in r.stdout

    p = tmp_path / "s9.jsonl"
    p.write_text("\n".join(json.dumps(x) for x in [
        {"type": "user", "sessionId": "s9", "cwd": "/x/proj", "timestamp": "2026-10-15T10:00:00.000Z",
         "message": {"role": "user", "content": "We decided that the nightly export always runs before the billing close."}}]))
    ev = {"session_id": "abcdef123456", "transcript_path": str(p), "cwd": "/x/proj", "hook_event_name": "SessionEnd", "reason": "other"}
    r, dt = neo(env, "hook", "session-end", stdin=json.dumps(ev))
    assert r.returncode == 0 and r.stdout == "" and dt < 1.0, dt
    for _ in range(100):  # the daemon ingests in the background
        r, _ = neo(env, "recall", "nightly export billing close")
        if "nightly export" in r.stdout:
            break
        time.sleep(0.3)
    assert "nightly export" in r.stdout, r.stdout
    q, _ = neo(env, "cypher", "MATCH (s:Session {id:'s9'})-[:BY]->(a:Agent) RETURN s.project, a.name")
    assert "claude-code:abcdef12" in q.stdout and "proj" in q.stdout
    assert "up at" in neo(env, "status")[0].stdout


def test_api_rejects_foreign_requests(daemon):
    import urllib.error
    import urllib.request
    env, _ = daemon
    base = env["NEO_DAEMON_URL"]
    for hdrs in ({"Content-Type": "text/plain"}, {"Content-Type": "application/json", "Host": "evil.example"}):
        with pytest.raises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(urllib.request.Request(base + "/api/brief", b"{}", hdrs))
        assert e.value.code in (403, 415)


def test_hook_without_daemon_is_silent(tmp_path):
    env = {**os.environ, "NEO_DAEMON_URL": f"http://127.0.0.1:{_free_port()}", "NEO_HOME": str(tmp_path)}
    for ev in ("session-start", "session-end", "pre-compact"):
        r, dt = neo(env, "hook", ev, stdin=json.dumps({"cwd": "/x/p", "transcript_path": "/nope.jsonl"}))
        assert (r.returncode, r.stdout, r.stderr) == (0, "", "") and dt < 1.0
    r, _ = neo(env, "hook", "session-start", stdin="not json")
    assert (r.returncode, r.stdout) == (0, "")
    assert neo(env, "status")[0].returncode == 1
    assert not list(tmp_path.iterdir()), "a hook must never open the DB"
