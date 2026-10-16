# neo_cortex

## Purpose

- The Neo-Cortex Python package: embedded/external FalkorDB store, schema, local models (GLiNER2.5 extraction/classification, EmbeddingGemma embeddings), and later the memory/retrieval/MCP layers.
- Design rules come from `knowledge/architecture/unified-plan.md`: no LLM inside the system; hybrid retrieval fused with RRF.

## Ownership

- Owns everything under `src/neo_cortex/`. Tests (`tests/`), `scripts/` and `pyproject.toml` at the repo root support this package and follow this doc.

## Local Contracts

Built (Phase 0 and the Phase 1 write path):
- `config.py`: `settings()` reads env at call time. `NEO_HOME` (default `~/.neo-cortex`, holds `neo.rdb`), `NEO_FALKORDB_URL` (if set, use that server and skip the embedded one), `NEO_PORT` (6390), `NEO_TENANT` (`default`), `NEO_DEVICE` (`auto` = cuda if available), `NEO_GLINER`, `NEO_EMBED` (repo-local model dir if present, else the Hub id). Default model dirs resolve against the repo root (`config.ROOT`), never the cwd.
- `store.py`: `Store` (context manager). Embedded falkordblite listens on TCP `127.0.0.1:NEO_PORT` only (redislite defaults to all interfaces, so `bind` is always passed). `graph(tenant)` returns graph `neo_<tenant>` and runs `ensure_schema` once per tenant; `query(cypher, params, tenant)` returns `result_set`. `close()` shuts the embedded server down unconditionally (redislite's own close skips it while another client such as FalkorDB Browser is attached) and waits for the pid; it takes about 3 s because the server module teardown is slow. Close every `Store` before exit, otherwise an orphan `redis-server` stays.
- `schema.py`: `ensure_schema(graph)` is idempotent. Vector indexes (768, cosine) on `Memory/Chunk/Entity.emb`, full-text on `Entity.name` (fuzzy name lookup only, it is not BM25), range indexes on `id` for Memory/Chunk/Entity/Document/Session/Agent/Handoff/Judgment, plus `Entity.key`, `Entity.type`, `Memory.created_ms`, `Memory.valid_from_ms`, `Chunk.date_ms`, `Document.date_ms`. Only "already indexed" errors are swallowed.
- `models.py`: lazy thread-safe singletons. `gliner()`; `embed_docs(texts, titles=None)` uses `title: {title or 'none'} | text: {text}`; `embed_query(text)` uses the `SearchQuery` prompt; both return float32 L2-normalized 768-d. Text-only load (vision/audio configs None, pillow + torchvision must still be installed). The model is forced to float32 (the checkpoint default is bf16, which gives unit norms of about 1.003 and the GTX 1660 Ti has no bf16). `embed_images(paths)` lazily loads a separate full model.
- `util.py`: `new_id(prefix)`, `now_ms()`, `content_hash(text)`, `normalize_key(name)` (the Entity.key rule).
- `cli.py`: `neo --version`; `neo ingest PATH`, `neo ingest-session JSONL`, `neo remember TEXT [--kind --about --supersedes --agent --project]`, each with `--tenant`; prints compact JSON. More subcommands arrive with the MCP tools.
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

### Module APIs

Contract refinements made while building the write path (the model above stays authoritative; these are additions):

- `Entity.aliases` holds normalised keys (not display names). `Session` also carries `hash` (transcript content hash, idempotence).
- `Chunk.id` is `<doc id>#<pos>`; `Document.id` is the frontmatter `id` (else a hash of the path). `REL.source_id` is the chunk id (or none for hand-written edges); `REL.valid_from_ms` is the document date.
- `Entity.mentions` counts MENTIONS edges from Chunks and Memories; `first_seen_ms`/`last_seen_ms` come from the mentioning chunks' document dates. They are recomputed for every entity an ingest touches.
- Entity types: GLiNER's type for a key is the highest `resolve._RANK` seen (person > team > customer > service > ticket/incident/decision > tool > config_setting/file > component/product > other). Any DEPENDS_ON endpoint becomes `service`.

- `extract.py`: `ENTITY_LABELS` / `REL_LABELS` map descriptive GLiNER labels to contract types (`RELATED_TO` is whitelisted but never extracted). `extract(text) -> {"entities": [{name, type, conf}], "relations": [{head, type, tail, conf}]}`, `extract_batch(texts)` (batched, long texts split by the library at 384 words), `classify_memory(text) -> (kind, conf)`, `worth_keeping(text) -> float` plus `_batch` forms. Choices that matter: classification labels are long descriptive phrases and the full softmax distribution is read (`multi_label=True, cls_threshold=0, class_act="softmax"`); `worth_keeping` is GLiNER label mass nudged by surface cues (the base model alone was about 70% right on a 16-sentence probe). Entity confidence floors are per type (person 0.6 up to 0.85 for component/product/decision), relation floors 0.6 (PART_OF/WORKS_ON 0.7). Junk filter: stop-list, more than 4 words, and for fuzzy types (component, config_setting, other, product, team, customer, decision, incident) a proper-noun shape (capital letter or `- _ . /` or digit). Ticket/ADR/INC ids are regex-extracted and override GLiNER's type. Relations need both ends among the surviving entities and obey head/tail type constraints (`REL_TYPES`). Markdown tables with an `Owner` column yield OWNS edges at conf 0.9.
- `resolve.py`: `resolve_entity(store, name, type, emb=None, tenant=None) -> id | None` (None only for an ambiguous lone surname), `resolve_many(store, [(name, type)])` (batches the embeddings), `judge(store, question, text, labels, tenant=None) -> {label: prob}` cached as `Judgment` (id = content hash). Order: exact key, alias, lone first/last name of a unique person, Entity vector neighbours (similarity = 1 - distance, at least 0.85) that pass a lexical guard (same words up to plurals, or a tail/head name part, equal digits, person names never fuzzy-merge); at or above 0.92 merge, between 0.85 and 0.92 the judge may only veto (`same` below 0.5). GLiNER2.5-base is close to chance as a same-entity judge on bare names, so it is never trusted to create a merge.
- `write.py`: `ingest_path(store, path, tenant=None) -> {documents, skipped, chunks, mentions, rels, errors, unsupported, new_entities}`; `chunk_text(body, kind)`; `remember(...) -> {id, status: created|reinforced, kind, entities, conflicts: [{id, text, sim}]}` (extra optional arg `confidence`; cosine at or above 0.92 reinforces, 0.75 to 0.92 with a shared entity is a conflict, `supersedes` skips dedupe, links SUPERSEDES and retires the old memory); `ingest_session(store, transcript_path, agent="claude-code", project=None, tenant=None)`. Documents: frontmatter per `data/synthetic/WORLD.md` section 0; chunks of 120 to 250 words on paragraph boundaries (chats on message boundaries); unchanged hash is skipped, a changed one is replaced; non-markdown goes through `anydoc.to_markdown`; images are skipped. Sessions: user and assistant text blocks only (meta, sidechain, tool traffic, code fences, system tags dropped), at most 600 unique segments scored, the best 15 with `worth_keeping >= 0.6` become Memories (`DERIVED_FROM` the Session, `(Session)-[:BY]->(Agent)`, `(Agent)-[:WROTE]->(Memory)`); an unchanged transcript is skipped, a grown one adds new memories without bumping `uses` on ones already derived from it.
- `retrieve/`: channel functions return ranked `[(node_id, score)]`; `rrf(lists, weights, k=60)`; `parse_query(q) -> {entities, intent: {label: conf}, since_ms, until_ms}`; `recall(store, query, k=8, since_ms=None, until_ms=None, kinds=None, weights=None, tenant=None) -> [{id, label, text, score, channels: {name: rank}, source, date_ms}]`.

Planned (not built): full `cli.py`, `dream.py`, `tune.py`.

## Work Guidance

- Python 3.12 only (`uv`), src layout. Use `uv run`.
- Check real library source (opensrc) before using an API; spike facts are in `knowledge/architecture/spike-2026-10-16.md`.
- Keep modules small; add abstractions only when two callers need them.

## Verification

- `uv run pytest -q`: store open/close with no orphan, loopback bind, schema idempotence, vector round trip, tenant isolation (port from `NEO_TEST_PORT`, default 6391).
- `tests/test_tools.py` (hand-built contract graph, fake models) and `tests/test_mcp.py` (in-process client, plus an HTTP daemon subprocess stopped by SIGTERM/SIGINT with an orphan check by DB port; `NEO_TEST_PORT` base +20/+21).
- Write-path tests use fake model functions (bag-of-words embeddings, regex extraction) so they run offline; the real-model checks are in `tests/test_write_slow.py`.
- `NEO_SLOW=1 uv run pytest -q`: also loads GLiNER and EmbeddingGemma.
- `uv run python scripts/bench_models.py`: model latency on the configured device.

## Child DOX Index

- None.
