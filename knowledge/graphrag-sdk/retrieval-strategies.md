---
type: Concept
title: GraphRAG SDK retrieval strategies
description: The retrieval strategies in graphrag-sdk 1.4.0 (MultiPathRetrieval default, LocalRetrieval, text-to-Cypher opt-in, cosine reranking), their parameters, the step-by-step pipeline, and the vendor benchmark numbers with their caveats.
resource: https://docs.falkordb.com/graphrag/retrieval
tags: [graphrag, retrieval, multi-hop, vector-search, text-to-cypher, benchmark]
status: stable
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/graphrag-sdk-agent, at: 2026-10-15T20:10:00Z }
sources:
  - id: docs-retrieval
    resource: https://docs.falkordb.com/graphrag/retrieval
    title: GraphRAG SDK Multi-Path Retrieval (FalkorDB docs)
  - id: docs-strategies
    resource: https://docs.falkordb.com/graphrag/strategies
    title: Strategy Reference (FalkorDB docs)
  - id: docs-configuration
    resource: https://docs.falkordb.com/graphrag/configuration
    title: GraphRAG SDK Configuration Reference (retrieval tuning)
  - id: docs-architecture
    resource: https://docs.falkordb.com/graphrag/architecture
    title: GraphRAG SDK Pipeline Architecture (retrieval flow)
  - id: docs-accuracy
    resource: https://docs.falkordb.com/graphrag/graphrag-accuracy-benchmark
    title: GraphRAG Accuracy Benchmark (FalkorDB docs)
  - id: src-pypi
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: graphrag-sdk 1.4.0 source (installed copy; files in evidence)
  - id: readme
    resource: https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md
    title: GraphRAG-SDK README
  - id: gh-issues
    resource: https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all
    title: "GitHub issues and PRs (state=all)"
  - id: run-docs
    resource: references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt
    title: "local run output (this research)"
  - id: run-e2e
    resource: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt
    title: "local run output (this research)"
  - id: src-multipath
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
evidence:
  - { name: retrieval.txt, url: "https://docs.falkordb.com/graphrag/retrieval", url_basis: inferred, sha256: b00732cd7252678fce2c2e8d7003bf0bdfe0326f4e1597121236d0bc7d69e80f, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: strategies.txt, url: "https://docs.falkordb.com/graphrag/strategies", url_basis: inferred, sha256: 406b86359245d89b44a5d991f87fc9bfca12711056decb7109cd7bec100bf9e6, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: configuration.txt, url: "https://docs.falkordb.com/graphrag/configuration", url_basis: inferred, sha256: 236cc936b838ef8845465aa04f852feea891a7d434c91cd35939be389045b7de, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: architecture.txt, url: "https://docs.falkordb.com/graphrag/architecture", url_basis: inferred, sha256: 4e67b3f2efb2668dfcf75e1b28cd40cb190c7aad9a8a760e0b499192499fc5c7, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: graphrag-accuracy-benchmark.txt, url: "https://docs.falkordb.com/graphrag/graphrag-accuracy-benchmark", url_basis: inferred, sha256: 9eb49b6db3d36eaf3e7374d4de719b5c374cc1665c4d47073fefd8d27f628b1e, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: multi_path.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: ae39c1ccdc51d0202be1344ff6585fab1dec460c9f8b4c8bb3de5fa9280f6642, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { file: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt, sha256: 020b6a709e6bb4c6c18a3ae7c5e5c592e926dab1f9ca783dfb1889ac5224f283, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt, sha256: 9e579b3fff87111d5772ddcf35378c4222d1b4d84906605ddc862c500bf05674, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { name: github-readme-main.txt, url: "https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md", url_basis: inferred, sha256: 6c18e22352b6b0cc7c84299a4cff996c23d883bb2c94f6173fe3d226d3e68b46, retrieved_at: 2026-10-15T19:23:43Z, method: curl, redistributed: false }
verified: { by: process:cross-check, at: 2026-10-15T20:00:00Z }
---

# GraphRAG SDK retrieval strategies

Summary: retrieval is a strategy object. The default is `MultiPathRetrieval`, which combines fact (RELATES edge) vector search, entity discovery, graph expansion, four chunk-retrieval paths, and cosine reranking. `LocalRetrieval` is a simpler vector-plus-one-hop alternative. Text-to-Cypher is opt-in. Pluggability is in [pluggability](/graphrag-sdk/pluggability.md). Storage and index details are in [db-connectivity](/graphrag-sdk/db-connectivity.md).

## Strategies in 1.4.0

| Strategy | Use | Notes |
|---|---|---|
| `MultiPathRetrieval` | Default | Full pipeline (below). Used by `GraphRAG` when no `retrieval_strategy=` is given. |
| `LocalRetrieval` | Simple, low latency, small graphs | "vector search on chunks + 1-hop entity traversal" (docs).[^docs-strategies] |
| `enable_cypher=True` on `MultiPathRetrieval` | Structural questions (counts, paths) | Text-to-Cypher. Docs label it `Text-to-Cypher *(experimental)*` (README).[^readme] |
| `CosineReranker` | Standalone reranking for `LocalRetrieval` or custom strategies | `CosineReranker(embedder=..., top_k=15)`.[^docs-strategies] |
| Custom | Any `RetrievalStrategy` subclass | Implement `_execute(query, ctx, **kwargs) -> RawSearchResult`.[^docs-strategies] |

Docs: `Production-grade retrieval with RELATES edge vector search, 2-path entity discovery, 4-path chunk retrieval, and cosine reranking. This is the default, and the strategy used for the GraphRAG-Bench results.`[^docs-strategies]

## MultiPathRetrieval parameters (verified in 1.4.0 source)

Constructor from the installed 1.4.0 `https://pypi.org/project/graphrag-sdk/1.4.0/`: `MultiPathRetrieval(graph_store, vector_store, embedder, llm, *, chunk_top_k=15, max_entities=30, max_relationships=20, rel_top_k=15, keyword_limit=10, enable_cypher=False, ontology=None, schema=None)`.[^src-multipath]

| Parameter | Default | Meaning (docs) |
|---|---|---|
| `chunk_top_k` | 15 | Final chunks after reranking |
| `max_entities` | 30 | Total entity cap across paths |
| `max_relationships` | 20 | Max relationships in context |
| `rel_top_k` | 15 | RELATES edge vector search results |
| `keyword_limit` | 10 | Max keywords extracted from question |
| `enable_cypher` | False | Text-to-Cypher path (opt-in) |

Source: `chunk_top_k: int = 15,  # Passage diversity without overwhelming LLM context`.[^src-multipath]

## Pipeline steps

Docs (retrieval page) list these steps. The architecture page gives the same flow in fewer words.[^docs-retrieval][^docs-architecture]

1. Keyword extraction: stopword filter plus LLM proper-noun extraction. Code: `MultiPathRetrieval._extract_keywords()`.
2. Embed the question (single embedding call).
3a. RELATES vector search: "Searches the relationship edges in the graph by meaning similarity." Returns fact strings.
3b. Text-to-Cypher (only if `enable_cypher=True`): "The query is validated (read-only, valid labels) and sanitized (adds LIMIT, removes unsupported FalkorDB patterns)." Results go straight to context, not reranked.
4. Entity discovery: Path A CONTAINS name match, Path B fulltext on the entity index, plus entities from 3a.
5. Relationship expansion: 1-hop (top 15 entities, limit 150) and 2-hop (top 5 entities, limit 25), per docs configuration.[^docs-configuration]
6. Chunk retrieval, four paths: A fulltext, B vector, C `MENTIONED_IN` traversal, D 2-hop entity to neighbour to chunk.
7. Document mapping (chunk to source document through `PART_OF`).
8. Reranking. 8a: passages re-scored by cosine using stored embeddings, keep top 15. 8b: facts filtered by a score threshold. Docs: `Facts use a higher threshold (0.25) and always keep at least 3 top facts.`[^docs-retrieval]
9. Context assembly. Sections: answer-format hint, Cypher results, key entities, relationships, facts, source passages.

Verified sections in a live `retrieve()` (default strategy, `runs/docs-snippets-pypi140.txt`): item metadata `section: hint` and a `## Source Document Passages` item with `[Source: acme_doc]`. `completion()` metadata reports `strategy: MultiPathRetrieval`.[^run-docs][^run-e2e]

Docs on the 3b path: `Runs in parallel with step 3a to avoid adding latency. If it fails, the other paths still produce results.`[^docs-retrieval]

## Text-to-Cypher

- Opt-in: `enable_cypher=False` is the default. Docs: `# With text-to-cypher (opt-in, adds ~1.5s latency)`.[^docs-retrieval]
- The LLM writes Cypher from a schema prompt. The query is checked (read-only, labels) and sanitized before running.[^docs-retrieval]
- Issue #292 (open, 2026-08-10): `Text-to-Cypher: invalid generated queries are retried 3x and never repaired`.[^gh-issues] Issue #305 PR "fix(retrieval): one LLM repair round for rejected text-to-Cypher queries" is open.[^gh-issues]

## Benchmark numbers in the docs (vendor claims)

These come from the FalkorDB docs and README. Nothing here was rerun. Treat each as a vendor claim.

Retrieval page, "Enhancement Comparison". The text extraction concatenates table cells, so the numbers are shown as they appear in `https://docs.falkordb.com/graphrag/retrieval`:[^docs-retrieval]

> `Baseline (MultiPath only)83.8%—4.2sCurrent default`
> `+ Text-to-Cypher84.2%+0.4%5.7sAdded graph query path`
> `+ All Enhancements84.8%+1.0%5.7sStored rerank + fact filtering + cypher`

Same page, "Isolated Path Performance" (each path alone): Vector Search 77.4%, Fulltext 74.8%, RELATES Vector 70.0%, Graph Traversal 69.1%, Text-to-Cypher 53.0%. Its text: `Key insight: No single path matches the combined pipeline (83.8%).`[^docs-retrieval]

Latency (P50): `Full MultiPath pipeline4.2s`, RELATES vector 1.6s, chunk vector 2.2s, Text-to-Cypher 4.5s.[^docs-retrieval]

**Measurement context.** This retrieval table is `100 questions scored by an LLM judge (0-10 scale)`, with one pre-built graph (`graphrag_sdk_v2_retrieval_benchmark`). That is not GraphRAG-Bench. The headline benchmark is different: `71.48 overall`, with `Overall = (Novel ACC + Medical ACC) / 2` on `Novel 2,010 questions` and `Medical 2,062 questions`. See [overview](/graphrag-sdk/overview.md) for those numbers and their caveats.[^docs-retrieval][^docs-accuracy]

The accuracy page says Text-to-Cypher was `enabled (enable_cypher=True)` for the 71.48 run and "contributed to 22% of Medical and 29% of Novel answers". That page also says `enable_cypher = True (SDK default False)`.[^docs-accuracy]

README: `FalkorDB scored August 2026 with gpt-4o-mini ... text-to-Cypher retrieval enabled, and the benchmark's own generation_eval.py unmodified as the judge.`[^readme]

## Known gaps and discrepancies

- Chunk size used in the benchmark is not the same across docs: the accuracy page uses `SentenceTokenCapChunking, max_tokens 512, overlap 2 sentences`, while the retrieval-tuning section recommends `1500/200` FixedSizeChunking as the benchmark value. Pick one and state it.[^docs-accuracy][^docs-configuration]
- Reranking is documented as "stored embeddings"; fact filtering uses a score threshold of 0.25 per docs. The 1.4.0 source for the threshold was not checked line by line.
- Issue #294 (closed) describes distance vs similarity ordering in vector search. That is a retrieval-quality bug on 1.4.0. See [db-connectivity](/graphrag-sdk/db-connectivity.md#ordering-bug-in-140-vector-scores-verified).[^gh-issues]

## Open questions

- Re-run the 71.48 benchmark with the released 1.4.0 package: not done. The reproduction package is "available on request" per the benchmark page.
- Is `LocalRetrieval` ported to 1.4.0 with the same ordering behavior? Not tested.

[^docs-strategies]: `https://docs.falkordb.com/graphrag/strategies`
[^docs-retrieval]: `https://docs.falkordb.com/graphrag/retrieval`
[^docs-configuration]: `https://docs.falkordb.com/graphrag/configuration`
[^docs-architecture]: `https://docs.falkordb.com/graphrag/architecture`
[^docs-accuracy]: `https://docs.falkordb.com/graphrag/graphrag-accuracy-benchmark`
[^src-multipath]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^readme]: `https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md`
[^run-e2e]: `references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt`
[^run-docs]: `references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt`
[^gh-issues]: `https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all&page=1`
