---
type: Concept
title: FalkorDB overview
description: What FalkorDB is, how it is built (Redis module, GraphBLAS sparse matrices), its license, and which versions were observed on 2026-10-15.
resource: https://github.com/FalkorDB/FalkorDB
tags: [falkordb, graph-database, overview, license, graphrag]
status: stable
generated: { by: claude-haiku-5-5/falkordb-agent, at: 2026-10-15T19:45:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:45:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: docs-design-index
    resource: https://docs.falkordb.com/design/index
    title: FalkorDB Architecture and Design Principles
  - id: docs-getting-started
    resource: https://docs.falkordb.com/getting-started/index
    title: Getting Started with FalkorDB
  - id: docs-license
    resource: https://docs.falkordb.com/references/license
    title: FalkorDB License (SSPLv1)
    last_modified: 2026-10-12T03:59:47.065Z
  - id: github-readme-main
    resource: https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/README.md
    title: FalkorDB README (main branch)
  - id: github-readme-master
    resource: https://raw.githubusercontent.com/FalkorDB/FalkorDB/master/README.md
    title: FalkorDB README (master branch, stale copy)
  - id: github-license-main
    resource: https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/LICENSE
    title: LICENSE file on main branch (SSPLv1 text plus Elastic License 2.0 text)
  - id: github-license-master
    resource: https://raw.githubusercontent.com/FalkorDB/FalkorDB/master/LICENSE.txt
    title: LICENSE.txt on master branch (SSPLv1 text only)
  - id: github-repo-api
    resource: https://api.github.com/repos/FalkorDB/FalkorDB
    title: GitHub API repository metadata
    last_modified: 2026-10-15T14:25:40Z
  - id: github-release-latest
    resource: https://api.github.com/repos/FalkorDB/FalkorDB/releases/latest
    title: GitHub latest release v6.0.2
    last_modified: 2026-10-08T14:49:34Z
  - id: docker-hub-tags
    resource: https://hub.docker.com/v2/repositories/falkordb/falkordb/tags
    title: Docker Hub tags for falkordb/falkordb
    last_modified: 2026-10-15T14:11:23Z
  - id: pypi-falkordb
    resource: https://pypi.org/pypi/falkordb/json
    title: PyPI metadata for FalkorDB client 1.8.0
    last_modified: 2026-10-14T11:54:31Z
evidence:
  - { name: docs-design__index.txt, url: "https://docs.falkordb.com/design/index", sha256: 2dd463c8cab32eb0ebee9e445ebc4da8f9b279d704cdb254e8f1dc4680b7900b, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-getting-started__index.txt, url: "https://docs.falkordb.com/getting-started/index", sha256: f68376e21b1c42ad040d8c41d606a88acd8eac7a4ac74ca1737ffd7f5cb41bb5, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-references__license.txt, url: "https://docs.falkordb.com/references/license", sha256: 9dd9675b2aeb7eabfddae89e51e24bdf5261b6b800fdf388be45b9c928915d04, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: github-README-main.md.txt, url: "https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/README.md", url_basis: inferred, sha256: 992fe2e53f68b0ad76b09cf3b3ae353838e9002292d6d8c869388cd2328ff3d9, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { name: github-README.md.txt, url: "https://raw.githubusercontent.com/FalkorDB/FalkorDB/master/README.md", url_basis: inferred, sha256: 51abc6e076aa2af65efca891f5d0ce5f3524551b99759b3320423a69f802d499, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { name: github-LICENSE-main.txt, url: "https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/LICENSE.txt", url_basis: inferred, sha256: 0e8f0497016466a84975d296ae768e4adb16a7267b4a6ed373157be96d127dfc, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { name: github-LICENSE.txt, url: "https://raw.githubusercontent.com/FalkorDB/FalkorDB/master/LICENSE.txt", url_basis: inferred, sha256: 34e94c5087ba6e9fb34f35ae71df5e6533c5fc7cbbf6c44186a71e82806b69e1, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { name: github-repo.json, url: "https://api.github.com/repos/FalkorDB/FalkorDB", sha256: f91b66969ebd41e390333b9af9e58f0f175970d726c66663193fb4221aeab580, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { name: github-license-api.json, url: "https://api.github.com/repos/FalkorDB/FalkorDB/license", sha256: cd04fb995c6f474f09f6ec18238ea8b67f10f2c129fdbfa973f2d3ca0a63c5de, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { name: github-release-latest.json, url: "https://api.github.com/repos/FalkorDB/FalkorDB/releases/latest", sha256: 3151fd0647ef9cd272788d46a2b32859f18d406dcbcc90911a081102c3ce7b07, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { name: github-releases.json, url: "https://api.github.com/repos/FalkorDB/FalkorDB/releases", sha256: 9521f4fc2eb698539581d8d917a741686e654eb379bba0af4b40480075e3ec7c, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { name: docker-hub-tags.json, url: "https://hub.docker.com/v2/repositories/falkordb/falkordb/tags?ordering=last_updated", sha256: e2e0809291a2f5d7c38edf4bb28630f9bdd9f32ec345aa058dcb03eb26cc0c1e, retrieved_at: 2026-10-15T19:40:00Z, method: curl, redistributed: false }
  - { name: docker-manifest-latest-amd64.json, url: "https://hub.docker.com/r/falkordb/falkordb/tags", url_basis: inferred, sha256: d998ed0dfd91da6208f257dfd61f5330335bd6e7006cfc0fd1ddd761269e2634, retrieved_at: 2026-10-15T19:40:00Z, method: curl, redistributed: false }
  - { name: docker-manifest-edge-rs-amd64.json, url: "https://hub.docker.com/r/falkordb/falkordb/tags", url_basis: inferred, sha256: a610bcff0bc41dc684d02925783debe8a0151c1ddc5bdb73eafdca433a048db3, retrieved_at: 2026-10-15T19:40:00Z, method: curl, redistributed: false }
  - { name: pypi-falkordb.json, url: "https://pypi.org/pypi/falkordb/json", sha256: d0c590052d766d723cad9285c97cafbc863bf651010345ac8d83d50159daf6bc, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { file: references/evidence/falkordb/run-4.22.1-redis-cli.txt, sha256: 4dd80f636385e39db5bd031d09b6ae5e61c9195157ccbfddd58bbc5ca4978e1e, retrieved_at: 2026-10-15T19:50:00Z, method: command }
---

# FalkorDB overview

FalkorDB is a graph database that runs as a Redis module and speaks Cypher. This concept covers what it is, how it is built, its license and the versions that were observed. Other FalkorDB concepts: [Cypher support](/falkordb/cypher-support.md), [indexing and vectors](/falkordb/indexing-and-vectors.md), [algorithms](/falkordb/algorithms-and-weighted-paths.md), [data model](/falkordb/data-model-and-constraints.md), [limits](/falkordb/limits-and-performance.md), [Python client](/falkordb/python-client.md), [docs site map](/falkordb/docs-site-map.md).

## What it is

> "FalkorDB is a graph database developed from scratch on top of Redis, using the new Redis Modules API to extend Redis" — evidence: `https://docs.falkordb.com/design/index` [^docs-design-index]

> "This repository is the Rust implementation of FalkorDB. It builds the `falkordb` Redis module (`libfalkordb.{so,dylib}`) from Rust, using GraphBLAS sparse matrices for graph storage and traversal." — evidence: `github-README-main.md` [^github-readme-main]

The older master-branch README describes a C build (`make`, `src/falkordb.so`). The default branch (`main`) is the Rust implementation. Treat the master README as stale.

## Architecture (sparse matrices and GraphBLAS)

> "FalkorDB uses **sparse adjacency matrices** to represent graphs. Each relationship type gets its own dedicated matrix, plus one global adjacency matrix that marks all connections regardless of type." — evidence: `https://docs.falkordb.com/design/index` [^docs-design-index]

> "To perform all of these operations for sparse matrices, FalkorDB uses [GraphBLAS](http://graphblas.org/) - a standard API similar to BLAS. The current implementation uses the CSC sparse matrix format (compressed sparse columns), although the underlying format is subject to change." — evidence: `https://docs.falkordb.com/design/index` [^docs-design-index]

Practical reading for a GraphRAG project: traversals are matrix multiplications, so multi-hop patterns and graph algorithms are fast, but everything is held in RAM (see [limits](/falkordb/limits-and-performance.md)). The design page says "Data stored in RAM using memory-efficient custom data structures" (`https://docs.falkordb.com/design/index`).

## Redis version requirement (conflicting)

- Docs: "> **Minimum Redis version:** FalkorDB requires **Redis 8.0.0 or later**. Earlier versions (including the Redis 7.x series) are not supported." — evidence: `https://docs.falkordb.com/getting-started/index` [^docs-getting-started]
- Master README (stale): "> Note: [Redis 7.4](https://redis.io/download) is required for the latest FalkorDB version." — evidence: `github-README.md`
- Main README does not state a Redis version.

Use Redis 8.0 or later, as the current docs say.

## License

The docs and the main README both name SSPLv1. The LICENSE file is not clean.

> "Licensed under the Server Side Public License v1 (SSPLv1). See [LICENSE](LICENSE)." — evidence: `github-README-main.md`

> "* **License**: This project is licensed under the Server Side Public License v1 (SSPLv1). See the [LICENSE](LICENSE) file for details." — evidence: `github-README-main.md`

The `main` branch `LICENSE` contains the full SSPLv1 text followed, after the SSPL end marker, by a separate "Elastic License 2.0" section (`https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/LICENSE.txt`):

> "Elastic License 2.0" — evidence: `https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/LICENSE.txt` (heading at about line 563; the file ends with the Elastic text). [^github-license-main]

> "You may not provide the software to third parties as a hosted or managed service, where the service provides users with access to any substantial set of the features or functionality of the software." — evidence: `https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/LICENSE.txt` [^github-license-main]

The master-branch `https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/LICENSE` contains only SSPLv1 text (`https://raw.githubusercontent.com/FalkorDB/FalkorDB/master/LICENSE.txt`, 30582 bytes against 34447 bytes on main). The GitHub API reports the license as `"name": "Other", "spdx_id": "NOASSERTION"` (`https://api.github.com/repos/FalkorDB/FalkorDB/license`).

SSPLv1 section 13 is the clause that matters for a service. From `https://raw.githubusercontent.com/FalkorDB/FalkorDB/master/LICENSE.txt` (master copy, identical SSPL text):

> "If you make the functionality of the Program or a modified version available to third parties as a service, you must make the Service Source Code available via network download to everyone at no charge, under the terms of this License." — evidence: `https://raw.githubusercontent.com/FalkorDB/FalkorDB/master/LICENSE.txt`

Implications for Neo-Cortex (a hackathon project, see the open questions):

- Using FalkorDB as an embedded or internal component of an app that you do not offer as a hosted service to third parties is what the docs describe as allowed: "> Yes! If you're using FalkorDB for internal purposes only—within your organization without providing it as a service to external users—you are not required to open-source your code." — evidence: `https://docs.falkordb.com/references/license` [^docs-license]
- Offering FalkorDB functionality to third parties over a network triggers section 13. The docs say so too: "> You can use FalkorDB commercially, but if your application provides FalkorDB as a service to users, then under SSPLv1, you must open-source the code that enables this service." — evidence: `https://docs.falkordb.com/references/license`
- This is not legal advice. The docs FAQ is not the license text.

## Versions and dates observed (2026-10-15 UTC)

| Item | Observed | Evidence |
| --- | --- | --- |
| GitHub repo `pushed_at` | `2026-10-15T14:25:40Z` | `github-repo.json` |
| GitHub stars / created | 10154 stars, created `2023-07-20T10:47:51Z` | `github-repo.json` |
| GitHub `releases/latest` | `v6.0.2`, published `2026-10-08T14:49:34Z` | `https://api.github.com/repos/FalkorDB/FalkorDB/releases/latest` |
| Newest GitHub release in list | `v4.22.1`, published `2026-10-15T06:00:43Z` | `https://api.github.com/repos/FalkorDB/FalkorDB/releases` |
| Docker Hub `latest` and `v4.22.1` | pushed `2026-10-15T06:05` | `https://hub.docker.com/v2/repositories/falkordb/falkordb/tags?ordering=last_updated` |
| Docker Hub `edge-rs` | pushed `2026-10-15T14:11` | `https://hub.docker.com/v2/repositories/falkordb/falkordb/tags?ordering=last_updated` |
| Module version of Docker `latest` (run locally) | `42201` (= 4.22.1) | `run-4.22.1-redis-cli.txt`, `run-4.22.1-verify-core.txt` |
| Module version of Docker `edge-rs` (run locally) | `999999` (dev build) | `run-edge-rs-verify-core.txt` |
| Python client `FalkorDB` | `1.8.0`, uploaded `2026-10-14T11:54:31` | `https://pypi.org/pypi/falkordb/json` |

Quotes for the release line:

> "# FalkorDB v6.0.2" — evidence: `https://api.github.com/repos/FalkorDB/FalkorDB/releases/latest` (body field)

> "Replace graphblas.sh/redisearch.sh with a `native-deps` crate; GraphBLAS and LAGraph are now submodules (#2695)" — evidence: `https://api.github.com/repos/FalkorDB/FalkorDB/releases/latest` (body field)

Key point: the highest GitHub release tag (v6.0.2) is not the image most people pull. Docker `latest` is 4.22.1. This project did not run the official v6.0.2 binary: the v6.0.2 release has no assets, and no v6 tag appeared among the 15 most recent Docker Hub tags. Behaviour recorded in this concept comes from the 4.22.1 image and the `edge-rs` dev image. See [limits](/falkordb/limits-and-performance.md) for how that affects claims.

Hashes of the image manifests and tags are in `https://hub.docker.com/r/falkordb/falkordb/tags` (digest `sha256:d998ed0d...`) and `https://hub.docker.com/v2/repositories/falkordb/falkordb/tags?ordering=last_updated`.

## Client libraries

- Python: `FalkorDB` on PyPI, MIT, version 1.8.0 (see [python-client](/falkordb/python-client.md)). The main README table lists falkordb-py as MIT.
- Other official clients per the README: falkordb-ts (Node.js), falkordb-rs (Rust), falkordb-go, jfalkordb, NFalkorDB (C#).
- Wire protocol: RESP (any Redis client can send `GRAPH.QUERY`) and Bolt. Bolt is off by default: "`BOLT_PORT` -1 (disabled)." (`https://docs.falkordb.com/getting-started/configuration`, Default section).

## Open questions

- Whether the Elastic License 2.0 text appended to the main-branch LICENSE applies to any part of the code, or is a leftover. The repo does not say (no dual-license clause). Ask the maintainers or a lawyer before shipping a hosted service.
- Behaviour of the official v6.0.2 binary. Not tested. The 4.22.1 and `edge-rs` results may differ (see [cypher-support](/falkordb/cypher-support.md), where `edge-rs` rejects a fulltext call that 4.22.1 accepts).
- The docs' performance claim about creating over 1 million nodes is a vendor claim. See [limits](/falkordb/limits-and-performance.md).

[^docs-design-index]: FalkorDB Architecture and Design Principles - https://docs.falkordb.com/design/index
[^docs-getting-started]: Getting Started with FalkorDB - https://docs.falkordb.com/getting-started/index
[^docs-license]: FalkorDB License (SSPLv1) - https://docs.falkordb.com/references/license (last_modified 2026-10-12T03:59:47.065Z)
[^github-license-main]: LICENSE file on main branch (SSPLv1 text plus Elastic License 2.0 text) - https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/LICENSE
[^github-readme-main]: FalkorDB README (main branch) - https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/README.md
