---
type: TestReport
title: anydoc 0.2.4 local test results
description: Reproduction of anydoc (Firecrawl document-to-Markdown) on self-generated .docx, .xlsx, .csv and PDF inputs through the Python and npm CLI, with raw outputs, exit codes, offline check, and the failures seen.
resource: https://github.com/firecrawl/anydoc
tags: [anydoc, test, evidence, docx, xlsx, pdf, cli]
stale_after: 2026-11-15T00:00:00Z
status: stable
generated: { by: claude-haiku-5-5/extraction-agent, at: 2026-10-15T19:45:00Z }
sources:
  - id: readme
    resource: https://raw.githubusercontent.com/firecrawl/anydoc/main/README.md
    title: anydoc README (main branch), used for the claims being tested
  - id: pypi
    resource: https://pypi.org/pypi/firecrawl-anydoc/json
    title: PyPI JSON for firecrawl-anydoc 0.2.4
  - id: npm
    resource: https://registry.npmjs.org/@firecrawl/anydoc
    title: npm registry metadata for @firecrawl/anydoc
  - id: test-commands
    resource: references/evidence/extraction/anydoc-test-commands.txt
    title: Exact commands run in this pass
  - id: make-samples
    resource: references/evidence/extraction/anydoc-test-script-make-samples.py.txt
    title: Generator script for sample.docx and sample.xlsx
  - id: make-pdfs
    resource: references/evidence/extraction/anydoc-test-script-make-pdfs.py.txt
    title: Generator script for text.pdf and scanned.pdf
  - id: py-api-output
    resource: references/evidence/extraction/anydoc-test-output-python-api.txt
    title: Python API run output
  - id: cli-output
    resource: references/evidence/extraction/anydoc-test-output-cli.txt
    title: CLI run output
  - id: pdf-output
    resource: references/evidence/extraction/anydoc-test-output-pdf.txt
    title: PDF run output
  - id: offline-check
    resource: references/evidence/extraction/anydoc-test-output-offline-check.txt
    title: Network-less run output
  - id: readme-node-check
    resource: references/evidence/extraction/anydoc-test-output-readme-node-check.txt
    title: node --check output for the README Node snippet
  - id: test-sums
    resource: references/evidence/extraction/anydoc-test-SHA256SUMS.txt
    title: SHA-256 list for test artifacts
evidence:
  - { file: references/evidence/extraction/anydoc-test-commands.txt, sha256: 15a8c788790e2ca6628ca400ed694ef7cab33780b92e7c75e350e5c2f83271b9, retrieved_at: 2026-10-15T19:26:30Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-input-sample.docx, sha256: 1758a6a87ef4656e40f1b30dc5232018faaf084ccd4eba6607acc7bc6b7e981c, retrieved_at: 2026-10-15T19:20:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-input-sample.xlsx, sha256: 159943440e3d57f5355354e1eebc85aeb838e704baea5e402a5a155eef5d9e7a, retrieved_at: 2026-10-15T19:20:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-input-text.pdf, sha256: ef195c60c2aa7d522900042d4971737a0b44ecf287f1844eb24c7c3d3ea459f8, retrieved_at: 2026-10-15T19:21:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-input-scanned.pdf, sha256: 9635de0a70c07759cb1a9eb4c3b666fff134fdd26f6911910687b4384e1e5ee1, retrieved_at: 2026-10-15T19:21:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-script-make-samples.py.txt, sha256: 502643b09e3cbd5b4bacb565b7ad0418d91d5ed335a072b981257ac8ccf15868, retrieved_at: 2026-10-15T19:20:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-script-make-pdfs.py.txt, sha256: de8c25175b9a6e3d8541a2f773db74128e85b0f2268ae23bfd4a2e8375d7933e, retrieved_at: 2026-10-15T19:21:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-script-python-api.py.txt, sha256: 75da0a74879a3441d55b6f65c50fbe1e328efe0625123fa93689b40f67a0782f, retrieved_at: 2026-10-15T19:22:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-output-python-api.txt, sha256: b4914cd70decf14c253848030802a5f6e9d7be186ae61d2d57225ee87075cd37, retrieved_at: 2026-10-15T19:22:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-output-cli.txt, sha256: b854ff489ee0ea0adcba48c64350941476d19740eaf2c8e61463668ad4abd27d, retrieved_at: 2026-10-15T19:23:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-output-xlsx.md.txt, sha256: 08842833e7851f888bcd4fad12ab520cee246306812f6fbbbd1784706b7fc593, retrieved_at: 2026-10-15T19:23:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-output-pdf.txt, sha256: b6222039c2ac59e356808e0a0532b3c002700721c5208021ae3d9f2fa33a219c, retrieved_at: 2026-10-15T19:24:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-output-offline-check.txt, sha256: 24a3ddc929911d1d5116e4a7d05b466784a3626928598e4681871f592ce091cc, retrieved_at: 2026-10-15T19:24:00Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-output-readme-node-check.txt, sha256: 839a541493a24442d5e445c86352da5e2d9c96f0eef9c2bd0408d88cbf2dc6c1, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-readme-node-snippet.txt, sha256: 17c76c91aa34cee242c76574dc333ee66be59e6d88abadc4dc81c2a858e5727c, retrieved_at: 2026-10-15T19:24:30Z, method: command }
  - { file: references/evidence/extraction/anydoc-test-SHA256SUMS.txt, sha256: 9123e15c14ab880f4a0df4825c48f5a075ce3c7d670936c675bf9863d963d3d1, retrieved_at: 2026-10-15T19:25:00Z, method: command }
