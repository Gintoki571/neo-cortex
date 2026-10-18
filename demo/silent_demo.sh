#!/usr/bin/env bash
# Hands-free demo for a silent screen recording: captions explain every step, commands type themselves and run.
# Usage: demo/silent_demo.sh [--fast]   (--fast shortens every pause, for testing). Needs the demo stack (demo/setup.sh).
set -uo pipefail
cd "$(dirname "$0")/.." && . demo/env.sh
FAST=0; [ "${1:-}" = "--fast" ] && FAST=1
COLS=$(tput cols 2>/dev/null || echo 110); [ "$COLS" -gt 40 ] || COLS=110
B=$'\e[1m'; BLUE=$'\e[94m'; ORANGE=$'\e[93m'; GREEN=$'\e[92m'; DIM=$'\e[2m'; R=$'\e[0m'
neo() { "$NEO" "$@"; }
pause() { if [ "$FAST" = 1 ]; then sleep 0.3; else sleep "$1"; fi; }
curl -fs "$NEO_DAEMON_URL/health" >/dev/null || { echo "demo daemon not running: run demo/setup.sh first" >&2; exit 1; }
trap 'printf "%s\n" "$R"; tput cnorm 2>/dev/null' EXIT

card() {  # card "title" "line" "line" ... : full-screen caption, then a pause proportional to the text
  clear; printf '\n\n  %s%s%s\n' "$B$BLUE" "$1" "$R"; shift
  local n=0; for l in "$@"; do printf '\n  %s\n' "$l"; n=$((n + ${#l})); done
  pause $(( 3 + n / 18 ))
}
caption() { printf '\n%s%s%s\n' "$B$ORANGE" "$1" "$R"; pause "${2:-4}"; }
run() {  # run "command" [seconds to read output] [max lines]
  printf '%s$ %s' "$GREEN" "$R"
  local s=0; while [ "$s" -lt "${#1}" ]; do printf '%s' "${1:$s:1}"; [ "$FAST" = 1 ] || sleep 0.02; s=$((s + 1)); done
  printf '\n'; pause 1
  eval "$1" 2>&1 | cut -c1-"$COLS" | head -n "${3:-30}"
  pause "${2:-6}"
}

card "Neo-Cortex" \
  "One FalkorDB graph that is an AI agent's memory, a company's brain," \
  "and a way to answer questions that need several steps." \
  "No big AI model inside: two small programs run on this computer, so there is no per-question bill." \
  "Entering all three tracks: 01 Agents that act on connected data  02 Agent memory  03 Company brain"

card "1/6  What is stored" \
  "A fictional company (Pellucid Pay): documents, tickets, chats and notes are already in the graph." \
  "Every count below is a real number from the database."
run "neo status" 6 12

card "2/6  A new document becomes cards and strings" \
  "Here is a short handover note. It has four claims: an owner, a dependency," \
  "a 'might move next quarter', and 'Mateo does not own it'."
run "cat demo/docs/handover-note.md" 12 20
caption "A small reading program finds the people, services and teams, and how they are linked." 3
run "neo ingest --wait demo/docs/handover-note.md" 6 6

card "3/6  A verdict for every link" \
  "Each link gets a verdict (fact, maybe, denied, plan) and a probability, like a weather forecast." \
  "A denial is dropped, a maybe is never treated as a current fact (idea from pg-jev)."
run "neo cypher \"MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk) WHERE d.path ENDS WITH 'handover-note.md' MATCH (a:Entity)-[r:REL]->(b:Entity) WHERE r.source_id = c.id RETURN a.name, r.type, b.name, r.modality, r.p_fact ORDER BY r.type\"" 8 8
caption "Only the real owner is listed: Mateo (denied) and the move (a maybe) did not become ownership." 3
run "neo who \"invoice-export-service\"" 8 8

card "4/6  An agent can write straight into the graph" \
  "When an agent already knows a fact it writes it directly: no reading step, exact, a fraction of a second."
run "time neo remember \"Mateo Alvarez now works on billing reconciliation after handing the export service to Priya Nair.\" --kind decision --entity \"Mateo Alvarez:person\" --entity \"billing reconciliation:component\" --rel \"Mateo Alvarez|WORKS_ON|billing reconciliation\"" 7 10

card "5/6  Four searches at once: words, meaning, connections, time" \
  "The tags after each result say which search found it." \
  "The graph (connections) is what plain text search cannot do: measured 0.80 vs 0.20 on 'what breaks' questions."
run "demo/tool.sh recall '{\"query\":\"Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?\"}'" 10 14
caption "If ledger-service stops, what breaks, and which owners should be told?" 3
run "neo impact ledger-service" 12 16
caption "How are two people connected? The graph follows the strings between them." 3
run "demo/tool.sh connect '{\"a\":\"Olivia Hartmann\",\"b\":\"Elif Yildiz\"}'" 8 6
caption "Time is a first-class idea: the owner list shows who owned it before, with an end date." 3
run "neo who \"session cache\" | grep 'OWNS\]-> session-cache'" 9 8

card "6/6  Memory that tidies itself, and a tuning rule that cannot fool itself" \
  "Two notes disagree (retry limit 3 versus 5). 'dream' flags the clash and writes a log (idea from Dream-RSI)."
run "neo remember \"The retry limit for the payment gateway is set to 3 attempts.\" --kind semantic --entity \"payment-gateway:service\"" 3 4
run "neo remember \"The retry limit for the payment gateway is set to 5 attempts.\" --kind semantic --entity \"payment-gateway:service\"" 5 6
run "neo dream" 5 4
caption "Self-tuning (idea from RRSI): new search settings are kept only if they also win on unseen questions." 3
run "python3 -c \"import json; d=json.load(open('eval/tune_clean.json')); print('practice questions:', round(d['odd_default'],3), '->', round(d['odd_score'],3), '| unseen questions change:', d['even_delta'], '| accepted:', d['accepted'])\"" 7 4

card "Neo-Cortex: one graph, three jobs" \
  "Built with Claude Code and other AI coding agents; the work was directed, reviewed and verified by a person." \
  "Seven more ideas were tried and not adopted because none beat the default (eval/flags.md)." \
  "Code, README and an interactive explainer: github.com/Gintoki571/neo-cortex" \
  "Team: bindesh (solo)"
