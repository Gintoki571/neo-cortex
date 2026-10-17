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


@pytest.fixture(autouse=True)
def isolated_daemon_url(monkeypatch):
    """No CLI test reaches the daemon on the default port (a demo may run there): each starts with an unused port, and the daemon
    fixture or a test's own fake daemon overrides it."""
    monkeypatch.setenv("NEO_DAEMON_URL", f"http://127.0.0.1:{_free_port()}")


def test_no_test_uses_the_default_daemon():
    assert cli.daemon_url() != cli.DEFAULT_URL  # red without the autouse fixture: NEO_DAEMON_URL unset means 8765


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


def test_parse_new_commands():
    ap = cli.parser()
    a = ap.parse_args(["impact", "Auth Service", "--max-hops", "2"])
    assert (a.cmd, a.entity, a.max_hops) == ("impact", "Auth Service", 2)
    a = ap.parse_args(["relate", "Priya Shah", "OWNS", "Checkout", "--source", "d1#0", "--supersede", "--agent", "codex"])
    assert (a.head, a.type, a.tail, a.source, a.supersede, a.agent) == ("Priya Shah", "OWNS", "Checkout", "d1#0", True, "codex")
    with pytest.raises(SystemExit):
        ap.parse_args(["relate", "Priya Shah", "OWNS"])  # tail is required
    a = ap.parse_args(["read", "d1#0", "--max-chars", "900"])
    assert (a.cmd, a.id, a.max_chars) == ("read", "d1#0", 900)
    a = ap.parse_args(["connect", "A", "B", "--max-hops", "5"])
    assert (a.cmd, a.a, a.b, a.max_hops) == ("connect", "A", "B", 5)
    a = ap.parse_args(["explore", "Checkout", "--hops", "2", "--since", "2026-01-01"])
    assert (a.cmd, a.entity, a.hops, a.since) == ("explore", "Checkout", 2, "2026-01-01")
    assert ap.parse_args(["ingest", "data/doc", "--wait"]).wait is True
    assert ap.parse_args(["ingest", "data/doc"]).wait is False  # a directory returns its job id at once
    assert ap.parse_args(["jobs", "job_3"]).id == "job_3" and ap.parse_args(["jobs"]).id is None


def test_install_claude_prints_and_merges(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert cli.install_claude("user", False) == 0
    out = capsys.readouterr().out
    assert f"claude mcp add --transport http --scope user neo-cortex {cli.daemon_url()}/mcp" in out
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


def test_dream_dry_run_via_daemon(daemon):
    env, _ = daemon
    r, _ = neo(env, "dream", "--dry-run")
    assert r.returncode == 0 and "dry run, nothing written" in r.stdout, r.stderr


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


def test_cli_rejects_bad_tenant(capsys, monkeypatch):
    monkeypatch.setattr(cli, "_post", lambda *a, **k: pytest.fail("no daemon call for an invalid tenant"))  # refused before any network
    assert cli.main(["recall", "x", "--tenant", "acme.eu"]) == 2
    assert 'tenant "acme.eu" is invalid' in capsys.readouterr().err


def test_job_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "_post", lambda *a, **k: json.dumps({"queued": "x", "job": "job_9"}))
    monkeypatch.setattr(cli, "_get", lambda *a, **k: [])
    assert cli.ingest(str(tmp_path), None, None, True) == 1
    assert "job not found" in capsys.readouterr().out


def test_status_label_and_empty_graph(monkeypatch, capsys):
    import io
    monkeypatch.setattr(cli.urllib.request, "urlopen", lambda url, timeout=0: io.BytesIO(json.dumps({"ok": True, "pending": 0, "done": 1, "errors": 0}).encode()))
    monkeypatch.setattr(cli, "_post", lambda *a, **k: "0 rows: label | n")
    assert cli.status() == 0
    out = capsys.readouterr().out
    assert "jobs: pending 0, done 1, errors 0" in out and "graph is empty" in out and "ingest-session" not in out


UNSUP = "ingested /x: documents 0, skipped 0, chunks 0, mentions 0, rels 0, errors 0, unsupported 3, new_entities 0"


def test_ingest_report_exits_2_when_nothing_was_stored(capsys):
    assert cli._ingest_report(UNSUP) == 2
    err = capsys.readouterr().err
    assert "3 file(s) unsupported" in err and "nothing ingested: 3 unsupported" in err
    assert cli._ingest_report(UNSUP.replace("documents 0", "documents 2")) == 0  # something stored: exit 0 with a warning
    assert cli._ingest_report(UNSUP.replace("unsupported 3", "unsupported 0").replace("skipped 0", "skipped 4")) == 0  # unchanged, not failed
    assert cli._ingest_report(UNSUP.replace("unsupported 3", "errors 2")) == 2


class _Clock:
    """Stands in for the time module in the poll loop: sleep advances the clock."""
    def __init__(self):
        self.t = 0.0

    def monotonic(self):
        return self.t

    def time(self):
        return self.t

    def sleep(self, s):
        self.t += s


def _job_post(monkeypatch):
    monkeypatch.setattr(cli, "_post", lambda *a, **k: json.dumps({"job": "job_1"}))