---

# anydoc 0.2.4 local test results

Result of running anydoc on inputs generated in this pass. Product facts and the README claims are in [anydoc](/extraction/anydoc.md). Index: [extraction](/extraction/index.md).

Every output below came from a command in the evidence file `anydoc-test-commands.txt` ([^test-commands]). Each block is confirmed by running code, so it carries the `verified` marker. Inputs are synthetic, not real business documents.

`verified: { by: process:cross-check, at: 2026-10-15T19:24:30Z }`

## Environment

- Linux x86_64, system Python 3.14.7, npm and node from `/usr/bin`. Ran in throwaway directories under `/home/bindesh/.claude/jobs/f6d15fef/tmp/extraction/`.
- Python package: `firecrawl-anydoc==0.2.4` in a fresh venv, import name `anydoc` ([^pypi]).
- CLI: `@firecrawl/anydoc` 0.2.4 installed from npm into its own prefix, binary at `npm-anydoc/node_modules/.bin/anydoc` ([^npm]).
- Input generators (not anydoc): `python-docx` 1.2.0, `openpyxl` 3.1.5, `reportlab`, `pillow`, in a separate venv.

## Inputs

Generated by `make_samples.py` and `make_pdfs.py` ([^make-samples], [^make-pdfs]):

| File | Content | SHA-256 |
|---|---|---|
| `sample.docx` | Heading 1, a paragraph with bold and italic runs, two bullets, a 3x3 table | `1758a6a8...` |
| `sample.xlsx` | Sheet `Sales` with a 3-row table, `D2` holds formula `=B2*C2+B3*C3`; sheet `Notes` with one row | `15994344...` |
| `text.pdf` | One page, text layer: "Revenue grew by twelve percent in Q2." | `ef195c60...` |
| `scanned.pdf` | One page, image only (a PNG embedded as a PDF, no text layer) | `9635de0a...` |
| `csv` input | `a,b` / `1,2`, given on stdin | n/a |

Full hashes are in the evidence files ([^test-sums]).

## Results

### 1. Python API on .docx and .xlsx

Command: `venv-anydoc/bin/python -I scripts/run_anydoc_py.py` ([^py-api-output]). Exit 0.

Docx output, verbatim:

```
# Quarterly Test Report

This is a sample paragraph with **bold text** and *italic text*.

## Findings

- First finding: revenue grew.
- Second finding: costs fell.

| Region | Q1 | Q2 |
| --- | --- | --- |
| North | 120 | 135 |
| South | 98 | 110 |
```

Result: heading level, bold and italic runs, bullets, and the table all survived. `verified: { by: process:cross-check, at: 2026-10-15T19:22:00Z }`

Xlsx output, verbatim excerpt:

```
## Sales

| Product | Units | Price | Total |
| --- | --- | --- | --- |
| Widget | 10 | 2.5 |  |
| Gadget | 4 | 19.99 |  |

## Notes

| Note |
| --- |
| Prices are in USD |
```

Result: both sheets come out as separate GFM tables, with sheet names as headings. The `Total` column is empty for both rows. The source cell `D2` holds the formula `=B2*C2+B3*C3` written by openpyxl, which stores no cached value. anydoc emitted an empty cell. Real Excel files store cached values, so this may not show up with them. Not tested with an Excel-saved file, because neither Excel nor LibreOffice is installed here.

`verified: { by: process:cross-check, at: 2026-10-15T19:22:00Z }`

The module exported `to_markdown`, `to_markdown_bytes`, `to_document`, `format_from_bytes`, `format_from_extension`, `format_from_path`, and the exception classes `ConvertError`, `EncryptedError`, `HostedError`, `MalformedError`, `MissingPartError`, `NeedsOcrError`, `ResourceLimitError`, `UnsupportedError`, `PackageNotFoundError` ([^py-api-output]).

### 2. CLI on .docx, .xlsx, stdin CSV and an unknown file

Command block in [^cli-output]. Verbatim results:

```
$ anydoc --version
0.2.4
$ anydoc sample.docx        # exit 0, same Markdown as the Python run
$ anydoc sample.xlsx -o sample-xlsx.md   # exit 0
$ printf 'a,b\n1,2\n' | anydoc - --format csv
| a | b |
| --- | --- |
| 1 | 2 |
exit 0
$ anydoc bogus.unknown
anydoc: unsupported input: unrecognized file content and extension: .../bogus.unknown
exit 1  (path shortened)
```

