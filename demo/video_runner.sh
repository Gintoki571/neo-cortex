#!/usr/bin/env bash
# demo/video_runner.sh <scene 1-9> [--fast] [--notes] [--dry]
# Guided terminal player for recording the Neo-Cortex demo video.
# For one scene: clear screen, print a caption banner, then walk the scene's
# commands (exact commands from demo/VIDEO.md "Show" blocks): print a `$ `
# prompt, wait for ENTER, type the command char by char (~25 ms/char;
# --fast instant), wait for ENTER, run it (real output), wait for ENTER.
# --notes prints each scene's "Point at" line from VIDEO.md in dim colour.
# --dry prints what would run without running or waiting.
# Preflight: refuses (non-dry) if the daemon is not answering at
# $NEO_DAEMON_URL/health; warns if ss -ltn does not show demo ports 8765/6399.
# Never calls demo/teardown.sh or demo/reset.sh. Ctrl-C leaves the terminal clean.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$DEMO_ROOT"
# shellcheck source=demo/env.sh
. "$DEMO_ROOT/demo/env.sh"
export NEO

RESET=$'\e[0m' BOLD=$'\e[1m' DIM=$'\e[2m'
BLUE=$'\e[94m' ORANGE=$'\e[93m' GREEN=$'\e[92m' RED=$'\e[91m' PURPLE=$'\e[95m' WHITE=$'\e[97m'
PROMPT='$ '
TYPE_DELAY=0.025

fast=0; notes=0; dry=0; scene=""
for arg in "$@"; do
  case "$arg" in
    --fast) fast=1 ;; --notes) notes=1 ;; --dry) dry=1 ;;
    [1-9]) scene="$arg" ;;
    *) echo "usage: $0 <scene 1-9> [--fast] [--notes] [--dry]" >&2; exit 2 ;;
  esac
done
[ -n "$scene" ] || { echo "usage: $0 <scene 1-9> [--fast] [--notes] [--dry]" >&2; exit 2; }

if command -v ss >/dev/null 2>&1; then
  ss -ltn 2>/dev/null | grep -qE ':(8765|6399)' || echo "warning: ss -ltn does not show demo ports 8765/6399 listening" >&2
fi
if [ "$dry" = 0 ]; then
  if ! curl -fs "$NEO_DAEMON_URL/health" >/dev/null 2>&1; then
    echo "refusing to run: daemon is not answering at $NEO_DAEMON_URL/health" >&2
    echo "start it with: demo/setup.sh" >&2
    exit 1
  fi
fi

cleanup() { printf '%s' "$RESET"; printf '\e[?25h'; }
trap cleanup INT
trap cleanup EXIT

