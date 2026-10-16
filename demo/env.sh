# Sourced by every demo script. Override any of these before sourcing.
DEMO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export NEO_HOME="${NEO_HOME:-$DEMO_ROOT/.neo/demo}"
export NEO_PORT="${NEO_PORT:-6399}"            # embedded FalkorDB (point FalkorDB Browser at 127.0.0.1:$NEO_PORT)
export NEO_DEVICE="${NEO_DEVICE:-cuda}"        # setup.sh falls back to cpu on OOM
export NEO_DAEMON_URL="${NEO_DAEMON_URL:-http://127.0.0.1:8765}"
NEO="$DEMO_ROOT/.venv/bin/neo"
BASELINE="$DEMO_ROOT/.neo/demo-baseline"       # DB snapshot taken by setup.sh, restored by reset.sh
PIDFILE="$DEMO_ROOT/.neo/demo-daemon.pid"
LOGFILE="$DEMO_ROOT/.neo/demo-daemon.log"

# start_daemon DEVICE: background daemon, waits until healthy, then probes the models (OOM shows up on first use, not at load).
start_daemon() {
  mkdir -p "$DEMO_ROOT/.neo" "$NEO_HOME"
  NEO_DEVICE="$1" nohup "$NEO" serve --warm >"$LOGFILE" 2>&1 & echo $! >"$PIDFILE"
  for _ in $(seq 1 180); do
    curl -fs "$NEO_DAEMON_URL/health" >/dev/null 2>&1 && break
    kill -0 "$(cat "$PIDFILE")" 2>/dev/null || return 1
    sleep 1
  done
  curl -fs "$NEO_DAEMON_URL/health" >/dev/null 2>&1 || return 1
  ! NEO_DEVICE="$1" "$NEO" ask "warmup" 2>&1 | grep -qiE "out ?of ?memory"
}
