---
type: Status Report
title: Neo-Cortex build status (what was actually built)
description: Snapshot of the finished Neo-Cortex system versus the unified build plan - what was done, changed or cut and why, the key design changes the evaluation forced, the final eval numbers copied from the eval files, and open risks.
tags: [architecture, status, build, eval, mcp, pagerank, graphrag, agent-memory, company-brain]
status: stable
generated: { by: glm-5-3-flash/orchestrator, at: 2026-10-16T21:37:00Z }
stale_after: 2026-10-18T18:29:00Z
sources:
  - id: plan
    resource: /architecture/unified-plan.md
    title: Unified build plan (draft)
---

# What was built, per plan section

The plan is [/architecture/unified-plan.md](/architecture/unified-plan.md). Product state lives in the repo (`README.md`, `src/neo_cortex/AGENTS.md`); eval numbers below are copied verbatim from the eval files, cited by repo path.

| Plan section | State | Notes |
|---|---|---|
| Store, schema, models (Phase 0) | done | `Store` over embedded falkordblite on `127.0.0.1:6390` or `NEO_FALKORDB_URL`; idempotent `ensure_schema`; lazy GLiNER2.5 + EmbeddingGemma singletons, float32-forced, text-only load. |
| Write path | done | `remember`, `ingest` (non-markdown via anydoc), GLiNER extraction, entity resolution with the cached `Judgment` judge, dedupe/supersede, vector batch writes. Extraction changed substantially (see design changes). |
| Synthetic corpus + gold set | changed | 102-doc Pellucid Pay corpus (`data/synthetic`, AI-generated, fictional); 80 retrieval questions + 30 structured-answer questions (plan said ~40). The public open-source org data became an eval distractor setting (~400 docs, `eval/results_distract.json`), not a demo corpus. |
| Read path (4 channels + RRF) | changed | Channels and weighted RRF shipped as planned, but the graph channel became HippoRAG-style Personalized PageRank instead of k-hop expansion + `algo.pageRank` + `algo.SPpaths`. |
| MCP tools (~10) | expanded | 15 tools shipped; `impact`, `relate`, `read` and `dream` were added beyond the planned list. |
| MCP server, `neo` CLI, hooks | done | Streamable-HTTP daemon at `/mcp` plus stdio entry point, loopback `/api` routes with background jobs, full `neo` CLI, Claude Code hooks (`session-start` brief; `session-end`/`pre-compact` return in ~60 ms and extract up to 15 memories in the background). |
| Dream consolidation | done (reduced) | Merge, promote (episodic clusters seen in >= 3 sessions), decay, conflict flagging, `DreamRun` nodes, idempotent. The plan's hypothesis-edge promotion was not built. |
| RRSI-style tuner | built, rejected its own weights | `eval/tune.py`: 36-combo grid, odd-split search, even-split acceptance. The best odd-split weights (bm25 x2, graph x0.5, temporal x2) scored -0.019 on the held-out even split, 95% CI [-0.075, +0.038], so `accepted: false`; the product ships untuned default weights. Every trial is a `:TuneRun` node. |
| graphrag-sdk | cut | User decision (already recorded in the plan): retrieval is own Cypher + `bm25s`. |
| Demo + README + blog | done | Demo kit (`demo/`) with verified shot list, README with evaluation summary, Cypher and architecture docs, blog post draft. |
| Live deploy | cut | Dropped per the plan's cut order; buffer used for audit fixes and the concurrency stress test. |

# Key design changes versus the plan

