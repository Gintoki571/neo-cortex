# Real-text check: RAG and graph on this repository's docs

Generated 2026-10-18T07:56+00:00 UTC. Tenant `real`, corpus 72 files (README, AGENTS files, docs/, eval reports, demo script, Claude Code integration README, knowledge/ without references/). Gold: `eval/real_gold.jsonl`, 30 questions and 5 entity and 5 relation checks. Settings: NEO_HOME=/home/bindesh/neo-cortex/.neo/real-flags NEO_PORT=6397 NEO_DEVICE=cuda.

Matching: `AnswerIn` is a whole-word, case- and punctuation-insensitive containment of the gold answer string. `out5` = `tools.recall(k=5)` text (each item is cut to 240 chars); `chunk5` = full chunk text of the top-5 documents; `ask` = `tools.ask` output. Rank = first gold document among unique documents of `recall(k=20)` (none = not in the top 20).

Ingest: {'documents': 72, 'skipped': 0, 'chunks': 423, 'mentions': 1166, 'rels': 5, 'errors': 0, 'unsupported': 0, 'new_entities': 594, 'seconds': 307.7}

## a. RAG

### Summary (overall and per type)

| group | n | Hit@1 | Hit@5 | MRR | AnswerIn@5 out5 | AnswerIn chunk5 | AnswerIn ask |
|---|---|---|---|---|---|---|---|
| overall | 30 | 0.27 | 0.50 | 0.41 | 0.43 | 0.70 | 0.47 |
| fact | 8 | 0.00 | 0.12 | 0.10 | 0.38 | 0.62 | 0.25 |
| why | 6 | 0.33 | 0.67 | 0.52 | 0.33 | 0.67 | 0.33 |
| how | 6 | 0.83 | 0.83 | 0.85 | 0.50 | 0.83 | 0.50 |
| number | 5 | 0.20 | 0.60 | 0.37 | 0.40 | 0.80 | 0.60 |
| where | 5 | 0.00 | 0.40 | 0.28 | 0.60 | 0.60 | 0.80 |

### Latency (ms)

| call | p50 | p95 | mean |
|---|---|---|---|
| recall k=20 | 133 | 192 | 144 |
| ask | 193 | 285 | 203 |

### Per question

