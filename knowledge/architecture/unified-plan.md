---
type: Design Proposal
title: Neo-Cortex unified build plan (all three tracks)
description: One local system serving agent memory, a company brain and GraphRAG reasoning on falkordblite, exposed over MCP. Covers the data model, write and read paths, hybrid retrieval with RRF, MCP tools, borrowed self-improvement ideas, evaluation, and an hour-by-hour plan to the deadline.
tags: [architecture, plan, mcp, graphrag, hybrid-retrieval, rrf, gliner2, embeddinggemma, agent-memory, company-brain, draft]
status: draft
generated: { by: claude-opus-5-5/orchestrator, at: 2026-10-16T09:30:00Z }
stale_after: 2026-10-18T18:29:00Z
sources:
  - id: judging
    resource: /hackathon/judging-and-prizes.md
    title: Judging and prizes
  - id: rules
    resource: /hackathon/rules.md
    title: Hackathon rules
  - id: spike
    resource: /architecture/spike-2026-10-16.md
    title: Stack de-risking spike
  - id: stack
    resource: /architecture/project-plan.md
    title: Stack decisions and risks
  - id: pgjev
    resource: /architecture/inspiration-pg-jev.md
    title: pg-jev inspiration
  - id: rrsi
    resource: /architecture/inspiration-rrsi.md
    title: RRSI inspiration
  - id: dream
    resource: /architecture/inspiration-dream-rsi.md
    title: Dream-RSI inspiration
  - id: cls
    resource: /architecture/classification-usecases.md
    title: Fast-classifier use cases
  - id: grag
    resource: /graphrag-sdk/retrieval-strategies.md
    title: GraphRAG SDK retrieval strategies
---

# Status

Superseded by the build report: [/architecture/build-status.md](/architecture/build-status.md) (what was actually built, final eval numbers, open risks).

# Goal

Win all three tracks with one product. Judges ask "whether the graph is doing work the agent could not do without it"[^judging], and rule 3 says the product must stop working without FalkorDB[^rules]. Entering several tracks is allowed, and each track has its own prize[^rules].

| Track | What we show |
|---|---|
| 01 Agents that act on connected data | Multi-hop `ask`/`connect` tools, graph algorithms as MCP tools, an agent that triages an incident from graph evidence and acts (assigns, writes a handoff), with the path shown |
| 02 Agent memory and coordination | Episodic, semantic, procedural and preference memory written by agents or auto-extracted from sessions, shared across agents and sessions, handoffs, a graph per tenant, nightly consolidation ("dream") |
| 03 Company brain | Docs, tickets and chats in one graph, who owns and knows what, decisions traced to sources, temporal supersession ("what changed"), every answer cited |

# Core decision: no LLM inside the system

GLiNER2.5 does extraction, typing, routing and yes/no judgments. EmbeddingGemma does vectors. The calling agent (Claude Code or any MCP client) is the reasoner: tools return compact, cited evidence and paths, and the agent writes the answer. This removes the hosted-LLM blocker in the stack plan[^stack], keeps everything local and free, and fits how agents work.

GraphRAG SDK's default retriever needs an LLM for keyword extraction and relation extraction[^grag]. So it stays out of the core path; it can be an evaluation baseline if a key is available (see open questions).

# Designed for the agent that uses it (requirements from Claude's side)

1. **Small, fixed tool set** with short descriptions (about 10 tools). Every tool description costs context in every session.
2. **Token-budgeted output.** Ranked items with ids, one-line text, source, date and confidence; a `max_tokens` budget; drill down by id. Never dump documents.
3. **Provenance on everything.** Each fact carries its source (session, doc, ticket, agent), time and confidence, so the agent can judge trust and cite.
4. **Why it matched.** Each result lists the channels that found it and, for graph hits, the path (`query entity -[OWNS]-> auth-service <-[MENTIONS]- memory`).
5. **Cheap writes.** `remember(text)` with optional hints; the server types, links, de-duplicates and flags conflicts. No schema ceremony.
6. **Current versus stale.** Superseded facts are hidden by default and shown in `timeline`, with what replaced them.
7. **Automatic, not discipline-based.** Claude Code hooks: SessionStart injects `brief`; SessionEnd/PreCompact sends the transcript to GLiNER auto-extraction. Memory works even if the agent forgets to call `remember`.
8. **Scopes.** Repo/project, user, team, org. Auto-detected from the working directory.
9. **One shared daemon.** Several agents and sessions at once. Models load once.
10. **Escape hatch.** Read-only Cypher with the schema in the description, for questions the tools do not cover.

