# Neo-Cortex video storyboard (3 minutes)

Every command and output below is verified in `demo/SCRIPT.md` (section noted per scene); ids such as `mem_...` change per run. Fictional company: Pellucid Pay (`data/synthetic`). No LLM inside: GLiNER2.5 + EmbeddingGemma extract and embed; the calling agent reasons.

## 0:00-0:20 Problem (SCRIPT.md "0:00 to 0:15 Cold open")

**On screen:** terminal, repo root.

```bash
neo status
```

**Point at:** `Chunk | 136  Entity | 134  Document | 102` — a company's docs, tickets, ADRs, chats and agent sessions already in one FalkorDB graph.

**Voice-over:** "Agents forget everything between sessions, and a company's knowledge is scattered across tickets, ADRs and chats. Neo-Cortex puts all of it in one FalkorDB graph — and answers the questions files alone cannot: who owns it now, what changed, and what do I do about it."

## 0:20-0:40 What it is (SCRIPT.md closing section, FalkorDB Browser)

**On screen:** FalkorDB Browser, host `127.0.0.1`, port `6399`, graph `neo_default`; run the ownership query:

```cypher
MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p, r, s
```

**Point at:** person nodes connected to the session cache by dated `OWNS` edges; mention 15 MCP tools plus the `neo` CLI.

**Voice-over:** "One graph is three things at once: agent memory, a company brain, and multi-hop reasoning, exposed over MCP. There is no LLM inside — GLiNER2.5 extracts and EmbeddingGemma embeds; Claude does the reasoning."

## 0:40-1:00 Blast radius — the measured graph win (SCRIPT.md "1:15 to 2:25", impact part)

```bash
neo impact ledger-service
```

**Point at:** the three dependents (reporting-service and fraud-scoring at hop 1, payment-gateway at hop 2), the four "Owners to tell", the linked INC-04.

**Voice-over:** "If ledger-service dies, three services break and four owners get notified — every edge cited to its source document. Measured: impact answers score 0.80 with the graph versus 0.20 with text search — the one category where the graph clearly wins."

## 1:00-1:30 Who owns it now, and what changed (SCRIPT.md "0:15 to 1:15", Shots 1-2)

```bash
neo who "session cache"
neo timeline "session.ttl_seconds"
```

**Point at (who):** Mateo Alvarez current with source `doc-14`; Lukas Brandt `FORMER, ended 2026-08-11`.
**Point at (timeline):** `session.ttl_seconds` 3600 to 900 on 2026-06-18 (CFG-4380), then to 300 on 2026-08-12 (ADR-007).

**Voice-over:** "Ownership is an edge with a validity window, not a sentence: Mateo owns it now, Lukas until the reorg. And every config change is dated and sourced — the TTL moved twice, and the graph knows when and why."

## 1:30-1:55 Multi-hop incident evidence pack (SCRIPT.md "1:15 to 2:25", ask + connect)

```bash
neo ask "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?"
demo/tool.sh connect '{"a":"Olivia Hartmann","b":"Elif Yildiz"}'
```

**Point at (ask):** the seeds (`reporting-service`, `Northgate Freight`), "Facts among them" (`reporting-service -[DEPENDS_ON]-> ledger-service`, `Elif Yildiz -[OWNS]-> ledger-service`), the cited ticket and postmortem ids.
**Point at (connect):** the printed path Olivia `-[:OWNS]-> reporting-service -[:DEPENDS_ON]-> ledger-service <-[:OWNS]- Elif`.

**Voice-over:** "One question spans a ticket, a meeting note and two ownership edges. The tool returns seeds, the bridging path and cited evidence — the agent never guesses the answer."

## 1:55-2:20 The agent writes the graph directly (SCRIPT.md "1:15 to 2:25", write calls)

```bash
neo relate "Elif Yildiz" "OWNS" "reporting-service" --supersede --source "INC-04 postmortem (tkt-24): dedupe contract moves to Payments after the v3.8 fix" --agent triage-agent
neo handoff "INC-04: Northgate totals doubled. ..." --from triage-agent --to payments-agent --task "Confirm txn_id-only key is live in ledger-service"
```

**Point at:** `created ... Elif Yildiz -[OWNS]-> reporting-service ... by triage-agent`, then both `closed Olivia Hartmann -[OWNS]-> reporting-service` lines, then the open handoff id. Then one `neo remember` call with `--entity Name:type` and `--rel 'head|TYPE|tail'` (output recorded 2026-10-18 on the project's own graph):

```
neo remember "Measured seven flag-gated retrieval ideas ... none beat the default" --kind decision --entity "eval/flags.md:file" --entity "NEO_RESOLVE_JW:config_setting" --rel "NEO_RESOLVE_JW|CAUSED_BY|falkordblite"
created [mem_29ce608cee2b] decision about: eval/flags.md [ent_9b4ce652645e], NEO_RESOLVE_JW [ent_3f14d4a0ec29], ...
edge NEO_RESOLVE_JW -[CAUSED_BY]-> falkordblite: created ... valid from 2026-10-18 by claude-code, src memory [mem_29ce608cee2b]
```
Point at: typed entities and an edge created in one call, about 0.2 s, no GLiNER.

**Voice-over:** "The agent that just did the work writes what it knows straight into the graph: a superseded ownership edge with its source, and a handoff for the next agent. No extractor in the loop — the agent's words are the facts."

## 2:20-2:40 Hooks: memory without discipline (SCRIPT.md "2:25 to 3:35", Shots 1 and 3)

```bash
echo '{"session_id":"a1b2c3d4-0000-4aaa-8bbb-5e11a0000001","transcript_path":"'$PWD'/demo/transcripts/agent_a.jsonl","cwd":"/x/reporting-service"}' | NEO_AGENT=agent-a neo hook session-end
echo '{"cwd":"/x/reporting-service"}' | NEO_AGENT=agent-b neo hook session-start
```

**Point at:** the extracted typed memories (decision, preference, procedural, semantic — from the Cypher check in SCRIPT.md), then agent-b's brief showing the open handoff, the preference and the lesson.

**Voice-over:** "Nobody called remember. The session-end hook extracted typed memories with provenance, and the next agent's session-start brief already contains the handoff, the preference and the lesson."

## 2:40-3:00 Closing: honest numbers, three tracks (SCRIPT.md closing + judges-guide section 6)

**On screen:** `eval/results.md` table next to the Browser.

**Voice-over:** "The honest results: the graph clearly wins blast radius, 0.80 versus 0.20, and finds owners better — 0.94 versus 0.71. Document retrieval ties text search. Value-change answers it actually loses, 0.80 versus 1.00, and we report that. One FalkorDB graph, one system, all three tracks: agents on connected data, agent memory and coordination, and a company brain."

---

## Recording checklist

- Big terminal font, repo root, one terminal plus FalkorDB Browser (`127.0.0.1:6399`, graph `neo_default`).
- Fresh state: run `demo/setup.sh` (about 2 min, daemon on 8765, DB on 6399); `demo/reset.sh` between takes; `demo/teardown.sh` at the end.
- Fallback for any scene: `demo/run_cli_demo.sh --pause` (same story, CLI only, Enter between steps).
- Avoid the known gaps in SCRIPT.md: no `timeline "session cache"`, no `recall "...15 July 2026..."`, use only the INC-04 chain for graph walks.
- Cut agent tool-call scrolling in editing; do not wait for every token.
