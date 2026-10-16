---
type: Design
title: LangExtract pipeline design and GLiNER2 reimplementation notes
description: Stage-by-stage map of the LangExtract extraction pipeline (chunk, prompt, examples, infer, parse, align, multi-pass, emit) with the source interfaces, and what could be reused if the LLM is replaced by a non-LLM extractor such as GLiNER2.
resource: https://github.com/google/langextract
tags: [extraction, pipeline, langextract, gliner2, alignment, design]
stale_after: 2026-11-15T00:00:00Z
status: draft
generated: { by: claude-haiku-5-5/extraction-agent, at: 2026-10-15T19:45:00Z }
sources:
  - id: src-extraction
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/extraction.py
    title: langextract/extraction.py at commit e92a6b7
  - id: src-annotation
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/annotation.py
    title: langextract/annotation.py at commit e92a6b7
  - id: src-resolver
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/resolver.py
    title: langextract/resolver.py at commit e92a6b7
  - id: src-base-model
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/base_model.py
    title: langextract/core/base_model.py at commit e92a6b7
  - id: src-data
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/data.py
    title: langextract/core/data.py at commit e92a6b7
  - id: src-chunking
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/chunking.py
    title: langextract/chunking.py at commit e92a6b7
  - id: src-tokenizer
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/tokenizer.py
    title: langextract/core/tokenizer.py at commit e92a6b7
  - id: src-prompting
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/prompting.py
    title: langextract/prompting.py at commit e92a6b7
  - id: src-format-handler
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/core/format_handler.py
    title: langextract/core/format_handler.py at commit e92a6b7
  - id: src-prompt-validation
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/prompt_validation.py
    title: langextract/prompt_validation.py at commit e92a6b7
  - id: src-gemini
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/gemini.py
    title: langextract/providers/gemini.py at commit e92a6b7
  - id: src-ollama
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/ollama.py
    title: langextract/providers/ollama.py at commit e92a6b7
  - id: src-io
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/io.py
    title: langextract/io.py at commit e92a6b7
  - id: longer-example
    resource: https://github.com/google/langextract/blob/main/docs/examples/longer_text_example.md
    title: LangExtract docs, longer text example
  - id: readme
    resource: https://raw.githubusercontent.com/google/langextract/main/README.md
    title: LangExtract README (main branch)
  - id: gliner2-pypi
    resource: https://pypi.org/pypi/gliner2/json
    title: GLiNER2 PyPI JSON (version 2.1.0, README in description)
    last_modified: 2026-10-15T19:24:00Z
  - id: test-run
    resource: references/evidence/extraction/langextract-test-output-offline-run.txt
    title: Local run of langextract 1.7.1 with fake provider
  - id: test-passes
    resource: references/evidence/extraction/langextract-test-output-passes-detail.txt
    title: Local run, extraction_passes=2 detail
  - id: src-openai
    resource: https://github.com/google/langextract/blob/e92a6b7e5e70d80a32ef55f9588c743fc6c12ffe/langextract/providers/openai.py
    title: langextract/providers/openai.py at commit e92a6b7
  - id: gliner2-github
    resource: https://api.github.com/repos/fastino-ai/GLiNER2
    title: GitHub API for fastino-ai/GLiNER2 (returned 403 rate limit; not usable)
  - id: gliner2-license
    resource: https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/LICENSE
    title: GLiNER2 LICENSE (Apache License 2.0 text)