type_cmd() {
  local cmd="$1" i ch
  if [ "$fast" = 1 ]; then printf '%s' "$cmd"; else
    for ((i = 0; i < ${#cmd}; i++)); do
      ch="${cmd:$i:1}"; printf '%s' "$ch"; sleep "$TYPE_DELAY"
    done
  fi; printf '\n'
}
run_cmd() {
  ( cd "$DEMO_ROOT"; . demo/env.sh; neo() { "$NEO" "$@"; }; eval "$1" )
}

load_scene() {
  SCENE_TITLE="" SCENE_CMDS=() SCENE_POINT_AT=""
  case "$1" in
    1) SCENE_TITLE="The problem, and the board that never forgets"
       SCENE_CMDS+=('neo status')
       SCENE_POINT_AT='the counts; then the picture: people (dots) joined to the session cache by strings labelled OWNS (4 rows: Mateo Alvarez and Lukas Brandt as people, Platform as a team, ownership edges with dates).' ;;
    2) SCENE_TITLE="One graph, three jobs, no bills"
       SCENE_CMDS+=('neo --help') SCENE_POINT_AT='' ;;
    3) SCENE_TITLE="How a document becomes a graph"
       SCENE_CMDS+=('neo ingest --wait demo/docs/handover-note.md')
       SCENE_POINT_AT='six cards are connected to the new document (two of them brand new, the rest already on the board): Priya Nair and Mateo Alvarez (person), invoice-export-service and ledger-service (service), Platform and "payments API" (team).' ;;
    4) SCENE_TITLE="The judge who writes down every verdict"
       SCENE_CMDS+=("neo cypher \"MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk) WHERE d.path ENDS WITH 'handover-note.md' MATCH (a:Entity)-[r:REL]->(b:Entity) WHERE r.source_id = c.id RETURN a.name, r.type, b.name, r.modality, r.p_fact ORDER BY r.type\"")
       SCENE_CMDS+=('neo who "invoice-export-service"')
       SCENE_CMDS+=('neo cypher "MATCH (j:Judgment) RETURN j.result"')
       SCENE_POINT_AT='fact and the probability on each string; the missing Mateo line even though the note mentions him; the verdict record.' ;;
    5) SCENE_TITLE="An agent can write straight into the graph"
       SCENE_CMDS+=('time neo remember "Mateo Alvarez now works on billing reconciliation after handing the export service to Priya Nair." --kind decision --entity "Mateo Alvarez:person" --entity "billing reconciliation:component" --rel "Mateo Alvarez|WORKS_ON|billing reconciliation"')
       SCENE_POINT_AT='the "created" line with typed names and the edge; the two stopwatch numbers.' ;;
    6) SCENE_TITLE="Asking questions, four searches at once"
       SCENE_CMDS+=("demo/tool.sh recall '{\"query\":\"Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?\"}'")
       SCENE_CMDS+=('neo impact ledger-service')
       SCENE_CMDS+=("demo/tool.sh connect '{\"a\":\"Olivia Hartmann\",\"b\":\"Elif Yildiz\"}'")
       SCENE_CMDS+=('neo who "session cache"')
       SCENE_CMDS+=('neo timeline "session.ttl_seconds"')
       SCENE_POINT_AT='the tags after each result, naming which searches found it; the path that walks from one person to another; the former owner.' ;;
    7) SCENE_TITLE="Memory that tidies itself"
       SCENE_CMDS+=('neo remember "The retry limit for the payment gateway is set to 3 attempts." --kind semantic --entity "payment-gateway:service"')
       SCENE_CMDS+=('neo remember "The retry limit for the payment gateway is set to 5 attempts." --kind semantic --entity "payment-gateway:service"')
       SCENE_CMDS+=('neo dream')
       SCENE_CMDS+=('neo cypher "MATCH (d:DreamRun) RETURN d.id, d.merged, d.promoted, d.decayed, d.conflicts"')
       SCENE_POINT_AT='the conflict line when the second note is written; the log record in the graph.' ;;
    8) SCENE_TITLE="Tuning that cannot fool itself"
       SCENE_CMDS+=("python3 -c \"import json; d=json.load(open('eval/tune_clean.json')); print(d['best'], round(d['odd_score'],3), round(d['odd_default'],3), d['even_delta'], d['ci'], d['accepted'])\"")
       SCENE_POINT_AT='0.752 on the practice questions (0.648 for the default settings), the negative change on unseen questions, and False.' ;;
    9) SCENE_TITLE="The honest close" SCENE_CMDS=() SCENE_POINT_AT='' ;;
    *) echo "unknown scene: $1" >&2; exit 2 ;;
  esac
}

print_banner() {
  clear
  local n="$1" line
  line=$(printf '%0.s=' $(seq 1 70))
  printf '%s%s%s\n' "$ORANGE" "$line" "$RESET"
  printf '%sSCENE %s — %s%s\n' "$BOLD$BLUE" "$n" "$SCENE_TITLE" "$RESET"
  printf '%s%s%s\n' "$ORANGE" "$line" "$RESET"
}

load_scene "$scene"
print_banner "$scene"

if [ "${#SCENE_CMDS[@]}" -eq 0 ]; then
  printf '\n%s%s%s\n' "$ORANGE" "No terminal command in this scene — switch to slide S$scene." "$RESET"
  exit 0
fi

printf '\n%s%s%s\n' "$ORANGE" "Run these commands (press ENTER between steps):" "$RESET"

idx=0; total=${#SCENE_CMDS[@]}
for cmd in "${SCENE_CMDS[@]}"; do
  idx=$((idx + 1))
  printf '%s%s%s ' "$WHITE" "$PROMPT" "$RESET"
  if [ "$dry" = 1 ]; then
    printf '%s[dry] %s%s\n' "$DIM" "$cmd" "$RESET"
  else
    read -r _
    type_cmd "$cmd"
    read -r _
    run_cmd "$cmd"
  fi
  if [ "$notes" = 1 ] && [ -n "$SCENE_POINT_AT" ]; then
    printf '%s%s  point at: %s%s\n' "$DIM" "$SCENE_POINT_AT" "$RESET"
  fi
  if [ "$idx" -lt "$total" ] || [ "$dry" = 1 ]; then
    [ "$dry" = 1 ] || read -r _
  fi
done
exit 0
