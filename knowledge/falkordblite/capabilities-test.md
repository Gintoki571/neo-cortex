---
type: Test Result
title: FalkorDBLite capabilities test
description: Run results for vector index, KNN, full-text, procedure list, weighted shortest paths, persistence across restarts, concurrency and connection paths, on falkordblite 0.10.0 with the bundled FalkorDB 4.18.3 module. Vector search works.
resource: https://pypi.org/project/falkordblite/0.10.0/
tags: [falkordblite, falkordb, vector-index, knn, fulltext, persistence, graphrag, test]
status: current
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/falkordblite-agent, at: 2026-10-15T19:35:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:35:00Z }
sources:
  - id: local-run
    resource: references/evidence/falkordblite/capabilities-run-all-output.txt
    title: Full capability run output (install in throwaway venv, two processes)
  - id: local-run-api
    resource: references/evidence/falkordblite/api-connection-probe-output.txt
    title: Connection, threading and async probe output
  - id: local-run-misc
    resource: references/evidence/falkordblite/constraints-command-probe-output.txt
    title: Constraint syntax probe output
  - id: pypi
    resource: https://pypi.org/pypi/falkordblite/json
    title: PyPI JSON for falkordblite
    last_modified: 2026-05-02T13:12:29Z
  - id: versions-cfg
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/versions.cfg
    title: versions.cfg (master)
  - id: gh-pr-94
    resource: https://api.github.com/repos/FalkorDB/falkordblite/issues?state=all
    title: "Closed PR 94 \"feat(ci): update FalkorDB server to v4.18.3\""
  - id: close-probe
    resource: references/evidence/falkordblite/close-shutdown-probe-output.txt
    title: close() shutdown probe output
  - id: procedures
    resource: references/evidence/falkordblite/dbms-procedures-full.json
    title: dbms.procedures() full rows
  - id: runtime-versions
    resource: references/evidence/falkordblite/runtime-versions.txt
    title: Runtime versions (redis-server, Python, redislite)
  - id: sp-probe
    resource: references/evidence/falkordblite/sp-probe-output.txt
    title: Shortest-path probe output
  - id: timing
    resource: references/evidence/falkordblite/timing-probe-output.txt
    title: Open/query/close timing probe output