evidence:
  - { file: references/evidence/extraction/gliner2-license-raw.txt, sha256: c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4, retrieved_at: 2026-10-15T19:24:00Z, method: curl }
  - { file: references/evidence/extraction/gliner2-github-repo.json, sha256: cd04fb995c6f474f09f6ec18238ea8b67f10f2c129fdbfa973f2d3ca0a63c5de, retrieved_at: 2026-10-15T19:24:00Z, method: curl }
  - { file: references/evidence/extraction/langextract-src-langextract_extraction.py.txt, sha256: 86d7dcab0c78e56be2ac943a02055f0d454783a6a76c54b351333c1a4db1e136, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_annotation.py.txt, sha256: 37f8d5d0398bc2d194dc6099e5a8cb93a50d1207424cad24e396bb97e5f67242, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_resolver.py.txt, sha256: d176e5cdada24b526e0ab559f9388e35df5057ca194a2552195dd101112b7f4b, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_core_base_model.py.txt, sha256: dfc7170a407af88618c916dc6bc172c0fe6283afea7e0648b705d66b3d1418ed, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_core_data.py.txt, sha256: 1bdd05d75387858d38b0bb6975a7b7753e957b855ce4e694dabe2985cf0fc8a3, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_chunking.py.txt, sha256: 0a620bc4c7c51b3dfee1ab7e9c4f9a51be3932b1b46555ae0c753ca661911941, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_core_tokenizer.py.txt, sha256: 2adf0f0e1d468d7a869314a5c3804ad0d67d4954f81e6f8bc635c51ef7c82922, retrieved_at: 2026-10-15T19:29:00Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_prompting.py.txt, sha256: 0dd7568510b54f6ef12a955140c2bc8aef37ed71116aa14805e212b7bab5d765, retrieved_at: 2026-10-15T19:29:00Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_core_format_handler.py.txt, sha256: 4cf27d4d6d861b3d626c66c47d52a556295a2cfbf7734215fdf3b25f824422ea, retrieved_at: 2026-10-15T19:29:00Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_prompt_validation.py.txt, sha256: 04e52ec0b684060660cd7edbde7201818b5d8465dcae0b2446d916e61813058a, retrieved_at: 2026-10-15T19:29:00Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_providers_gemini.py.txt, sha256: 5a30e1c23f75a46accb099fd38782a3a71fc914a3a00e59d85e86321043078fa, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_providers_openai.py.txt, sha256: 4710a8286f35931e38dec6fa7e294ccc2f7000e9c2c988b776965cf0095d0009, retrieved_at: 2026-10-15T19:29:00Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_providers_ollama.py.txt, sha256: 301586368ab9de065bed3b79f3004d6914dab14ca677612db6e64462097107a9, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-src-langextract_io.py.txt, sha256: 6718c46334306d038ab4b518e5c8a6566096faec7e6dc6244f4910d7d1b47495, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/langextract-doc-longer-text-example.txt, sha256: 52cd585f3580036bf32df1f4ca459b8f1e15ecb80a8bbaf209471650c181e6e7, retrieved_at: 2026-10-15T19:29:00Z, method: command }
  - { file: references/evidence/extraction/langextract-readme.txt, sha256: 94e3bc80c96336a97a21281b596fd2e00b28acc5410ea0920bae398c741190e4, retrieved_at: 2026-10-15T19:23:41Z, method: curl }
  - { file: references/evidence/extraction/gliner2-pypi-description.txt, sha256: 78f50ae3c773afe07941adea199311d6527a6001111b660f4110223f938feeae, retrieved_at: 2026-10-15T19:24:00Z, method: curl }
  - { file: references/evidence/extraction/pypi-gliner2.json, sha256: c133c8aafac94bfe3c18668127f6b102b6b85632ea569442e04fcade029bb02e, retrieved_at: 2026-10-15T19:24:00Z, method: curl }
  - { file: references/evidence/extraction/langextract-test-output-offline-run.txt, sha256: e9514af04e393c631fb6d3e0fa5820b68c70ecadecf15a87ed577ef1712d7563, retrieved_at: 2026-10-15T19:27:00Z, method: command }
  - { file: references/evidence/extraction/langextract-test-output-passes-detail.txt, sha256: 7200a4b98e6ea939ef8f8f49fd613244ff8d4f8d3256cd315c1fbf6fd247a07a, retrieved_at: 2026-10-15T19:27:40Z, method: command }
---

# LangExtract pipeline design and GLiNER2 reimplementation notes

This note breaks the [LangExtract](/extraction/langextract.md) pipeline into stages. For each stage it gives the source interface, what it needs from the LLM, and whether it could sit behind a non-LLM extractor such as GLiNER2. Index: [extraction](/extraction/index.md).

Source references are to commit `e92a6b7` (2026-10-15). Quotes are verbatim from the saved evidence files. Line-wrapped docstrings are quoted with the wrap removed.

## Pipeline at a glance

