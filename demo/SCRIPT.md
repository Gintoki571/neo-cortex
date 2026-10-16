# Neo-Cortex demo script (3 min 50 s)

One daemon, one FalkorDB graph, three tracks. There is no LLM in Neo-Cortex: the tools return cited evidence and graph paths, Claude Code does the reasoning. Everything below uses the fictional company **Pellucid Pay** (`data/synthetic`, never `WORLD.md`).

All outputs in this file are real, from `demo/run_cli_demo.sh` on a fresh `demo/setup.sh` DB (trimmed with `...`; ids such as `mem_...`/`hand_...` change per run).

## Before recording

```bash
demo/setup.sh            # about 2 min 10 s on a free GPU, creates .neo/demo, daemon on 127.0.0.1:8765, DB on 127.0.0.1:6399 (--public adds data/public/falkordb)
. demo/env.sh; alias neo="$NEO"      # or: uv tool install --editable . (then plain `neo`)
demo/reset.sh            # back to the post-setup state between takes (15 s)
demo/teardown.sh         # stop the daemon, no orphan redis-server
```

Windows: (1) terminal, large font, repo root; (2) Claude Code started from the project dirs below; (3) FalkorDB Browser connected to host `127.0.0.1`, port `6399`, graph `neo_default`.

Claude Code launch (hooks + MCP only for this demo; `demo/setup.sh` generates `demo/claude-settings.json` with the absolute `neo` path):

```bash
CC='claude --strict-mcp-config --mcp-config /home/bindesh/neo-cortex/demo/mcp.json --settings /home/bindesh/neo-cortex/demo/claude-settings.json --allowedTools mcp__neo-cortex'
```

Fallback for any segment: `demo/run_cli_demo.sh --pause` runs the same story with neo CLI calls only (about 6 s of compute, Enter between steps).

---

## 0:00 to 0:15  Cold open (voice only, terminal showing `neo status`)

Say: "This is a company's tickets, ADRs, chats and agent sessions in one FalkorDB graph. Three questions an agent cannot answer from files: who owns it now, what changed, and what do I do about it."

```bash
neo status
```
```
daemon: up at http://127.0.0.1:8765  ingest-session queue: pending 0, done 0, errors 0
7 rows: label | n
Chunk | 136   Entity | 134   Document | 102   Memory | 4   Session | 2   Agent | 1
```

## 0:15 to 1:15  Track 03: Company Brain

**Shot 1, who (0:15 to 0:35).** Point at the first line, and at the path with the source doc and date.

```bash
neo who "session cache"
```
```
# who: "session cache" (entities: session-cache), ranked, with evidence
1. Mateo Alvarez score 3.50
   Mateo Alvarez -[OWNS]-> session-cache (src "Engineering handbook: teams and ownership" [doc-14] 2026-09-03)
...
3. Lukas Brandt score 2.21
   Lukas Brandt -[OWNS]-> session-cache (src "Identity and session design" [doc-02] 2026-06-05) FORMER, ended 2026-08-11
```
Say: "Current owner Mateo, with the document that says so. Lukas owned it until the reorg decision ADR-006 (2026-08-11); `OWNS` is an edge with a validity window, not a sentence in a doc." (The ownership moved on 2026-09-01; the edge closes on the date of the document that announced it.)

**Shot 2, timeline (0:35 to 0:55).** Point at the rename chain, then the policy reversal.

```bash
neo timeline "bankbridge"
neo timeline "config approval"
```
```
2026-07-10 REL bank-connector <-[RENAMED_TO]- bankbridge src "PAY-455: Rename bankbridge to bank-connector" [tkt-11]
2026-07-17 REL bank-connector <-[RENAMED_TO]- bankbridge src "ADR-005: Rename bankbridge to bank-connector" [adr-005]
2026-07-20 chat [chat-08] "#payments: rename day"
...
2026-08-14 [adr-008#0] adr: # ADR-008: Two approvals for production config changes ## Status Accepted, 2026-08-14. ...
2026-10-06 [adr-011#0] adr: # ADR-011: One approver plus automated validation for config ... a partial reversal of the two-approver rule ...
```
Say: "Old docs still say bankbridge; the graph knows it is bank-connector since 2026-07-20. The config rule went from one engineer, to two approvals after an outage, to one approver plus cfglint. Newest decision wins, with its source."

**Shot 3, ask (0:55 to 1:15).** Point at "Facts among them" (decision edges) and the cited ids.

