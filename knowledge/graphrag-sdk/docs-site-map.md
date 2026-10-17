---
type: Concept
title: FalkorDB GraphRAG docs site map
description: Every page under docs.falkordb.com/graphrag (20 sitemap entries), what each covers, its sitemap lastmod, the evidence file that holds it, and which page claims match or conflict with the 1.4.0 release.
resource: https://docs.falkordb.com/graphrag
tags: [graphrag, falkordb, docs, sitemap]
status: stable
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/graphrag-sdk-agent, at: 2026-10-15T20:10:00Z }
sources:
  - id: sitemap
    resource: https://docs.falkordb.com/sitemap.xml
    title: FalkorDB docs sitemap
  - id: llms-txt
    resource: https://docs.falkordb.com/llms.txt
    title: FalkorDB docs index (llms.txt)
  - id: docs-graphrag-index
    resource: https://docs.falkordb.com/graphrag/
    title: GraphRAG SDK index page
  - id: llms
    resource: https://docs.falkordb.com/llms.txt
    title: "FalkorDB docs index (llms.txt)"
  - id: run-claims
    resource: references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt
    title: "local run output (this research)"
  - id: run-docs
    resource: references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt
    title: "local run output (this research)"
  - id: src-init
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
evidence:
  - { name: docs-sitemap.xml, url: "https://docs.falkordb.com/sitemap.xml", sha256: 09275a9f67e8dc1f7c106e72ec8b697a254c9a20654a3eb3b2117f223e758283, retrieved_at: 2026-10-15T19:23:43Z, method: curl, redistributed: false }
  - { name: llms.txt, url: "https://docs.falkordb.com/llms.txt", sha256: b6f5810330759d9ecdb3617831ff5ae92044230caeb7e20a7bd143a40babc5f5, retrieved_at: 2026-10-15T19:36:05Z, method: curl, redistributed: false }
  - { name: graphrag-index-slash.html, url: "https://docs.falkordb.com/graphrag/", sha256: 10b8768c819fbb303a3aa2488c8749d3b7e089a78d68fbd909071e0766d8c645, retrieved_at: 2026-10-15T19:36:05Z, method: curl, redistributed: false }
  - { name: graphrag-index.txt, url: "https://docs.falkordb.com/graphrag/", sha256: 24b1b133417f18af82549a83ba38e817897bd41a41b118c77f7cafb16fe9f55e, retrieved_at: 2026-10-15T19:36:05Z, method: curl, redistributed: false }
verified: { by: process:cross-check, at: 2026-10-15T20:00:00Z }
---

# FalkorDB GraphRAG docs site map

The docs site serves each page as HTML and as Markdown (`…/graphrag/<page>.md`, listed in `https://docs.falkordb.com/llms.txt`). The index is `https://docs.falkordb.com/llms.txt`.[^llms] Sitemap: `https://docs.falkordb.com/sitemap.xml`, which lists 20 pages under `/graphrag` (including the index). Evidence: the raw HTML and text conversions are not redistributed; each page's URL (`https://docs.falkordb.com/graphrag/<page>`) and sha256 are in the frontmatter.

Index URL note: the sitemap lists `https://docs.falkordb.com/graphrag` (no trailing slash). That URL returned **404** when fetched with curl. `https://docs.falkordb.com/graphrag/` (trailing slash) returned 200. Saved as the finding: `https://docs.falkordb.com/graphrag` holds the 404 body, `https://docs.falkordb.com/graphrag/` the 200 page.[^sitemap]

The Accuracy page's "Last updated" line: `Last updated: August 2026.` The docs pages carry no visible "last updated" stamps other than the sitemap `lastmod`.

## Page list

Sitemap `lastmod` is the sitemap value. Evidence file is the text conversion.

