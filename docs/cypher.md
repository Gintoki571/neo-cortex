# Cypher and graph algorithms

Neo-Cortex runs every query against one FalkorDB graph per tenant, named `neo_<tenant>` (`store.py:_graph_name`). Parameters are `$name`. Times are epoch-ms integers. In f-string blocks `{{` and `}}` are literal braces, as in the source. Blocks are copied from the source: `{label}`, `{prop}`, `{n}`, `{cond}`, `{edge}`, `{key}`, `{other}`, `{int(...)}` are f-string placeholders filled at run time, and `{DIM}` is 768. Each section names the file and function that issues the query.

The product depends on these queries: the write path (`MERGE`/`CREATE`/`UNWIND` batches), vector and full-text lookups, variable-length paths (`who`), shortest paths (`algo.SPpaths`, in `connect` and `ask`), the subgraph fetch for Personalized PageRank, and the temporal reads for `timeline` and supersession.

Not used: `algo.pageRank` (FalkorDB has no personalization vector, so PPR is computed in numpy over the fetched subgraph; see `channels.ppr`).

## 1. Schema and indexes

`schema.py:ensure_schema`, run once per tenant graph by `store.py:Store.graph`. Idempotent: only "already indexed" errors are swallowed.

```cypher
CREATE VECTOR INDEX FOR (n:{label}) ON (n.{prop}) OPTIONS {{dimension:{DIM}, similarityFunction:'cosine'}}
CREATE FULLTEXT INDEX FOR (n:Entity) ON (n.name)
CREATE INDEX FOR (n:{label}) ON (n.{prop})
```

Vector indexes: `Memory.emb`, `Chunk.emb`, `Entity.emb`. Range indexes: `id` on Memory, Chunk, Entity, Document, Session, Agent, Handoff, Judgment; plus `Entity.key`, `Entity.type`, `Memory.created_ms`, `Memory.valid_from_ms`, `Chunk.date_ms`, `Document.date_ms`. The full-text index is for fuzzy entity-name lookup only; BM25 is in-process (section 5).

## 2. Ingest and memory writes

### Documents, chunks, mentions, relations

`write.py:_ingest_doc` (one document per call; `_replace_old` runs first when a changed document is re-ingested).

```cypher
CREATE (:Document {id:$id, kind:$kind, title:$title, uri:$uri, path:$path, author:$author, date_ms:$date, status:$status, labels:$labels, hash:$hash})
UNWIND $rows AS r CREATE (c:Chunk {id:r.id, doc_id:$d, pos:r.pos, text:r.text, kind:$k, date_ms:$t, emb:vecf32(r.emb)}) WITH c MATCH (d:Document {id:$d}) CREATE (d)-[:HAS_CHUNK]->(c)
UNWIND $rows AS r MATCH (c:Chunk {id:r.c}), (e:Entity {id:r.e}) CREATE (c)-[:MENTIONS {conf:r.conf}]->(e)
UNWIND $rows AS r MATCH (a:Entity {id:r.h}), (b:Entity {id:r.t}) CREATE (a)-[:REL {type:r.type, conf:r.conf, source_id:r.src, valid_from_ms:$t}]->(b)
MATCH (e:Entity {id:$e}), (d:Document {id:$d}) MERGE (e)-[:{edge}]->(d)
```

The last statement uses `edge` = `AUTHORED` or `PARTICIPATED`.

### Re-ingest: delete a changed document

`write.py:_replace_old`.

```cypher
MATCH ()-[r:REL]->() WHERE r.source_id IN $c DELETE r
MATCH (c:Chunk) WHERE c.id IN $c DETACH DELETE c
MATCH (d:Document {id:$d}) DETACH DELETE d
```

### Entity mention counts

`write.py:_refresh_entities`. Recomputed for every entity an ingest or dream run touches.

```cypher
MATCH (e:Entity) WHERE e.id IN $ids OPTIONAL MATCH (e)<-[:MENTIONS]-(x) WITH e, count(x) AS n, min(x.date_ms) AS f, max(x.date_ms) AS l SET e.mentions = n, e.first_seen_ms = coalesce(f, e.first_seen_ms), e.last_seen_ms = coalesce(l, e.last_seen_ms)
```

### Single-valued relations end (supersession of OWNS and MEMBER_OF)

`write.py:_supersede` (rendered for `OWNS`, tail side; `MEMBER_OF` uses the head side). The second statement closes `valid_to_ms` on the old edges.