```bash
neo ask "Why was the session idle TTL lowered to 300 seconds, and who decided it?"
```
```
## Facts among them
- Tobias Wren -[DECIDED]-> ADR-007 (2026-08-12, conf 0.90) src "ADR-007: Lower session idle TTL to 300 seconds" [adr-007]
- Ravi Chandrasekar -[APPROVED]-> ADR-007 (2026-08-12, conf 0.90) src "ADR-007: ..." [adr-007]
## Evidence (cite ids)
1. [adr-007#0] adr 2026-08-12 ... Supersedes the TTL value in ADR-003 (the 900 s figure) ... SOC 2 Type II audit, run by Ashgrove Assurance, produced...
6. [tkt-20#0] ticket 2026-08-04 | "SEC-9: SOC 2 finding AF-12 (idle sessions)" ...
```
Say: "Tobias decided, Ravi approved, because of audit finding AF-12 from Ashgrove Assurance. Every claim carries a document id." (Gold Q15: AF-12, 300 s.)

## 1:15 to 2:25  Track 01: Agents that act (Claude Code, `triage-agent`)

Terminal: `cd demo/work/pellucid-ops && NEO_AGENT=triage-agent $CC` (interactive) or `-p` with the same prompt. Paste `demo/prompts/01_triage.txt`. The agent should call `ask`, `cypher` (read the cut snippet), `connect`, `who`, then `handoff` and `remember`. Show the tool calls scrolling; do not wait for every token (cut in editing).

The same calls with the CLI (what the agent sees):

```bash
neo ask "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?"
```
```
## Seeds (linked entities)
- reporting-service (match 1.00)
- Northgate Freight (match 1.00)
## Facts among them
- reporting-service -[DEPENDS_ON]-> ledger-service (2026-06-10, conf 0.92) src "Data platform overview" [doc-04]
- Elif Yildiz -[OWNS]-> ledger-service (2026-09-08, conf 0.92) src "PAY-501: Release ledger-service v3.8" [tkt-22]
- Olivia Hartmann -[OWNS]-> reporting-service (2026-06-10, conf 0.78) src "Data platform overview" [doc-04]
## Evidence (cite ids)
2. [tkt-24#0] ticket 2026-09-09 | "INC-04: Reporting totals inflated" ...
7. [mtg-05#0] meeting 2026-09-11 | "Postmortem: INC-04 duplicate totals" ...
```
```bash
demo/tool.sh connect '{"a":"Olivia Hartmann","b":"Elif Yildiz"}'
```
```
- Olivia Hartmann -[OWNS]-> reporting-service -[DEPENDS_ON]-> ledger-service <-[OWNS]- Elif Yildiz
    src: OWNS "Data platform overview" [doc-04]; DEPENDS_ON "Data platform overview" [doc-04]; OWNS "PAY-501: Release ledger-service v3.8" [tkt-22]
```
Point at: "This is the path behind the answer: the broken report depends on ledger-service, whose owner is Elif (Payments). The agent never guessed."

The cited postmortem is longer than the 240-character snippet, so the agent reads it with read-only Cypher (`substring(c.text,190,190)`): "the ledger-service outbox republished after a broker rebalance on 2026-09-08 ... a different key format ... reverted 2026-09-09" (mtg-05).

Then it **acts** (point at the two write calls, they are the "action based on what the graph shows"):

```
handoff [hand_...] open for payments-agent: it appears in their brief.
created [mem_...] decision about: INC-04, ledger-service, event-pipeline, reporting-service, Elif Yildiz, Payments
```
Close the shot by starting the receiving agent (what its SessionStart hook injects):
```bash
echo '{"cwd":"/x/ledger-service"}' | NEO_AGENT=payments-agent neo hook session-start
```
```
## Open handoffs (finish, then handoff(done=<id>))
- [hand_...] 2026-10-16 from triage-agent to payments-agent: INC-04: Northgate totals doubled. ledger-service v3.8 changed the idempotency key ...
```

## 2:25 to 3:35  Track 02: Memory and coordination (`agent-a` to `agent-b`)

**Shot 1, agent A ends and is auto-ingested (2:25 to 2:50).** Show `demo/transcripts/agent_a.jsonl` for two seconds ("a normal Claude Code transcript"), then run exactly what the SessionEnd hook runs:

