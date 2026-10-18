# Neo-Cortex: judge Q&A drill

Thirty questions a technical judge is likely to ask, with short answers a person can say out loud and the repo file that backs each one. Jargon is defined in a clause where it first appears. Numbers are copied from the named file; nothing here is new measurement.

## Architecture

**1. In one sentence, what is Neo-Cortex?**
One FalkorDB graph that is at the same time an agent's long-term memory, a company brain built from documents, and a reasoning layer that answers multi-hop questions; agents reach it through an MCP server (MCP = the protocol that lets an AI agent call tools) with 15 tools or the `neo` command line. There is no LLM inside — two small local models do the fast work and the calling agent reasons.
File: README.md; docs/judges-guide.md section 1.

**2. Walk me through ingesting one document.**
The file is converted to Markdown (anydoc handles Office and PDF formats), cut into chunks of 120-250 words on paragraph or message boundaries, embedded with EmbeddingGemma, and read by GLiNER2.5 for entities and typed relations. Deterministic patterns add ownership, dependency, renaming and supersession relations, because zero-shot relation extraction is weak (published GLiNER2.5 relation F1 is about 0.27-0.37). Every extracted relation then passes an assertion gate before it becomes an edge.
File: docs/judges-guide.md section 4; docs/lineage.md section 8.

**3. Who owns the database, and how do teams keep data apart?**
One daemon opens the graph; the embedded FalkorDB takes an exclusive file lock, so a second writer gets an error naming the lock instead of corrupting data. Every tenant is its own graph named `neo_<tenant>`, so a company brain and a personal agent memory can share one server without seeing each other's data.
File: README.md; docs/judges-guide.md section 3.

## FalkorDB usage

