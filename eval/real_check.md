# Real-text check: RAG and graph on this repository's docs

Generated 2026-10-17T10:04+00:00 UTC. Tenant `real`, corpus 69 files (README, AGENTS files, docs/, eval reports, demo script, Claude Code integration README, knowledge/ without references/). Gold: `eval/real_gold.jsonl`, 30 questions and 5 entity and 5 relation checks. Settings: NEO_HOME=/tmp/claude-1000/integ2/real NEO_PORT=6442 NEO_DEVICE=auto.

Matching: `AnswerIn` is a whole-word, case- and punctuation-insensitive containment of the gold answer string. `out5` = `tools.recall(k=5)` text (each item is cut to 240 chars); `chunk5` = full chunk text of the top-5 documents; `ask` = `tools.ask` output. Rank = first gold document among unique documents of `recall(k=20)` (none = not in the top 20).

Ingest: {'documents': 69, 'skipped': 0, 'chunks': 388, 'mentions': 1048, 'rels': 12, 'errors': 0, 'unsupported': 0, 'new_entities': 550, 'seconds': 381.4}

## a. RAG

### Summary (overall and per type)

| group | n | Hit@1 | Hit@5 | MRR | AnswerIn@5 out5 | AnswerIn chunk5 | AnswerIn ask |
|---|---|---|---|---|---|---|---|
| overall | 30 | 0.23 | 0.53 | 0.39 | 0.47 | 0.73 | 0.47 |
| fact | 8 | 0.00 | 0.12 | 0.14 | 0.38 | 0.75 | 0.38 |
| why | 6 | 0.17 | 0.67 | 0.38 | 0.50 | 0.67 | 0.50 |
| how | 6 | 0.83 | 0.83 | 0.86 | 0.33 | 0.83 | 0.33 |
| number | 5 | 0.20 | 0.80 | 0.37 | 0.60 | 0.80 | 0.60 |
| where | 5 | 0.00 | 0.40 | 0.28 | 0.60 | 0.60 | 0.60 |

### Latency (ms)

| call | p50 | p95 | mean |
|---|---|---|---|
| recall k=20 | 373 | 426 | 366 |
| ask | 651 | 729 | 646 |

### Per question