```bash
echo '{"session_id":"a1b2c3d4-0000-4aaa-8bbb-5e11a0000001","transcript_path":"'$PWD'/demo/transcripts/agent_a.jsonl","cwd":"/x/reporting-service"}' | NEO_AGENT=agent-a neo hook session-end
neo cypher "MATCH (s:Session {id:'a1b2c3d4-0000-4aaa-8bbb-5e11a0000001'})<-[:DERIVED_FROM]-(m:Memory) RETURN m.kind, m.text ORDER BY m.kind"
```
```
decision   | The agent decided to alert on the duplicate ratio instead of an absolute count, because invoice volume is spiky at month end ...
preference | Don't change the production dedupe thresholds without asking Olivia Hartmann.
procedural | When `pytest -q tests/alerts` failed with "ModuleNotFoundError: No module named 'reporting'", the `reporting` package was not installed in editable mode, so `pip install -e .` is needed ...
semantic   | Olivia Hartmann suggested a 1 percent threshold over a 15 minute window for the alert.
semantic   | The alert threshold of 1 percent has not been confirmed with Olivia Hartmann yet, and the `dup_ratio` rule has not been added to `deploy/alerts.yaml`.
semantic   | The agent added the duplicate-ratio alert for reporting-service in `reporting/alerts/dup_ratio.py`, and 4 tests passed ...
```
Say: "Nobody called remember. The hook extracted preferences, a decision, a lesson and facts, typed, with provenance to the session." (Hook returns in about 60 ms; extraction runs in the background, 2 to 10 s.)

**Shot 2, A leaves a handoff (2:50 to 3:00).** `cd demo/work/reporting-service && NEO_AGENT=agent-a $CC -p "$(cat ../../prompts/02a_agent_a_handoff.txt)"`. CLI equivalent:

```bash
neo handoff "Duplicate-ratio alert for reporting-service is implemented and tested. Get the 1 percent threshold confirmed with Olivia Hartmann and add the dup_ratio rule to deploy/alerts.yaml." --from agent-a --to agent-b --task "Confirm the threshold with Olivia Hartmann" --task "Add dup_ratio to deploy/alerts.yaml"
```

**Shot 3, B starts: the brief (3:00 to 3:15).** `cd demo/work/reporting-service && NEO_AGENT=agent-b $CC` (SessionStart hook injects the brief). Point at the handoff, the preferences and the lesson. CLI equivalent:

