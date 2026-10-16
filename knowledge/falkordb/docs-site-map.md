---
type: Concept
title: FalkorDB docs site map and how it was crawled
description: How the docs.falkordb.com site was enumerated (sitemap, llms.txt, llms-full.txt), which sections were read or skipped, the page-to-concept mapping, and doc-site defects noticed during the crawl.
resource: https://docs.falkordb.com/
tags: [falkordb, docs, sitemap, llms-txt, crawl, provenance]
status: stable
generated: { by: claude-haiku-5-5/falkordb-agent, at: 2026-10-15T19:45:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:45:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: docs-sitemap
    resource: https://docs.falkordb.com/sitemap.xml
    title: FalkorDB docs sitemap (624 URLs, newest lastmod 2026-10-15T14:37:32Z)
  - id: docs-llms-txt
    resource: https://docs.falkordb.com/llms.txt
    title: FalkorDB docs page index for LLMs
  - id: docs-llms-full
    resource: https://docs.falkordb.com/llms-full.txt
    title: FalkorDB docs full text for LLMs (2,668,377 bytes)
  - id: docs-home
    resource: https://docs.falkordb.com/
    title: FalkorDB Documentation | Graph Database for GraphRAG & GenAI
evidence:
  - { file: references/evidence/falkordb/sitemap.xml, sha256: 09275a9f67e8dc1f7c106e72ec8b697a254c9a20654a3eb3b2117f223e758283, retrieved_at: 2026-10-15T19:30:00Z, method: curl }
  - { file: references/evidence/falkordb/llms.txt, sha256: b6f5810330759d9ecdb3617831ff5ae92044230caeb7e20a7bd143a40babc5f5, retrieved_at: 2026-10-15T19:30:00Z, method: curl }
  - { file: references/evidence/falkordb/llms-full.txt, sha256: 88cf73920ae23e38cf1b9b5534a8663608ff89f8572300bad2dd328980d2276d, retrieved_at: 2026-10-15T19:31:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-index.txt, sha256: 6cd57bdc84c779ec0e227d6da37e5bc09c87d219d28375e320703ca78affb132, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
---

# FalkorDB docs site map and crawl method

## How the site was enumerated

Three machine-readable sources exist. All three were fetched and cross-checked:

1. `https://docs.falkordb.com/sitemap.xml`: 624 `<url>` entries, each with a `<lastmod>`. The newest `lastmod` is `2026-10-15T14:37:32.488Z` (`references/evidence/falkordb/sitemap.xml`, sha256 `09275a9f…`).
2. `https://docs.falkordb.com/llms.txt`: the LLM-oriented page index (`llms.txt`).
3. `https://docs.falkordb.com/llms-full.txt`: all pages concatenated, 2,668,377 bytes. Each page starts with `# <title>` then `Source: <url>`. Splitting on that pattern yields 624 pages, matching the sitemap count.

The per-page Markdown (`https://docs.falkordb.com/<path>.md`) is also served as raw Markdown. The MDX-rendered HTML from the obscura CLI includes navigation chrome and is noisier. For this bundle the per-page slices come from `llms-full.txt`, and the slices used as evidence are saved as `references/evidence/falkordb/docs-<section>__<page>.txt`.

Both have 624 entries, but the URL strings differ for 31 of them: `llms-full.txt` uses `…/index` forms (for example `https://docs.falkordb.com/index`) and the sitemap lists the directory form (for example `https://docs.falkordb.com/`). Graph-RAG, UDF and other sub-pages match as paths. Normalise `/index` before diffing the two lists.

## Scope read for this concept set

The `/graphrag` subtree (20 pages) was skipped on purpose; another agent owns it. The other 604 sitemap pages are counted below by first path segment. A plain `grep -c graphrag` on the sitemap gives 22, because two `genai-tools` pages (`/genai-tools/graphrag-sdk`, `/genai-tools/graphrag-toolkit`) contain the word in their names; they are not in the skipped subtree.

| Section (first path segment) | Pages | Read for this concept set |
| --- | --- | --- |
| `cloud` | 227 | no (hosted product) |
| `enterprise` | 181 | no (API reference for an enterprise control plane) |
| `udfs` | 50 | no (Flex UDF library; one open question, see below) |
| `cypher` | 29 | yes (full: language, indexing, procedures, limitations) |
| `browser` | 24 | no (browser UI) |
| `operations` | 22 | partly (durability, FalkorDBLite, bulk-loader in integration) |
| `commands` | 16 | yes (GRAPH.* command pages) |
| `genai-tools` | 14 | no (framework integrations; out of scope) |
| `algorithms` | 12 | yes (all algorithm pages) |
| `integration` | 10 | partly (bulk-loader, index) |
| `design` | 6 | yes (architecture, concurrency, result structure, bulk spec, client spec) |
| `agentic-memory` | 5 | no |
| `getting-started` | 3 | yes (index, clients, configuration) |
| `references` | 2 | yes (license) |
| `support` | 1 | yes (contact list) |
| `datatypes` | 1 | yes |
| (root) `/` | 1 | yes |

Totals: 624 = 227 + 181 + 50 + 29 + 24 + 22 + 16 + 14 + 12 + 10 + 6 + 5 + 3 + 2 + 1 + 1 + 1 + 20 (graphrag).

## Pages behind each concept

| Concept | Main pages (sitemap `lastmod`) |
| --- | --- |
| [overview](/falkordb/overview.md) | `/` (root), `/design/index` (2026-09-15), `/references/license` (2026-10-12), `/getting-started/index` |
| [cypher-support](/falkordb/cypher-support.md) | `/cypher/cypher-support` (2026-09-15), `/cypher/known-limitations` (2026-09-15), `/cypher/functions` (2026-09-15), `/cypher/procedures` (2026-09-15), `/cypher/merge` (2026-10-12), `/cypher/unwind` (2026-09-15), `/cypher/cheat-sheet` |
| [indexing-and-vectors](/falkordb/indexing-and-vectors.md) | `/cypher/indexing` (2026-09-30), `/cypher/indexing/vector-index` (2026-09-30), `/cypher/indexing/fulltext-index` (2026-09-15), `/cypher/indexing/range-index` (2026-09-15), `/cypher/indexing/cch-index` (2026-09-30) |
| [algorithms-and-weighted-paths](/falkordb/algorithms-and-weighted-paths.md) | `/algorithms/sppath` (2026-09-15), `/algorithms/sspath` (2026-09-15, sitemap 04:06), `/algorithms/astar` (2026-09-30), `/algorithms/pagerank`, `/algorithms/wcc`, `/algorithms/cdlp` (2026-09-15), `/algorithms/msf`, `/algorithms/bfs` |
| [data-model-and-constraints](/falkordb/data-model-and-constraints.md) | `/datatypes` (2026-09-15), `/commands/graph.constraint-create` (2026-09-15), `/commands/graph.constraint-drop` |
| [limits-and-performance](/falkordb/limits-and-performance.md) | `/getting-started/configuration` (2026-10-15T10:03:32Z, newest of the set), `/design/index`, `/design/bulk-spec` (2026-09-15), `/design/concurrency` (2026-09-15), `/commands/graph.slowlog`, `/commands/graph.memory` |
| [python-client](/falkordb/python-client.md) | `/getting-started/clients`, `/commands/graph.query`, `/commands/graph.profile`, `/commands/graph.explain` (all 2026-09-15) |

Sitemap `lastmod` values are the only dates the site publishes per page. The concept frontmatter records them in `last_modified`.

## Doc-site defects seen during the crawl

- Broken anchors: the Cypher support page links to `/commands/graph.query#procedures` and `/commands/graph.query#functions` (`docs-cypher__cypher-support.txt`). The GRAPH.QUERY page has no such sections (`docs-commands__graph.query.txt`). The Procedures and Functions pages are the right targets.
- The docs' procedure table omits `algo.HarmonicCentrality`, `algo.maxFlow`, and `db.idx.cch.query`, which exist and run.
- Several doc snippets are pseudo-code with `<angle>` placeholders or named-argument signatures. They are not runnable (for example `CREATE VECTOR INDEX FOR <entity_pattern> ...`). Use the working examples in these concepts.
- Some doc examples fail as written on 4.22.1: the BFS friend-recommendation block, the betweenness block with quoted map keys, the PageRank expected values, and the CDLP expected grouping. Details are in [algorithms](/falkordb/algorithms-and-weighted-paths.md).
- The page for `Time` in datatypes contradicts itself (body: time of day; FAQ: with timezone). See [data model](/falkordb/data-model-and-constraints.md).
- The docs' Python vector example has an f-string with unescaped braces (see [python-client](/falkordb/python-client.md)).
- The explain page's example output shows `Index Scan`; the 4.22.1 server prints `Node By Index Scan`.

## Open questions

- The `udfs` section (50 pages, the "Flex UDF library") was not read. The Cypher support page both lists UDFs as unsupported and says they are supported. Read `/udfs` before deciding.
- `enterprise` and `cloud` pages were not read. They may contain licence and limit details that differ from the open-source docs.
- `llms-full.txt` is 2.67 MB. Re-fetch it to refresh; the sitemap `lastmod` will tell you which pages changed.
