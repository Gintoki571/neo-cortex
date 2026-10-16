import argparse
import json
import sys

from . import __version__


def main(argv=None):
    ap = argparse.ArgumentParser(prog="neo", description="Neo-Cortex: agent memory and company brain on FalkorDB")
    ap.add_argument("--version", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    for name, help_ in (("ingest", "ingest a file or directory"), ("ingest-session", "ingest a Claude Code JSONL transcript"),
                        ("remember", "store one memory")):
        p = sub.add_parser(name, help=help_)
        p.add_argument("arg", metavar={"ingest": "PATH", "ingest-session": "JSONL", "remember": "TEXT"}[name])
        p.add_argument("--tenant")
        if name == "remember":
            p.add_argument("--kind", choices=["episodic", "semantic", "procedural", "preference", "decision"])
            p.add_argument("--about", action="append", help="entity name this memory is about (repeatable)")
            p.add_argument("--supersedes", help="id of the memory this one replaces")
        if name != "ingest":
            p.add_argument("--agent", default="claude-code")
            p.add_argument("--project")
    a = ap.parse_args(sys.argv[1:] if argv is None else argv)
    if a.version:
        print(__version__)
        return 0
    if not a.cmd:
        ap.print_help()
        return 0
    from . import write
    from .store import Store
    with Store() as s:
        if a.cmd == "ingest":
            out = write.ingest_path(s, a.arg, tenant=a.tenant)
        elif a.cmd == "ingest-session":
            out = write.ingest_session(s, a.arg, agent=a.agent, project=a.project, tenant=a.tenant)
        else:
            out = write.remember(s, a.arg, kind=a.kind, about=a.about, supersedes=a.supersedes, agent=a.agent,
                                 project=a.project, tenant=a.tenant)
    print(json.dumps(out, separators=(",", ":")))
    return 0