Results: CLI output matches the Python output. The stdin CSV path needs `--format csv`, as the help text says. The unknown-format error goes to stderr and exits 1.

`verified: { by: process:cross-check, at: 2026-10-15T19:23:00Z }`

### 3. Text PDF and image-only PDF

Command block in [^pdf-output]:

```
$ anydoc input/text.pdf
# Text PDF Sample

Revenue grew by twelve percent in Q2.
exit 0

$ anydoc input/scanned.pdf
anydoc: page 1 of 1 needs OCR
exit 3

$ anydoc input/scanned.pdf --ocr hosted (no key, expected to call network)
anydoc: Firecrawl Parse: Unfortunately, your IP address looks like a VPN or proxy, so Firecrawl can't be used without an API key from here. Sign up ... for a free API key with 1000 credits and higher rate limits. ...
exit 1
```

Results: text PDF converted locally; the title line came out as a level-1 heading. The image-only PDF exited 3 with `needs OCR`, which matches the README and the `--help` exit-code table. With `--ocr hosted` and no key, the hosted service refused the request from this IP and asked for a key. No sign-up was done and no key was used. The message text is quoted from the service response.

`verified: { by: process:cross-check, at: 2026-10-15T19:24:00Z }`

### 4. Offline conversion

`unshare -rn anydoc sample.docx` (a new network namespace with no interfaces) printed the same Markdown and exited 0 ([^offline-check]). This supports the README claim that the Rust crate makes no network calls. The README documents the hosted OCR path as the only network use, and it was not used here. `verified: { by: process:cross-check, at: 2026-10-15T19:24:00Z }`

### 5. README Node example

The Node.js section of the README contains:

```js
const markdown = await toMarkdown('report.docx', { ocr: 'hosted' );
```

`node --check` on that line ([^readme-node-check]):

```
SyntaxError: Unexpected token ')'
exit 1
```

The object literal is missing its closing brace. A reader who copies the snippet gets a syntax error. The README snippet is quoted verbatim from [^readme].

`verified: { by: process:cross-check, at: 2026-10-15T19:24:30Z }`

## What was not run

- `.doc`, `.pptx`, `.xlsb`, `.odt`, `.ods`, `.odp`, `.epub`, `.rtf`. No inputs created. The `anydoc --help` lists these formats, which is not the same as testing them.
- Node and WASM bindings. Only the npm CLI was run. `anydoc.js` was not imported.
- Rust crate. Not built. The README's `cargo add anydoc` path was not run.
- Hosted OCR with a valid key. Not run, because no key was used.
- The vendor benchmark. Not reproduced. The corpus is private ([^readme]).
- Excel files saved by Excel or LibreOffice. Not available here.

## Summary

- anydoc 0.2.4 installs and runs locally, on Linux, from both PyPI and npm, with no key, in a network-less namespace.
- Office Markdown output was clean for docx and xlsx, with one gap: openpyxl formulas with no cached value render as empty cells.
- Scanned PDFs are refused (exit 3). The hosted fallback needs a key from a non-blocked IP.
- The README Node snippet does not parse.

## Reproduce

Run the commands in `anydoc-test-commands.txt` from the evidence directory. Use fresh directories and `python3 -I` for generator scripts, as in the research protocol.

## Related

- [anydoc](/extraction/anydoc.md)
- [LangExtract](/extraction/langextract.md)
- [Index](/extraction/index.md)

[^test-commands]: Commands run in this pass. Evidence: references/evidence/extraction/anydoc-test-commands.txt.
[^make-samples]: Input generator for docx and xlsx. Evidence: references/evidence/extraction/anydoc-test-script-make-samples.py.txt.
[^make-pdfs]: Input generator for PDFs. Evidence: references/evidence/extraction/anydoc-test-script-make-pdfs.py.txt.
[^py-api-output]: Python API run output. Evidence: references/evidence/extraction/anydoc-test-output-python-api.txt.
[^cli-output]: CLI run output. Evidence: references/evidence/extraction/anydoc-test-output-cli.txt.
[^pdf-output]: PDF run output. Evidence: references/evidence/extraction/anydoc-test-output-pdf.txt.
[^offline-check]: Network-less run output. Evidence: references/evidence/extraction/anydoc-test-output-offline-check.txt.
[^readme-node-check]: node --check output for the README snippet. Evidence: references/evidence/extraction/anydoc-test-output-readme-node-check.txt.
[^readme]: anydoc README. Evidence: references/evidence/extraction/anydoc-readme.txt.
[^pypi]: PyPI firecrawl-anydoc. Evidence: references/evidence/extraction/anydoc-pypi.json.
[^npm]: npm @firecrawl/anydoc. Evidence: references/evidence/extraction/anydoc-npm.json.
[^test-sums]: SHA-256 list for all test artifacts. Evidence: references/evidence/extraction/anydoc-test-SHA256SUMS.txt.
