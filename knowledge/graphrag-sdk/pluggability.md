---
type: Concept
title: GraphRAG SDK pluggability (LLM, embedder, NER, chunker, resolver, retriever)
description: How graphrag-sdk 1.4.0 lets you replace the LLM, embedder, entity extractor (GLiNER or any non-LLM NER), chunker, resolver, retriever and reranker; base classes, signatures, and which swaps were executed.
resource: https://docs.falkordb.com/graphrag/strategies
tags: [graphrag, falkordb, pluggability, llm, embedder, gliner, extraction]
status: stable
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/graphrag-sdk-agent, at: 2026-10-15T20:10:00Z }
sources:
  - id: docs-strategies
    resource: https://docs.falkordb.com/graphrag/strategies
    title: Strategy Reference (FalkorDB docs)
  - id: docs-providers
    resource: https://docs.falkordb.com/graphrag/providers
    title: LLM and Embedder Providers for GraphRAG SDK
  - id: docs-configuration
    resource: https://docs.falkordb.com/graphrag/configuration
    title: GraphRAG SDK Configuration Reference
  - id: docs-extraction
    resource: https://docs.falkordb.com/graphrag/extraction
    title: GraphRAG SDK Entity & Relation Extraction
  - id: docs-architecture
    resource: https://docs.falkordb.com/graphrag/architecture
    title: GraphRAG SDK Pipeline Architecture
  - id: src-pypi
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: graphrag-sdk 1.4.0 source (installed copy; files in evidence)
  - id: llms-txt
    resource: https://docs.falkordb.com/llms.txt
    title: FalkorDB docs index (llms.txt)
  - id: docs-getting-started
    resource: https://docs.falkordb.com/graphrag/getting-started
    title: "Getting Started (FalkorDB docs)"
  - id: pypi
    resource: https://pypi.org/pypi/graphrag_sdk/json
    title: "PyPI JSON for graphrag_sdk"
  - id: run-claims
    resource: references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt
    title: "local run output (this research)"
  - id: run-e2e
    resource: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt
    title: "local run output (this research)"
  - id: run-gliner-offline
    resource: references/evidence/graphrag-sdk/runs/gliner-default-offline.txt
    title: "local run output (this research)"
  - id: run-gliner-online
    resource: references/evidence/graphrag-sdk/runs/gliner-default-online.txt
    title: "local run output (this research)"
  - id: src-base
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-entity
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-extraction
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-main-api
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-main-finalize
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-storage
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
evidence:
  - { name: strategies.txt, url: "https://docs.falkordb.com/graphrag/strategies", url_basis: inferred, sha256: 406b86359245d89b44a5d991f87fc9bfca12711056decb7109cd7bec100bf9e6, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: providers.txt, url: "https://docs.falkordb.com/graphrag/providers", url_basis: inferred, sha256: 8b251d63efb7c92f809279639493b19af0ce844d45f48edef3e04a1af3167d21, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: configuration.txt, url: "https://docs.falkordb.com/graphrag/configuration", url_basis: inferred, sha256: 236cc936b838ef8845465aa04f852feea891a7d434c91cd35939be389045b7de, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: extraction.txt, url: "https://docs.falkordb.com/graphrag/extraction", url_basis: inferred, sha256: f7427360df531a63bb0dc09e097a42549ed05df942d821704d84b26268ef55f2, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: architecture.txt, url: "https://docs.falkordb.com/graphrag/architecture", url_basis: inferred, sha256: 4e67b3f2efb2668dfcf75e1b28cd40cb190c7aad9a8a760e0b499192499fc5c7, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: entity_extractors.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: b71221bc4957898fc400c3a71dff5dd5cafea9ada5f8a4ff6af79d377b90d0bc, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { name: core_providers_base.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: 4e8e2068eff184f7caad5e4fc3d46875a3004d255894b5a1c3954177ce2c575b, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { name: graph_extraction.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: b6c15b2c371310fe0647f954b1a979a2088f47d9a1ee1de8ae90536dd60cec67, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { file: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt, sha256: 020b6a709e6bb4c6c18a3ae7c5e5c592e926dab1f9ca783dfb1889ac5224f283, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/sdk-e2e-inject-pypi140.txt, sha256: 955ef9ec6257e43575a3699f1ac3e5b48655725e63bd10500e3a15b398da101b, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/gliner-default-offline.txt, sha256: afc636e791cdff86700860743c85f218eca617dae2e9d6d0b7224bb98d07527e, retrieved_at: 2026-10-15T20:05:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/gliner-default-online.txt, sha256: 46e1cd0eeea96816535b2e4dbad6195d7256eb398272f8e81c2dcda17ddac4cd, retrieved_at: 2026-10-15T20:05:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt, sha256: 020b6a709e6bb4c6c18a3ae7c5e5c592e926dab1f9ca783dfb1889ac5224f283, retrieved_at: 2026-10-15T20:00:00Z, method: command }
verified: { by: process:cross-check, at: 2026-10-15T20:00:00Z }
---

# GraphRAG SDK pluggability

**Short answer.** The SDK is built around abstract base classes. You can replace the LLM, the embedder, the entity extractor (NER), the chunker, the resolver, the retriever and the reranker by subclassing an ABC and passing your object to the constructor or to `ingest()` / `completion()`. A non-LLM NER backend is supported as an `EntityExtractor` subclass. A local embedding model is supported as an `Embedder` subclass. Both were run end to end in this research with stand-in implementations (see the table). GLiNER is the built-in default NER, but its real model could not be loaded in this sandbox, so it is not verified end to end.

Related: [architecture](/graphrag-sdk/architecture.md), [retrieval-strategies](/graphrag-sdk/retrieval-strategies.md), [db-connectivity](/graphrag-sdk/db-connectivity.md).

## Summary table

| Concern | Base class (1.4.0) | Built-ins | Custom subclass run? |
|---|---|---|---|
| LLM | `LLMInterface` (abstract `invoke`) | `LiteLLM`, `OpenRouterLLM` | Yes: `FakeLLM` (deterministic, no network) |
| Embedder | `Embedder` (abstract `model_name`, `embed_query`) | `LiteLLMEmbedder`, `OpenRouterEmbedder` | Yes: `HashEmbedder` (256-dim, deterministic) |
| NER step (GraphExtraction step 1) | `EntityExtractor` (abstract `extract_entities`) | `GLiNERExtractor` (default), `LLMExtractor` | Yes, non-LLM: `RegexExtractor` |
| Whole extraction | `ExtractionStrategy` (abstract `extract`) | `GraphExtraction` | Not run |
| Chunking | `ChunkingStrategy` (abstract `chunk`) | `FixedSizeChunking` (default), `SentenceTokenCapChunking`, `ContextualChunking`, `CallableChunking`, `StructuralChunking` | Not run (`CallableChunking` is the adapter for any `text -> list[str]`) |
| Loading | `LoaderStrategy` (abstract `load`) | `TextLoader`, `PdfLoader`, `MarkdownLoader` | Not run |
| Resolution | `ResolutionStrategy` (abstract `resolve`) | `ExactMatchResolution` (ingest default), `LLMVerifiedResolution` (main: finalize default) | Not run. On 1.4.0 `finalize()` uses `EntityDeduplicator`, not a `ResolutionStrategy` |
| Retrieval | `RetrievalStrategy` (template method, abstract `_execute`) | `MultiPathRetrieval` (default), `LocalRetrieval` | Not run (default `MultiPathRetrieval` ran) |
| Reranking | `RerankingStrategy` (abstract `rerank`) | `CosineReranker` | Not run |
| Coreference | `CorefResolver` | `FastCorefResolver` (extra `fastcoref`) | Not run |

Docs statement: `Every swappable strategy ABC and its built-in implementations.`[^docs-strategies]

## LLM

Docs: `GraphRAG SDK uses two provider types: LLM (for text generation and extraction) and Embedder (for vector embeddings). Both are abstract base classes with built-in implementations for LiteLLM and OpenRouter.`[^docs-providers]

Base class (1.4.0 `core/providers/base.py`): `LLMInterface(ABC)`, constructor `__init__(self, model_name: str, model_params: dict[str, Any] | None = None, max_concurrency: int = 12)`, abstract method `invoke(self, prompt: str, **kwargs: Any) -> LLMResponse`. Optional overrides: `ainvoke`, `ainvoke_messages`, `invoke_with_model`, `abatch_invoke`.[^src-base][^docs-providers]

Enforcement check (ran): `LLMInterface` subclass without `invoke` raises `TypeError: Can't instantiate abstract class _NoInvoke without an implementation for abstract method 'invoke'`.[^run-claims]

Built-in providers: `LiteLLM` ("Azure OpenAI, OpenAI, Anthropic, Cohere, 100+" per the providers table) and `OpenRouterLLM`. Docs: `LiteLLM provides a unified interface to 100+ LLM providers. It is the recommended default.` Local models are a custom subclass: `Custom LLMInterface wrapping Ollama, vLLM, etc.`[^docs-providers]

The docs index says `100+ LLM providers via LiteLLM (OpenAI, Azure, Anthropic, Cohere, Ollama, and more)`. Ollama is not tested here.[^llms-txt]

Note: `LiteLLM` and `LiteLLMEmbedder` construct without a key (no network call). Provider calls were not made.[^run-claims]

## Embedder

Base class (1.4.0 `core/providers/base.py`): `class Embedder(ABC)`, with abstract property `model_name` and abstract method `embed_query(self, text: str, **kwargs: Any) -> list[float]`. Its docstring: `Subclasses must implement ``embed_query`` and expose a`` ``model_name`` property identifying the model (used for graph config validation).`[^src-base]

Docs on the model name: `The model_name property is used by the graph config node to validate that the same embedding model is used for ingestion and retrieval.`[^docs-providers]

Dimension: `embedding_dimension` (default 256) is passed to `GraphRAG`. Docs: `If your embedding model produces a different dimensionality (e.g., 1024, 1536, or 3072), set embedding_dimension accordingly.`[^docs-getting-started]

Batch: docs say `The embed_documents() and aembed_documents() methods are critical for performance.`[^docs-providers]

Verified run: a custom 256-dim `HashEmbedder(Embedder)` ingested and retrieved text, created vector indexes at `dimension: 256`, and returned nearest chunks (`runs/sdk-e2e-tcp-pypi140.txt`, `db.indexes` rows).[^run-e2e]

**Sentence-transformers / EmbeddingGemma.** The docs list `Local embeddings | Custom Embedder wrapping sentence-transformers` as the supported route.[^docs-providers] A real sentence-transformers model was not loaded in this research (no embedding model in the local HF cache, and `sentence-transformers` not installed). The `Embedder` seam is verified with the hashing stand-in only. Treat the EmbeddingGemma path as **unverified**. The dimension must match `embedding_dimension`, and the index dimension comes from that value.[^src-storage]

## Entity extractor (NER step)

`GraphExtraction` takes an `entity_extractor`. Docs: `Custom Extractors — Subclass EntityExtractor to plug in any NER backend`.[^docs-extraction]

Base class (1.4.0 `ingestion/extraction_strategies/entity_extractors.py`). Its docstring: `Subclass this to build your own NER backend. Built-in implementations:` with `GLiNERExtractor` and `LLMExtractor`. Abstract method:[^src-entity]

```python
class EntityExtractor(ABC):
    @abstractmethod
    async def extract_entities(self, text: str, entity_types: list[str], source_chunk_id: str) -> list[ExtractedEntity]: ...
```

Constructor used by the default: `GraphExtraction(llm, *, entity_extractor=None, ...)` with `self.entity_extractor = entity_extractor or GLiNERExtractor()` (source, `https://pypi.org/project/graphrag-sdk/1.4.0/`).[^src-extraction]

Verified non-LLM extractor: `RegexExtractor(EntityExtractor)` (capitalised word runs, no model, no API) was passed as `GraphExtraction(llm=..., entity_extractor=RegexExtractor())` and ingested the sample text. Output nodes were `Alice Johnson`, `Acme Corp`, `London` with `WORKS_AT` and `LOCATED_IN` edges from the relation step (`runs/sdk-e2e-tcp-pypi140.txt`).[^run-e2e]

Important: step 2 (relationships) still calls the LLM. `GraphExtraction.__init__` requires `llm`. A non-LLM NER therefore does not remove the LLM. Only a full `ExtractionStrategy` replacement would (not run).[^src-extraction]

### GLiNER

- Default: `GLiNERExtractor` (docs: `GLiNERExtractor (default): Local GLiNER transformer model, no API calls. Returns typed entities with confidence scores and character spans.`).[^docs-strategies]
- Default model: `urchade/gliner_medium-v2.1`. The 1.4.0 class in `https://pypi.org/project/graphrag-sdk/1.4.0/` uses `model_name: str = "urchade/gliner_medium-v2.1"`. The model is loaded with `GLiNER.from_pretrained(model_name)` from the Hugging Face Hub. (Main adds a `DEFAULT_MODEL` constant; 1.4.0 does not have it.)[^src-entity]
- `GLiNER` is a hard PyPI dependency (`gliner<1,>=0.2`), so it is always installed (and pulls torch).[^pypi]
- Swap the model or threshold with `GLiNERExtractor(threshold=..., model_name=...)`. The 1.4.0 signature is `GLiNERExtractor(threshold: float = 0.75, model_name: str = "urchade/gliner_medium-v2.1")` (source). The docs' `candidate_threshold` and window parameters are main-only. A non-default model was not tested.[^docs-strategies][^run-claims]
- **Run result.** The default extractor was executed. In the first attempt the HF cache held `models--urchade--gliner_medium-v2.1` with `gliner_config.json` and `README.md` only. Offline load failed with `IncompleteSnapshotError: ... 2 file(s) are missing (model.safetensors, pytorch_model.bin)`. An online attempt sat at `Fetching 5 files: 0/5` for about 17 minutes and was stopped. **GLiNER inference was not verified in this sandbox.**[^run-gliner-offline][^run-gliner-online]

### LangExtract

Not tested. LangExtract is not an SDK integration. A wrapper would subclass `EntityExtractor` and return `ExtractedEntity` objects with `name`, `type`, `description`, `source_chunk_ids` and `spans` (the shape shown in the docs `SpaCyExtractor` example).[^docs-extraction] The LangExtract wrapper is an open question.

## Chunking

`ChunkingStrategy.chunk(self, text: str, ctx: Context) -> TextChunks` is abstract. Built-ins: `FixedSizeChunking`, `SentenceTokenCapChunking`, `ContextualChunking`, `CallableChunking` ("Use this to plug in any chunking library — LlamaIndex, LangChain, Unstructured, spaCy, or your own logic"), `StructuralChunking`.[^docs-strategies]

Verified defaults in 1.4.0: `FixedSizeChunking` 1000/100, `SentenceTokenCapChunking` `max_tokens=512`. Other chunkers not run.[^run-claims]

## Loader

`LoaderStrategy.load(self, source: str, ctx: Context) -> DocumentOutput` (abstract). Docs example `HtmlLoader` using BeautifulSoup. Not run.[^docs-strategies]

## Resolution

`ResolutionStrategy.resolve(self, graph_data: GraphData, ctx: Context) -> ResolutionResult` (abstract). `ExactMatchResolution` is the ingest default. `LLMVerifiedResolution(llm=..., embedder=...)` needs both passed explicitly when constructed by hand. Docs: `Both providers are optional but must be passed explicitly when you construct the strategy yourself`.[^docs-strategies] On 1.4.0, `api/main.py` never constructs `LLMVerifiedResolution`; `finalize()` runs `EntityDeduplicator` (exact name match, optional fuzzy). The docs' "default at finalize()" describes main (`_default_finalize_resolver`).[^src-main-api][^src-main-finalize]

## Retrieval and reranking

`RetrievalStrategy` uses the template method pattern. `search()` validates and formats; subclasses implement `_execute(query, ctx, **kwargs) -> RawSearchResult`. Constructor: `__init__(self, graph_store=None, vector_store=None)`. Docs example `GlobalRetrieval(RetrievalStrategy)` with `_execute`. Plug in per call with `rag.completion(..., strategy=...)` or at init with `retrieval_strategy=`.[^docs-strategies][^docs-configuration]

`RerankingStrategy.rerank(self, query: str, result: RetrieverResult, ctx: Context) -> RetrieverResult` (abstract). `CosineReranker(embedder=..., top_k=15)` is built in. Details are in [retrieval-strategies](/graphrag-sdk/retrieval-strategies.md).[^docs-strategies]

## Custom strategy seam

Docs: `To add a custom strategy, subclass the relevant ABC`, then `await rag.ingest("doc.txt", chunker=SemanticChunking())`. Docs also say `The same pattern applies to all 6 strategy ABCs: LoaderStrategy, ChunkingStrategy, ExtractionStrategy, ResolutionStrategy, RetrievalStrategy, RerankingStrategy.`[^docs-architecture]

## Open questions

- A real sentence-transformers or EmbeddingGemma embedder: not run (no cached weights, no install).
- GLiNER inference: not run (weights incomplete in cache; online download stalled).
- LangExtract: no wrapper written, not run.
- Chunker, loader, resolver, reranker, and whole-extraction custom classes: documented ABCs, not run.
- Ollama through LiteLLM: docs claim only, not run.

[^docs-strategies]: `https://docs.falkordb.com/graphrag/strategies`
[^docs-providers]: `https://docs.falkordb.com/graphrag/providers`
[^docs-configuration]: `https://docs.falkordb.com/graphrag/configuration`
[^docs-extraction]: `https://docs.falkordb.com/graphrag/extraction`
[^docs-architecture]: `https://docs.falkordb.com/graphrag/architecture`
[^docs-getting-started]: `https://docs.falkordb.com/graphrag/getting-started`
[^src-base]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-entity]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-main-api]: `https://pypi.org/project/graphrag-sdk/1.4.0/` (grep: no `LLMVerifiedResolution(` call; `resolver or ExactMatchResolution()` at lines 1591 and 2191)
[^src-main-finalize]: `https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/CHANGELOG.md` (#317 and #327 entries) and main `api/main.py` `_default_finalize_resolver` (not saved as evidence; `src-main-35e67a0` holds only CHANGELOG, pyproject, connection.py)
[^src-extraction]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-storage]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^pypi]: `https://pypi.org/pypi/graphrag-sdk/json`
[^llms-txt]: `https://docs.falkordb.com/llms.txt`
[^run-claims]: `references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt`
[^run-e2e]: `references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt`
[^run-gliner-offline]: `references/evidence/graphrag-sdk/runs/gliner-default-offline.txt`
[^run-gliner-online]: `references/evidence/graphrag-sdk/runs/gliner-default-online.txt`