```
text / Document(s)
  -> 1 tokenize            RegexTokenizer (core/tokenizer.py)
  -> 2 chunk               ChunkIterator, max_char_buffer, batch_length
  -> 3 context             optional tail of previous chunk (context_window_chars)
  -> 4 prompt              prompt_description + few-shot examples (Q/A) + chunk text
  -> 5 constrain output    format handler (JSON/YAML, fences) + schema from examples or output_schema
  -> 6 infer               provider.infer(batch_prompts)   <- the only LLM call
  -> 7 parse               Resolver.resolve -> format_handler.parse_output -> ordered Extraction list
  -> 8 align               Resolver.align: exact (dp) then fuzzy (LCS) -> CharInterval + AlignmentStatus
  -> 9 multi-pass merge    extraction_passes > 1: first pass wins on overlap
  -> 10 emit               AnnotatedDocument -> JSONL (io) -> HTML (visualize)
```

The orchestration is `Annotator._annotate_documents_single_pass` and `_annotate_documents_sequential_passes` in `annotation.py` ([^src-annotation]). Stages 2, 6, 7, 8 and 9 hold the logic. Stages 1, 3 and 10 are supporting.

## Stage by stage

### 0. Entry point

`lx.extract(text_or_documents, prompt_description, examples, model_id, ..., extraction_passes, max_char_buffer, max_workers, batch_length, ...)` is in `extraction.py` ([^src-extraction]). It resolves a provider from `model` / `config` / `model_id`, then runs the annotator.

The `model` argument is the injection point for a custom backend. Its docstring: "Pre-configured language model to use for extraction. Takes precedence over all other parameters including config." ([^src-extraction]). A non-LLM model can be passed this way, but it still has to satisfy the provider interface in stage 6, and the rest of the pipeline still runs.

### 1. Tokenize

Default is `RegexTokenizer`: "Optional Tokenizer instance to use for chunking and alignment. If None, defaults to RegexTokenizer." ([^src-extraction]). Alignment is token-based: `align` takes `token_offset` and `char_offset` and sets token and char intervals ([^src-resolver]).

Reusable for GLiNER2: yes, for chunk boundaries and offset mapping. Keep one tokenizer per pipeline so there is one offset system.

### 2. Chunk

`ChunkIterator` builds chunks from sentences. When a sentence is too long, it breaks it "in a way that maximizes the chunk length while respecting newlines (if present) and token boundaries." ([^src-chunking]). `make_batches_of_textchunk` groups chunks into batches of `batch_length` ([^src-chunking]). Defaults from the `extract()` signature: `max_char_buffer=1000`, `batch_length=10`, `max_workers=10` ([^src-extraction]).

README guidance: `max_char_buffer=1000    # Smaller contexts for better accuracy` ([^readme]).

Reusable for GLiNER2: yes. This is the most reusable stage. GLiNER2 has its own long-text chunking (see below), so pick one.

### 3. Context window (optional)

`ContextAwarePromptBuilder` adds the previous chunk's tail to the prompt. Docstring: "Number of characters from the previous chunk's tail to include as context. Defaults to None (disabled)." ([^src-prompting]). It changes the prompt only; alignment is unaffected.

Reusable for GLiNER2: no. GLiNER2 scores chunks independently. Its equivalent is `chunk_overlap`.

### 4. Prompt construction

The prompt is the instruction text, then the few-shot examples as Q/A, then the chunk. Abridged from the offline run ([^test-run]):

```
Extract characters and emotions.

Examples
Q: ROMEO. But soft! What light through yonder window breaks?
A: ```json
{ "extractions": [ { "character": "ROMEO", "character_attributes": { "role": "lover" } }, ... ] }
```

Q: Lady Juliet gazed longingly at the stars, her heart aching for Romeo.
A:
```

Example objects are `ExampleData(text, extractions=[Extraction(extraction_class, extraction_text, attributes=...)])` ([^src-data]). The format handler serialises them into the Q/A form ([^src-format-handler], [^src-prompting]).

Example validation: `prompt_validation_level` defaults to `WARNING`, which "logs issues but continues" per the `extract()` docstring ([^src-extraction]). The checks live in `prompt_validation.py` ([^src-prompt-validation]).

Reusable for GLiNER2: no. GLiNER2 takes a label list or a schema, not a prompt with examples. Its README describes the input as "Schema-driven information extraction and classification" ([^gliner2-pypi]). The public API has no few-shot example format. Adapting it means fine-tuning, which the README points to Fastino for ([^gliner2-pypi]).

