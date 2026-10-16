# Neo-Cortex: One FalkorDB Graph for Agent Memory, Company Knowledge, and Reasoning

AI agents are good at the task in front of them and surprisingly bad at the past. A session ends, the useful decision disappears into a transcript, and the next session starts from zero. Inside a company, the situation is worse: the answer may be split across an ADR, a ticket, a chat thread, a meeting note, and somebody's memory. A conventional text-RAG system can retrieve passages, but it struggles with questions whose answer is a relationship rather than a paragraph: **Who owns this now?** What changed? **What breaks if this service fails?**

Neo-Cortex is our answer for the WeMakeDevs x FalkorDB Graph Hacks hackathon. It uses one FalkorDB graph as three things at once: agent memory, a company brain, and a substrate for multi-hop reasoning. Agents reach it through MCP, while Claude Code hooks make memory automatic. The graph is not a decorative index around a text database. It stores the entities, typed relationships, memories, documents, sessions, ownership changes, and provenance that make structural questions answerable.

## The design: keep the reasoner outside

The most important design decision was to put **no LLM inside Neo-Cortex**. GLiNER2.5 runs locally for entity and relation extraction, memory classification, query intent routing, and small judgments such as borderline entity resolution. EmbeddingGemma runs locally for vector representations. FalkorDB stores the resulting graph and indexes. The calling agent—Claude Code or another MCP client—does the reasoning and writes the final answer.

That boundary is deliberate. The server returns compact, cited evidence: chunks and memories, dates, confidence, channel ranks, and graph paths. It does not pretend that an extracted relation is a complete explanation. The agent can inspect the evidence, decide how much to trust it, and explain the result to the user. It also means the same graph tools work for different agents without hiding an additional hosted model call in the middle.

The graph has typed `Entity` nodes for people, teams, services, components, files, configuration settings, tickets, customers, and more. Documents become chunks connected by `HAS_CHUNK`; chunks and memories connect to entities through `MENTIONS`; entity-to-entity facts are represented by a single `REL` edge with a whitelisted `type` such as `OWNS`, `DEPENDS_ON`, `CAUSED_BY`, `APPROVED`, or `REPLACED_BY`. Memories can be episodic, semantic, procedural, preference, or decision memories. They retain source, time, agent, project, confidence, and status.

This is where FalkorDB does work that a flat collection of passages cannot do as naturally. `OWNS` can be closed when a later document names a new owner. `SUPERSEDES` can connect a new memory to the fact it replaced. `DEPENDS_ON` edges can be traversed in both directions to expose a blast radius. Every answer can lead back to the chunk, session, or memory that supplied it.

For example, the project’s read-only Cypher escape hatch supports ordinary graph inspection:

```cypher
MATCH (n) RETURN labels(n)[0] AS label, count(n) AS n ORDER BY n DESC
```

And the owner tool follows ownership-style paths rather than merely searching for the word “owner”:

```cypher
MATCH p=(x:Entity {type:'person'})-[:REL*1..2]->(t:Entity) WHERE t.id IN $t AND all(r IN relationships(p) WHERE r.type IN $ty) RETURN x.id, x.name, [n IN nodes(p) | [n.id, n.name]], [r IN relationships(p) | [r.type, startNode(r).id, r.source_id, r.valid_from_ms, r.conf]]
```

## Retrieval is hybrid, and intent changes the mix

Neo-Cortex’s `recall` path runs four retrieval channels over the same graph-backed corpus:

1. **Vector search** uses EmbeddingGemma over chunk and memory embeddings.
2. **BM25** uses `bm25s` in process over those same texts.
3. **Graph search** builds a local subgraph around linked query entities and top dense/BM25 hits, then computes a Personalized PageRank-style score over it.
4. **Temporal retrieval** applies explicit windows and validity dates, while “current” and “latest” act as recency cues.

The lists are fused with weighted reciprocal rank fusion: `score = sum_c w_c / (60 + rank_c)`. GLiNER parses the query into entities, intent, and time expressions. An owner or connection question boosts the graph channel; a temporal question boosts the temporal channel; a fact question leans more on vector and BM25. The weights are soft, so a routing mistake nudges the ranking instead of making the system choose one brittle path.

The graph channel is intentionally bounded: at most three expansion hops and 500 local nodes, with specificity weighting so a heavily mentioned hub does not overwhelm the result. For `ask` and `connect`, the system also returns shortest paths between seed entities. The output is an evidence pack, not a giant context dump.

## Memory without relying on user discipline

An agent can explicitly call `remember`, but the lifecycle is designed not to depend on that habit. Claude Code’s `SessionStart` hook asks for a brief containing active preferences, decisions, lessons, recent episodes, and open handoffs. `SessionEnd` and `PreCompact` send the transcript to the daemon, which returns quickly and extracts candidates in the background.

