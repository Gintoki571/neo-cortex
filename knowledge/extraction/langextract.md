---
type: Tool
title: LangExtract
description: Google's Python library that runs an LLM over text with a prompt and few-shot examples, then grounds each extraction to a character span in the source. Facts, API, providers, output, license and limits, with evidence.
resource: https://github.com/google/langextract
tags: [extraction, llm, structured-output, grounding, python, google]
stale_after: 2026-11-15T00:00:00Z
status: stable
generated: { by: claude-haiku-5-5/extraction-agent, at: 2026-10-15T19:28:15Z }
sources:
  - id: readme
    resource: https://raw.githubusercontent.com/google/langextract/main/README.md
    title: LangExtract README (main branch)
  - id: repo-api
    resource: https://api.github.com/repos/google/langextract
    title: GitHub API repository metadata, google/langextract
    last_modified: 2026-10-15T19:07:21Z
  - id: release-api
    resource: https://api.github.com/repos/google/langextract/releases/latest
    title: GitHub API latest release, v1.7.1
    last_modified: 2026-10-08T22:57:20Z
  - id: pypi
    resource: https://pypi.org/pypi/langextract/json
    title: PyPI JSON for langextract
    last_modified: 2026-10-08T22:57:53Z
  - id: src-extraction
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/extraction.py
    title: langextract/extraction.py at commit e92a6b7 (2026-10-15)
  - id: src-data
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/data.py
    title: langextract/core/data.py at commit e92a6b7
  - id: src-base-model
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/base_model.py
    title: langextract/core/base_model.py at commit e92a6b7
  - id: src-resolver
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/resolver.py
    title: langextract/resolver.py at commit e92a6b7
  - id: src-annotation
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/annotation.py
    title: langextract/annotation.py at commit e92a6b7
  - id: src-gemini
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/gemini.py
    title: langextract/providers/gemini.py at commit e92a6b7
  - id: src-ollama
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/ollama.py
    title: langextract/providers/ollama.py at commit e92a6b7
  - id: src-router
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/router.py
    title: langextract/providers/router.py at commit e92a6b7
  - id: src-provider-readme
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/README.md
    title: langextract/providers/README.md at commit e92a6b7
  - id: src-pyproject
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/pyproject.toml
    title: pyproject.toml at commit e92a6b7
  - id: license
    resource: https://raw.githubusercontent.com/google/langextract/main/LICENSE
    title: LangExtract LICENSE (Apache 2.0 text)
  - id: test-run
    resource: references/evidence/extraction/langextract-test-output-offline-run.txt
    title: Local run of langextract 1.7.1 with a fake provider (no network)
  - id: src-chunking
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/chunking.py
    title: langextract/chunking.py at commit e92a6b7
  - id: src-io
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/io.py
    title: langextract/io.py at commit e92a6b7