### 5. Constrain output

Format is JSON or YAML, with or without fences. `fence_output` is "automatically determined based on provider schema capabilities" when None ([^src-extraction]). `output_schema` "replaces example-derived provider constraints" ([^src-extraction]). Providers can store a schema through `apply_schema`, whose base implementation stores `_schema` ([^src-base-model]).

Reusable for GLiNER2: not applicable. The output is typed by construction. The useful idea to keep is the closed label set, which acts as a constraint on the classes.

### 6. Inference (the only LLM call)

The provider contract:

> def infer(
>       self, batch_prompts: Sequence[str], **kwargs
>   ) -> Iterator[Sequence[types.ScoredOutput]]: [^src-base-model]

The orchestrator calls it once per batch, then passes `scored_outputs[0].output` to the resolver ([^src-annotation]). The contract is text in, text out.

Parallelism lives here, not in the pipeline. Gemini uses a thread pool over the batch: `concurrent.futures.ThreadPoolExecutor(max_workers=min(self.max_workers, len(batch_prompts)))` ([^src-gemini]). OpenAI does the same ([^src-openai]). Ollama's `infer` has no thread pool in this version ([^src-ollama]).

Reusable for GLiNER2: yes, but only in a limited way. A string-in, string-out adapter would need to recover the text and labels from the prompt, then return JSON that stage 8 re-aligns by text search. That discards the native offsets. The recommended route is in the GLiNER2 section below.

### 7. Parse

`Resolver.resolve(input_text, suppress_parse_errors=..., **kwargs)` parses and orders the output ([^src-resolver]). The format handler accepts a dict with an `extractions` key, and also "Some models return [...] instead of {"extractions": [...]}" ([^src-format-handler]). Each item is `{<class>: <text>, <class>_attributes: {...}}`, with optional index keys ([^src-resolver]).

Failure handling: when `suppress_parse_errors` is false the resolver raises `ResolverParsingError`; otherwise it logs and returns `[]` for that chunk ([^src-resolver]). `extract()` defaults to the suppressing path ([^src-extraction]).

Reusable for GLiNER2: no, unless you keep the JSON hop. Do not push GLiNER2 spans through this text envelope.

### 8. Align (grounding)

Interface, from `AbstractResolver` ([^src-resolver]):

> Aligns extractions with source text, setting token/char intervals and alignment status.

Algorithm, from the code and the `extract()` docstring:

- Exact match first. Default `exact_alignment_algorithm` is `"dp"`; `"difflib"` is the legacy path ([^src-extraction]). The `Resolver.align` docstring still says "Uses exact matching first (difflib)" ([^src-resolver]), which is stale. The code default is `_DEFAULT_EXACT_ALGORITHM = _EXACT_ALGORITHM_DP` ([^src-resolver]). Trust the code.
- Fuzzy fallback: LCS-based. Constants are `_FUZZY_ALIGNMENT_MIN_THRESHOLD = 0.75` and `_FUZZY_ALIGNMENT_MIN_DENSITY = 1 / 3` ([^src-resolver]).
- Statuses: `MATCH_EXACT`, `MATCH_GREATER`, `MATCH_LESSER`, `MATCH_FUZZY`, or none ([^src-data]).

Observed in the local run ([^test-run]): the extraction `longing for Romeo` does not occur in the text, which says `aching for Romeo` and `longingly`. It got no interval, so fuzzy matching did not reach the threshold. The `Juliet` extractions got exact intervals at 5-11 and 77-83. `verified: { by: process:cross-check, at: 2026-10-15T19:27:00Z }`

Reusable for GLiNER2: the aligner is useful for any LLM-free extractor that returns text without offsets, for example a dictionary or rule matcher. It is not needed for GLiNER2, which returns offsets. The `CharInterval` and `AlignmentStatus` types are reusable as the output contract, but `AlignmentStatus` has no value for "model-provided span" (open question).

### 9. Multi-pass merge

`extraction_passes > 1` reruns the whole pass and calls `_merge_non_overlapping_extractions`. The rule, from its docstring: "the extraction from the earlier pass is kept (first-pass wins strategy)." ([^src-annotation]).

