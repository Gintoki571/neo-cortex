---
type: Reference
title: OKF example bundles, tools and how to run them
description: Every example bundle, sample, reference-agent module, connector and third-party package found for OKF, with paths, what each demonstrates, and the validator run here.
resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
tags: [okf, tooling, examples, validator, reference-agent]
status: stable
generated: { by: claude-haiku-5-5/okf-agent, at: 2026-10-15T19:27:17Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: okf-repo
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
    title: open-knowledge-format repo (bundles/, samples/, src/, tests/)
    last_modified: 2026-08-21T20:08:36Z
  - id: kc-repo
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog
    title: knowledge-catalog repo (okf/ frozen copy, toolbox/mdcode, connectors)
    last_modified: 2026-10-15T19:15:22Z
  - id: pypi-okf
    resource: https://pypi.org/pypi/okf/json
    title: PyPI JSON for package okf
  - id: npm-okf-validator
    resource: https://registry.npmjs.org/okf-validator
    title: npm registry entry for okf-validator
evidence:
  - { file: references/evidence/okf/okfrepo-tree.json, sha256: 9eb22b075dbe9eb3682cbd0224093dd0020d135d77f2647ba7125fc7c7215877, retrieved_at: 2026-10-15T19:24:06Z, method: curl }
  - { file: references/evidence/okf/git-trees-main.json, sha256: f7072ac24dd44f02eeef75dacf0ee9b839b836e5c7830d311ebe2fb262a32e0c, retrieved_at: 2026-10-15T19:23:47Z, method: curl }
  - { file: references/evidence/okf/okfrepo-connector-gcp-knowledge-catalog.md.txt, sha256: 230a57a05f3e67a67cab952307436d9b35bf1d4479e6fc1f5962f3539619b58b, retrieved_at: 2026-10-15T19:24:15Z, method: curl }
  - { file: references/evidence/okf/mdcode-README.md.txt, sha256: c25869affebe61933c40e3be3ce50c3a6cfa2fc8018dc3ba8a3ce0c4c0a0febd, retrieved_at: 2026-10-15T19:24:28Z, method: curl }
  - { file: references/evidence/okf/okf-samples_ga4_merch_store_README.md.txt, sha256: 560f76b93f86b2769bfcc5e03df7992d72597ebd4b8669b1800c57e25c8e9a2b, retrieved_at: 2026-10-15T19:23:56Z, method: curl }
  - { file: references/evidence/okf/okf-samples_crypto_bitcoin_README.md.txt, sha256: a8f11d07ac932df028e888692d20c5d57e60cb383e029fc9156de47e49975cc8, retrieved_at: 2026-10-15T19:23:56Z, method: curl }
  - { file: references/evidence/okf/okf-samples_stackoverflow_README.md.txt, sha256: a2c15f82edb42f694eaf0a64ca8257a2e0958fda31d8f0be15d108211144f9f9, retrieved_at: 2026-10-15T19:23:56Z, method: curl }
  - { file: references/evidence/okf/okfrepo-pyproject.toml, sha256: 4926df9b322cc18fb1f77240b798143f32f0a83f9c4fa9d69d00d038946ac1a6, retrieved_at: 2026-10-15T19:24:16Z, method: curl }
  - { file: references/evidence/okf/okfrepo-CONTRIBUTING.md.txt, sha256: d9914ba5224f9123de02f2b1778c5a664d9c44faa587ce8d06cd9e64bcbc725a, retrieved_at: 2026-10-15T19:24:15Z, method: curl }
  - { file: references/evidence/okf/okfrepo-refagent-bundle_document.py, sha256: 7d9be6961b38f0fd2196e1cbe630afb1a4682e33ccd43daf3f233401ca62a43b, retrieved_at: 2026-10-15T19:25:09Z, method: curl }
  - { file: references/evidence/okf/okfrepo-refagent-bundle_index.py, sha256: 252eacfb6ee3dd3263136f4af9512030b9c3bc42bf94cc043266865110ca301d, retrieved_at: 2026-10-15T19:25:09Z, method: curl }
  - { file: references/evidence/okf/pypi-okf.json, sha256: 109babf962cba3eeafaea52de4bb1a6d4a77a1a570a6586ed15cad455b4ca4e4, retrieved_at: 2026-10-15T19:24:54Z, method: curl }
  - { file: references/evidence/okf/pypi-okf-0.1.0-wheel-contents.txt, sha256: ed880f8b29357416bfafbbf8f89498d398fcb23489bedc33c1c601882f08fa78, retrieved_at: 2026-10-15T19:25:59Z, method: command }
  - { file: references/evidence/okf/npm-okf.json, sha256: 48fe79b6337be33cc8078a08bed5f68c7a65bdaa836de805e8105fa49682a458, retrieved_at: 2026-10-15T19:24:54Z, method: curl }
  - { file: references/evidence/okf/npm-okf-validator.json, sha256: 0a75f75344cc62f584bcad576bb42aeed3174aa809364660510c4d14c8f69b64, retrieved_at: 2026-10-15T19:24:54Z, method: curl }
  - { file: references/evidence/okf/npm-open-knowledge-format.json, sha256: 6a280430824cbf9d50858c036b4ef7d4d7babf70ce87090f1bb62233f74ddaac, retrieved_at: 2026-10-15T19:24:55Z, method: curl }
  - { file: references/evidence/okf/validate_okf.py, sha256: 1cb592462e0515dd1381cf038f21beadc14f6df3457467a2fed7f6f58f98327b, retrieved_at: 2026-10-15T19:27:17Z, method: command }
  - { file: references/evidence/okf/validate_okf-run.txt, sha256: f7228dc0b9c8a39bdecccb7849b99bdf78df9ae02cd7c6c3bd5ebee26ce46a7d, retrieved_at: 2026-10-15T19:27:17Z, method: command }
  - { file: references/evidence/okf/validate_okf-upstream-bundles.txt, sha256: 8083575bb3f5696477b4b13e1c1ac0dbb5ff577d71ddff0e686e8c45b702255a, retrieved_at: 2026-10-15T19:27:17Z, method: command }
  - { file: references/evidence/okf/validate_okf-selftest.txt, sha256: c6568c72269cfd824cb4fe2279da6cc5a7b2867a4179f48503f43f2291edab8a, retrieved_at: 2026-10-15T19:27:17Z, method: command }
---

# Summary

There is **no official OKF validator or linter**. The upstream spec says "no required tooling" (`references/okf-spec-v0.2.txt` L11-12). The repo ships four example bundles, three sample configs for a reference enrichment agent, a viewer, and tests. A Dataplex connector is in the knowledge-catalog repo. Third-party packages named `okf` on PyPI and npm are placeholders or unrelated.[^okf-repo]

# 1. Example bundles (canonical repo)

Path: `bundles/<name>/` in `https://github.com/GoogleCloudPlatform/open-knowledge-format`. Each has `viz.html` (a viewer page built by the reference agent). Counts are from `okfrepo-tree.json` and the fetched `.md` files.

| Bundle | Concept / reserved `.md` (validator) | What it demonstrates (quoted from repo README) |
|---|---|---|
| `bundles/ga4/` | 9 / 5 | "GA4 e-commerce dataset" (README). One denormalised events table plus metric references. |
| `bundles/stackoverflow/` | 26 / 6 | "Stack Overflow public dataset" (README). Many tables and many joins. |
| `bundles/crypto_bitcoin/` | 9 / 6 | "Bitcoin blocks/transactions" (README). A few tightly related fact tables. |
| `bundles/acme_retail/` | 9 / 8 | "Acme Retail" (README). The only bundle that uses `Attested Computation`, `Policy`, `Skill`, and an attester (see below). |

Source: `okfrepo-readme.md` (quotes the bundle list). Validator run: `references/evidence/okf/validate_okf-upstream-bundles.txt` (fetched from main on 2026-10-15).[^okf-repo]

## acme_retail: the only spec-v0.2 example in the repo

- `bundles/acme_retail/computations/revenue-ytd.md` and `gross-margin-period.md`: `type: Attested Computation`, `runtime: bigquery`, `attester.resource: attesters/sql_equality.py`. This is the closest thing to a worked v0.2 example.
- `bundles/acme_retail/attesters/sql_equality.py`: a deterministic attester (not fetched, the `.md` only was downloaded). `attesters/index.md` lists it as: "Canonicalizes SQL and verifies BigQuery receipts against the sanctioned computation."
- `bundles/acme_retail/skills/run-on-bq.md`: `type: Skill`, the executor the computation references.
- `bundles/acme_retail/log.md`: `type: Log` frontmatter, with entries such as "**Verified** the full bundle for OKF v0.2 conformance. `human:kliu@acme` reviewed all `verified` and `sources` entries." This is the only example of a `log.md` carrying frontmatter (not forbidden by §9, not in the spec example).

## Known problems in the upstream examples (found by our checker)

- `bundles/stackoverflow/tables/votes.md` (and 7 other stackoverflow files) use `tags: Stack Overflow, votes, posts, community`, a plain string. §4.1 says `tags` is "A YAML list". The upstream commit "okf: write stackoverflow bundle tags as YAML lists (#293)" (2026-08-14) did not fix all of them (see `okf-commits-all.json`). Validator advisory, not a §11 failure.
- `bundles/stackoverflow/` has 11 concepts whose footnote `[^1]` has no matching `sources[].id`. §5.1 says the label is the join key, so this is a weak attribution (advisory).
- Upstream bundles pass §11 C1-C5 (see the run output).

# 2. Samples (canonical repo)

Each sample is a README plus `seeds.txt` (web URLs for the reference agent's web pass). Paths: `samples/ga4_merch_store/`, `samples/crypto_bitcoin/`, `samples/stackoverflow/`.

- GA4 sample: "Runs the reference agent against the public `bigquery-public-data.ga4_obfuscated_sample_ecommerce` dataset (a GA4 export from the Google Merchandise Store)..." (`okf-samples_ga4_merch_store_README.md`).
- Crypto sample: "This sample contrasts with GA4 (single denormalized events table) and Stack Overflow (many independent entities) by exercising a **small set of tightly related fact tables**..." (`okf-samples_crypto_bitcoin_README.md`).
- Stack Overflow sample: "This sample contrasts with the GA4 sample by exercising **multi-concept enrichment**: a single schema-docs page typically describes several tables..." (`okf-samples_stackoverflow_README.md`).

These samples need BigQuery and Gemini credentials to run. Nothing was run here.

# 3. Reference agent (canonical repo `src/reference_agent/`)

Python package, `pyproject.toml` name `reference-agent`, version `0.1.0`, `requires-python >=3.11`, script `reference-agent = reference_agent.cli:main` (`okfrepo-pyproject.toml`). Dependencies: `google-adk>=2.0`, `google-cloud-bigquery>=3.20`, `pyyaml>=6.0`, `pydantic>=2.0`, `markdownify>=0.11`.

| Path | Role |
|---|---|
| `cli.py`, `__main__.py`, `runner.py`, `agent.py` | Entry point and agent loop (`python -m reference_agent`). |
| `bundle/document.py` | `OKFDocument` parse/serialize, `validate()` (only `type` required), `trust_tier()`, `is_stale()`. Fetched as `okfrepo-refagent-bundle_document.py`. |
| `bundle/index.py`, `bundle/paths.py`, `bundle/synthesizer.py` | Index generation and path handling. |
| `sources/bigquery.py` | BigQuery metadata source (the "BQ pass"). |
| `web/fetcher.py`, `tools/web_tools.py` | Web fetch for the "web pass" (`--web-seed`, `--web-max-pages`). |
| `prompts/reference_instruction.md`, `prompts/web_ingestion_instruction.md` | Agent prompts. |
| `viewer/generator.py` + `templates/viz.html` + `static/viz.js`, `viz.css` | Builds a graph viewer HTML per bundle. |

Important: `document.py` loads YAML with the timestamp resolver removed, so timestamps stay text (see its docstring). Its `validate()` checks only `type`, which matches §11.2 but not the §11.1 "parseable" rule, which the loader covers.

Run (from the README, not run here):

```
python3.13 -m venv .venv
.venv/bin/pip install --index-url https://pypi.org/simple/ -e .[dev]
.venv/bin/python -m reference_agent enrich --source bq \
    --dataset bigquery-public-data.ga4_obfuscated_sample_ecommerce \
    --web-seed-file samples/ga4_merch_store/seeds.txt --out ./bundles/ga4
```

Options quoted from the GA4 sample: `--concept tables/events_` (one concept), `--no-web` (skip web pass), `--web-max-pages N` (default 100). Credentials: "set `GEMINI_API_KEY` (AI Studio) **or** use Vertex AI..." and `gcloud auth application-default login` (`okf-README.md`).[^okf-repo]

Tests: `tests/` has 7 modules (`test_bigquery_source.py`, `test_bundle_tools.py`, `test_document.py`, `test_index.py`, `test_viewer.py`, `test_web_fetcher.py`, `test_web_tools.py`). CONTRIBUTING says: "Ensure that all tests pass by running `.venv/bin/pytest`" (`okfrepo-CONTRIBUTING.md`). Not run here.

# 4. Connector: knowledge-catalog toolbox/mdcode (Dataplex)

Repo: `https://github.com/GoogleCloudPlatform/knowledge-catalog`, paths `toolbox/mdcode/` and `connectors/gcp-knowledge-catalog.md` in the OKF repo (`okfrepo-connector-gcp-knowledge-catalog.md`).

- `toolbox/mdcode` README: "Metadata as Code is a Knowledge Catalog (Dataplex) provides data stewards and data producers and AI agents with a source code artifact-based UX for metadata management and context engineering." It ships "a CLI tool (kcmd), and an MCP server" (`mdcode-README.md`).[^kc-repo]
- The OKF demo: `toolbox/mdcode/demo/okf/` with `setup.ts`, `push.ts`, `pull.ts`, `cleanup.ts`, `okf.ts`, `okf-aspect.json`, and a `catalog/` copy of the GA4 bundle (`git-trees-main.json`).
- Run per the connector doc: `bun setup.ts && bun push.ts && bun pull.ts`, then `git diff --exit-code catalog/`. Requires GCP project, `gcloud`, Bun. Build: `npm install && npm run build` (produces `dist/kcmd`).
- Its limitations, quoted: "**Only `.md` files are carried.**", "**Cross-links resolve to nothing.** Relative paths (§6.1) are stored verbatim.", "**Scale is untested** beyond the 14-file demo." Also: "Seven frontmatter keys are carried, plus the markdown body."

This connector is the only tool in the repos that round-trips OKF into a real catalog. It is not a validator. Not run here.

# 5. Frozen copy inside knowledge-catalog

`https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf`. Same spec (identical sha256), and its own README says "Stop using the copy under `okf/` in this repository." The knowledge-catalog repo has no releases or tags (`releases.json`, `tags.json`). Last commit touching `okf/` is `62651738da` (2026-08-21). The frozen copy's bundle and agent files were not diffed against the canonical repo.[^kc-repo]

# 6. Third-party packages named okf (checked 2026-10-15)

| Registry | Name | What it is (quoted from registry metadata) |
|---|---|---|
| PyPI | `okf` 0.1.0 (uploaded 2026-07-05) | Summary "A CLI for OKF", body "Currently in development." Wheel contains only `okf/__init__.py` with `def hello() -> str: return "Hello from okf!"`. No CLI entry point in the wheel (`pypi-okf-0.1.0-wheel-contents.txt`). Placeholder. |
| npm | `okf` 0.0.0 (2019-10-26) | Description "okf". Unrelated, empty. |
| npm | `okf-validator` 1.0.0 (2026-08-01) | "OKF Payment Safety Bundle Validator for PCI DSS v4 Compliance", MIT, `bin: okf-validator`. Domain-specific third-party validator for payment bundles. Not a general OKF v0.2 conformance checker. |
| npm | `open-knowledge-format` 0.0.1 | "Open Knowledge Format for AI agents. Coming soon." Placeholder. |

None of these is maintained by the OKF repo, and none is a general §11 validator. Do not depend on them. The `okf` PyPI README points to the spec in the frozen knowledge-catalog copy, not to the canonical repo.[^pypi-okf]

# 7. Local validator: `references/evidence/okf/validate_okf.py`

Written for this bundle because none exists upstream. Stdlib plus PyYAML. Checks:

- **C1** frontmatter present and parseable (§11.1).
- **C2** non-empty `type` (§11.2).
- **C3** reserved files: `index.md` has no frontmatter except bundle-root `okf_version` (§8, §12); `log.md` date headings are `YYYY-MM-DD` (§9).
- **C4** timestamps (`generated.at`, `stale_after`, `sources[].last_modified`, `usage_window`) are ISO 8601 with an explicit offset (§5 intro, L284-285).
- **C5** `verified` is a mapping or list of `{by, at}` (§5.2).
- **C6** broken links (informational, §6.1 and §11).
- Advisory notes (not failures): `tags` not a list (§4.1), footnote label without a matching `sources[].id` (§5.1), Attested Computation without `runtime` (§10.2), legacy `timestamp` / `# Citations` (§13.1), actor prefix (§7), `log.md` with frontmatter.

Run:

```
python3 -I references/evidence/okf/validate_okf.py <bundle_root>
```

Exit code 1 if any C1-C5 failure, else 0. Self-test on a planted fixture: `references/evidence/okf/validate_okf-selftest.txt` (it detects the planted errors).

Results:

- **Neo-Cortex bundle** (`/home/bindesh/neo-cortex/knowledge/`, snapshot 2026-10-15T19:30Z): `references/evidence/okf/validate_okf-run.txt`. Other agents were writing concurrently, so this is a snapshot. It fails C1 on other agents' files with invalid YAML frontmatter (for example unquoted colons in `title` in `hackathon/overview.md`, `models/embeddinggemma.md`). `AGENTS.md` at the bundle root has no frontmatter and is counted as a concept per the research protocol. The OKF concepts in `okf/` pass.
- **Upstream bundles** (fetched from the canonical repo, `main`): `references/evidence/okf/validate_okf-upstream-bundles.txt`. All four pass C1-C5. Advisories as above.

# Open questions

- Will the upstream spec adopt a JSON Schema (issue #8) or a validator? None exists as of 2026-10-15.
- Is `log.md` allowed frontmatter? §9 says nothing; upstream `acme_retail` uses it.
- Are the `attesters/sql_equality.py` and `skills/run-on-bq.md` files in the canonical repo runnable as shown? Not checked. They are not in the local evidence.

[^okf-repo]: GoogleCloudPlatform/open-knowledge-format repo. Evidence: `references/evidence/okf/okfrepo-*.json|md|py`, `okf-samples_*`, `validate_okf-upstream-bundles.txt`.
[^kc-repo]: GoogleCloudPlatform/knowledge-catalog repo. Evidence: `references/evidence/okf/mdcode-README.md.txt`, `okf-README.md`, `okf-commits-all.json`, `git-trees-main.json`.
[^pypi-okf]: PyPI `okf` 0.1.0 metadata and wheel contents. Evidence: `references/evidence/okf/pypi-okf.json`, `pypi-okf-0.1.0-wheel-contents.txt`.
