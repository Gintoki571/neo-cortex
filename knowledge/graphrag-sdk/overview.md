---
type: Concept
title: GraphRAG SDK overview
description: What FalkorDB's graphrag-sdk is, its latest release, Python and license facts, install extras, maintenance activity, API generations, and vendor benchmark claims, each with evidence.
resource: https://github.com/FalkorDB/GraphRAG-SDK
tags: [graphrag, falkordb, knowledge-graph, python, sdk]
status: stable
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/graphrag-sdk-agent, at: 2026-10-15T20:10:00Z }
sources:
  - id: readme
    resource: https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md
    title: GraphRAG-SDK README (main)
  - id: gh-repo
    resource: https://api.github.com/repos/FalkorDB/GraphRAG-SDK
    title: GitHub repository metadata
  - id: gh-releases
    resource: https://api.github.com/repos/FalkorDB/GraphRAG-SDK/releases
    title: GitHub releases list
  - id: gh-issues
    resource: https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all
    title: GitHub issues and PRs (state=all, first 100)
  - id: pypi
    resource: https://pypi.org/pypi/graphrag_sdk/json
    title: PyPI JSON for graphrag_sdk
  - id: changelog
    resource: https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0b27fdcc7f2c28508b09e86169851a8187/CHANGELOG.md
    title: CHANGELOG.md at main commit 35e67a0 (clone)
  - id: accuracy
    resource: https://docs.falkordb.com/graphrag/graphrag-accuracy-benchmark
    title: GraphRAG Accuracy Benchmark (FalkorDB docs)
  - id: docs-retrieval
    resource: https://docs.falkordb.com/graphrag/retrieval
    title: GraphRAG SDK Multi-Path Retrieval (FalkorDB docs)
  - id: docs-accuracy
    resource: https://docs.falkordb.com/graphrag/graphrag-accuracy-benchmark
    title: "GraphRAG Accuracy Benchmark (FalkorDB docs)"
  - id: docs-architecture
    resource: https://docs.falkordb.com/graphrag/architecture
    title: "GraphRAG SDK Pipeline Architecture (FalkorDB docs)"
  - id: docs-configuration
    resource: https://docs.falkordb.com/graphrag/configuration
    title: "GraphRAG SDK Configuration Reference (FalkorDB docs)"
  - id: docs-getting-started
    resource: https://docs.falkordb.com/graphrag/getting-started
    title: "Getting Started (FalkorDB docs)"
  - id: docs-index
    resource: https://docs.falkordb.com/graphrag/
    title: "GraphRAG SDK index page (FalkorDB docs)"
  - id: repo-pyproject
    resource: https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0b27fdcc7f2c28508b09e86169851a8187/graphrag_sdk/pyproject.toml
    title: "GraphRAG-SDK pyproject.toml at main 35e67a0"
  - id: run-claims
    resource: references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt
    title: "local run output (this research)"
  - id: run-docs
    resource: references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt
    title: "local run output (this research)"
  - id: src-init
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-main
    resource: https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0b27fdcc7f2c28508b09e86169851a8187/graphrag_sdk/src/graphrag_sdk/core/connection.py
    title: "core/connection.py at main 35e67a0"