| id | type | rank | out5 | chunk5 | ask | ms recall | ms ask | gold | question |
|---|---|---|---|---|---|---|---|---|---|
| Q01 | fact | 6 | 1.0 | 1.0 | 1.0 | 426 | 581 | README.md | Which model turns the text into vectors for the similarity search? |
| Q02 | fact | none | 0.0 | 1.0 | 0.0 | 325 | 592 | README.md | What model pulls entities and their types out of documents without calling a language model? |
| Q03 | fact | 9 | 0.0 | 1.0 | 0.0 | 350 | 622 | README.md | Which library runs the keyword side of search inside the Python process? |
| Q04 | fact | none | 0.0 | 0.0 | 0.0 | 349 | 615 | docs/architecture.md | When a newer document names a different owner for something, what happens to the old owner edge? |
| Q05 | fact | 2 | 0.0 | 1.0 | 0.0 | 381 | 712 | README.md | If I supersede a memory, is the old one removed from the database? |
| Q06 | fact | 6 | 0.0 | 0.0 | 0.0 | 408 | 707 | integrations/claude-code/README.md | If the daemon is not running, does a Claude Code hook make the session fail? |
| Q07 | fact | 6 | 1.0 | 1.0 | 1.0 | 316 | 597 | README.md | Which graph procedure builds the shortest bridging paths that connect and ask return? |
| Q08 | fact | none | 1.0 | 1.0 | 1.0 | 344 | 618 | README.md | What is the exact Hugging Face id of the GLiNER checkpoint the project loads? |
| Q09 | why | 1 | 0.0 | 1.0 | 0.0 | 395 | 662 | README.md | Why does Neo-Cortex leave answer writing to the calling agent instead of generating answers itself? |
| Q10 | why | 7 | 0.0 | 0.0 | 0.0 | 380 | 666 | AGENTS.md | Why did the team take graphrag-sdk out of the core? |
| Q11 | why | 4 | 0.0 | 0.0 | 0.0 | 427 | 696 | README.md | Why does the graph-routed retrieval not improve on plain vector plus BM25 for finding documents? |
| Q12 | why | 4 | 1.0 | 1.0 | 1.0 | 389 | 663 | src/neo_cortex/AGENTS.md | Why does the embedded FalkorDB server get an explicit bind address instead of the library default? |
| Q13 | why | 2 | 1.0 | 1.0 | 1.0 | 386 | 730 | knowledge/architecture/build-status.md | Why was the tuned retrieval weight set left out of the shipped product? |
| Q14 | why | 8 | 1.0 | 1.0 | 1.0 | 374 | 666 | README.md | Why is there a single REL edge type with a type property rather than one Neo4j-style relationship type per relation? |
| Q15 | how | 1 | 0.0 | 1.0 | 0.0 | 405 | 691 | README.md | What command starts the daemon so MCP clients and hooks can reach it on port 8765? |
| Q16 | how | 7 | 0.0 | 0.0 | 0.0 | 382 | 649 | integrations/claude-code/README.md | What command registers the Neo-Cortex MCP endpoint with Claude Code at user scope? |
| Q17 | how | 1 | 1.0 | 1.0 | 1.0 | 377 | 659 | README.md | How do I load a folder of synthetic documents into the graph and block until the job is done? |
| Q18 | how | 1 | 1.0 | 1.0 | 1.0 | 402 | 673 | eval/README.md | My GPU keeps running out of memory during the eval. How do I force the eval onto the CPU? |
| Q19 | how | 1 | 0.0 | 1.0 | 0.0 | 350 | 671 | eval/README.md | How do I throw away the eval tenant and re-ingest the corpus from zero? |
| Q20 | how | 1 | 0.0 | 1.0 | 0.0 | 387 | 729 | eval/stress.md | Which script do I run to hammer the daemon with concurrent clients and count lost writes? |
| Q21 | number | 4 | 1.0 | 1.0 | 1.0 | 343 | 607 | README.md | How many gold questions does the retrieval evaluation use? |
| Q22 | number | 4 | 1.0 | 1.0 | 1.0 | 314 | 605 | README.md | At what cosine similarity does a new memory count as a repeat and reinforce the stored one? |
| Q23 | number | 6 | 0.0 | 0.0 | 0.0 | 321 | 583 | README.md | What is the most memories one finished session can add? |
| Q24 | number | 5 | 1.0 | 1.0 | 1.0 | 394 | 665 | README.md | How large can the local subgraph for the graph channel get, in nodes? |
| Q25 | number | 1 | 0.0 | 1.0 | 0.0 | 313 | 612 | eval/stress.md | What was the read p95 latency in milliseconds with 16 clients hitting the daemon? |
| Q26 | where | 11 | 0.0 | 0.0 | 0.0 | 351 | 616 | README.md | Which file lists every Cypher query the product issues and the function that runs it? |
| Q27 | where | 7 | 0.0 | 0.0 | 0.0 | 347 | 623 | AGENTS.md | Where is the binding graph data model contract for the Python package written down? |
| Q28 | where | 7 | 1.0 | 1.0 | 1.0 | 312 | 588 | knowledge/architecture/build-status.md | Which module runs the Personalized PageRank over the local subgraph? |
| Q29 | where | 2 | 1.0 | 1.0 | 1.0 | 373 | 652 | README.md | Which file is the answer key the synthetic company corpus was generated from, and what must never be ingested? |
| Q30 | where | 2 | 1.0 | 1.0 | 1.0 | 356 | 630 | README.md | Where do I find the saved numbers from the graph-native answers evaluation? |

### Five worst questions: which documents beat the gold one

