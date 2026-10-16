# neo_cortex

## Purpose

- The Neo-Cortex Python package: embedded/external FalkorDB store, schema, local models (GLiNER2.5 extraction/classification, EmbeddingGemma embeddings), and later the memory/retrieval/MCP layers.
- Design rules come from `knowledge/architecture/unified-plan.md`: no LLM inside the system; hybrid retrieval fused with RRF.

## Ownership

- Owns everything under `src/neo_cortex/`. Tests (`tests/`), `scripts/` and `pyproject.toml` at the repo root support this package and follow this doc.

## Local Contracts

Built (Phase 0):
- `config.py`: `settings()` reads env at call time. `NEO_HOME` (default `~/.neo-cortex`, holds `neo.rdb`), `NEO_FALKORDB_URL` (if set, use that server and skip the embedded one), `NEO_PORT` (6390), `NEO_TENANT` (`default`), `NEO_DEVICE` (`auto` = cuda if available), `NEO_GLINER`, `NEO_EMBED` (repo-local model dir if present, else the Hub id).
- `store.py`: `Store` (context manager). Embedded falkordblite listens on TCP `127.0.0.1:NEO_PORT` only (redislite defaults to all interfaces, so `bind` is always passed). `graph(tenant)` returns graph `neo_<tenant>` and runs `ensure_schema` once per tenant; `query(cypher, params, tenant)` returns `result_set`. `close()` shuts the embedded server down unconditionally (redislite's own close skips it while another client such as FalkorDB Browser is attached) and waits for the pid; it takes about 3 s because the server module teardown is slow. Close every `Store` before exit, otherwise an orphan `redis-server` stays.
- `schema.py`: `ensure_schema(graph)` is idempotent. Vector indexes (768, cosine) on `Memory/Chunk/Entity.emb`, full-text on `Entity.name` (fuzzy name lookup only, it is not BM25), range indexes on `id` for Memory/Chunk/Entity/Document/Session/Agent/Person, `Entity.key`, `Memory.created_at`, `Memory.valid_from`. Only "already indexed" errors are swallowed.
- `models.py`: lazy thread-safe singletons. `gliner()`; `embed_docs(texts, titles=None)` uses `title: {title or 'none'} | text: {text}`; `embed_query(text)` uses the `SearchQuery` prompt; both return float32 L2-normalized 768-d. Text-only load (vision/audio configs None, pillow + torchvision must still be installed). The model is forced to float32 (the checkpoint default is bf16, which gives unit norms of about 1.003 and the GTX 1660 Ti has no bf16). `embed_images(paths)` lazily loads a separate full model.
- `util.py`: `new_id(prefix)`, `now_ms()`, `content_hash(text)`.
- `cli.py`: stub, `neo --version` only.
- Data conventions: times are epoch-ms ints (no `datetime()` in falkordblite Cypher); vector `score` from `queryNodes` is a distance (smaller is nearer).

### Graph data model (binding for every module; change it here first)

All nodes carry `id` (str). Times are `*_ms` epoch-ms ints. Each tenant is its own graph, so there is no tenant property.

- `Document {id, kind: doc|adr|ticket|chat|meeting|session|file, title, uri, path, author, date_ms, status, labels: [str], hash}`
- `Chunk {id, doc_id, pos, text, kind, date_ms, emb}`: `kind` and `date_ms` are copied from the Document. The date is the *document* date, not the ingest time.
- `Entity {id, key, name, type, aliases: [str], emb, first_seen_ms, last_seen_ms, mentions}`: every named thing, people included (`type: person`). `key` is the normalised name (lowercase, collapsed whitespace and punctuation). Types: person, team, service, component, file, config_setting, ticket, customer, product, tool, incident, decision, other.
- `Memory {id, text, kind: episodic|semantic|procedural|preference|decision, confidence, created_ms, valid_from_ms, valid_to_ms, status: active|superseded, uses, last_used_ms, source_id, agent, project, emb}`
- `Session {id, agent, project, started_ms, path}`, `Agent {id, name}`, `Handoff {id, summary, tasks: [str], status: open|done, created_ms}`
- `Judgment {id (= content hash), question, result (json str), created_ms}`: cache for GLiNER yes/no or choice decisions.

Edges:

- `(Document)-[:HAS_CHUNK]->(Chunk)`; `(Chunk|Memory)-[:MENTIONS {conf}]->(Entity)`
- `(Entity)-[:REL {type, conf, source_id, valid_from_ms}]->(Entity)`. `type` is upper snake from a whitelist: OWNS, MEMBER_OF, DEPENDS_ON, CAUSED_BY, FIXED_BY, APPROVED, DECIDED, PART_OF, WORKS_ON, REPORTED, REPLACED_BY, RENAMED_TO, RELATED_TO. It is one relationship type with a `type` property, so Cypher never builds types from strings.
- `(Entity {type:'person'})-[:AUTHORED]->(Document)`, `-[:PARTICIPATED]->(Document)`
- `(Memory)-[:DERIVED_FROM]->(Chunk|Session)`, `(Memory)-[:SUPERSEDES]->(Memory)`, `(Agent)-[:WROTE]->(Memory)`, `(Session)-[:BY]->(Agent)`, `(Handoff)-[:FROM]->(Agent)`, `(Handoff)-[:TO]->(Agent)`

### Module APIs (Phase 1 and 2)

- `extract.py`: GLiNER label sets with descriptions. `extract(text) -> {"entities": [{name, type, conf}], "relations": [{head, type, tail, conf}]}`, `classify_memory(text) -> (kind, conf)`, `worth_keeping(text) -> float`.
- `write.py`: `remember(store, text, kind=None, about=None, supersedes=None, agent=None, project=None, source_id=None, tenant=None) -> {id, status: created|reinforced, kind, entities, conflicts: [{id, text, sim}]}`; `ingest_path(store, path, tenant=None) -> counts` (a file or a directory; markdown with YAML frontmatter natively, other formats through anydoc); `ingest_session(store, transcript_path, agent="claude-code", project=None, tenant=None) -> counts` (Claude Code JSONL transcript to Session plus auto-extracted Memories).
- `resolve.py`: `resolve_entity(store, name, type, emb=None) -> entity id` (exact key, then alias, then vector nearest neighbour plus a cached GLiNER judge for borderline pairs); `judge(store, question, text, labels) -> {label: prob}`, cached as `Judgment`.
- `retrieve/`: channel functions return ranked `[(node_id, score)]`; `rrf(lists, weights, k=60)`; `parse_query(q) -> {entities, intent: {label: conf}, since_ms, until_ms}`; `recall(store, query, k=8, since_ms=None, until_ms=None, kinds=None, weights=None, tenant=None) -> [{id, label, text, score, channels: {name: rank}, source, date_ms}]`.

Planned (not built): `tools.py`, `mcp_server.py` (`from mcp.server.mcpserver import MCPServer`), full `cli.py`, `dream.py`, `tune.py`.

## Work Guidance

- Python 3.12 only (`uv`), src layout. Use `uv run`.
- Check real library source (opensrc) before using an API; spike facts are in `knowledge/architecture/spike-2026-10-16.md`.
- Keep modules small; add abstractions only when two callers need them.

## Verification

- `uv run pytest -q`: store open/close with no orphan, loopback bind, schema idempotence, vector round trip, tenant isolation (uses port 6391).
- `NEO_SLOW=1 uv run pytest -q`: also loads GLiNER and EmbeddingGemma.
- `uv run python scripts/bench_models.py`: model latency on the configured device.

## Child DOX Index

- None.
