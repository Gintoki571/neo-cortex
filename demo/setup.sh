#!/usr/bin/env bash
# Fresh demo DB + daemon + synthetic corpus + last week's agent-a sessions.  Usage: demo/setup.sh [--public]
# --public also ingests data/public/falkordb (real FalkorDB issues/PRs/docs; about 15 more minutes).
# Alone on the GPU this takes about 2 minutes; the models need ~1.5 GB of GPU memory, otherwise it falls back to cpu.
set -euo pipefail
. "$(dirname "$0")/env.sh"
cd "$DEMO_ROOT"; mkdir -p .neo

"$(dirname "$0")/teardown.sh" >/dev/null 2>&1 || true
if curl -fs "$NEO_DAEMON_URL/health" >/dev/null 2>&1; then
  echo "another daemon already answers on $NEO_DAEMON_URL; stop it first" >&2; exit 1
fi
rm -rf "$NEO_HOME" "$BASELINE"; mkdir -p "$NEO_HOME"

if ! start_daemon "$NEO_DEVICE"; then
  echo "device $NEO_DEVICE failed (GPU out of memory?); falling back to cpu" >&2
  "$(dirname "$0")/teardown.sh" >/dev/null 2>&1 || true
  rm -rf "$NEO_HOME"; mkdir -p "$NEO_HOME"; export NEO_DEVICE=cpu
  start_daemon cpu
fi
echo "daemon up (device $NEO_DEVICE, pid $(cat "$PIDFILE"), db port $NEO_PORT, home $NEO_HOME)"

# The six kind folders only: WORLD.md is the answer key and manifest.jsonl is not a document.
log=$(mktemp)
{
  for k in doc adr ticket chat meeting session; do "$NEO" ingest --wait "data/synthetic/$k"; done
  # one file per call: `neo ingest <dir>` has a 300 s client timeout, the public set takes about 15 min
  [ "${1:-}" = "--public" ] && find data/public/falkordb -name '*.md' | sort | while read -r f; do "$NEO" ingest "$f" >/dev/null; done
  # Last week's sessions of agent-a (the live one, demo/transcripts/agent_a.jsonl, is ingested on camera).
  for t in demo/transcripts/history/*.jsonl; do "$NEO" ingest-session "$t" --agent agent-a --project reporting-service; done
} 2>&1 | grep -av "Batches" | tee "$log"
if grep -qiE "out ?of ?memory" "$log" && [ "$NEO_DEVICE" != cpu ]; then
  echo "GPU ran out of memory during ingest; redoing everything on cpu" >&2; NEO_DEVICE=cpu exec "$0" "$@"
fi
rm -f "$log"
"$NEO" status

# Claude Code side: hooks settings (absolute path, so no `uv tool install` needed) and per-agent project dirs
# (the hooks take the project name from the cwd basename).
mkdir -p demo/work/reporting-service demo/work/ledger-service demo/work/pellucid-ops
"$NEO" install-claude 2>/dev/null | python3 -c 'import json,sys; t=sys.stdin.read(); print(t[:t.index("\n\n#")])' >demo/claude-settings.json

# snapshot for demo/reset.sh (stop the daemon so the RDB is flushed, copy, restart)
"$(dirname "$0")/teardown.sh" >/dev/null; cp -r "$NEO_HOME" "$BASELINE"
start_daemon "$NEO_DEVICE"; echo "baseline saved; ready (device $NEO_DEVICE)"
