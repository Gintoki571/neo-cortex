#!/usr/bin/env bash
# The whole demo story as neo CLI calls: fallback recording if the live Claude Code run is flaky.
# Needs a fresh demo state: demo/setup.sh once, then demo/reset.sh between takes.  Usage: demo/run_cli_demo.sh [--pause]
# --pause waits for Enter between steps (live recording).  Neo-Cortex has no LLM: every answer below is evidence the agent reasons over.
set -uo pipefail
. "$(dirname "$0")/env.sh"
cd "$DEMO_ROOT"
PAUSE=${1:-}
agent_a_session=a1b2c3d4-0000-4aaa-8bbb-5e11a0000001
t0=$SECONDS; seg_t=$SECONDS

curl -fs "$NEO_DAEMON_URL/health" >/dev/null || { echo "daemon is down: run demo/setup.sh" >&2; exit 1; }
[ "$("$NEO" cypher "MATCH (h:Handoff) RETURN count(h)" 2>&1 | sed -n 2p)" = 0 ] || { echo "demo state is not fresh: run demo/reset.sh" >&2; exit 1; }

seg()  { echo; echo "=== $* ==="; seg_t=$SECONDS; }
end()  { echo "--- segment took $((SECONDS - seg_t)) s"; }
say()  { echo; echo "# $*"; [ "$PAUSE" = --pause ] && read -r -p "[enter] " _; return 0; }
run()  { echo "\$ neo $*"; "$NEO" "$@" 2>&1 | grep -av Batches; }
tool() { echo "\$ demo/tool.sh $1 '$2'"; demo/tool.sh "$1" "$2"; }   # connect/explore have no CLI subcommand
mem()  { "$NEO" cypher "MATCH (m:Memory) WHERE m.text CONTAINS '$1' AND m.status = 'active' RETURN m.id" | sed -n 2p; }
hook() { echo "\$ echo '$2' | NEO_AGENT=$3 neo hook $1" >&2; echo "$2" | NEO_AGENT=$3 "$NEO" hook "$1"; }
ctx()  { python3 -c 'import json,sys; print(json.load(sys.stdin)["hookSpecificOutput"]["additionalContext"])'; }

seg "TRACK 03  Company Brain (graph built from docs, tickets, chats, ADRs)"
say "Who should review a change to the session cache? The owner changed in September."
run who "session cache"
say "Names change too: what happened to bankbridge, and how did the config approval rule evolve?"
run timeline "bankbridge"
run timeline "config approval"
say "Why is the session TTL 300 seconds, and who decided it? Decision edges and the cited ADR, ticket and audit finding."
run ask "Why was the session idle TTL lowered to 300 seconds, and who decided it?"
end

seg "TRACK 01  Agents that act: INC-04 triage by triage-agent"
say "Northgate Freight reports doubled totals. ask gives the evidence pack with the graph facts."
run ask "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?"
say "connect: the path from the broken report to the owner of the upstream service."
tool connect '{"a":"Olivia Hartmann","b":"Elif Yildiz"}'
say "The snippets are 240 characters: read the cited postmortem chunk in full with read-only Cypher."
run cypher "MATCH (c:Chunk {id:'mtg-05#0'}) RETURN substring(c.text,0,190) AS a, substring(c.text,190,190) AS b, substring(c.text,380,190) AS c, substring(c.text,570,190) AS d"
say "who: confirm the owner of the root-cause service."
run who "ledger-service"
say "ACT: hand the fix to the owning team's agent and record the decision."
run handoff "INC-04: Northgate totals doubled. ledger-service v3.8 changed the idempotency key from txn_id to txn_id:attempt, so reporting-service could not dedupe. Confirm the txn_id-only key is live (ADR-009) and review the contract test." --from triage-agent --to payments-agent --task "Confirm txn_id-only key is live in ledger-service" --task "Review the consumer contract test"
run remember "INC-04 root cause: the ledger-service v3.8 idempotency key change (txn_id to txn_id:attempt) after the event-pipeline rebalance made reporting-service count events twice. Owner of the fix: Elif Yildiz (Payments)." --kind decision --agent triage-agent --project reporting-service --about "ledger-service" --about "INC-04"
say "payments-agent starts a session: its SessionStart hook injects the brief with the handoff."
hook session-start '{"session_id":"pay00001","cwd":"/home/bindesh/work/ledger-service"}' payments-agent | ctx | head -8
end

seg "TRACK 02  Memory and coordination: agent-a hands over to agent-b"
say "agent-a finishes; its SessionEnd hook queues the transcript, the daemon extracts memories in the background."
hook session-end "{\"session_id\":\"$agent_a_session\",\"transcript_path\":\"$DEMO_ROOT/demo/transcripts/agent_a.jsonl\",\"cwd\":\"/home/bindesh/work/reporting-service\"}" agent-a
for _ in $(seq 1 120); do curl -s "$NEO_DAEMON_URL/health" | grep -q '"done":1,.*"pending":0' && break; sleep 1; done
run cypher "MATCH (s:Session {id:'$agent_a_session'})<-[:DERIVED_FROM]-(m:Memory) RETURN m.kind, m.text ORDER BY m.kind"
say "agent-a leaves a handoff for agent-b."
run handoff "Duplicate-ratio alert for reporting-service is implemented and tested. Get the 1 percent threshold confirmed with Olivia Hartmann and add the dup_ratio rule to deploy/alerts.yaml." --from agent-a --to agent-b --task "Confirm the threshold with Olivia Hartmann" --task "Add dup_ratio to deploy/alerts.yaml"
say "agent-b starts: the brief shows the handoff, preferences, the decision and the lesson from agent-a."
hook session-start '{"session_id":"b0000001","cwd":"/home/bindesh/work/reporting-service"}' agent-b | ctx
say "Olivia confirmed 0.5 percent. agent-b records the corrected fact and supersedes the stale memory."
run recall "what is the dup_ratio alert threshold" -k 3
old=$(mem "has not been confirmed with Olivia")
run remember "Olivia Hartmann confirmed that the dup_ratio alert uses a 0.5 percent threshold over a 15 minute window, and the rule is now in deploy/alerts.yaml." --supersedes "$old" --agent agent-b --project reporting-service
run recall "what is the dup_ratio alert threshold" -k 3
tool handoff "{\"done\":\"$("$NEO" cypher "MATCH (h:Handoff)-[:TO]->(a:Agent {name:'agent-b'}) RETURN h.id" | sed -n 2p)\"}"
say "agent-b fixed one stale memory; consolidation catches the one it missed (the older 1 percent suggestion). Preview, then run."
run dream --dry-run
run dream
run cypher "MATCH (a:Memory)-[c:CONFLICTS_WITH]->(b:Memory) RETURN a.text, b.text"
end

seg "Evaluation (80 gold questions, synthetic corpus)"
sed -n '/^## recall@10/,/^| auto/p' eval/results.md
echo "=== total $((SECONDS - t0)) s ==="