# Architecture

```
 Claude Code / other MCP clients ──(streamable HTTP, or stdio shim)──┐
 Claude Code hooks (SessionStart, SessionEnd, PreCompact) ──(CLI)────┤
                                                                     ▼
                         neo-cortex daemon (one Python process)
     ┌───────────── write path ─────────────┐   ┌──────────── read path ────────────┐
     │ anydoc → chunk → GLiNER (entities,   │   │ GLiNER query parse (entities,      │
     │ relations, type, worth-keeping) →    │   │ intent → channel weights, time)    │
     │ entity resolution (name + vector +   │   │ 4 channels → RRF → graph paths →   │
     │ cached GLiNER judge) → dedupe /      │   │ token-budgeted cited evidence pack │
     │ supersede → EmbeddingGemma → UNWIND  │   │                                    │
     └──────────────────────────────────────┘   └────────────────────────────────────┘
                  ▼                                              ▲
     falkordblite (127.0.0.1 TCP) – one graph per tenant; or FalkorDB Docker via URL
     + bm25s in-process index (rebuilt lazily from the graph)
```

- **Store**: one helper starts falkordblite bound to 127.0.0.1 or connects to a `FALKORDB_URL` (Docker), so the "Docker / self-hosted" rule path is one env var away[^stack]. Users can view the graph in FalkorDB Browser.
- **Models**: GLiNER2.5 base and EmbeddingGemma 2 text-only (`vision_config: None, audio_config: None`)[^spike]. The vision encoder loads lazily only when an image or screenshot is ingested; audio only for audio. GPU when available.

# Graph data model

Nodes (every node has `id`, `tenant`, `created_at` epoch ms, `source_id`):

- `Memory {text, kind: episodic|semantic|procedural|preference|decision, confidence, valid_from, valid_to, status: active|superseded, uses, last_used, emb}`
- `Document {title, kind: doc|ticket|chat|session|adr, uri, author}` → `Chunk {text, pos, emb}`
- `Entity {name, type, aliases, emb}` (types from GLiNER: person, team, service, component, file, config, ticket, customer, ...)
- `Person`, `Team`, `Agent`, `Session {agent, started_at, project}`, `Project`
- `Handoff {summary, status}`, `TuneRun {weights, score, accepted}`

Edges (fixed whitelist, because Cypher relationship types cannot be parameters):

- `(Chunk|Memory)-[:MENTIONS {conf}]->(Entity)`, `(Document)-[:HAS_CHUNK]->(Chunk)`
- `(Entity)-[:REL {type, conf, valid_from, valid_to, source_id}]->(Entity)`: typed GLiNER relations (owns, depends_on, caused_by, approved, fixed_by, part_of, ...)
- `(Person)-[:OWNS|MEMBER_OF|AUTHORED]->(...)`, `(Memory)-[:DERIVED_FROM]->(Chunk|Session)`, `(Memory)-[:SUPERSEDES]->(Memory)`, `(Agent)-[:WROTE]->(Memory)`, `(Handoff)-[:FROM|TO]->(Agent)`
- Indexes: vector on `Memory.emb`, `Chunk.emb`, `Entity.emb` (768, cosine); full-text on `Entity.name` and aliases; range on `created_at`, `valid_from`.

# Write path