| Page | Covers | lastmod | Evidence | Match vs 1.4.0 |
|---|---|---|---|---|
| `/graphrag/` (index) | Product intro, key highlights, quick start | 2026-08-31 | `https://docs.falkordb.com/graphrag/` | Claims "#1 on GraphRAG-Bench" and "100+ LLM providers via LiteLLM (OpenAI, Azure, Anthropic, Cohere, Ollama, and more)" (vendor claim, Ollama untested) |
| `getting-started` | Install, Docker FalkorDB, schema, `ingest`, `retrieve`/`completion`, multi-turn, `finalize` | 2026-09-15 | `https://docs.falkordb.com/graphrag/getting-started` | Partly stale: `GraphSchema`/`schema=` (deprecated), positional `ingest("acme_doc", text=...)` raises on 1.4.0. `rag.graph_store` is private (1.0+). |
| `architecture` | Pipeline design, ABCs, data flow, storage summary, retrieval flow | 2026-09-15 | `https://docs.falkordb.com/graphrag/architecture` | Describes "GraphRAG SDK v2" strategy pipeline. Matches main; partly ahead of 1.4.0 (relation vocabulary, structured ingestion). |
| `reducing-llm-hallucinations` | Grounding, provenance, abstention guide | 2026-08-31 | `https://docs.falkordb.com/graphrag/reducing-llm-hallucinations` | Not verified against the release. Linked from README. |
| `configuration` | ConnectionConfig, LLM and embedder params, GraphSchema, pipeline tuning, retrieval tuning, finalize, indexes | 2026-09-15 | `https://docs.falkordb.com/graphrag/configuration` | `finalize()` steps match 1.4.0 output (dedup, backfill, embed_relationships, indexes). Retry backoff text says linear; 1.4.0 code is exponential. `ConnectionConfig` fields match. |
| `ingestion` | The 9-step ingest pipeline, chunking, loaders, resolution | 2026-09-15 | `https://docs.falkordb.com/graphrag/ingestion` | Not compared line by line. Pipeline steps and defaults match 1.4.0 behavior seen in runs. |
| `structured-ingestion` | CSV and tabular ingestion via `Ontology(tables=...)`, `TableMapping`, `Column`, `Link` | 2026-09-12 | `https://docs.falkordb.com/graphrag/structured-ingestion` | **Not in 1.4.0** (`TableMapping` import fails). Documented against main (Unreleased). |
| `extraction` | Hybrid NER plus LLM extraction, EntityExtractor, GLiNER, ontology types, aggregation | 2026-09-15 | `https://docs.falkordb.com/graphrag/extraction` | Consistent in part. Relation vocabulary (31 default labels) is main-only. |
| `retrieval` | Multi-path retrieval steps, benchmark tables, text-to-Cypher toggle | 2026-09-15 | `https://docs.falkordb.com/graphrag/retrieval` | Steps and defaults consistent. Benchmark tables are vendor claims (100-question LLM-judge set). |
| `storage` | GraphStore batched UNWIND MERGE, VectorStore indexes, dedup | 2026-09-28 | `https://docs.falkordb.com/graphrag/storage` | Index syntax matches 1.4.0 source. |
| `graph-schema` | Node labels, edge types, properties, indexes | 2026-08-17 | `https://docs.falkordb.com/graphrag/graph-schema` | Not compared in depth. |
| `strategies` | All strategy ABCs with built-ins and examples | 2026-09-15 | `https://docs.falkordb.com/graphrag/strategies` | Main-era (e.g., `LLMVerifiedResolution` default at finalize, `SpacyExtractor`). Core ABCs match 1.4.0. |
| `providers` | LiteLLM, OpenRouter, custom `LLMInterface` and `Embedder`, env vars | 2026-09-15 | `https://docs.falkordb.com/graphrag/providers` | Matches 1.4.0 ABCs (`invoke`, `embed_query`, `model_name`). |
| `api-reference` | Every public class and method | 2026-09-28 | `https://docs.falkordb.com/graphrag/api-reference` | Constructor matches 1.4.0 (`ontology=`, deprecated `schema=`). Includes main-only classes. |
| `reliability-and-grounding` | Grounding, provenance, evidence trails, confidence thresholds, abstention, mapped to APIs | 2026-08-31 | `https://docs.falkordb.com/graphrag/reliability-and-grounding` | Not verified against the release. |
| `ontology-discovery` | Bootstrap an ontology from a corpus, propose additions as docs arrive | 2026-09-09 | `https://docs.falkordb.com/graphrag/ontology-discovery` | `discover_ontology` / `suggest_schema_extensions` exist in 1.4.0 source. Not run. |
| `ontology-evolution` | Mutating schema evolution (rename, add, drop, backfill) | 2026-08-17 | `https://docs.falkordb.com/graphrag/ontology-evolution` | Not run. Methods `rename_entity`, `add_attribute`, `rename_relation`, `drop_attribute`, `drop_entity`, `add_entity` exist in 1.4.0 `https://pypi.org/project/graphrag-sdk/1.4.0/`. |
| `incremental-updates` | `update`, `delete_document`, `apply_changes`, crash-safe cutover | 2026-09-09 | `https://docs.falkordb.com/graphrag/incremental-updates` | Methods exist in 1.4.0 `https://pypi.org/project/graphrag-sdk/1.4.0/`. Not run. |
| `graphrag-accuracy-benchmark` | 71.48 vs 55.39 comparison, configuration, limitations, citation | 2026-09-09 | `https://docs.falkordb.com/graphrag/graphrag-accuracy-benchmark` | Vendor claim. States SDK 1.3.0, `enable_cypher=True`, embeddings 1024-dim. |
| `benchmark` | GraphRAG-Bench methodology, 15-system leaderboard, reproduction | 2026-09-15 | `https://docs.falkordb.com/graphrag/benchmark` | Vendor claim; competitor numbers are copied from the public leaderboard. Not re-run. |

## Adjacent pages outside `/graphrag`

Not fetched (out of scope): `genai-tools/graphrag-sdk` and `genai-tools/graphrag-toolkit` appear in the sitemap. `agentic-memory/graphiti`, `agentic-memory/mem0` and `agentic-memory/cognee` also appear.[^sitemap]

## Docs claims that do not match the 1.4.0 release

These came out of this research. Each is backed by a run in `runs/`:

- Positional `ingest("acme_doc", text=...)` (getting-started step 7). Raises `ValueError`.[^run-docs]
- `rag.graph_store.get_statistics()` (getting-started step 9). `graph_store` is private since 1.0. Use `rag.get_statistics()`.[^run-docs]
- Dict-style `finalize()` result (getting-started step 10). `finalize()` returns `FinalizeResult`.[^run-docs]
- Structured ingestion (`TableMapping`, `Ontology(tables=...)`). Not in 1.4.0.[^run-claims]
- Default chunk `max_tokens`: docs say 384 for `SentenceTokenCapChunking`. 1.4.0 says 512.[^run-claims]
- `GraphSchema`, `EntityType`, `RelationType` and `schema=` throughout docs. Deprecated aliases in 1.4.0.[^src-init]

## Open questions

- Whether the docs site gets versioned (v1 vs v2 pages) or stays on main. The architecture page says "GraphRAG SDK v2", and PyPI's latest is 1.4.0.
- The `reliability-and-grounding` and `reducing-llm-hallucinations` pages were fetched but not checked claim by claim.

[^llms]: `https://docs.falkordb.com/llms.txt`
[^sitemap]: `https://docs.falkordb.com/sitemap.xml`
[^run-docs]: `references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt`
[^run-claims]: `references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt`
[^src-init]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