The overlap check runs only when `char_interval is not None`. An unaligned extraction is appended in every pass. The local run shows this ([^test-passes]): `extraction_passes=2` over the two-chunk text returned six extractions. The two aligned `Juliet` spans were deduplicated, but the unaligned `emotion` item appeared four times. `verified: { by: process:cross-check, at: 2026-10-15T19:27:40Z }`

The stated reason for passes is model variance: "This approach captures entities that might be missed in any single run due to the stochastic nature of language model generation." ([^longer-example]).

Reusable for GLiNER2: no. A deterministic extractor returns the same output each pass, so extra passes add nothing except the duplicate problem. Drop this stage for GLiNER2. If you keep it for other reasons, dedupe unaligned items as well.

### 10. Emit

Each document is yielded as an `AnnotatedDocument(document_id, extractions, text)` ([^src-annotation], [^src-data]). `save_annotated_documents` writes JSON Lines. It does not sanitise `output_name`: "Not sanitized; callers passing untrusted input (e.g. in a hosted service) should validate it first" ([^src-io]). `visualize(path)` renders self-contained animated HTML ([^readme]).

Reusable for GLiNER2: yes. The data classes, JSONL writer and visualiser are the most valuable parts for a team. They work on any `AnnotatedDocument` with `char_interval` set, whatever produced the spans.

## GLiNER2 reimplementation notes

What GLiNER2 is, from its PyPI description (version 2.1.0):

> GLiNER2 is a **schema-conditioned** encoder family for **Named Entity Recognition**, **Text Classification**, **Structured Data Extraction**, **Relation Extraction**, and **span attributes**. [^gliner2-pypi]

Claims from the same README:

> **CPU first**: fast local inference on standard hardware — no GPU required [^gliner2-pypi]

> **Privacy**: 100% local processing, zero external dependencies [^gliner2-pypi]

Install and load: "Local inference needs `pip install "gliner2[local]"`" and `AutoExtractor.from_pretrained("fastino/gliner2.5-base-v1")` ([^gliner2-pypi]). "GLiNER2 requires Python 3.10 or newer" ([^gliner2-pypi]). Hub checkpoints download on first load, so "100% local" applies after that download.

Entity call, from the README example:

```python
result = model.extract_entities(text, ["company", "person", "product", "location"])
```

Output has the shape `{'entities': {'company': ['Apple'], ...}}`, and with spans each item carries `start` and `end` ([^gliner2-pypi]).

Long text with native global offsets, verbatim from the README:

```python
result = model.extract_entities_long(
    long_text,
    ["company", "person", "product", "location"],
    chunk_size=384,
    chunk_overlap=64,
    include_spans=True,
    include_confidence=True,
)

# Spans are global offsets into long_text.
for company in result["entities"].get("company", []):
    assert long_text[company["start"]:company["end"]] == company["text"]
```

([^gliner2-pypi]). One call covers LangExtract's stages 2 (chunk), 6 (inference) and 8 (grounding).

Overlap policy: "`allow` keeps every distinct span, `nested` permits containment but rejects crossing spans, `flat`/`disallow` selects a deterministic non-overlapping set" ([^gliner2-pypi]).

Custom tokenisation for non-space languages: "You can also pass a custom callable that yields `(token, start, end)` with exclusive-end offsets into the **original** text" ([^gliner2-pypi]).

### Recommended route: bypass the text interface

LangExtract's provider interface is text in, text out. Pushing GLiNER2 through it means recovering prompts and labels in the adapter, then emitting JSON that stage 8 re-aligns by searching for the text again. That throws away the native offsets, and repeated mentions are then matched by search order instead of position.

Recommended: keep the reusable parts and replace stages 4 to 7 and 9 with one GLiNER2 call per document or chunk.

1. Chunking: use GLiNER2's `extract_entities_long` (its own chunking, global offsets), or LangExtract's `ChunkIterator` if you need its chunk boundaries.
2. Call GLiNER2 with the label list for the task, instead of a prompt.
3. Convert each returned span into `data.Extraction(extraction_class=label, extraction_text=text, char_interval=CharInterval(start_pos=start, end_pos=end), alignment_status=...)`. Check `document_text[start:end] == text` before accepting, as the README does. Pick a status convention for model-provided spans, since none exists.
4. Emit `AnnotatedDocument` and reuse `io.save_annotated_documents` and `visualize`.
5. Drop prompt building, example validation, format handler, resolver parsing, the aligner and the multi-pass merge. None of them does anything for a deterministic model.

