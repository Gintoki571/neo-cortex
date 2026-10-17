# Neo-Cortex: a guide for explaining it to judges

Plain answers to what a judge is likely to ask. Every number here comes from a file in `eval/` or from a commit message; the file is named next to it.

## 1. The 30-second pitch

AI agents forget everything between sessions, and the knowledge they need lives in documents, tickets and chats they cannot see as a whole. Neo-Cortex is one FalkorDB graph that is at the same time an agent's long-term memory, a company brain built from documents, and a reasoning layer that answers multi-hop questions. Agents use it through an MCP server (15 tools) or a `neo` command line. There is no LLM inside: two small local models (GLiNER2.5 for extraction and decisions, EmbeddingGemma for embeddings) do the fast "System 1" work, and the calling agent (Claude) does the reasoning.

## 2. Which track is it for?

All three, with one system:
- **01 Agents that act on connected data:** `ask` returns an evidence pack (seeds, graph paths between them, facts, cited chunks); `connect`, `impact`, `who` walk the graph.
- **02 Agent memory and coordination:** `remember`, `brief`, `handoff`, session ingestion through Claude Code hooks, `dream` consolidation, agents writing facts straight into the graph.
- **03 Company brain:** documents, tickets, ADRs, chats and meeting notes in one graph; owners, dependencies, decisions and their history.

## 3. How it is built (one picture in words)

`neo serve` starts one daemon on 127.0.0.1:8765. It owns the database (embedded FalkorDB through `falkordblite`; a file lock makes sure only one process opens it), loads the two models lazily, and serves MCP at `/mcp` plus a small HTTP API for hooks. Every tenant (team or project) is its own graph `neo_<tenant>`.

**Data model** (contract in `src/neo_cortex/AGENTS.md`):
- `Document` (one source file; kind doc/adr/ticket/chat/meeting/session/file) has `Chunk`s (slices with an embedding, the unit of search and citation).
- `Entity` (person, team, service, component, ticket, decision, customer, config setting, ...), linked from chunks by `MENTIONS`.
- `REL` edges between entities with a `type` (OWNS, MEMBER_OF, DEPENDS_ON, DECIDED, APPROVED, CAUSED_BY, REPLACED_BY, RENAMED_TO, ...), a confidence, the source chunk or memory, `valid_from`/`valid_to` dates, and (new) `modality` + `p_fact`.
- `Memory` (episodic, semantic, procedural, preference, decision) with `SUPERSEDES`, `CONFLICTS_WITH`, `MERGED_INTO`; `Session`, `Agent`, `Handoff`; audit nodes `Judgment`, `DreamRun`, `TuneRun`.

Time is a first-class property: an edge with an end date is history, so "who owns X now" and "what changed" are graph queries, not text guesses.

## 4. Getting knowledge in

Two ways, on purpose:

1. **Automatic, for documents nobody has read yet.** `ingest` converts the file (Markdown and text directly; docx, xlsx, pptx, pdf, rtf, csv through anydoc; HTML through a small built-in converter), chunks it (120-250 words on paragraph or message boundaries), embeds the chunks, and runs GLiNER2.5 for entities and relations. Relations also come from deterministic patterns ("X owns Y", "depends on", "replaced by", tables with an Owner column) because zero-shot relation extraction is weak (published GLiNER2.5 relation F1 is about 0.27-0.37). Every extracted relation then goes through an **edge gate**: its source sentence is classified as fact, possibility, denial or plan; denials are dropped, hedges are kept but not treated as current.
2. **Direct, for what an agent already knows.** `remember(text, kind, entities=[{name,type}], relations=[[head, TYPE, tail]])` writes typed entities and edges without running GLiNER at all (about 0.2 s, mostly the embedding). `relate(head, TYPE, tail)` adds or corrects one edge; `relate(..., end=True)` retires it and keeps it as history. Explicitly named entities only match exact names, so the agent's words are never fuzzily merged into something else.

Why both: on this repository's own prose GLiNER found only 12 relations in 69 documents (`eval/real_check.md`). The agent that just did the work knows the facts better than any extractor, so we let it write them.

**Entity resolution** (`resolve.py`): exact name, alias, a spelling-variant key (`GLiNER 2.5 base` = `gliner2.5-base-v1`), then embedding neighbours that must pass a lexical guard; in the borderline band GLiNER can only veto a merge. Code-like names merge only exactly. An entity's type is a confidence-weighted vote over all its mentions (one bad mention cannot turn FalkorDB into a "team").

**Sessions** (`session_mem.py`): Claude Code hooks send each transcript at session end; deterministic rules plus GLiNER scoring keep durable facts, decisions, preferences and lessons, and drop narration, fragments and plans.

## 5. Getting answers out (the RAG)

`recall` runs four channels and fuses them with weighted Reciprocal Rank Fusion (RRF, k=60):
1. **Vector:** EmbeddingGemma embeddings in FalkorDB's vector index (cosine).
2. **Text:** BM25 with `bm25s` (FalkorDB's full-text index is not BM25, so we keep a BM25 index next to it).
3. **Graph:** HippoRAG-style personalized PageRank over the entity-chunk graph, seeded by the question's entities. It only runs when a question entity links strongly (seed-strength gate); otherwise weak matches would pull rankings off.
4. **Temporal:** recency and explicit dates ("since June", "on 2026-07-15") as filters or a channel.

GLiNER2.5 classifies the question's intent (owner, connection, change over time, decision, fact) and shifts channel weights softly; "why/decided" questions boost decision memories and ADRs. Output shows, for every hit, the sentences that best match the question (not just the chunk's first lines), its id, source and which channels found it.

