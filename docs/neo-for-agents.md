# Using Neo-Cortex from the command line (for coding agents)

Neo-Cortex is this project's own memory. Any agent that can run shell commands can use it; no MCP setup is needed.

## Setup (once per machine)

```bash
cd ~/neo-cortex
NEO_TENANT=neo-cortex nohup uv run --no-sync neo serve --port 8765 --warm > /tmp/neo.log 2>&1 &
export NEO_DAEMON_URL=http://127.0.0.1:8765 NEO_TENANT=neo-cortex
uv run --no-sync neo status        # must show counts, not an error
```

The daemon owns the database (one process at a time). Never start a second `neo serve` on the same home, and never run an evaluation while the daemon is up on a small GPU; ask the orchestrator first.

## Before you start work

```bash
neo brief                          # recent decisions, open handoffs, lessons
neo recall "what you are about to change" -k 5
neo ask "why does X work this way?"      # multi-hop evidence pack
neo who "topic"   |   neo impact "component"   |   neo timeline "setting"
```

Read the cited chunk when a hit looks relevant: `neo read <id>`.

## After you finish work (this is the part that matters)

Write what you learned straight into the graph. No extraction model runs, it is fast and exact:

```bash
neo remember "Fusion normalization changed the RRF weights; flag NEO_FUSE_NORM, default off." \
  --kind decision \
  --entity "NEO_FUSE_NORM:config" --entity "fuse.py:file" \
  --rel "fuse.py|CONFIGURED_BY|NEO_FUSE_NORM"
neo relate "NEO_FUSE_NORM" REPLACED_BY "NEO_FUSE_BOOST" --supersede     # correct an edge
neo relate "old-service" DEPENDS_ON "db" --end                          # retire an edge, keep history
neo handoff "what is half done and who should pick it up"
```

Rules:
- One fact per `remember`. Say what, why and the evidence (a file, a number).
- Use `--kind decision` for choices, `procedural` for how-tos, `semantic` for facts, `preference` for user wishes.
- Name entities exactly as they appear in the code or docs; named entities match exactly, they are never fuzzily merged.
- Never write secrets, the user's email, or the contents of `data/synthetic/WORLD.md` (the eval answer key) into memory.
- If `neo recall` returns something that is wrong, fix it with `relate --supersede` or `remember --supersedes <id>`; do not add a contradicting memory.

## Output limits

Every command takes `--max-chars` (default 4000). Keep it small; read full text only with `neo read`.
