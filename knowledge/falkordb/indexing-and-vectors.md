---
type: Concept
title: FalkorDB indexing and vector search
description: Exact DDL and query procedures for range, full-text, vector (HNSW, cosine/euclidean) and CCH indexes, with the 4.22.1 run results and the doc claims that did not hold.
resource: https://docs.falkordb.com/cypher/indexing/vector-index
tags: [falkordb, vector-index, hnsw, fulltext, range-index, cch, graphrag, embeddings]
status: stable
generated: { by: claude-haiku-5-5/falkordb-agent, at: 2026-10-15T19:45:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:45:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: docs-indexing-index
    resource: https://docs.falkordb.com/cypher/indexing
    title: Indexing in FalkorDB
  - id: docs-vector-index
    resource: https://docs.falkordb.com/cypher/indexing/vector-index
    title: "Vector Indexing: Fast Similarity Search for GraphRAG"
    last_modified: 2026-09-30T11:44:18.508Z
  - id: docs-fulltext-index
    resource: https://docs.falkordb.com/cypher/indexing/fulltext-index
    title: Full-Text Indexing
  - id: docs-range-index
    resource: https://docs.falkordb.com/cypher/indexing/range-index
    title: Range Indexing
  - id: docs-cch-index
    resource: https://docs.falkordb.com/cypher/indexing/cch-index
    title: CCH Indexing
  - id: docs-functions
    resource: https://docs.falkordb.com/cypher/functions
    title: Cypher Functions (vector functions)
  - id: docs-procedures
    resource: https://docs.falkordb.com/cypher/procedures
    title: Cypher Procedures (vector and full-text procedure table)
  - id: docs-python-client-source
    resource: https://github.com/falkorDB/falkordb-py/blob/1.8.0/falkordb/graph.py
    title: falkordb-py 1.8.0 graph.py (create_node_vector_index)
evidence:
  - { name: docs-cypher__indexing__vector-index.txt, url: "https://docs.falkordb.com/cypher/indexing/vector-index", sha256: 8813129c1fe2e0be59a448bc70b347b9cfa389c637a919b6bedf53b403cc2b1b, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-cypher__indexing__index.txt, url: "https://docs.falkordb.com/cypher/indexing/index", sha256: 81d245c41a86da884f1ea3ac7a5d73835f33afbb19288c210212b7bc9fb2a680, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-cypher__indexing__range-index.txt, url: "https://docs.falkordb.com/cypher/indexing/range-index", sha256: 1f07204e511824d3a55a6b54d59f0e4ab3fe0deee9bee0d005ed97dc505a5fe3, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-cypher__indexing__fulltext-index.txt, url: "https://docs.falkordb.com/cypher/indexing/fulltext-index", sha256: b49be26c26b66c8c759359620c881a5d08b6342480cecd84a66d85a4245b521a, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-cypher__indexing__cch-index.txt, url: "https://docs.falkordb.com/cypher/indexing/cch-index", sha256: a825fc3f38908e0e9ec4752130cc62b803e58710de24e34efc0769b0cb5c1c94, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-cypher__functions.txt, url: "https://docs.falkordb.com/cypher/functions", sha256: a59272920050969fc515ef1e46d3083cfd3054c1363e138d996bab0b239252e3, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-cypher__procedures.txt, url: "https://docs.falkordb.com/cypher/procedures", sha256: b87859e804610dc243820cd4b02d17d260bf2f7c899cb0c76bd96d9dee3ea8f8, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: pyclient-1.8.0-source-excerpts.txt, url: "https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz", sha256: ae5e72fa77ed957a9f477e2391674715fdfdbba5c352d9c53568073b9d15374c, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
  - { file: references/evidence/falkordb/run-4.22.1-verify-core.txt, sha256: 256daa11aed5e75e142c84795b89ed8ea83ddb7a0248785c94fb4d8355b2a182, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-more.txt, sha256: 31c4152d51a15164f974cfa17a21023e3bca1ec85f675cce4def1c6f68bb6775, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-client.txt, sha256: bf904c98fb20054b1e0eebadf42b1e2eb1916c04e0c9d5ed524ff0e445b0ffbb, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-edge-rs-verify-core.txt, sha256: 0dd029631f7bcddb2e3a0ae2971e005a5388238d8850f9d661d1fa702a375d17, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-doc-snippets.txt, sha256: cc0852ee6c03b854201c782b71bb70e959b43d241327b1fe4beceaf1ac0d825e, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-exact-snippets.txt, sha256: 498c1827b101f9518996ed9626b730149d7155ee622e2c66f6295177d98a8cf7, retrieved_at: 2026-10-15T20:02:00Z, method: command }

---

# FalkorDB indexing and vector search

FalkorDB has four index types. The docs say:

> "FalkorDB supports four index types: **Range indexes** for exact-match and comparison queries, **Full-text indexes** for text search with stemming and scoring, **Vector indexes** for similarity search on embeddings, and **CCH indexes** for weighted point-to-point shortest-path (routing) queries." — evidence: `https://docs.falkordb.com/cypher/indexing/index` [^docs-indexing-index]

Each index is a separate DDL form. `CALL db.indexes()` lists them all, with `RANGE`, `FULLTEXT`, `VECTOR` or `CCH` as type (docs; run shows `VECTOR` rows with options in `run-4.22.1-verify-core.txt`).

Related: [Cypher support](/falkordb/cypher-support.md), [limits](/falkordb/limits-and-performance.md) (vector memory), [Python client](/falkordb/python-client.md) (index helper methods).

Run legend: **run** = executed on falkordb/falkordb:latest (module 4.22.1). **dev** = executed on the `edge-rs` dev image (module 999999). **doc** = docs only.

## Vector index (the GraphRAG path)

### DDL (run on 4.22.1)

```cypher
CREATE VECTOR INDEX FOR (p:Product) ON (p.embedding) OPTIONS {dimension:768, similarityFunction:'cosine', M:32, efConstruction:200}
```

Verbatim form in the docs (`https://docs.falkordb.com/cypher/indexing/vector-index`): `CREATE VECTOR INDEX FOR <entity_pattern> ON <entity_attribute> OPTIONS <options>`. The option map in the docs:

> "dimension: INT, // Required, length of the vector to be indexed" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index` [^docs-vector-index]

> "similarityFunction: STRING, // Required, currently only euclidean or cosine are allowed" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index` [^docs-vector-index]

> "M: INT, // Optional, maximum number of outgoing edges per node. default 16" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index`

> "efConstruction: INT, // Optional, number of candidates during construction. default 200" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index`

> "efRuntime: INT // Optional, number of candidates during search. default 10" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index`

Run results on 4.22.1 (`run-4.22.1-verify-core.txt`):

- `db.indexes` output for a euclidean index: `'dimension': 3, 'similarityFunction': 'euclidean', 'M': 16, 'efConstruction': 200, 'efRuntime': 10` (defaults filled in).
- Missing `dimension` or unknown similarity name is rejected: `Invalid vector index configuration` (4.22.1). On `edge-rs` the messages are `Invalid vector index configuration: dimension is required` and `Unknown similarity function 'manhattan', expected 'euclidean', 'ip', or 'cosine'`. The dev build accepts `ip`, which the docs do not list.
- Dimension range per docs: "**Note:** The supported dimension range is 1–4096." — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index`.

Doc-only detail (not run): "**Important**: When creating a vector index, both the vector dimension and similarity function must be provided."

### Insert and query (run)

Insert with `vecf32`:

```cypher
CREATE (p:Product {name:'a', description: vecf32([2.1, 0.82, 1.3])})
```

Query (doc signature, `https://docs.falkordb.com/cypher/indexing/vector-index`):

```cypher
CALL db.idx.vector.queryNodes('Product', 'embedding', 5, vecf32($q)) YIELD node, score RETURN node.name, score
```

Run with a Python list parameter `q` (run, `run-4.22.1-verify-more.txt`): `vector param knn -> [['a', 0.00611627101898193]]`.

Run with literals (`run-4.22.1-verify-core.txt`), cosine index on `embedding`:

```cypher
CALL db.idx.vector.queryNodes('Product', 'embedding', 2, vecf32([1.0, 0.1, 0.0])) YIELD node, score RETURN node.name, score
```

Result: `[['x', 0.00496286153793335], ['y', 0.900496304035187]]`.

Signature from the docs:

Signature block from the docs (`https://docs.falkordb.com/cypher/indexing/vector-index`, copied verbatim; the named-argument style is a placeholder, the working call uses positional arguments as shown above):

```cypher
CALL db.idx.vector.queryNodes(
    label: STRING,
    attribute: STRING,
    k: INTEGER,
    query: VECTOR
) YIELD node, score
```

Relationship form: `db.idx.vector.queryRelationships(relationshipType, attribute, k, query) YIELD relationship, score` (doc; the DDL `CREATE VECTOR INDEX FOR ()-[r:REV]->() ON (r.emb) OPTIONS {dimension:3, similarityFunction:'euclidean'}` ran on 4.22.1 without error (run)).

Errors seen (run):

- Query vector of wrong length: `Vector dimension mismatch, expected 3 but got 2`.
- `k = 0`: `Invalid arguments for procedure 'db.idx.vector.queryNodes'`.
- Insert with wrong length succeeded silently: a node with a 2-element vector in a 3-dim index was created (run). The 6.0.2 release notes say "A wrong-dimension vector no longer drops the entity from every index on its label (#3087)" (`https://api.github.com/repos/FalkorDB/FalkorDB/releases/latest` body). Check your own writes.

### Score meaning (important, contradicted by run)

The docs describe cosine as a similarity:

> "Range: -1 to 1 (1 = identical direction)" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index`

Run results show `score` is a **distance** (smaller = closer) for both metrics:

- euclidean: query equal to a stored vector gave `0.0`; the next nearest gave `0.316859513521194` (`run-4.22.1-verify-core.txt`).
- cosine: `[1,0,0]` against query `[1,0.1,0]` gave `0.00496`; orthogonal `[0,1,0]` gave `0.900`. Those are `1 - cos` values, so they are distances.

Also run: `vec.cosineDistance(p.description, vecf32([...]))` and `vec.euclideanDistance(...)` return the same kind of value (see the table in `run-4.22.1-verify-core.txt`). Sort ascending for nearest-first.

### Vector functions (doc, and run)

> "| vec.cosineDistance(*vector*, *vector*) | Returns the Cosine distance between the two input vectors |" — evidence: `https://docs.falkordb.com/cypher/functions` [^docs-functions]

`vecf32` creates a 32-bit float vector. `vecf64` is named in the functions FAQ but is unknown on 4.22.1 (run: `Unknown function 'vecf64'`). See [Cypher support](/falkordb/cypher-support.md).

### Parameters and HNSW tuning (doc)

> "**M** (default: 16): Maximum number of connections per node in the graph" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index`

> "**efRuntime** (default: 10): Number of candidates evaluated during search" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index`

The docs also say `efRuntime` "Can be adjusted per-query for speed/accuracy tradeoffs", but the DDL-level option is the only place shown. Per-query override was not tested. Open question.

### Limits the docs state about vectors (doc)

> "Vector queries don't combine well with property filters" — evidence: `https://docs.falkordb.com/cypher/indexing/vector-index`

Memory example (doc, `https://docs.falkordb.com/cypher/indexing/vector-index`): "Formula: `vectors × dimensions × 4 bytes + HNSW overhead (~20%)`". Check: 1,000,000 × 768 × 4 bytes = 3.07 GB before overhead, so with 20% overhead it is about 3.7 GB. The docs text says about 3 GB for that case. The two figures differ; treat the docs as approximate. Not measured here.

### Drop and inspect

```cypher
DROP VECTOR INDEX FOR (p:Product) ON (p.description)
```

Doc form (`https://docs.falkordb.com/cypher/indexing/vector-index`). Run on 4.22.1 for a relationship index: DDL accepted.

### Python client

`create_node_vector_index(label, *properties, dim=0, similarity_function=...)` builds the same DDL (source: `https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz`). Its client-side defaults are `dim=0` and a similarity name of `euclidean`, so pass both. Run: `create_node_vector_index('Doc', 'emb', dim=3, similarity_function='cosine')` returned ok. A broken f-string in the docs' Python example is covered in [python-client](/falkordb/python-client.md).

## Range index

DDL (doc, run `CREATE INDEX FOR (p:Person) ON (p.age)`):

```cypher
CREATE INDEX FOR (p:Person) ON (p.age)
CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)
DROP INDEX ON :Person(age)
```

Older form still accepted (doc): `CREATE INDEX ON :Person(age)`.

Plan check (run on 4.22.1, `run-4.22.1-verify-core.txt`): `GRAPH.EXPLAIN` for `MATCH (p:Person) WHERE p.age > 80 RETURN p` shows `Node By Index Scan | (p:Person)`. The docs show `Index Scan | (p:Person)`. The docs text is out of date for 4.22.1; search the plan for `Index Scan`.

Composite index (run): `CREATE INDEX FOR (p:Person) ON (p.first_name, p.last_name)` succeeded. The docs say "FalkorDB supports single-property indexes for node labels and for relationship type." (`https://docs.falkordb.com/cypher/indexing/index`). The constraint page relies on the composite form. Contradicted by run; trust the run.

Geospatial: "Geospatial indexes can currently only be leveraged with `<` and `<=` filters" (`https://docs.falkordb.com/cypher/indexing/range-index`).

Not handled: `<>` filters (known limitation, see [Cypher support](/falkordb/cypher-support.md)).

## Full-text index

DDL (doc):

```cypher
CREATE FULLTEXT INDEX FOR (n:Movie) ON (n.title)
CREATE FULLTEXT INDEX FOR (n:Movie) ON (n.title) OPTIONS { language: 'German', stopwords: ['a', 'ab'] }
DROP FULLTEXT INDEX FOR (n:Movie) ON (n.title)
```

Procedure form, run on 4.22.1:

```cypher
CALL db.idx.fulltext.createNodeIndex('Movie', 'title')
CALL db.idx.fulltext.queryNodes('Movie', 'Jun*') YIELD node RETURN node.title
```

Run result: `[['The Jungle Book'], ['June Forest'], ['Book of Jungle']]` for `Jun*` over three movies.

Scores (run): `CALL db.idx.fulltext.queryNodes('Movie', 'Jungle') YIELD node, score RETURN node.title, score ORDER BY score DESC` returned `The Jungle Book` and `Book of Jungle` with score `2.0`.

Doc: "In addition to yielding matching nodes, full-text index scans will return the score of each node." — evidence: `https://docs.falkordb.com/cypher/indexing/fulltext-index` (the score is TF-IDF). Query syntax is RediSearch's (doc, the page cites `Jun*`, `%Jngle%2` fuzzy, `Book -Jungle`, `Jungle|Forest`).

Version difference (dev): on `edge-rs`, `createNodeIndex('Movie', 'title')` with two arguments fails with `Received 2 arguments to procedure 'db.idx.fulltext.createNodeIndex', expected at most 1`. On 4.22.1 the same call works. The 6.0.2 changelog has "Validate index OPTIONS like 4.x" (`https://api.github.com/repos/FalkorDB/FalkorDB/releases/latest`). Test the exact form on the version you deploy.

Relationship full-text: `CALL db.idx.fulltext.queryRelationships('Manager','x') YIELD relationship RETURN ...` ran on 4.22.1 (returned no rows, no error). DDL `CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)` is doc-only.

## CCH index (weighted routing)

DDL (doc, run on 4.22.1):

```cypher
CREATE CCH INDEX FOR ()-[e:ROAD]->() ON (e.w)
CREATE CCH INDEX FOR ()-[e:ROAD|FERRY]->() ON (e.w)
```

Query (run, `run-4.22.1-verify-more.txt`):

```cypher
MATCH (a:Junction {id: 0}), (b:Junction {id: 2})
CALL db.idx.cch.query({sourceNode: a, targetNode: b, relTypes: ['ROAD'], weightProp: 'w'})
YIELD pathWeight, path
RETURN pathWeight, [n IN nodes(path) | n.id]
```

Result: `[[3.0, [0, 1, 2]]]` (run). The direct edge had weight 5.0, so the index found the cheaper two-hop route.

Errors (run):

- Second index with the same key: `a CCH index already exists over these relationship types and weight attribute`.
- Node pattern: `CCH index is only supported on relationships`.

Doc claims (doc only, `https://docs.falkordb.com/cypher/indexing/cch-index`): "Because the CCH index lives inside the index object, **nothing is written into your graph**"; "**Edge direction is respected**"; "When the weight property is missing on an edge, its weight defaults to `1`."; "routing technique for answering weighted point-to-point shortest-path queries in microseconds" (no measurement given).

The docs say the query returns in microseconds (doc: "answering weighted point-to-point shortest-path queries in microseconds"). Not measured.

## Open questions

- Score semantics on the official 6.0.2 build (run here on 4.22.1 and dev).
- Whether `efRuntime` can be set per query (doc says yes, not tested).
- Query-time behaviour of vector search combined with a label or property filter. The docs say it does not combine well. Measure before depending on it.

[^docs-functions]: Cypher Functions (vector functions) - https://docs.falkordb.com/cypher/functions
[^docs-indexing-index]: Indexing in FalkorDB - https://docs.falkordb.com/cypher/indexing
[^docs-vector-index]: Vector Indexing: Fast Similarity Search for GraphRAG - https://docs.falkordb.com/cypher/indexing/vector-index (last_modified 2026-09-30T11:44:18.508Z)
