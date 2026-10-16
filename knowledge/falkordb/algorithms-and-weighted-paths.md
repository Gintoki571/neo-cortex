---
type: Concept
title: FalkorDB graph algorithms and weighted shortest paths
description: CALL syntax, arguments and yields for FalkorDB's built-in algorithms (SPpaths, SSpaths, AStar, PageRank, BFS, WCC, CDLP, MSF, betweenness, harmonic, max flow, CCH), with run results and doc-vs-run differences.
resource: https://docs.falkordb.com/algorithms
tags: [falkordb, algorithms, shortest-path, weighted, pagerank, wcc, cdlp, msf, maxflow, graphrag]
status: stable
generated: { by: claude-haiku-5-5/falkordb-agent, at: 2026-10-15T19:45:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:45:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: docs-algorithms-index
    resource: https://docs.falkordb.com/algorithms
    title: Graph Algorithms in FalkorDB
  - id: docs-sppath
    resource: https://docs.falkordb.com/algorithms/sppath
    title: Shortest Paths Between Nodes (algo.SPpaths)
  - id: docs-sspath
    resource: https://docs.falkordb.com/algorithms/sspath
    title: Single Source Shortest Path (algo.SSpaths)
  - id: docs-astar
    resource: https://docs.falkordb.com/algorithms/astar
    title: algo.AStar
  - id: docs-pagerank
    resource: https://docs.falkordb.com/algorithms/pagerank
    title: PageRank
  - id: docs-bfs
    resource: https://docs.falkordb.com/algorithms/bfs
    title: Breadth-First Search (BFS)
  - id: docs-wcc
    resource: https://docs.falkordb.com/algorithms/wcc
    title: Weakly Connected Components (WCC)
  - id: docs-cdlp
    resource: https://docs.falkordb.com/algorithms/cdlp
    title: Community Detection using Label Propagation (CDLP)
  - id: docs-msf
    resource: https://docs.falkordb.com/algorithms/msf
    title: Minimum Spanning Forest (MSF)
  - id: docs-betweenness
    resource: https://docs.falkordb.com/algorithms/betweenness-centrality
    title: Betweenness Centrality
  - id: docs-harmonic
    resource: https://docs.falkordb.com/algorithms/harmonic-centrality
    title: Harmonic Centrality
  - id: docs-maxflow
    resource: https://docs.falkordb.com/algorithms/maxflow
    title: Maximum Flow
  - id: docs-cch
    resource: https://docs.falkordb.com/cypher/indexing/cch-index
    title: CCH Indexing
  - id: docs-procedures
    resource: https://docs.falkordb.com/cypher/procedures
    title: Cypher Procedures
evidence:
  - { file: references/evidence/falkordb/docs-algorithms__index.txt, sha256: 68f89a1b39c41f512c093948b5661c81c6df1edf4aa4e05982de59c250e3fb08, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__sppath.txt, sha256: 35229cbf1b7ef99bda8536230dcc9e4bfc8b9bf96f86c06ec1f3809a1c0f8519, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__sspath.txt, sha256: 44b4fa43fb7586d3a9946931b7d69b10f924e2581982d5dcf80ae8681eafeb8a, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__astar.txt, sha256: bf6dcf5aac47715b2b159a8798a0943cff507c074ce80d7624a33c320b7e50d0, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__pagerank.txt, sha256: c0395c7c91add49b55e4b8f9fe313f7156ed88b080c08c9778797a1228585cb5, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__bfs.txt, sha256: 069b040a5fc8467b4ad123554a9c47b6bb1862c36c39dbf4d5b779a82ec15c76, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__wcc.txt, sha256: 59ffc4ef8bed5115f40ec4f55aa41f5495ae216a2d4217e8d9c30e4e6bae9ae9, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__cdlp.txt, sha256: d6f91453e5bd894e8f2f00d53c26ab702aa49dee6a02e40cb17bd31a51c69c55, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__msf.txt, sha256: 758df7006a5ec269ded88d1abaa96f3feda04a373391b858d44757a0156ffdec, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__betweenness-centrality.txt, sha256: bd63274040dc8355a23b97e0b6215f1faf62c203be5ddc6a8d07a6447c014761, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__harmonic-centrality.txt, sha256: 1764f18d199001a35cd932930529c4ce7fc9d25ab36c3c231fb3543831d0ce45, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-algorithms__maxflow.txt, sha256: 1bd24461d84119b63d0b7de3662a780325a6b8441ece4b721ce186dfcb25288c, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-cypher__procedures.txt, sha256: b87859e804610dc243820cd4b02d17d260bf2f7c899cb0c76bd96d9dee3ea8f8, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/docs-cypher__indexing__cch-index.txt, sha256: a825fc3f38908e0e9ec4752130cc62b803e58710de24e34efc0769b0cb5c1c94, retrieved_at: 2026-10-15T19:35:00Z, method: curl }
  - { file: references/evidence/falkordb/doc-cypher-snippets-extracted.json, sha256: 49ee7fc0c96f547345caec375a83a4bd83e5ff30b31a2cd74fe83dba262519c5, retrieved_at: 2026-10-15T19:40:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-doc-snippets.txt, sha256: cc0852ee6c03b854201c782b71bb70e959b43d241327b1fe4beceaf1ac0d825e, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-more.txt, sha256: 31c4152d51a15164f974cfa17a21023e3bca1ec85f675cce4def1c6f68bb6775, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-bfs.txt, sha256: 49947e8ed2bfc195b172e72fc4eb7562387c61833f79f1fbf6c96ed8d27b29e0, retrieved_at: 2026-10-15T19:55:00Z, method: command }
  - { file: references/evidence/falkordb/script-run_blocks.py.txt, sha256: 26527e0203b2d6d5d13a2fab4713892f6e4c3b541eff8a92b1483857f8321ea2, retrieved_at: 2026-10-15T19:50:00Z, method: command }
---

# FalkorDB graph algorithms and weighted shortest paths

Algorithms are CALL procedures. They run against the in-memory graph and stream rows. The docs list them in one table (`docs-cypher__procedures.txt`):

> "| algo.SPpaths | `config` | `path`, `pathWeight`, `pathCost` | Finds shortest paths between a source and a target node. See [SPpaths Algorithm](/algorithms/sppath) for details. |" — evidence: `docs-cypher__procedures.txt` [^docs-procedures]

Related: [Cypher support](/falkordb/cypher-support.md) (CALL syntax, YIELD), [indexing and vectors](/falkordb/indexing-and-vectors.md) (CCH index, `db.idx.cch.query`), [data model](/falkordb/data-model-and-constraints.md) (weights are properties).

Run legend as elsewhere: **run** = executed on falkordb/falkordb:latest (module 4.22.1). **doc** = docs only.

## Procedure index

| Procedure | Config / args | Yields | Docs | Run |
| --- | --- | --- | --- | --- |
| `algo.SPpaths` | map: sourceNode, targetNode, relTypes, weightProp, costProp, maxCost, maxLen, relDirection, pathCount | path, pathWeight, pathCost | yes | run |
| `algo.SSpaths` | map: sourceNode, relTypes, weightProp, costProp, maxCost, maxLen, relDirection, pathCount | path, pathWeight, pathCost | yes | run |
| `algo.AStar` | map: sourceNode, targetNode, relTypes, weightProp, latitudeProperty, longitudeProperty, heuristicScale, relDirection, pathCount | path, pathWeight | yes | run |
| `algo.pageRank` | (label, relationship-type), positional | node, score | yes | run |
| `algo.BFS` / `algo.bfs` | (start_node, max_depth, relationship) | nodes, edges | yes | run (see BFS caveat) |
| `algo.WCC` / `algo.wcc` | [config] (nodeLabels, relationshipTypes) | node, componentId | yes | run |
| `algo.labelPropagation` (CDLP) | [config] (nodeLabels, relationshipTypes, maxIterations) | node, communityId | yes | run |
| `algo.MSF` | config (nodeLabels, relationshipTypes, objective, weightAttribute) | edges, nodes | yes | run |
| `algo.betweenness` | map (nodeLabels, relationshipTypes, samplingSize, samplingSeed) | node, score | yes | run (map-key caveat) |
| `algo.HarmonicCentrality` | [config] (nodeLabels, relationshipTypes) | node, score, reachable | yes (not in procedure table) | run |
| `algo.maxFlow` | config (sourceNodes, targetNodes, relationshipTypes, capacityProperty, nodeLabels), required | nodes, edges, edgeFlows, maxFlow | yes (not in procedure table) | run |
| `db.idx.cch.query` | map (sourceNode, targetNode, relTypes, weightProp) | pathWeight, path | yes (CCH page) | run |

The procedure table in the docs omits `algo.HarmonicCentrality`, `algo.maxFlow` and `db.idx.cch.query`. They still run (run). Procedure names are matched case-insensitively in practice: `algo.wcc` and `algo.WCC` both ran.

## Weighted shortest paths

### algo.SPpaths (point to point)

Docs syntax (`docs-algorithms__sppath.txt`), verbatim:

```cypher
CALL algo.SPpaths({
  sourceNode: <node>,
  targetNode: <node>,
  relTypes: [<relationship_type>],
  weightProp: <property>,
  costProp: <property>,         // optional
  maxCost: <int>,               // optional
  maxLen: <int>,                // optional
  relDirection: "outgoing",    // or "incoming", "both"
  pathCount: <int>              // 0 = all, 1 = single (default), n > 1 = up to n
})
YIELD path, pathWeight, pathCost
```

Docs semantics (quotes):

> "`weightProp` | String | Property to minimize along the path (e.g., `dist`, `time`)" — evidence: `docs-algorithms__sppath.txt` [^docs-sppath]

> "`pathCount` | Integer | Number of paths to return (0 = all shortest, 1 = default, n = max number of results)" — evidence: `docs-algorithms__sppath.txt`

> "**weightProp** is the property the algorithm *minimizes* (e.g. distance). **costProp** is a separate property used as a *constraint* — you can set `maxCost` to exclude paths whose total cost exceeds a threshold." — evidence: `docs-algorithms__sppath.txt`

Run on a small graph (`run-4.22.1-verify-more.txt`). Nodes A, B, C, D. Edges A-B (dist 1, time 5), B-D (dist 1, time 5), A-C (dist 3, time 1), C-D (dist 3, time 1), A-D (dist 2, time 2).

```cypher
MATCH (a:City{name:'A'}), (d:City{name:'D'})
CALL algo.SPpaths({sourceNode: a, targetNode: d, relTypes: ['Road'], weightProp: 'dist'})
YIELD path, pathWeight
RETURN pathWeight, [n IN nodes(path) | n.name]
```

Result: `[[2.0, ['A', 'D']]]` (run).

```cypher
MATCH (a:City{name:'A'}), (d:City{name:'D'})
CALL algo.SPpaths({sourceNode: a, targetNode: d, relTypes: ['Road'], weightProp: 'dist', costProp: 'time', pathCount: 0})
YIELD path, pathWeight, pathCost
RETURN pathWeight, pathCost, [n IN nodes(path) | n.name]
```

Result (run): `[[2.0, 10.0, ['A', 'B', 'D']], [2.0, 2.0, ['A', 'D']]]`. Both paths tie on distance (2.0). `pathCount: 0` returned both.

- No path: returns zero rows, no error (run: `SPpaths no path -> []`; docs say the same in the FAQ).
- `relDirection: 'both'` from D to A found the path (run: `[[2.0]]`).
- `weightProp` names a property that is missing on every edge: the run returned `pathWeight` `1.0` (one hop, default weight). Unknown config keys (`bogus: 1`) were ignored silently (run).
- `pathWeight` came back as a float (`2.0`) on 4.22.1, though the docs table says Integer.

Doc's own example uses a road-network image not present in the text. Its expected output (`pathWeight 12`, `[A, D, E, G]`) cannot be reproduced from the page. Open question; see the bottom.

### algo.SSpaths (one source, many targets)

Docs signature (`docs-algorithms__sspath.txt`): `CALL algo.SSpaths({ sourceNode, relTypes, weightProp, costProp, maxCost, maxLen, relDirection, pathCount })`. `weightProp` is optional. If omitted, "all edges are treated as having equal weight" (FAQ, doc) and the search counts hops.

Run (`run-4.22.1-verify-more.txt`):

```cypher
MATCH (a:City{name:'A'})
CALL algo.SSpaths({sourceNode: a, relTypes: ['Road'], pathCount: 10})
YIELD path, pathCost
RETURN pathCost, [n IN nodes(path) | n.name] ORDER BY pathCost
```

Result: `[[1.0, ['A','D']], [1.0, ['A','C']], [1.0, ['A','B']], [2.0, ['A','B','D']], [2.0, ['A','C','D']]]` (run). Hop counts, as documented.

### algo.AStar (geographic heuristic)

Docs: "Like [algo.SPpaths](/algorithms/sppath), it minimizes a numeric edge property (`weightProp`), but it is guided by a geographic heuristic" — evidence: `docs-algorithms__astar.txt` [^docs-astar]

Every node needs latitude and longitude properties (doc: "Every node must carry latitude and longitude properties").

Doc example, verbatim graph, run:

```cypher
CREATE
  (a:Junction {name:'A', lat:40.7128, lon:-74.0060}),
  (b:Junction {name:'B', lat:40.7300, lon:-73.9950}),
  (c:Junction {name:'C', lat:40.7580, lon:-73.9855}),
  (a)-[:ROAD {length:3200, time:240}]->(b),
  (b)-[:ROAD {length:4100, time:300}]->(c),
  (a)-[:ROAD {length:8000, time:360}]->(c)
```

```cypher
MATCH (a:Junction {name:'A'}), (c:Junction {name:'C'})
CALL algo.AStar({
  sourceNode: a,
  targetNode: c,
  relTypes: ['ROAD'],
  weightProp: 'length',
  latitudeProperty: 'lat',
  longitudeProperty: 'lon'
})
YIELD path, pathWeight
RETURN pathWeight, [n IN nodes(path) | n.name] AS route
```

Run result: `[[7300.0, ['A', 'B', 'C']]]` (docs expected `7300`, match).

Time-based (run): with `weightProp: 'time'` and `heuristicScale: 0.0333`, the result is `[[360.0, ['A', 'C']]]`. Check: A to C direct = 360 s; A-B-C = 240 + 300 = 540 s. Correct.

Heuristic rule (doc): "`heuristicScale` must be a non-negative number." — evidence: `docs-algorithms__astar.txt`. The docs add that a smaller value stays optimal but explores more nodes, and a larger value than the true minimum weight-per-meter trades optimality for speed.

Doc table: "| Travel time in seconds | `1 / max_speed_m_per_s` | Fastest possible time to cover one meter |". Use `heuristicScale` = 1 / max speed in m/s when `weightProp` is seconds (for example 0.0333 for 30 m/s).

### BFS

Docs: "CALL algo.bfs(start_node, max_depth, relationship) YIELD nodes, edges" (`docs-algorithms__bfs.txt`). `relationship` may be null (all types). Run (`run-4.22.1-bfs.txt`):

```cypher
MATCH (alice:Person {name: 'Alice'}) CALL algo.bfs(alice, 2, 'FRIEND') YIELD nodes, edges RETURN [n IN nodes | n.name], size(edges)
```

Result: `[[['Bob', 'Charlie', 'David', 'Eve'], 4]]`. `nodes` is a list of all visited nodes within depth 2 (excluding the start).

**Caveat (run):** the docs' "friend recommendations" snippet fails on 4.22.1 with `Type mismatch: expected Null but was Pointer`. It has `WHERE size(nodes) >= 3` directly after `YIELD nodes`. Do not copy that block. Filter in a `WITH` instead, for example `... YIELD nodes WITH alice, nodes AS reached UNWIND reached AS f ...` (not run; write your own and test).

### Connected components, communities, spanning forest

WCC (run; matches the docs' componentIds):

```cypher
CALL algo.WCC(null) yield node, componentId
```

Docs expected component ids `0` (Alice, Bob, Charlie), `3` (David, Emma), `5` (Frank). Run: `[['David', 'Emma'], 3]`, `[['Frank'], 5]`, `[['Alice', 'Bob', 'Charlie'], 0]` (run, `run-4.22.1-doc-snippets.txt`). Component ids are not contiguous.

Label propagation (CDLP), run with the docs' graph:

```cypher
CALL algo.labelPropagation() YIELD node, communityId RETURN node.name AS name, communityId ORDER BY communityId, name
```

Run: Alice, Bob, Charlie, Diana, Grace, Henry = 0; Frank and Iris = 2; Eve and Jack = 4; Kate = 10. The docs expected Eve, Frank, Iris and Jack together in community 2. **Contradicted by run.** The docs also say "nodes are processed in random order" (`docs-algorithms__cdlp.txt`), so split results can vary between runs. Config keys `maxIterations`, `nodeLabels` and `relationshipTypes` ran. An unknown relationship type fails: `labelPropagation configuration, unknown relationship-type NOPE`.

Minimum spanning forest (run). Docs example:

```cypher
CALL algo.MSF({weightAttribute: 'cost'}) YIELD edges, nodes RETURN edges, nodes
```

Result: one row with edges and nodes lists (run). Requires the graph from the docs; ran.

### PageRank

Docs syntax: `CALL algo.pageRank(label, relationship-type) YIELD node, score` with positional arguments (`docs-algorithms__pagerank.txt`). `label` null means all nodes; `relationship-type` null means all types.

```cypher
CALL algo.pageRank('Paper', 'CITES')
YIELD node, score
RETURN node.title AS paper, score
ORDER BY score DESC
```

Run on the docs' citation graph (run):

| paper | docs expected | run (4.22.1) |
| --- | --- | --- |
| Graph Algorithms in Database Systems | 0.43 | 0.399256944656372 |
| Data Mining Techniques | 0.21 | 0.157152637839317 |
| PageRank Applications | 0.19 | 0.206247434020042 |
| Network Analysis Methods | 0.14 | 0.139464408159256 |
| Social Network Graph Theory | 0.03 | 0.0978785678744316 |

**Contradicted by run.** The run values sum to 1.0. The order of the middle rows also differs. The docs' table may be illustrative. Use the ranking, not the docs' numbers.

The docs state: "The sum of all scores in a graph equals 1.0" (quote from `docs-algorithms__pagerank.txt`).

### Betweenness and harmonic centrality

Betweenness syntax (docs): `CALL algo.betweenness({nodeLabels: [...], relationshipTypes: [...], samplingSize: <int>, samplingSeed: <int>}) YIELD node, score`. Map keys are bare identifiers. The docs' FAQ example with quoted keys (`{'nodeLabels': ['Person']}`) fails with a parse error on 4.22.1 (`expected a property name or '}'`, run). Use bare keys.

Harmonic (run): `CALL algo.HarmonicCentrality() YIELD node, score, reachable` ran; results for the docs' graph: `Alice 2.84`, `Bob 1.50`, `Charlie 1.50`, `David 1.00`, `Eve 0.0`. The docs say the score is "algorithm based on HyperLogLog (HLL) sketches" (`docs-algorithms__harmonic-centrality.txt`); expect estimates, not exact sums.

### Max flow

Docs syntax: `CALL algo.maxFlow(config) YIELD nodes, edges, edgeFlows, maxFlow`. `config` is required. Required keys: `sourceNodes`, `targetNodes`, `relationshipTypes`. Calling with no config fails: `Procedure algo.maxFlow requires 1 arguments, got 0` (run).

Run of the docs example (run, `run-4.22.1-doc-snippets.txt`): `maxFlow = 13.0` (docs expected `13`), and edges A-B 8.0, A-C 5.0, B-C 8.0 (docs expected 8, 5, 8). Match.

### CCH (point-to-point on a weighted index)

Index DDL and details are in [indexing-and-vectors](/falkordb/indexing-and-vectors.md). Query (run on 4.22.1): `db.idx.cch.query({sourceNode, targetNode, relTypes, weightProp})` returned `pathWeight` 3.0 and the path through the cheaper two-hop route, where the direct edge weighed 5.0.

## Doc claims about complexity (doc only)

These are complexity statements, not measurements.

> "The algorithm operates with a time complexity of **O(V · E²)**, where" — evidence: `docs-algorithms__maxflow.txt` (max flow)

> "WCC operates with a time complexity of **O(|V| + |E|)**" — evidence: `docs-algorithms__wcc.txt` [^docs-wcc]

> "CDLP operates with a time complexity of **O(m + n)** per iteration" — evidence: `docs-algorithms__cdlp.txt`

Not timed here.

## Open questions

- Does `algo.SPpaths` use Dijkstra? The docs never say so. The A* page compares only to "a plain Dijkstra search" (`docs-algorithms__astar.txt`). Not confirmed.
- Behaviour with negative weights in SPpaths/SSpaths (docs say nothing).
- The docs' road-network example for SPpaths and SSpaths (expected `pathWeight 12`) relies on a graph image; the text does not give the edges. Not reproduced.
- BFS friend-recommendation snippet: correct form not documented (the docs' block fails on 4.22.1).
- CDLP grouping and PageRank numbers differ from the docs (see above). Confirm on 6.0.2 before relying on exact values.

[^docs-astar]: algo.AStar - https://docs.falkordb.com/algorithms/astar
[^docs-procedures]: Cypher Procedures - https://docs.falkordb.com/cypher/procedures
[^docs-sppath]: Shortest Paths Between Nodes (algo.SPpaths) - https://docs.falkordb.com/algorithms/sppath
[^docs-wcc]: Weakly Connected Components (WCC) - https://docs.falkordb.com/algorithms/wcc
