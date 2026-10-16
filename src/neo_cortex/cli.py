"""`neo` CLI. The embedded DB has one owner (the daemon), so commands talk to it over loopback HTTP and only open a
local Store when no daemon is listening. Hooks never open the DB and never fail the user's session."""
import argparse
import json
import os
import shlex
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

from . import __version__

DEFAULT_URL = "http://127.0.0.1:8765"
HOOK_EVENTS = {"session-start": "SessionStart", "session-end": "SessionEnd", "pre-compact": "PreCompact"}
HOOK_TIMEOUT = {"session-start": 15, "session-end": 5, "pre-compact": 5}  # SessionEnd's default budget is only 1.5 s


class Down(Exception):
    """No daemon is listening."""


def daemon_url():
    return os.environ.get("NEO_DAEMON_URL", DEFAULT_URL).rstrip("/")


def _post(path, body, timeout=300):
    req = urllib.request.Request(daemon_url() + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode()
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode(errors="replace")) from None
    except urllib.error.URLError as e:
        if isinstance(e.reason, ConnectionRefusedError):
            raise Down from None
        raise


def _local(tool, args):
    from .store import Store
    with Store() as s:
        if tool == "ingest-session":
            from . import write
            return json.dumps(write.ingest_session(s, **args), separators=(",", ":"))
        from . import tools
        return getattr(tools, tool)(s, **args)


def call(tool, args):
    args = {k: v for k, v in args.items() if v is not None}
    try:
        return _post("/api/" + tool, args)
    except Down:
        args.pop("background", None)
        return _local(tool, args)


def _agent(sid=""):
    return os.environ.get("NEO_AGENT") or (f"claude-code:{sid[:8]}" if sid else "claude-code")


def _abs(p):
    p = Path(p).expanduser()
    return str(p.resolve()) if p.exists() else str(p)  # the daemon has another cwd; non-paths stay raw text


def hook(event):
    """Read the Claude Code hook JSON on stdin. Silent no-op on any failure."""
    try:
        d = json.load(sys.stdin)
        project = Path(d.get("cwd") or os.getcwd()).name
        if event == "session-start":
            text = _post("/api/brief", {"project": project, "agent": os.environ.get("NEO_AGENT") or "claude-code",
                                        "max_chars": 3000}, 10)
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}))
        elif d.get("transcript_path"):  # the daemon queues it and a worker thread does the extraction
            _post("/api/ingest-session", {"transcript_path": d["transcript_path"], "agent": _agent(d.get("session_id", "")),
                                          "project": project, "background": True}, 3)
    except Exception:
        pass
    return 0


def _neo_cmd():
    exe = Path(sys.executable).parent / "neo"
    return shlex.quote(str(exe)) if exe.exists() else shutil.which("neo") or f"{shlex.quote(sys.executable)} -m neo_cortex.cli"


def hooks_block(cmd):
    return {"hooks": {HOOK_EVENTS[e]: [{"hooks": [{"type": "command", "command": f"{cmd} hook {e}", "timeout": t}]}]
                      for e, t in HOOK_TIMEOUT.items()}}


def install_claude(scope, yes):
    block = hooks_block(_neo_cmd())
    path = Path.home() / ".claude" / "settings.json" if scope == "user" else Path.cwd() / ".claude" / "settings.json"
    print(json.dumps(block, indent=2))
    print(f"\n# hooks go under \"hooks\" in {path}" + ("" if yes else " (re-run with --yes to merge them)"))
    print(f"claude mcp add --transport http --scope {scope} neo-cortex {daemon_url()}/mcp")
    if not yes:
        return 0
    cur = json.loads(path.read_text()) if path.exists() else {}
    hooks = cur.setdefault("hooks", {})
    for ev, groups in block["hooks"].items():
        mine = lambda g: any(h.get("command", "").split()[-2:-1] == ["hook"] and h["command"].split()[-1] in HOOK_EVENTS  # noqa: E731
                             for h in g.get("hooks", []))
        hooks[ev] = [g for g in hooks.get(ev, []) if not mine(g)] + groups  # idempotent: replace our old entry
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cur, indent=2) + "\n")
    print(f"merged hooks into {path}")
    return 0


def status():
    try:
        with urllib.request.urlopen(daemon_url() + "/health", timeout=3) as r:
            h = json.load(r)
    except Exception:
        print(f"daemon: down at {daemon_url()} (start it with `neo serve`)")
        return 1
    print(f"daemon: up at {daemon_url()}  ingest-session queue: pending {h['pending']}, done {h['done']}, errors {h['errors']}")
    print(_post("/api/cypher", {"query": "MATCH (n) RETURN labels(n)[0] AS label, count(n) AS n ORDER BY n DESC"}, 30))
    return 0