Session extraction is deterministic first: it looks for self-contained preferences, decisions, procedural lessons, and concrete outcomes, then uses GLiNER to score and type candidates. Up to 15 useful memories can be stored, each linked back to its session and source. A near-duplicate reinforces an active memory instead of multiplying it. A caller can explicitly supersede an old memory, and conflicting memories remain visible for the agent to resolve rather than being silently overwritten.

The `dream` operation is the consolidation pass. It merges near-duplicate memories, promotes recurring episodic information into semantic memory with provenance, decays unused memories without deleting them, and flags conflicts. It is intentionally not an LLM “reflection” loop: it reads the graph, plans deterministic changes, writes them in batches, and records a `DreamRun`.

## What the evaluation actually showed

We evaluated against a fictional Pellucid Pay company corpus: 102 AI-generated documents and 80 gold retrieval questions. The question set includes single-hop, multi-hop, temporal, ownership, and procedural cases. The gold set and world specification were kept separate from the product. Comparisons use paired bootstrap confidence intervals with 1,000 resamples and seed 0.

The honest result is not “the graph wins every retrieval metric.” For document retrieval at top 10, vector search reached Recall@10 **0.73** and FullCover@10 **0.53**. The product’s graph-routed `auto` configuration reached **0.75** and **0.59**; the `full` four-channel configuration reached **0.75** and **0.60**. Against vector + BM25 + temporal, the full configuration’s Recall@10 delta was **-0.002 [-0.031, +0.031]**, and its FullCover@10 delta was **+0.000 [-0.062, +0.062]**. The confidence intervals include zero. In other words, on this corpus, the graph ties text-oriented retrieval for finding documents.

The stronger signal appears when we stop asking whether the right document was retrieved and ask for a structured answer. In the separate 30-question graph-native evaluation, the impact/blast-radius category scored **0.80** all-keys for the tool versus **0.20** for the top-8 vector baseline: **+0.60 [+0.30, +0.90]**, statistically significant. That is the category most directly aligned with the graph’s purpose: enumerate dependents, owners to notify, customers, and incidents across multiple hops.

For current ownership, the tool and baseline both scored **1.00** all-keys, and both had correct current-owner accuracy **1.00**. That is a tie, not a claim that the graph improved the number. For value changes, the tool scored **0.80** versus the baseline’s **1.00**, a delta of **-0.20 [-0.50, +0.00]**, inside noise and lower. Overall all-keys was **0.87** versus **0.73**, a delta of **+0.13 [-0.03, +0.33]**, also inside noise.

The dedicated `who` and `timeline` checks add useful detail. For `who` with the whole question as the topic, a gold person appeared in the top three **0.82** of the time and all gold people appeared **0.71** of the time, over 17 questions. When given the gold non-person entity, those numbers were **0.94** and **0.88**. The vector-document baseline was **0.71** for any person and **0.65** for all people. For eight temporal questions with an old and new value, `timeline` listed both values **1.00**, put the old value before the new **0.88**, and placed both on dated lines **1.00**. The baseline got both values, and both values plus at least two ISO dates, **0.75**.

## Lessons and limitations

Extraction quality was the bottleneck. Relation recall improved from **0.41 to 0.83** while relation precision was **0.88**. That improvement changed the product more than another retrieval tweak: missing edges mean a graph query has nothing to traverse. The evaluation forced a similar conceptual pivot. We began with “find the right documents,” then learned that the compelling use case is “answer structurally”—show the owner path, the timeline, or the blast radius with citations.

There are important limits. This is one synthetic corpus and 80 questions written by the same team, so the results do not establish general accuracy. Relation extraction can still miss facts, leaving text channels to carry the answer. The no-LLM design means answer quality still depends on the calling agent. The current deployment is a single loopback daemon with no replication, authentication, or multi-writer scaling. BM25 indexes are rebuilt when the corpus changes, which is acceptable at demo size but not a final large-scale architecture.

Neo-Cortex is therefore not a claim that graphs replace search. The evaluation says they are comparable for document retrieval here. The claim is narrower and more useful: when the question is about ownership, change, dependencies, or consequences, explicit structure gives an agent evidence it can traverse, inspect, and explain. One FalkorDB graph lets memory, company knowledge, and reasoning share that structure instead of rebuilding it separately for every session.

**AI use disclosure:** Neo-Cortex was built with AI coding assistants. Humans directed the design, reviewed the implementation, and verified the evaluation and claims; the synthetic corpus and gold questions are fictional and AI-generated from a written specification.