```cypher
MATCH (a:Entity)-[r:REL {{type:$t}}]->(b:Entity) WHERE {key}.id IN $e RETURN id(r), {key}.id, {other}.id, r.valid_from_ms, r.valid_to_ms
UNWIND $r AS x MATCH ()-[r:REL]->() WHERE id(r) = x.i SET r.valid_to_ms = x.v
```

### Agent memories

`write.py:remember` and `write.py:_agent_edge`.

```cypher
MERGE (a:Agent {id:$i}) SET a.name=$n WITH a MATCH (m:Memory {id:$m}) MERGE (a)-[:WROTE]->(m)
CREATE (:Memory {id:$id, text:$text, kind:$kind, confidence:$conf, created_ms:$t, valid_from_ms:$vf, status:'active', uses:0, last_used_ms:$t, source_id:$src, agent:$agent, project:$project, emb:vecf32($e)})
UNWIND $e AS i MATCH (m:Memory {id:$m}), (e:Entity {id:i}) CREATE (m)-[:MENTIONS {conf:1.0}]->(e)
MATCH (n:Memory {id:$n}), (o:Memory {id:$o}) CREATE (n)-[:SUPERSEDES]->(o) SET o.status='superseded', o.valid_to_ms=$t
MATCH (m:Memory {id:$m}) OPTIONAL MATCH (s:Session {id:$s}) OPTIONAL MATCH (c:Chunk {id:$s}) WITH m, coalesce(s, c) AS src WHERE src IS NOT NULL CREATE (m)-[:DERIVED_FROM]->(src)
MATCH (m:Memory {id:$m}) SET m.uses = m.uses + 1, m.last_used_ms = $t
MATCH (m:Memory)-[:MENTIONS]->(e:Entity) WHERE e.id IN $e AND m.status='active' RETURN DISTINCT m.id
```

The sixth line reinforces a near-duplicate (`uses + 1`). The seventh reads the shared-entity set used to flag conflicts (cosine 0.75 to 0.92 with a shared entity).

### Sessions

`write.py:ingest_session` (Claude Code transcripts, from the SessionEnd and PreCompact hooks).

```cypher
MERGE (s:Session {id:$s}) SET s.agent=$a, s.project=$p, s.started_ms=$t, s.path=$path, s.hash=$h WITH s MERGE (g:Agent {id:$gid}) SET g.name=$a MERGE (s)-[:BY]->(g)
```

### Handoffs

`tools.py:handoff`.

```cypher
CREATE (:Handoff {id:$i, summary:$s, tasks:$t, status:'open', created_ms:$c})
MERGE (a:Agent {id:$a}) ON CREATE SET a.name=$n WITH a MATCH (h:Handoff {id:$h}) CREATE (h)-[:{edge}]->(a)
MATCH (h:Handoff {id:$i}) SET h.status='done' RETURN h.summary
```

`{edge}` is `TO` for the recipient and `FROM` for the sender. The last line marks a handoff done.

## 3. Entity resolution

`resolve.py:resolve_entity`, `resolve_many`, `judge`, `_upgrade`, `_add_alias`. Order: exact key, alias, lone name of a unique person, then vector neighbours that pass a lexical guard.

```cypher
MATCH (e:Entity {key:$k}) RETURN e.id, e.type
MATCH (e:Entity) WHERE $k IN e.aliases RETURN e.id, e.type
MATCH (e:Entity {type:'person'}) WHERE e.key STARTS WITH $p OR e.key ENDS WITH $s RETURN e.id
CALL db.idx.vector.queryNodes('Entity','emb',4,vecf32($e)) YIELD node, score RETURN node.id, node.key, node.type, 1 - score ORDER BY score
MATCH (e:Entity) WHERE e.key IN $ks RETURN e.key
MATCH (e:Entity {id:$i}) SET e.type=$t
MATCH (e:Entity {id:$i}) WHERE e.key <> $k AND NOT $k IN e.aliases SET e.aliases = e.aliases + [$k]
```

GLiNER judgments are cached as `Judgment` nodes (`resolve.py:judge`), keyed by the content hash:

```cypher
MATCH (j:Judgment {id:$i}) RETURN j.result
MERGE (j:Judgment {id:$i}) SET j.question=$q, j.result=$r, j.created_ms=$t
```

## 4. Vector and full-text search

Vector search returns a distance: smaller is nearer (`score = 1 - cosine`), so `retrieve/channels.py:vector` sorts ascending.