evidence:
  - { name: github-readme-main.txt, url: "https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md", url_basis: inferred, sha256: 6c18e22352b6b0cc7c84299a4cff996c23d883bb2c94f6173fe3d226d3e68b46, retrieved_at: 2026-10-15T19:23:43Z, method: curl, redistributed: false }
  - { name: LICENSE.txt, url: "https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/LICENSE", url_basis: inferred, sha256: 27fbe8666fbffd8e0dbc32866f04344535b7b3179797bb21a4abcf028c433ea5, retrieved_at: 2026-10-15T19:23:43Z, method: curl, redistributed: false }
  - { name: gh-repo.json, url: "https://api.github.com/repos/FalkorDB/GraphRAG-SDK", sha256: 7f3ee97bfe0595985eef31c3905e58ee27b863b693e64621c87ff5886a618486, retrieved_at: 2026-10-15T19:23:43Z, method: curl, redistributed: false }
  - { name: gh-releases.json, url: "https://api.github.com/repos/FalkorDB/GraphRAG-SDK/releases", sha256: 42602fd394714f76ba6d6f0a21231e68d75c5d2ab5c8710313c10051cc2b24bb, retrieved_at: 2026-10-15T19:23:43Z, method: curl, redistributed: false }
  - { name: gh-releases-latest.json, url: "https://api.github.com/repos/FalkorDB/GraphRAG-SDK/releases/latest", sha256: de89ada4832d94ee77a98aa4b0f4b99c71e6b926b2827660573bb12b877b1a20, retrieved_at: 2026-10-15T19:23:43Z, method: curl, redistributed: false }
  - { name: gh-issues-all-p1.json, url: "https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all&page=1", url_basis: inferred, sha256: dd881082d44be55d752428bc8e05776beed69cd9c52b353b512df3369fcc0634, retrieved_at: 2026-10-15T19:36:22Z, method: command, redistributed: false }
  - { name: pypi-graphrag_sdk.json, url: "https://pypi.org/pypi/graphrag-sdk/json", sha256: e95be5e9e4be46ab40dff48cbc9e74e8fdba20263b16b5884381c48120d77ab4, retrieved_at: 2026-10-15T19:23:43Z, method: curl, redistributed: false }
  - { name: CHANGELOG.txt, url: "https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/CHANGELOG.md", url_basis: inferred, sha256: d2bf12d190162f2869ba03dfe923017a953c4c3ef174bc124139b744a7456efc, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
  - { name: pyproject.toml, url: "https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/pyproject.toml", url_basis: inferred, sha256: a0ede91e7cc294eb9afc3ce43caad2acd4900af12b82d13657d63bf8e7cbc7a4, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
  - { name: graphrag-accuracy-benchmark.txt, url: "https://docs.falkordb.com/graphrag/graphrag-accuracy-benchmark", url_basis: inferred, sha256: 9eb49b6db3d36eaf3e7374d4de719b5c374cc1665c4d47073fefd8d27f628b1e, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: retrieval.txt, url: "https://docs.falkordb.com/graphrag/retrieval", url_basis: inferred, sha256: b00732cd7252678fce2c2e8d7003bf0bdfe0326f4e1597121236d0bc7d69e80f, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { file: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt, sha256: 020b6a709e6bb4c6c18a3ae7c5e5c592e926dab1f9ca783dfb1889ac5224f283, retrieved_at: 2026-10-15T20:00:00Z, method: command }
verified: { by: process:cross-check, at: 2026-10-15T20:00:00Z }
---

# GraphRAG SDK overview

GraphRAG SDK (`graphrag_sdk`, repo `FalkorDB/GraphRAG-SDK`) is a Python framework that builds a knowledge graph from documents and answers questions over it, storing the graph in FalkorDB. Architecture: [architecture](/graphrag-sdk/architecture.md). Pluggable seams: [pluggability](/graphrag-sdk/pluggability.md). DB: [db-connectivity](/graphrag-sdk/db-connectivity.md).

## Identity and release facts

- Latest PyPI release is `1.4.0`, uploaded 2026-08-10. The GitHub release `v1.4.0` has the same date.[^pypi][^gh-releases]
  > `"tag_name": "v1.4.0"` / `"published_at": "2026-08-10T13:57:02Z"` (`https://api.github.com/repos/FalkorDB/GraphRAG-SDK/releases/latest`)
- PyPI `requires_python`: `>=3.10`. Repo `https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/pyproject.toml`: `requires-python = ">=3.10"`.[^pypi][^repo-pyproject]
  > `"requires_python":">=3.10"` (`https://pypi.org/pypi/graphrag-sdk/json`)
- License: Apache-2.0. Verified in GitHub metadata, PyPI, and `LICENSE`.[^gh-repo][^pypi]
  > `"spdx_id": "Apache-2.0"` (`https://api.github.com/repos/FalkorDB/GraphRAG-SDK`)
  > `Apache License` / `Version 2.0, January 2004` (`https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/LICENSE`)
- Language: Python. Topics include `falkordb`, `graphrag`, `knowledge-graph`, `rag`, `sdk`.[^gh-repo]
- Environment limit: we ran the SDK only on Python 3.14.7. The `requires-python` floor of 3.10 was not tested.

## Maintenance activity (as of 2026-10-15)

- Repo `pushed_at` 2026-10-14T12:40:03Z, `updated_at` 2026-10-15T10:09:31Z, not archived, 1017 stars, 48 open issues (includes PRs).[^gh-repo]
  > `"pushed_at": "2026-10-14T12:40:03Z"`, `"open_issues_count": 48`, `"stargazers_count": 1017` (`gh-repo.json`)
- Release cadence: 1.0.0 (2026-04-21), 1.0.1 (04-29), 1.0.2 (05-04), 1.1.0 (05-11), 1.1.1 (05-13), 1.2.0 (06-01), 1.3.0 (06-04), 1.4.0 (08-10). Earlier 0.x line ended at 0.8.1 (2025-09-29) on GitHub, and PyPI also lists 0.8.2.[^gh-releases][^pypi]
- `main` is ahead of the 1.4.0 release. The repo CHANGELOG has an `## [Unreleased]` section headed "Structured ingestion — tables declared on the ontology", while `https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/pyproject.toml` on main still says `version = "1.4.0"`.[^changelog][^repo-pyproject]
  > `## [Unreleased]` and `#### Structured ingestion — tables declared on the ontology, one node for a row and its mention` (`https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/CHANGELOG.md`)
- Open issue #344 (2026-10-15) reports failures on FalkorDB 6.0.x. See [db-connectivity](/graphrag-sdk/db-connectivity.md).[^gh-issues]

## Install and extras

PyPI declares these hard dependencies: `falkordb<2,>=1.0`, `gliner<1,>=0.2`, `hnswlib>=0.8`, `numpy<3,>=1.24`, `pydantic<3.0,>=2.0`, `python-dotenv>=1.0`, `scipy<2,>=1.11`, `tiktoken<1.0,>=0.5`.[^pypi]

Extras (`provides_extra`): `all`, `anthropic`, `cohere`, `dev`, `fastcoref`, `litellm`, `markdown`, `openai`, `openrouter`, `pdf`, `pdf-fast`, `sentence-transformers`, `spacy`.[^pypi]

- README quick start: `pip install graphrag-sdk[litellm]`. Docs getting-started: `pip install "graphrag-sdk[all]"`.[^readme][^docs-getting-started]
- Because `gliner` is a hard dependency, a plain install pulls PyTorch and CUDA wheels. In our sandbox the first install attempt failed mid-download (triton, 154.9/248.0 MB). We then installed with `--no-deps` and listed core deps by hand. See `runs/pip-freeze-sdk-venv.txt`.

## API generations

- README: `Still on the v0.x API? Pin the legacy release: pip install graphrag-sdk==0.8.2`.[^readme]
- CHANGELOG 1.0.0: `First stable release of the v1.0 rewrite.` It lists breaking changes: storage privatized (`rag.graph_store` becomes `_graph_store`), `ingest(max_concurrent=)` renamed to `max_concurrency=`, `source` and `text` become mutually exclusive, batch `ingest` returns per-source results, `finalize()` returns a typed `FinalizeResult`, and `query()` / `query_sync()` are removed.[^changelog]
- Rename in 1.2+: the source says `` `graphrag_sdk.{name}` has been renamed to `` with `GraphSchema` mapped to `Ontology`. `schema=` on `GraphRAG` is deprecated in favor of `ontology=`.[^src-init][^src-main]
- Docs site: `GraphRAG SDK v2`. Docs describe v2 (strategy pattern, structured ingestion) but still show `GraphSchema` / `schema=` in getting-started, which the 1.4.0 source deprecates.[^docs-architecture][^docs-getting-started]
  > `GraphRAG SDK v2 follows a strategy-based pipeline architecture.` (`https://docs.falkordb.com/graphrag/architecture`)
  > `This document is the comprehensive configuration reference for GraphRAG SDK v2.` (`https://docs.falkordb.com/graphrag/configuration`)

**Which API does the current README describe?** The README uses `GraphRAG(connection=ConnectionConfig(...), llm=LiteLLM(...), embedder=LiteLLMEmbedder(...))`, `ingest(text=..., document_id=...)`, `finalize()`, and `completion()`. Those signatures match the 1.4.0 source. The README quick start itself was not run because it needs an OpenAI key. The equivalent `ingest(text=..., document_id=...)` call was run and works (see below). The docs getting-started call `ingest("acme_doc", text=...)` raises `ValueError` on 1.4.0 (verified, see below).

## Verified by running code (PyPI graphrag-sdk 1.4.0)

- Imports and ABCs behave as the 1.4.0 source reads. `GraphRAG.query` is absent and `graph_store` is private (`AttributeError`).[^run-claims]
- Docs getting-started snippet `ingest("acme_doc", text=...)` fails: `ValueError: Cannot pass both 'source' and 'text'.`[^run-docs]
- Docs snippet `rag.graph_store.get_statistics()` fails with `AttributeError`. The replacement `rag.get_statistics()` works.[^run-docs]
- `finalize()` returns a `FinalizeResult` object, so the docs' dict-style `["entities_deduplicated"]` raises `TypeError`.[^run-docs]
- Default chunker: `SentenceTokenCapChunking.max_tokens` default is `512` in 1.4.0. Docs and main say `384`.[^run-claims][^docs-accuracy]

## Benchmark claims (vendor claims, not independently reproduced)

- README and docs headline: `#1 on GraphRAG-Bench — 66.09 ACC on Novel and 76.87 on Medical (benchmark)` (docs index page).[^docs-index]
  > `"Benchmark-leading accuracy"` (`https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md`)
- README table row 1: `| **1** | **FalkorDB GraphRAG SDK ◄** | **66.09** | **76.87** | **71.48** |`. Row 6 is `RAG (w rerank) (Vector RAG)` at `55.39` overall.[^readme]
- Accuracy page: `GraphRAG-SDK on FalkorDB scores 71.48 overall on GraphRAG-Bench vs 55.39 for vector RAG with reranking`. It says `Overall = (Novel ACC + Medical ACC) / 2. Overall is our own cross-dataset summary; the GraphRAG-Bench leaderboard ranks each dataset separately.`[^docs-accuracy]
- Version mismatch: README says the run was "August 2026 with `gpt-4o-mini` (Azure OpenAI) ... `text-embedding-3-large` at 1024 dimensions, text-to-Cypher retrieval enabled". The accuracy page says `GraphRAG-SDK 1.3.0`, and `enable_cypher = True (SDK default False)`, `embedding_dimension = 1024 (SDK default 256)`.[^readme][^docs-accuracy]
- Different measure: the retrieval page reports `Baseline (MultiPath only)` at `83.8%` on `100 questions scored by an LLM judge (0-10 scale)`. That is not the GraphRAG-Bench score.[^docs-retrieval]
- Chunk size is inconsistent. The accuracy page uses `SentenceTokenCapChunking, max_tokens 512` and says `SDK default at 1.3.0 (the default is now 384)`. The retrieval-tuning docs use `chunk_size=1500, chunk_overlap=200` as the "benchmark" value.[^docs-accuracy][^docs-configuration]

## Open questions

- Does the docs site describe the released 1.4.0 API or unreleased `main`? Structured ingestion (`TableMapping`, `Ontology(tables=...)`) is absent from 1.4.0 (`TableMapping` import fails). See [architecture](/graphrag-sdk/architecture.md).
- Is the 71.48 benchmark reproducible from the published package? Not tested. The reproduction package is "available on request" per the benchmark page.
- Who maintains it: all commits and issues seen are FalkorDB org, no third-party maintainers were checked.

[^readme]: `https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md`
[^gh-repo]: `https://api.github.com/repos/FalkorDB/GraphRAG-SDK`
[^gh-releases]: `https://api.github.com/repos/FalkorDB/GraphRAG-SDK/releases`
[^gh-issues]: `https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all&page=1`
[^pypi]: `https://pypi.org/pypi/graphrag-sdk/json`
[^changelog]: `https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/CHANGELOG.md`
[^repo-pyproject]: `https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/pyproject.toml`
[^src-init]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-main]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^docs-getting-started]: `https://docs.falkordb.com/graphrag/getting-started`
[^docs-architecture]: `https://docs.falkordb.com/graphrag/architecture`
[^docs-configuration]: `https://docs.falkordb.com/graphrag/configuration`
[^docs-accuracy]: `https://docs.falkordb.com/graphrag/graphrag-accuracy-benchmark`
[^docs-retrieval]: `https://docs.falkordb.com/graphrag/retrieval`
[^docs-index]: `https://docs.falkordb.com/graphrag/`
[^run-claims]: `references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt`
[^run-docs]: `references/evidence/graphrag-sdk/runs/docs-snippets-pypi140.txt`
