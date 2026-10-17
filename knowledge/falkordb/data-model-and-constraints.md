---
type: Concept
title: FalkorDB data model, types and constraints
description: Nodes, relationships, labels, multi-type edges, property value types (what can and cannot be stored), temporal and point types, and unique/mandatory constraints, with run results from a 4.22.1 server.
resource: https://docs.falkordb.com/datatypes
tags: [falkordb, data-model, property-graph, types, constraints, labels, relationships]
status: stable
generated: { by: claude-haiku-5-5/falkordb-agent, at: 2026-10-15T19:45:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:45:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: docs-datatypes
    resource: https://docs.falkordb.com/datatypes
    title: FalkorDB Data Types
  - id: docs-constraint-create
    resource: https://docs.falkordb.com/commands/graph.constraint-create
    title: GRAPH.CONSTRAINT CREATE
  - id: docs-constraint-drop
    resource: https://docs.falkordb.com/commands/graph.constraint-drop
    title: GRAPH.CONSTRAINT DROP
  - id: docs-range-index
    resource: https://docs.falkordb.com/cypher/indexing/range-index
    title: Range Indexing
  - id: docs-functions
    resource: https://docs.falkordb.com/cypher/functions
    title: Cypher Functions
  - id: docs-cypher-support
    resource: https://docs.falkordb.com/cypher/cypher-support
    title: OpenCypher Standard Compatibility
evidence:
  - { name: docs-datatypes.txt, url: "https://docs.falkordb.com/datatypes", sha256: d4c27a2fbe09d5fa4a28251d6675e691c24226604d279017efae772690da8af5, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-commands__graph.constraint-create.txt, url: "https://docs.falkordb.com/commands/graph.constraint-create", sha256: e35f528430aa7cfabc38eced4fea925fb49be14dfb482005518b7d79b80e2ca8, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-cypher__indexing__range-index.txt, url: "https://docs.falkordb.com/cypher/indexing/range-index", sha256: 1f07204e511824d3a55a6b54d59f0e4ab3fe0deee9bee0d005ed97dc505a5fe3, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { name: docs-cypher__functions.txt, url: "https://docs.falkordb.com/cypher/functions", sha256: a59272920050969fc515ef1e46d3083cfd3054c1363e138d996bab0b239252e3, retrieved_at: 2026-10-15T19:35:00Z, method: curl, redistributed: false }
  - { file: references/evidence/falkordb/run-4.22.1-data-model.txt, sha256: 91d68336541fde73a262b2e6387409f247dcb713bb7ba9889837813c3332b970, retrieved_at: 2026-10-15T19:55:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-client.txt, sha256: bf904c98fb20054b1e0eebadf42b1e2eb1916c04e0c9d5ed524ff0e445b0ffbb, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-core.txt, sha256: 256daa11aed5e75e142c84795b89ed8ea83ddb7a0248785c94fb4d8355b2a182, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { file: references/evidence/falkordb/run-4.22.1-verify-more.txt, sha256: 31c4152d51a15164f974cfa17a21023e3bca1ec85f675cce4def1c6f68bb6775, retrieved_at: 2026-10-15T19:50:00Z, method: command }
  - { name: pyclient-1.8.0-source-excerpts.txt, url: "https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz", sha256: ae5e72fa77ed957a9f477e2391674715fdfdbba5c352d9c53568073b9d15374c, retrieved_at: 2026-10-15T19:45:00Z, method: command, redistributed: false }
---

# FalkorDB data model, types and constraints

FalkorDB is a labelled property graph. The docs define the parts in one page:

> "Nodes are persistent graph elements that can be connected to each other via relationships." — evidence: `https://docs.falkordb.com/datatypes` [^docs-datatypes]

> "They must have exactly one type that describes what they represent." — evidence: `https://docs.falkordb.com/datatypes` (relationships)

> "Relationships are always directed, connecting a source node to its destination." — evidence: `https://docs.falkordb.com/datatypes`

Related: [Cypher support](/falkordb/cypher-support.md), [indexing and vectors](/falkordb/indexing-and-vectors.md) (range index on properties), [algorithms](/falkordb/algorithms-and-weighted-paths.md) (weights are relationship properties), [limits](/falkordb/limits-and-performance.md).

## Labels and relationship types (run)

- A node can have several labels. The docs example is "a node representing London may be created with the `Place` and `City` labels" (`https://docs.falkordb.com/datatypes`). Run: `CREATE (:Place:City {name:'London'})`, then `MATCH (n:Place:City) RETURN n.name` returned `London`.
- A relationship has exactly one type in its definition. A pattern may list several types: "When querying relationships, multiple types can be specified by separating them with a pipe (`|`)." Run: `MATCH (:P)-[r:RESIDENT_OF|VISITOR_TO]->(:City) RETURN count(r)` returned `2` with one edge of each type.
- Weights and other numbers live as relationship properties, for example `[:ROAD {length:3200, time:240}]` (see [algorithms](/falkordb/algorithms-and-weighted-paths.md)).

## What a property value can be

Docs list the scalar types (`https://docs.falkordb.com/datatypes`, Scalar Types) and the FAQ answer: "You can store **strings**, **booleans**, **integers** (64-bit signed), **floating-point values** (64-bit doubles), **geospatial points**, and **temporal types** (Date, Time, DateTime, Duration) as property values."

Run results on 4.22.1 (`run-4.22.1-verify-client.txt`, `run-4.22.1-data-model.txt`):

| Value stored as a property | Result |
| --- | --- |
| String, integer, float, boolean | accepted |
| `null` in `CREATE (n:N {v: null})` | accepted but not stored: `keys(n)` returned `[]` |
| Map, `{a:1}` | error: `Property values can only be of primitive types or arrays of primitive types` |
| List of primitives, `[1,2,3]`, `['a', null]` with null inside | list of primitives accepted; a list containing `null` was rejected with the same primitive-only error |
| List of maps, `[{a:1}]` | same primitive-only error |
| List of floats (vector) via `vecf32([...])` | accepted (see [indexing](/falkordb/indexing-and-vectors.md)) |
| `date(...)`, `localtime(...)`, `localdatetime(...)`, `duration(...)` | accepted |
| `point({...})` | accepted, see below |

Docs quotes:

> "Unlike all other scalars, `null` cannot be stored as a property value." — evidence: `https://docs.falkordb.com/datatypes` [^docs-datatypes]

> "Maps cannot be stored as property values." — evidence: `https://docs.falkordb.com/datatypes`

> "Arrays can be stored as property values provided that no array element is of an unserializable type, such as graph entities or `null` values." — evidence: `https://docs.falkordb.com/datatypes`

The run confirmed the rule for maps and nulls. A `null` written as a property is dropped silently, not rejected.

## Numbers and booleans

> "All FalkorDB integers are treated as 64-bit signed integers." — evidence: `https://docs.falkordb.com/datatypes`

> "All FalkorDB floating-point values are treated as 64-bit signed doubles." — evidence: `https://docs.falkordb.com/datatypes`

Booleans and integers are different types. Run: `RETURN 1 = true` returned `false`. Docs: "As FalkorDB considers types in its comparisons, 1 is not considered equal to `true`" (`https://docs.falkordb.com/datatypes`).

Null logic (run): `RETURN null = null` returned `null`. Docs: "`null = null` will evaluate to `null`" (`https://docs.falkordb.com/datatypes`).

## Points

> "The Point data type is a set of latitude/longitude coordinates, stored within FalkorDB as a pair of 32-bit floats." — evidence: `https://docs.falkordb.com/datatypes` [^docs-datatypes]

Run: `RETURN point({latitude: 41.4, longitude: -75.7})` returned `{'latitude': 41.4000015258789, 'longitude': -75.6999969482422}` (`run-4.22.1-verify-client.txt`). Float32 rounding is real. Keep the coordinates in a double property if you need exact values. The range index can take point properties (see [indexing](/falkordb/indexing-and-vectors.md)), and `distance(e.location, scranton) < 5000` is the doc example (`https://docs.falkordb.com/cypher/indexing/range-index`).

## Strings

> "FalkorDB strings are Unicode character sequences." — evidence: `https://docs.falkordb.com/datatypes`

`intern('...')` deduplicates a string value across the database (run: `CREATE (:A {v:intern('VERY LONG STRING')})` ran). Docs: "This function deduplicates the input string by storing a single internal copy across the database." (`https://docs.falkordb.com/cypher/functions`).

## Temporal types (run)

Docs: "FalkorDB supports the following temporal types that allow modeling and querying time-related data" (`https://docs.falkordb.com/datatypes`): Date, Time, DateTime, Duration, ISO 8601.

Run:

```cypher
RETURN date('2025-09-15').year, localtime('15:45:20').hour, duration('P1Y2M3DT4H5M6S').hours
```

Result: `[[2025, 15, 4.0]]`. Also ran: `CREATE (:Log {at: localdatetime('2025-06-29T13:45:00')})` and `CREATE (:Cooldown { period: duration('P3DT12H') })`.

Doc inconsistency: the body says "Represents a time of day in the format HH:MM:SS.", but the FAQ says "**Time** (HH:MM:SS with timezone)" (`https://docs.falkordb.com/datatypes`). Not tested.

## Maps and map projections (doc)

Maps are returned from queries and used as projections, for example `RETURN n {.name, .age} AS projection`. Maps are not stored as properties (see above). Map projections of a `null` entity evaluate to `null`, so `collect()` skips them (doc quote in `https://docs.falkordb.com/datatypes`). Not run.

## Constraints

FalkorDB supports two constraint types. The command page defines them:

> "A mandatory constraint enforces existence of given attributes for all nodes with a given label or for all edges with a given relationship-type." — evidence: `https://docs.falkordb.com/commands/graph.constraint-create` [^docs-constraint-create]

> "A unique constraint enforces uniqueness of values of a given set of attributes for all nodes with a given label or for all edges with a given relationship-type." — evidence: `https://docs.falkordb.com/commands/graph.constraint-create`

Syntax, verbatim from the docs (`https://docs.falkordb.com/commands/graph.constraint-create`):

```
GRAPH.CONSTRAINT CREATE key constraintType {NODE label | RELATIONSHIP reltype} PROPERTIES propCount prop [prop...]
```

Doc restrictions:

- "A unique constraint requires the existence of an exact-match index prior to its creation." (`https://docs.falkordb.com/commands/graph.constraint-create`) Create the index first. The run created it first.
- "A unique constraint is enforced for a given node or edge only if all the constrained properties are defined (non-null)." (same page)
- "Unique constraints are not enforced for array-valued properties." (same page)
- Creation is asynchronous. Quote: "Constraints are created asynchronously. The constraint creation command will reply with `PENDING`" (same page). Status values: `UNDER CONSTRUCTION`, `OPERATIONAL`, `FAILED`.

Run on 4.22.1 (`run-4.22.1-verify-core.txt`, `run-4.22.1-data-model.txt`; the calls below are the ones in `script-verify_core.py.txt`, with the variable named `g5` and comments added):

```python
g5.query("CREATE INDEX FOR (p:Person) ON (p.first_name, p.last_name)")
g5.create_node_unique_constraint("Person", "first_name", "last_name")   # -> PENDING
g5.list_constraints()   # -> [{'type': 'UNIQUE', 'label': 'Person', 'properties': ['first_name', 'last_name'], 'entitytype': 'NODE', 'status': 'OPERATIONAL'}]
g5.query("CREATE (:Person {first_name:'Frank', last_name:'Costanza'})")  # -> ResponseError: unique constraint violation on node of type Person
```

Mandatory (run, clean graph):

```python
g.query("CREATE (:P {id:1}), (:P {id:2})")
g.create_node_mandatory_constraint("P", "id")       # -> PENDING
# status after wait: OPERATIONAL
g.query("CREATE (:P {n:10})")
# -> ResponseError: mandatory constraint violation: node with label P missing property id
```

FAILED case (run): a mandatory constraint created on nodes that lacked the property went to `status: FAILED` and was not enforced (the next insert without `id` succeeded). That matches the doc: "otherwise, if a conflict is detected, the constraint status is updated to `FAILED` and the constraint is not enforced" (`https://docs.falkordb.com/commands/graph.constraint-create`). Clean the data first.

Synchronous rejects (doc): syntax error, constraint already exists, missing supporting index for a unique constraint.

Drop: `GRAPH.CONSTRAINT DROP` (docs page `https://docs.falkordb.com/commands/graph.constraint-drop`); Python `drop_node_unique_constraint(label, *props)`. Not run.

## Python helpers

`create_node_unique_constraint`, `create_node_mandatory_constraint`, `create_edge_*`, `drop_*_constraint`, `list_constraints` exist in falkordb-py 1.8.0 (source: `https://files.pythonhosted.org/packages/dd/96/a2f4d214a0c8871e72d0fdb80b5e7caf93037ff8583d1c4e822c4344bd17/falkordb-1.8.0.tar.gz`). See [python-client](/falkordb/python-client.md).

## Open questions

- Behaviour of unique constraints on relationship types and on array-valued properties (doc only).
- Whether a unique constraint without a backing index fails synchronously on 4.22.1 (doc says it must; not run).
- Whether relationship `RESIDENT_OF|VISITOR_TO` creation (multi-type in CREATE) is rejected. Doc says a relationship has one type; the CREATE form was not tested.

[^docs-constraint-create]: GRAPH.CONSTRAINT CREATE - https://docs.falkordb.com/commands/graph.constraint-create
[^docs-datatypes]: FalkorDB Data Types - https://docs.falkordb.com/datatypes
