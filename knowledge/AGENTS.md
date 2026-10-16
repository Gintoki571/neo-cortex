---
type: DOX Contract
title: knowledge/ bundle contract
description: Binding work rules for the OKF knowledge bundle (DOX AGENTS.md; frontmatter keeps the bundle OKF-conformant).
---

# knowledge/

## Purpose

OKF v0.2 (Open Knowledge Format) bundle holding verified research and design knowledge for the Neo-Cortex FalkorDB hackathon project. Spec: `references/okf-spec-v0.2.txt`.

## Ownership

- Every `.md` here except `AGENTS.md`, `index.md`, `log.md` is an OKF concept with YAML frontmatter and a non-empty `type`.
- Area directories: `hackathon/`, `falkordblite/`, `graphrag-sdk/`, `falkordb/`, `models/`, `extraction/`, `okf/`, `architecture/`.
- `references/` holds the research protocol (a concept), the verbatim OKF spec, and raw evidence under `references/evidence/<area>/`. Evidence files are never `.md` (rename mirrored markdown to `.md.txt`).

## Local Contracts

- Follow `references/research-protocol.md`: every important fact has a verbatim quote, a saved evidence file, and its sha256.
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
- Evidence audit: every `evidence[].sha256` in concept frontmatter must equal the file's sha256.

## Child DOX Index

None yet. Area directories are covered by this file.
