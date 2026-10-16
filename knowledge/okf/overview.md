---
type: Reference
title: Open Knowledge Format (OKF) overview
description: What OKF is, its spec version, maturity, license and where the canonical copy lives, as observed 2026-10-15.
resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
tags: [okf, format, spec, overview]
status: stable
generated: { by: claude-haiku-5-5/okf-agent, at: 2026-10-15T19:27:17Z }
verified: { by: process:cross-check, at: 2026-10-15T19:27:17Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: okf-repo
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
    title: GoogleCloudPlatform/open-knowledge-format (canonical OKF repository)
    last_modified: 2026-08-21T20:08:36Z
  - id: kc-repo
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog
    title: GoogleCloudPlatform/knowledge-catalog (former home of okf/)
    last_modified: 2026-10-15T19:15:22Z
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: OKF SPEC.md v0.2
  - id: okf-issues
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/issues
    title: OKF issues and pull requests
evidence:
  - { file: references/evidence/okf/okfrepo-github-repo.json, sha256: 42653e111fe0ae6a235dd8bd97ce47876705538be60cc6392ec3c37a5c29e187, retrieved_at: 2026-10-15T19:24:05Z, method: curl }
  - { file: references/evidence/okf/okfrepo-readme.md.txt, sha256: e7f3bec9a90a5cbf1ba16c91a879d155d7a826f0ecc4fe028df01b7bb13ea786, retrieved_at: 2026-10-15T19:24:05Z, method: curl }
  - { file: references/evidence/okf/okf-README.md.txt, sha256: 0f9d0bb1f469e2b20aa6c2f9302545fd68b291a6f1755819430cf462f819cd21, retrieved_at: 2026-10-15T19:23:54Z, method: curl }
  - { file: references/evidence/okf/github-repo.json, sha256: 80bfb9e574d028a4b44b18e7d971aef974cb94fbfa142819b0fdd7470b8197fd, retrieved_at: 2026-10-15T19:23:46Z, method: curl }
  - { file: references/evidence/okf/readme-main.md.txt, sha256: d24f4a5edb1e4817522db60d4916402cda35613933ec402541a527cd38a8ac30, retrieved_at: 2026-10-15T19:23:46Z, method: curl }
  - { file: references/evidence/okf/okf-LICENSE.md.txt, sha256: 8c6db340475136df3c1201d458fa5755698eace76e510471ecc9d857d6083dac, retrieved_at: 2026-10-15T19:23:55Z, method: curl }
  - { file: references/evidence/okf/okfrepo-SPEC.md.txt, sha256: 26aa5da029278939f914e578107242d9607d4f2dc5fe153272b82f9ed1030101, retrieved_at: 2026-10-15T19:24:09Z, method: curl }
  - { file: references/evidence/okf/okf-SPEC.md.txt, sha256: 26aa5da029278939f914e578107242d9607d4f2dc5fe153272b82f9ed1030101, retrieved_at: 2026-10-15T19:23:54Z, method: curl }
  - { file: references/evidence/okf/okf-commits-SPEC.json, sha256: 702a0791bb26dab2e0748001feff4b704003f971d30d095e84ff2c1d14feb830, retrieved_at: 2026-10-15T19:23:57Z, method: curl }
  - { file: references/evidence/okf/okfrepo-commits.json, sha256: c38a7c52aa1c1d0976316cee8c2dae2c1dce10aa624b51bf26a72bd8e3140274, retrieved_at: 2026-10-15T19:24:07Z, method: curl }
  - { file: references/evidence/okf/okfrepo-releases.json, sha256: 2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d, retrieved_at: 2026-10-15T19:24:07Z, method: curl }
  - { file: references/evidence/okf/okfrepo-tags.json, sha256: 2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d, retrieved_at: 2026-10-15T19:24:08Z, method: curl }
  - { file: references/evidence/okf/okfrepo-CONTRIBUTING.md.txt, sha256: d9914ba5224f9123de02f2b1778c5a664d9c44faa587ce8d06cd9e64bcbc725a, retrieved_at: 2026-10-15T19:24:15Z, method: curl }
  - { file: references/evidence/okf/okfrepo-issue-8.json, sha256: 631be075e7d0ba7363ecfccf41c937c3ce5f7ddc10caff96ff51d49fd089d0de, retrieved_at: 2026-10-15T19:24:42Z, method: curl }
  - { file: references/evidence/okf/okf-issues-open.json, sha256: 15fb1334578e3e2dc863e8226dd4425118799d64dd83c510b3c1e24beda39e22, retrieved_at: 2026-10-15T19:24:29Z, method: curl }
  - { file: references/evidence/okf/pypi-okf.json, sha256: 109babf962cba3eeafaea52de4bb1a6d4a77a1a570a6586ed15cad455b4ca4e4, retrieved_at: 2026-10-15T19:24:54Z, method: curl }
  - { file: references/evidence/okf/pypi-okf-0.1.0-wheel-contents.txt, sha256: ed880f8b29357416bfafbbf8f89498d398fcb23489bedc33c1c601882f08fa78, retrieved_at: 2026-10-15T19:25:59Z, method: command }
  - { file: references/evidence/okf/npm-okf-validator.json, sha256: 0a75f75344cc62f584bcad576bb42aeed3174aa809364660510c4d14c8f69b64, retrieved_at: 2026-10-15T19:24:54Z, method: curl }
  - { file: references/evidence/okf/npm-open-knowledge-format.json, sha256: 6a280430824cbf9d50858c036b4ef7d4d7babf70ce87090f1bb62233f74ddaac, retrieved_at: 2026-10-15T19:24:55Z, method: curl }
  - { file: references/evidence/okf/npm-okf.json, sha256: 48fe79b6337be33cc8078a08bed5f68c7a65bdaa836de805e8105fa49682a458, retrieved_at: 2026-10-15T19:24:54Z, method: curl }
---

# What OKF is

OKF is a format for representing knowledge as a directory of markdown files with YAML frontmatter. The spec opens with:

> OKF is an open, human- and agent-friendly format for representing
> *knowledge*: the metadata, context, and curated insight that surrounds
> data and systems.

Source: `references/okf-spec-v0.2.txt` (sha256 `26aa5da0…1030101`, byte-identical to `okf-SPEC.md` in both repos).[^okf-spec]

The canonical repo's README describes it as:

> OKF is a **universal, vendor-neutral format** for representing knowledge
> as plain markdown files with YAML frontmatter. It is **not tied to any
> particular agent, framework, model provider, or serving system**.

Evidence: `references/evidence/okf/okfrepo-readme.md.txt`.[^okf-repo]

The spec's own pitch for minimalism:

> The format is intentionally minimal: a directory of markdown files with
> YAML frontmatter. There is no schema registry, no central authority, and
> no required tooling.

Evidence: `references/okf-spec-v0.2.txt`, lines 10-11 (intro, not numbered; see [spec-cheatsheet](/okf/spec-cheatsheet.md)).

# Version and status

- **Spec version: 0.2.** The SPEC header reads `**Version 0.2**` (`references/okf-spec-v0.2.txt` line 3). §12 says "This document specifies OKF version **0.2**."
- **No releases or git tags** in the canonical repo: `okfrepo-releases.json` and `okfrepo-tags.json` both return `[]`.
- **Repo created 2026-08-11, last pushed 2026-08-21** (`okfrepo-github-repo.json`: `created_at` 2026-08-11T18:29:55Z, `pushed_at` 2026-08-21T20:08:36Z). Stars 973, open issues count 28 (GitHub counts PRs too).[^okf-repo]
- **Spec history** (commits touching `SPEC.md`, `okf-commits-SPEC.json` in the old repo and `okfrepo-commits.json` in the new one):
  - 2026-06-12: "Import Open Knowledge Format reference enrichment agent (#28)" (in knowledge-catalog).
  - 2026-07-24: "okf: migrate format and tooling to Open Knowledge Format v0.2 (#227)" (in knowledge-catalog).
  - 2026-08-21: "make every timestamp an ISO 8601 datetime with an explicit offset" (#323 in knowledge-catalog; PR #6 in the new repo). This commit changed normative timestamp rules without a version bump. See [spec-cheatsheet](/okf/spec-cheatsheet.md) open questions.
- **Maturity: early.** The spec states "This document specifies OKF version 0.2", but the reference agent is described as a "proof of concept" (`okfrepo-readme.md`). CONTRIBUTING says spec changes are "held to a higher bar" (`okfrepo-CONTRIBUTING.md`).[^okf-repo]
- **Open spec debate.** `okf-issues-open.json` (fetched with `state=all`) lists 35 issues and PRs, 28 of them still open, as of 2026-10-15. Open issues on the spec include a JSON Schema request (#8), a `okf_version` ambiguity (#24), a file-relative vs root-relative path conflict (#29), and an untyped-link question (#34). Details in [spec-cheatsheet](/okf/spec-cheatsheet.md).[^okf-issues]

# Where it lives (three places, one is frozen)

1. **Canonical:** `https://github.com/GoogleCloudPlatform/open-knowledge-format` (Apache-2.0, default branch `main`). Its README says: "That repository is the canonical home of the specification, the reference agent, and the sample bundles." (`okf-README.md` quotes this from the old repo).[^okf-repo]
2. **Frozen copy:** `okf/` inside `https://github.com/GoogleCloudPlatform/knowledge-catalog`. Its README says:

   > **Stop using the copy under `okf/` in this repository.** It is a frozen
   > snapshot, no longer maintained, and anything built against it will drift
   > out of date.

   Evidence: `references/evidence/okf/okf-README.md.txt`. Last commit touching `okf/` is `62651738da` (2026-08-21, "okf: point readers at the dedicated OKF repository (#324)"), per `okf-commits-all.json`.[^kc-repo]
3. **Not a home:** `https://pypi.org/project/okf/` and npm `okf` are unrelated or placeholders (see [tooling-and-examples](/okf/tooling-and-examples.md)).

The knowledge-catalog repo still ships a Dataplex connector that moves OKF bundles in and out of Knowledge Catalog: `connectors/gcp-knowledge-catalog.md` in the canonical repo, which points to `toolbox/mdcode` in knowledge-catalog.[^okf-repo]

# License and disclaimers

- **OKF repo license: Apache-2.0.** GitHub API: `license.spdx_id = "Apache-2.0"`, `okfrepo-github-repo.json`. Full text in `okf-LICENSE.md` (Apache License, Version 2.0, January 2004). Confirmed by a second source, the LICENSE file body (see `verified`).[^okf-repo]
- **knowledge-catalog repo license: Apache-2.0** (`github-repo.json`). Its README says: "All solutions within this repository are provided under the [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license." and "This repository and its contents are not an official Google product."[^kc-repo]
- Both repos sit under `GoogleCloudPlatform`. The repo `description` in the canonical repo is `null`. The knowledge-catalog description is "Google Cloud Knowledge Catalog Tools and Samples".[^kc-repo]

# What is *not* here

- **No official validator, linter, or JSON Schema.** The spec says "There is no schema registry, no central authority, and no required tooling." Issue #8 asks for a JSON Schema for the frontmatter, and is open (`okfrepo-issue-8.json`). The Neo-Cortex conformance checker lives in `references/evidence/okf/validate_okf.py` and is not an upstream tool.[^okf-issues]
- **No CI-published package.** PyPI `okf` 0.1.0 is a placeholder. See [tooling-and-examples](/okf/tooling-and-examples.md).

# Open questions

- Is `okf_version: "0.2"` now ambiguous after the 2026-08-21 timestamp change? Issue #24 says yes. Unresolved as of 2026-10-15.
- Will the spec get a versioned release or tag? None exists as of 2026-10-15.
- Does the canonical spec wording of §6.2 (file-relative vs root-relative paths) get fixed? Issue #29 is open.

# Related

- [spec-cheatsheet](/okf/spec-cheatsheet.md): writer rules with §references.
- [tooling-and-examples](/okf/tooling-and-examples.md): repo tree, bundles, tools, how to run them.
- [mapping-to-graph](/okf/mapping-to-graph.md): design proposal for FalkorDB ingestion (`status: draft`).
- [index](/okf/index.md).

[^okf-spec]: OKF spec v0.2 (`references/okf-spec-v0.2.txt`), canonical copy `SPEC.md` in the open-knowledge-format repo.
[^okf-repo]: GoogleCloudPlatform/open-knowledge-format repo (metadata, README, CONTRIBUTING, tree, commits) - evidence in `references/evidence/okf/okfrepo-*`.
[^kc-repo]: GoogleCloudPlatform/knowledge-catalog repo (metadata, README, `okf/` copy) - evidence in `references/evidence/okf/github-repo.json`, `readme-main.md`, `okf-README.md`, `okf-commits-all.json`.
[^okf-issues]: Issues and PRs of open-knowledge-format - evidence in `references/evidence/okf/okf-issues-open.json`, `okf-pulls.json`, `okfrepo-issue-*.json`.