- **Q04** (fact, rank none, answer `end their old edge`): When a newer document names a different owner for something, what happens to the old owner edge? Gold `docs/architecture.md`. Above it: `src/neo_cortex/AGENTS.md` via vector#2, bm25#1, graph#2; `demo/SCRIPT.md` via vector#1, bm25#12, graph#3; `AGENTS.md` via vector#3, bm25#14, graph#4.
- **Q02** (fact, rank none, answer `GLiNER2.5`): What model pulls entities and their types out of documents without calling a language model? Gold `README.md`. Above it: `knowledge/graphrag-sdk/pluggability.md` via vector#2, bm25#3; `knowledge/extraction/langextract-pipeline-design.md` via vector#4, bm25#7; `src/neo_cortex/AGENTS.md` via vector#1, bm25#34.
- **Q08** (fact, rank none, answer `fastino/gliner2.5-base-v1`): What is the exact Hugging Face id of the GLiNER checkpoint the project loads? Gold `README.md`. Above it: `knowledge/models/gliner2-family-and-paper.md` via vector#7, bm25#9, graph#1; `knowledge/graphrag-sdk/pluggability.md` via vector#22, bm25#1, graph#2; `knowledge/models/gliner2-5-base.md` via vector#8, bm25#13, graph#5.
- **Q26** (where, rank 11, answer `docs/cypher.md`): Which file lists every Cypher query the product issues and the function that runs it? Gold `README.md`. Above it: `knowledge/falkordb/cypher-support.md` via vector#26, bm25#4, graph#1; `knowledge/falkordb/indexing-and-vectors.md` via vector#33, bm25#1, graph#5; `knowledge/architecture/inspiration-pg-jev.md` via vector#9, bm25#17, graph#11.
- **Q03** (fact, rank 9, answer `bm25s`): Which library runs the keyword side of search inside the Python process? Gold `README.md`. Above it: `knowledge/falkordblite/overview.md` via vector#20, bm25#1, graph#2; `knowledge/falkordblite/python-api.md` via vector#14, bm25#3, graph#7; `knowledge/extraction/langextract.md` via vector#9, bm25#16, graph#3.

## b. Graph health

### Counts

- Documents by kind: {'doc': 69}
- Documents by doc_type (frontmatter `type`): {'(none)': 22, 'DOX Contract': 1, 'Status Report': 1, 'Design Proposal': 6, 'Research Finding': 2, 'Test Report': 1, 'TestReport': 1, 'Tool': 2, 'Design': 1, 'Research Note': 1, 'Concept': 14, 'Test Result': 1, 'Risk Register': 1, 'Reference': 7, 'Hackathon Prizes': 1, 'Hackathon': 1, 'Hackathon Rules': 1, 'Checklist': 1, 'Model': 2, 'Claim Check': 1, 'Comparison': 1}
- Chunks: 388; MENTIONS: 1048; Entities: 550
- Entities by type: {'service': 44, 'file': 202, 'tool': 54, 'product': 40, 'customer': 10, 'person': 44, 'config_setting': 57, 'component': 32, 'ticket': 25, 'decision': 8, 'team': 22, 'incident': 5, 'other': 7}
- REL edges by type: {'DECIDED': 2, 'DEPENDS_ON': 5, 'OWNS': 5}

- Single-word entity names: 149; generic single words (`is_generic`): 0: (none)
- Entities typed `file`: 202: /architecture/build-status.md, /architecture/classification-usecases.md, /architecture/inspiration-rrsi.md, /architecture/project-plan.md, /architecture/unified-plan.md, /extraction/anydoc.md, /extraction/langextract.md, /falkordb/cypher-support.md, /falkordb/index.md, /falkordb/overview.md, /falkordb/python-client.md, /falkordblite/index.md, /graphrag-sdk/architecture.md, /graphrag-sdk/index.md, /hackathon/index.md, /hackathon/submission-checklist.md, /models/embeddinggemma.md, /models/index.md, /okf/index.md, /okf/spec-cheatsheet.md, /providers/router.py, /tables/customers.md, AGENTS.md, Cargo.toml, README.md, Root AGENTS.md, SCRIPT.md, WORLD.md, annotation.py, api-connection-probe.py, api/main.py, attesters/index.md, attesters/sql_equality.py, auth/login_test.py, build-status.md, bundle/document.py, bundle/index.py, bundle/paths.py, bundle/synthesizer.py, capabilities-probe.py