On top of `recall` sit graph-native tools: `who` (owners and experts), `impact` (blast radius over DEPENDS_ON), `timeline` (dated changes with sources, superseded values marked), `connect` (shortest paths with `algo.SPpaths`), `explore`, `read`, `ask` (evidence pack), `brief` (session-start context), `cypher` (read-only queries).

## 6. Results (and their honest limits)

| What | Result | File |
|---|---|---|
| Graph tools vs plain text search, 30 questions | impact (blast radius) 0.80 vs 0.20, delta +0.60 [+0.30, +0.90], significant; current owner 1.00 vs 1.00; value changes 0.80 vs 1.00; overall 0.87 vs 0.73 (inside noise) | `eval/answers.md` |
| Document retrieval, 80 questions, synthetic company | recall@10: vector 0.73, BM25 0.71, vector+BM25 0.75, full 0.76; graph ties text on finding documents | `eval/results.md` |
| `who` with the entity as topic | gold person in top 3: 0.94 vs 0.71 baseline | `eval/results.md` |
| Relation extraction (synthetic, graded types) | precision 0.88, recall 0.83; on the facts the tools read after the edge gate: 0.903 / 0.812 | `eval/graph_quality.py`, commit eac7484 |
| Real documents (this repo's 69 docs, 30 questions) | gold doc in top 5: 0.53, MRR 0.39; answer text in the top-5 chunks 0.73 | `eval/real_check.md` |
| MCP | 15 of 15 tools pass end to end; tool schemas cost about 2,100 tokens of agent context | `eval/mcp_smoke.md` |
| Concurrency | 16 clients, 0 errors, 0 lost writes; read p50 about 10 ms | `eval/stress.md` |

What to say about the limits: the synthetic company is AI-generated (the gold answers come from a spec the product never reads); the graph clearly wins on structural questions (blast radius, owners) and ties on plain document finding; real prose gives few automatic relations, which is why agents write relations directly; the published 0.33 -> 0.40 edge-gate gain did not reproduce on our data.

## 7. Decisions we made with evidence (good judge material)

- **No LLM inside.** Small local models are fast (GLiNER about 26 ms per call on a 6 GB GPU), cheap, private and deterministic; reasoning stays with the calling agent. Research and our own runs showed escalating hard cases to a bigger LLM did not help.
- **GLiNER2.5 vs GLiNER2.5-Decide** for the edge gate: on 25 hand-labelled trap sentences, base model 17/25, base + a negation rule 20/25, Decide 20/25 but a second 1.9 GB model and 6x slower. We kept base + rule.
- **JointIE and one combined schema** (GLiNER2.5's newer decoding): implemented and measured, precision 0.72 and 0.77 vs 0.88, slower on real documents. Not adopted.
- **fp16** on the GTX 1660 Ti: half the memory but 2.4x slower. Opt-in only.
- **Self-tuning with an acceptance rule (RRSI idea):** the tuner proposes new channel weights and keeps them only if they beat the noise band on held-out questions without a cost penalty. It rejected its own weights, which is the rule working.
- **Dream consolidation (Dream-RSI idea):** `neo dream` merges duplicate memories, promotes, decays and flags conflicts, logged as `DreamRun` nodes.
- **pg-jev idea:** decisions are cached next to the data (`Judgment` nodes) and every relation carries its assertion verdict.

Details and sources: `docs/lineage.md`.

## 8. FalkorDB features used

Embedded FalkorDB (`falkordblite`) on 127.0.0.1 only, Cypher, vector indexes on Chunk/Memory/Entity embeddings, `algo.SPpaths` for bridging paths, variable-length paths for impact and ownership, read-only `GRAPH.RO_QUERY` for the agent's `cypher` tool, one graph per tenant. Personalized PageRank is computed in numpy over a local subgraph because `algo.pageRank` has no personalization.

## 9. Likely questions

- **"Why not just a vector database?"** Vector search finds similar text; it cannot tell you who owns a service now, what breaks if it goes down, or which decision replaced which. Measured: blast radius 0.80 with the graph vs 0.20 with text.
- **"Where does the graph come from without an LLM?"** GLiNER2.5 plus deterministic patterns for documents, and agents writing facts directly with `remember(entities, relations)` / `relate`.
- **"How do you avoid stale facts?"** Edges and memories carry validity dates; a newer document or `relate --supersede` closes the old edge; `timeline` shows the history; `dream` flags conflicting memories for the agent to resolve.
- **"How do you know it works?"** Two evaluations (synthetic gold set with paired bootstrap CIs, and this repo's own docs), an MCP smoke test, a stress test and 230 unit tests. We report where the graph loses too.
- **"Is it safe?"** Loopback-only daemon, one owner per database (file lock), read-only Cypher for agents, request size limits, tests isolated from real data.
- **"What would you do next?"** Better relation extraction from real prose, an answer-grounding check, and lessons from open memory systems (agentmemory, graphify, Hindsight) for fusion and temporal reasoning.

## 10. How it was built

With Claude Code as orchestrator and AI coding sub-agents (Claude models, GitHub Copilot CLI, CodeBuddy, OpenCode), directed, reviewed and verified by the team. The project's own research is an OKF knowledge bundle in `knowledge/`; the work rules are AGENTS.md files (DOX). See the AI-use disclosure in the README.
