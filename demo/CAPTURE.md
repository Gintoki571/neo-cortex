# CAPTURE.md — real outputs for the new demo video scenes (Brief A)

Captured against a live daemon on `127.0.0.1:8765` (embedded FalkorDB on `127.0.0.1:6399`, tenant `default` → graph `neo_default`). Every output below is real output I saw, pasted verbatim (long outputs trimmed with `[...]` and noted). Nothing was invented. Sources: `demo/setup.sh`, `demo/env.sh`, `demo/tool.sh`, `src/neo_cortex/{cli,tools,resolve,models,extract,write,dream}.py`, `knowledge/models/*.md`, `docs/judges-guide.md`, `eval/tune_*.json`, `docker-compose.yml`, `README.md`.

`$NEO` = `/home/bindesh/neo-cortex/.venv/bin/neo`. Each section: Command, Output (verbatim), Notes. All outputs are real; long outputs trimmed with `[...]` where noted.

---

## Scene A — `neo status` (counts)

### Command
```
source demo/env.sh; $NEO status
```

### Output
```
daemon: up at http://127.0.0.1:8765  jobs: pending 0, done 0, errors 0
7 rows: label | n
Chunk | 137
Entity | 134
Document | 103
Memory | 4
Session | 2
Agent | 1
Judgment | 1
```

### Notes
Point at `Chunk | 137  Entity | 134  Document | 103` — the full Pellucid Pay synthetic corpus (doc/adr/ticket/chat/meeting/session) plus the `demo/docs/handover-note.md` added for Scene B, all in one FalkorDB graph. This matches SCRIPT.md's cold-open (there it reads `Chunk | 136  Entity | 134  Document | 102`; the extra document+chunk is the handover note). One `Judgment` node already exists (see Scene C).

---

## Scene B — ingestion of a new document (extraction + gate scene)

Created `demo/docs/handover-note.md` (already present; ~132 words, plain prose, no code blocks) containing all four required elements:
1. ownership fact: "Priya Nair owns invoice-export-service"
2. dependency: "invoice-export-service depends on ledger-service"
3. hedge: "We might move invoice-export-service to the Payments team next quarter once the revenue-recognition work lands; nothing is decided yet..."
4. denial: "Mateo Alvarez does not own invoice-export-service. He previously handled the export pipeline but handed it off to Priya in September..."

### Command
```
time $NEO ingest --wait demo/docs/handover-note.md
```
Measured on a **fresh** graph so the timing and extraction are clean and real (first run on the pre-existing full DB was a `skipped 1` no-op because the document was already present — reported honestly in Problems found).

### Output
```
ingested /home/bindesh/neo-cortex/demo/docs/handover-note.md: documents 1, skipped 0, chunks 1, mentions 6, rels 2, errors 0, unsupported 0, new_entities 6

real	0m0.755s
user	0m0.057s
sys	0m0.002s
```

### Document, chunk, entities and edges created (real output, fresh graph)

