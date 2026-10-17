---
type: Concept
title: GraphRAG SDK architecture
description: Ingestion pipeline stages, ontology (manual and discovered), extraction, resolution, storage layout in FalkorDB, retrieval entry points, and what "chat session" means in graphrag-sdk 1.4.0.
resource: https://docs.falkordb.com/graphrag/architecture
tags: [graphrag, falkordb, architecture, ingestion, retrieval]
status: stable
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/graphrag-sdk-agent, at: 2026-10-15T20:10:00Z }
sources:
  - id: docs-architecture
    resource: https://docs.falkordb.com/graphrag/architecture
    title: GraphRAG SDK Pipeline Architecture (FalkorDB docs)
  - id: docs-getting-started
    resource: https://docs.falkordb.com/graphrag/getting-started
    title: Getting Started with GraphRAG SDK in Python
  - id: docs-extraction
    resource: https://docs.falkordb.com/graphrag/extraction
    title: GraphRAG SDK Entity & Relation Extraction
  - id: docs-storage
    resource: https://docs.falkordb.com/graphrag/storage
    title: How GraphRAG SDK Stores Graphs in FalkorDB
  - id: docs-strategies
    resource: https://docs.falkordb.com/graphrag/strategies
    title: Strategy Reference
  - id: src-pypi
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: graphrag-sdk 1.4.0 source (installed from PyPI, copies in evidence)
  - id: changelog
    resource: https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0b27fdcc7f2c28508b09e86169851a8187/CHANGELOG.md
    title: CHANGELOG.md at main commit 35e67a0
  - id: gh-issues
    resource: https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all
    title: GitHub issues and PRs
  - id: docs-configuration
    resource: https://docs.falkordb.com/graphrag/configuration
    title: "GraphRAG SDK Configuration Reference (FalkorDB docs)"
  - id: readme
    resource: https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md
    title: "GraphRAG-SDK README (main)"
  - id: run-claims
    resource: references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt
    title: "local run output (this research)"
  - id: run-docs
    resource: references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt
    title: "local run output (this research)"
  - id: run-e2e
    resource: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt
    title: "local run output (this research)"
  - id: src-extraction
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-pypi-listing
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-storage
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
evidence:
  - { name: architecture.txt, url: "https://docs.falkordb.com/graphrag/architecture", url_basis: inferred, sha256: 4e67b3f2efb2668dfcf75e1b28cd40cb190c7aad9a8a760e0b499192499fc5c7, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: getting-started.txt, url: "https://docs.falkordb.com/graphrag/getting-started", url_basis: inferred, sha256: 25524f91e16e58a35df4b9daadf7c4bb820d03bd3be2120dbe3fffaba8b8e9e7, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: extraction.txt, url: "https://docs.falkordb.com/graphrag/extraction", url_basis: inferred, sha256: f7427360df531a63bb0dc09e097a42549ed05df942d821704d84b26268ef55f2, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: storage.txt, url: "https://docs.falkordb.com/graphrag/storage", url_basis: inferred, sha256: d75adfc930efbdc1181c912c5988ecc08fa9abfa16ceccf9568ea379a59ce606, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: api_main.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: b4245004e02fdb9095e580b35fc32797abd19f1566f1492261dbd5b00c60521d, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { name: multi_path.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: ae39c1ccdc51d0202be1344ff6585fab1dec460c9f8b4c8bb3de5fa9280f6642, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { file: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt, sha256: 020b6a709e6bb4c6c18a3ae7c5e5c592e926dab1f9ca783dfb1889ac5224f283, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt, sha256: eee5456404439fc99e47fb8d0d650a46e4b724a195be4655cf7e34f42cd0e019, retrieved_at: 2026-10-15T20:00:00Z, method: command }
verified: { by: process:cross-check, at: 2026-10-15T20:00:00Z }
---

# GraphRAG SDK architecture

Summary: the SDK is a strategy-pattern pipeline. A single facade, `GraphRAG`, drives an ingestion pipeline (load, chunk, extract, resolve, write) and a retrieval pipeline (search, rerank, generate). Every algorithmic step is a swappable ABC; see [pluggability](/graphrag-sdk/pluggability.md). Retrieval details are in [retrieval-strategies](/graphrag-sdk/retrieval-strategies.md). Connection details are in [db-connectivity](/graphrag-sdk/db-connectivity.md).

## Facade

`GraphRAG` is the only entry point. Verified 1.4.0 signature (from the installed package):[^src-pypi]

```
GraphRAG.__init__(self, connection: 'FalkorDBConnection | ConnectionConfig', llm: 'LLMInterface', embedder: 'Embedder', ontology: 'Ontology | None' = None, retrieval_strategy: 'RetrievalStrategy | None' = None, embedding_dimension: 'int' = 256, *, schema: 'Ontology | None' = None)
```

Public methods in 1.4.0 `api/main.py`: `ingest`, `update`, `delete_document`, `apply_changes`, `retrieve`, `completion`, `finalize`, plus `*_sync` wrappers (`ingest_sync`, `retrieve_sync`, `completion_sync`, `finalize_sync`) and `async with` support (`__aenter__`).[^src-pypi]

Default retrieval wiring, quoted from `api/main.py`:[^src-pypi]

> `self._retrieval_strategy = retrieval_strategy or MultiPathRetrieval(`

## Ingestion pipeline

Docs say 9 steps:

> `The ingestion pipeline runs a 9-step process: Load, Chunk, Lexical Graph, Extract (includes quality filtering), Prune, Resolve, Write, then Mentions and Chunk Indexing in parallel.` [^docs-getting-started]

Docs table (`https://docs.falkordb.com/graphrag/architecture`): 1 Load (`LoaderStrategy`), 2 Chunk (`ChunkingStrategy`), 3 Lexical Graph (built-in), 4 Extract (`ExtractionStrategy`), 5 Prune (built-in, filters off-schema data), 6 Resolve (`ResolutionStrategy`), 7 Write (built-in MERGE), 8 Mentions (parallel), 9 Index Chunks (parallel).[^docs-architecture]

Source: `class IngestionPipeline:` in `ingestion/pipeline.py` whose docstring is `Sequential orchestrator for knowledge graph construction.`[^src-pypi-listing]

Ingest call signature in 1.4.0:[^run-claims]

```
GraphRAG.ingest(self, source: 'str | list[str] | None' = None, *, text: 'str | None' = None, document_id: 'str | None' = None, loader: ..., chunker: ..., extractor: ..., resolver: ..., max_concurrency: 'int' = 3, ...)
```

Input modes are mutually exclusive: a `source` path, or `text=` with optional `document_id=`. Verified by running `ingest(text=..., document_id=...)` (works) and `ingest("acme_doc", text=...)` (raises `ValueError: Cannot pass both 'source' and 'text'.`).[^run-docs]

Default loader by extension (`_default_loader_for` in `api/main.py`): `.pdf` gets `PdfLoader`, `.md` gets `MarkdownLoader`, and everything else gets `TextLoader`. This is per docs; the PDF and markdown loaders need extras.[^docs-strategies]

### Chunking

Built-ins in 1.4.0 (`ingestion/chunking_strategies/`): `FixedSizeChunking` (defaults `chunk_size=1000`, `chunk_overlap=100`, verified), `SentenceTokenCapChunking` (default `max_tokens=512` in 1.4.0, verified; docs and main say 384), `ContextualChunking` (one LLM call per chunk), `CallableChunking`, `StructuralChunking`.[^run-claims][^docs-strategies]

### Extraction

Default extraction is `GraphExtraction`, a composable two-step strategy. Docs describe it as: "Step 1 — Entity NER (pluggable via EntityExtractor ABC)" with `GLiNERExtractor` as default, then "Step 2 — LLM Verify + Relationship Extraction".[^docs-strategies][^docs-extraction]

Source docstring: `Composable 2-step extraction with pluggable entity NER.` Constructor (1.4.0): `GraphExtraction(llm, *, entity_extractor=None, coref_resolver=None, entity_types=None, max_concurrency=None)`. Default entity extractor is `GLiNERExtractor()`.[^src-extraction][^run-claims]

Entity types in 1.4.0 default to 11 names (`Person, Organization, Technology, Product, Location, Date, Event, Concept, Law, Dataset, Method`) per docs. `relation_types` is **absent** in 1.4.0 (`AttributeError: 'GraphExtraction' object has no attribute 'relation_types'`); the docs' 31-label default relation vocabulary appears in unreleased `main` only.[^docs-extraction][^run-claims]

All LLM-extracted relations are stored as a single `RELATES` edge type, with the original type in `rel_type`. Docs quote: `All LLM-extracted relationships use the single RELATES edge type. The original relationship type (e.g. WORKS_AT, LOCATED_IN) is preserved as the rel_type property on the edge.` Verified: the e2e run returned `[['Alice Johnson', 'WORKS_AT', 'Acme Corp'], ['Acme Corp', 'LOCATED_IN', 'London']]` from `MATCH (a)-[r:RELATES]->(b)`.[^docs-architecture][^run-e2e]

### Ontology

The ontology is the schema. Types are `Ontology`, `Entity`, `Relation`, `Attribute` in `core/models.py`. `GraphSchema`, `EntityType` and `RelationType` are deprecated aliases (`` `graphrag_sdk.GraphSchema` has been renamed to `graphrag_sdk.Ontology` ``).[^src-pypi-listing][^run-claims]

- Manual: pass `ontology=` (or deprecated `schema=`) to `GraphRAG`. Priority for entity types, per docs: `schema.entities > entity_types param > defaults`.[^docs-extraction]
- Open schema: an empty ontology skips pruning (`Open Schema Mode` in configuration docs).[^docs-configuration]
- Discovered: `Ontology.from_sources` (in `core/models.py`) calls `discover_ontology` in `discovery/pipeline.py`. `GraphRAG.suggest_schema_extensions` proposes additions to a live graph. The discovery module's `DBpediaCatalog` fetches from an external catalog. This path was not run.[^src-pypi-listing]
- Persistent: the ontology is stored in a second graph named `<data_graph>__ontology` (`ONTOLOGY_GRAPH_SUFFIX = "__ontology"` in `storage/ontology_store.py`). Source only, not inspected in a live DB.[^src-pypi-listing]

### Resolution

- `ExactMatchResolution` is the ingest default. It dedups by normalised name plus label.[^docs-strategies]
- `LLMVerifiedResolution` is opt-in at ingest. It uses an embedder and an LLM for near-duplicates. Docs (main behavior): `Across documents, finalize() already runs it over the whole graph by default (resolve=False turns that off).`[^docs-strategies] On 1.4.0, `finalize()` does not use `LLMVerifiedResolution`; it runs `EntityDeduplicator` (exact name match, optional fuzzy) (verified by grep of `https://pypi.org/project/graphrag-sdk/1.4.0/`, no construction site). Main's CHANGELOG #317 and #327 describe the LLM-judged finalize dedup.
- `finalize()` runs `deduplicate_entities`, `backfill_entity_embeddings`, `embed_relationships`, and `ensure_indices`. Docs: `It bundles four steps in order`.[^docs-configuration]

### Write and storage layout

Nodes and edges are written with batched UNWIND MERGE (500 per batch). Quoting `https://docs.falkordb.com/graphrag/storage`: `Nodes and relationships are written in batches of 500 items per query.`[^docs-storage]

Graph elements observed in a live run (`runs/sdk-e2e-tcp-pypi140.txt`, `get_statistics()` output): labels `Document`, `Chunk`, `__Entity__`, entity labels such as `Person`, `Organization`, `Location`, and the internal `__GraphRAGConfig__` node. Edge types: `PART_OF`, `RELATES`, `MENTIONED_IN`. The `__GraphRAGConfig__` node stores the embedding model and dimension, which retrieval checks (CHANGELOG 1.0.0: "`__GraphRAGConfig__` singleton stores the embedding model and dimension used to build the graph; mismatches are caught on retrieval.").[^run-e2e][^changelog]

Doc table of edges: `PART_OF` (Document to Chunk), `NEXT_CHUNK` (Chunk to Chunk), `MENTIONED_IN` (Entity to Chunk), `RELATES` (Entity to Entity).[^docs-architecture]

Indexes created by `ensure_indices` (verified with `CALL db.indexes()`): vector indexes on `Chunk.embedding`, `__Entity__.embedding`, and `RELATES.embedding`, plus fulltext indexes on `Chunk.text` and `__Entity__.name, description`. Syntax is in [db-connectivity](/graphrag-sdk/db-connectivity.md#vector-index-syntax).[^run-e2e][^src-storage]

## Retrieval pipeline (summary)

- Default: `MultiPathRetrieval`. Docs: `Production-grade retrieval with RELATES edge vector search, 2-path entity discovery, 4-path chunk retrieval, and cosine reranking. This is the default, and the strategy used for the GraphRAG-Bench results.`[^docs-strategies]
- `retrieve()` returns context only. `completion()` retrieves and then generates with the LLM.[^docs-getting-started]
- Details and the list of steps are in [retrieval-strategies](/graphrag-sdk/retrieval-strategies.md).

## Chat sessions and agents

- `completion()` supports history. There is no session object, no agent class, and no server-side conversation state in 1.4.0. Grep over `src-pypi-1.4.0` finds no `*Session*`, `*Agent*`, or `*Chat*` class except `ChatMessage` (a pydantic message model).[^src-pypi-listing]
- Docs: `completion() supports native multi-turn conversations. Messages are passed directly to the LLM’s chat API as structured messages:` The caller stores and passes `history=` each turn. Roles are `system`, `user`, and `assistant`; other roles raise `ValueError`.[^docs-getting-started]
- Agentic work is roadmap only. Issue #263 "Agentic GraphRAG" is open. PR #276 "Agentic GraphRAG toolkit (`graphrag_sdk.tools`)" is open. Neither is in 1.4.0.[^gh-issues]

## Unreleased structured ingestion (main only)

The docs site's "Structured Ingestion" page describes `Ontology(tables=[TableMapping(...)])` and `rag.ingest("data/employees.csv")`. On the 1.4.0 release, `graphrag_sdk.TableMapping` does not exist and the `Ontology` model has no `tables` field (verified).[^run-claims] The main branch CHANGELOG describes this feature under `## [Unreleased]`.[^changelog] Treat the docs page as describing unreleased main.

## Open questions

- Whether the structured-ingestion and relation-vocabulary features ship in the next release (main is ahead of 1.4.0).
- The docs site and main both changed chunk defaults (512 to 384) and the relation vocabulary after 1.4.0. Re-check at next release.

[^docs-architecture]: `https://docs.falkordb.com/graphrag/architecture`
[^docs-getting-started]: `https://docs.falkordb.com/graphrag/getting-started`
[^docs-extraction]: `https://docs.falkordb.com/graphrag/extraction`
[^docs-storage]: `https://docs.falkordb.com/graphrag/storage`
[^docs-strategies]: `https://docs.falkordb.com/graphrag/strategies`
[^docs-configuration]: `https://docs.falkordb.com/graphrag/configuration`
[^src-pypi]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-pypi-listing]: `https://pypi.org/project/graphrag-sdk/1.4.0/` and the installed package at `venv-pypi/lib/python3.14/site-packages/graphrag_sdk/` (listed in `runs/pip-freeze-sdk-venv.txt`)
[^src-extraction]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-storage]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^run-claims]: `references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt`
[^run-docs]: `references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt`
[^run-e2e]: `references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt`
[^readme]: `https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md`
[^changelog]: `https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/CHANGELOG.md`
[^gh-issues]: `https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all&page=1`