evidence:
  - { name: langextract-readme.txt, url: "https://raw.githubusercontent.com/google/langextract/main/README.md", sha256: 94e3bc80c96336a97a21281b596fd2e00b28acc5410ea0920bae398c741190e4, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { name: langextract-api-repo.json, url: "https://api.github.com/repos/google/langextract", sha256: 283d461007ac576d3a9d1cadb4bcfb08d8cb6088bc5007320b99f57b834b0e91, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { name: langextract-releases-latest.json, url: "https://api.github.com/repos/google/langextract/releases/latest", sha256: 7e7ecca91d8394cde52aeac521fdac12988e6957f233b7f5f07eeec2a705a9e4, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { name: langextract-pypi.json, url: "https://pypi.org/pypi/langextract/json", sha256: a11cb3c9204727547c07b792c8090f453d099d4995f3ab8148c3d8cbe785c39b, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { name: langextract-src-langextract_extraction.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/extraction.py", sha256: 86d7dcab0c78e56be2ac943a02055f0d454783a6a76c54b351333c1a4db1e136, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_core_data.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/data.py", sha256: 1bdd05d75387858d38b0bb6975a7b7753e957b855ce4e694dabe2985cf0fc8a3, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_core_base_model.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/base_model.py", sha256: dfc7170a407af88618c916dc6bc172c0fe6283afea7e0648b705d66b3d1418ed, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_resolver.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/resolver.py", sha256: d176e5cdada24b526e0ab559f9388e35df5057ca194a2552195dd101112b7f4b, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_annotation.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/annotation.py", sha256: 37f8d5d0398bc2d194dc6099e5a8cb93a50d1207424cad24e396bb97e5f67242, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_providers_gemini.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/gemini.py", sha256: 5a30e1c23f75a46accb099fd38782a3a71fc914a3a00e59d85e86321043078fa, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_providers_ollama.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/ollama.py", sha256: 301586368ab9de065bed3b79f3004d6914dab14ca677612db6e64462097107a9, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_providers_router.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/router.py", sha256: 2eaaae485cbcc7bdc95b30210d4ab77c50d4a10304020490b5ffcbdf6ada1a50, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_providers_README.md.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/README.md", sha256: dea79dc5d4fdd1e823243e61389600aa124db5a1d1b071b147632a67f6bea988, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-pyproject.toml.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/pyproject.toml", sha256: 3f1cb85f94185c10778732b915ad88153a68ca9ccfa749880d55a1f68dc404a2, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-src-langextract_io.py.txt, url: "https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/io.py", sha256: 6718c46334306d038ab4b518e5c8a6566096faec7e6dc6244f4910d7d1b47495, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: langextract-license.txt, url: "https://raw.githubusercontent.com/google/langextract/main/LICENSE", sha256: cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { file: references/evidence/extraction/langextract-test-output-offline-run.txt, sha256: e9514af04e393c631fb6d3e0fa5820b68c70ecadecf15a87ed577ef1712d7563, retrieved_at: 2026-10-15T19:27:00Z, method: command }
  - { file: references/evidence/extraction/langextract-test-output-passes-detail.txt, sha256: 7200a4b98e6ea939ef8f8f49fd613244ff8d4f8d3256cd315c1fbf6fd247a07a, retrieved_at: 2026-10-15T19:27:40Z, method: command }
---

# LangExtract

LangExtract is a Python library for structured extraction from unstructured text with an LLM, plus a visualiser for the results. See the [pipeline design](/extraction/langextract-pipeline-design.md) for how the stages fit together, and the [index](/extraction/index.md) for the area.

## What it does

> LangExtract is a Python library that uses LLMs to extract structured information from unstructured text documents based on user-defined instructions. [^readme]

Its differentiator is grounding. Each extraction is mapped back to a span of the source text:

> Maps every extraction to its exact location in the source text, enabling visual highlighting for easy traceability and verification. [^readme]

Extractions that cannot be located in the source get `char_interval = None` (see below), so grounding is checkable rather than assumed.

## Core API

Source of the signature (`langextract/extraction.py`, commit e92a6b7):

> def extract(
>     text_or_documents: str | Iterable[data.Document],
>     prompt_description: str | None = None,
>     examples: typing.Sequence[typing.Any] | None = None,
>     model_id: str = "gemini-3.5-flash",
>     api_key: str | None = None,
>     ...
>     max_char_buffer: int = 1000,
>     ...
>     batch_length: int = 10,
>     max_workers: int = 10,
>     ...
>     extraction_passes: int = 1,
>     context_window_chars: int | None = None,
>     config: typing.Any = None,
>     model: typing.Any = None,
>     *,
>     output_schema: core_types.JsonSchema | None = None,
>     fetch_urls: bool = False,
>     ...
> ) -> list[data.AnnotatedDocument] | data.AnnotatedDocument: [^src-extraction]

Notes from the docstring:

- `model_id` default is `gemini-3.5-flash` ([^src-extraction]); the README calls it the recommended default ([^readme]).
- `fetch_urls` defaults to `False`. When `True`, http(s) strings are fetched "via `requests.get` with no sanitization (SSRF risk: internal metadata, loopback, redirects, DNS rebinding, etc.)" ([^src-extraction]).
- When `output_schema` is given, `examples` become optional: "Required unless `output_schema` is provided." ([^src-extraction])
- A pre-built `model` takes precedence over `config`, `model_id` and `api_key`. The live test printed `UserWarning: 'use_schema_constraints' is ignored when 'model' is provided.` ([^test-run]).

## Few-shot example format

Examples are `lx.data.ExampleData(text=..., extractions=[lx.data.Extraction(...)])`. Source (`langextract/core/data.py`):

> class ExampleData:
>     """A single training/example data instance for a structured prompting.
>     Attributes:
>       text: The raw input text (sentence, paragraph, etc.).
>       extractions: A list of Extraction objects extracted from the text.

[^src-data]

The `Extraction` constructor is `Extraction(extraction_class, extraction_text, *, token_interval, char_interval, alignment_status, extraction_index, group_index, description, attributes)`, with `attributes: dict[str, str | list[str]] | None` ([^src-data]).

The README guidance on examples:

> Each `extraction_text` should ideally be verbatim from the example's `text` (no paraphrasing), listed in order of appearance. [^readme]

Prompt validation runs on examples. The default level is `WARNING` ("`prompt_validation_level` ... Defaults to WARNING") ([^src-extraction]).

## Source grounding (char offsets)

`CharInterval` holds `start_pos` (inclusive) and `end_pos` (exclusive) ([^src-data]). The README states the behaviour for unmatched text:

> LangExtract automatically detects this: extractions that cannot be located in the source text will have `char_interval = None`. [^readme]

Alignment statuses are `MATCH_EXACT`, `MATCH_GREATER`, `MATCH_LESSER`, `MATCH_FUZZY` ([^src-data]). Fuzzy alignment is on by default with threshold `0.75` (docstring in [^src-extraction]: `'fuzzy_alignment_threshold' (float, 0.75)`).

Confirmed by running code (see [^test-run]): on a two-chunk text, both `Juliet` extractions got absolute offsets (5-11 and 77-83), and `source_slice` equalled the extraction text. The paraphrase `longing for Romeo`, which does not occur in the text, got `char_interval=None`.
`verified: { by: process:cross-check, at: 2026-10-15T19:27:00Z }`

## Chunking, workers, multi-pass

Chunking is sentence-first with a character budget. The `ChunkIterator` docstring says chunks "may consist of sentences or sentence fragments that can fit into the maximum character buffer that we can run inference on." [^src-chunking]

Parallelism is inside the provider, not the pipeline. Gemini and OpenAI use a `ThreadPoolExecutor` when a batch has more than one prompt and `max_workers > 1`:

> # Use parallel processing for batches larger than 1
> if len(batch_prompts) > 1 and self.max_workers > 1: [^src-gemini]

`extract()` documents the cap: "Effective parallelization is limited by min(batch_length, max_workers)." ([^src-extraction]). Ollama's `infer` does not use a thread pool in this version (checked in [^src-ollama]).

Multi-pass merges non-overlapping results with a first-pass-wins rule:

> the extraction from the earlier pass is kept (first-pass wins strategy). [^src-annotation]

Verified by running, with a deterministic fake model (output `langextract-test-output-passes-detail.txt`, [^test-run]): `extraction_passes=2` produced 6 extractions. The two aligned `Juliet` spans were deduplicated, but the two unaligned `emotion` items were appended once per pass per chunk, giving four copies. Cause: the merge only checks overlap when `char_interval is not None` ([^src-annotation]).
`verified: { by: process:cross-check, at: 2026-10-15T19:27:40Z }`

## Model providers

Built-in providers are registered by regex on model ID (`@router.register`) and exposed as entry points under `langextract.providers` ([^src-pyproject], [^src-router]).

| Provider | Selection | Key | Source |
|---|---|---|---|
| Gemini | model IDs matching `^gemini` (default provider); default model | `LANGEXTRACT_API_KEY` / `GEMINI_API_KEY`, or Vertex AI `language_model_params` | [^src-gemini] |
| OpenAI | model IDs matching `^gpt-3\.5`, `^gpt-4`, `^gpt4\.` etc. (optional extra `langextract[openai]`) | `OPENAI_API_KEY` or `LANGEXTRACT_API_KEY` | [^readme], [^src-pyproject] |
| Ollama (local) | model IDs matching `^gemma`, `^llama` (auto), or `ModelConfig(provider="ollama")`; `model_url=` sets the endpoint | none; local server at `http://localhost:11434` in the example | [^readme], [^src-ollama] |

Gemini, quoted from the README: "Using cloud-hosted models like Gemini requires an API key." [^readme]. Ollama: "LangExtract supports local inference using Ollama, allowing you to run models without API keys" [^readme].

Custom provider plugin interface:

> def infer(
>       self, batch_prompts: Sequence[str], **kwargs
>   ) -> Iterator[Sequence[types.ScoredOutput]]: [^src-base-model]

Subclass `base_model.BaseLanguageModel` (abstract `infer`), then register with `@router.register(r'^pattern', priority=N)` ([^src-router], [^src-provider-readme]). The README describes "a lightweight plugin system" with "Distribute your provider as a separate Python package" ([^readme]). The provider README gives `lx.factory.ModelConfig(model_id=..., provider="OpenAILanguageModel", provider_kwargs={...})` for explicit selection ([^src-provider-readme]).

The README also documents OpenAI-compatible endpoints via `ModelConfig(model_id=..., provider="openai", provider_kwargs={"api_key": ..., "base_url": ...})` ([^readme]).

## Output structure

- `lx.extract` returns an `AnnotatedDocument` for a string input, or a list for an iterable of documents ([^src-extraction]).
- `AnnotatedDocument` has `extractions`, `text`, `document_id` (auto `doc_<8 hex>`) ([^src-data]).
- Persistence: `lx.io.save_annotated_documents(...)` writes JSON Lines; `lx.visualize(path)` returns self-contained animated HTML ([^readme], [^src-extraction]).

Actual JSON line produced by the test run ([^test-run] artifact `langextract-test-output-annotated.jsonl.txt`), trimmed to one extraction:

> {"extraction_class": "character", "extraction_text": "Juliet", "char_interval": {"start_pos": 5, "end_pos": 11}, "alignment_status": "match_exact", "extraction_index": 1, "group_index": 0, "description": null, "attributes": {"role": "daughter"}}

`verified: { by: process:cross-check, at: 2026-10-15T19:27:00Z }`

## Versions and requirements

- Latest release on GitHub: `v1.7.1`, published 2026-10-08T22:57:20Z ([^release-api]). PyPI latest `1.7.1`, upload 2026-10-08T22:57:53 ([^pypi]).
- Python: `"requires_python":">=3.10"` in the PyPI JSON ([^pypi]).
- Core dependencies include `google-genai>=1.39.0`, `pandas>=1.3.0`, `pydantic>=1.8.0`, `requests>=2.25.0` ([^pypi]). `openai>=1.50.0` is an optional extra ([^pypi]).
- Installed cleanly into a fresh Python 3.14.7 venv with `pip install langextract==1.7.1` (see [^test-run]).
  `verified: { by: process:cross-check, at: 2026-10-15T19:27:00Z }`

## Repository and maturity

- Repository: `google/langextract`, Python, Apache-2.0, created 2025-07-08, pushed 2026-10-15, 38,957 stars, 2,718 forks, 111 open issues ([^repo-api]).

> "stargazers_count": 38957 [^repo-api]

- Citation DOI on Zenodo, cited as version 1.6.0 in the README ([^readme]).

## License

Apache-2.0 ([^repo-api], [^license]). The README adds an extra terms note: "For health-related applications, use of LangExtract is also subject to the Health AI Developer Foundations Terms of Use" ([^readme]).

## Known limitations

- Not an officially supported Google product: "This is not an officially supported Google product." ([^readme])
- Output quality depends on the model and prompt. The README says accuracy "and its adherence to the task specification are contingent upon the selected LLM, the complexity of the task, the clarity of the prompt instructions, and the nature of the prompt examples." ([^readme])
- Cost scales with passes and chunking. The `extract()` docstring says "extraction_passes=3 reprocesses tokens 3x." ([^src-extraction])
- Model lifecycle: "Gemini models have a lifecycle with defined retirement dates." ([^readme]). The default `gemini-3.5-flash` will need changing when retired.
- Multi-pass duplicates unaligned extractions (verified above).
- Parse failures drop the whole chunk by default: "By default, parsing errors log a warning and omit the affected chunk." ([^src-extraction])
- `fetch_urls` is an SSRF risk when enabled on untrusted input ([^src-extraction]).
- Ollama has no `output_schema` support: "Ollama does not currently support `output_schema`." ([^readme])
- `save_annotated_documents` does not sanitise its file name: "Not sanitized; callers passing untrusted input (e.g. in a hosted service) should validate it first" ([^src-io]).

## Open questions

- Whether `gemini-3.5-flash` and the other Gemini IDs in the README are current; the README says to check the Google model-version page. Not checked.
- Live-model accuracy and cost were not measured here. No API key was used.

## Related

- [Pipeline design and GLiNER2 reimplementation notes](/extraction/langextract-pipeline-design.md)
- [anydoc](/extraction/anydoc.md) (document-to-Markdown, a possible upstream step)
- [Index](/extraction/index.md)

[^readme]: LangExtract README. Evidence: https://raw.githubusercontent.com/google/langextract/main/README.md (sha256 94e3bc80...).
[^repo-api]: GitHub API, google/langextract. Evidence: https://api.github.com/repos/google/langextract.
[^release-api]: GitHub latest release. Evidence: https://api.github.com/repos/google/langextract/releases/latest.
[^pypi]: PyPI JSON. Evidence: https://pypi.org/pypi/langextract/json.
[^src-extraction]: langextract/extraction.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/extraction.py.
[^src-data]: langextract/core/data.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/data.py.
[^src-base-model]: langextract/core/base_model.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/base_model.py.
[^src-resolver]: langextract/resolver.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/resolver.py.
[^src-annotation]: langextract/annotation.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/annotation.py.
[^src-chunking]: langextract/chunking.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/chunking.py.
[^src-io]: langextract/io.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/io.py.
[^src-gemini]: langextract/providers/gemini.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/gemini.py.
[^src-ollama]: langextract/providers/ollama.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/ollama.py.
[^src-router]: langextract/providers/router.py at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/router.py.
[^src-provider-readme]: langextract/providers/README.md at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/README.md.
[^src-pyproject]: pyproject.toml at e92a6b7. Evidence: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/pyproject.toml.
[^license]: LICENSE. Evidence: https://raw.githubusercontent.com/google/langextract/main/LICENSE.
[^test-run]: Local run, langextract 1.7.1 in a throwaway venv, fake provider. Evidence: references/evidence/extraction/langextract-test-output-offline-run.txt and langextract-test-commands.txt.