### Name variants per stem (10 biggest groups)

A stem is each letter run of 4+ and the letters-only key; a group is every entity key that contains the stem.

| stem | variant keys | examples (mentions) |
|---|---|---|
| langextract | 14 | langextract (9), langextract pipeline (3), langextract core data py (3), langextract extraction py (2), langextract annotation py (2), langextract resolver py (2) |
| falkordb | 13 | falkordb (34), falkordb cypher support md (4), falkordb cloud (3), falkordb python client md (3), falkordb py (3), neo falkordb url (1) |
| eval | 12 | eval results md (7), eval readme md (4), eval answers md (3), eval graph quality md (3), eval graph quality py (2), eval tune py (2) |
| index | 11 | index md (5), extraction index md (4), models index md (3), hackathon index md (1), falkordblite index md (1), falkordb index md (1) |
| readme | 10 | eval readme md (4), readme md (4), github readme main md (4), okf readme md (4), okfrepo readme md (2), langextract providers readme md (1) |
| test | 10 | tests test write py (2), auth login test py (1), tests test resolve py (1), capabilities test md (1), test bigquery source py (1), tests test dream py (1) |
| tests | 10 | tests (3), tests test write py (2), tests test resolve py (1), tests test dream py (1), tests conftest py (1), tests test isolation py (1) |
| probe | 9 | sspaths rowcount probe py (2), capabilities probe py (1), listen probe py (1), orphan server probe py (1), timing probe py (1), constraints probe py (1) |
| python | 9 | requires python (3), python client md (3), falkordb python client md (3), python pyproject toml (2), python (1), python client (1) |
| architecture | 8 | architecture project plan md (3), architecture build status md (3), docs architecture md (1), graphrag sdk architecture md (1), architecture unified plan md (1), architecture inspiration rrsi md (1) |

### Entity checks

| id | entity | expected types | found (name, type, mentions) | pass |
|---|---|---|---|---|
| E01 | FalkorDB | product/tool/service | FalkorDB (service, 34) | PASS |
| E02 | EmbeddingGemma | tool/product/component | EmbeddingGemma (tool, 5) | PASS |
| E03 | GLiNER2.5 | tool/product/component | GLiNER2.5 (product, 9) | PASS |
| E04 | bm25s | tool/product/component | not found | FAIL |
| E05 | retrieve/channels.py | file/component | retrieve/channels.py (file, 6) | PASS |

### Relation checks

| id | head -REL->tail | edge found | reversed | head/tail in graph | other REL edges from head |
|---|---|---|---|---|---|
| R01 | Neo-Cortex -DEPENDS_ON-> algo.SPpaths | FAIL | no | yes / no | - |
| R02 | Claude Code hooks -DEPENDS_ON-> daemon | FAIL | no | yes / no | - |
| R03 | k-hop expansion -REPLACED_BY-> Personalized PageRank | FAIL | no | no / no | - |
| R04 | user -DECIDED-> graphrag-sdk | FAIL | no | no / yes | - |
| R05 | daemon -OWNS-> graph | FAIL | no | no / no | - |

### Random REL edges for human judgement (random seed 0)

