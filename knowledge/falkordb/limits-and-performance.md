---
type: Concept
title: FalkorDB limits, timeouts, memory and performance claims
description: Configuration defaults and hard limits (timeouts, result size, query memory, cache, queue, bulk-string size), vendor performance claims flagged as such, and what a local 4.22.1 run measured.
resource: https://docs.falkordb.com/getting-started/configuration
tags: [falkordb, limits, performance, timeouts, memory, benchmarks, configuration]
status: stable
generated: { by: claude-haiku-5-5/falkordb-agent, at: 2026-10-15T19:45:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:45:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: docs-configuration
    resource: https://docs.falkordb.com/getting-started/configuration
    title: FalkorDB Server Configuration Parameters Reference
    last_modified: 2026-10-15T10:03:32.512Z
  - id: docs-design-index
    resource: https://docs.falkordb.com/design/index
    title: FalkorDB Architecture and Design Principles
  - id: docs-bulk-spec
    resource: https://docs.falkordb.com/design/bulk-spec
    title: GRAPH.BULK Endpoint Specification
  - id: docs-concurrency
    resource: https://docs.falkordb.com/design/concurrency
    title: Atomicity and Concurrency Control in FalkorDB
  - id: docs-graph-query
    resource: https://docs.falkordb.com/commands/graph.query
    title: GRAPH.QUERY
  - id: docs-slowlog
    resource: https://docs.falkordb.com/commands/graph.slowlog
    title: GRAPH.SLOWLOG
  - id: docs-graph-memory
    resource: https://docs.falkordb.com/commands/graph.memory
    title: GRAPH.MEMORY
  - id: github-readme-main
    resource: https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/README.md
    title: FalkorDB README (main branch)
evidence:
  - { name: docs-getting-started__configuration.txt, url: "https://docs.falkordb.com/getting-started/configuration", sha256: ceb6445ce935fb619711cc650fcaf7c38a8a0c43c36c96824894c4de9c0d9748, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-design__index.txt, url: "https://docs.falkordb.com/design/index", sha256: 2dd463c8cab32eb0ebee9e445ebc4da8f9b279d704cdb254e8f1dc4680b7900b, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-design__bulk-spec.txt, url: "https://docs.falkordb.com/design/bulk-spec", sha256: a23d3c3d15d67267b1f572b23c36e5896998ee67bec2d97f29357fadb7b60109, retrieved_at: 2026-10-15T19:45:00Z, method: curl, redistributed: false }
  - { name: docs-design__concurrency.txt, url: "https://docs.falkordb.com/design/concurrency", sha256: 9f65bd88db8dbc326749c07cd2b7c4543608cf8b7fae1b320f4610bc2e26f3cd, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-commands__graph.query.txt, url: "https://docs.falkordb.com/commands/graph.query", sha256: 65049ee8288ec987d4b7de6922e3d0b3c2f55772ec52dde7fc1240eea2e3dfd3, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-commands__graph.slowlog.txt, url: "https://docs.falkordb.com/commands/graph.slowlog", sha256: 9813a76da98e264a32f511c1ac708971073775921a49a0d7ee5ea8e7e80088a2, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-commands__graph.memory.txt, url: "https://docs.falkordb.com/commands/graph.memory", sha256: b9cf4d2d0523e5d5904399b4a1a0fd798b87dfe2457b7d294c494ce1ab6640b2, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: github-README-main.md.txt, url: "https://raw.githubusercontent.com/FalkorDB/FalkorDB/main/README.md", url_basis: inferred, sha256: 992fe2e53f68b0ad76b09cf3b3ae353838e9002292d6d8c869388cd2328ff3d9, retrieved_at: 2026-10-15T19:37:00Z, method: curl, redistributed: false }
  - { file: references/evidence/falkordb/run-4.22.1-perf-1M-nodes.txt, sha256: 19ed3712d4afb082fde445b1572fc1d64d890edf725ffa5853cadc08602d06a0, retrieved_at: 2026-10-15T19:55:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-client.txt, sha256: bf904c98fb20054b1e0eebadf42b1e2eb1916c04e0c9d5ed524ff0e445b0ffbb, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-atomicity.txt, sha256: e09b4af8d9add0ecb2b63dc20e576cd4dc2e1f7b817f0343aef962b8da845740, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/script-perf_nodes.py.txt, sha256: e3768912d26271ea75ef9b3e333f4cfb6476584ade3881101dc2734929f9af80, retrieved_at: 2026-10-15T19:55:00Z, method: command }
---

# FalkorDB limits, timeouts, memory and performance

Limits fall into three groups: hard limits and defaults in the server config, limits the docs state about data (types, sizes), and performance claims. The performance claims are vendor claims. This concept marks them as such and gives the local run next to them.

Related: [Cypher support](/falkordb/cypher-support.md) (eager LIMIT, `<>` not indexed), [data model](/falkordb/data-model-and-constraints.md) (what can be stored), [Python client](/falkordb/python-client.md) (timeout argument).

## Server configuration (docs defaults)

Set at module load (`redis-server --loadmodule ... PARAM value`) or at run time with `GRAPH.CONFIG SET` where marked (`https://docs.falkordb.com/getting-started/configuration`, table "FalkorDB configuration parameters").

| Parameter | Default (quoted) | Run-time settable |
| --- | --- | --- |
| `THREAD_COUNT` | "`THREAD_COUNT` defaults to the system's hardware threads (logical cores)." | no |
| `CACHE_SIZE` | "`CACHE_SIZE` default value is 25." | no |
| `OMP_THREAD_COUNT` | "`OMP_THREAD_COUNT` is defined by GraphBLAS." | no |
| `NODE_CREATION_BUFFER` | "`NODE_CREATION_BUFFER` is 16,384." (minimum 128) | no |
| `RESULTSET_SIZE` | "`RESULTSET_SIZE` defaults to 10,000." | yes |
| `QUERY_MEM_CAPACITY` | "`QUERY_MEM_CAPACITY` is unlimited" | yes |
| `MAX_QUEUED_QUERIES` | "effectively unlimited (config value of `UINT64_MAX`)" | yes |
| `TIMEOUT_MAX` | "Since v2.10: `TIMEOUT_MAX` is off (set to `0`)." | yes |
| `TIMEOUT_DEFAULT` | "Since v2.10: `TIMEOUT_DEFAULT` is equal to `TIMEOUT_MAX` (set to `0`)." | yes |
| `VKEY_MAX_ENTITY_COUNT` | "`VKEY_MAX_ENTITY_COUNT` is 100,000." | yes |
| `ASYNC_DELETE` | "`ASYNC_DELETE` is `yes`." | yes |
| `MAX_INFO_QUERIES` | "`MAX_INFO_QUERIES` is 1000." | yes |

Notes:

- `CACHE_SIZE` is the number of cached query plans (LRU). Doc on GRAPH.QUERY: "The execution plans of queries, both regular and parameterized, are cached" (`https://docs.falkordb.com/commands/graph.query`). Use parameters so one plan serves many calls.
- `NODE_CREATION_BUFFER` trades memory for write speed: "Reducing this value will reduce memory consumption, but cause performance degradation due to the increased frequency of matrix resizes." (`https://docs.falkordb.com/getting-started/configuration`).
- `TIMEOUT` (single value) is deprecated since v2.10 in favour of `TIMEOUT_MAX` and `TIMEOUT_DEFAULT` (`https://docs.falkordb.com/getting-started/configuration`).
- `RESULTSET_SIZE` caps rows returned. Doc: "Result set size is a limit on the number of records that should be returned by any query." (`https://docs.falkordb.com/getting-started/configuration`). Run not performed. Note the cap applies to returned records, not to work done.
- `MAX_QUEUED_QUERIES` rejects with `Max pending queries exceeded` (doc quote: "Setting the maximum number of queued queries allows the server to reject incoming queries with the error message `Max pending queries exceeded`." `https://docs.falkordb.com/getting-started/configuration`).
- `QUERY_MEM_CAPACITY` kills a query over the cap: "return with the error message `Query's mem consumption exceeded capacity`" (`https://docs.falkordb.com/getting-started/configuration`). Set it on any multi-tenant or shared server.

## Timeouts (run)

Per-query timeout is the `timeout` argument (milliseconds) on `GRAPH.QUERY`, `GRAPH.RO_QUERY`, `GRAPH.PROFILE` (`https://docs.falkordb.com/getting-started/configuration`, Query Timeout). Quote: "When a query execution time exceeds the maximal execution time, the query is aborted and the query reply is `(error) Query timed out`." — evidence: `https://docs.falkordb.com/getting-started/configuration`. For writes: "For a write query - any change to the graph is undone (which may take additional time)." — evidence: `https://docs.falkordb.com/getting-started/configuration`.

Run (`run-4.22.1-verify-client.txt`): `g.query('UNWIND range(1,3000000) AS x RETURN count(x)', timeout=1)` raised `ResponseError Query timed out`. The Python client rejects non-integer timeouts with `Timeout argument must be a positive integer` (run).

## Query size and bulk limits

> "The main complicating factor in writing bulk importers is that Redis has a maximum string length of 512 megabytes and a default maximum query size of 1 gigabyte." — evidence: `https://docs.falkordb.com/design/bulk-spec` [^docs-bulk-spec]

Practical consequence: split large loads into batches. A batch of a few thousand rows per `UNWIND $rows` call should stay far below 1 GB (estimate, not measured). The run used a 1,000,000-row `UNWIND` with no parameter payload and it worked (below). The GRAPH.BULK endpoint (see [integration docs](/falkordb/docs-site-map.md)) is the documented route for huge loads; not tested here.

## Memory

Docs: "FalkorDB stores all data in RAM using memory-efficient custom data structures" (`https://docs.falkordb.com/design/index`). So the working set must fit in RAM.

Measure with `GRAPH.MEMORY USAGE` (`https://docs.falkordb.com/commands/graph.memory`): "GRAPH.MEMORY USAGE reports per-graph memory consumption in megabytes, broken down by nodes, edges, schemas, and indices, for monitoring and capacity planning." (`https://docs.falkordb.com/commands/graph.memory`) (`https://docs.falkordb.com/commands/graph.memory`). Not run.

Vector index memory formula (doc): see [indexing and vectors](/falkordb/indexing-and-vectors.md). It is an estimate.

## Concurrency and transactions

- Each query is atomic (run; see [Cypher support](/falkordb/cypher-support.md)): a failed query left no nodes and no new labels behind.
- Multi-query transactions are not native. Quote: "FalkorDB does not natively support multi-query transactions. For cases where multiple independent queries must all succeed or fail together, use Redis `MULTI`/`EXEC` blocks. Note that this serializes all enclosed commands across all graphs." — evidence: `https://docs.falkordb.com/design/concurrency` (FAQ)

## Slow queries and profiling

- `GRAPH.SLOWLOG`: "Only queries with a latency of 10 milliseconds or more are logged." (`https://docs.falkordb.com/commands/graph.slowlog`). Returns up to 10 entries.
- `GRAPH.PROFILE` and `GRAPH.EXPLAIN` details are in [python-client](/falkordb/python-client.md) and [Cypher support](/falkordb/cypher-support.md).

## Vendor performance claims (not independently proven)

These are marketing or design-page statements. Flag them as vendor claims when you reuse them.

> "FalkorDB is able to create over 1 million nodes under half a second and form 500K relations within 0.3 of a second." — evidence: `https://docs.falkordb.com/design/index` [^docs-design-index] (vendor claim)

> "Depending on the underlying hardware results may vary. However, inserting a new relationship is done in O(1)." — evidence: `https://docs.falkordb.com/design/index` (vendor claim)

> "It can create over 1 million nodes in under half a second." — evidence: `https://docs.falkordb.com/design/index` (FAQ; vendor claim)

The README links "📊 [Latest Performance Benchmarks](https://benchmark.falkordb.com/)" (`github-README-main.md`). That page was not fetched; it is the place to check the claim with their hardware.

Local measurement (run, `run-4.22.1-perf-1M-nodes.txt`), falkordb/falkordb:latest (module 4.22.1), 12 logical cores, 15 GB RAM, one client on the same host:

```cypher
UNWIND range(1, 1000000) AS x CREATE (:N {v: x})
```

Result: `nodes_created 1000000.0`, `server_run_time_ms 686.2`, client wall time `0.687 s`. For 100,000 nodes: `91.3 ms` server time (`run-4.22.1-perf-1M-nodes.txt`).

So the 1M-node claim ("over 1 million nodes under half a second", `https://docs.falkordb.com/design/index`) did not hold on this machine: 0.69 s. The hardware and Redis build differ from the vendor's, and the run is a single UNWIND. The relationship claim (500K relations in 0.3 s) was not measured: the first attempt (a cartesian `MATCH ... MATCH ... WHERE`) did not finish within the time budget.

Known cost signals from the docs (doc only):

- WCC: "O(|V| + |E|)" (`https://docs.falkordb.com/algorithms/wcc`).
- CDLP: "CDLP operates with a time complexity of **O(m + n)** per iteration" (`https://docs.falkordb.com/algorithms/cdlp`).
- Max flow: "O(V · E²)" (`https://docs.falkordb.com/algorithms/maxflow`). See [algorithms](/falkordb/algorithms-and-weighted-paths.md).
- The BFS doc warns: "large depths in highly connected graphs can result in exponential growth of traversed nodes" (`https://docs.falkordb.com/algorithms/bfs`).

## Limits that bite (confirmed by run)

- Eager operators ignore LIMIT: `UNWIND [1,2,3] AS value CREATE (a {property: value}) RETURN a LIMIT 1` created 3 nodes (run).
- Index not used for `<>` (docs; see Cypher support).
- Property values: no maps, no lists of maps, no `null` in lists (run).
- Read-only query endpoints reject writes: `GRAPH.RO_QUERY` / `ro_query` returned `graph.RO_QUERY is to be executed only on read-only queries` for a `CREATE` (run).
- Float32 points (run).

## Open questions

- Official 6.0.2 performance and timeout behaviour (not tested; see [overview](/falkordb/overview.md)).
- Whether `RESULTSET_SIZE` limits a query's work or only its output (docs say records returned).
- Relationship-creation throughput at 500K (not measured).
- Query size limit on the Rust (6.x) build. The 1 GB figure comes from the bulk-spec page; the 4.22.1 build was not tested with payloads near that size.

[^docs-bulk-spec]: GRAPH.BULK Endpoint Specification - https://docs.falkordb.com/design/bulk-spec
[^docs-design-index]: FalkorDB Architecture and Design Principles - https://docs.falkordb.com/design/index