| id | type | rank | out5 | chunk5 | ask | ms recall | ms ask | gold | question |
|---|---|---|---|---|---|---|---|---|---|
| Q01 | fact | 6 | 1.0 | 1.0 | 1.0 | 320 | 166 | README.md | Which model turns the text into vectors for the similarity search? |
| Q02 | fact | 9 | 0.0 | 1.0 | 0.0 | 99 | 167 | README.md | What model pulls entities and their types out of documents without calling a language model? |
| Q03 | fact | none | 0.0 | 0.0 | 0.0 | 131 | 191 | README.md | Which library runs the keyword side of search inside the Python process? |
| Q04 | fact | none | 0.0 | 0.0 | 0.0 | 127 | 184 | docs/architecture.md | When a newer document names a different owner for something, what happens to the old owner edge? |
| Q05 | fact | 5 | 0.0 | 1.0 | 0.0 | 160 | 285 | README.md | If I supersede a memory, is the old one removed from the database? |
| Q06 | fact | 6 | 0.0 | 0.0 | 0.0 | 192 | 245 | integrations/claude-code/README.md | If the daemon is not running, does a Claude Code hook make the session fail? |
| Q07 | fact | 11 | 1.0 | 1.0 | 1.0 | 97 | 166 | README.md | Which graph procedure builds the shortest bridging paths that connect and ask return? |
| Q08 | fact | 10 | 1.0 | 1.0 | 0.0 | 123 | 183 | README.md | What is the exact Hugging Face id of the GLiNER checkpoint the project loads? |
| Q09 | why | 1 | 0.0 | 1.0 | 0.0 | 155 | 214 | README.md | Why does Neo-Cortex leave answer writing to the calling agent instead of generating answers itself? |
| Q10 | why | none | 0.0 | 0.0 | 0.0 | 161 | 219 | AGENTS.md | Why did the team take graphrag-sdk out of the core? |
| Q11 | why | 1 | 0.0 | 1.0 | 0.0 | 189 | 245 | README.md | Why does the graph-routed retrieval not improve on plain vector plus BM25 for finding documents? |
| Q12 | why | 8 | 0.0 | 0.0 | 0.0 | 159 | 218 | src/neo_cortex/AGENTS.md | Why does the embedded FalkorDB server get an explicit bind address instead of the library default? |
| Q13 | why | 2 | 1.0 | 1.0 | 1.0 | 164 | 287 | knowledge/architecture/build-status.md | Why was the tuned retrieval weight set left out of the shipped product? |
| Q14 | why | 2 | 1.0 | 1.0 | 1.0 | 138 | 195 | README.md | Why is there a single REL edge type with a type property rather than one Neo4j-style relationship type per relation? |
| Q15 | how | 1 | 1.0 | 1.0 | 1.0 | 155 | 215 | README.md | What command starts the daemon so MCP clients and hooks can reach it on port 8765? |
| Q16 | how | 9 | 0.0 | 0.0 | 0.0 | 153 | 214 | integrations/claude-code/README.md | What command registers the Neo-Cortex MCP endpoint with Claude Code at user scope? |
| Q17 | how | 1 | 1.0 | 1.0 | 1.0 | 167 | 226 | README.md | How do I load a folder of synthetic documents into the graph and block until the job is done? |
| Q18 | how | 1 | 1.0 | 1.0 | 1.0 | 155 | 216 | eval/README.md | My GPU keeps running out of memory during the eval. How do I force the eval onto the CPU? |
| Q19 | how | 1 | 0.0 | 1.0 | 0.0 | 130 | 224 | eval/README.md | How do I throw away the eval tenant and re-ingest the corpus from zero? |
| Q20 | how | 1 | 0.0 | 1.0 | 0.0 | 189 | 248 | eval/stress.md | Which script do I run to hammer the daemon with concurrent clients and count lost writes? |
| Q21 | number | 4 | 1.0 | 1.0 | 1.0 | 124 | 178 | README.md | How many gold questions does the retrieval evaluation use? |
| Q22 | number | 3 | 1.0 | 1.0 | 1.0 | 100 | 160 | README.md | At what cosine similarity does a new memory count as a repeat and reinforce the stored one? |
| Q23 | number | 8 | 0.0 | 0.0 | 0.0 | 100 | 159 | README.md | What is the most memories one finished session can add? |
| Q24 | number | 8 | 0.0 | 1.0 | 1.0 | 129 | 230 | README.md | How large can the local subgraph for the graph channel get, in nodes? |
| Q25 | number | 1 | 0.0 | 1.0 | 0.0 | 97 | 162 | eval/stress.md | What was the read p95 latency in milliseconds with 16 clients hitting the daemon? |
| Q26 | where | 9 | 0.0 | 0.0 | 0.0 | 124 | 182 | README.md | Which file lists every Cypher query the product issues and the function that runs it? |
| Q27 | where | 6 | 0.0 | 0.0 | 1.0 | 128 | 187 | AGENTS.md | Where is the binding graph data model contract for the Python package written down? |
| Q28 | where | 7 | 1.0 | 1.0 | 1.0 | 99 | 160 | knowledge/architecture/build-status.md | Which module runs the Personalized PageRank over the local subgraph? |
| Q29 | where | 2 | 1.0 | 1.0 | 1.0 | 127 | 186 | README.md | Which file is the answer key the synthetic company corpus was generated from, and what must never be ingested? |
| Q30 | where | 2 | 1.0 | 1.0 | 1.0 | 134 | 189 | README.md | Where do I find the saved numbers from the graph-native answers evaluation? |

### Five worst questions: which documents beat the gold one