```cypher
CALL db.idx.vector.queryNodes('{label}','emb',{n},vecf32($v)) YIELD node, score RETURN node.id, score
```

`{label}` is `Chunk` and `Memory` (`channels.vector`).

```cypher
CALL db.idx.fulltext.queryNodes('Entity',$q) YIELD node RETURN node.id, node.name, node.key
CALL db.idx.vector.queryNodes('Entity','emb',3,vecf32($v)) YIELD node, score RETURN node.id, node.name, score
```

The first is fuzzy name lookup (`channels.link_entities`); the second is the nearest-entity fallback in the same function.

```cypher
CALL db.idx.vector.queryNodes('Memory','emb',8,vecf32($e)) YIELD node, score RETURN node.id, node.text, score, node.status ORDER BY score
CALL db.idx.vector.queryNodes('Memory','emb',$k,vecf32($e)) YIELD node, score RETURN node.id, score
```

The first is the duplicate check in `write.py:remember`; the second is the exact top-N neighbour search in `dream.py:_neighbours`.

Entity lookup by id, key or alias, for tools (`tools.py:_resolve`; falls back to `link_entities`):

```cypher
MATCH (e:Entity) WHERE e.id=$n OR e.key=$k OR $k IN e.aliases RETURN e.id, e.name, e.type ORDER BY e.mentions DESC LIMIT 1
```

## 5. BM25 (in process, not Cypher)

`retrieve/channels.py:_bm25_index` builds a `bm25s` index over all Chunk and Memory texts. A signature query decides whether to rebuild the cached index:

```cypher
MATCH (n) WHERE n:Chunk OR n:Memory RETURN count(n), sum(size(n.text)), max(coalesce(n.date_ms, n.created_ms, 0))
MATCH (n) WHERE n:Chunk OR n:Memory RETURN n.id, n.text
```

Full rebuild on any change (O(corpus), noted in the source).

## 6. Hydrating results

`retrieve/channels.py:meta`: label, kind, date and status for ranked ids (the temporal and status filter).

```cypher
MATCH (n) WHERE (n:Chunk OR n:Memory) [AND n.id IN $ids] RETURN n.id, labels(n)[0], n.kind, coalesce(n.date_ms, n.valid_from_ms, n.created_ms), n.status
```

`retrieve/__init__.py:recall`: evidence text, source document and provenance for the final list.

```cypher
MATCH (n) WHERE (n:Chunk OR n:Memory) AND n.id IN $ids OPTIONAL MATCH (d:Document)-[:HAS_CHUNK]->(n) RETURN n.id, labels(n)[0], n.text, coalesce(n.date_ms, n.valid_from_ms, n.created_ms), n.kind, n.status, n.source_id, n.agent, n.project, d.id, d.title, d.kind, d.uri, d.author
```

## 7. Graph channel: subgraph fetch for Personalized PageRank

`retrieve/channels.py:ppr` (HippoRAG-style PPR, numpy). `link_entities` gives the seeds; the walk fetches at most 3 expansion hops and 500 nodes. `current` appends the validity condition for edges.

```cypher
MATCH (e:Entity) WHERE e.id IN $i RETURN e.id, e.name, e.mentions
MATCH (a:Entity)-[r:REL]-(b:Entity) WHERE a.id IN $ids {cond} RETURN a.id, b.id, b.name, b.mentions, r.type, coalesce(r.conf, 0.5), startNode(r).id
MATCH (n)-[m:MENTIONS]->(e:Entity) WHERE e.id IN $ids AND (n:Chunk OR n:Memory) RETURN n.id, e.id, coalesce(m.conf, 1.0) ORDER BY m.conf DESC LIMIT 3000
MATCH (n)-[m:MENTIONS]->(e:Entity) WHERE n.id IN $ids RETURN n.id, e.id, e.name, e.mentions, coalesce(m.conf, 1.0)
```

`{cond}` is `AND (r.valid_to_ms IS NULL OR r.valid_to_ms > $now)` when only current edges count, else empty. The third query caps each entity's chunks (`PER_ENT` = 25) through a source-level shortcut (a hub entity keeps its best 25 chunks by confidence, not all of them).

`channels.graph` reads the chunk-to-entity map used by the same walk:

```cypher
MATCH (n)-[m:MENTIONS]->(e:Entity) WHERE n.id IN $ids RETURN n.id, e.id, coalesce(m.conf, 1.0)
```