def parser():
    ap = argparse.ArgumentParser(prog="neo", description="Neo-Cortex: agent memory and company brain on FalkorDB")
    ap.add_argument("--version", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    tn = argparse.ArgumentParser(add_help=False)
    tn.add_argument("--tenant")

    def add(name, help_, *positional, parent=tn):
        p = sub.add_parser(name, help=help_, parents=[parent] if parent else [])
        for a in positional:
            p.add_argument(a)
        return p

    p = sub.add_parser("serve", help="start the daemon (MCP at /mcp, API at /api)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--warm", action="store_true", help="load the models at start")
    add("status", "daemon health and graph counts", parent=None)
    p = add("brief", "session-start context")
    p.add_argument("--project")
    p.add_argument("--agent")
    p = add("recall", "hybrid search", "query")
    p.add_argument("-k", type=int, default=8)
    add("ask", "multi-hop evidence pack", "question")
    add("who", "owners/experts for a topic", "topic")
    add("timeline", "dated events about a topic", "topic")
    p = add("remember", "store one memory", "text")
    p.add_argument("--kind", choices=["episodic", "semantic", "procedural", "preference", "decision"])
    p.add_argument("--about", action="append", help="entity name this memory is about (repeatable)")
    p.add_argument("--supersedes", help="id of the memory this one replaces")
    p.add_argument("--agent", default=_agent())
    p.add_argument("--project")
    add("ingest", "ingest a file or directory", "path")
    p = add("ingest-session", "ingest a Claude Code JSONL transcript", "jsonl")
    p.add_argument("--agent", default=_agent())
    p.add_argument("--project")
    p = add("handoff", "leave work for another agent", "summary")
    p.add_argument("--to", required=True)
    p.add_argument("--task", action="append", help="repeatable")
    p.add_argument("--from", dest="from_agent", default=_agent())
    add("cypher", "read-only Cypher", "query")
    p = add("dream", "consolidate memories (merge, promote, decay, conflicts)")
    p.add_argument("--dry-run", action="store_true", help="report what would change, write nothing")
    p = sub.add_parser("hook", help="Claude Code hook entry point (reads the hook JSON on stdin)")
    p.add_argument("event", choices=list(HOOK_EVENTS))
    p = sub.add_parser("install-claude", help="print (or with --yes merge) the Claude Code hooks and the MCP add command")
    p.add_argument("--scope", choices=["user", "project"], default="user")
    p.add_argument("--yes", action="store_true", help="write the hooks into the settings file")
    return ap


def main(argv=None):
    ap = parser()
    a = ap.parse_args(sys.argv[1:] if argv is None else argv)
    if a.version:
        print(__version__)
        return 0
    if not a.cmd:
        ap.print_help()
        return 0
    if a.cmd == "hook":
        return hook(a.event)
    if a.cmd == "install-claude":
        return install_claude(a.scope, a.yes)
    if a.cmd == "status":
        return status()
    if a.cmd == "serve":
        from . import mcp_server
        mcp_server.main(["--transport", "http", "--port", str(a.port)] + ["--warm"] * a.warm)
        return 0
    t = a.tenant
    try:
        if a.cmd == "ingest-session":
            out = call("ingest-session", {"transcript_path": _abs(a.jsonl), "agent": a.agent, "project": a.project, "tenant": t})
        else:
            out = call(a.cmd, {
                "brief": lambda: {"project": a.project, "agent": a.agent},
                "recall": lambda: {"query": a.query, "k": a.k},
                "ask": lambda: {"question": a.question},
                "who": lambda: {"topic": a.topic},
                "timeline": lambda: {"topic": a.topic},
                "remember": lambda: {"text": a.text, "kind": a.kind, "about": a.about, "supersedes": a.supersedes,
                                     "agent": a.agent, "project": a.project},
                "ingest": lambda: {"path_or_text": _abs(a.path)},
                "handoff": lambda: {"to": a.to, "summary": a.summary, "tasks": a.task, "from_agent": a.from_agent},
                "cypher": lambda: {"query": a.query},
                "dream": lambda: {"dry_run": a.dry_run},
            }[a.cmd]() | {"tenant": t})
    except (RuntimeError, OSError) as e:
        print(f"neo {a.cmd}: {e}", file=sys.stderr)
        return 1
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
