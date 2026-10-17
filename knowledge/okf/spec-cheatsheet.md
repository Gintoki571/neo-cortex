---
type: Reference
title: OKF v0.2 writer cheat sheet
description: Writer-facing summary of OKF v0.2 frontmatter, provenance, trust, lifecycle, links, index/log files and conformance, with spec section references.
resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
tags: [okf, spec, cheatsheet, frontmatter]
status: stable
generated: { by: claude-haiku-5-5/okf-agent, at: 2026-10-15T19:27:17Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: OKF Version 0.2 spec (local copy, sha256 26aa5da0...1030101)
  - id: okf-issues
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/issues
    title: OKF issues and PRs (open questions)
  - id: okf-refagent
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/src/reference_agent/bundle/document.py
    title: Reference agent document.py (upstream helpers)
evidence:
  - { name: okf-spec-v0.2.txt, url: "https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md", sha256: 26aa5da029278939f914e578107242d9607d4f2dc5fe153272b82f9ed1030101, retrieved_at: 2026-10-15T19:27:17Z, method: command, redistributed: false }
  - { name: okfrepo-refagent-bundle_document.py, url: "https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/src/reference_agent/bundle/document.py", sha256: 7d9be6961b38f0fd2196e1cbe630afb1a4682e33ccd43daf3f233401ca62a43b, retrieved_at: 2026-10-15T19:25:09Z, method: curl, redistributed: false }
  - { name: okfrepo-issue-8.json, url: "https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues/8", sha256: 631be075e7d0ba7363ecfccf41c937c3ce5f7ddc10caff96ff51d49fd089d0de, retrieved_at: 2026-10-15T19:24:42Z, method: curl, redistributed: false }
  - { name: okfrepo-issue-24.json, url: "https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues/24", sha256: d4a7b006c9caff4a962be2b78c24fc1bf99ebf39cf0e86da79bc7e426ad43c60, retrieved_at: 2026-10-15T19:24:43Z, method: curl, redistributed: false }
  - { name: okfrepo-issue-29.json, url: "https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues/29", sha256: 1b9cb53c379f7ebf7ebda6e5a9be6dc7f308db77806a1da89042e6a7585072a7, retrieved_at: 2026-10-15T19:24:43Z, method: curl, redistributed: false }
  - { name: okfrepo-issue-34.json, url: "https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues/34", sha256: f712074ec4db8b3f7552fe1a71ef276b9d289ba544e2c42ee114b170670585d5, retrieved_at: 2026-10-15T19:24:44Z, method: curl, redistributed: false }
  - { name: okf-pulls.json, url: "https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/pulls", sha256: 27f1f07e87abaae75b9525da9a8c3584475cc8b57c790e21773af8563c44db0c, retrieved_at: 2026-10-15T19:24:30Z, method: curl, redistributed: false }
  - { file: references/evidence/okf/validate_okf.py, sha256: 1cb592462e0515dd1381cf038f21beadc14f6df3457467a2fed7f6f58f98327b, retrieved_at: 2026-10-15T19:25:46Z, method: command }
---

Every rule below cites the spec as `§n`. Line numbers are in `https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md`. The spec is authoritative. This sheet only summarises it, and the open questions at the end are not settled.[^okf-spec]

# 1. Bundle layout (§3, L109-149)

- A bundle is a directory tree of `.md` files. Subdirectories are free-form (§3, L111-113).
- Reserved filenames `index.md` and `log.md` mean the same thing at any depth. They MUST NOT be used for concept documents (§3.1, L136-137).
- Every other `.md` file is a concept (§3.1, L144).
- Tags are not a separate file. Use the `tags` frontmatter key (§3.1, L146-149).

# 2. Concept frontmatter (§4.1, L161-207)

A concept is a UTF-8 markdown file whose frontmatter starts with `---` on the first line and closes with `---` on its own line (§4, L155-158).

| Key | Level | Rule |
|---|---|---|
| `type` | REQUIRED | Non-empty string. Only always-required key. A concept with only `type` is conformant (§4.1 L175-188, §11). |
| `title` | recommended | Display name. Consumers may derive one from the filename (L192-193). |
| `description` | recommended | One sentence. Used by index generators and search snippets (L194-195). |
| `resource` | recommended | Canonical URI for the underlying asset. Absent for abstract ideas (L196-198). |
| `tags` | recommended | YAML **list** of short strings (L199). |
| extra keys | allowed | Producers MAY add any keys. Consumers SHOULD preserve unknown keys and MUST NOT reject them (L205-207). |

> "`type`: A short string identifying the kind of concept." Type values are "**not** registered centrally." (spec L177-184)

Example types in the spec: `BigQuery Table`, `BigQuery Dataset`, `API Endpoint`, `Metric`, `Playbook`, `Reference`, `Attested Computation` (L177-180).

# 3. Body (§4.2, L209-225)

- Free-form markdown. Prefer structure (headings, lists, tables, fenced code) over prose (L211-213).
- No required sections. Conventional headings SHOULD be used when they apply: `# Schema`, `# Examples`, `# Computation` (L215-222).
- Claim-level attribution uses footnotes keyed to `sources[].id`, not a body citations list (L224-225).

# 4. Provenance: `sources` (§5.1, L287-364)

```yaml
sources:
  - id: ga4-schema              # SHOULD be present when the body cites it (L309-310)
    resource: https://...       # REQUIRED within an entry (L305)
    title: GA4 BigQuery Export schema   # optional (L311)
    author: team:ga4-docs       # optional credibility signal, actor form (L322-323)
    usage_count: 5000           # optional, coarse liveness signal (L324-341)
    last_modified: 2026-05-30T00:00:00Z # optional, ISO datetime (L329)
usage_window: { from: ..., to: ... } # sibling of sources; frames usage_count (L332-334)
```

- `resource` names one of: an absolute URL, a bundle-relative path, a path into `references/`, or a scope descriptor such as `all queries in BigQuery project X` (L305-308).
- Credibility is recorded as signals, not as a score. Do not store a credibility score (L315-318).
- Lineage uses links, not a `derived_from` key. Deeper lineage is out of scope for v0.2 (L343-348).
- Attribution: a footnote whose label is exactly a `sources[].id` (L350-359). Labels are keyed, not positional, so a reorder does not misattribute (L361-364).

> "The footnote label is the join key into `sources`; consumers resolve attribution through the matching entry, not by parsing the footnote prose." (spec L359-360)

# 5. Trust: `generated` and `verified` (§5.2, L366-399)

```yaml
generated: { by: reference_agent/gemini-2.5-pro, at: 2026-06-20T22:53:05Z }   # by REQUIRED within generated
verified:                                  # list of independent checks
  - { by: human:ahormati, at: 2026-06-25T09:00:00Z }
  - { by: process:finance-nightly, at: 2026-06-26T02:00:00Z }
```

- `generated` = who wrote the current content, and when its last meaningful change was (L372-380).
- `verified` = who confirmed the content against its sources or `resource`. It is independent of `generated.at` (L388-393).
- A single verifier MAY be a bare mapping. Consumers MUST treat a bare mapping as a one-element list (L395-399). Example: `verified: { by: human:ahormati, at: 2026-06-25T09:00:00Z }` (L398).

Trust tiers (consumer-derived, §5.3, L403-410):

- no `verified` ⇒ **unverified**
- `verified` only by non-`human:` actors ⇒ **machine-confirmed**
- any `verified` by `human:<id>` ⇒ **human-reviewed**

Trust tiers are advisory. Not access control (L409-410).

# 6. Lifecycle (§5.4-5.5, L412-433)

- `status: draft | stable | deprecated`. Absent ⇒ `stable` (L414-422).
- `stale_after: <ISO datetime with offset>`. A concept is stale when `now >= stale_after` (L424-433).

> "An absolute instant, not a relative TTL, keeps the staleness decision a plain comparison" (spec L430-433)

# 7. Timestamps (§5 intro, L284-285)

> "Every timestamp-valued key in OKF is an ISO 8601 datetime with an explicit UTC offset, for example `2026-06-30T14:00:00Z`." (spec L284-285)

Keys that are timestamps: `generated.at`, `verified[].at`, `stale_after`, `sources[].last_modified`, `usage_window.from/to`. A date-only value such as `2026-09-23` is non-conformant under this rule. The §11 list does not repeat this rule, which is one reason issue #24 is open (see §12 below).

Our checker enforces this as C4 (`references/evidence/okf/validate_okf.py`).[^okf-issues]

# 8. Links (§6.1-6.3, L439-485)

- Absolute, bundle-relative: begins with `/`, e.g. `[customers](/tables/customers.md)`. Recommended (L444-450).
- Relative: standard markdown relative path, e.g. `[neighbour](./other.md)` (L452-456).
- A link asserts a relationship. Its kind is conveyed by prose, not by the link (L458-462). Issue #34 disputes whether links carry parent/child semantics at all.[^okf-issues]
- **Broken links MUST be tolerated.** Consumers MUST NOT treat them as malformed (L464-466).
- Path-valued fields: `resource`, `sources[].resource`, `computation`, `executor.resource`, `attester.resource` accept an absolute URL, `/`-rooted bundle path, or relative path (L468-477).
- `references/` is a naming convention, not a requirement (L479-485).

Open conflict (issue #29): §6.2 says a non-slash path is "a relative path", but §6.3 and the §10 examples write root-relative paths without a leading slash. A literal reading of §6.2 would not match the spec's own examples.[^okf-issues]

# 9. Actors (§7, L489-501)

- Agents and tools: `<producer>/<version>`, e.g. `reference_agent/gemini-2.5-pro`.
- People: `human:<id>`, e.g. `human:ahormati`.
- Automated processes: `process:<id>`, e.g. `process:finance-nightly`.
- Producers MUST use `human:` for hand-authored or human-confirmed content, because trust tiers key off that prefix (L500-501).

# 10. Index files (§8, L505-529)

- An `index.md` MAY appear in any directory. It enumerates the directory for progressive disclosure (L507-510).
- **No frontmatter**, except a bundle-root `index.md` MAY carry `okf_version` (L512-513, L776-778).
- Body: one or more `#` section headings. Entries are bullets: `* [Title](relative-url) - short description` (L516-525).
- Entries SHOULD include the linked concept's `description` (L527-528).
- Producers MAY generate `index.md`. Consumers MAY synthesise one when it is absent (L528-529).

# 11. Log files (§9, L533-552)

- `log.md` MAY appear at any level. It is a flat list of date-grouped entries, newest first (L535-536).
- Date headings MUST be ISO `YYYY-MM-DD` (L550).
- Entries are prose. The bold leading word (`**Update**`, `**Creation**`) is a convention, not a requirement (L550-552).

# 12. Attested Computation (§10, L556-732)

Use `type: Attested Computation` for a computation that must be run, not improvised.

- **`runtime`: REQUIRED** for this type. Example values: `bigquery`, `postgres`, `dbt`, `python`, `Looker` (L590-593).
- `parameters`: list of `{ name, type, required }` (L594-595).
- `computation`: optional path to a file. If absent, the body `# Computation` fence is the computation (L596-598, L645-653).
- `executor`: `resource` (run instructions) and `receipt` (fields the run must return) (L599-603).
- `attester`: `resource` naming deterministic, no-LLM code that checks a receipt (L604-605).
- The agent MAY only supply *values* for declared parameters. It MUST NOT author or edit the computation (L662-664).
- `verified` (definition still matches policy) and attestation (one run produced the value the sanctioned way) are separate (§10.6, L721-732).

# 13. Conformance (§11, L736-762)

A bundle is conformant with v0.2 if:

1. Every non-reserved `.md` has a parseable YAML frontmatter block (L740-741).
2. Every frontmatter block has a non-empty `type` (L742).
3. Each `index.md` / `log.md` follows §8 / §9 (L743-744).

When trust, lifecycle, provenance, or computation families are present, producers SHOULD follow §5-§10 (L746-747). Consumers MUST NOT reject a concept for missing optional families, unknown `type`, unknown keys, broken cross-links, or missing `index.md` (L749-762).

# 14. Versioning (§12, L766-780)

- Versions are `<major>.<minor>`. Minor = backward-compatible additions. Major = breaking changes such as renaming required fields or changing reserved filenames (L768-774).
- A bundle MAY declare `okf_version: "0.2"` in its bundle-root `index.md` frontmatter (L776-778).
- Consumers that do not understand the declared version SHOULD try best-effort consumption (L778-780).

# 15. Changes from v0.1 (§13, L796-830)

- `timestamp` is superseded by `generated.at`. Consumers MAY fall back to `timestamp` (L805-807).
- The body `# Citations` list is superseded by `sources`. Consumers MAY still parse it for v0.1 files (L809-811).

# 16. Writer checklist

1. Start with frontmatter: `type` (required), `title`, `description`, `resource`, `tags` as a list.
2. Add `generated: { by, at }`. Use `human:` for any human-written or human-confirmed content.
3. Add `sources` entries with `id` and `resource`. Attribute claims with footnotes labelled by `sources[].id`.
4. Write every timestamp as `YYYY-MM-DDTHH:MM:SSZ` (or with `+hh:mm`). Date-only is non-conformant.
5. Link with `/`-rooted bundle paths. Broken links are tolerated.
6. Use `status` and `stale_after` for anything that will change.
7. Index and log files: no frontmatter in sub-indexes. Log date headings are `YYYY-MM-DD`.

# Open questions (unsettled upstream, 2026-10-15)

- **`okf_version` and timestamps (issue #24, open).** PR #6 made timestamps need an explicit offset and turned date-only `stale_after` non-conformant, without a version bump. Two bundles that both say `okf_version: "0.2"` can disagree about the same `stale_after` value.[^okf-issues]
- **Path resolution (issue #29, open).** See §6 above.
- **Links and parent/child (issue #34, open).** Does a plain markdown link carry any semantics?[^okf-issues]
- **JSON Schema (issue #8, open).** No upstream schema or validator exists yet.[^okf-issues]
- **Reference agent parser (PR #38, open).** "Fix parser accepting falsy non-mapping frontmatter." Upstream `document.py` does `yaml.load(...) or {}` before its mapping check, so falsy non-mapping YAML (for example `[]` or `0`) becomes `{}` and passes silently (code reading, not run).[^okf-refagent]

# Local tooling

- `references/evidence/okf/validate_okf.py` checks C1-C5 (conformance) and C6 (broken links). Run output: `references/evidence/okf/validate_okf-run.txt`. See [tooling-and-examples](/okf/tooling-and-examples.md).

[^okf-spec]: `https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md`. Sections and line numbers as cited above.
[^okf-issues]: OKF issues and pull requests - evidence in `https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues?state=open`, `https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/pulls`, `https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues/8`, `https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues/24`, `https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues/29`, `https://api.github.com/repos/GoogleCloudPlatform/open-knowledge-format/issues/34`.
[^okf-refagent]: `https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/src/reference_agent/bundle/document.py`, `REQUIRED_FRONTMATTER_KEYS = ("type",)`, `is_stale()` (ignores stale_after without an explicit offset).