```bash
echo '{"cwd":"/x/reporting-service"}' | NEO_AGENT=agent-b neo hook session-start
```
```
## Open handoffs (finish, then handoff(done=<id>))
- [hand_...] 2026-10-16 from agent-a to agent-b: Duplicate-ratio alert for reporting-service is implemented and tested. Get the 1 percent threshold confirmed ...
## Preferences
- [mem_...] preference 2026-10-08 (agent-a, reporting-service, conf 0.80, used 1x) Always run tests with `pytest -q`, never unittest.
## Lessons (procedural)
- [mem_...] procedural 2026-10-14 (agent-a, ...) When `pytest -q tests/alerts` failed with "ModuleNotFoundError: ...
```
("used 1x": the same preference came from last week's session and was reinforced instead of duplicated.)

**Shot 4, corrected fact with `supersedes` (3:15 to 3:30).** Paste `demo/prompts/02b_agent_b_continue.txt` into B. CLI equivalent:

```bash
neo recall "what is the dup_ratio alert threshold" -k 3
neo remember "Olivia Hartmann confirmed that the dup_ratio alert uses a 0.5 percent threshold over a 15 minute window, and the rule is now in deploy/alerts.yaml." --supersedes mem_<the "not confirmed" id> --agent agent-b --project reporting-service
neo recall "what is the dup_ratio alert threshold" -k 3
```
```
1. [mem_...] semantic 2026-10-14 | memory agent-a/reporting-service session a1b2... | The alert threshold of 1 percent has not been confirmed with Olivia Hartmann yet ...      <- before
...
created [mem_...] semantic about: Olivia Hartmann, deploy/alerts.yaml
superseded mem_...: The alert threshold of 1 percent has not been confirmed with Olivia Hartmann yet, ...
conflicts: similar active memories that may be stale; call remember again with supersedes=<id> to replace one:
- [mem_...] sim 0.84 Olivia Hartmann suggested a 1 percent threshold over a 15 minute window for the alert.
1. [mem_...] semantic 2026-10-16 | memory agent-b/reporting-service | Olivia Hartmann confirmed that the dup_ratio alert uses a 0.5 percent threshold ...        <- after
```
Point at: "superseded", then the "conflicts" list (the tool tells the agent which other memory may be stale), then the new fact ranking first.

**Shot 5, dream (3:30 to 3:35).**
```bash
neo dream --dry-run
neo dream
neo cypher "MATCH (a:Memory)-[c:CONFLICTS_WITH]->(b:Memory) RETURN a.text, b.text"
```
```
# dream (dry run, nothing written): merged 0, promoted 0, decayed 0, conflicts 1
# dream (dream_...): merged 0, promoted 0, decayed 0, conflicts 1
1 rows: Olivia Hartmann suggested a 1 percent threshold over a 15 minute window for the alert. | Olivia Hartmann confirmed that the dup_ratio alert uses a 0.5 percent threshold ...
```
Say: "Dream previews, then writes. It merges near-duplicates, promotes episodes seen in three sessions, decays unused memories, and flags contradictions an agent missed. On this small graph it found one contradiction." (Merge and promote stay at 0 here: see "Known gaps".)

## 3:35 to 3:50  FalkorDB Browser and the eval table

Browser (host `127.0.0.1`, port `6399`, graph `neo_default`). Paste, one at a time:

```cypher
// the path behind the INC-04 answer
MATCH p=(a:Entity {key:'olivia hartmann'})-[:REL*1..3]-(b:Entity {key:'elif yildiz'}) RETURN p

// ownership over time (current and former owners of the session cache)
MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p, r, s

// memory provenance: memory -> session -> agent
MATCH p=(m:Memory)-[:DERIVED_FROM]->(s:Session)-[:BY]->(a:Agent) RETURN p

// supersession, handoffs, flagged conflicts
MATCH p=(n:Memory)-[:SUPERSEDES]->(o:Memory) RETURN p
MATCH p=(h:Handoff)-[:FROM|TO]->(a:Agent) RETURN p
MATCH p=(:Memory)-[:CONFLICTS_WITH]-(:Memory) RETURN p
```
Say: "The graph is the only store. Ownership, supersession and handoffs are edges, so these answers are graph queries."

Eval table (`eval/results.md`, 80 gold questions, recall@10):

```
| config            | overall | single | multi | temporal | ownership | procedural |
| vector            | 0.73 | 1.00 | 0.61 | 0.62 | 0.71 | 0.93 |
| bm25              | 0.71 | 0.92 | 0.65 | 0.53 | 0.79 | 0.81 |
| vector+bm25       | 0.75 | 1.00 | 0.65 | 0.66 | 0.76 | 0.85 |
| vector+bm25+graph | 0.75 | 0.92 | 0.69 | 0.66 | 0.74 | 0.89 |
| auto (product)    | 0.74 | 0.92 | 0.69 | 0.62 | 0.74 | 0.89 |
```
Say only what the table shows: the graph channel helps the multi-hop column (0.65 to 0.69); the single-fact column is a control.

---

## Verified Q&A (real runs against the demo DB)

| Question | Answer in the output | Gold |
|---|---|---|
| `who "session cache"` | Mateo Alvarez current, Lukas Brandt FORMER | Q29, Q28 |
| `timeline "bankbridge"` | renamed to bank-connector, rename day 2026-07-20 | Q26 |
| `timeline "config approval"` | ADR-008 two approvals (2026-08-14), ADR-011 one approver plus cfglint (2026-10-06) | Q25 |
| `ask` TTL 300 | Tobias Wren decided, Ravi approved, AF-12 Ashgrove Assurance | Q15 |
| `ask` INC-04 + `connect` | reporting-service depends on ledger-service, owner Elif Yildiz; Olivia Hartmann owns reporting-service | Q13, Q44, Q57 |

## Known gaps to avoid on camera

- Snippets are cut at 240 characters and cypher cells at 200, so the cause of an incident sits one `cypher substring()` away from the `ask` pack (the prompt tells the agent how).
- Only 40 `REL` edges exist for 102 documents (3 of 20 `DEPENDS_ON`, 0 `OWNS` for auth-service). Use the INC-04 chain (reporting-service, ledger-service); it is fully connected. `connect payment-gateway "Chen Wei"` (INC-03) finds no path.
- `timeline "session cache"` shows a Platform to Lukas to Mateo flip-flop; show `who` for ownership instead.
- `recall "What was the session lifetime setting on 15 July 2026?"` does not return the 900 s answer; do not use it.
- Dream merge and promote need duplicate or recurring memories; `remember` already reinforces near-duplicates, so only conflicts show.
- The `claude` runs were not executed while building this kit; only the equivalent neo calls were.