- **Q03** (fact, rank none, answer `bm25s`): Which library runs the keyword side of search inside the Python process? Gold `README.md`. Above it: `knowledge/falkordblite/overview.md` via vector#20, bm25#1, graph#2; `knowledge/falkordblite/python-api.md` via vector#11, bm25#3, graph#8; `knowledge/extraction/langextract.md` via vector#5, bm25#15, graph#4.
- **Q04** (fact, rank none, answer `end their old edge`): When a newer document names a different owner for something, what happens to the old owner edge? Gold `docs/architecture.md`. Above it: `demo/SCRIPT.md` via vector#1, bm25#18, graph#3; `src/neo_cortex/AGENTS.md` via vector#10, bm25#4, graph#6; `docs/blog.md` via vector#23, bm25#1, graph#21.
- **Q10** (why, rank none, answer `user decision 2026-10-16`): Why did the team take graphrag-sdk out of the core? Gold `AGENTS.md`. Above it: `knowledge/architecture/unified-plan.md` via vector#8, bm25#1, graph#1; `knowledge/graphrag-sdk/overview.md` via vector#4, bm25#6, graph#8; `knowledge/architecture/project-plan.md` via vector#3, bm25#11, graph#11.
- **Q07** (fact, rank 11, answer `algo.SPpaths`): Which graph procedure builds the shortest bridging paths that connect and ask return? Gold `README.md`. Above it: `docs/cypher.md` via vector#4, bm25#4; `knowledge/falkordb/algorithms-and-weighted-paths.md` via vector#1, bm25#13; `knowledge/hackathon/blog-agent-reasons-over-graph.md` via vector#2, bm25#14.
- **Q08** (fact, rank 10, answer `fastino/gliner2.5-base-v1`): What is the exact Hugging Face id of the GLiNER checkpoint the project loads? Gold `README.md`. Above it: `src/neo_cortex/AGENTS.md` via vector#7, bm25#6, graph#1; `knowledge/models/gliner2-family-and-paper.md` via vector#8, bm25#10, graph#2; `knowledge/graphrag-sdk/pluggability.md` via vector#30, bm25#1, graph#5.

## b. Graph health

### Counts

- Documents by kind: {'doc': 72}
- Documents by doc_type (frontmatter `type`): {'(none)': 25, 'DOX Contract': 1, 'Status Report': 1, 'Design Proposal': 6, 'Research Finding': 2, 'Test Report': 1, 'TestReport': 1, 'Tool': 2, 'Design': 1, 'Research Note': 1, 'Concept': 14, 'Test Result': 1, 'Risk Register': 1, 'Reference': 7, 'Hackathon Prizes': 1, 'Hackathon': 1, 'Hackathon Rules': 1, 'Checklist': 1, 'Model': 2, 'Claim Check': 1, 'Comparison': 1}
- Chunks: 423; MENTIONS: 1166; Entities: 594
- Entities by type: {'service': 48, 'file': 202, 'tool': 59, 'customer': 10, 'person': 43, 'component': 47, 'product': 38, 'config_setting': 79, 'ticket': 24, 'decision': 7, 'team': 26, 'incident': 5, 'other': 6}
- REL edges by type: {'DECIDED': 1, 'OWNS': 1, 'DEPENDS_ON': 3}

- Single-word entity names: 154; generic single words (`is_generic`): 0: (none)
- Entities typed `file`: 202: /architecture/build-status.md, /architecture/classification-usecases.md, /architecture/index.md, /architecture/inspiration-rrsi.md, /architecture/project-plan.md, /architecture/unified-plan.md, /extraction/anydoc.md, /extraction/index.md, /extraction/langextract.md, /extraction/system1-adoption.md, /falkordb/cypher-support.md, /falkordb/index.md, /falkordb/overview.md, /falkordb/python-client.md, /falkordblite/index.md, /graphrag-sdk/architecture.md, /graphrag-sdk/index.md, /hackathon/index.md, /models/embeddinggemma.md, /models/index.md, /okf/index.md, /tables/customers.md, AGENTS.md, Cargo.toml, README.md, Root AGENTS.md, SCRIPT.md, SPEC.md, WORLD.md, annotation.py, anydoc-test-results.md, api-connection-probe.py, api/main.py, attesters/index.md, attesters/sql_equality.py, auth/login_test.py, build-status.md, bundle/document.py, bundle/index.py, bundle/paths.py

### Name variants per stem (10 biggest groups)

