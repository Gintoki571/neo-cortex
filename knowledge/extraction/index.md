# Extraction area index

Research on document and text extraction tools for the Neo-Cortex project: an LLM-based structured extractor (LangExtract), its pipeline, a document-to-Markdown converter (anydoc), and System 1 encoders (GLiNER family, label-set classifiers) in knowledge-graph pipelines. Research protocol: [/references/research-protocol.md](/references/research-protocol.md). Spec: [/https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).

## Concepts

- [LangExtract](/extraction/langextract.md): what it is, `lx.extract` signature, few-shot format, char-offset grounding, chunking and multi-pass, providers, output, license, version, limits.
- [LangExtract pipeline design](/extraction/langextract-pipeline-design.md): stage-by-stage map of the pipeline, source interfaces, and what can be reused with GLiNER2 instead of an LLM.
- [anydoc](/extraction/anydoc.md): Firecrawl's Rust converter (with Node, Python and WASM bindings) for office files and PDFs to Markdown. Formats, install, OCR path, license, maturity.
- [anydoc test results](/extraction/anydoc-test-results.md): local run on generated docx, xlsx, csv and PDF inputs, with raw outputs and failures.
- [System 1 models in knowledge-graph pipelines](/extraction/system1-models-in-graphs.md) (Research Note, stable): what GLiNER-family encoders and label-set classifiers do per job (extract, type, relate, resolve, verify, route, escalate, agent-written graphs), measured numbers apart from opinion, source conflicts.
- [System 1 adoption plan](/extraction/system1-adoption.md) (Design Proposal, draft): seven ranked ideas for Neo-Cortex with impact, effort, source and file, what the code already does, gaps found, and what not to adopt.

## Headline findings

- System 1: on a 10-document corpus measured by a single author, a label-set verifier over GLiNER's own edges raised F1 from 0.330 to 0.396 with no gold triple lost. Escalating uncertain edges to a bigger LLM did not help. One GLiNER2.5-base run on the POLE+O set gave relation F1 0.37 (lenient) and 0.27 (strict), and relation recall falls past roughly 400 words.
- System 1 models decide what a mention is, not whether two mentions are the same thing. Decide's same-entity judgment accepted 6 of 11 false merges.
- Neo-Cortex's soft-band resolver merge (`src/neo_cortex/resolve.py:121`) lets the judge create merges, which the code comment and the package doc say it must not. Decide this before any resolver change.

- LangExtract 1.7.1 (Apache-2.0, Python 3.10+) grounds each extraction to a character span. Unaligned extractions get `char_interval = None`. Verified by running with a fake provider.
- In multi-pass mode, LangExtract duplicates unaligned extractions once per pass. Verified by running.
- LangExtract's parallelism lives in the provider (thread pool in Gemini and OpenAI), not in the pipeline. Ollama has none in this version.
- A GLiNER2 version does not need the LLM stages. GLiNER2 returns global character spans natively, so the pipeline reduces to chunk, extract, and emit.
- anydoc 0.2.4 (MIT, Rust core, Firecrawl) converts docx and xlsx to clean GFM locally, with no key and no network. Scanned PDFs exit 3 and need OCR. Hosted OCR refused the test IP without a key.
- anydoc: openpyxl formulas with no cached value render as empty cells. Not tested with Excel-saved files.
- The anydoc README's Node example does not parse (missing `}`), verified with `node --check`.

## Open questions

- Excel-saved `.xlsx` files and the other formats anydoc claims (`.pptx`, `.odt`, `.epub`, `.rtf`) were not tested.
- GLiNER2 was not run. Its `[local]` extra pulls PyTorch and a Hub checkpoint.
- Whether the LangExtract default model `gemini-3.5-flash` and the Gemini IDs in the README are current was not checked against Google's model list.
- System 1: the GLiNER-Relex paper's text and its Table 2 disagree on the GLiNER2 row; the Decide gate F1 is 0.396 (0.404 is the hosted Jev gate); whether the base GLiNER2.5 classification head reproduces the Decide gate is untested. Details in the research note.

## Evidence

Own test artifacts are stored in `/references/evidence/extraction/` (checksums in `SHA256SUMS.txt` and `anydoc-test-SHA256SUMS.txt` in the same folder). Third-party sources, including the System 1 pages (obscura fetches of 2026-10-17, not re-fetched), are not redistributed; URL and sha256 are in each note's frontmatter.
