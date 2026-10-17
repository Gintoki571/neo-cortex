---
type: Tool
title: anydoc
description: Firecrawl's Rust library and CLI (with Node, Python and WebAssembly bindings) that converts Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, CSV and text PDFs to GitHub-Flavored Markdown locally. Install, formats, output, OCR path, relation to Firecrawl, license, maturity, and usage.
resource: https://github.com/firecrawl/anydoc
tags: [document-conversion, markdown, office, pdf, rust, firecrawl, ingestion]
stale_after: 2026-11-15T00:00:00Z
status: stable
generated: { by: claude-haiku-5-5/extraction-agent, at: 2026-10-15T19:45:00Z }
sources:
  - id: readme
    resource: https://raw.githubusercontent.com/firecrawl/anydoc/main/README.md
    title: anydoc README (main branch)
  - id: repo-api
    resource: https://api.github.com/repos/firecrawl/anydoc
    title: GitHub API repository metadata, firecrawl/anydoc
    last_modified: 2026-10-15T18:08:14Z
  - id: release-api
    resource: https://api.github.com/repos/firecrawl/anydoc/releases/latest
    title: GitHub API latest release, v0.2.4
    last_modified: 2026-08-27T19:14:19Z
  - id: releases-list
    resource: https://api.github.com/repos/firecrawl/anydoc/releases
    title: GitHub API release list (14 releases)
  - id: pypi
    resource: https://pypi.org/pypi/firecrawl-anydoc/json
    title: PyPI JSON for firecrawl-anydoc
  - id: npm
    resource: https://registry.npmjs.org/@firecrawl/anydoc
    title: npm registry metadata for @firecrawl/anydoc
  - id: crates
    resource: https://crates.io/api/v1/crates/anydoc
    title: crates.io metadata for anydoc
  - id: src-cargo
    resource: https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/Cargo.toml
    title: Cargo.toml at commit 261fc25
  - id: src-python-pyproject
    resource: https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/python/pyproject.toml
    title: python/pyproject.toml at commit 261fc25
  - id: src-node-package
    resource: https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/node/package.json
    title: node/package.json at commit 261fc25
  - id: license
    resource: https://raw.githubusercontent.com/firecrawl/anydoc/main/LICENSE
    title: anydoc LICENSE
  - id: test-results
    resource: references/evidence/extraction/anydoc-test-commands.txt
    title: Local anydoc 0.2.4 test run (see anydoc-test-results.md)