A stem is each letter run of 4+ and the letters-only key; a group is every entity key that contains the stem.

| stem | variant keys | examples (mentions) |
|---|---|---|
| eval | 13 | eval results md (12), eval real check md (6), eval graph quality py (5), eval readme md (4), eval answers md (4), eval graph quality md (4) |
| falkordb | 13 | falkordb (36), falkordb cypher support md (4), falkordb cloud (3), falkordb py (3), neo falkordb url (1), falkordb url (1) |
| index | 12 | extraction index md (6), index md (5), models index md (5), architecture index md (2), okf index md (2), hackathon index md (1) |
| algo | 11 | algo sppaths (8), algo sspaths (4), algo astar (1), algo pagerank (1), algo bfs (1), algo wcc (1) |
| langextract | 11 | langextract (9), langextract pipeline (3), langextract extraction py (3), langextract core data py (3), langextract annotation py (2), langextract resolver py (2) |
| test | 11 | tests test dream py (2), tests test write py (2), anydoc test results md (1), auth login test py (1), tests test resolve py (1), capabilities test md (1) |
| readme | 10 | readme md (5), eval readme md (4), github readme main md (4), okf readme md (4), okfrepo readme md (2), src provider readme (1) |
| tests | 10 | tests (3), tests test dream py (2), tests test write py (2), tests test resolve py (1), tests conftest py (1), tests test isolation py (1) |
| architecture | 9 | architecture project plan md (4), architecture build status md (3), architecture index md (2), architecture unified plan md (2), docs architecture md (1), architecture classification usecases md (1) |
| graph | 9 | eval graph quality py (5), eval graph quality md (4), graph store (2), channels graph (1), graph rag (1), graph query (1) |

### Entity checks

| id | entity | expected types | found (name, type, mentions) | pass |
|---|---|---|---|---|
| E01 | FalkorDB | product/tool/service | FalkorDB (service, 36) | PASS |
| E02 | EmbeddingGemma | tool/product/component | EmbeddingGemma (tool, 5) | PASS |
| E03 | GLiNER2.5 | tool/product/component | GLiNER2.5 (tool, 14) | PASS |
| E04 | bm25s | tool/product/component | not found | FAIL |
| E05 | retrieve/channels.py | file/component | retrieve/channels.py (file, 7) | PASS |

### Relation checks

| id | head -REL->tail | edge found | reversed | head/tail in graph | other REL edges from head |
|---|---|---|---|---|---|
| R01 | Neo-Cortex -DEPENDS_ON-> algo.SPpaths | FAIL | no | yes / yes | - |
| R02 | Claude Code hooks -DEPENDS_ON-> daemon | FAIL | no | yes / no | - |
| R03 | k-hop expansion -REPLACED_BY-> Personalized PageRank | FAIL | no | no / no | - |
| R04 | user -DECIDED-> graphrag-sdk | FAIL | no | no / yes | - |
| R05 | daemon -OWNS-> graph | FAIL | no | no / no | - |

### Random REL edges for human judgement (random seed 0)

1. `SDK` -DEPENDS_ON-> `FalkorDB` (conf 0.0718, chunk `doc_c2072f0c03fd0116#0` in `knowledge/graphrag-sdk/db-connectivity.md`): "How graphrag-sdk 1.4.0 builds its FalkorDB client, which injection points exist, whether falkordblite (embedded FalkorDB) works with it (verified two ways), vec"
2. `SDK` -DEPENDS_ON-> `GraphRAG` (conf 0.9, chunk `doc_c2072f0c03fd0116#0` in `knowledge/graphrag-sdk/db-connectivity.md`): "How graphrag-sdk 1.4.0 builds its FalkorDB client, which injection points exist, whether falkordblite (embedded FalkorDB) works with it (verified two ways), vec"
3. `Elif Yildiz` -OWNS-> `ledger-service` (conf 0.9, chunk `doc_f78fd6600c2d34aa#4` in `demo/SCRIPT.md`): "```bash neo ask "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?" ``` ``` ## Seeds (linked entitie"
4. `FalkorDB` -DEPENDS_ON-> `Redis` (conf 0.9, chunk `doc_0a26f86f36a0f1aa#1` in `knowledge/falkordb/overview.md`): "Practical reading for a GraphRAG project: traversals are matrix multiplications, so multi-hop patterns and graph algorithms are fast, but everything is held in "
5. `Lukas Brandt` -DECIDED-> `ADR-006` (conf 0.7918, chunk `doc_f78fd6600c2d34aa#1` in `demo/SCRIPT.md`): "Say: "This is a company's tickets, ADRs, chats and agent sessions in one FalkorDB graph. Three questions an agent cannot answer from files: who owns it now, wha"