Reusable as-is: `CharInterval`, `Extraction`, `AnnotatedDocument`, the JSONL writer and the HTML visualiser. `BaseLanguageModel` remains usable if you want the `model=` injection point for the LLM path, but a GLiNER2 object would need its own loop, because the `infer` contract does not carry labels or spans.

### What the LLM-free version does not match

- Few-shot steering is replaced by label wording or fine-tuning. The public API has no example format.
- Attributes and relations depend on the schema. GLiNER2 covers entities, classification, records, relations and span attributes, with the span-attribute support depending on the checkpoint ([^gliner2-pypi]). LangExtract's `attributes` dict is open-ended ([^src-data]).
- Grounding is native for GLiNER2, so the `char_interval = None` case from LangExtract does not occur. Text-to-span consistency is asserted in the README example, but that does not make labels correct. Wrong labels and missed spans remain possible.

### Not tested

GLiNER2 was not installed or run in this pass. Its PyPI JSON has `license: None`, so the licence is taken from the LICENSE file, which is Apache License 2.0 ([^gliner2-license]). The GitHub API call for `fastino-ai/GLiNER2` returned HTTP 403 (rate limit) and gave no repository metadata ([^gliner2-github]). The `[local]` extra pulls PyTorch, and no Hub checkpoint was downloaded. The offset assertion above is from the README, not from a run, so no `verified` marker is set for GLiNER2 facts.

## Open questions

- Which `AlignmentStatus`-like value to use for model-provided spans, since the enum has none ([^src-data]).
- Whether GLiNER2's `overlap_policy` (`allow`, `nested`, `flat`) changes results for nested entities compared with LangExtract's first-pass-wins merge. Not tested.
- Whether a labelled benchmark exists comparing LangExtract and GLiNER2 on the same corpus. Not searched in this pass.

## Related

- [LangExtract](/extraction/langextract.md)
- [anydoc](/extraction/anydoc.md), for converting office files to Markdown before extraction
- [Index](/extraction/index.md)

[^src-extraction]: langextract/extraction.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_extraction.py.txt.
[^src-annotation]: langextract/annotation.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_annotation.py.txt.
[^src-resolver]: langextract/resolver.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_resolver.py.txt.
[^src-base-model]: langextract/core/base_model.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_core_base_model.py.txt.
[^src-data]: langextract/core/data.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_core_data.py.txt.
[^src-chunking]: langextract/chunking.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_chunking.py.txt.
[^src-tokenizer]: langextract/core/tokenizer.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_core_tokenizer.py.txt.
[^src-prompting]: langextract/prompting.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_prompting.py.txt.
[^src-format-handler]: langextract/core/format_handler.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_core_format_handler.py.txt.
[^src-prompt-validation]: langextract/prompt_validation.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_prompt_validation.py.txt.
[^src-gemini]: langextract/providers/gemini.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_providers_gemini.py.txt.
[^src-openai]: langextract/providers/openai.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_providers_openai.py.txt.
[^src-ollama]: langextract/providers/ollama.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_providers_ollama.py.txt.
[^src-io]: langextract/io.py at e92a6b7. Evidence: references/evidence/extraction/langextract-src-langextract_io.py.txt.
[^readme]: LangExtract README. Evidence: references/evidence/extraction/langextract-readme.txt.
[^longer-example]: docs/examples/longer_text_example.md at main. Evidence: references/evidence/extraction/langextract-doc-longer-text-example.txt.
[^gliner2-pypi]: GLiNER2 PyPI description (version 2.1.0). Evidence: references/evidence/extraction/gliner2-pypi-description.txt and pypi-gliner2.json.
[^gliner2-license]: GLiNER2 LICENSE from raw GitHub. Evidence: references/evidence/extraction/gliner2-license-raw.txt.
[^gliner2-github]: GitHub API response for fastino-ai/GLiNER2 (rate-limited). Evidence: references/evidence/extraction/gliner2-github-repo.json.
[^test-run]: Local run of langextract 1.7.1. Evidence: references/evidence/extraction/langextract-test-output-offline-run.txt.
[^test-passes]: Local run, extraction_passes=2. Evidence: references/evidence/extraction/langextract-test-output-passes-detail.txt.
