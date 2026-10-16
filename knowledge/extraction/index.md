# Extraction area index

Research on document and text extraction tools for the Neo-Cortex project: an LLM-based structured extractor (LangExtract), its pipeline, and a document-to-Markdown converter (anydoc). Research protocol: [/references/research-protocol.md](/references/research-protocol.md). Spec: [/references/okf-spec-v0.2.txt](/references/okf-spec-v0.2.txt).

## Concepts

- [LangExtract](/extraction/langextract.md): what it is, `lx.extract` signature, few-shot format, char-offset grounding, chunking and multi-pass, providers, output, license, version, limits.
- [LangExtract pipeline design](/extraction/langextract-pipeline-design.md): stage-by-stage map of the pipeline, source interfaces, and what can be reused with GLiNER2 instead of an LLM.
- [anydoc](/extraction/anydoc.md): Firecrawl's Rust converter (with Node, Python and WASM bindings) for office files and PDFs to Markdown. Formats, install, OCR path, license, maturity.
- [anydoc test results](/extraction/anydoc-test-results.md): local run on generated docx, xlsx, csv and PDF inputs, with raw outputs and failures.

## Headline findings

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

## Evidence

All raw sources and test artifacts: `/references/evidence/extraction/` (checksums in `SHA256SUMS.txt` in the same folder).
