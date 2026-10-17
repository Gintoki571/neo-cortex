---
type: DOX Contract
title: knowledge/ bundle contract
description: Binding work rules for the OKF knowledge bundle (DOX AGENTS.md; frontmatter keeps the bundle OKF-conformant).
---

# knowledge/

## Purpose

OKF v0.2 (Open Knowledge Format) bundle holding verified research and design knowledge for the Neo-Cortex FalkorDB hackathon project. Spec: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md (not stored here; sha256 in `references/research-protocol.md`).

## Ownership

- Every `.md` here except `AGENTS.md`, `index.md`, `log.md` is an OKF concept with YAML frontmatter and a non-empty `type`.
- Area directories: `hackathon/`, `falkordblite/`, `graphrag-sdk/`, `falkordb/`, `models/`, `extraction/`, `okf/`, `architecture/`.
- `references/` holds the research protocol (a concept) and own evidence under `references/evidence/<area>/`: outputs this project produced (run logs, probe scripts, command outputs, `SHA256SUMS.txt`, own test inputs). Third-party material is never stored here. Evidence files are never `.md`.

## Local Contracts

- Follow `references/research-protocol.md`: every important fact has a verbatim quote and evidence. Own outputs are stored in `references/evidence/<area>/` with sha256. Third-party evidence is recorded in frontmatter as `url` + `sha256` + `retrieved_at` with `redistributed: false`; the file is not kept in the repo (the repo is public).
- Third-party copies (web pages, READMEs, API JSON, model cards, docs, source code, licence texts, specs, PDFs, search results) are never committed. Body links point to the source URL. A third-party file may be stored only if a bundle check needs it to run and its licence allows redistribution with attribution; the licence notice goes next to it.
- Evidence files are immutable once recorded. To refresh, add a new dated file and update `evidence:` and `stale_after`.
- Unconfirmed facts go under `# Open questions`, never stated as fact. A nonexistent entity is recorded as a finding with failing evidence.
- `verified` uses a non-human actor only when a second independent source or executed code confirmed the claim. `human:` actors are reserved for the user.
- Links are bundle-absolute (`/area/file.md`). Each directory has an `index.md` with no frontmatter (root `index.md` may carry `okf_version`).
- Append notable bundle changes to `log.md` (newest first, ISO dates).

## Work Guidance

- Facts that can change quickly (deadlines, versions, model availability) carry `stale_after`.
- Design proposals are `status: draft` and kept separate from facts (`architecture/`).

## Verification

- `python3 -I references/evidence/okf/validate_okf.py .` from this directory must report PASS (0 conformance violations). Broken-link output (C6) is informational.
- Evidence audit: every stored `evidence[]` entry (has `file:`) must match that file's sha256 (`sha256sum -c --ignore-missing` on the `SHA256SUMS.txt` lists; `--ignore-missing` skips third-party files that are not stored). Entries with `redistributed: false` must carry `url`, `sha256` and `retrieved_at`.

## Child DOX Index

None yet. Area directories are covered by this file.
