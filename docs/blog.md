# Neo-Cortex: One FalkorDB Graph for Agent Memory, Company Knowledge, and Reasoning

AI agents are good at the task in front of them and surprisingly bad at the past. A session ends, the useful decision disappears into a transcript, and the next session starts from zero. Inside a company, the situation is worse: the answer may be split across an ADR, a ticket, a chat thread, a meeting note, and somebody's memory. A conventional text-RAG system can retrieve passages, but it struggles with questions whose answer is a relationship rather than a paragraph: **Who owns this now?** What changed? **What breaks if this service fails?**

Neo-Cortex is our answer for the WeMakeDevs x FalkorDB Graph Hacks hackathon. It uses one FalkorDB graph as three things at once: agent memory, a company brain, and a substrate for multi-hop reasoning. Agents reach it through MCP, while Claude Code hooks make memory automatic. The graph is not a decorative index around a text database. It stores the entities, typed relationships, memories, documents, sessions, ownership changes, and provenance that make structural questions answerable.

## The design: keep the reasoner outside

The most important design decision was to put **no LLM inside Neo-Cortex**. GLiNER2.5 runs locally for entity and relation extraction, memory classification, query intent routing, and small judgments such as borderline entity resolution. EmbeddingGemma runs locally for vector representations. FalkorDB stores the resulting graph and indexes. The calling agent—Claude Code or another MCP client—does the reasoning and writes the final answer.

That boundary is deliberate. The server returns compact, cited evidence: chunks and memories, dates, confidence, channel ranks, and graph paths. It does not pretend that an extracted relation is a complete explanation. The agent can inspect the evidence, decide how much to trust it, and explain the result to the user. It also means the same graph tools work for different agents without hiding an additional hosted model call in the middle.

The graph has typed `Entity` nodes for people, teams, services, components, files, configuration settings, tickets, customers, and more. Documents become chunks connected by `HAS_CHUNK`; chunks and memories connect to entities through `MENTIONS`; entity-to-entity facts are represented by a single `REL` edge with a whitelisted `type` such as `OWNS`, `DEPENDS_ON`, `CAUSED_BY`, `APPROVED`, or `REPLACED_BY`. Memories can be episodic, semantic, procedural, preference, or decision memories. They retain source, time, agent, project, confidence, and status.

This is where FalkorDB does work that a flat collection of passages cannot do as naturally. `OWNS` can be closed when a later document names a new owner. `SUPERSEDES` can connect a new memory to the fact it replaced. `DEPENDS_ON` edges can be traversed in both directions to expose a blast radius. Every answer can lead back to the chunk, session, or memory that supplied it.

## Retrieval is hybrid, and intent changes the mix

Neo-Cortex's `recall` path runs four retrieval channels over the same graph-backed corpus:

1. **Vector search** uses EmbeddingGemma over chunk and memory embeddings.
2. **BM25** uses `bm25s` in process over those same texts.
3. **Graph search** builds a local subgraph around linked query entities and top dense/BM25 hits, then computes a Personalized PageRank-style score over it. A seed-strength gate keeps the channel out of the fusion unless a question entity links strongly to the graph, so a weak or wrong entity match cannot pull the ranking off the text channels.
4. **Temporal retrieval** applies explicit windows and validity dates, while "current" and "latest" act as recency cues.

The lists are fused with weighted reciprocal rank fusion: `score = sum_c w_c / (60 + rank_c)`. GLiNER parses the query into entities, intent, and time expressions. An owner or connection question boosts the graph channel; a temporal question boosts the temporal channel; a fact question leans more on vector and BM25. The weights are soft, so a routing mistake nudges the ranking instead of making the system choose one brittle path.

The graph channel is intentionally bounded: at most three expansion hops and 500 local nodes, with specificity weighting so a heavily mentioned hub does not overwhelm the result. For `ask` and `connect`, the system also returns shortest paths between seed entities. The output is an evidence pack, not a giant context dump.

## Memory without relying on user discipline

An agent can explicitly call `remember`, but the lifecycle is designed not to depend on that habit. Claude Code's `SessionStart` hook asks for a brief containing active preferences, decisions, lessons, recent episodes, and open handoffs. `SessionEnd` and `PreCompact` send the transcript to the daemon, which returns in about 60 ms and extracts candidates in the background.

Session extraction is deterministic first: it looks for self-contained preferences, decisions, procedural lessons, and concrete outcomes, then uses GLiNER to score and type candidates. Up to 15 useful memories can be stored, each linked back to its session and source. A near-duplicate reinforces an active memory instead of multiplying it. A caller can explicitly supersede an old memory, and conflicting memories remain visible for the agent to resolve rather than being silently overwritten.

The `dream` operation is the consolidation pass. It merges near-duplicate memories, promotes recurring episodic information into semantic memory with provenance, decays unused memories without deleting them, and flags conflicts. It is intentionally not an LLM "reflection" loop: it reads the graph, plans deterministic changes, writes them in batches, and records a `DreamRun`.

## Agents write the graph directly

Extraction is for documents nobody has read yet. When the agent already knows the facts, it writes them itself: `remember(text, kind, entities=[{name, type}], relations=[[head, TYPE, tail]])` stores typed entities and edges without running GLiNER at all (about 0.2 s, mostly the embedding), and `relate(head, TYPE, tail)` writes or corrects one edge — with `supersede` closing the edge it replaces and `end` retiring it while keeping the history. Explicitly named entities only ever match by exact name or alias, so the agent's words are never fuzzily merged into something else.