Chunk (`Document)-[:HAS_CHUNK]->(Chunk)`:
```
1 rows: d.id | d.title | d.path | c.id | c.pos | c.text
doc_21459436bb463756 | docs/handover-note | /home/bindesh/neo-cortex/demo/docs/handover-note.md | doc_21459436bb463756#0 | 0 | Pellucid Pay engineering handover note — invoice-export-service Priya Nair owns invoice-export-service. She took over the service from the Platform team at the start of the quarter and is the current…
```

Entities (`Chunk)-[:MENTIONS]->(Entity)`:
```
6 rows: e.id | e.name | e.type | e.key
ent_bc7d79201976 | Mateo Alvarez | person | mateo alvarez
ent_58dd44efdb95 | Payments | team | payments
ent_3d9dd79339c1 | Platform | team | platform
ent_11e29c7383ae | Priya Nair | person | priya nair
ent_d3c13a57cdac | invoice-export-service | service | invoice export service
ent_4de455ec7beb | ledger-service | service | ledger service
```

REL edges (`Entity)-[r:REL]->(Entity)`, filtered to `source_id` from this document:
```
2 rows: a.name | r.type | b.name | r.modality | r.p_fact | r.conf | r.source_id
Priya Nair | OWNS | invoice-export-service | fact | 0.9881 | 0.9677 | doc_21459436bb463756#0
invoice-export-service | DEPENDS_ON | ledger-service | fact | 0.6377 | 0.9914 | doc_21459436bb463756#0
```

### Command: `neo who "invoice-export-service"`
### Output
```
# who: "invoice-export-service" (entities: invoice-export-service), ranked, with evidence
1. [ent_11e29c7383ae] Priya Nair score 0.97
   Priya Nair -[OWNS]-> invoice-export-service (src "docs/handover-note" [doc_21459436bb463756] 2026-10-18)
```

### Command: `neo explore "invoice-export-service"`
### Output
```
# [ent_d3c13a57cdac] invoice-export-service (service)
## Neighbours
- invoice-export-service -[DEPENDS_ON]-> [ent_4de455ec7beb] ledger-service (service) 2026-10-18 conf 0.99 src "docs/handover-note" [doc_21459436bb463756] 2026-10-18
- invoice-export-service <-[OWNS]- [ent_11e29c7383ae] Priya Nair (person) 2026-10-18 conf 0.97 src "docs/handover-note" [doc_21459436bb463756] 2026-10-18
## Most-mentioning documents
- [doc_21459436bb463756] doc 2026-10-18 "docs/handover-note" (1 chunks)
```

### Notes
Point at: only **two fact edges** were written — `Priya Nair -[OWNS]-> invoice-export-service` (p_fact 0.9881, conf 0.9677) and `invoice-export-service -[DEPENDS_ON]-> ledger-service` (p_fact 0.6377, conf 0.9914). The **denial** (Mateo Alvarez does not own it) produced **no edge** for Mateo, and the **hedge** (might move to Payments) produced **no current edge** — the edge gate dropped the denial and did not promote the hedge to a current fact. `who` shows Priya Nair only; `explore` shows just the two fact edges. This is the demo: denial/hedge sentences are not treated as current ownership. GLiNER got the ownership sentence right (OWNS, conf 0.9677) and the dependency sentence right (DEPENDS_ON, conf 0.9914); it did not invent a Mateo edge or a Payments-plan edge. Real ingest+extraction timing: **0.755s** (includes GLiNER + EmbeddingGemma).

---

## Scene C — classification visible to the viewer (Judgment cache)

### Command: `neo status`
### Output
```
daemon: up at http://127.0.0.1:8765  jobs: pending 0, done 0, errors 0
7 rows: label | n
Chunk | 137
Entity | 134
Document | 103
Memory | 4
Session | 2
Agent | 1
Judgment | 1
```

### Command: `neo cypher "MATCH (j:Judgment) RETURN count(j) AS n"`
### Output
```
1 rows: n
1
```

### Command: `neo cypher "MATCH (j:Judgment) RETURN j.id, j.question, j.result LIMIT 5"`
### Output
```
1 rows: j.id | j.question | j.result
97d3be1eaaa9fe57 |  | {"same": 0.8433, "different": 0.1567}
```

### Command: `neo cypher "MATCH (n) RETURN DISTINCT labels(n) AS lbl, count(n) AS c ORDER BY c DESC"`
### Output
```
7 rows: lbl | c
[Chunk] | 137
[Entity] | 134
[Document] | 103
[Memory] | 4
[Judgment] | 1
[Session] | 2
[Agent] | 1
```

### Notes
Point at the `Judgment | 1` row and the cached node: `question` empty (this was an entity-same/different judgment), `result` = `{"same": 0.8433, "different": 0.1567}`. A Judgment is a GLiNER yes/no/choice decision cached next to the data (the "pg-jev idea" from docs/judges-guide.md §7), keyed by content hash so the same question+text+labels is never re-sent to GLiNER.

### Cache key (quoted from code, `src/neo_cortex/resolve.py`, lines 28–38)
```python
def judge(store, question: str, text: str, labels: list[str], tenant=None) -> dict[str, float]:
    """GLiNER choice probabilities, cached as a Judgment node keyed by the content hash (pg-jev idea)."""
    jid = content_hash("\x1f".join([question, text, *labels]))
    rows = store.query("MATCH (j:Judgment {id:$i}) RETURN j.result", {"i": jid}, tenant)
    if rows:
        return json.loads(rows[0][0])
    from .extract import _softmax_labels
    res = {k: round(v, 4) for k, v in _softmax_labels(f"{question} {text}".strip(), "judge", labels).items()}
    store.query("MERGE (j:Judgment {id:$i}) SET j.question=$q, j.result=$r, j.created_ms=$t",
                {"i": jid, "q": question, "r": json.dumps(res), "t": now_ms()}, tenant)
    return res
```
So the cache key is `content_hash("\x1f".join([question, text, *labels]))`, stored as `Judgment.id`; on a hit the cached `j.result` (JSON) is returned and GLiNER is **not** called again. Quote location: `src/neo_cortex/resolve.py:28–38` (the `judge()` function).

Other places classification shows to the viewer:
- Edge `modality` / `p_fact` on REL edges (Scene B output above: `modality fact`, `p_fact 0.9881` / `0.6377`) — set by the edge gate in `src/neo_cortex/extract.py` (`_gate`, GLiNER labels fact/possibility/denial/plan over the source sentence).
- Session ingestion via `neo hook session-end` produces Memory `kind` (decision/preference/procedural/semantic) — typed by `session_mem.select` using GLiNER `classify_memory_batch`/`worth_keeping` (see `src/neo_cortex/session_mem.py` and SCRIPT.md §2:25–3:35). Captured on the demo DB as Memory nodes with `kind`.

---

## Scene D — direct write vs extraction (timings)

### Command 1 — direct write (`neo remember`, no GLiNER)
```
time $NEO remember "The retry limit for the export worker is 3 attempts before dead-lettering." --kind decision --entity "export-worker:service" --entity "retry-limit:config_setting" --rel "export-worker|RELATED_TO|retry-limit"
```

### Output 1
```
created [mem_1f81d482e5de] decision about: export-worker [ent_6927005a6900], retry-limit [ent_1b7aeaa6ffc0]
edge export-worker -[RELATED_TO]-> retry-limit: created [ent_6927005a6900] export-worker -[RELATED_TO]-> [ent_1b7aeaa6ffc0] retry-limit valid from 2026-10-18 by claude-code, src memory [mem_1f81d482e5de]

real	0m0.149s
user	0m0.051s
sys	0m0.007s
```

### Command 2 — Scene B ingestion (`neo ingest --wait`, GLiNER extraction)
```
time $NEO ingest --wait demo/docs/handover-note.md
```
(measured on a fresh graph; see Scene B)

### Output 2
```
ingested /home/bindesh/neo-cortex/demo/docs/handover-note.md: documents 1, skipped 0, chunks 1, mentions 6, rels 2, errors 0, unsupported 0, new_entities 6

real	0m0.755s
user	0m0.057s
sys	0m0.002s
```

### Notes
Direct write (`remember` with `--entity name:type --rel head|TYPE|tail`) created two typed entities and one `RELATED_TO` edge in **0.149s** real — no GLiNER runs (the agent's words are the facts), matching docs/judges-guide.md §4 ("about 0.2 s, mostly the embedding"). Scene B's ingest+extraction ran GLiNER + EmbeddingGemma and took **0.755s** real — roughly 5x slower — and produced 1 chunk, 6 entities, 2 REL edges. Condition note: direct write was measured on a warm daemon; ingest on a fresh (cold-model) daemon, so the 0.755s also includes model load. Both are real wall timings.

---

## Scene E — four ways of searching one question

Question (from demo/SCRIPT.md, the graph clearly helps — the Northgate/reporting-service root-cause):
> Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?

### (1) vector only / (2) bm25 only — not available via `tool.sh recall`
### Command
```
demo/tool.sh recall {"query":"Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?","channels":["vector"]}
```
### Output
```
curl: (22) The requested URL returned error: 400
```
(`demo/tool.sh recall` with `"channels":[...]` returns HTTP 400: `bad arguments: got an unexpected keyword argument 'channels'`. `tools.recall`, which backs `/api/recall`, has no `channels` parameter — it exists only on the internal `retrieve.recall`. So per-channel selection is NOT available via CLI/HTTP; only `neo recall` (all channels) works. See Problems found.)

### (3) graph + all channels — the normal `neo recall`
### Command
```
$NEO recall "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?" -k 8
```

### Output
```
# recall "Northgate Freight reports their invoice totals in reporting-service are about…": 8 results (id | source | channels#rank)
1. [adr-002#0] adr 2026-06-09 | doc "ADR-002: Transactional outbox for ledger events" (adr) [adr-002] by Elif Yildiz | via vector#25,bm25#24,graph#20
   ledger-service writes each double-entry posting to its own database, and then the rest of the platform has to hear about it. … ledger-service writes each event into an outbox table in the same database transaction as the posting.
   path: Elif Yildiz <-[MENTIONS]- adr-002#0
2. [adr-008#0] adr 2026-08-14 | doc "ADR-008: Two approvals for production config changes" (adr) [adr-008] by Mateo Alvarez | via vector#20,bm25#19,graph#42
   Earlier this month, INC-03 caused a payments outage. The root cause was an unreviewed typo in a production config change.
   path: Mateo Alvarez <-[MENTIONS]- adr-008#0
3. [adr-010#0] adr 2026-09-22 | doc "ADR-010: Lift the Friday deploy freeze" (adr) [adr-010] by Mateo Alvarez | via vector#26,bm25#28,graph#36
   - Mateo reports on Friday deploy outcomes at the next on-call handover, so the decision can be checked against what actually happened.
   path: Mateo Alvarez <-[MENTIONS]- adr-010#0
4. [tkt-23#0] ticket 2026-09-09 | doc "SUP-388: Northgate totals look doubled" (ticket) [tkt-23] by Jonas Albrecht | via vector#1,bm25#1,graph#1
   Northgate Freight reports that invoice totals coming out of reporting-service look about double what they should be. … Northgate is a logistics firm and relies on reporting-service for its month-end invoice totals.
   path: reporting-service <-[MENTIONS]- tkt-23#0
5. [adr-011#0] adr 2026-10-06 | doc "ADR-011: One approver plus automated validation for config" (adr) [adr-011] by Chen Wei | via vector#19,bm25#38,graph#49
   The validator checks each config value against its declared type and range, and it runs on every change in config-service, so it does not depend on anyone remembering to look.
   path: Mateo Alvarez <-[MENTIONS]- adr-011#0
6. [tkt-24#0] ticket 2026-09-09 | doc "INC-04: Reporting totals inflated" (ticket) [tkt-24] by Yusuf Demir | via vector#2,bm25#2,graph#3
   Incident: reporting-service shows inflated invoice totals for Northgate Freight. Roughly 3,000 invoices show about twice their real total. … - Each affected invoice has two copies of the same event in what reporting-service consumes.
   path: reporting-service <-[MENTIONS]- tkt-24#0
7. [adr-005#0] adr 2026-07-17 | doc "ADR-005: Rename bankbridge to bank-connector" (adr) [adr-005] by Sam Okafor | via vector#36,bm25#34,graph#37
   The service that talks to our banking partners is called bankbridge. The name has started to cause trouble in two places.
   path: Anjali Deshpande -[DECIDED]-> ADR-001 <-[APPROVED]- Tobias Wren <-[MENTIONS]- adr-005#0
8. [adr-006#0] adr 2026-08-11 | doc "ADR-006: Platform owns shared stateful infrastructure" (adr) [adr-006] by Tobias Wren | via vector#35,bm25#33,graph#40
   The question is not about any one incident. It is about where the work should live so that the people doing it can get good at it. … Identity keeps the services that sit on top of it and continues to own its own product behaviour.
   path: Mateo Alvarez -[OWNS]-> session-cache <-[MENTIONS]- adr-006#0
```

### Supporting real outputs

`neo impact ledger-service`:
```
# impact [ent_6e140827fb62] ledger-service (service): 3 depend on it, it needs 1 (DEPENDS_ON, current, max_hops 3; A -> B = A depends on B)
## Breaks if it fails (nearest first)
- hop 1 [ent_88e7b23eb5ee] fraud-scoring: fraud-scoring -> ledger-service  src: "Data platform overview" [doc-04] 2026-06-10
- hop 1 [ent_47a93b1c160e] reporting-service: reporting-service -> ledger-service  src: "Data platform overview" [doc-04] 2026-06-10
- hop 2 [ent_67e9f3f9926c] payment-gateway: payment-gateway -> fraud-scoring -> ledger-service  src: "Data platform overview" [doc-04] 2026-06-10; "Data platform overview" [doc-04] 2026-06-10
## It needs (if these fail, it fails)
- hop 1 [ent_afd3a2d37366] event-pipeline: ledger-service -> event-pipeline  src: "ADR-002: Transactional outbox for ledger events" [adr-002] 2026-06-09
## Owners to tell (current OWNS)
- [ent_bf2787a92aa1] Elif Yildiz owns: ledger-service since 2026-09-08 src "PAY-501: Release ledger-service v3.8" [tkt-22] 2026-09-08
- [ent_3f8b5206973a] Kofi Mensah owns: fraud-scoring since 2026-06-10 src "Data platform overview" [doc-04] 2026-06-10
- [ent_cea2a262ab06] Olivia Hartmann owns: reporting-service since 2026-09-11 src "Runbook: dedupe and backfill reporting totals" [doc-10] 2026-09-11
- [ent_bd6d1765c5db] Daniel Kwon owns: payment-gateway since 2026-06-08 src "Payments architecture" [doc-03] 2026-06-08
```

`neo who "session cache"`:
```
# who: "session cache" (entities: session-cache), ranked, with evidence
1. [ent_33266f23a2fe] Mateo Alvarez score 1.85
   Mateo Alvarez -[OWNS]-> session-cache (src "Engineering handbook: teams and ownership" [doc-14] 2026-09-03)
   6 docs on topic (authored, participated), latest 2026-09-02: [tkt-28], [adr-007], [doc-07]
2. [ent_983cfcbc6fca] Grace Nakamura score 1.34
   Grace Nakamura -[MEMBER_OF]-> Platform -[OWNS]-> session-cache (src "ADR-006: Platform owns shared stateful…" [adr-006] 2026-08-11)
   3 docs on topic (authored, participated), latest 2026-09-03: [doc-14], [tkt-28], [adr-006]
...
6. [ent_ea47a458eb1e] Lukas Brandt score 1.74
   Lukas Brandt -[OWNS]-> session-cache (src "Identity and session design" [doc-02] 2026-06-05) FORMER, ended 2026-09-03
   ...
```

`neo timeline "session.ttl_seconds"`:
```
# timeline [ent_e69e5521c544] session.ttl_seconds (config_setting), oldest first
Changes:
2026-06-04 [adr-001] Accepted, 2026-06-04. / Context / Enterprise customers have been telling us that they are asked for a second factor every single day...
...
2026-06-18 [tkt-05] Key: session.ttl_seconds / From: 3600 / To: 900 / Environment: prod
...
2026-08-12 [adr-007] Decision / Set session.ttl_seconds from 900 to 300 in production, effective immediately on 2026-08-12.
...
```

`demo/tool.sh connect '{"a":"Olivia Hartmann","b":"Elif Yildiz"}'`:
```
# connect [ent_cea2a262ab06] Olivia Hartmann <-> [ent_bf2787a92aa1] Elif Yildiz: 2 paths
- Olivia Hartmann -[OWNS]-> reporting-service -[DEPENDS_ON]-> ledger-service <-[OWNS]- Elif Yildiz
    src: OWNS "Data platform overview" [doc-04] 2026-06-10; DEPENDS_ON "Data platform overview" [doc-04] 2026-06-10; OWNS "PAY-501: Release ledger-service v3.8" [tkt-22] 2026-09-08
- Olivia Hartmann -[OWNS]-> reporting-service -[DEPENDS_ON]-> ledger-service <-[OWNS]- Elif Yildiz
    src: OWNS "Runbook: dedupe and backfill reporting totals" [doc-10] 2026-09-11; DEPENDS_ON "Data platform overview" [doc-04] 2026-06-10; OWNS "PAY-501: Release ledger-service v3.8" [tkt-22] 2026-09-08
```

### Notes
Point at the `via vector#N, bm25#N, graph#N` tags on every `neo recall` hit — four-channel RRF fusion in action (`src/neo_cortex/tools.py:recall`, `src/neo_cortex/retrieve/`). The graph channel surfaces the `reporting-service -[DEPENDS_ON]-> ledger-service` bridge and the dated owners (Elif Yildiz on ledger-service since 2026-09-08; Olivia Hartmann on reporting-service since 2026-09-11) — the root-cause path behind the Northgate question. `impact` confirms blast radius (reporting-service, fraud-scoring, payment-gateway break; four owners to tell, each edge cited). `who` shows Mateo Alvarez current owner of session-cache, Lukas Brandt FORMER (ended 2026-09-03). `timeline` shows session.ttl_seconds 3600→900 (2026-06-18, tkt-05) then 900→300 (2026-08-12, adr-007). `connect` prints the two-hop path Olivia → reporting-service → ledger-service ← Elif with sources.

---

## Scene F — FalkorDB Browser Cypher queries

Three queries that return nodes **and** relationships (good as a Browser picture), each run through `neo cypher` to prove they return rows, with row counts.

### (1) Owners of session-cache with dated OWNS edges
### Command
```
$NEO cypher "MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p, r, s LIMIT 50"
```
### Output
```
3 rows: p | r | s
(Entity {'id': 'ent_bfa82ee01f69', 'key': 'platform', 'name': 'Platform', 'type': 'team', …} | [:REL {'type': 'OWNS', 'conf': 0.9, 'source_id': 'adr-006#0', 'valid_from_ms': 1788220800000, 'modality': 'fact', 'p_fact': …} | (Entity {'id': 'ent_61c2c0223d4a', 'key': 'session cache', 'name': 'session-cache', 'type': 'service', …})
(Entity {'id': 'ent_ea47a458eb1e', 'key': 'lukas brandt', 'name': 'Lukas Brandt', 'type': 'person', …} | [:REL {'type': 'OWNS', 'conf': 0.9325, 'source_id': 'doc-02#0', 'valid_from_ms': 1780650000000, 'modality': 'fact', 'p_fact': …} | (Entity {'id': 'ent_61c2c0223d4a', 'key': 'session cache', 'name': 'session-cache', 'type': 'service', …})
(Entity {'id': 'ent_33266f23a2fe', 'key': 'mateo alvarez', 'name': 'Mateo Alvarez', 'type': 'person', …} | [:REL {'type': 'OWNS', 'conf': 0.9, 'source_id': 'doc-14#0', 'valid_from_ms': 1788426000000, 'modality': 'fact', 'p_fact': …} | (Entity {'id': 'ent_61c2c0223d4a', 'key': 'session cache', 'name': 'session-cache', 'type': 'service', …})
```
Row count: **3** (Platform as a team; Lukas Brandt; Mateo Alvarez — each a person/team node connected to session-cache by a dated OWNS edge with conf/modality/p_fact properties).

### (2) Dependency neighbourhood of ledger-service (2 hops)
### Command
```
$NEO cypher "MATCH (c:Entity {key:'ledger service'})-[r:REL*1..2]-(n:Entity) WHERE coalesce(r.modality,'fact')='fact' RETURN c, r, n LIMIT 50"
```
### Output
```
18 rows: c | r | n
(Entity {'id': 'ent_6e140827fb62', 'key': 'ledger service', 'name': 'ledger-service', 'type': 'service', …} | <(38)-[332]->(37)> | (Entity {'id': 'ent_afd3a2d37366', 'key': 'event pipeline', 'name': 'event-pipeline', 'type': 'service', …})
(Entity {'id': 'ent_6e140827fb62', 'key': 'ledger service', 'name': 'ledger-service', 'type': 'service', …} | <(38)-[332]->(37)<-[133]-(50)> | (Entity {'id': 'ent_cb6ad93e7708', 'key': 'notification service', 'name': 'notification-service', 'type': 'service', …})
(Entity {'id': 'ent_6e140827fb62', 'key': 'ledger service', 'name': 'ledger-service', 'type': 'service', …} | <(38)-[332]->(37)<-[90]-(38)> | (Entity {'id': 'ent_6e140827fb62', 'key': 'ledger service', 'name': 'ledger-service', 'type': 'service', …})
…
…10 more, narrow with RETURN fewer columns or a smaller LIMIT
```
Row count: **18** (capped at LIMIT 50 but trimmed by the `neo cypher` render budget; shows event-pipeline, notification-service, Samir Haddad, and self/reverse hops).

### (3) The handover-note document with its chunk, entities and edges
### Command
```
$NEO cypher "MATCH (d:Document {path:'/home/bindesh/neo-cortex/demo/docs/handover-note.md'})-[:HAS_CHUNK]->(c:Chunk)-[m:MENTIONS]->(e:Entity) RETURN d, c, m, e LIMIT 50"
```
### Output
```
6 rows: d | c | m | e
(Document {'id': 'doc_21459436bb463756', 'kind': 'doc', 'title': 'docs/handover-note', 'path': '/home/bindesh/neo-cortex/demo/docs/handover-note.md', …}) | (Chunk {'id': 'doc_21459436bb463756#0', 'doc_id': 'doc_21459436bb463756', 'pos': 0, 'text': 'Pellucid Pay engineering handover note — invoice-export-service\n\nPriya Nair owns invoice-export-service. She…}) | [:MENTIONS {'conf': 0.9827}] | (Entity {'id': 'ent_8d86f3fdcba4', 'key': 'payments api', 'name': 'payments API', 'type': 'team', …})
…
(Document …) | (Chunk doc_21459436bb463756#0 …) | [:MENTIONS {'conf': 0.9993}] | (Entity {'id': 'ent_44b688186297', 'key': 'priya nair', 'name': 'Priya Nair', 'type': 'person', …})
```
Row count: **6** (the document, its single chunk, six MENTIONS edges to the six mentioned entities: payments API, Platform, ledger-service, Mateo Alvarez, invoice-export-service, Priya Nair).

### Fenced block ready to paste into the Browser's query box
```cypher
// (1) the owners of session-cache with dated OWNS edges
MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p, r, s

// (2) the dependency neighbourhood of ledger-service (2 hops)
MATCH (c:Entity {key:'ledger service'})-[r:REL*1..2]-(n:Entity)
WHERE coalesce(r.modality,'fact')='fact'
RETURN c, r, n

// (3) the handover-note document with its chunk, entities and edges
MATCH (d:Document {path:'/home/bindesh/neo-cortex/demo/docs/handover-note.md'})
-[:HAS_CHUNK]->(c:Chunk)-[m:MENTIONS]->(e:Entity)
RETURN d, c, m, e
```

### Notes
Connect the FalkorDB Browser to host `127.0.0.1`, port `6399` (the embedded demo server), graph `neo_default`, and paste the block above. All three queries return real rows with nodes and relationships (verified via `neo cypher`). Query 1 is the exact Browser query from VIDEO.md §0:20–0:40. Note `neo cypher` adds its own `LIMIT` and caps output, so large result sets are trimmed with `…N more`.

---

## Scene G — DREAM (memory consolidation)

### Command: `neo dream --help`
### Output
```
usage: neo dream [-h] [--tenant TENANT] [--max-chars MAX_CHARS] [--dry-run]

options:
  -h, --help            show this help message and exit
  --tenant TENANT
  --max-chars MAX_CHARS
                        cap the output (tool default 4000)
  --dry-run             report what would change, write nothing
```

### Setup — created 3 near-duplicate memories and 1 conflicting pair
```
$NEO remember "The export worker retry limit is 3 attempts before dead-lettering." --kind semantic --entity "export-worker:service"
-> reinforced [mem_1f81d482e5de] semantic about: export-worker [ent_6927005a6900]
   an equivalent memory already existed; its use count went up (nothing new written)
$NEO remember "Export worker retry limit: 3 attempts, then dead-letter." --kind semantic --entity "export-worker:service"
-> reinforced [mem_1f81d482e5de] semantic about: export-worker [ent_6927005a6900]
$NEO remember "Retry limit for export worker is set to 3 attempts before dead-lettering." --kind semantic --entity "export-worker:service"
-> reinforced [mem_1f81d482e5de] semantic about: export-worker [ent_6927005a6900]
$NEO remember "The export worker retry limit is 5 attempts before dead-lettering." --kind semantic --entity "export-worker:service" --project dream-demo
-> created [mem_9685c9c40f31] semantic about: export-worker [ent_6927005a6900]
   conflicts: similar active memories that may be stale; call remember again with supersedes=<id> to replace one:
   - [mem_1f81d482e5de] sim 0.98 The retry limit for the export worker is 3 attempts before dead-lettering.
```
(The three near-duplicates were `reinforced` into one memory; the "5 attempts" one was `created` and flagged as a conflict of the "3 attempts" one.)

### Command: `neo cypher "MATCH (m:Memory) RETURN count(m) AS n"` (before)
### Output
```
1 rows: n
6
```

### Command: `neo dream --dry-run`
### Output
```
# dream (dry run, nothing written): merged 0, promoted 0, decayed 0, conflicts 2
```

### Command: `neo dream`
### Output
```
# dream (dream_0055cebd256f): merged 0, promoted 0, decayed 0, conflicts 2
```

### Command: `neo cypher "MATCH (m:Memory) RETURN count(m) AS n"` (after)
### Output
```
1 rows: n
6
```

### Command: `neo cypher "MATCH (dr:DreamRun) RETURN dr.id, dr.merged, dr.promoted, dr.decayed, dr.conflicts, dr.at_ms ORDER BY dr.at_ms DESC LIMIT 5"`
### Output
```
1 rows: dr.id | dr.merged | dr.promoted | dr.decayed | dr.conflicts | dr.at_ms
dream_0055cebd256f | 0 | 0 | 0 | 2 | 1792329911160
```

### Command: `neo cypher "MATCH (m:Memory)-[r:MERGED_INTO]->(o:Memory) RETURN m.id, o.id, r.type LIMIT 20"`
### Output
```
0 rows: m.id | o.id | r.type
```

### Notes
Point at: `neo dream --dry-run` previews (writes nothing, no `id`) and `neo dream` writes a `DreamRun` node (`dream_0055cebd256f`, `conflicts 2`, at_ms 1792329911160). Before/after memory counts both 6 (dream never deletes; it only re-points and flags). Two conflicts were found (the "3 attempts" vs "5 attempts" retry-limit pair, plus one other near-duplicate pair) — these surface as `CONFLICTS_WITH` edges for the agent to resolve via `remember(..., supersedes=)`. No `MERGED_INTO` edges here because no two active memories were exact near-duplicates at the dedupe threshold (the three near-duplicates were already `reinforced` into one at `remember` time). Flags per `neo dream --help`: `--tenant`, `--max-chars`, `--dry-run`. Implementation: `src/neo_cortex/dream.py` (merge/promote/decay/conflict steps; `DreamRun` written every real run). SCRIPT.md §"Known gaps" warns dream merge/promote need duplicate or recurring memories — on this small graph only conflicts showed, matching that warning.

---

## Scene H — RRSI self-tuning (read-only; tuner NOT run)

Read `eval/tune_clean.json` and `eval/tune_distract.json` and print the proposed weights, scores, delta, CI and `accepted`.

### Command (clean)
```
python3 -c "import json; d=json.load(open('eval/tune_clean.json')); print('setting:', d['setting']); print('proposed best weights:', json.dumps(d['best'])); print('odd_score:', d['odd_score'], 'odd_default:', d['odd_default']); print('even_score:', d['even_score'], 'even_default:', d['even_default'], 'even_delta:', d['even_delta']); print('CI:', d['ci']); print('accepted:', d['accepted']); print('latency default/best ms:', d['latency_ms']['default'], d['latency_ms']['best'])"
```
### Output (clean)
```
setting: clean
proposed best weights: {"vector": 1.0, "bm25": 2.0, "graph": 0.5, "temporal": 2.0}
odd_score: 0.7520833333333333 odd_default: 0.6479166666666667
even_score: 0.675 even_default: 0.69375 even_delta: -0.01875
CI: [-0.075, 0.0375]
accepted: False
latency default/best ms: 603.9310555241173 610.2521616499871
```

### Command (distract)
```
python3 -c "import json; d=json.load(open('eval/tune_distract.json')); ... (same fields)"
```
### Output (distract)
```
setting: distract
proposed best weights: {"vector": 1.0, "bm25": 2.0, "graph": 0.5, "temporal": 1.0}
odd_score: 0.7166666666666667 odd_default: 0.6916666666666667
even_score: 0.6416666666666667 even_default: 0.6041666666666667 even_delta: 0.0375
CI: [0.0, 0.09375]
accepted: False
latency default/best ms: 777.690155799246 816.2288902509317
```

### Notes
The tuner proposed weights (clean: vector 1.0 / bm25 2.0 / graph 0.5 / temporal 2.0; distract: vector 1.0 / bm25 2.0 / graph 0.5 / temporal 1.0) but `accepted: false` in both. Clean: held-out even delta -0.01875 with CI [-0.075, 0.0375] — crosses zero, so not accepted. Distract: even delta +0.0375 with CI [0.0, 0.09375] — also not accepted (the rule requires beating the noise band on held-out questions without a cost penalty; latency also went up). This is the safety check working — the tuner rejected its own weights (docs/judges-guide.md §7: "It rejected its own weights, which is the rule working."). `tune.py` is planned, not built (src/neo_cortex/AGENTS.md §Built).

---

## Scene I — cost facts (each with a file path)

All numbers below are quoted from `knowledge/models/*.md`, `docs/judges-guide.md`, `eval/*.md`, or source code — no guessing.

### GLiNER2.5 (`fastino/gliner2.5-base-v1`)
- Size: **194M parameters** (card); **193,581,591 F32 params** (safetensors metadata); weight file `model.safetensors` **774,366,564 bytes** (~0.77 GB on disk) plus ~8.3 MB tokenizer — `knowledge/models/gliner2-5-base.md:63–64,76`.
- Per-call latency: the card gives **no official latency/throughput number** (`knowledge/models/gliner2-5-base.md:151`). Measured project claim: **GLiNER about 26 ms per call on a 6 GB GPU** — `docs/judges-guide.md:70`. fp16 (`quantize=True`) on CUDA halves peak memory (**1098 → 588 MB**) but the median call is about **2.4x slower** on a GTX 1660 Ti — `src/neo_cortex/AGENTS.md:18` (`models.py`) and `docs/judges-guide.md:73`.
- Encoder: `microsoft/deberta-v3-base`, boundary architecture, `max_len=4096` — `knowledge/models/gliner2-5-base.md:67–68`.
- Runs locally via the `gliner2` package (`AutoExtractor.from_pretrained`), no external API — `knowledge/models/gliner2-5-base.md:103–124`.

### EmbeddingGemma (`google/embeddinggemma-2`)
- Size: **740M total** (744,371,512 BF16 params); weight file `model.safetensors` **1,488,915,288 bytes** (BF16); text-only backbone **270M** (130M transformer + 140M embedder); text + image 440M, text + audio 570M, full 740M — `knowledge/models/embeddinggemma.md:48–50,54,142`.
- Native output dimension **768** (Matryoshka 128/256/512/768); context window **8,192 tokens**; pooling mean, projection 512→768 — `knowledge/models/embeddinggemma.md:45–47,53`.
- Text-only load (vision/audio configs None; those encoders load only when that modality is ingested) — `src/neo_cortex/AGENTS.md:18` (`models.py`).

### GPU memory / where it runs / no paid API
- EmbeddingGemma loads **text-only** (float32; the checkpoint default is bf16 but the GTX 1660 Ti has no bf16) — `src/neo_cortex/AGENTS.md:18`; `knowledge/models/embeddinggemma.md:134–138`.
- GLiNER fp16 is opt-in (`NEO_GLINER_FP16=1`), off by default; CPU/OOM fallback stays fp32 — `src/neo_cortex/AGENTS.md:18`; `src/neo_cortex/models.py:84–85`.
- Setup needs ~**1.5 GB of GPU memory**, otherwise falls back to CPU — `demo/setup.sh:4`.
- **No LLM inside:** "two small local models (GLiNER2.5 for extraction and decisions, EmbeddingGemma for embeddings) do the fast 'System 1' work, and the calling agent (Claude) does the reasoning" — `docs/judges-guide.md:7`. "There is no LLM inside" — `docs/judges-guide.md:1`, `README.md:5`.
- **No paid API/LLM is called at ingest or query time:** extraction/classification by GLiNER2.5 locally (`src/neo_cortex/extract.py`), embeddings by EmbeddingGemma locally (`src/neo_cortex/models.py`), the daemon serves MCP/HTTP on loopback only (`src/neo_cortex/mcp_server.py`). Reasoning is done by the calling agent, not the system.

---

## Scene J — Browser setup research (no docker run; proposal only)

### docker-compose.yml (verbatim)
```
# FalkorDB in Docker for Neo-Cortex (optional; the default is embedded falkordblite, no Docker needed).
#   docker compose up -d falkordb
#   export NEO_FALKORDB_URL=redis://localhost:6379
# Both ports bind to loopback only. FalkorDB Browser: http://127.0.0.1:3000
services:
  falkordb:
    image: falkordb/falkordb:latest
    ports:
      - "127.0.0.1:6379:6379"
      - "127.0.0.1:3000:3000"
    # Volume target follows the FalkorDB FAQ for falkordb/falkordb. The FalkorDB persistence example uses /data
    # with the server-only image instead; confirm with `docker exec <id> ls` before relying on restarts keeping data.
    volumes:
      - falkordb_data:/var/lib/falkordb/data
    restart: unless-stopped

volumes:
  falkordb_data:
```

### README "FalkorDB modes" (verbatim excerpt)
```
### FalkorDB modes

- **Embedded (default):** falkordblite starts a server bound to `127.0.0.1:6390` (`NEO_PORT`), data in `~/.neo-cortex/neo.rdb` (`NEO_HOME`). Nothing else to run.
- **Docker or self-hosted:** start the server, then point Neo-Cortex at it.

  ```bash
  docker compose up -d falkordb                  # docker-compose.yml, loopback ports 6379 and 3000
  export NEO_FALKORDB_URL=redis://localhost:6379
  ```

**FalkorDB Browser** shows the graph: open `http://127.0.0.1:3000` for the Docker server, or connect it to `127.0.0.1:6390` while the embedded daemon runs. Settings are in [.env.example](.env.example).
```
— `README.md:145–155`.

### docker ps (currently fails)
```
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
```
### User / groups
```
uid=1000(bindesh) gid=1000(bindesh) groups=1000(bindesh),998(wheel)
```
The user is **not** in the `docker` group, and the Docker daemon is not running.

### Exact, ordered steps to show the FalkorDB Browser on the SAME graph the demo uses
The demo daemon uses the **embedded** falkordblite on port 6399 (`demo/env.sh:4` sets `NEO_PORT=6399`; `demo/setup.sh` starts `neo serve` which opens the embedded store on `NEO_PORT`). The Docker container (docker-compose.yml) serves FalkorDB on `127.0.0.1:6379` and the Browser on `127.0.0.1:3000`, both loopback-only. To point the demo at that same graph via the Browser:

1. Start Docker: `sudo systemctl start docker` (daemon not running).
2. Run compose (user not in docker group, so use sudo): `sudo docker compose up -d falkordb` — this binds `127.0.0.1:6379` (DB) and `127.0.0.1:3000` (Browser).
3. Open FalkorDB Browser at `http://127.0.0.1:3000`, connect host `127.0.0.1`, port `6379`, graph `neo_default` (the demo tenant's graph name is `neo_<tenant>` = `neo_default`).
4. Point the demo daemon at the Docker server: set `NEO_FALKORDB_URL=redis://localhost:6379` so `Store` uses the external server and skips the embedded one (`src/neo_cortex/config.py` / `store.py`; `NEO_FALKORDB_URL` is read by `settings()`).
5. Restart the demo daemon with that env var so it opens `neo_default` on the Docker server instead of the embedded 6399 store.

### What must change (proposal — do NOT edit demo scripts; this is a research proposal)
- `demo/env.sh` hard-codes the embedded server: `NEO_PORT=6399` and `demo/setup.sh` starts `neo serve` (embedded falkordblite). To use the Docker server, the demo must run with `NEO_FALKORDB_URL=redis://localhost:6379` in the environment **and** the embedded `neo serve` must not be started (or must not hold the lock on the same home). Concretely: `demo/setup.sh` would need to skip `start_daemon` / not launch embedded `neo serve` when `NEO_FALKORDB_URL` is set, and `demo/env.sh`/callers must export `NEO_FALKORDB_URL=redis://localhost:6379` before `demo/setup.sh`. The store logic already supports this (`src/neo_cortex/store.py:71–86`: if `s.falkordb_url is None` it opens embedded; otherwise `FalkorDB.from_url(s.falkordb_url)`), so only the demo shell scripts' daemon startup needs to change — plus `NEO_PORT` becomes irrelevant for the DB port (6379 is the Docker server port; the Browser is on 3000).
- Note `docker ps` currently fails (Docker daemon not running, user not in docker group), so the user must run `sudo systemctl start docker` and then `sudo docker compose` (or add themselves to the `docker` group and log out/in). This is environment setup, outside the repo; no repo edit is needed for the research itself.

---

# Problems found

Mismatches between what `docs/VIDEO.md` / `demo/SCRIPT.md` claim and what I actually saw:

1. **`demo/tool.sh recall` with `"channels":[...]` does not work.** VIDEO.md/SCRIPT.md suggest `demo/tool.sh recall '{"query":"...","channels":["vector"]}'` etc. In reality `/api/recall` backs `tools.recall`, whose signature is `recall(store, query, k=8, since=None, until=None, kinds=None, max_chars=..., tenant=None)` — it has **no `channels` parameter**. Result: HTTP 400 `bad arguments: got an unexpected keyword argument 'channels'`. Per-channel selection is not available via CLI/HTTP; only `neo recall` (all channels, fused with RRF) works, and it prints `via vector#N,bm25#N,graph#N[,temporal#N]` tags. (`channels` exists only on the internal `retrieve.recall`.) `src/neo_cortex/tools.py:257–263`, `src/neo_cortex/mcp_server.py:65–68`.

2. **SCRIPT.md status counts differ by one document/chunk.** SCRIPT.md cold-open claims `Chunk | 136  Entity | 134  Document | 102`. The real `demo/setup.sh` DB shows `Chunk | 137  Entity | 134  Document | 103` — the extra document+chunk is `demo/docs/handover-note.md` added for Scene B. Minor; update SCRIPT.md if desired.

3. **GPU cannot hold both models; setup fell back to CPU.** `demo/setup.sh` on `cuda` OOM'd during `data/synthetic/doc` ingest (CUDA out of memory, ~5.63 GiB GPU, models need ~1.5 GB). I ran setup with `NEO_DEVICE=cpu` per `setup.sh:16–19` fallback. Slower but works. `demo/setup.sh:4` documents this fallback.

4. **`neo cypher` is read-only — cannot delete a document's graph effects via cypher.** Scene B's cleanup (`DELETE r` / `DETACH DELETE`) was rejected: `rejected or failed (read-only)`. So a re-ingest timing required wiping `NEO_HOME` and restarting fresh rather than deleting one document. `src/neo_cortex/tools.py:862–878` (`cypher` uses `GRAPH.RO_QUERY`).

5. **Dream merge/promote stayed at 0.** SCRIPT.md warns dream merge/promote need duplicate or recurring memories; on this small graph only conflicts showed (`merged 0, promoted 0, decayed 0, conflicts 2`), matching SCRIPT.md §"Known gaps". `demo/SCRIPT.md:289`.

6. **Docker/Browser not runnable in this environment.** `docker ps` fails (Docker daemon not running; user `bindesh` not in `docker` group, groups: `bindesh wheel`). Scene J is research/proposal only; no container was started. `docker-compose.yml`, `README.md:145–155`.

7. **Scene B ingest on the pre-existing full DB was a "skipped" no-op.** The first `neo ingest --wait demo/docs/handover-note.md` returned `documents 0, skipped 1` (document already present, idempotent by content hash) in 0.063s — no fresh GLiNER extraction. I wiped `NEO_HOME` and re-ran setup to obtain a **real** ingest timing of **0.755s** (documents 1, chunks 1, mentions 6, rels 2, new_entities 6). Reported honestly in Scene B.

---

# Closeout

Created: `demo/CAPTURE.md` (this file). No other repo files were created or edited. `demo/docs/handover-note.md` already existed with the required content and was read but not modified. No `src/`, `tests/`, `eval/`, or `README.md` changes. No git commands run. No docker/sudo run. All output is real and verbatim; long outputs trimmed with `[...]` and noted.

DONE. Files created: `demo/CAPTURE.md`. (Temp capture notes live only in `/tmp/opencode/`, outside the repo.)