## Corpus files

- `AGENTS.md`
- `README.md`
- `demo/SCRIPT.md`
- `docs/architecture.md`
- `docs/blog.md`
- `docs/cypher.md`
- `docs/judges-guide.md`
- `docs/lineage.md`
- `docs/neo-for-agents.md`
- `eval/README.md`
- `eval/answers.md`
- `eval/results.md`
- `eval/stress.md`
- `integrations/claude-code/README.md`
- `knowledge/AGENTS.md`
- `knowledge/architecture/build-status.md`
- `knowledge/architecture/classification-usecases.md`
- `knowledge/architecture/index.md`
- `knowledge/architecture/inspiration-dream-rsi.md`
- `knowledge/architecture/inspiration-pg-jev.md`
- `knowledge/architecture/inspiration-rrsi.md`
- `knowledge/architecture/project-plan.md`
- `knowledge/architecture/spike-2026-10-16.md`
- `knowledge/architecture/unified-plan.md`
- `knowledge/extraction/anydoc-test-results.md`
- `knowledge/extraction/anydoc.md`
- `knowledge/extraction/index.md`
- `knowledge/extraction/langextract-pipeline-design.md`
- `knowledge/extraction/langextract.md`
- `knowledge/extraction/system1-adoption.md`
- `knowledge/extraction/system1-models-in-graphs.md`
- `knowledge/falkordb/algorithms-and-weighted-paths.md`
- `knowledge/falkordb/cypher-support.md`
- `knowledge/falkordb/data-model-and-constraints.md`
- `knowledge/falkordb/docs-site-map.md`
- `knowledge/falkordb/index.md`
- `knowledge/falkordb/indexing-and-vectors.md`
- `knowledge/falkordb/limits-and-performance.md`
- `knowledge/falkordb/overview.md`
- `knowledge/falkordb/python-client.md`
- `knowledge/falkordblite/capabilities-test.md`
- `knowledge/falkordblite/index.md`
- `knowledge/falkordblite/limitations-and-open-issues.md`
- `knowledge/falkordblite/overview.md`
- `knowledge/falkordblite/python-api.md`
- `knowledge/graphrag-sdk/architecture.md`
- `knowledge/graphrag-sdk/db-connectivity.md`
- `knowledge/graphrag-sdk/docs-site-map.md`
- `knowledge/graphrag-sdk/index.md`
- `knowledge/graphrag-sdk/overview.md`
- `knowledge/graphrag-sdk/pluggability.md`
- `knowledge/graphrag-sdk/retrieval-strategies.md`
- `knowledge/hackathon/blog-agent-reasons-over-graph.md`
- `knowledge/hackathon/index.md`
- `knowledge/hackathon/judging-and-prizes.md`
- `knowledge/hackathon/overview.md`
- `knowledge/hackathon/rules.md`
- `knowledge/hackathon/submission-checklist.md`
- `knowledge/index.md`
- `knowledge/log.md`
- `knowledge/models/embeddinggemma.md`
- `knowledge/models/gliner2-5-base.md`
- `knowledge/models/gliner2-family-and-paper.md`
- `knowledge/models/index.md`
- `knowledge/models/jev-typesafe-claim-check.md`
- `knowledge/models/system1-classifier-candidates.md`
- `knowledge/okf/index.md`
- `knowledge/okf/mapping-to-graph.md`
- `knowledge/okf/overview.md`
- `knowledge/okf/spec-cheatsheet.md`
- `knowledge/okf/tooling-and-examples.md`
- `src/neo_cortex/AGENTS.md`