## 8. Shortest paths (algo.SPpaths)

`tools.py:_paths`. Used by `ask` (bridging paths between seed pairs, `count=1`, max 3 hops) and `connect` (`count=5`, `max_hops` default 4). Both directions, relationship type `REL`.

```cypher
MATCH (a:Entity {id:$a}), (b:Entity {id:$b}) CALL algo.SPpaths({sourceNode:a, targetNode:b, relTypes:['REL'], maxLen:{int(max_hops)}, relDirection:'both', pathCount:{int(count)}}}) YIELD path RETURN [x IN nodes(path) | [x.id, x.name]], [r IN relationships(path) | [r.type, startNode(r).id, r.source_id, r.valid_from_ms, r.conf]]
```

## 9. Owners and experts (variable-length paths)

`tools.py:who`. Finds people who reach the topic entity through ownership-type relations (`OWN_TYPES` = OWNS, MEMBER_OF, WORKS_ON, APPROVED, DECIDED, PART_OF), up to two hops, then ranks by path weight with document evidence.

```cypher
MATCH p=(x:Entity {type:'person'})-[:REL*1..2]->(t:Entity) WHERE t.id IN $t AND all(r IN relationships(p) WHERE r.type IN $ty) RETURN x.id, x.name, [n IN nodes(p) | [n.id, n.name]], [r IN relationships(p) | [r.type, startNode(r).id, r.source_id, r.valid_from_ms, r.conf]]
MATCH (d:Document)-[:HAS_CHUNK]->(c)-[:MENTIONS]->(t:Entity) WHERE t.id IN $t RETURN d.id, count(c)
MATCH (x:Entity {type:'person'})-[a:AUTHORED|PARTICIPATED]->(d:Document) WHERE d.id IN $d RETURN x.id, x.name, type(a), d.id, d.title, d.date_ms
```

## 10. Timeline

`tools.py:timeline`: relations, documents and memories about one entity, dated, with supersession (`SUPERSEDED on ... by`).

```cypher
MATCH (a:Entity)-[r:REL]-(b:Entity {id:$i}) RETURN a.id, a.name, r.type, startNode(r).id = a.id, r.valid_from_ms, r.source_id, r.conf
MATCH (d:Document)-[:HAS_CHUNK]->(c)-[:MENTIONS]->(e:Entity {id:$i}) RETURN d.id, d.kind, d.date_ms, d.title, count(c)
MATCH (m:Memory)-[:MENTIONS]->(e:Entity {id:$i}) WHERE m.status <> 'merged' OPTIONAL MATCH (n:Memory)-[:SUPERSEDES]->(m) WHERE n.status <> 'merged' RETURN m.id, m.kind, coalesce(m.valid_from_ms, m.created_ms), m.text, m.status, n.id, coalesce(m.valid_to_ms, n.valid_from_ms, n.created_ms)
```

## 11. Brief (session start)

`tools.py:brief`: active memories by kind (`$k` is `preference`, `decision`, `procedural`, `semantic` or `episodic`), open handoffs for the agent, and the most recent documents.

```cypher
MATCH (m:Memory {kind:$k}) WHERE m.status='active' AND ($p IS NULL OR m.project IS NULL OR m.project=$p) RETURN m.id, m.kind, coalesce(m.valid_from_ms, m.created_ms), m.agent, m.project, m.confidence, m.text, m.uses, m.status ORDER BY {order} LIMIT {n}
MATCH (h:Handoff {status:'open'}) OPTIONAL MATCH (h)-[:FROM]->(f:Agent) OPTIONAL MATCH (h)-[:TO]->(t:Agent) WITH h, f, t WHERE $a IS NULL OR t.id=$a OR t.name=$an RETURN h.id, f.name, t.name, h.created_ms, h.summary, h.tasks ORDER BY h.created_ms DESC LIMIT 10
MATCH (d:Document) WHERE d.date_ms IS NOT NULL RETURN d.id, d.kind, d.date_ms, d.title ORDER BY d.date_ms DESC LIMIT 5
```

`{order}` is `m.created_ms DESC` for episodic memories, else `coalesce(m.uses,0) DESC, coalesce(m.created_ms,0) DESC`.

## 12. Explore and ask (neighbourhood and facts)

`tools.py:explore` walks REL neighbours breadth-first, up to 3 hops:

```cypher
MATCH (a:Entity)-[r:REL]-(b:Entity) WHERE a.id IN $f RETURN a.name, b.id, b.name, b.type, r.type, startNode(r).id = a.id, r.conf, r.valid_from_ms, r.source_id
```