1. `remember(text, kind?, about?, supersedes?)` from an agent, or `ingest(path|text, kind)` for docs, tickets, chats and session transcripts.
2. GLiNER with descriptive labels[^spike]: entities and relations (keep spans and confidence; drop below threshold), memory kind, and "worth remembering?" for auto-extracted session text.
3. Entity resolution: exact or alias match, then vector nearest-neighbour, then a cached GLiNER yes/no judge for borderline pairs. Judgments are cached by content hash and written as edge properties. This is the pg-jev idea, done locally[^pgjev][^cls].
4. Dedupe and conflict: near-duplicate memories reinforce (`uses+1`) instead of adding rows. A same-subject, different-value fact gets a `SUPERSEDES` edge or a conflict flag returned to the agent.
5. Embed with the right prefix (`title: … | text: …`) and write in one `UNWIND` batch (5000 rows in 0.013 s in the spike[^spike]).

# Read path: hybrid retrieval with RRF

1. Parse the query with GLiNER: entities, intent (owner / connection / temporal / how-to / fact), time words ("last week", "before the change").
2. Four channels, each returning a ranked list:
   - **Vector**: EmbeddingGemma `SearchQuery` → `db.idx.vector.queryNodes` over memories and chunks.
   - **BM25**: `bm25s` over the same texts. FalkorDB full-text is not BM25 (term frequency is ignored and scores tie)[^spike], so it is only used for fuzzy entity-name lookup.
   - **Graph**: link the query entities, then score nodes by k-hop expansion, `algo.pageRank` around the seeds, and `algo.SPpaths` between seeds (bridging paths are the multi-hop evidence).
   - **Temporal**: hard filter for explicit windows; a recency or validity rank for "current" questions; superseded facts only for "what changed".
3. Fuse with weighted RRF, `score = Σ w_c / (60 + rank_c)`. The weights come from the GLiNER intent confidence (soft routing; the spike showed one misroute in six[^spike]) and from the tuned defaults.
4. Assemble a token-budgeted evidence pack: items, channel tags, graph paths and citations.

# MCP tools (about 10)

| Tool | Purpose | Track |
|---|---|---|
| `brief(scope?)` | Session-start context: preferences, active decisions, recent episodes, open handoffs, gotchas | 02 |
| `recall(query, k, since?, until?, kinds?)` | Hybrid RRF search with "why it matched" | all |
| `remember(text, kind?, about?, supersedes?)` | Write memory; returns id, links, conflicts | 02 |
| `ask(question)` | Multi-hop evidence pack: seeds, bridging paths, cited chunks | 01, 03 |
| `explore(entity, hops, since?)` | Neighbourhood subgraph, compact | 01 |
| `connect(a, b, max_hops)` | Weighted paths between two entities | 01 |
| `who(topic)` | Owners and experts (ownership edges plus PageRank or betweenness over authorship) | 03 |
| `timeline(entity or topic)` | What changed, what superseded what, decisions in order with sources | 03 |
| `ingest(path or text, kind)` | Docs, tickets, chats, session transcripts | 02, 03 |
| `handoff(to, summary, tasks)` | Leave work for another agent; shown in that agent's `brief` | 02 |
| `cypher(query)` | Read-only escape hatch | 01 |

Transport: MCP SDK 2.x `MCPServer` with `streamable-http` (one shared daemon for many agents), plus a `stdio` entry point for harnesses that need it[^spike]. The same functions back a `neo` CLI used by the hooks.

# Borrowed ideas (from the three research passes)

All three recommend adapting, not porting[^pgjev][^rrsi][^dream].

- **pg-jev → cached judgments.** Write GLiNER yes/no or choice probabilities as node and edge properties, cached by content hash, so Cypher filters by threshold. Used for entity resolution and assertion gating. About 4 to 6 hours, folded into the write path.
- **Dream-RSI → `neo dream` consolidation job.** Merge near-duplicates, promote facts seen in 3 or more sessions to semantic memory with provenance edges, decay unused facts (never delete), and promote hypothesis edges only when seen again. Present it as consolidation. About 9 to 11 hours as scoped by the research agent; ship a smaller version (merge, promote, decay) in about 4 hours.
- **RRSI → self-tuning retrieval with an acceptance rule.** Tune the RRF weights on the gold set; accept a change only if it beats the bootstrap noise band on a held-out split. Each trial is a `:TuneRun` node in the graph. About 7 hours; cut first if late.

