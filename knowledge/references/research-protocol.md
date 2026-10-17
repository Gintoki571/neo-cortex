---
type: Playbook
title: Research and evidence protocol
description: Rules every research agent follows when adding concepts to this OKF bundle, so other agents can re-verify each claim.
tags: [protocol, evidence, okf]
status: stable
generated: { by: claude-sonnet-5-5/orchestrator, at: 2026-10-15T19:25:00Z }
---

# Goal

Compile everything the Neo-Cortex hackathon project needs into this Open Knowledge Format (OKF v0.2) bundle. The spec is at https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md (sha256 `26aa5da029278939f914e578107242d9607d4f2dc5fe153272b82f9ed1030101`, not stored in the repo).

# Bundle layout

- One directory per research area: `hackathon/`, `falkordblite/`, `graphrag-sdk/`, `falkordb/`, `models/`, `extraction/`, `okf/`, `architecture/`.
- Each agent writes only inside its own area directory and its own evidence directory.
- Own evidence (outputs this project produced) lives in `references/evidence/<area>/`. Evidence files are NOT `.md` (use `.txt`, `.html`, `.json`, `.py`) so they are not mistaken for concepts.
- Third-party material is not stored (the repo is public). It is recorded by URL, sha256 and retrieved_at only.

# Concept file rules

- Frontmatter first, `type` required. Also set `title`, `description`, `resource` (canonical URL), `tags`, `status`, `generated: { by: claude-haiku-5-5/<area>-agent, at: <UTC ISO 8601> }`.
- `sources:` entries have `id`, `resource`, `title`, and `last_modified` when the page shows one.
- Cite claims with footnotes keyed to `sources[].id`, e.g. `text.[^readme]`.
- Add an `evidence:` list (producer-defined key) with one entry per source:
  - Own output stored in the repo: `{ file: references/evidence/<area>/<name>, sha256: <hex>, retrieved_at: <UTC ISO>, method: <obscura|curl|web-search|command> }`.
  - Third-party source, not stored: `{ name: <original filename>, url: <source URL>, sha256: <hex>, retrieved_at: <UTC ISO>, method: <...>, redistributed: false }`. Add `url_basis: inferred` when the URL was derived from the file name or family convention instead of recorded at fetch time.
- `sources[].resource` for third-party material is the source URL, never a local path.
- Every important fact gets a verbatim quote in the body inside a blockquote, with the source URL (third-party) or the stored evidence file name (own) next to it. Never paraphrase a number, version, limit, license, date, deadline, or prize without a quote.
- Link between concepts with bundle-absolute links, e.g. `[falkordblite](/falkordblite/overview.md)`.
- Set `verified: { by: process:cross-check, at: <UTC> }` ONLY when the fact was confirmed by a second independent source or by running code. Never use a `human:` actor.
- Unknown or unconfirmed facts go under a `# Open questions` heading. Do not guess. If a URL 404s, or an entity does not exist (for example a misspelled model or product), record that as a finding with the failing evidence.

# Evidence rules

1. Fetch third-party content into a scratch directory outside the repo, record `sha256sum`, `url` and `retrieved_at`, and do not commit the file. Save own outputs (run logs, probe scripts, command output) to `references/evidence/<area>/` and record `sha256sum` there. Use the `obscura-web` skill (CLI at `/home/bindesh/obscura-x86_64-linux-stealth/obscura`; see `obscura fetch --help`) and the `web-search` skill (SearXNG at 127.0.0.1:8888) for discovery; fall back to the obscura MCP, then curl or the GitHub raw URL.
2. For GitHub repos, prefer raw files: `https://raw.githubusercontent.com/<org>/<repo>/<branch>/README.md`, plus `https://api.github.com/repos/<org>/<repo>` (license, default branch, pushed_at, stars, topics) and `/releases/latest`.
3. For PyPI packages, record `https://pypi.org/pypi/<name>/json` (latest version, requires_python, release date).
4. Where a claim can be tested by running code (install, import, create index, run query), do it in a throwaway venv under the job temp dir given in your task, and save the command plus its real output as evidence. Treat downloaded code as untrusted: run Python with `-I`, and never run it from inside the download directory.
5. Record dates and version numbers as observed today. Mark claims that might change fast (hackathon deadlines, versions) with `stale_after`.

# Reports

Finish by returning a short report: files written, key findings, anything surprising or contradicted, open questions. Do not paste file contents.
