# Submission form answers (paste-ready)

**Description: What problem does your project solve, and who is it for?**
AI agents forget everything between sessions, and a company's knowledge is scattered across documents, tickets, chats and meeting notes, so nobody (human or agent) can answer "who owns this now, what changed, and what breaks if it stops?" from a search box. Neo-Cortex puts all of it in one FalkorDB graph that is an agent's long-term memory, a company brain built from documents, and a way to answer multi-step questions. It is for developers building coding or workflow agents and for teams that want their agents to share and keep knowledge. Agents use it through 15 MCP tools or a small `neo` command line. There is no large language model inside: two small local models (GLiNER2.5 and EmbeddingGemma) do extraction and embeddings, so there is no per-question cost and data stays on the machine.

**How did you use FalkorDB in your project?**
FalkorDB is the only database: one graph per team, embedded (falkordblite) or in Docker. Documents, chunks, entities, memories, sessions and agents are nodes; ownership, dependency and supersession are dated edges. We use vector indexes (cosine, 768-d) for search by meaning; `algo.SPpaths` for the shortest bridging paths between two entities; variable-length paths for "who owns or knows this" and "what breaks if this stops"; time on edges (`valid_from_ms`/`valid_to_ms`) so a new owner closes the old edge and history stays queryable; `GRAPH.RO_QUERY` for the agent's read-only Cypher tool; and audit nodes in the same graph (cached model verdicts, memory tidy-up logs, tuning trials). Queries are listed in the README and docs/cypher.md.

**Tell us what technical problems you solved using FalkorDB**
(1) Blast radius: "what breaks if this service stops, and who should be told" is a graph walk over DEPENDS_ON edges; measured 0.80 vs 0.20 for plain text search (30 questions). (2) Current vs former owners: edges carry validity dates, so supersession is a graph update, not a text guess. (3) Bridging two things no single document links, using shortest paths. (4) One store for memory, documents and reasoning, with four searches (words, meaning, graph, time) merged by rank fusion. (5) Safe extraction: every extracted relation carries a fact/maybe/denial/plan verdict and probability, so a denied sentence never becomes a fact. (6) Concurrency: 16 clients at once, no errors, no lost writes (read median about 10 ms).

**What did you like about FalkorDB?**
The embedded falkordblite option: zero setup, one file, the same Cypher as the server, so a judge can run the project in minutes. Having vector indexes, shortest-path algorithms, variable-length paths and read-only queries in one engine meant no second database. It was fast enough for 16 concurrent clients, and the FalkorDB Browser makes the graph easy to show and understand.

**What improvements would you like to see in FalkorDB?**
(1) A personalized `algo.pageRank` (restart vector); we computed it in numpy over a fetched subgraph. (2) A real BM25 option in the full-text index; we kept a separate BM25 index. (3) falkordblite: cleaner shutdown (we saw orphaned server processes) and a correct package version (reports 0.0.0). (4) Clearer docs for vector query results (distance, smaller is nearer) and the output shape of `algo.SPpaths`. (5) Clear license metadata on the main repository (GitHub's API reports NOASSERTION).

**Blog link**
https://github.com/Gintoki571/neo-cortex/blob/master/docs/blog.md  (works after the push)

**Other fields (if asked)**
- Repo: https://github.com/Gintoki571/neo-cortex
- Tracks: all three: 01 Agents that act on connected data, 02 Agent memory and coordination, 03 Company brain
- Team: bindesh (solo)
- AI use: built with Claude Code and other AI coding agents; directed, reviewed and verified by the author; the system itself contains no large language model.