**4. Which FalkorDB features are you actually using?**
Embedded falkordblite bound to loopback only, Cypher, vector indexes on chunk, memory and entity embeddings, `algo.SPpaths` (FalkorDB's shortest-path algorithm) for the bridging paths behind `ask` and `connect`, variable-length paths for impact and ownership walks, and read-only `GRAPH.RO_QUERY` for the agent's `cypher` tool. One graph per tenant — that is the whole surface.
File: docs/judges-guide.md section 8.

**5. Why not just use a vector database?**
Vector search finds similar text; it cannot tell you who owns a service now, what breaks if it goes down, or which decision replaced which. Measured on 30 structured questions: blast-radius answers (what depends on a component) scored 0.80 with the graph versus 0.20 with top-8 text chunks, a difference of +0.60 with a 95% confidence interval of [+0.30, +0.90].
File: docs/judges-guide.md sections 6 and 9.

**6. Why is PageRank computed in numpy instead of `algo.pageRank`?**
`algo.pageRank` has no personalization — you cannot tell it to start the walk at the query's entities. So the graph channel runs Personalized PageRank (a graph walk that scores nodes by how strongly the query entities reach them; restart probability 0.5, at most 3 hops and 500 nodes) over a local subgraph in numpy, HippoRAG-style. A seed-strength gate keeps the channel out of the fusion unless a query entity links strongly (below a seed floor of 0.2 it returns nothing), so weak entity matches cannot pull rankings off the text channels.
File: docs/judges-guide.md section 8; docs/lineage.md section 4.

## Why GLiNER

**7. Why GLiNER2.5 instead of an LLM for extraction?**
GLiNER2.5 is a small encoder — about 26 ms per call on a 6 GB GPU — that extracts entities and relations, types memories, routes query intent and judges borderline entity merges. It is deterministic, private and needs no API, and no LLM SDK is imported anywhere under `src/neo_cortex/`. The reasoning stays with the calling agent.
File: docs/judges-guide.md section 7; docs/lineage.md section 5.

**8. How good is the extraction, honestly?**
On the synthetic corpus, graded relation types give precision 0.88 and recall 0.83, and 0.903 / 0.812 on the facts the tools read after the assertion gate. On this repository's own prose GLiNER found only 5 relations in 72 documents, which is exactly why agents can write relations directly.
File: README.md; docs/judges-guide.md sections 4 and 6.

**9. What is the edge gate?**
Every extracted relation is classified on its source sentence as fact, possibility, denial or plan; denials are dropped and hedges are kept but not treated as current. The verdict (`modality`, `p_fact`) is stored on the edge, so "current state" queries read facts only.
File: docs/judges-guide.md section 4; docs/lineage.md section 1.

## Why no LLM

**10. Why is there no LLM inside the system?**
Small local models are fast, cheap, private and deterministic, and research plus our own runs showed that escalating hard cases to a bigger LLM did not help. The calling agent is better at reasoning over evidence, so the tools return compact, cited evidence packs and the agent writes the answer.
File: docs/judges-guide.md section 7; README.md.

**11. If there is no LLM, who writes the final answers?**
The calling agent — Claude Code or any MCP client. `ask` returns seeds, bridging paths, facts and cited chunks, and the agent composes the answer, so answer quality depends on that agent; we list that as a limitation, not hide it.
File: README.md.

**12. How do you keep the system auditable without an LLM?**
Decisions are stored as data: `Judgment` nodes cache yes/no and choice decisions by content hash, every relation carries its source and its assertion verdict, and each consolidation or tuning run writes a `DreamRun` or `TuneRun` node. You can replay why an edge exists.
File: docs/judges-guide.md section 3; docs/lineage.md section 1.

## Evaluation honesty

**13. How do you know it works?**
Two evaluations: an 80-question synthetic gold set with paired-bootstrap confidence intervals (1000 resamples, seed 0 — resampling the questions to estimate the range the true difference lies in), and this repository's own 72 documents with 30 questions an agent working on it asks. On top of that, an MCP smoke test where 15 of 15 tools pass, a concurrency stress test of 16 clients with 0 errors and 0 lost writes, and unit tests. We report where the graph loses too.
File: docs/judges-guide.md sections 6 and 9; README.md.

**14. Isn't the synthetic corpus graded by the people who built the tools?**
Yes, and we say so in the README: the 102 documents are AI-generated and fictional, and the gold answers come from a world specification the product never reads. The numbers show the design works on this corpus; they do not establish general accuracy.
File: README.md; docs/judges-guide.md section 6.

**15. Where does the graph lose?**
Value-change answers: 0.80 with the graph versus 1.00 for the text baseline — inside noise and lower. Document finding is a tie with text retrieval, and the overall structured-answer delta of +0.13 is inside noise. Current-owner answers are a 1.00 versus 1.00 tie. All of that is in the README results table rather than hidden.
File: README.md; docs/judges-guide.md section 6.

**16. What did you measure on real, non-synthetic prose?**
On this repository's own 72 documents and 30 questions, the gold document is in the top 5 for 0.50 of questions with MRR 0.41 (mean reciprocal rank — how high the right document usually sits), and the answer string appears in the top-5 chunks for 0.70. GLiNER finds few relations there — 5 edges in 72 documents — so agents write relations directly.
File: README.md; docs/judges-guide.md section 6.

## Limits

**17. What are the biggest limitations?**
The evaluation is small and self-graded; GLiNER misses many relations (CAUSED_BY recall is 0 of 5, so some relations are simply absent from the graph); it is single-node with no replication, no multi-writer scaling and no authentication beyond the loopback binding; and the BM25 index is rebuilt in full whenever the corpus changes.
File: README.md; docs/lineage.md section 5; knowledge/architecture/build-status.md.

**18. Does it scale beyond one machine?**
Not today: one daemon owns one graph, there is no replication or multi-writer scaling, and writes are GPU-bound at roughly 0.4-2 s p50, with reads queueing behind writes on the daemon's single store at high concurrency. The stress test still showed 16 clients at 13.1 ops/s with 0 errors and 0 lost writes, and read p50 about 10 ms.
File: knowledge/architecture/build-status.md; docs/judges-guide.md section 6.

**19. What does the MCP interface cost the agent?**
The 15 tool schemas cost about 2,100 tokens of agent context per session — real, but small next to what the tools return, since each tool answer is token-budgeted with ids, sources, dates and confidence.
File: docs/judges-guide.md section 6; README.md.

## Security

**20. Is it safe to run?**
The daemon binds loopback only, exactly one process owns the graph via a file lock, agents get read-only Cypher, and request sizes are limited. There is no authentication, so keeping the daemon off public interfaces is a hard requirement, not advice.
File: docs/judges-guide.md section 9; README.md.

**21. Can one tenant read another tenant's data?**
No — each tenant is a separate graph (`neo_<tenant>`, default `default`) and nodes carry no tenant property, so the queries themselves cannot cross the boundary.
File: README.md.

## What is novel vs prior systems

**22. How is this different from HippoRAG?**
We took the Personalized PageRank idea but removed the LLM extraction step, added validity-dated edges, a seed-strength gate and agent-direct writes. Our measured results also differ: the graph channel adds nothing on document finding (recall@10 0.74 for vector+BM25+graph versus 0.75 for vector+BM25) but wins blast radius 0.80 versus 0.20.
File: docs/lineage.md section 4; eval/results.md.

**23. How is this different from GraphRAG?**
graphrag-sdk was cut by decision early in the project; retrieval is our own Cypher plus bm25s, and the graph's value sits in graph-native answer tools (`impact`, `who`, `timeline`, `relate`) rather than community summaries. We never built an LLM indexing pipeline.
File: knowledge/architecture/build-status.md; README.md.

**24. How is this different from Mem0 or Zep?**
We did not build on either; every outside idea we took is listed in the lineage file with what we measured. Our memory layer is typed (episodic, semantic, procedural, preference, decision), validity-dated, and consolidated by a deterministic `dream` pass — no LLM writes, scores or edits memories.
File: docs/lineage.md; README.md.

**25. So what is genuinely novel here?**
The combination: a no-LLM "System 1" stack, assertion-gated edges with validity windows, agents writing facts directly, and — unusually — measured rejections, including a self-tuning rule that rejected its own weights and three extraction variants we built and dropped.
File: docs/judges-guide.md section 7; docs/lineage.md.

## How agents use it

**26. How does an agent use this day to day?**
Through MCP: `brief` at session start for context, `recall` for hybrid search with "why it matched", `remember` to store facts, `ask` for multi-hop evidence, and `cypher` as the read-only escape hatch. Or through the `neo` CLI, which exposes the same operations as commands.
File: README.md.

**27. What do the Claude Code hooks do?**
The session-start hook injects the brief, so memory works even if the agent never calls `remember`; the session-end and pre-compact hooks send the transcript, return in about 60 ms, and extract up to 15 memories in the background using deterministic patterns with GLiNER only scoring them.
File: README.md; knowledge/architecture/build-status.md.

**28. What does `ask` actually return?**
An evidence pack, not prose: seeds, the bridging paths between them, facts and cited chunks with ids and dates. The calling agent reads it and writes the answer — that split is the "no LLM inside" design.
File: README.md.

## What failed

**29. What did you build and throw away?**
GLiNER2.5-Decide as the edge gate (same 20/25 trap-probe score as base plus rule, but a second ~1.9 GB model about 6x slower); JointIE and a combined extraction schema (precision 0.719 and 0.774 versus 0.880, and slower on real documents); fp16 as a default (half the memory, 1098 -> 589 MB, but 2.4x slower — kept opt-in); and seven flag-gated ideas from agentmemory, graphify and Hindsight, none of which beat the default on both corpora.
File: README.md; docs/judges-guide.md section 7; eval/flags.md.

**30. Why did the tuner's weights never ship, and what is next?**
The RRSI-style acceptance rule (accept only if the held-out lower confidence bound is above zero and latency stays within 20%) searched 36 weight combinations; the best odd-split weights scored -0.019 on the even split with CI [-0.075, +0.038], so `accepted: false` and the product ships the defaults. Next: better relation extraction from real prose and an answer-grounding check.
File: docs/lineage.md section 2; docs/judges-guide.md section 9.

## Things we do NOT claim

From docs/judges-guide.md section 6 and knowledge/architecture/build-status.md (open risks):

1. **No independent evaluation.** The synthetic company is AI-generated and its gold answers come from a specification the product never reads. (docs/judges-guide.md section 6)
2. **No general win on document finding.** The graph ties text search: recall@10 0.76 for full versus 0.75 for vector+BM25, CI [-0.029, +0.040]. (docs/judges-guide.md section 6; eval/results.md)
3. **No overall win on structured answers.** 0.87 versus 0.73 overall is inside noise. (docs/judges-guide.md section 6)
4. **No win on current-owner questions.** 1.00 versus 1.00, a tie. (docs/judges-guide.md section 6)
5. **Value-change answers lose.** 0.80 versus 1.00, inside noise, tool lower. (docs/judges-guide.md section 6)
6. **No automatic knowledge capture from real prose.** 5 relation edges in 72 real documents; agents must write relations directly. (docs/judges-guide.md section 6; README.md)
7. **No reproduction of the published edge-gate gain.** The published edge F1 0.330 -> 0.396 did not reproduce on our data. (docs/judges-guide.md section 6)
8. **No free MCP interface.** Tool schemas cost about 2,100 tokens of agent context per session. (docs/judges-guide.md section 6)
9. **No strong real-docs retrieval.** Gold document in the top 5 for 0.50 of questions, MRR 0.41. (docs/judges-guide.md section 6)
10. **No extraction-quality claim for the edge gate.** It is F1-neutral on synthetic relations (0.852 -> 0.855, fact-only view) and the base model misses most negations. (knowledge/architecture/build-status.md)
11. **No general accuracy claim.** One synthetic corpus, 110 questions written by the team that built the tools. (knowledge/architecture/build-status.md)
12. **No timeline win beyond noise.** `timeline`'s advantage over the text baseline is inside noise (n=8). (knowledge/architecture/build-status.md)
13. **No CAUSED_BY extraction.** Recall 0 of 5; some relations are absent and answers then depend on the text channels. (knowledge/architecture/build-status.md)
14. **No temporal answer-in-chunk retrieval.** AnswerIn is 0.00 for temporal questions in every retrieval config. (knowledge/architecture/build-status.md)
15. **No write-latency claim.** Writes are GPU-bound at roughly 0.4-2 s p50 and reads queue behind writes at high concurrency. (knowledge/architecture/build-status.md)
16. **No scale-out, no auth.** Single node, one daemon owns one graph, loopback-only, no authentication; the BM25 index is fully rebuilt on corpus change; `dream` neighbour search is O(N^2). (knowledge/architecture/build-status.md)
17. **No license certainty for EmbeddingGemma 2.** The card header says Apache-2.0 but the license link points to a Gemma URL — read it before redistributing weights. (knowledge/architecture/build-status.md)
18. **No confirmation of the FalkorDB requirement.** Whether falkordblite (BSD) or SSPLv1 FalkorDB satisfies the hackathon rule was never confirmed by the organisers. (knowledge/architecture/build-status.md)