1. `Olivia Hartmann` -OWNS-> `reporting-service` (conf 0.8289, chunk `doc_f78fd6600c2d34aa#5` in `demo/SCRIPT.md`): "```bash neo impact ledger-service ``` ``` # impact [ent_e008439ebc28] ledger-service (service): 3 depend on it, it needs 1 (DEPENDS_ON, current, max_hops 3; A -"
2. `topic` -DEPENDS_ON-> `broker` (conf 0.9, chunk `doc_4b98794861b249bd#7` in `src/neo_cortex/AGENTS.md`): "Relations are extracted per sentence window (up to 40 words) instead of per chunk, from GLiNER (floors above; OWNS/MEMBER_OF only from a sentence that asserts i"
3. `Daniel Kwon` -OWNS-> `payment-gateway` (conf 0.9349, chunk `doc_f78fd6600c2d34aa#5` in `demo/SCRIPT.md`): "```bash neo impact ledger-service ``` ``` # impact [ent_e008439ebc28] ledger-service (service): 3 depend on it, it needs 1 (DEPENDS_ON, current, max_hops 3; A -"
4. `Lukas Brandt` -DECIDED-> `ADR-006` (conf 0.7918, chunk `doc_f78fd6600c2d34aa#1` in `demo/SCRIPT.md`): "Say: "This is a company's tickets, ADRs, chats and agent sessions in one FalkorDB graph. Three questions an agent cannot answer from files: who owns it now, wha"
5. `SDK` -DEPENDS_ON-> `FalkorDB` (conf 0.9, chunk `doc_c2072f0c03fd0116#0` in `knowledge/graphrag-sdk/db-connectivity.md`): "How graphrag-sdk 1.4.0 builds its FalkorDB client, which injection points exist, whether falkordblite (embedded FalkorDB) works with it (verified two ways), vec"
6. `FalkorDB` -DEPENDS_ON-> `Redis` (conf 0.9, chunk `doc_0a26f86f36a0f1aa#1` in `knowledge/falkordb/overview.md`): "Practical reading for a GraphRAG project: traversals are matrix multiplications, so multi-hop patterns and graph algorithms are fast, but everything is held in "
7. `Elif Yildiz` -OWNS-> `ledger-service` (conf 0.9695, chunk `doc_f78fd6600c2d34aa#5` in `demo/SCRIPT.md`): "```bash neo impact ledger-service ``` ``` # impact [ent_e008439ebc28] ledger-service (service): 3 depend on it, it needs 1 (DEPENDS_ON, current, max_hops 3; A -"
8. `reporting-service` -DEPENDS_ON-> `ledger-service` (conf 0.7307, chunk `doc_f78fd6600c2d34aa#4` in `demo/SCRIPT.md`): "```bash neo ask "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?" ``` ``` ## Seeds (linked entitie"
9. `Olivia Hartmann` -OWNS-> `reporting-service` (conf 0.6434, chunk `doc_f78fd6600c2d34aa#4` in `demo/SCRIPT.md`): "```bash neo ask "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?" ``` ``` ## Seeds (linked entitie"
10. `SDK` -DEPENDS_ON-> `GraphRAG` (conf 0.9, chunk `doc_c2072f0c03fd0116#0` in `knowledge/graphrag-sdk/db-connectivity.md`): "How graphrag-sdk 1.4.0 builds its FalkorDB client, which injection points exist, whether falkordblite (embedded FalkorDB) works with it (verified two ways), vec"
11. `Tobias Wren` -DECIDED-> `ADR-007` (conf 0.8323, chunk `doc_f78fd6600c2d34aa#3` in `demo/SCRIPT.md`): "```bash neo ask "Why was the session idle TTL lowered to 300 seconds, and who decided it?" ``` ``` ## Facts among them - Tobias Wren -[DECIDED]-> ADR-007 (2026-"
12. `Elif Yildiz` -OWNS-> `ledger-service` (conf 0.9502, chunk `doc_f78fd6600c2d34aa#4` in `demo/SCRIPT.md`): "```bash neo ask "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?" ``` ``` ## Seeds (linked entitie"

## Corpus files

- `AGENTS.md`
- `README.md`
- `demo/SCRIPT.md`
- `docs/architecture.md`
- `docs/blog.md`
- `docs/cypher.md`
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
