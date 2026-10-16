#!/usr/bin/env bash
# Back to the state right after setup.sh (no handoffs, no new memories): use between takes.  About 15 s.
set -euo pipefail
. "$(dirname "$0")/env.sh"
[ -d "$BASELINE" ] || { echo "no baseline: run demo/setup.sh first" >&2; exit 1; }
"$(dirname "$0")/teardown.sh" >/dev/null
rm -rf "$NEO_HOME"; cp -r "$BASELINE" "$NEO_HOME"
start_daemon "$NEO_DEVICE" || { echo "falling back to cpu" >&2; "$(dirname "$0")/teardown.sh" >/dev/null; start_daemon cpu; }
echo "demo reset"