`tools.py:ask` pulls the relations among the entities it reached (plus owner-type edges touching the seeds):

```cypher
MATCH (a:Entity)-[r:REL]->(b:Entity) WHERE (a.id IN $i AND b.id IN $i) OR ((a.id IN $r OR b.id IN $r) AND r.type IN $ty) RETURN a.name, r.type, b.name, r.conf, r.valid_from_ms, r.source_id ORDER BY r.conf DESC LIMIT 15
```

## 13. Dream (memory consolidation)

`dream.py`. Reads once, plans in Python, then writes with `UNWIND` batches. Re-running a finished dream changes nothing.

Reads (`dream.py:_load`):

```cypher
MATCH (s:Session) RETURN s.id
MATCH (m:Memory) RETURN m.id, m.kind, m.status, m.text, m.confidence, m.created_ms, m.uses, m.last_used_ms, m.decayed_ms, m.emb
MATCH (m:Memory)-[x:MENTIONS]->(e:Entity) RETURN m.id, e.id, x.conf
MATCH (m:Memory)-[:DERIVED_FROM]->(t) RETURN m.id, t.id
MATCH (s:Memory)-[:DERIVED_FROM]->(m:Memory) RETURN s.id, m.id
MATCH (a:Memory)-[:CONFLICTS_WITH]->(b:Memory) RETURN a.id, b.id
```

Writes (`dream.py:_write`):

```cypher
UNWIND $rows AS r MATCH (d:Memory {id:r.d}), (c:Memory {id:r.c}) SET d.status='merged' CREATE (d)-[:MERGED_INTO]->(c)
UNWIND $rows AS r MATCH (c:Memory {id:r.c}) SET c.uses = c.uses + r.n
UNWIND $rows AS r MATCH (c:Memory {id:r.c}), (e:Entity {id:r.e}) CREATE (c)-[:MENTIONS {conf:r.conf}]->(e)
UNWIND $rows AS r MATCH (d:Memory {id:r})-[x:MENTIONS]->() DELETE x
UNWIND $rows AS r MATCH (c:Memory {id:r.c}), (t {id:r.t}) CREATE (c)-[:DERIVED_FROM]->(t)
UNWIND $rows AS r MATCH (d:Memory {id:r})-[x:DERIVED_FROM]->() DELETE x
CREATE (:Memory {id:$id, text:$text, kind:'semantic', confidence:$conf, created_ms:$t, valid_from_ms:$t, status:'active', uses:0, last_used_ms:$t, emb:vecf32($e)})
UNWIND $rows AS r MATCH (c:Memory {id:r.c}), (e:Entity {id:r.e}) CREATE (c)-[:MENTIONS {conf:r.conf}]->(e)
UNWIND $rows AS r MATCH (s:Memory {id:r.s}), (m:Memory {id:r.m}) CREATE (s)-[:DERIVED_FROM]->(m)
UNWIND $rows AS r MATCH (m:Memory {id:r.id}) SET m.confidence=r.conf, m.decayed_ms=r.d
UNWIND $rows AS r MATCH (a:Memory {id:r.a}), (b:Memory {id:r.b}) CREATE (a)-[:CONFLICTS_WITH {found_ms:$t}]->(b)
CREATE (:DreamRun {id:$id, at_ms:$t, merged:$merged, promoted:$promoted, decayed:$decayed, conflicts:$conflicts})
```

Lines 1 to 6 merge duplicates (the duplicate gets `status: merged`, `MERGED_INTO`, and its MENTIONS and DERIVED_FROM edges move to the canonical Memory). Lines 7 to 9 promote a recurring episode cluster to one `semantic` Memory with provenance. Line 10 writes decay and line 11 writes conflict edges; nothing is deleted. Line 12 writes one `DreamRun` per real run.

## 14. Read-only Cypher (escape hatch)

`tools.py:cypher` runs the caller's query with `GRAPH.RO_QUERY` (10 s timeout). It appends `LIMIT <limit>` when the query has none, and caps rows (500 max) and characters. Writes are rejected by the server. The MCP tool description carries the schema (`mcp_server.py:SCHEMA`).

```cypher
MATCH (n) RETURN labels(n)[0] AS label, count(n) AS n ORDER BY n DESC
```

That count query is what `neo status` runs (`cli.py:status`), through `/api/cypher`.