def test_wait_survives_transient_poll_timeouts(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "time", _Clock())
    _job_post(monkeypatch)
    n = {"k": 0}

    def get(path, timeout=10):
        n["k"] += 1
        if n["k"] <= 2:
            raise TimeoutError("timed out")
        return [{"id": "job_1", "status": "done", "result": "ingested /x: documents 1, skipped 0, chunks 2, mentions 0, rels 0, errors 0, unsupported 0, new_entities 0"}]
    monkeypatch.setattr(cli, "_get", get)
    assert cli.ingest(str(tmp_path), None, None, True) == 0
    assert n["k"] == 3 and "documents 1" in capsys.readouterr().out


def test_wait_gives_up_only_after_two_minutes_of_silence(tmp_path, monkeypatch, capsys):
    clock = _Clock()
    monkeypatch.setattr(cli, "time", clock)
    _job_post(monkeypatch)
    monkeypatch.setattr(cli, "_get", lambda path, timeout=10: (_ for _ in ()).throw(TimeoutError("timed out")))
    assert cli.ingest(str(tmp_path), None, None, True) == 1
    assert 120 < clock.t < 130 and "no answer from the daemon for 2 min" in capsys.readouterr().err


def test_wait_prints_progress_at_most_every_30_seconds(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "time", _Clock())
    _job_post(monkeypatch)
    n = {"k": 0}

    def get(path, timeout=10):
        n["k"] += 1
        if n["k"] < 70:
            return [{"id": "job_1", "status": "running"}]
        return [{"id": "job_1", "status": "done", "result": "ingested /x: documents 1, skipped 0, chunks 2, mentions 0, rels 0, errors 0, unsupported 0, new_entities 0"}]
    monkeypatch.setattr(cli, "_get", get)
    assert cli.ingest(str(tmp_path), None, None, True) == 0
    assert capsys.readouterr().err.count("job_1 running") == 2  # ~69 s of polling


def test_explicit_daemon_url_never_falls_back_to_the_embedded_store(monkeypatch, capsys):
    monkeypatch.setattr(cli, "_local", lambda *a: pytest.fail("an explicit NEO_DAEMON_URL must not open the embedded store"))
    with pytest.raises(RuntimeError, match="not reachable"):
        cli.call("cypher", {"query": "MATCH (n) RETURN n"})
    assert cli.main(["recall", "x"]) == 1
    assert "not reachable" in capsys.readouterr().err


def test_default_daemon_url_falls_back_to_the_embedded_store(monkeypatch):
    monkeypatch.delenv("NEO_DAEMON_URL", raising=False)
    monkeypatch.setattr(cli, "DEFAULT_URL", f"http://127.0.0.1:{_free_port()}")
    monkeypatch.setattr(cli, "_local", lambda tool, args: f"local {tool}")
    assert cli.call("cypher", {"query": "x"}) == "local cypher"


def test_store_lock_is_a_message_not_a_traceback(monkeypatch, capsys):
    from neo_cortex import store as store_mod
    monkeypatch.delenv("NEO_DAEMON_URL", raising=False)
    monkeypatch.setattr(cli, "DEFAULT_URL", f"http://127.0.0.1:{_free_port()}")

    def locked(*a, **k):
        raise RuntimeError("NEO_HOME /x is already in use by another process")
    monkeypatch.setattr(store_mod, "Store", locked)
    assert cli.main(["cypher", "MATCH (n) RETURN n"]) == 1
    assert "already in use" in capsys.readouterr().err


def test_remember_defaults_project_to_cwd_basename(monkeypatch, tmp_path):
    sent = {}
    monkeypatch.setattr(cli, "_post", lambda path, body, timeout=300: sent.update(body) or "created")
    monkeypatch.chdir(tmp_path)
    assert cli.main(["remember", "use uv run"]) == 0
    assert sent["project"] == tmp_path.name
    assert cli.main(["remember", "use uv run", "--project", "other"]) == 0
    assert sent["project"] == "other"


def test_remember_and_relate_flags_reach_the_tool_arguments(monkeypatch, capsys):
    sent = []
    monkeypatch.setattr(cli, "_post", lambda path, body, timeout=300: sent.append((path, body)) or "ok")
    assert cli.main(["remember", "Ann runs it", "--entity", "Auth: Service:service", "--entity", "Ops:team",
                     "--rel", "Ann|OWNS|Auth: Service"]) == 0
    assert sent[-1][1]["entities"] == [{"name": "Auth: Service", "type": "service"}, {"name": "Ops", "type": "team"}]
    assert sent[-1][1]["relations"] == [["Ann", "OWNS", "Auth: Service"]]
    assert cli.main(["remember", "plain"]) == 0
    assert "entities" not in sent[-1][1] and "relations" not in sent[-1][1]  # None values are not sent
    assert cli.main(["relate", "Ann", "OWNS", "Checkout", "--end"]) == 0
    assert sent[-1] == ("/api/relate", {"head": "Ann", "type": "OWNS", "tail": "Checkout",
                                        "supersede": False, "end": True, "agent": sent[-1][1]["agent"]})
    n = len(sent)
    assert cli.main(["remember", "x", "--entity", "no-colon"]) == 2 and cli.main(["remember", "x", "--rel", "a|b"]) == 2
    assert len(sent) == n and "name:type" in capsys.readouterr().err