evidence:
  - { name: anydoc-readme.txt, url: "https://raw.githubusercontent.com/firecrawl/anydoc/main/README.md", sha256: 0cc4383125c1640584f73b4630499529c9a7188b97c17d82065f9a9dad5b7cb6, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { name: anydoc-api-repo.json, url: "https://api.github.com/repos/firecrawl/anydoc", sha256: b51e913ae5b4523a523ac66494467d6300851eae8e1c953c1822166117a639c9, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { name: anydoc-releases-latest.json, url: "https://api.github.com/repos/firecrawl/anydoc/releases/latest", sha256: 88095be9d58b1eabca85d1b1fe41774dbd52ed7a82386903fcf094c0c627b479, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { name: anydoc-releases-list.json, url: "https://api.github.com/repos/firecrawl/anydoc/releases", sha256: bfa4e0ac16c9771e65a8e3f292436e93c85f6d0d67f6991a09d7a291897b9661, retrieved_at: 2026-10-15T19:26:00Z, method: curl, redistributed: false }
  - { name: anydoc-pypi.json, url: "https://pypi.org/pypi/firecrawl-anydoc/json", sha256: 872a20ddac73b7296d90b3dd74b7cd1fa9d1fbd689e913bff90141330d7d5475, retrieved_at: 2026-10-15T19:26:00Z, method: curl, redistributed: false }
  - { name: anydoc-npm.json, url: "https://registry.npmjs.org/@firecrawl/anydoc", sha256: 0443a456d232683be6803d977e1d94fb49c9fee9682536ee0c65a048f16628b0, retrieved_at: 2026-10-15T19:26:00Z, method: curl, redistributed: false }
  - { name: anydoc-crates.json, url: "https://crates.io/api/v1/crates/anydoc", sha256: c51db2549a1ac5ccc1a52e377854653be29e9cbce66f42ba7d8b88ab2956ac7e, retrieved_at: 2026-10-15T19:26:00Z, method: curl, redistributed: false }
  - { name: anydoc-src-Cargo.toml.txt, url: "https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/Cargo.toml", sha256: 9c1c134e3f5b1c1559f88afd8d86ab4f4db2950fc633b3f5fb2b7dc14c37b55c, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: anydoc-src-python-pyproject.toml.txt, url: "https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/python/pyproject.toml", sha256: 77df7b8ce6b9f4a8236b3de8eb053aa7a96e0e3c31d49c027068f3671cf192be, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: anydoc-src-node-package.json.txt, url: "https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/node/package.json", sha256: 5db0f5ee97f584b472cbc3026d2da67efcfe2786a0bfec65d00ba14ddb680ab3, retrieved_at: 2026-10-15T19:24:30Z, method: command, redistributed: false }
  - { name: anydoc-license.txt, url: "https://raw.githubusercontent.com/firecrawl/anydoc/main/LICENSE", sha256: 03a9e7657aac6536fb6458bd220347c4e7f85bd0a51d8d9e8528530b7a682ade, retrieved_at: 2026-10-15T19:23:41Z, method: curl, redistributed: false }
  - { file: references/evidence/extraction/anydoc-test-commands.txt, sha256: 15a8c788790e2ca6628ca400ed694ef7cab33780b92e7c75e350e5c2f83271b9, retrieved_at: 2026-10-15T19:26:30Z, method: command }
---

# anydoc

anydoc is a Rust library, CLI and set of bindings from [Firecrawl](https://firecrawl.dev) that converts office documents and PDFs to GitHub-Flavored Markdown. Test results for this document are in [anydoc test results](/extraction/anydoc-test-results.md). Index: [extraction](/extraction/index.md).

## What it is

> Fast Rust library that converts documents (Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, CSV, and PDF) into clean GitHub-Flavored Markdown. Includes bindings for Node.js, Python, and the browser (WebAssembly). (Links in the source removed.) [^readme]

It is a converter, not an LLM or extraction tool. The README's own position:

> Pure Rust, no ML models, no external services. [^readme]

GitHub reports the repository language as Rust ([^repo-api]). The Cargo manifest sets `edition = "2024"` and `rust-version = "1.88"` ([^src-cargo]).

## Language and packages

| Channel | Name and version observed | Notes | Evidence |
|---|---|---|---|
| Rust crate | `anydoc` 0.2.4, crates.io max_version `0.2.4`, 682,239 downloads | `cargo add anydoc` | [^crates] |
| Python | `firecrawl-anydoc` 0.2.4, `requires_python >=3.10`, import name `anydoc` | `pip install firecrawl-anydoc` | [^pypi] |
| Node / CLI | `@firecrawl/anydoc` 0.2.4, npm dist-tag `latest` 0.2.4 | provides the `anydoc` binary; `npx` downloads a prebuilt per-platform binary | [^npm], [^readme] |
| Browser | `@firecrawl/anydoc-wasm` | WebAssembly build, runs in the browser | [^readme] |
| Agent skill | `npx skills add firecrawl/anydoc` | ships a `convert-documents-to-markdown` skill | [^readme] |

Python wheel dependencies were not inspected; the wheel contains a compiled extension `_anydoc.abi3.so` (see [test results](/extraction/anydoc-test-results.md)).

## Install

```bash
pip install firecrawl-anydoc
npm install -g @firecrawl/anydoc      # or npx @firecrawl/anydoc report.docx
cargo add anydoc
```

Commands above are from the README and the registry pages ([^readme], [^pypi], [^npm], [^crates]). The CLI and Python package were both installed and run in the test ([^test-results]).

## Supported input formats

From the README table ([^readme]):

| Format | Extensions |
|---|---|
| Word | `.doc`, `.docx`, `.docm` |
| PowerPoint | `.ppt`, `.pps`, `.pot`, `.pptx`, `.pptm`, `.ppsx`, `.ppsm` |
| Excel | `.xls`, `.xlsx`, `.xlsm`, `.xlsb` |
| OpenDocument | `.odt`, `.ods`, `.odp` |
| Rich Text Format | `.rtf` |
| EPUB | `.epub` |
| CSV | `.csv` |
| PDF | `.pdf` |

Format is detected from content, not extension: "The format is read from the file content, using the marker its specification designates" ([^readme]). CSV has no marker, so the extension or an explicit `--format csv` names it ([^readme]).

Tested here: `.docx`, `.xlsx`, `.csv` (stdin), text `.pdf`, image-only `.pdf` ([^test-results]). Not tested: `.doc`, `.pptx`, `.xlsb`, `.odt`, `.epub`, `.rtf`.

## Output

Output is one GFM Markdown string per document. The README lists the structure it keeps: headings with anchors, bold/italic/strikethrough, code, links, lists "with the source's own numbering", tables "with merged cells and header rows", footnotes and endnotes, and speaker notes ([^readme]). Equations become LaTeX: "Word and PowerPoint (OMML), OpenDocument and EPUB (MathML), and RTF equations convert to GitHub-flavored math" ([^readme]).

Embedded images render as alt text in the Markdown. Raw bytes stay available on the document model: "Images and embedded objects render as their alt text in the Markdown, and the raw bytes stay available on the document model, tagged with their media type." ([^readme]).

Lower-level API: `to_document` returns the shared document model before serialisation ([^readme]).

## Usage

CLI, from `anydoc --help` in the test run ([^test-results]):

```
anydoc <file> [options]
anydoc - [options] < file
  -o, --output <path>    Write the Markdown to <path> instead of stdout
  -f, --format <format>  Name the input format instead of detecting it
  --ocr <mode>           reject (default) exits 3; hosted sends the document to Firecrawl Parse
  --api-key <key>        Firecrawl API key for --ocr hosted, else FIRECRAWL_API_KEY, else keyless
  --api-url <url>        ...
```

Exit codes: `0` success, `1` could not read or convert, `2` usage error, `3` pages of a PDF need OCR ([^test-results]).

Python:

```python
import anydoc
markdown = anydoc.to_markdown("report.docx")
markdown = anydoc.to_markdown_bytes(data, "csv")
document = anydoc.to_document(data)
```

([^readme]). Node: `toMarkdown`, `toMarkdownBytes`, `toDocument` ([^readme]). Rust: `anydoc::to_markdown(path)` returning `Result` with `ConvertError` variants `Unsupported`, `NeedsOcr`, `Malformed`, `Encrypted`, `ResourceLimit`, `MissingPart`, `Io` ([^readme]).

Note: the Node example in the README has a syntax error. It is reproduced verbatim in [^readme] as `const markdown = await toMarkdown('report.docx', { ocr: 'hosted' );`. `node --check` rejects it with `SyntaxError: Unexpected token ')'` ([^test-results]). The object literal is missing its closing brace.

## API keys, local processing, OCR

- Default conversion is local and needs no key: "The Rust crate has no `ocr` option and never makes network calls." ([^readme]). Confirmed by running the CLI in a network-less namespace ([^test-results]).
- Scanned pages are not OCR'd locally: "anydoc reads text-based PDFs locally but does no OCR, so a PDF with scanned or image-only pages fails with `NeedsOcr`." ([^readme]).
- Hosted OCR is opt-in and sends the whole document: "Only documents that need OCR leave the machine, and the whole document goes, since Parse has no page selection." ([^readme]).
- Key: "No signup needed; set `FIRECRAWL_API_KEY` for higher limits." ([^readme]). In the test, `--ocr hosted` without a key was refused from this IP with a message asking for a key ([^test-results]). No account was created and no key was used.
- PDF text extraction uses `pdf-inspector`, declared in `Cargo.toml` ([^src-cargo]) and linked in the README to github.com/firecrawl/pdf-inspector ([^readme]).

## Relation to Firecrawl

anydoc is "Built by [Firecrawl]" ([^readme]). The README describes it as the conversion layer behind the hosted Firecrawl Parse service:

> It powers [Firecrawl Parse](https://firecrawl.dev/parse), so if you'd rather not run it yourself, the hosted API gives you the same conversion plus our OCR models for the scanned pages anydoc can't read on its own. [^readme]

So the local library and the hosted Parse API share the conversion code. The only thing the hosted path adds is OCR for scanned pages. The README calls the hosted OCR "Firecrawl Parse" and says it "OCRs them and returns the same Markdown" ([^readme]).

## License

MIT. Confirmed by the repository API (`spdx_id: MIT`), the LICENSE file, `Cargo.toml`, `python/pyproject.toml`, `node/package.json`, and the npm and PyPI metadata ([^repo-api], [^license], [^src-cargo], [^src-python-pyproject], [^src-node-package], [^npm], [^pypi]). The crates.io `license` field returned null, so the Cargo manifest is the source for the crate ([^crates], [^src-cargo]). `verified: { by: process:cross-check, at: 2026-10-15T19:26:00Z }`

## Maturity

Repository metadata at observation time ([^repo-api]):

- Created 2026-08-03T16:36:14Z, pushed 2026-08-28T02:13:16Z. The project is about ten weeks old at observation. Repository `updated_at` was 2026-10-15T18:08:14Z.
- 22,864 stars, 1,470 forks, 109 open issues. Topics list empty. Not archived.
- Releases: 14 in the release list, from `v0.1.1` (2026-08-04) to `v0.2.4` (2026-08-27) ([^releases-list]). Latest is `v0.2.4`, titled "Scanned pages" ([^release-api]). Release titles include "Checkboxes" (v0.2.3) and "Prices stay prices" (v0.2.2). Release notes were not read in full.

The star count is high for a repository this young. Treat it as a fact about the page, not as evidence of production use.

Vendor benchmark, as stated in the README: 100 documents across fourteen formats, scored by an LLM judge. "an LLM judge (Claude Sonnet 5) compares two tools' outputs blind against ground truth" ([^readme]). The corpus "is not redistributable and is not in the repo" ([^readme]). The benchmark therefore cannot be reproduced from this repository alone. Treat its scores as vendor-reported.

## Known limitations

- No OCR. Image-only or scanned PDF pages fail with exit 3 (CLI) or `NeedsOcr` (library) ([^readme], [^test-results]).
- Hosted OCR works without signup for limited use: "No signup needed; set `FIRECRAWL_API_KEY` for higher limits." ([^readme]). From the test IP, the service refused without a key ([^test-results]).
- Formula cells: an `.xlsx` written by openpyxl, which stores no cached result, rendered the formula cell as empty. Excel-saved files carry cached values, so this may not affect real files. Not tested with Excel-saved input ([^test-results]).
- Images appear as alt text, not as embedded files, in the Markdown output ([^readme]).
- Benchmark is vendor-run and the corpus is private ([^readme]).

## Open questions

- Behaviour on Excel-saved `.xlsx` files with cached formula values. Needs a file from Excel or LibreOffice, neither installed here.
- Behaviour on `.pptx`, `.odt`, `.epub` and `.rtf` input. Not tested.
- Whether the Python wheel's native extension is the same code as the Node and WASM builds. Not checked.
- The hosted OCR path with a valid key. Not tested, because no key was used.

## Related

- [anydoc test results](/extraction/anydoc-test-results.md)
- [LangExtract](/extraction/langextract.md), which consumes plain text and could take anydoc Markdown as input
- [Index](/extraction/index.md)

[^readme]: anydoc README (main). Evidence: https://raw.githubusercontent.com/firecrawl/anydoc/main/README.md.
[^repo-api]: GitHub API, firecrawl/anydoc. Evidence: https://api.github.com/repos/firecrawl/anydoc.
[^release-api]: GitHub latest release v0.2.4. Evidence: https://api.github.com/repos/firecrawl/anydoc/releases/latest.
[^releases-list]: GitHub release list. Evidence: https://api.github.com/repos/firecrawl/anydoc/releases.
[^pypi]: PyPI firecrawl-anydoc. Evidence: https://pypi.org/pypi/firecrawl-anydoc/json.
[^npm]: npm @firecrawl/anydoc. Evidence: https://registry.npmjs.org/@firecrawl/anydoc.
[^crates]: crates.io anydoc. Evidence: https://crates.io/api/v1/crates/anydoc.
[^src-cargo]: Cargo.toml at 261fc25. Evidence: https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/Cargo.toml.
[^src-python-pyproject]: python/pyproject.toml at 261fc25. Evidence: https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/python/pyproject.toml.
[^src-node-package]: node/package.json at 261fc25. Evidence: https://github.com/firecrawl/anydoc/blob/261fc257d17c3eab0f673be31c408fd9fdc2171a/node/package.json.
[^license]: LICENSE. Evidence: https://raw.githubusercontent.com/firecrawl/anydoc/main/LICENSE.
[^test-results]: Local test run of anydoc 0.2.4. See [anydoc test results](/extraction/anydoc-test-results.md) and references/evidence/extraction/anydoc-test-*.
