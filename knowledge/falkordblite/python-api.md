---
type: Reference
title: FalkorDBLite Python API
description: How to open an embedded FalkorDB, run Cypher with parameters, use the async client, and reach the same server from other Redis or falkordb-py clients over a unix socket or TCP.
resource: https://github.com/FalkorDB/falkordblite/blob/master/README.md
tags: [falkordblite, python-api, cypher, async, falkordb-py]
status: current
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/falkordblite-agent, at: 2026-10-15T19:35:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:35:00Z }
sources:
  - id: readme
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/README.md
    title: FalkorDBLite README (master)
  - id: src-falkordb-client
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/falkordb_client.py
    title: redislite/falkordb_client.py (master)
  - id: src-async-client
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/async_falkordb_client.py
    title: redislite/async_falkordb_client.py (master)
  - id: src-init
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/__init__.py
    title: redislite/__init__.py (master)
  - id: redislite-client
    resource: https://pypi.org/project/falkordblite/0.10.0/
    title: redislite/client.py as shipped in falkordblite 0.10.0 wheel
  - id: docs-async
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/docs/ASYNC_API.md
    title: docs/ASYNC_API.md (master)
  - id: local-run
    resource: references/evidence/falkordblite/capabilities-run-all-output.txt
    title: Local probe runs in throwaway venv
  - id: external
    resource: references/evidence/falkordblite/external-client-probe-output.txt
    title: External falkordb-py client over unix socket output
  - id: gh-issues
    resource: https://api.github.com/repos/FalkorDB/falkordblite/issues?state=all
    title: GitHub issues and PRs (state=all)
  - id: redislite-config
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/configuration.py
    title: redislite/configuration.py (master)

evidence:
  - { name: readme-raw.txt, url: "https://raw.githubusercontent.com/FalkorDB/falkordblite/master/README.md", sha256: 668d42ad26430520bc50891f1bc36c69efd3549281bd6504c020a461115513b2, retrieved_at: 2026-10-15T19:23:42Z, method: curl, redistributed: false }
  - { name: src__redislite_falkordb_client.py, url: "https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/falkordb_client.py", url_basis: inferred, sha256: 51dfb1ddc75772ea14e6b127b53fdafae1ac6d8143bed1295d3cf2dc9f457a9a, retrieved_at: 2026-10-15T19:23:50Z, method: curl, redistributed: false }
  - { name: src__redislite_async_falkordb_client.py, url: "https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/async_falkordb_client.py", url_basis: inferred, sha256: dc4dbd89d47ecc5c10b833b687a84ae613ace84a69dd4e2ed6d3ba373207ec31, retrieved_at: 2026-10-15T19:23:51Z, method: curl, redistributed: false }
  - { name: src__redislite___init__.py, url: "https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/__init__.py", url_basis: inferred, sha256: fc1aedab64b7afc28cf2f0074c672e90bc28536de070ab2809a2f356b8a778e2, retrieved_at: 2026-10-15T19:23:50Z, method: curl, redistributed: false }
  - { name: wheel-redislite-client.py.txt, url: "https://pypi.org/project/falkordblite/0.10.0/", url_basis: inferred, sha256: b1dba5d9f35c0de1df504b23c148058c247c2f95cf521cdab13becdc4670db9b, retrieved_at: 2026-10-15T19:29:15Z, method: command, redistributed: false }
  - { name: src__docs_ASYNC_API-raw.txt, url: "https://raw.githubusercontent.com/FalkorDB/falkordblite/master/docs/ASYNC_API.md", url_basis: inferred, sha256: f509c2d5b484cdb27d3d8ce54c880e83aede8b2b46bdb59c8cd9c1f7ee20b9e1, retrieved_at: 2026-10-15T19:23:52Z, method: curl, redistributed: false }
  - { file: references/evidence/falkordblite/capabilities-run-all-output.txt, sha256: 37a128b6a40f386e0e4ef0739df1b32179e45be029cb102036b0ccc987471cc5, retrieved_at: 2026-10-15T19:27:36Z, method: command }
  - { file: references/evidence/falkordblite/api-connection-probe-output.txt, sha256: 4d4750d52c4d377e06f183e8a85cc34477c156b843d9221dbecf429ff650d385, retrieved_at: 2026-10-15T19:27:50Z, method: command }
  - { file: references/evidence/falkordblite/external-client-probe-output.txt, sha256: 23cf323c60abbe891e7108360bdcc90210e51b496d10c5f6c231217eef834130, retrieved_at: 2026-10-15T19:28:30Z, method: command }
  - { file: references/evidence/falkordblite/tcp-probe-output.txt, sha256: d1268bc5da784771425b5df1bd51f0c28f3daad8c71fc7ce931308a75233f863, retrieved_at: 2026-10-15T19:31:03Z, method: command }
  - { file: references/evidence/falkordblite/close-shutdown-probe-output.txt, sha256: 9d5d951be26f6d503102b34abcaa51b8f87514f33961b82564b2be134968c51a, retrieved_at: 2026-10-15T19:27:50Z, method: command }