evidence:
  - { file: references/evidence/falkordblite/capabilities-run-all-output.txt, sha256: 37a128b6a40f386e0e4ef0739df1b32179e45be029cb102036b0ccc987471cc5, retrieved_at: 2026-10-15T19:27:36Z, method: command }
  - { file: references/evidence/falkordblite/capabilities-write-phase.json, sha256: 605832744292574cc365130f6c59a64586ffe285d3768ce6b3370997b4f39592, retrieved_at: 2026-10-15T19:27:36Z, method: command }
  - { file: references/evidence/falkordblite/capabilities-reopen-phase.json, sha256: 37c72d39903e132d6550b48d53eb81bbe49519d2be1de47730804fe06a2eeb5d, retrieved_at: 2026-10-15T19:27:36Z, method: command }
  - { file: references/evidence/falkordblite/dbms-procedures-full.json, sha256: b5a7dba571d3f49c361266efcb3b76c1f1f0bee9c01b54424e546666f9f86402, retrieved_at: 2026-10-15T19:27:36Z, method: command }
  - { file: references/evidence/falkordblite/capabilities-probe.py, sha256: 29b679deff58fcc861ff77d24298d32efe1461357e78cf11208e026ec26a0ac6, retrieved_at: 2026-10-15T19:27:00Z, method: command }
  - { file: references/evidence/falkordblite/capabilities-run-all.sh, sha256: 0e9e7820108d9abcffec424393af767b1e0d3081bbb6a81be3bc34093c047a08, retrieved_at: 2026-10-15T19:27:00Z, method: command }
  - { file: references/evidence/falkordblite/sp-probe-output.txt, sha256: 5ac6313aa3df47cd6e13f7cf552b95ee95c92bc93245b984c3351eb7187fce33, retrieved_at: 2026-10-15T19:27:36Z, method: command }
  - { file: references/evidence/falkordblite/sspaths-rowcount-output.txt, sha256: c00dd109fba0bcc4e0422514f0afc0b5a3936baa6f6dfa40a56384fbcc979694, retrieved_at: 2026-10-15T19:27:50Z, method: command }
  - { file: references/evidence/falkordblite/api-connection-probe-output.txt, sha256: 4d4750d52c4d377e06f183e8a85cc34477c156b843d9221dbecf429ff650d385, retrieved_at: 2026-10-15T19:27:50Z, method: command }
  - { file: references/evidence/falkordblite/close-shutdown-probe-output.txt, sha256: 9d5d951be26f6d503102b34abcaa51b8f87514f33961b82564b2be134968c51a, retrieved_at: 2026-10-15T19:27:50Z, method: command }
  - { file: references/evidence/falkordblite/orphan-server-driver-output.txt, sha256: fa57433a89da6689f4e254ff16acd8b2a04bb1e3f10a3c167b02f17f20f48cde, retrieved_at: 2026-10-15T19:30:23Z, method: command }
  - { file: references/evidence/falkordblite/constraints-command-probe-output.txt, sha256: 790b1b026574c7c00f164e52bf63af4ae9cd084505cc0ae911d4934df17ad9e5, retrieved_at: 2026-10-15T19:28:30Z, method: command }
  - { file: references/evidence/falkordblite/external-client-probe-output.txt, sha256: 23cf323c60abbe891e7108360bdcc90210e51b496d10c5f6c231217eef834130, retrieved_at: 2026-10-15T19:28:30Z, method: command }
  - { file: references/evidence/falkordblite/tcp-probe-output.txt, sha256: d1268bc5da784771425b5df1bd51f0c28f3daad8c71fc7ce931308a75233f863, retrieved_at: 2026-10-15T19:31:03Z, method: command }
  - { file: references/evidence/falkordblite/timing-probe-output.txt, sha256: 4df99ef91f74a1971167cfeae4238b8ea6bd520f4a1fb76bb3b04eb72e3ac0e3, retrieved_at: 2026-10-15T19:31:03Z, method: command }
  - { file: references/evidence/falkordblite/runtime-versions.txt, sha256: 7a52c8abf8ef5b91f53e58e2506225ccd5a33a5ef99be2cb37666edf33ce347b, retrieved_at: 2026-10-15T19:27:36Z, method: command }
---

# Answer: vector support

**Yes, the bundled build supports vector indexes and nearest-neighbour search.** The steps that matter for GraphRAG all passed in a real run (`vecf32` storage, `CREATE VECTOR INDEX`, `db.idx.vector.queryNodes`, and persistence across a process restart). The bundled module is FalkorDB `4.18.3`, which matches the repo's `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/versions.cfg` and the closed PR `feat(ci): update FalkorDB server to v4.18.3` (#94):

> `FALKORDB_VERSION=v4.18.3`

[^versions-cfg] [^gh-pr-94]

The module as loaded by the test reports `'ver': 41803`:

> `{'name': 'graph', 'ver': 41803, 'path': '.../redislite/bin/falkordb.so', 'args': []}`

[^local-run]

Fulltext index also works. Weighted shortest paths work for `algo.SPpaths` with `weightProp`, but not for the `weight` output column.

# Environment

- Host: Linux x86_64, kernel `7.2.9-arch1-1`, glibc `2.44`. [^local-run]
- Python `3.14.7` in a throwaway venv under the job temp dir. Probes run with `python -I`, scripts kept outside the venv. [^runtime-versions]
- Packages: `falkordblite 0.10.0`, `falkordb 1.8.0`, `redis 8.1.0`, `psutil 7.2.2`. [^local-run]
- Embedded: `redis-server v=8.6.2`, FalkorDB module `v4.18.3` (encoded `41803`). [^runtime-versions] [^local-run]

Reproduce (scripts and outputs in the evidence folder):

```sh
python3 -m venv venv && venv/bin/pip install falkordblite
venv/bin/python -I capabilities-probe.py <db.rdb> write out.json   # process 1
venv/bin/python -I capabilities-probe.py <db.rdb> reopen out2.json # process 2, new interpreter
```

Full sequence: `capabilities-run-all.sh`. [^local-run]

