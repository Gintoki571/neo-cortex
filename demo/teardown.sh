#!/usr/bin/env bash
# Stop the demo daemon cleanly (SIGTERM closes the embedded DB) and make sure no redis-server is left on the demo DB port.
. "$(dirname "$0")/env.sh"
if [ -f "$PIDFILE" ]; then
  pid=$(cat "$PIDFILE")
  kill -TERM "$pid" 2>/dev/null
  for _ in $(seq 1 40); do kill -0 "$pid" 2>/dev/null || break; sleep 0.5; done
  kill -0 "$pid" 2>/dev/null && { echo "daemon ignored SIGTERM, killing" >&2; kill -KILL "$pid"; }
  rm -f "$PIDFILE"
fi
PAT="^/[^ ]*redis-server 127\.0\.0\.1:$NEO_PORT"  # anchored: must not match a shell whose command line mentions it
# backstop: only a redis-server bound to OUR db port (never touches other agents' servers)
for _ in $(seq 1 10); do pgrep -f "$PAT" >/dev/null || break; sleep 0.5; done  # let a clean shutdown finish first
pkill -f "$PAT" 2>/dev/null && echo "killed orphan redis-server on $NEO_PORT" >&2
echo "demo daemon stopped"; exit 0
