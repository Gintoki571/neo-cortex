---
type: Concept
title: FalkorDB Cypher support
description: Which Cypher clauses, operators, functions, procedures and parameter forms FalkorDB supports, the documented gaps, and what a 4.22.1 server actually did when tested.
resource: https://docs.falkordb.com/cypher/cypher-support
tags: [falkordb, cypher, query-language, merge, unwind, parameters]
status: stable
generated: { by: claude-haiku-5-5/falkordb-agent, at: 2026-10-15T19:45:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:45:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: docs-cypher-support
    resource: https://docs.falkordb.com/cypher/cypher-support
    title: OpenCypher Standard Compatibility and Feature Coverage
    last_modified: 2026-09-15T04:06:33.081Z
  - id: docs-known-limitations
    resource: https://docs.falkordb.com/cypher/known-limitations
    title: Cypher Query Limitations and Unsupported Features
    last_modified: 2026-09-15T03:15:01.536Z
  - id: docs-functions
    resource: https://docs.falkordb.com/cypher/functions
    title: Cypher Functions
  - id: docs-procedures
    resource: https://docs.falkordb.com/cypher/procedures
    title: Cypher Procedures
  - id: docs-merge
    resource: https://docs.falkordb.com/cypher/merge
    title: MERGE Clause
  - id: docs-unwind
    resource: https://docs.falkordb.com/cypher/unwind
    title: UNWIND Clause
  - id: docs-cheat-sheet
    resource: https://docs.falkordb.com/cypher/cheat-sheet
    title: Cypher Cheat Sheet
  - id: docs-getting-started-clients
    resource: https://docs.falkordb.com/getting-started/clients
    title: FalkorDB Client Libraries
evidence:
  - { file: references/evidence/falkordb/docs-cypher__cypher-support.txt, sha256: e5b65742168d132286b078676d619b914522b42db426a91e5566803f97710c03, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-cypher__known-limitations.txt, sha256: 5fe1f53e7a1ffa2312e1108e69d142dcfd51cff4ea7ee114e2705b25ee276ce3, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-cypher__functions.txt, sha256: a59272920050969fc515ef1e46d3083cfd3054c1363e138d996bab0b239252e3, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-cypher__procedures.txt, sha256: b87859e804610dc243820cd4b02d17d260bf2f7c899cb0c76bd96d9dee3ea8f8, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-cypher__merge.txt, sha256: 51eef3ac6f011de70c1a6da8d2929e4b5782ef1c07ed7d5bd7e4d6c8d09732db, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-cypher__unwind.txt, sha256: 0985a8e0e92cd7c84a94c638a4f07ec695c389cd86e89f198ddb77251150ed5d, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/run-4.22.1-verify-core.txt, sha256: 256daa11aed5e75e142c84795b89ed8ea83ddb7a0248785c94fb4d8355b2a182, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-client.txt, sha256: bf904c98fb20054b1e0eebadf42b1e2eb1916c04e0c9d5ed524ff0e445b0ffbb, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-more.txt, sha256: 31c4152d51a15164f974cfa17a21023e3bca1ec85f675cce4def1c6f68bb6775, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-redis-cli.txt, sha256: 4dd80f636385e39db5bd031d09b6ae5e61c9195157ccbfddd58bbc5ca4978e1e, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-atomicity.txt, sha256: e09b4af8d9add0ecb2b63dc20e576cd4dc2e1f7b817f0343aef962b8da845740, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-doc-snippets.txt, sha256: cc0852ee6c03b854201c782b71bb70e959b43d241327b1fe4beceaf1ac0d825e, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-edge-rs-verify-core.txt, sha256: 0dd029631f7bcddb2e3a0ae2971e005a5388238d8850f9d661d1fa702a375d17, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/script-verify_client.py.txt, sha256: fa49614107688de07c47f8259e204e71f81772ca9159ca09ef917ad76d0c3e96, retrieved_at: 2026-10-15T19:50:00Z, method: command }
---

# FalkorDB Cypher support

FalkorDB implements an openCypher subset. The docs say so in their own words:

> "FalkorDB implements a subset of the Cypher language, which is growing as development continues." — evidence: `docs-cypher__cypher-support.txt` [^docs-cypher-support]

> "FalkorDB is based on the **OpenCypher Query Language Reference version 9**, available at opencypher.org. It implements a growing subset of the specification with proprietary extensions." — evidence: `docs-cypher__cypher-support.txt` [^docs-cypher-support]

Related concepts: [indexing and vectors](/falkordb/indexing-and-vectors.md) (DDL, vector functions), [algorithms](/falkordb/algorithms-and-weighted-paths.md) (CALL algo.*), [data model](/falkordb/data-model-and-constraints.md) (types), [Python client](/falkordb/python-client.md) (parameters).

Status legend: **run** = reproduced on the falkordb/falkordb:latest image (module 4.22.1); **doc** = taken from docs only.

## Supported clauses (docs)

Label expressions are listed as unsupported under the OPTIONAL MATCH heading: "Label expressions" — evidence: `docs-cypher__cypher-support.txt` (reading clauses).

Clauses the support page lists as supported: MATCH, OPTIONAL MATCH, RETURN, AS, WITH, UNWIND, WHERE, ORDER BY, SKIP, LIMIT, CREATE, DELETE, SET, REMOVE, MERGE, CALL, UNION, UNION ALL (`docs-cypher__cypher-support.txt`). FOREACH and LOAD CSV have their own docs pages (`docs-cypher__foreach.txt`, `docs-cypher__load-csv.txt`) but are not on the support page; LOAD CSV needs a file under the import folder (run: `Error opening CSV URI: file://x.csv` without one).

> "  * We actually implement DETACH DELETE, the distinction being that relationships invalidated by node deletions are automatically deleted." — evidence: `docs-cypher__cypher-support.txt`

The docs imply that plain `DELETE` of a node also removes its relationships (doc; not tested here).

## Parameters (run)

Docs syntax (redis-cli form, shown in the docs):

Verbatim from the docs (`docs-cypher__cypher-support.txt`, Parameters section):

```cypher
CYPHER name_param = "Niccolò Machiavelli" birth_year_param = 1469 MATCH (p:Person {name: $name_param, birth_year: $birth_year_param}) RETURN p
```

Run on 4.22.1 (`run-4.22.1-redis-cli.txt`):

```cypher
CYPHER name_param = "Niccolò Machiavelli" birth_year_param = 1469 MATCH (p:Person {name: $name_param, birth_year: $birth_year_param}) RETURN p.name
```

Result: `p.name` = `Niccolò Machiavelli` (run).

From a client, parameters are passed as a map. The Python client turns them into a `CYPHER` header (see [python-client](/falkordb/python-client.md)). Run:

```python
g.query("UNWIND $rows AS r MERGE (n:Doc {id: r.id}) SET n.emb = vecf32(r.emb) RETURN count(n)", {"rows": rows})
```

Returned `[[5]]` for five rows (run, `run-4.22.1-verify-client.txt`).

## MERGE and UNWIND bulk-loading pattern

> "The `UNWIND` clause transforms a list into individual rows, creating one row for each element in the list." — evidence: `docs-cypher__unwind.txt` [^docs-unwind]

> "MERGE either matches existing nodes and binds them, or it creates new data and binds that." — evidence: `docs-cypher__merge.txt` [^docs-merge]

> "We should use multiple MERGE clauses to merge a relation and only create non-existent endpoints:" — evidence: `docs-cypher__merge.txt` [^docs-merge]

Recommended bulk shape (run, one round trip per batch):

```cypher
UNWIND $rows AS r
MERGE (n:Doc {id: r.id})
SET n.emb = vecf32(r.emb)
RETURN count(n)
```

Pass `rows` as a list of maps with `id` (int) and `emb` (list of float). Batch size is a choice for you: 1,000 to 10,000 per call is typical. Do not build the batch as a literal string.

Relationship pattern from the docs (doc only, not run):

```cypher
MERGE (charlie { name: 'Charlie Sheen' })
MERGE (wallStreet:Movie { name: 'Wall Street' })
MERGE (charlie)-[r:ACTED_IN]->(wallStreet)
```

Source: `docs-cypher__merge.txt`.

## Single-statement rule (run)

Each GRAPH.QUERY string holds one statement. Extra statements after a schema DDL fail:

```cypher
CREATE INDEX FOR (p:Person) ON (p.age) CREATE (:Person {age: 1})
```

Error (run, `run-4.22.1-verify-more.txt`): `Invalid input 'C': expected ';'`. Plain clause chains like `CREATE (:Q) CREATE (:Q)` ran fine (run).

Writes followed by reads need `WITH`:

```cypher
CREATE (:Z) MATCH (z:Z) RETURN z
```

Error (run): `A WITH clause is required to introduce MATCH after an updating clause.`

## Atomicity (run)

The docs claim each query is atomic: "Every query that modifies the graph — using any combination of `CREATE`, `SET`, `DELETE`, or `MERGE` — is **atomic**." — evidence: `docs-design__concurrency.txt`. Test on 4.22.1 (`run-4.22.1-atomicity.txt`):

```cypher
UNWIND [1,2,0] AS x CREATE (:Atom {v: x}) WITH x RETURN 1/x
```

Result: `Division by zero`, and afterwards `MATCH (a:Atom) RETURN count(a)` returned `0`. A label created by the failed query was also rolled back (`CALL db.labels()` showed only `Seed`).

## Known limitations (docs, several confirmed by run)

- Relationship uniqueness (run). Quote: "When a relation in a match pattern is not referenced elsewhere in the query, FalkorDB will only verify that at least one matching relation exists" — evidence: `docs-cypher__known-limitations.txt` [^docs-known-limitations]. (The MATCH lines below are from `script-verify_client.py.txt`, with comments added.)

  ```cypher
  CREATE (a)-[:e {val:'1'}]->(b), (a)-[:e {val:'2'}]->(b)
  MATCH (a)-[e]->(b) RETURN COUNT(e)      -- run: 2
  MATCH (a)-[e]->(b) RETURN COUNT(b)      -- run: 1
  ```

  Workaround from the docs: `MATCH (a)-[e]->(b) WHERE ID(e) >= 0 RETURN COUNT(b)` (doc only).

- LIMIT does not stop eager operators (run). Quote: "This limitation affects all eager operations: CREATE, SET, DELETE, MERGE, and projections with aggregate functions." — evidence: `docs-cypher__known-limitations.txt`

  ```cypher
  UNWIND [1,2,3] AS value CREATE (a {property: value}) RETURN a LIMIT 1
  ```

  Run: 3 nodes were created, although one row was returned.

- Index not used for `<>` filters. Quote: "The current index implementation, however, does not handle not-equal (`<>`) filters." — evidence: `docs-cypher__known-limitations.txt`

- Aggregates inside pattern comprehensions are rejected (doc only). The docs give the error `Invalid use of aggregating function 'count'` for `RETURN [(n)-[r:REL]->(m) WHERE n IS NOT NULL | count(n)] AS v`. Workaround: `WITH [(n)-[:REL]->(m:Paper) | m] AS connected RETURN size(connected) AS count`.

## Operators and functions

- Regex operator is unsupported (run). `RETURN 'abc' =~ 'a.*'` fails with `FalkorDB does not currently support =~`. Docs: "String operators (STARTS WITH, ENDS WITH, CONTAINS) are supported." and, under the same section, "Regex operator" listed as unsupported (`docs-cypher__cypher-support.txt`).
- The function `string.matchRegEx` exists and ran: `RETURN string.matchRegEx('abc', 'a.*')` returned a result (run). Use it when you need regex.
- Booleans, NULL and three-valued logic (run): `RETURN 1 = true` gives `false`; `RETURN null = null` gives `null`. Docs quote: "Unlike all other scalars, `null` cannot be stored as a property value." — evidence: `docs-datatypes.txt` (see [data model](/falkordb/data-model-and-constraints.md)).
- Hex literals: docs list "Hexadecimal and octal numerics" under unsupported (`docs-cypher__cypher-support.txt`). **Contradicted by run:** `RETURN 0x1F` returned `31` on 4.22.1 (`run-4.22.1-verify-client.txt`).
- Temporal functions run: `RETURN date('2025-09-15').year, localtime('15:45:20').hour` gave `[[2025, 15, 4.0]]` (run; the third value is `duration(...).hours`).
- `intern('...')` runs (docs, `docs-cypher__functions.txt`: "This function deduplicates the input string by storing a single internal copy across the database.").
- `point({latitude: ..., longitude: ...})` runs; the returned values were float32-rounded (`41.4000015258789`). See [data model](/falkordb/data-model-and-constraints.md).
- Vector functions: `vecf32([...])`, `vec.euclideanDistance(a, b)`, `vec.cosineDistance(a, b)` run (see [indexing and vectors](/falkordb/indexing-and-vectors.md)).
- `vecf64` is **not** a function on 4.22.1: `Unknown function 'vecf64'` (run). The FAQ on the functions page says "`vecf64()` for 64-bit float vectors" (doc, `docs-cypher__functions.txt`). Contradicted.
- User-defined functions: contradicted within the docs. The Cypher support page lists "User-defined functions" under unsupported, and its FAQ says "Yes. FalkorDB supports user-defined functions through the **Flex UDF library**" (`docs-cypher__cypher-support.txt`). Not tested here. Open question.
- Unsupported: temporal arithmetic functions (doc).

Functions table quote for vectors: "Returns the Cosine distance between the two input vectors" — evidence: `docs-cypher__functions.txt`.

## Procedures (CALL)

Procedure list and signatures are in [algorithms-and-weighted-paths](/falkordb/algorithms-and-weighted-paths.md) and [indexing-and-vectors](/falkordb/indexing-and-vectors.md). Syntax from the docs:

Verbatim from the docs (`docs-cypher__procedures.txt`): `GRAPH.QUERY social "CALL db.labels() YIELD label"` [^docs-procedures]

Run: `CALL db.labels() YIELD label RETURN label` and `CALL db.meta.stats()` both returned data (run).

These procedures ran on 4.22.1 but are missing from the docs procedure table: `algo.HarmonicCentrality`, `algo.maxFlow`, and `db.idx.cch.query` (the last is documented on the CCH page). Run.

Case: `algo.wcc` (lowercase) ran, the doc table uses `algo.WCC`. Procedure names are case-insensitive in practice (run).

## Search path and text search

- `CALL db.idx.fulltext.queryNodes('Movie', 'Jun*') YIELD node RETURN node.title` ran on 4.22.1 (run).

## Parse-error examples to avoid

- Single-quoted map keys in a CALL config fail: `CALL algo.betweenness({'nodeLabels': ['Person']})` -> `Invalid input '\''`. Use `{nodeLabels: [...]}` (run, `run-4.22.1-doc-snippets.txt`).
- Doc snippets with `<angle>` placeholders (for example `CALL algo.SPpaths({ sourceNode: <node> ...})`) are signatures, not runnable code.

## Open questions

- Whether `vecf64` and UDFs exist in the official 6.0.2 release (not tested; see [overview](/falkordb/overview.md)).
- Whether the hex-literal behaviour is intended (doc says unsupported; 4.22.1 accepts it).
- Full openCypher TCK pass rate. Not measured. The README links a TCK test (`TCK_DONE=tck_done.txt pytest tests/tck/test_tck.py`), but no result was checked.

[^docs-cypher-support]: OpenCypher Standard Compatibility and Feature Coverage - https://docs.falkordb.com/cypher/cypher-support (last_modified 2026-09-15T04:06:33.081Z)
[^docs-known-limitations]: Cypher Query Limitations and Unsupported Features - https://docs.falkordb.com/cypher/known-limitations (last_modified 2026-09-15T03:15:01.536Z)
[^docs-merge]: MERGE Clause - https://docs.falkordb.com/cypher/merge
[^docs-procedures]: Cypher Procedures - https://docs.falkordb.com/cypher/procedures
[^docs-unwind]: UNWIND Clause - https://docs.falkordb.com/cypher/unwind
