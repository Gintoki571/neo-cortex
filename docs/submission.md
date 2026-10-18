# Neo-Cortex — hackathon submission text

Ready to paste into the hackathon form. Every number names the repo file it was copied from.

## 1. Project name and tagline

**Neo-Cortex**

One FalkorDB graph: agent memory, company brain, and multi-hop reasoning over MCP — no LLM inside.

(98 characters; wording follows README.md line 3.)

## 2. Inspiration

AI agents forget everything between sessions, and the knowledge they need is scattered across documents, tickets and chats no agent can read whole. One typed graph holds both, because ownership, dependency and supersession are edges with validity dates, so "who owns it now" and "what changed" become queries, not text guesses. Memory, company knowledge and reasoning in one store is what lets one system serve all three tracks. (README.md)

## 3. What it does

**01 Agents that act on connected data.** `ask` returns a multi-hop evidence pack — seeds, shortest `SPpaths` between them, cited chunks and facts — so the agent acts on cited structure, not similar text; `connect`, `impact` and `who` walk the same graph. (README.md)

**02 Agent memory and coordination.** Episodic, semantic, procedural, preference and decision memories with `SUPERSEDES`, `CONFLICTS_WITH` and `MERGED_INTO` edges; Claude Code hooks inject a brief at session start and extract memories at session end; `neo dream` consolidates. (README.md)

**03 Company brain.** Documents, tickets, ADRs and chats in one graph; `who` finds owners and experts; `timeline` traces decisions to sources and shows what superseded what. (README.md)

## 4. How we built it

FalkorDB is the only store: embedded `falkordblite` on loopback, one graph per tenant, vector indexes on chunk, memory and entity embeddings, `algo.SPpaths` for bridging paths, variable-length paths for impact and ownership, read-only `GRAPH.RO_QUERY` for the agent's `cypher` tool (docs/judges-guide.md section 8). GLiNER2.5 extracts, types, routes intent and judges; EmbeddingGemma (text-only) embeds; `recall` fuses vector, `bm25s`, HippoRAG-style personalized PageRank and temporal channels with weighted RRF (README.md). No LLM inside — the calling agent reasons; 15 MCP tools and the `neo` CLI return compact, cited evidence. (README.md)

## 5. Challenges

- **Which model judges an edge?** Each extracted relation is classified fact / possibility / denial / plan. On 25 hand-labelled trap sentences: base model 17/25, base plus negation rule 20/25; GLiNER2.5-Decide also 20/25, but a second ~1.9 GB model about 6x slower — we kept base plus rule. (docs/judges-guide.md section 7)
- **Borrowed ideas had to earn their place.** Seven retrieval and resolution changes from agentmemory, graphify and Hindsight sit behind flags; none beat the default across both corpora, so all stay off. (README.md; eval/flags.md)
- **The self-tuner rejected its own weights.** An RRSI-style rule tried 36 weight combinations; the best odd-split weights scored -0.019 on held-out questions, CI [-0.075, +0.038], so `accepted: false`. (docs/lineage.md section 2)

## 6. Results

Copied as-is from docs/judges-guide.md section 6:

| What | Result | File |
|---|---|---|
| Graph tools vs plain text search, 30 questions | impact (blast radius) 0.80 vs 0.20, delta +0.60 [+0.30, +0.90], significant; current owner 1.00 vs 1.00; value changes 0.80 vs 1.00; overall 0.87 vs 0.73 (inside noise) | `eval/answers.md` |
| Document retrieval, 80 questions, synthetic company | recall@10: vector 0.73, BM25 0.71, vector+BM25 0.75, full 0.76; graph ties text on finding documents | `eval/results.md` |
| `ask` evidence pack vs vector top-8 text cut to the same length, multi-hop questions | answer keys present +0.23 [+0.04, +0.42], significant; multi-hop + ownership +0.07, inside noise | `eval/run_eval.py` (README) |
| `who` with the entity as topic | gold person in top 3: 0.94 vs 0.71 baseline | `eval/results.md` |
| Relation extraction (synthetic, graded types) | precision 0.88, recall 0.83; on the facts the tools read after the edge gate: 0.903 / 0.812 | `eval/graph_quality.py`, commit eac7484 |
| Real documents (this repo's 72 docs, 30 questions) | gold doc in top 5: 0.50, MRR 0.41; answer text in the top-5 chunks 0.70 | `eval/real_check.md` |
| MCP | 15 of 15 tools pass end to end; tool schemas cost about 2,100 tokens of agent context | `eval/mcp_smoke.md` |
| Concurrency | 16 clients, 0 errors, 0 lost writes; read p50 about 10 ms | `eval/stress.md` |

## 7. What we learned / what is next

- **Learned:** the graph clearly wins structural questions (blast radius 0.80 vs 0.20) and only ties plain document finding; real prose gives few relations (5 edges in 72 docs), so agents write relations directly. (README.md)
- **Learned:** measure everything you borrow — the published edge-gate gain (edge F1 0.330 -> 0.396) did not reproduce here. (docs/lineage.md section 5)
- **Next:** better relation extraction from real prose, an answer-grounding check, and fusion and temporal ideas from open memory systems. (docs/judges-guide.md section 9)

## 8. Built with

FalkorDB, falkordblite, GLiNER2.5 (`fastino/gliner2.5-base-v1`), EmbeddingGemma (`google/embeddinggemma-2`), bm25s, anydoc, numpy, Python, Model Context Protocol (MCP), Claude Code hooks

## 9. How to run it

Four commands from the README quick start, which also lists prerequisites and the two model downloads:

```bash
uv sync
uv run --no-sync neo serve --port 8765 --warm
for d in doc adr ticket chat meeting session; do uv run --no-sync neo ingest --wait data/synthetic/$d; done
uv run --no-sync neo ask "Who should review a change to the session cache today?"
```

## 10. AI use disclosure

Neo-Cortex was built with Claude Code, using Anthropic Claude models as the
orchestrator and coding sub-agents. The synthetic company corpus and
gold questions were AI-generated from a written specification and are
fictional. Humans directed, reviewed and verified the work, and are
responsible for the architecture, correctness claims and submitted material.
