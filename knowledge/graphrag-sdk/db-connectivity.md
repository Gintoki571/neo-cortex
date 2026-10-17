---
type: Concept
title: GraphRAG SDK to FalkorDB connectivity and falkordblite compatibility
description: How graphrag-sdk 1.4.0 builds its FalkorDB client, which injection points exist, whether falkordblite (embedded FalkorDB) works with it (verified two ways), vector and fulltext index syntax, and known FalkorDB 6.x incompatibilities.
resource: https://docs.falkordb.com/graphrag/configuration
tags: [graphrag, falkordb, falkordblite, connection, vector-index, redis]
status: stable
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/graphrag-sdk-agent, at: 2026-10-15T20:10:00Z }
sources:
  - id: docs-configuration
    resource: https://docs.falkordb.com/graphrag/configuration
    title: GraphRAG SDK Configuration Reference
  - id: docs-storage
    resource: https://docs.falkordb.com/graphrag/storage
    title: How GraphRAG SDK Stores Graphs in FalkorDB
  - id: src-pypi
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: graphrag-sdk 1.4.0 source (installed copy; files in evidence)
  - id: src-main
    resource: https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0b27fdcc7f2c28508b09e86169851a8187/graphrag_sdk/src/graphrag_sdk/core/connection.py
    title: core/connection.py at main 35e67a0
  - id: falkordblite-repo
    resource: https://github.com/FalkorDB/falkordblite
    title: FalkorDBLite repository (clone at ae24b52)
  - id: falkordblite-pypi
    resource: https://pypi.org/pypi/falkordblite/json
    title: falkordblite PyPI JSON (0.10.0)
  - id: falkordb-pypi
    resource: https://pypi.org/pypi/falkordb/json
    title: falkordb (Python client) PyPI JSON
  - id: gh-issues
    resource: https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all
    title: GraphRAG-SDK issues (#294, #344)
  - id: falkordb-module-info
    resource: references/evidence/graphrag-sdk/runs/falkordb-module-info.txt
    title: "local run output (this research)"
  - id: falkordblite-conf
    resource: https://github.com/FalkorDB/falkordblite
    title: "falkordblite source at ae24b52 (evidence copy)"
  - id: falkordblite-readme
    resource: https://github.com/FalkorDB/falkordblite
    title: "falkordblite source at ae24b52 (evidence copy)"
  - id: falkordblite-src
    resource: https://github.com/FalkorDB/falkordblite
    title: "falkordblite source at ae24b52 (evidence copy)"
  - id: gh-falkordblite
    resource: https://api.github.com/repos/FalkorDB/falkordblite
    title: "FalkorDBLite GitHub API (rate-limited body)"
  - id: readme
    resource: https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md
    title: "GraphRAG-SDK README (main)"
  - id: run-claims
    resource: references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt
    title: "local run output (this research)"
  - id: run-inject
    resource: references/evidence/graphrag-sdk/runs/sdk-e2e-inject-pypi140.txt
    title: "local run output (this research)"
  - id: run-rank-main
    resource: references/evidence/graphrag-sdk/runs/vector-rank-main-35e67a0.txt
    title: "local run output (this research)"
  - id: run-rank-pypi
    resource: references/evidence/graphrag-sdk/runs/vector-rank-pypi140.txt
    title: "local run output (this research)"
  - id: run-raw
    resource: references/evidence/graphrag-sdk/runs/raw-driver-probe-pypi140.txt
    title: "local run output (this research)"
  - id: run-smoke
    resource: references/evidence/graphrag-sdk/runs/lite-smoke.txt
    title: "local run output (this research)"
  - id: run-tcp
    resource: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt
    title: "local run output (this research)"
  - id: run-tcp-notes
    resource: references/evidence/graphrag-sdk/runs/commands.txt
    title: "local run output (this research)"
  - id: src-pypi-api
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-pypi-conn
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-pypi-main
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-pypi-storage
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
  - id: src-pypi-storage-ontology
    resource: https://pypi.org/project/graphrag-sdk/1.4.0/
    title: "graphrag-sdk 1.4.0 source snapshot (evidence copy)"
evidence:
  - { name: configuration.txt, url: "https://docs.falkordb.com/graphrag/configuration", url_basis: inferred, sha256: 236cc936b838ef8845465aa04f852feea891a7d434c91cd35939be389045b7de, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: storage.txt, url: "https://docs.falkordb.com/graphrag/storage", url_basis: inferred, sha256: d75adfc930efbdc1181c912c5988ecc08fa9abfa16ceccf9568ea379a59ce606, retrieved_at: 2026-10-15T19:24:06Z, method: curl, redistributed: false }
  - { name: core_connection.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: cc6f9d24023558ee718734f18a7f35f1e3c0ddbb32ef1fec688494a193529bef, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { name: api_main.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: b4245004e02fdb9095e580b35fc32797abd19f1566f1492261dbd5b00c60521d, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { name: storage_vector_store.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: 57abad41d65d1aad6f590e368e2ffffa1801bf1360de75fac8fd474f853d318e, retrieved_at: 2026-10-15T19:50:00Z, method: command, redistributed: false }
  - { name: core_connection.py, url: "https://github.com/FalkorDB/GraphRAG-SDK/tree/35e67a0", url_basis: inferred, sha256: c0e43c0630eabfb3690087c79285f2153b0381d493e3e111c6e9aaf21de084e2, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
  - { name: async_falkordb_client.py, url: "https://github.com/FalkorDB/falkordblite/blob/ae24b52/redislite/async_falkordb_client.py", url_basis: inferred, sha256: dc4dbd89d47ecc5c10b833b687a84ae613ace84a69dd4e2ed6d3ba373207ec31, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
  - { name: README.txt, url: "https://github.com/FalkorDB/falkordblite/blob/ae24b52/README.md", url_basis: inferred, sha256: 668d42ad26430520bc50891f1bc36c69efd3549281bd6504c020a461115513b2, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
  - { name: pypi-falkordblite.json, url: "https://pypi.org/pypi/falkordblite/json", url_basis: inferred, sha256: 97ceafd4f0cd8e4e4f79dc68de4593ed420d08928db3e4c4b25fb5abf366b070, retrieved_at: 2026-10-15T19:36:00Z, method: curl, redistributed: false }
  - { name: gh-falkordblite.json, url: "https://api.github.com/repos/FalkorDB/falkordblite", url_basis: inferred, sha256: cd04fb995c6f474f09f6ec18238ea8b67f10f2c129fdbfa973f2d3ca0a63c5de, retrieved_at: 2026-10-15T19:36:00Z, method: curl, redistributed: false }
  - { file: references/evidence/graphrag-sdk/gh-falkordblite-raw-readme-404.txt, sha256: d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed, retrieved_at: 2026-10-15T19:36:00Z, method: curl }
  - { name: gh-issues-all-p1.json, url: "https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all&page=1", url_basis: inferred, sha256: dd881082d44be55d752428bc8e05776beed69cd9c52b353b512df3369fcc0634, retrieved_at: 2026-10-15T19:36:22Z, method: command, redistributed: false }
  - { file: references/evidence/graphrag-sdk/runs/lite-smoke.txt, sha256: 2802962efffe184fc13c20327fc70cdca7f25c586f1ee10c6be4e308ee74f969, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/lite-tcp-probe.txt, sha256: f6f89cfe9e6ee88d2b6c5276a20e00a1e11e5dcce28547f9746ac8f212c1ada8, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt, sha256: 020b6a709e6bb4c6c18a3ae7c5e5c592e926dab1f9ca783dfb1889ac5224f283, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/sdk-e2e-inject-pypi140.txt, sha256: 955ef9ec6257e43575a3699f1ac3e5b48655725e63bd10500e3a15b398da101b, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/raw-driver-probe-pypi140.txt, sha256: aa922f9e099a38372916366243837763b8bdb66680622e264fa0b2f7fc87c499, retrieved_at: 2026-10-15T20:10:00Z, method: command }
  - { name: storage_ontology_store.py, url: "https://pypi.org/project/graphrag-sdk/1.4.0/", sha256: 1343680dfb32c86aba13029c0d217e15ffb08ed53841d90a703647606a719f77, retrieved_at: 2026-10-15T20:10:00Z, method: command, redistributed: false }
  - { file: references/evidence/graphrag-sdk/runs/falkordb-module-info.txt, sha256: 2deed28dfeab5d582e67d6f47be3f8c6c4ce5539c8db50e225e7c4f731875558, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/graphrag-sdk/runs/pip-freeze-sdk-venv.txt, sha256: 023d5dde752cccb89c3de0405bf2b1b316859e21137cc2896f886b907dcfce7b, retrieved_at: 2026-10-15T20:00:00Z, method: command }
verified: { by: process:cross-check, at: 2026-10-15T20:00:00Z }
---

# GraphRAG SDK to FalkorDB connectivity

## Short answer

- The SDK talks to FalkorDB through the **async `falkordb` Python client over a `redis.asyncio` connection pool**. You give it `host`, `port`, and `graph_name` in a `ConnectionConfig`. It also accepts a pre-built `FalkorDBConnection`. It does **not** accept a bare driver or redis client object.[^src-pypi-conn][^src-pypi-main][^docs-configuration]
- **falkordblite works, but only through one of two workarounds, both verified:**
  1. **Unmodified SDK.** Start falkordblite's embedded server with a TCP port (`serverconfig={"port": "16400", "bind": "127.0.0.1"}`) and point `ConnectionConfig(host="127.0.0.1", port=16400)` at it. Full ingest, finalize, retrieve, completion, and index creation passed.[^run-tcp]
  2. **In-process injection.** Subclass `FalkorDBConnection`, build falkordblite's `AsyncFalkorDB` in `_ensure_client()`, and set `_driver`, `_pool`, `_graph`. The same run also passed. This depends on private attributes.[^run-inject]
- **Not supported.** Passing `AsyncFalkorDB` directly as `GraphRAG(connection=...)` fails with `AttributeError 'AsyncFalkorDB' object has no attribute 'config'`.[^run-raw]

## How the SDK builds its client (1.4.0)

`ConnectionConfig` is a dataclass with `host="localhost"`, `port=6379`, `username`, `password`, `graph_name="knowledge_graph"`, `max_connections=16`, `retry_count=3`, `retry_delay=1.0`, `pool_timeout=30.0`, `query_timeout_ms=10_000`, and TLS fields (`ssl`, `ssl_cert_reqs="required"`, …). Field names verified in the installed class.[^run-claims]

Docs: `ConnectionConfig is a dataclass that defines how the SDK connects to a FalkorDB instance. It is passed to GraphRAG or used to create a FalkorDBConnection directly.`[^docs-configuration]

`FalkorDBConnection._ensure_client()` (1.4.0, `core/connection.py`) does:[^src-pypi-conn]

```python
from falkordb.asyncio import FalkorDB
from redis.asyncio import BlockingConnectionPool
...
self._pool = self._pool or BlockingConnectionPool(**pool_kwargs)   # host, port, username, password, max_connections, timeout, decode_responses=True
self._driver = FalkorDB(connection_pool=self._pool)
self._graph = self._driver.select_graph(self.config.graph_name)
```

Class docstring: `Wraps ``falkordb.asyncio.FalkorDB`` with:` followed by the redis pool and retry bullets.[^src-pypi-conn]

`GraphRAG.__init__` decides between the two forms:[^src-pypi-api]

```python
if isinstance(connection, ConnectionConfig):
    self._conn = FalkorDBConnection(connection)
else:
    self._conn = connection
```

The SDK then depends on several members of `self._conn` beyond `query()`. A substitute must provide all of them:

- `query(cypher, params, timeout=, expected_errors=)`: used about 92 times across the package.
- `config` (with `graph_name`): read in `GraphRAG.__init__` through `OntologyStore(self._conn, self._conn.config.graph_name)`. This is the line that fails for a raw driver.
- `_ensure_client()`, `_driver`: `storage/ontology_store.py` calls `driver = self._conn._driver` and `driver.select_graph(...)`.
- `_pool`: used by `ping()`, `delete_graph()` and `ontology_store` to make `redis.asyncio.Redis(connection_pool=...)`.
- `close()`, `delete_graph()`, `ping()`.

Grep counts over the installed 1.4.0 package (`_conn.` member uses): `query` 76, `_ensure_client` 2, `config` 1, `_driver` 1, `_pool` 1, `delete_graph` 1, `close` 1.[^src-pypi-conn][^src-pypi-api][^src-pypi-storage-ontology]

Retry and circuit breaker: query retries use `retry_count`, and non-transient messages are not retried. Docs: `Queries are retried up to retry_count times with linear backoff (retry_delay * attempt_number).` **Code differs:** `core/connection.py` computes `base_delay = self.config.retry_delay * (2**attempt)` and then sleeps `base_delay * (0.5 + random.random())`, which is exponential with jitter.[^docs-configuration][^src-pypi-conn]

`query_timeout_ms` defaults to `10_000` (10 seconds). Docs: `Per-query timeout in milliseconds forwarded to FalkorDB. Set to None to disable.`[^docs-configuration]

`graph_name` is the per-tenant isolation key. README: `graph_name = per-tenant isolation`.[^readme]

## falkordblite: what it is and how it is built

- `falkordblite` 0.10.0 (PyPI, uploaded 2026-05-02) is "FalkorDB embedded in a Python package". Requires Python `>=3.12.0`. Dependencies: `redis>=4.5`, `falkordb>=1.2.0`, `psutil`, `setuptools>38.0`.[^falkordblite-pypi]
- The README: `It provides enhanced versions of the Redis-Py Python bindings with FalkorDB graph database functionality.` and `The falkordblite module requires Python 3.12 or higher.`[^falkordblite-readme]
- Note: the falkordblite `raw.githubusercontent.com/.../main/README.md` URL returned 404 (evidence `gh-falkordblite-README.md` holds the 404 body). The clone's README at `ae24b52` is the saved copy. The GitHub API for the repo was rate-limited when we tried, so `https://api.github.com/repos/FalkorDB/falkordblite` holds the rate-limit body.[^gh-falkordblite]
- Bundled binaries (from the wheel, verified after install): `redislite/bin/redis-server` (Redis 8.6.2 per `package_metadata.json`) and `redislite/bin/falkordb.so`. `MODULE LIST` on the embedded server reports graph module `ver 41803` (FalkorDB 4.18.3 encoding), so the bundled module is **FalkorDB 4.18.3**.[^falkordb-module-info]
- Python API: `redislite.falkordb_client.FalkorDB` (sync) and `redislite.async_falkordb_client.AsyncFalkorDB` (async). The async class subclasses `falkordb.asyncio.FalkorDB` but has its own constructor: `def __init__(self, dbfilename: Optional[str] = None, serverconfig: Optional[dict] = None, **kwargs):`, which builds its own `AsyncRedis`. It does not take a `connection_pool=` argument.[^falkordblite-src]
- Default server config has `'port': '0'`, so no TCP listener. The server listens on a unix socket in a temp directory only. Setting `serverconfig={"port": ...}` opens TCP.[^falkordblite-conf][^run-tcp]

Smoke test (ran): sync `CREATE`/`MATCH` returned `['Alice']`, async `CREATE` returned `['Bob']`, `RETURN 1 + 1` returned `[[2]]`.[^run-smoke]

## Route 1: unmodified SDK over TCP (verified)

```python
from redislite.async_falkordb_client import AsyncFalkorDB
server = AsyncFalkorDB("/path/embedded.db", serverconfig={"port": "16400", "bind": "127.0.0.1"})
rag = GraphRAG(connection=ConnectionConfig(host="127.0.0.1", port=16400, graph_name="g"), llm=..., embedder=...)
```

Verified with a deterministic fake LLM, a hash embedder, and a regex non-LLM extractor (see [pluggability](/graphrag-sdk/pluggability.md)). Results:[^run-tcp]

- `ingest` created 6 nodes and 8 relationships, and 1 chunk.
- `finalize` returned `indexes={'vector_Chunk': True, 'vector_Entity': True, 'vector_RELATES': True, 'fulltext_Chunk': True, 'fulltext_Entity': True}`.
- `MATCH (a)-[r:RELATES]->(b)` returned `['Alice Johnson', 'WORKS_AT', 'Acme Corp']` and `['Acme Corp', 'LOCATED_IN', 'London']`.

Caveats observed:

- **Bind address.** Without `bind`, the embedded server listened on `0.0.0.0` (seen with `ss -ltnp`). Use `"bind": "127.0.0.1"`.[^run-tcp-notes]
- **Lifetime.** The embedded server belongs to the Python process. A crashed run left a `redis-server` process holding the port, and the next run failed with `RedisLiteServerStartError`. We killed it manually.[^run-tcp-notes]
- **Port collisions.** A first attempt on port 6390 failed. Another process held that port, and redislite's startup does not report the bind error clearly.[^run-tcp-notes]

## Route 2: in-process injection (verified, private API)

```python
class FalkorDBLiteConnection(FalkorDBConnection):
    def __init__(self, config, driver):
        super().__init__(config)
        self._injected = driver
    def _ensure_client(self):
        if self._driver is not None: return
        self._driver = self._injected
        self._pool = self._injected.connection.connection_pool
        self._graph = self._driver.select_graph(self.config.graph_name)
```

Results match Route 1 (`runs/sdk-e2e-inject-pypi140.txt`). No TCP port is opened. Caveat: this relies on `_ensure_client`, `_driver`, `_pool` and `_graph`. Those are private attributes and may change in any SDK release. Test before upgrading.[^run-inject]

## Route 3: raw driver (fails)

Passing `AsyncFalkorDB(...)` as `GraphRAG(connection=...)` raises `AttributeError 'AsyncFalkorDB' object has no attribute 'config'` at construction, because `GraphRAG.__init__` reads `self._conn.config.graph_name`.[^run-raw]

## Vector and fulltext index syntax

The SDK creates indexes in `VectorStore`. Source (1.4.0 `storage/vector_store.py`):[^src-pypi-storage]

```
CREATE VECTOR INDEX FOR (n:Chunk) ON (n.embedding) OPTIONS {dimension:256, similarityFunction:'cosine'}
CREATE VECTOR INDEX FOR (n:__Entity__) ON (n.embedding) OPTIONS {dimension:256, similarityFunction:'cosine'}
CREATE VECTOR INDEX FOR ()-[e:RELATES]->() ON (e.embedding) OPTIONS {dimension:256, similarityFunction:'cosine'}
CALL db.idx.fulltext.createNodeIndex('Chunk', 'text')
CALL db.idx.fulltext.createNodeIndex('__Entity__', 'name', 'description')
```

The `dimension` comes from `embedding_dimension` (default 256). Docs: `Vector indexes use FalkorDB’s native vector index syntax:` followed by the same `CREATE VECTOR INDEX` form.[^docs-storage]

Query syntax used by the SDK:

- Chunk and entity: `CALL db.idx.vector.queryNodes('Chunk', 'embedding', $top_k, vecf32($vector)) YIELD node, score ...`
- RELATES edges: `CALL db.idx.vector.queryRelationships('RELATES', 'embedding', $top_k, vecf32($vector)) YIELD relationship AS r, score ...`
- Fulltext: `CALL db.idx.fulltext.queryNodes('Chunk', $query_text)`.[^src-pypi-storage]

Index creation is idempotent: "already indexed" errors are caught. Logged at DEBUG on the run: `Non-transient FalkorDB query failure: ResponseError: Attribute 'embedding' is already indexed`.[^run-tcp][^src-pypi-conn]

**Are vector indexes required?** Chunk and entity search call the vector procedures directly. For RELATES edges, if `db.idx.vector.queryRelationships` raises, the code logs `Edge vector query not available, falling back to Cypher scan` and runs a brute-force `vec.cosineDistance` scan over all RELATES edges. The fallback is in source. It was not run with the index removed, so the fallback behavior is source-only.[^src-pypi-storage]

Verified live: after `finalize()`, `CALL db.indexes()` listed vector indexes on `RELATES.embedding`, `__Entity__.embedding`, `Chunk.embedding` (dimension 256, cosine), and fulltext on `Chunk.text`, `__Entity__.name`, `__Entity__.description`.[^run-tcp]

## Ordering bug in 1.4.0 (vector scores) (verified)

Issue #294 (closed): `VectorStore.search_chunks`, `search_entities` and `search_relationships` return distance (0 = identical) and order `ORDER BY score DESC`, which puts the worst match first. Issue body: `The exact self-match scores 0.0000 and is ranked **last**.`[^gh-issues]

We reproduced this on PyPI 1.4.0. Querying with the exact text of a stored chunk returned `score=0.0000 text='Erik Hort was born in Montebello in February 1987.'` as the **last** of 3 rows. The same probe on main commit `35e67a0` put the exact match first with `score=1.0000`.[^run-rank-pypi][^run-rank-main]

Main's code is `"RETURN node.id AS id, node.text AS text, (1-score) AS score "` then `ORDER BY score DESC`. The 1.4.0 release still has `RETURN node.id AS id, node.text AS text, score ... ORDER BY score DESC` for chunks, and the same pattern for entities and relationships. **Use main, or patch the query, before relying on vector ranking with 1.4.0.** The RELATES edge query in 1.4.0 uses the same raw-score pattern. Not run.[^src-pypi-storage]

## FalkorDB 6.x incompatibilities (open, reported 2026-10-15)

Issue #344 (open, created 2026-10-15): `SDK incompatibilities with FalkorDB 6.0.x (Rust engine)`. The author says it was reproduced on `FalkorDB 6.0.2 (Rust)`. Quotes from the issue:[^gh-issues]

> `Fulltext indexes are never created. VectorStore.create_chunk_fulltext_index() and create_entity_fulltext_index() use db.idx.fulltext.createNodeIndex(...), which 6.0.2 rejects (vector_store.py:149). As a result, fulltext search returns nothing.`

> `drop_*_vector_index doesn’t drop anything. It calls db.idx.vector.drop, which doesn’t exist (vector_store.py:162). This one is also broken on 4.22, so it isn’t caused by Rust.`

Our tests ran on FalkorDB module 4.18.3 (falkordblite bundle). **Not tested on 6.x.** A FalkorDB 6.x server would need its own run.

## Open questions

- Does the docs' Docker image `falkordb/falkordb:latest` (used in the README quick start) map to 6.x? Not checked; no image was pulled.
- Is a supported, public injection hook planned? Today's workaround is private-API subclassing.
- Does `falkordblite` work with Python 3.10 or 3.11? Its package requires 3.12, so the SDK's 3.10 floor can't be combined with falkordblite on those versions.

[^docs-configuration]: `https://docs.falkordb.com/graphrag/configuration`
[^docs-storage]: `https://docs.falkordb.com/graphrag/storage`
[^readme]: `https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/README.md`
[^src-pypi-conn]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-pypi-api]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-pypi-storage]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-pypi-storage-ontology]: `https://pypi.org/project/graphrag-sdk/1.4.0/`
[^src-pypi-main]: `https://github.com/FalkorDB/GraphRAG-SDK/tree/35e67a0`
[^falkordblite-pypi]: `https://pypi.org/pypi/falkordblite/json`
[^falkordblite-readme]: `https://github.com/FalkorDB/falkordblite/blob/ae24b52/README.md`
[^falkordblite-src]: `https://github.com/FalkorDB/falkordblite/blob/ae24b52/redislite/async_falkordb_client.py`
[^falkordblite-conf]: falkordblite `redislite/configuration.py` line 39 (`'port': '0',`), in the installed wheel; not saved as evidence
[^falkordb-module-info]: `references/evidence/graphrag-sdk/runs/falkordb-module-info.txt`
[^run-claims]: `references/evidence/graphrag-sdk/runs/claims-probe-pypi140.txt`
[^run-smoke]: `references/evidence/graphrag-sdk/runs/lite-smoke.txt`
[^run-tcp]: `references/evidence/graphrag-sdk/runs/sdk-e2e-tcp-pypi140.txt`
[^run-tcp-notes]: `references/evidence/graphrag-sdk/runs/commands.txt` (port notes) and session observations recorded there
[^run-inject]: `references/evidence/graphrag-sdk/runs/sdk-e2e-inject-pypi140.txt`
[^run-raw]: `references/evidence/graphrag-sdk/runs/raw-driver-probe-pypi140.txt`
[^run-rank-pypi]: `references/evidence/graphrag-sdk/runs/vector-rank-pypi140.txt`
[^run-rank-main]: `references/evidence/graphrag-sdk/runs/vector-rank-main-35e67a0.txt`
[^gh-issues]: `https://api.github.com/repos/FalkorDB/GraphRAG-SDK/issues?state=all&page=1`
[^gh-falkordblite]: `references/evidence/graphrag-sdk/gh-falkordblite-raw-readme-404.txt` (404) and `https://api.github.com/repos/FalkorDB/falkordblite` (rate-limit body)