# Proof: evaluation the judges can read

- A synthetic company corpus ("public, synthetic, or your own" data only[^rules]): about 80 to 120 docs, tickets, chat threads, ADRs and session logs, with planted multi-hop, ownership and temporal facts. Disclosed as AI-generated.
- A gold set of about 40 questions (single-hop, 2–3-hop, temporal, owner).
- An ablation table in the README: vector, BM25, vector+BM25, +graph, +temporal, +GLiNER routing, tuned. This shows that the graph channel is what answers the multi-hop and owner questions (rule 3). It also feeds the RRSI-style tuner.

# Demo story (3 to 4 minutes)

1. Two Claude Code sessions share one daemon. Session A fixes a bug; the hook auto-extracts memories, and Session A leaves a handoff.
2. Session B starts: `brief` shows the handoff and the lesson learned. Track 02.
3. Company brain: "Who should review a change to the session cache, and why did we set TTL to 300?" `who` and `timeline` answer with a cited path from the ADR, the ticket and the chat. Track 03.
4. Incident: "Checkout errors since yesterday." `ask` finds a multi-hop path (checkout → auth-service → config change → owner), and the agent assigns the ticket and writes a handoff. Track 01.
5. FalkorDB Browser shows the subgraph; the ablation table and `dream` run close the demo.

# Plan to the deadline (2026-10-18 18:29 UTC, about 57 h from 09:30 UTC on 2026-10-16)

| When (UTC) | Work | Exit check |
|---|---|---|
| Oct 16 10–12 | uv project, `Store` (falkordblite or URL), schema and indexes, model loaders (CUDA torch), config | pytest: schema created, models load |
| Oct 16 12–20 | Write path: `remember`, `ingest` (anydoc, chunking, sessions), GLiNER extraction with labels, entity resolution and cached judge, dedupe and supersede | ingest the synthetic corpus; entity counts look right |
| Oct 16 20–24 | Synthetic company corpus and gold set (written in parallel by a subagent) | 40 questions with gold ids |
| Oct 17 08–15 | Read path: 4 channels, RRF, GLiNER routing, `ask`, `connect`, `explore`, `who`, `timeline`; eval harness and ablation | ablation table produced; fused beats every single channel |
| Oct 17 15–20 | MCP server (HTTP and stdio), `neo` CLI, Claude Code hooks, `brief`, `handoff`, read-only `cypher` | Claude Code connects; two sessions share memory |
| Oct 17 20–24 | `dream` (merge, promote, decay); RRSI tuner if on schedule | dream run visibly changes the graph; tuned weights logged |
| Oct 18 06–13 | README (setup, data model, Cypher used, ablation), AI-use disclosure, demo recording, optional live deploy, blog post | fresh-clone setup works |
| Oct 18 13–17 | Buffer, fixes, submit (name all three tracks) | submitted with more than 1 h of margin |

Cut order if late: RRSI tuner, then the hypothesis edges in `dream`, then the live deploy, then the blog. Never cut: the eval table, the MCP server, the hooks, the README items rule 10 requires.

# User decisions (2026-10-16)

- graphrag-sdk is dropped from the core. Retrieval is our own Cypher plus bm25s.
- Demo data uses both: a synthetic company (gold set, ablation) and a public open-source org's issues, PRs and docs (real-data demo). Add about 4 h to the corpus step and cut it before the eval if late.

# Open questions

- Does the hackathon accept falkordblite as "FalkorDB"? Ask organisers; the Docker path stays one env var away.
- GPU speed for GLiNER and EmbeddingGemma on the GTX 1660 Ti: not measured yet.

[^judging]: Judging and prizes
[^rules]: Hackathon rules
[^spike]: Stack de-risking spike
[^stack]: Stack decisions and risks
[^pgjev]: pg-jev inspiration
[^rrsi]: RRSI inspiration
[^dream]: Dream-RSI inspiration
[^cls]: Fast-classifier use cases
[^grag]: GraphRAG SDK retrieval strategies