1. **Graph channel became Personalized PageRank.** The planned `algo.pageRank` has no personalization, so the built channel (`retrieve/channels.py`) runs numpy PPR over a local subgraph (max 3 hops, 500 nodes): reset mass is 50% linked query entities + 50% entities from the top dense/BM25 hits, chunk-to-entity mass weighted by confidence x specificity, so hub entities carry little. `algo.SPpaths` survives only in `connect`/`ask` bridging.
2. **The eval showed document retrieval ties text, so the product pivoted to graph-native answer tools.** Graph-routed retrieval adds nothing measurable over vector+BM25 on document finding (see numbers below), so the graph's value was moved into `impact`/`who`/`timeline`/`relate`, which answer from edges (ownership, dependency, supersession) rather than from retrieved text. Impact/blast radius is the one category where the graph significantly beats text search.
3. **Relation recall roughly doubled after the extraction rework.** The 0.41 baseline is from an earlier pre-fix extraction run that appears in no `eval/` file; it is recorded only in the commit message of `65bd4c7` ("Extraction recall: relation recall 0.41 -> 0.83 at precision 0.87", 2026-10-17). The graded numbers that exist today (`eval/graph_quality.md`, fresh ingest vs `data/synthetic/WORLD.md`): precision 0.880 (66/75), recall 0.825. Extraction moved from per-chunk GLiNER relations to per-sentence GLiNER plus deterministic patterns (owns/depends-on/rename/replaced/decided/caused-by), OWNS supersession from later-dated documents, and former-state cues blocked.
4. **Session memory extraction is deterministic-first.** The plan said GLiNER auto-extracts session text; built (`session_mem.py`), deterministic patterns pick self-contained candidates (preferences, decisions, lessons, outcomes) and GLiNER only scores and types them, with up to 15 memories stored per session.
5. **REL edges are one relationship type with a `type` property**, so Cypher never builds relationship types from strings (the plan listed a fixed whitelist of edge types).
6. **Tenants are separate graphs** (`neo_<tenant>`), so nodes carry no tenant property (the plan had a `tenant` property on every node).
7. **Hooks return immediately.** `session-end`/`pre-compact` POST to the daemon with `background: true` and return in ~60 ms; extraction runs on the daemon's job thread.

# Final evaluation numbers

Copied exactly from the eval files (repo paths; they are outside this bundle).

**Retrieval** (`eval/results.md`; clean setting, 102 docs, 80 gold questions, recall@10 / fullcover@10, top 10 unique documents):

| config | recall@10 | fullcover@10 |
|---|---|---|
| vector | 0.73 | 0.53 |
| bm25 | 0.71 | 0.54 |
| vector+bm25 | 0.75 | 0.59 |
| auto (graph-routed, product default) | 0.74 | 0.56 |
| full (all four channels, intent weights) | 0.76 | 0.60 |

Paired bootstrap (1000 resamples, seed 0), all questions vs `vector+bm25` (`eval/results.md`, "Paired bootstrap"): recall@10 `full` +0.006 [-0.029, +0.040] (n=80, inside noise), `auto` -0.010 [-0.044, +0.023]; fullcover@10 `full` +0.013 [-0.062, +0.087], `auto` -0.025 [-0.087, +0.037]. Document retrieval ties text.

**Graph-native answers** (`eval/answers.md`, run `final`; 30 questions, 4000-char budget on both sides; baseline = top-8 vector chunks; "all keys" = every expected key present):

| Category (n) | Tool, all keys | Baseline, all keys | Tool minus baseline, 95% CI |
|---|---|---|---|
| Impact / blast radius (10) | 0.80 | 0.20 | +0.60 [+0.30, +0.90], significant |
| Current owner (10) | 1.00 | 1.00 | +0.00 [+0.00, +0.00], tie |
| Value changes (10) | 0.80 | 1.00 | -0.20 [-0.50, +0.00], inside noise, tool lower |
| Overall (30) | 0.87 | 0.73 | +0.13 [-0.03, +0.33], inside noise |

**Tool checks** (`eval/results.md`, "Tools vs vector-only baselines"): `ask` gold answer keys multi 0.65 / ownership 0.76 (n=26/17) vs baseline 0.85 / 0.82, mean output 3810 vs 9932 chars, ask 205 ms; `who` with the gold non-person entity as topic: gold person in top 3 (any) 0.94 vs baseline 0.71; `timeline`: both old+new values listed 1.00 vs baseline 0.75.

**Extraction** (`eval/graph_quality.md`, fresh ingest vs `data/synthetic/WORLD.md`): REL edges 97 (79 distinct); overall graded precision 0.880 (66/75), recall 0.825; OWNS 0.93/1.00, DECIDED 1.00/1.00, CAUSED_BY recall 0/5.

**Concurrency** (`eval/stress.md`, 2026-10-17 run): 16 clients, 13.1 ops/s, 0 errors, 0 lost writes; daemon shut down cleanly on SIGTERM with no orphan server.

