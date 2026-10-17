---
type: Concept
title: FalkorDB Python client (falkordb package)
description: Install, connect, query, parameters, async usage, index and constraint helpers, result object shape and the query-building details of falkordb-py 1.8.0, verified against the source and a live 4.22.1 server.
resource: https://pypi.org/project/FalkorDB/
tags: [falkordb, python, client, falkordb-py, async, parameters, result-set]
status: stable
generated: { by: claude-haiku-5-5/falkordb-agent, at: 2026-10-15T19:45:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:45:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: pypi-falkordb
    resource: https://pypi.org/pypi/falkordb/json
    title: FalkorDB 1.8.0 on PyPI (long description and metadata)
    last_modified: 2026-10-14T11:54:31Z
  - id: pypi-sdist
    resource: https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz
    title: falkordb 1.8.0 sdist (code identical to opensrc copy)
    last_modified: 2026-10-14T11:54:32Z
  - id: falkordb-py-repo
    resource: https://github.com/falkorDB/falkordb-py
    title: falkordb-py repository (tag 1.8.0)
  - id: docs-clients
    resource: https://docs.falkordb.com/getting-started/clients
    title: FalkorDB Client Libraries
  - id: docs-graph-query
    resource: https://docs.falkordb.com/commands/graph.query
    title: GRAPH.QUERY
  - id: docs-graph-profile
    resource: https://docs.falkordb.com/commands/graph.profile
    title: GRAPH.PROFILE
  - id: docs-graph-explain
    resource: https://docs.falkordb.com/commands/graph.explain
    title: GRAPH.EXPLAIN
  - id: docs-vector-index
    resource: https://docs.falkordb.com/cypher/indexing/vector-index
    title: Vector Indexing (Python example)
evidence:
  - { name: pypi-falkordb.json, url: "https://pypi.org/pypi/falkordb/json", sha256: d0c590052d766d723cad9285c97cafbc863bf651010345ac8d83d50159daf6bc, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { file: references/evidence/falkordb/pypi-sdist-1.8.0-url-and-sha256.txt, sha256: 8af2d544b54ccb8f692c778a6bb417c02261f0843319ccb6dc7c9e170423360e, retrieved_at: 2026-10-15T19:45:00Z, method: curl }
  - { name: pyclient-1.8.0-source-excerpts.txt, url: "https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz", sha256: ae5e72fa77ed957a9f477e2391674715fdfdbba5c352d9c53568073b9d15374c, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
  - { name: pyclient-1.8.0-pyproject.toml.txt, url: "https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz", sha256: 2095e5d5610087dfe3cdc3f69c33a66c0926bc6f7732500a51e8ef36a5cf1794, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
  - { name: docs-getting-started__clients.txt, url: "https://docs.falkordb.com/getting-started/clients", sha256: e5eeef46771daf198ef22df2f2a8cded0815f155f0ea57e3acde11daf48fd3db, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-commands__graph.profile.txt, url: "https://docs.falkordb.com/commands/graph.profile", sha256: 3cdeb327b32e35dc86dfb0bcb7c698b6bd49f596ed75457785ffaa99e43a11ea, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-commands__graph.explain.txt, url: "https://docs.falkordb.com/commands/graph.explain", sha256: 8f8d1254f7970d3122d6d1053cc4795de32ccb2625f317e374762c3be9a06fd1, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { file: references/evidence/falkordb/run-4.22.1-client-api.txt, sha256: 76e5b0772a3a31f282d2d7b307c2d04b35b2407b4de7cc19f456deffabe7a853, retrieved_at: 2026-10-15T19:58:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-pypi-sync-example.txt, sha256: 6a55935e20b751e5ce8130ff40792ae23f8f919afe0e6df1ca34c4d62b6c1e87, retrieved_at: 2026-10-15T20:00:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-readme-motogp.txt, sha256: 2c47144a59fc5600ba6e41118eed8f890fc37db177dc6bf021370ee9220aab9c, retrieved_at: 2026-10-15T19:58:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-client.txt, sha256: bf904c98fb20054b1e0eebadf42b1e2eb1916c04e0c9d5ed524ff0e445b0ffbb, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-core.txt, sha256: 256daa11aed5e75e142c84795b89ed8ea83ddb7a0248785c94fb4d8355b2a182, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-more.txt, sha256: 31c4152d51a15164f974cfa17a21023e3bca1ec85f675cce4def1c6f68bb6775, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-pypi-sync-example.txt, sha256: 6a55935e20b751e5ce8130ff40792ae23f8f919afe0e6df1ca34c4d62b6c1e87, retrieved_at: 2026-10-15T20:00:00Z, method: command }

---

# FalkorDB Python client (falkordb package)

The Python client is `FalkorDB` on PyPI (import name `falkordb`), MIT-licensed per the README table and the PyPI classifiers. Version 1.8.0, uploaded 2026-10-14. It needs Python 3.10 or newer (`https://pypi.org/pypi/falkordb/json`: `requires_python` `>=3.10`).

Related: [Cypher support](/falkordb/cypher-support.md) (what to put in the query), [indexing and vectors](/falkordb/indexing-and-vectors.md), [data model](/falkordb/data-model-and-constraints.md) (what can be stored), [limits](/falkordb/limits-and-performance.md) (timeouts).

Run legend: **run** = executed against falkordb/falkordb:latest (module 4.22.1) with the falkordb 1.8.0 package, in a throwaway venv. **src** = read from the 1.8.0 source. **doc** = docs only.

## Install and dependencies

PyPI page (`https://pypi.org/pypi/falkordb/json`, long description, verbatim):

```sh
pip install FalkorDB
```

```sh
pip install "FalkorDB[hiredis]"
```

> "For faster parsing of large results (for example vector properties), install the optional `hiredis` parser. `redis` uses it automatically:" — evidence: `https://pypi.org/pypi/falkordb/json` [^pypi-falkordb]

Dependencies (src, `https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/pyproject.toml` in `https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz`):

```toml
dependencies = [
    "redis>=8.0.0,<9",
    "python-dateutil>=2.9.0,<3",
]
```

The package is a thin layer over `redis-py` 8.x. Commands go out as `GRAPH.QUERY` / `GRAPH.RO_QUERY` and replies are parsed in the client.

The sdist 1.8.0 package code (`falkordb/` directory) is byte-identical to the opensrc copy used for the source excerpts (`pypi-sdist-1.8.0-url-and-sha256.txt`, checked by `diff -rq`).

## Connect and select a graph (verbatim from PyPI page, run)

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host="localhost", port=6379)

# Select the social graph
g = db.select_graph("social")

# Create 100 nodes and return a handful
nodes = g.query(
    "UNWIND range(0, 100) AS i CREATE (n {v:1}) RETURN n LIMIT 10"
).result_set
for n in nodes:
    print(n)

# Read-only query the graph for the first 10 nodes
nodes = g.ro_query("MATCH (n) RETURN n LIMIT 10").result_set

# Copy the Graph
copy_graph = g.copy("social_copy")

# Delete the Graph
g.delete()
```

Run result (`run-4.22.1-pypi-sync-example.txt`): the `UNWIND ... LIMIT 10` returned ten rows, but the eager `CREATE` made 101 nodes (`MATCH (n) RETURN count(n)` gave `[[101]]`), as [Cypher support](/falkordb/cypher-support.md) describes for LIMIT.

The README's MotoGP example (`github-README-main.md`) ran as written, except the port was changed to 6391 for this server (run, `run-4.22.1-readme-motogp.txt`): it printed `Valentino Rossi` and `1`.

## FalkorDB class (src)

`FalkorDB(host="localhost", port=6379, password=None, socket_timeout=None, ..., connection_pool=None, ..., max_connections=None, ...)` — evidence: `https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz` (falkordb.py). Also:

- `FalkorDB.from_url(url, **kwargs)`
- `select_graph(graph_id) -> Graph`
- `list_graphs() -> List[str]` (run: returned all graph keys)
- `config_get(name)` / `config_set(name, value=None)` (run: `config_get("TIMEOUT_MAX")` returned `0`)
- `close()`, context manager support
- `udf_load`, `udf_list`, `udf_flush`, `udf_delete` (UDF library management; not tested here)

## Graph methods (src)

| Method | Behaviour (src) |
| --- | --- |
| `query(q, params=None, timeout=None)` | runs `GRAPH.QUERY` with `--compact` |
| `ro_query(q, params=None, timeout=None)` | runs `GRAPH.RO_QUERY` |
| `profile(query, params=None)` | returns an `ExecutionPlan` (runs the query) |
| `explain(query, params=None)` | returns an `ExecutionPlan` (no execution) |
| `call_procedure(procedure, read_only=True, args=None, emit=None)` | builds `CALL proc($param0, ...)` and `YIELD` from `emit` |
| `copy(clone)` / `delete()` | `GRAPH.COPY` / `GRAPH.DELETE` (run: `copy` returns a `Graph`) |
| `slowlog()` / `slowlog_reset()` | `GRAPH.SLOWLOG` |
| `list_indices()` | `CALL db.indexes()`-style result (`QueryResult`) |
| `create_node_range_index(label, *props)` | `CREATE INDEX FOR (e:Label) ON (e.a, e.b)` |
| `create_node_fulltext_index(label, *props)` | `CREATE FULLTEXT INDEX ...` |
| `create_node_vector_index(label, *props, dim=0, similarity_function="euclidean")` | `CREATE VECTOR INDEX ... OPTIONS {dimension:..., similarityFunction:'...'}` |
| `create_edge_range_index / create_edge_fulltext_index / create_edge_vector_index(relation, *props, ...)` | same, for `()-[e:Rel]->()` |
| `drop_node_range_index(label, attribute)` and siblings | `DROP ...` forms |
| `create_node_unique_constraint(label, *props)` / `create_node_mandatory_constraint(label, *props)` | `GRAPH.CONSTRAINT CREATE` |
| `create_edge_unique_constraint(relation, *props)` / `create_edge_mandatory_constraint(...)` | edge versions |
| `drop_*_constraint(...)`, `list_constraints()` | constraint management |

Source confirmation for the index helper (src, `https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz`): "`if entity_type == "NODE": pattern = f"(e:{label})"`" and for edges `()-[e:{label}]->()`. The helper builds `CREATE {idx_type} INDEX FOR {pattern} ON (e.a,e.b)`, so composite range indexes are created through the helper too.

Vector helper defaults (src, `https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz`): `dim` defaults to 0 and `similarity_function` to the string euclidean. Pass both explicitly. Run: `create_node_vector_index('Doc', 'emb', dim=3, similarity_function='cosine')` succeeded.

Call-procedure default (src): `read_only: bool = True`. Pass `read_only=False` for a write procedure.

## Parameters: how they are sent (src, important)

Parameters are not sent as separate Redis arguments. The client renders them into a `CYPHER` header that is prepended to the query text. From `graph.py` (`_build_params_header`, verbatim lines from `https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz`):

```python
params_header = "CYPHER "
for key, value in params.items():
    ...
    params_header += f"`{key_str}`={stringify_param_value(value)} "
```

Consequences:

- Each parameter value is serialized into the query string, so large vectors and lists travel as text. This is why the docs recommend `hiredis` for large vector results.
- Parameter names cannot contain a backtick, and an empty name is rejected (src: `ValueError`).
- Whether the plan cache keys on the rendered text (values included) was not verified. Open question. If it does, parameterised queries still avoid re-planning only when the text is identical.

Value rendering (src, `helpers.py` docstring in `https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz`): "you may pass any value that would be accepted by json.dumps()". The same docstring says strings are quoted, `None` becomes `null`, and dictionary keys are wrapped in backticks. Run results (`run-4.22.1-verify-client.txt`): a string containing a double quote came back unchanged, and a dictionary key containing a dash was accepted and returned as `{'a-b': 1}`.

Runs of the parameter path:

```python
g.query("UNWIND $rows AS r MERGE (n:Doc {id: r.id}) SET n.emb = vecf32(r.emb) RETURN count(n)", {"rows": rows})
g.query("MATCH (n:Doc {id:$id}) RETURN n.id", {"id": 3})
g.query("CALL db.idx.vector.queryNodes('Doc', 'emb', 1, vecf32($q)) YIELD node, score RETURN node.t, score", {"q": [0.9, 0.1, 0.0]})
```

All three ran (run). A 5-row `UNWIND` batch returned `[[5]]`.

The raw redis form of the same idea is in [Cypher support](/falkordb/cypher-support.md): `CYPHER name_param = "..." MATCH ... $name_param`.

## Result object (QueryResult, src and run)

Source (`query_result.py`, `QueryResult.__init__`): the response's last element is the statistics, and the result set is parsed from the rest. Attributes and methods (src):

- `header`: list of `[type_code, column_name]` pairs (run: `[[1, 'a'], [1, 'b'], [1, 'one']]` for `RETURN a, b, 1 AS one`).
- `result_set`: list of rows; each cell is a Python value, `Node`, `Edge`, `Path`, `datetime`, `date`, `time`, `relativedelta` for durations, or a point dict.
- Statistics properties: `labels_added`, `labels_removed`, `nodes_created`, `nodes_deleted`, `properties_set`, `properties_removed`, `relationships_created`, `relationships_deleted`, `indices_created`, `indices_deleted`, `cached_execution`, `run_time_ms`.

Run (`run-4.22.1-client-api.txt`): `CREATE (:A {x:1})-[:R {w:2.5}]->(:B {y:'z'}) RETURN 1` gave `nodes_created 2.0`, `relationships_created 1.0`, `properties_set 3.0`, `labels_added 2.0`. The counters came back as floats. `cached_execution` was `False` on the first run and `run_time_ms` was positive.

Entities (run): `Node` has `.id`, `.labels`, `.properties`. `Edge` has `.relation`, `.properties`, `.src_node`, `.dest_node`. Example: `Edge R {'w': 2.5} 0 1`.

Errors: server errors surface as `redis.exceptions.ResponseError` with the server message, for example `Query timed out` or `graph.RO_QUERY is to be executed only on read-only queries`. Client-side argument errors use plain `Exception` (`Timeout argument must be a positive integer`). Schema version mismatches raise `SchemaVersionMismatchException` after the client refreshes its schema.

## Read-only queries

`ro_query` runs `GRAPH.RO_QUERY`. A write inside it fails:

```python
g.ro_query("CREATE (:X)")
# ResponseError: graph.RO_QUERY is to be executed only on read-only queries
```

Run. Use `ro_query` for read replicas if you have them; see [limits](/falkordb/limits-and-performance.md).

## Async client (run)

```python
import asyncio
from falkordb.asyncio import FalkorDB
from redis.asyncio import BlockingConnectionPool

async def main():
    pool = BlockingConnectionPool(max_connections=16, timeout=None, decode_responses=True)
    db = FalkorDB(connection_pool=pool)
    g = db.select_graph("social")
    result = await g.query("UNWIND range(0, 100) AS i CREATE (n {v:1}) RETURN n LIMIT 10")
    for n in result.result_set:
        print(n)
    await pool.aclose()

asyncio.run(main())
```

The PyPI page shows this shape (`https://pypi.org/pypi/falkordb/json`; the snippet below drops the connection-pool host arguments that the local run needed). A shortened version ran against the local server: `await ag.query(...)` and `await ag.ro_query(...)` both worked (`run-4.22.1-verify-more.txt`, `async create -> [[11]]`). Pass `host` and `port` on the pool (`BlockingConnectionPool(host=..., port=...)`) when not using localhost.

## Profile and explain (run)

```python
print(g.explain("MATCH (a:A) RETURN a"))
# Results
#     Project
#         Node By Label Scan | (a:A)
```

`ExecutionPlan` prints the operation tree (run; see the client-API run log). `profile` adds per-operation counts and timings, as in the docs (`https://docs.falkordb.com/commands/graph.profile`): "returning the operation tree structure alongside the number of records produced and total runtime of each operation" (`https://docs.falkordb.com/commands/graph.profile`). `GRAPH.PROFILE` executes the query; `GRAPH.EXPLAIN` does not.

Index use check (run): an equality or range predicate on an indexed property shows `Node By Index Scan` (4.22.1). The docs show `Index Scan`. Look for `Index Scan` in the text.

## Doc example bugs

The Python vector example in the docs builds its CREATE with an f-string that does not close its braces:

```python
graph.query(f"CREATE (p:Product {name: 'Laptop', embedding: vecf32({embedding.tolist()})})")
```

The docs' Python vector example (`https://docs.falkordb.com/cypher/indexing/vector-index`, "Realistic Vector Search") builds its CREATE with an f-string whose braces are not escaped. Evaluating that line raises `NameError: name 'name' is not defined` (run). Escape the braces, or better, pass the vector as a parameter:

```python
g.query("CREATE (p:Product {name:'Laptop', embedding: vecf32($e)})", {"e": embedding.tolist()})
```

Test it before use.

## Open questions

- Plan cache keying with rendered parameter values (see above).
- Client behaviour against the official 6.0.2 server (not tested).
- `hiredis` speed-up size for vector results (docs say "faster", no numbers).
- `redis` 8.x pin: the client refuses `redis` 9 (`<9`). Check when upgrading.

[^pypi-falkordb]: FalkorDB 1.8.0 on PyPI (long description and metadata) - https://pypi.org/pypi/falkordb/json (last_modified 2026-10-14T11:54:31Z)
