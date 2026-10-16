---
type: Design Proposal
title: Mapping an OKF bundle to a property graph (FalkorDB ingest)
description: Proposed mapping of OKF concepts, links, tags, sources, trust and attested computations onto nodes, edges and provenance properties for ingestion into FalkorDB. Design proposal, not verified behaviour.
resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
tags: [okf, graph, falkordb, design, proposal]
status: draft
generated: { by: claude-haiku-5-5/okf-agent, at: 2026-10-15T19:27:17Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: okf-spec
    resource: references/okf-spec-v0.2.txt
    title: OKF Version 0.2 spec (local copy, sha256 26aa5da0...1030101)
  - id: okf-issues
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/issues
    title: OKF issues (#11 deletion, #16 typed relationships, #29 path resolution, #34 links)
  - id: okf-refagent
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/src/reference_agent/bundle/document.py
    title: Reference agent document.py (trust_tier, is_stale helpers)
evidence:
  - { file: references/okf-spec-v0.2.txt, sha256: 26aa5da029278939f914e578107242d9607d4f2dc5fe153272b82f9ed1030101, retrieved_at: 2026-10-15T19:27:17Z, method: command }
  - { file: references/evidence/okf/okfrepo-refagent-bundle_document.py, sha256: 7d9be6961b38f0fd2196e1cbe630afb1a4682e33ccd43daf3f233401ca62a43b, retrieved_at: 2026-10-15T19:25:09Z, method: curl }
  - { file: references/evidence/okf/okf-issues-open.json, sha256: 15fb1334578e3e2dc863e8226dd4425118799d64dd83c510b3c1e24beda39e22, retrieved_at: 2026-10-15T19:24:29Z, method: curl }
  - { file: references/evidence/okf/okfrepo-issue-29.json, sha256: 1b9cb53c379f7ebf7ebda6e5a9be6dc7f308db77806a1da89042e6a7585072a7, retrieved_at: 2026-10-15T19:24:43Z, method: curl }
  - { file: references/evidence/okf/validate_okf-upstream-bundles.txt, sha256: 8083575bb3f5696477b4b13e1c1ac0dbb5ff577d71ddff0e686e8c45b702255a, retrieved_at: 2026-10-15T19:27:17Z, method: command }
---

> **Status: design proposal (`status: draft`). Not verified.** Nothing here has been run against FalkorDB. The mapping follows the OKF spec and the reference agent's helpers, and the labels, keys and Cypher are proposals to test, not facts.

# Goal

Load an OKF bundle into one FalkorDB graph so that:

- a consumer can traverse concept links, source attribution and attested-computation dependencies with Cypher;
- every node and edge carries enough provenance to trace it back to a file and a content hash;
- trust (`verified`), freshness (`stale_after`) and lifecycle (`status`) are queryable.

Spec basis: concepts are markdown files (§4), links are untyped relationships (§6.1, L458-462), `sources` carries provenance (§5.1), `generated` and `verified` carry trust (§5.2), and `runtime`/`parameters`/`executor`/`attester` carry computations (§10.2). Spec references are to `references/okf-spec-v0.2.txt`.[^okf-spec]

# 1. Node types

| Label | Key (MERGE on) | Source in bundle | Notes |
|---|---|---|---|
| `Bundle` | `bundle` (name) | root directory | Holds `okf_version` from root `index.md` (§12, L776-778) when present. |
| `Dir` | `bundle`, `path` | every directory | Gives the hierarchy. Subdirectories are free-form (§3, L111-113). |
| `Concept` | `bundle`, `id` | each non-reserved `.md` | `id` = path without `.md` (§2, L79-80). `type` is a property, not a label (see §4 below). |
| `Source` | `bundle`, `concept_id`, `source_id` | each `sources[]` entry | Per-entry, because credibility signals live on the entry (§5.1). Use `source_id` as given; `resource` may be a scope descriptor (L305-308). |
| `Actor` | `name` | `generated.by`, `verified[].by` | `kind` = `agent` / `human` / `process`, from the prefix (§7, L491-499). |
| `Tag` | `name` | `tags` | Normalise to a list. The upstream stackoverflow bundle has string tags (see [tooling-and-examples](/okf/tooling-and-examples.md)). |
| `Param` | `bundle`, `computation_id`, `name` | `parameters[]` of an Attested Computation | `{name, type, required}` (§10.2, L594-595). |
| `Resource` | `uri` | `computation`, `executor.resource`, `attester.resource`, and any path-valued field | Stores the raw path plus the resolved target (see §6). |
| `LogEntry` | `bundle`, `path`, `date`, `ordinal` | `log.md` headings and bullets | §9. Log entries are prose, so keep text, not structure. |

Do not create nodes for `index.md`. Its content is derivable from `Dir` and `Concept` (§8, L527-529). Keep `index.md` as a property on `Dir` (`index_sha256`), if you need it.

# 2. Edge types

| Edge | From → To | Properties | Source |
|---|---|---|---|
| `IN_DIR` | `Concept` → `Dir` | | §3 |
| `SUBDIR_OF` | `Dir` → `Dir` | | §3 |
| `LINKS_TO` | `Concept` → `Concept` or `Resource` | `raw`, `form` (`absolute` / `relative`), `resolved` (bool) | §6.1. Untyped on purpose (L458-462). |
| `DERIVES_FROM` | `Concept` → `Source` | `source_id` | §5.1 provenance. |
| `CITES` | `Concept` → `Source` | `label`, `count` | Footnote `[^label]` whose label equals `sources[].id` (L350-359). Resolve by label, never by prose (L359-360). |
| `GENERATED_BY` | `Concept` → `Actor` | `at` | §5.2, L377-380. |
| `VERIFIED_BY` | `Concept` → `Actor` | `at` | One edge per event. Bare mapping is one event (L395-399). |
| `HAS_PARAM` | `Concept` → `Param` | | §10.2. |
| `EXECUTOR` / `ATTESTER` / `COMPUTATION` | `Concept` → `Resource` | `receipt` (for executor) | §10.2 contract fields. |
| `TAGGED` | `Concept` → `Tag` | | §4.1, L199. |
| `HAS_ENTRY` | `Concept` or `Dir` → `LogEntry` | | §9 |

**Derived edges (not in the spec).** A consumer may add `USES_COMPUTATION` (`Concept` → `Concept` with `runtime`) by following a link to an Attested Computation (§10.4, L672-695). Mark it `derived: true` and `rule: okf-ingest-v1`. Do not write it as a link. The spec says the link's kind is "conveyed by the surrounding prose" (L458-462), so a derived edge is an interpretation.

# 3. Provenance on every node and edge

Store these on every node and edge the ingest creates. They make an OKF-derived fact traceable back to its source file.

| Property | Meaning |
|---|---|
| `okf_bundle` | Bundle name (same as `Bundle.bundle`). |
| `okf_path` | Path of the source file, relative to the bundle root. |
| `okf_sha256` | SHA-256 of the file's bytes at ingest. A re-read with a different hash means the node is stale. |
| `okf_spec` | `"0.2"`, or the value of `okf_version` if the bundle declares one. |
| `okf_run` | Ingest run id (UUID). Used for mark-and-sweep (see §5). |
| `okf_ingested_at` | UTC ISO 8601 with offset (the spec's own rule, §5 intro L284-285). |
| `okf_derived` | `true` for edges and properties the ingest interprets (e.g. `USES_COMPUTATION`, `trust_tier`, `stale_now`). |

Spec-declared fields keep their own meaning. `generated.at` stays the producer's time (§5.2). `okf_ingested_at` is the ingest time. Do not overwrite one with the other.

# 4. Concept properties

From frontmatter, copied as given unless noted:

- `type`, `title`, `description`, `resource`, `status`, `stale_after`, `tags` (list), `generated_by`, `generated_at`.
- Keep unknown keys in `extra` (JSON string) rather than promoting each one. The spec says consumers MUST NOT reject unknown keys (§4.1 L205-207). Promoting them makes the schema drift with every producer.
- **Derived (`okf_derived: true`):**
  - `trust_tier`: `unverified` / `machine-confirmed` / `human-reviewed` (§5.3, L403-410). Same rule as the reference agent's `trust_tier()` (`okfrepo-refagent-bundle_document.py`).[^okf-refagent]
  - `stale_after_ms` (epoch ms, parsed from `stale_after`) and `stale_now` (computed at ingest). A stale-check at query time is cleaner: store `stale_after_ms` and compare with the query clock (§5.5, L430-433).
  - `body` (the markdown body), if you want full-text search.

`type` is a property, not a label. Spec types are free-form (§4.1 L183-184), so labels built from them would need escaping and would fragment queries.

# 5. Ingest procedure (proposal)

1. **Parse.** Use the same rules as `validate_okf.py` (`references/evidence/okf/validate_okf.py`). Split the frontmatter on `---`. Load YAML with the timestamp resolver off, so timestamps stay strings. Otherwise `2026-06-30T14:00:00Z` is rewritten on round-trip (see the `_Loader` docstring in `okfrepo-refagent-bundle_document.py`).
2. **Normalise.** A bare `verified` mapping becomes a one-element list (§5.2, L395-399). A string `tags` value becomes a list, and emit a warning. Keep the raw form in `extra`.
3. **Emit rows.** Batch with `UNWIND $rows AS r MERGE ... SET ...`. One Cypher statement per node or edge type. Pass the rows as parameters, never by string interpolation (labels are fixed, values are parameters).
4. **Resolve links.** For `LINKS_TO`, resolve absolute (`/...`) paths against the bundle root and relative paths against the file's directory (§6.1, §6.2). Record `resolved: false` for broken links. Per §6.1 and §11, a broken link is not an error (L464-466, L749-762).
5. **Mark-and-sweep.** Stamp every node and edge with `okf_run`. After the run, delete nodes and edges from that bundle whose `okf_run` is not the current one. This implements deletion, which OKF does not define (see open questions).

## Sketch (illustrative, not run)

```cypher
// Parameters: $rows = [{id, path, sha256, type, title, description, resource,
//                       status, stale_after, generated_by, generated_at, run}]
UNWIND $rows AS r
MERGE (c:Concept {bundle: $bundle, id: r.id})
SET c += {type: r.type, title: r.title, description: r.description,
          resource: r.resource, status: coalesce(r.status, 'stable'),
          stale_after: r.stale_after, okf_path: r.path, okf_sha256: r.sha256,
          okf_run: r.run, okf_spec: $spec, okf_derived: false}
```

Then `LINKS_TO`, `CITES`, and the rest follow the same pattern. Confirm the exact Cypher subset, `MERGE`/`UNWIND` behaviour, parameter binding and datetime handling against FalkorDB's own docs before implementing. None of that was checked here.

# 6. Path resolution (open conflict)

`resource`, `sources[].resource`, `computation`, `executor.resource`, and `attester.resource` are path-valued (§6.2, L468-477). Issue #29 reports that §6.2 says a non-slash path is "relative", while §6.3 and the §10 examples write root-relative paths without a leading slash.[^okf-issues] Until the spec settles it:

- store the **raw** string on the edge or `Resource` node (`raw`);
- store two resolutions, `resolved_file` (relative to the concept) and `resolved_root` (relative to the bundle), with a flag saying which rule produced the edge;
- do not drop a `Resource` node because its resolution is ambiguous.

# 7. Deletion and identity

- Identity is `(bundle, id)`. A rename is a new concept plus a deleted old one. OKF does not define deletion or rename (issue #11, open).[^okf-issues]
- Use mark-and-sweep (§5 step 5). A concept absent from the new run is deleted, with its edges. A consumer that needs history keeps `deprecated` concepts (§5.4, L418-420), since they remain in the bundle.

# 8. Open questions

- Should Attested Computation receipts be stored? §10 says receipts are "not stored in the bundle" (L701-702, L727-728). Do not put them in the graph unless the consumer is the executor.
- Multiple bundles in one graph: does a cross-bundle link resolve? The spec does not define it (§6.1 is per bundle). Current proposal: `LINKS_TO` stays within a bundle.
- Typed relationships: issue #16 proposes typed `relationships` in frontmatter. If accepted, `LINKS_TO` gains a `kind` property and the derived edges change.[^okf-issues]
- Trust: issue #13 proposes a third trust field, `refuted`.[^okf-issues] If accepted, `trust_tier` changes.
- The FalkorDB side (Cypher subset, index support, datetime handling, bulk-load path) is unverified. Check against `/falkordb/` and `/falkordblite/` concepts once they are written, and test on a copy of the upstream `bundles/acme_retail` (17 `.md` files, includes Attested Computations).

[^okf-spec]: `references/okf-spec-v0.2.txt`. Line numbers as cited.
[^okf-issues]: OKF issues - evidence in `references/evidence/okf/okf-issues-open.json`, `okfrepo-issue-29.json`.
[^okf-refagent]: `references/evidence/okf/okfrepo-refagent-bundle_document.py` (`trust_tier`, `is_stale`, `_Loader`).