# Built on 2026-10-17 (final day)

One line each; the source is the named commit or eval file.

- Agent-direct graph writes: `remember(kind, entities, relations)` writes without GLiNER extraction; `relate(end=True)` retires an edge as history (commit `bc62cc8`).
- Code ingestion: `.py` files are chunked via `ast` and yield component entities (commit `bc62cc8`).
- OKF frontmatter fields: `doc_type`/`description`/`tags` from bundle frontmatter are stored on Document nodes (commit `bc62cc8`).
- Single-owner store lock: exclusive `flock` per `NEO_HOME`; the CLI never falls back to a local store for an explicit `NEO_DAEMON_URL` (commit `bc62cc8`).
- CUDA OOM fallback to CPU under `NEO_DEVICE=auto` (commit `bc62cc8`).
- Entity type by weighted vote across mentions (commit `6898afb`).
- File-entity rule: file entities are created only for repo paths (commit `6898afb`).
- Seed-strength gate for the graph channel: no graph channel without a strong seed, channel weight scaled by seed strength (commit `bc62cc8`).
- Decision routing (commit `bc62cc8`).
- Query-matching snippets in `recall`/`ask` output (commit `6898afb`).
- Real-docs check (`eval/real_check.py` + `eval/real_gold.jsonl`, commit `e4e196d`; numbers in `eval/real_check.md`): the repository's own 69 docs, 30 questions - Hit@5 0.53, MRR 0.39, AnswerIn chunk5 0.73; entity checks 4/5 PASS; targeted relation checks 0/5 found; only 12 REL edges in the whole corpus.
- MCP smoke test (`scripts/mcp_smoke.py`, commit `e4e196d`; numbers in `eval/mcp_smoke.md`): 15 of 15 tools OK on commit `bc62cc8`, tool descriptions plus schemas cost about 2077 tokens of agent context per session.
- anydoc ingestion verified for docx, xlsx, pptx, pdf, rtf, csv - converts with tables, entities and relations; unsupported/scanned/encrypted files are counted, never abort a batch (commit `2637587`).
- `docs/lineage.md`: source, what we took, code location and measured result per outside idea (commit `504c816`).
- Third-party evidence no longer redistributed: 410 files deleted from `knowledge/`, each source now recorded in frontmatter as `url` + `sha256` + `retrieved_at` + `redistributed: false` (commit `dd6f36f`; `knowledge/log.md`, 2026-10-17).

# Open risks

- GLiNER finds few relations in real prose (`eval/real_check.md`: 12 REL edges in 69 docs, most from command text in demo scripts), so on real data agents should write relations directly (`remember(entities=, relations=)`, `relate`). JointIE and a combined schema were measured and did not beat the split extractor (2026-10-17: P 0.719 / 0.774 vs 0.880).
- The edge gate (pg-jev-style assertion gating) is built on the base model and neutral on synthetic F1 (0.852 -> 0.855, fact-only view); the base model misses most negations. A GLiNER2.5-Decide comparison is in progress; no result is claimed here.
- Small evaluation: one synthetic corpus, 110 questions written by the team that built the tools; numbers show the design works on this corpus, not general accuracy.
- Value-change answers did not beat the text baseline (0.80 vs 1.00 all keys) and `timeline`'s win is inside noise (n=8).
- CAUSED_BY relations are never extracted (recall 0/5); some other relations are absent from the graph, and answers then depend on the text channels.
- AnswerIn is 0.00 for temporal questions in every retrieval config (`eval/results.md`) - the gold answer strings are not in retrieved chunk text.
- Write latency is GPU-bound (~0.4-2 s p50); reads queue behind writes on the daemon's single Store at high concurrency.
- Single-node design: one daemon owns one graph, loopback-only, no authentication; BM25 index is rebuilt in full on corpus change; `dream` neighbour search is O(N^2).
- EmbeddingGemma 2 license ambiguity (card header says Apache-2.0, license link points to a Gemma URL) - read before redistributing weights.
- Whether falkordblite (BSD) or SSPLv1 FalkorDB satisfies the hackathon's FalkorDB requirement was never confirmed by the organisers.