---

# Import names

The distribution is `falkordblite` but the importable package is `redislite`. The README uses:

> `from redislite.falkordb_client import FalkorDB`

[^readme]

Also exported from the package root (`redislite/__init__.py`):

> `from .falkordb_client import FalkorDB, Graph  # NOQA`

[^src-init]

Gotcha, observed: `redislite.__version__` reports `0.0.0` in the installed 0.10.0 wheel, because the code looks up the metadata name `redislite`, not `falkordblite`:

> `redislite 0.0.0 redis-server 8.6.2 falkordb.so ...`

[^local-run]

# Open a database

```python
from redislite.falkordb_client import FalkorDB

db = FalkorDB('/tmp/falkordb.db')     # path = RDB file, server data lives there
g = db.select_graph('social')          # returns a Graph
```

- A path opens or creates a persistent database. README: "FalkorDB data persists between sessions. Open the same database file to access previously stored graphs:" [^readme]
- Tested: `CREATE` in one process, a new process with the same file path read the 4 nodes, the vector index and the fulltext index back. See [capabilities-test](/falkordblite/capabilities-test.md#persistence).
- Passing `serverconfig` changes the server config. Tested with `{"port": "6399"}`. Constructor source: `def __init__(self, dbfilename=None, serverconfig=None, **kwargs):` [^src-falkordb-client]
- No path: a temp directory is created. In the client code, `self.redis_dir = tempfile.mkdtemp()` and the DB dir falls back to it, and cleanup calls `shutil.rmtree(self.redis_dir)`. [^redislite-client] This was read in code and not run as a test. See [open questions](#open-questions).
- In-memory mode is not documented in the README and was not tested.

# Graphs and Cypher

```python
g.query('CREATE (p:Person {name: "Alice", age: 30}) RETURN p')
res = g.query('MATCH (p:Person) RETURN p.name, p.age')
for row in res.result_set:
    print(row)
g.ro_query('MATCH (p:Person) RETURN count(p)')
db.list_graphs()
```

[^readme]

- `select_graph(name)` returns a `Graph` subclass of falkordb-py's `Graph`. `db.list_graphs()` returns graph names. Tested: returned `['vecgraph', 'roads']`. [^local-run]
- `g.query(cypher, params_dict)` passes parameters as a dict. Tested: `g.query("CREATE (:T {i: $i})", {"i": i})` in 20 threads on one handle wrote 20 nodes with no error. [^local-run]
- Keyword form used in the README async example: `params={'name': 'Alice'}`. [^readme]
- `g.ro_query(...)` runs read-only. Tested: a `CREATE` through it was rejected with `graph.RO_QUERY is to be executed only on read-only queries`. [^local-run]
- `res.result_set` is a list of rows. A `vecf32(...)` property reads back as a Python list of floats. Tested: `[[[1.0, 0.0, 0.0, 0.0]]]`. [^local-run]
- `g.delete()` appears in the README but was not run. [^readme]

## Vectors and full text

Query syntax tested in [capabilities-test](/falkordblite/capabilities-test.md):

```cypher
CREATE VECTOR INDEX FOR (d:Doc) ON (d.emb) OPTIONS {dimension: 4, similarityFunction: 'cosine'}
CALL db.idx.vector.queryNodes('Doc', 'emb', $k, vecf32($q)) YIELD node, score RETURN node.id, score
CALL db.idx.fulltext.createNodeIndex('Doc', 'title')
CALL db.idx.fulltext.queryNodes('Doc', 'search') YIELD node, score RETURN node.id, score
```

# Close

```python
db.close()
```

`FalkorDB.close()` calls the client cleanup. [^src-falkordb-client] The cleanup only stops the server when no other client is connected:

> `            if self._connection_count() <= 1:`

[^redislite-client]

Observed: `close()` stopped the server that the test had started, and an earlier server from another test stayed up because it was still counted as in use. [^local-run] See [limitations-and-open-issues](/falkordblite/limitations-and-open-issues.md#orphaned-server-processes).

# Async API

```python
import asyncio
from redislite.async_falkordb_client import AsyncFalkorDB

async def main():
    async with AsyncFalkorDB('/tmp/falkordb.db') as db:
        g = db.select_graph('social')
        await g.query('CREATE (n:Person {name: $name}) RETURN n', params={'name': 'Alice'})
        res = await g.query('MATCH (n:Person) RETURN n.name')
        print(res.result_set)

asyncio.run(main())
```

[^readme]

- Classes: `AsyncFalkorDB`, `AsyncGraph`, `AsyncQueryResult`, plus `AsyncRedis` and `AsyncStrictRedis` in `redislite/async_client.py`. [^src-init] [^src-async-client]
- Tested: parameterized `CREATE`, a `MATCH` read, a vector index, and a `db.idx.vector.queryNodes` call all ran through `await`. [^local-run]
- Async UDF helpers exist in source (`udf_load`, `udf_list`, `udf_delete`). They were not tested. [^src-async-client]
- `async with` is supported. Source: `async def __aenter__(self):` and `async def close(self):`. [^src-async-client]
- Known issue: the test run printed `RuntimeWarning: coroutine 'AsyncManagementCommands.shutdown' was never awaited` from `redislite/client.py:112`. This matches open GitHub issue `#61 Warnings in tests`. [^local-run] [^gh-issues]

# Redis key-value API

```python
from redislite import Redis
r = Redis('/tmp/redis.db')
r.set('key', 'value')
```

[^readme]

Not run. The same embedded server answers ordinary Redis commands. Tested through redis-py over the unix socket with `GRAPH.QUERY`. [^local-run]

# Connection model and other clients

The server listens on a unix socket by default. The socket path is in a `redis.socket` file under a temp dir:

> `redis-server unixsocket:/tmp/tmpn6unc0bt/redis.socket`

[^local-run]

How to get the URL or path:

```python
sock = db.client.connection_pool.connection_kwargs.get("path")
```

Tested results:

| Client | Transport | Result |
|---|---|---|
| redis-py (`redis.Redis(unix_socket_path=sock)`) | unix socket | `GRAPH.QUERY` returned `[[1]]` |
| pure falkordb-py (`falkordb.FalkorDB(unix_socket_path=sock)`), separate process, no redislite import | unix socket | count and vector KNN both returned |
| pure falkordb-py (`falkordb.FalkorDB(host="127.0.0.1", port=6399)`) after `serverconfig={"port": "6399"}` | TCP | count returned `[[1]]` |
| second Python process opening the same DB file while the first is alive | same unix socket | got the same socket path and read the data |

[^local-run] [^external]

- TCP is off by default because the default config has `'port': '0'`. [^redislite-config]
- The unix socket permission default is `700` and the README calls the setup secure: "Uses a secure default Redis configuration that is only accessible by the creating user on the computer system it is run on." [^readme] [^redislite-config]
- Whether graphrag-sdk connects this way was not tested. That is outside this area. See [open questions](#open-questions).

# Known API gaps seen in testing

- `CREATE CONSTRAINT ON (x:Persona) ASSERT x.name IS UNIQUE` is rejected with `Invalid constraint command use the GRAPH.CONSTRAINT command instead`. `GRAPH.CONSTRAINT CREATE ... UNIQUE` works after an exact-match index exists. [^local-run] [^gh-issues]
- `CALL db.procedures()` is not registered. Use `CALL dbms.procedures()`. [^local-run]

Full details: [capabilities-test](/falkordblite/capabilities-test.md) and [limitations-and-open-issues](/falkordblite/limitations-and-open-issues.md).

# Open questions

- Behaviour of `FalkorDB()` with no path (temp dir): read in code, not run. Whether data is discarded at exit is unconfirmed.
- In-memory mode: not documented; not tested.
- Whether `graphrag-sdk` can point at the unix socket URL without code changes. Not tested here.
- `g.delete()`, `Redis` key-value calls, and `AsyncRedis` were not run.

[^readme]: FalkorDBLite README, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/README.md`.
[^src-init]: `redislite/__init__.py`, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/__init__.py`.
[^src-falkordb-client]: `redislite/falkordb_client.py`, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/falkordb_client.py`.
[^src-async-client]: `redislite/async_falkordb_client.py`, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/async_falkordb_client.py`.
[^redislite-client]: `redislite/client.py` from the 0.10.0 wheel, evidence `https://pypi.org/project/falkordblite/0.10.0/`.
[^redislite-config]: `redislite/configuration.py`, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/configuration.py`.
[^local-run]: Probe outputs: `references/evidence/falkordblite/capabilities-run-all-output.txt`, `api-connection-probe-output.txt`, `close-shutdown-probe-output.txt`, `constraints-command-probe-output.txt`, `runtime-versions.txt`.
[^external]: `references/evidence/falkordblite/external-client-probe-output.txt` and `tcp-probe-output.txt`, produced by `external-client-driver.py` and `tcp-probe.py`.
[^gh-issues]: GitHub issues list, evidence `https://api.github.com/repos/FalkorDB/falkordblite/issues?state=open`.