The motivation is measured: on our own repository's 72 prose documents, GLiNER found only 5 relations (`eval/real_check.md`). The agent that just fixed the bug knows what changed better than any extractor, so we let it write. In the demo, the triage agent moves ownership of `reporting-service` to Elif Yildiz with one `relate --supersede` call — the old edge is closed and kept as dated history — and leaves a handoff that appears in the next agent's session-start brief.

## What the evaluation actually showed

We evaluated against a fictional Pellucid Pay company corpus: 102 AI-generated documents and 80 gold retrieval questions. The question set includes single-hop, multi-hop, temporal, ownership, and procedural cases. The gold set and world specification were kept separate from the product. Comparisons use paired bootstrap confidence intervals with 1,000 resamples and seed 0.

The honest result is not "the graph wins every retrieval metric." For document retrieval at top 10, vector search reached Recall@10 **0.73** and FullCover@10 **0.53**. The product's graph-routed `auto` configuration reached **0.74** and **0.56**; the `full` four-channel configuration reached **0.76** and **0.60**. Full versus vector + BM25: Recall@10 **+0.006 [-0.029, +0.040]**, FullCover@10 **+0.013 [-0.062, +0.087]**. The confidence intervals include zero. In other words, on this corpus, the graph ties text-oriented retrieval for finding documents.

The stronger signal appears when we stop asking whether the right document was retrieved and ask for a structured answer. In the separate 30-question graph-native evaluation, the impact/blast-radius category scored **0.80** all-keys for the tool versus **0.20** for the top-8 vector baseline: **+0.60 [+0.30, +0.90]**, statistically significant. That is the category most directly aligned with the graph's purpose: enumerate dependents, owners to notify, customers, and incidents across multiple hops.

For current ownership, the tool and baseline both scored **1.00** all-keys, and both had correct current-owner accuracy **1.00**. That is a tie, not a claim that the graph improved the number. For value changes, the tool scored **0.80** versus the baseline's **1.00**, a delta of **-0.20 [-0.50, +0.00]**, inside noise and lower — we report where the graph loses too. Overall all-keys was **0.87** versus **0.73**, a delta of **+0.13 [-0.03, +0.33]**, also inside noise.

The dedicated `who` check adds useful detail: with the entity as topic, a gold person appeared in the top three **0.94** of the time versus **0.71** for the vector-document baseline. On real documents — this repository's own 69 docs and 30 questions an agent working on it asks — the gold document was in the top 5 for **0.53** of questions (MRR 0.39), and the answer string appeared in the top-5 chunks for **0.73**, because facts repeat across documents.

## What we measured and dropped

Several plausible upgrades were implemented, measured, and rejected on evidence:

- **GLiNER2.5-Decide as the edge gate.** Every extracted relation is classified on its source sentence as fact, possibility, denial, or plan. On a 25-sentence trap probe, the base model alone scored 17/25, base plus a negation-cue rule 20/25, and the dedicated Decide checkpoint also 20/25 — but Decide is a second ~1.9 GB model and about 6x slower. We kept base + rule (the gate moves synthetic fact-only relations to precision 0.903, recall 0.812).
- **JointIE and one combined schema** (GLiNER2.5's newer typed decoding) behind `NEO_EXTRACT`: relation precision 0.719 and 0.774 versus 0.880 for the default split extractor, and slower on real documents (222 s and 140 s versus 92 s). The default stays split.
- **fp16 GLiNER on the GTX 1660 Ti**: peak GPU memory halved (1098 -> 589 MB) but roughly 2.4x slower per call. Opt-in only (`NEO_GLINER_FP16=1`), never the default.
- The published edge-gate gain this idea came from (edge F1 0.330 -> 0.396 on one author's 10-document corpus) did not reproduce on our data.

## Lessons and limitations

Extraction quality was the bottleneck. Relation precision is **0.88** with recall **0.83** on the synthetic corpus (graded relation types); on the facts the tools read after the edge gate, 0.903 / 0.812. Missing edges mean a graph query has nothing to traverse, and on real prose GLiNER still finds few relations — which is why agents write edges directly. The evaluation forced a similar conceptual pivot. We began with "find the right documents," then learned that the compelling use case is "answer structurally" — show the owner path, the timeline, or the blast radius with citations.

There are important limits. This is one synthetic corpus and 80 questions written by the same team, so the results do not establish general accuracy. Relation extraction can still miss facts, leaving text channels to carry the answer. The no-LLM design means answer quality still depends on the calling agent. The current deployment is a single loopback daemon with no replication, authentication, or multi-writer scaling. BM25 indexes are rebuilt when the corpus changes, which is acceptable at demo size but not a final large-scale architecture.

Neo-Cortex is therefore not a claim that graphs replace search. The evaluation says they are comparable for document retrieval here. The claim is narrower and more useful: when the question is about ownership, change, dependencies, or consequences, explicit structure gives an agent evidence it can traverse, inspect, and explain. One FalkorDB graph lets memory, company knowledge, and reasoning share that structure instead of rebuilding it separately for every session.

**AI use disclosure:** Neo-Cortex was built with AI coding assistants. Humans directed the design, reviewed the implementation, and verified the evaluation and claims; the synthetic corpus and gold questions are fictional and AI-generated from a written specification.