# Results

Status is from the run. `PASS` means the call returned without error and the expected value was seen. `FAIL` means the call raised an error, quoted from the output.

| Step | Capability | Result | Evidence (verbatim) |
|---|---|---|---|
| a | Create graph with 4 `:Doc` nodes that each have a `vecf32` property | PASS | `[PASS] a2_count_nodes: [[4]]` |
| b | Read `vecf32` back | PASS | `[PASS] b_vecf32_readback: [[[1.0, 0.0, 0.0, 0.0]]]` |
| c | `CREATE VECTOR INDEX FOR (d:Doc) ON (d.emb) OPTIONS {dimension: 4, similarityFunction: 'cosine'}` | PASS | index listing shows `'dimension': 4, 'similarityFunction': 'cosine', 'M': 16, 'efConstruction': 200, 'efRuntime': 10` |
| d | `CALL db.idx.vector.queryNodes('Doc','emb',2, vecf32([1,0,0,0]))` | PASS | `[PASS] d_knn_vector_query: [[1, 'graph databases intro', 0.0], [2, 'vector search basics', 0.00611627101898193]]` |
| d2 | Same with parameters `$k` and `$q` (k=3, query [0,1,0,0]) | PASS | `[PASS] d2_knn_with_params: [[4, 0.0], [2, 0.889568448066711], [1, 1.0]]` |
| e | `CALL db.idx.fulltext.createNodeIndex('Doc','title')` | PASS | `[PASS] e_create_fulltext_index: []` |
| e2 | `CALL db.idx.fulltext.queryNodes('Doc','search')` | PASS | `[PASS] e2_fulltext_query: [[2, 'vector search basics', 1.0], [4, 'fulltext search with lucene', 1.0]]` |
| f | `CALL dbms.procedures()` | PASS, 22 rows | full list in [procedures list](#procedures-and-functions) |
| f2 | `CALL db.procedures()` | FAIL | `ResponseError: Procedure \`db.procedures\` is not registered` |
| f3 | `CALL dbms.functions()` | PASS, 144 rows | includes `vecf32`, `vec.cosineDistance`, `vec.euclideanDistance` |
| g1 | `algo.SPpaths({sourceNode, targetNode, relTypes, weightProp:'w'})` | PASS | `[PASS] g1_algo_SPpaths_weighted: [[['A', 'B', 'C'], 2]]` (two-hop route A-B-C; with weights 1+1 it beats the direct A-C edge of weight 5. The weight value itself is not printed by the call) |
| g1b | Same without `weightProp` | PASS | `[PASS] SPpaths_no_weight_hops: [[['A', 'C'], 1]]` |
| g1c | Unknown key `notAKey` in the config map | PASS (silently accepted) | `[PASS] SPpaths_bogus_key: [[1]]` |
| g2 | `algo.SSpaths({sourceNode, relTypes, weightProp:'w'})` | PASS, but one row | `[PASS] g2_algo_SSpaths_weighted: [[['A', 'B']]]` |
| g2b | Tree A to B, A to C, B to D with `SSpaths` (see [sspaths](#sspaths-row-count)) | Returned one row only | `[[['A', 'C']]]` (unweighted and weighted) |
| g4 | `YIELD path, weight` on `SPpaths` or `SSpaths` | FAIL | `ResponseError: Procedure \`algo.SPpaths\` does not yield output \`weight\`` |
| h | Reopen after process exit: list graphs, count, KNN, fulltext, SPpaths | PASS, all | see [persistence](#persistence) |
| m1 | `db.list_graphs()` | PASS | `['roads', 'vecgraph']` |
| m2 | `MODULE LIST` | PASS | graph module `ver 41803`, plus `vectorset` `ver 1` (no path) |
| m3 | `GRAPH.CONFIG GET VERSION` | FAIL | `ResponseError: Unknown configuration field` |
| m4 | `g.ro_query` with a read | PASS | `[PASS] m_ro_query: [[4]]` |
| x1 | `CREATE CONSTRAINT ON (x:Persona) ASSERT x.name IS UNIQUE` (Cypher) | FAIL | `Invalid constraint command use the GRAPH.CONSTRAINT command instead` |
| x2 | `CREATE CONSTRAINT FOR (x:Persona) REQUIRE x.name IS UNIQUE` (Cypher) | FAIL | `Invalid input 'F': expected '=' or CREATE CONSTRAINT ON` |
| x3 | `CREATE INDEX FOR (x:Persona) ON (x.name)` then `GRAPH.CONSTRAINT CREATE ... UNIQUE` | PASS | `[PASS] GRAPH.CONSTRAINT CREATE UNIQUE -> PENDING`; duplicate insert then `unique constraint violation on node of type Persona` |

Notes on the table:

- The index metadata and KNN score are cosine distance. Identical vectors score `0.0`. This is read from the output, not from documentation.
- The fulltext query matched two nodes. Both scored `1.0`. No stemming or ranking behaviour was tested.
- The `g2b` case was added because `SSpaths` returned only one row in the first probe. It was not explained by the docs or by the output.

## Procedures and functions

`CALL dbms.procedures()` returned 22 procedures, saved in `dbms-procedures-full.json`:

- Algorithms: `algo.betweenness`, `algo.BFS`, `algo.labelPropagation`, `algo.MSF`, `algo.pageRank`, `algo.SPpaths`, `algo.SSpaths`, `algo.WCC`.
- Constraints and indexes: `db.constraints`, `db.indexes`, `db.idx.fulltext.createNodeIndex`, `db.idx.fulltext.drop`, `db.idx.fulltext.queryNodes`, `db.idx.fulltext.queryRelationships`, `db.idx.vector.queryNodes`, `db.idx.vector.queryRelationships`.
- Schema and stats: `db.labels`, `db.meta.stats`, `db.propertyKeys`, `db.relationshipTypes`.
- Meta: `dbms.functions`, `dbms.procedures`.

Excerpt from `dbms-procedures-full.json`: `['db.idx.vector.queryNodes', 'READ']` and `['db.idx.fulltext.createNodeIndex', 'WRITE']`.

`dbms.functions()` returned 144 rows. Vector functions present: `vecf32`, `vec.cosineDistance`, `vec.euclideanDistance`. Tested `vec.euclideanDistance(vecf32([1,0]), vecf32([0,1]))` = `1.41421353816986`. [^sp-probe]

## SSpaths row count

`sspaths-rowcount-probe.py` (evidence folder) ran on a tree `A->B`, `A->C`, `B->D` with `relTypes: ['E']`:

- Unweighted `SSpaths` returned: `[[['A', 'C']]]`. Two rows were expected for paths to B and C.
- Weighted `SSpaths` returned the same single row.
- `SPpaths` from A to D returned `[[['A', 'B', 'D']]]`, which is correct.

Conclusion: `algo.SSpaths` in this build returned one path in each test. The cause is unknown. Do not rely on `SSpaths` for all-targets output until it is checked against upstream.

## Persistence

Process 1 wrote the data, called `SAVE`, and exited. The server process was gone after exit (`ps` showed none). Process 2 is a new interpreter on the same file:

- `[PASS] h_reopen_list_graphs: ['roads', 'vecgraph']`
- `[PASS] h_reopen_count: [[4]]`
- `[PASS] h_reopen_knn: [[1, 0.0], [2, 0.00611627101898193]]`
- `[PASS] h_reopen_fulltext: [[2, 1.0], [4, 1.0]]`
- `[PASS] h_reopen_SPpaths_names_hops: [[['A', 'B', 'C'], 2]]`

[^local-run]

The data directory after process 1 contained only `falkor.rdb` (2250 bytes) plus test files. The RDB file is the persistence unit. Vector and fulltext index definitions also came back after restart, because the KNN and fulltext queries returned results.

## Concurrency and connection paths

| Test | Result | Evidence |
|---|---|---|
| 20 threads each run `CREATE` on one `Graph` handle | PASS, 20 nodes written, no errors | `[PASS] threads_20_writes_same_handle: count=20 errors=[]` |
| `AsyncFalkorDB`: parameterized create, read, vector index and KNN | PASS | `[PASS] async_query_params: [['Alice', 30]]`, `[PASS] async_vector_knn: [[0.0]]` |
| Second process opens the same DB file while the first is alive | PASS, attaches to the running server and reads `1` | `second_process_socket_same_as_first` |
| redis-py over unix socket: `GRAPH.QUERY` | PASS | `[PASS] redis-py_over_unix_socket_GRAPH.QUERY: ...` |
| Pure falkordb-py in another process over the unix socket (count, KNN) | PASS | `[PASS] count: [[2]]`, `[PASS] knn: [[1, 0.0]]` |
| TCP: `FalkorDB(path, serverconfig={"port": "6399"})` then pure falkordb-py `host/port` | PASS | `[PASS] pure falkordb-py over TCP count: [[1]]` |

Concurrency across processes beyond attach-and-read was not tested. Writes from two processes were not tested.

## Lifecycle and timing

- `db.close()` on a single-client handle stopped the server. Observed: `after open: 2`, then `after close(): 1`, where the remaining one was from an earlier test. [^close-probe]
- Open, query and close timing from one run: `import=0.121s open_server=0.134s query=0.0030s close=3.245s`, wall clock `3.571s`. The close step is most of the time. This matches open GitHub issue `#113 Process shutdown takes ~4s while the actual work takes ~0.2s`. [^timing]
- An extra raw client left connected at process exit leaves the server running. See [limitations-and-open-issues](/falkordblite/limitations-and-open-issues.md#orphaned-server-processes).

## Scorecard

| Capability asked about | Verdict |
|---|---|
| Vector index (`CREATE VECTOR INDEX`) | PASS |
| `vecf32` storage | PASS |
| KNN (`db.idx.vector.queryNodes`), with and without params | PASS |
| Fulltext index and query | PASS (basic) |
| Procedure list | PASS (`dbms.procedures`), FAIL (`db.procedures`) |
| Weighted shortest path, `algo.SPpaths` with `weightProp` | PASS (path and hops) |
| `algo.SSpaths` weighted | PASS (runs), returns one path only |
| `weight` yield on SP/SS paths | FAIL, no such output column |
| Persistence across restart (graph, vector, fulltext, SP) | PASS |
| Thread-safety on one handle (20 writes) | PASS |
| Async client with vector | PASS |
| Redis-compatible socket for other clients | PASS (unix socket and TCP) |
| Cypher `CREATE CONSTRAINT` | FAIL (use `GRAPH.CONSTRAINT`) |

# Procedures and functions

The full list is in `dbms-procedures-full.json`. [^procedures]

# Open questions

- `SSpaths` returns one row. Is this a bug in FalkorDB 4.18.3, or does the procedure need a target or other argument this test did not pass?
- The config map silently accepts unknown keys (`notAKey` passed). Is that intended?
- Vector index behaviour with a dimension mismatch, and with deletes or updates, was not tested.
- Whether the bundled module matches upstream FalkorDB 4.18.3 byte for byte was not checked.
- `g.delete()` and the vector index with `efRuntime` tuning were not tested.

[^versions-cfg]: `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/versions.cfg` at master, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/versions.cfg`.
[^local-run]: `references/evidence/falkordblite/capabilities-run-all-output.txt`, `capabilities-write-phase.json`, `capabilities-reopen-phase.json`, `api-connection-probe-output.txt`, `external-client-probe-output.txt`, `constraints-command-probe-output.txt`.
[^runtime-versions]: `references/evidence/falkordblite/runtime-versions.txt`.
[^sp-probe]: `references/evidence/falkordblite/sp-probe-output.txt` (script `capabilities-shortest-path-probe.py`).
[^procedures]: `references/evidence/falkordblite/dbms-procedures-full.json`.
[^close-probe]: `references/evidence/falkordblite/close-shutdown-probe-output.txt` (script `close-shutdown-probe.py`).
[^timing]: `references/evidence/falkordblite/timing-probe-output.txt` (script `timing-probe.py`).
[^gh-pr-94]: Closed PR `#94` titled `feat(ci): update FalkorDB server to v4.18.3`, in the GitHub issues and PR list (state=all), evidence `https://api.github.com/repos/FalkorDB/falkordblite/issues?state=open`.
