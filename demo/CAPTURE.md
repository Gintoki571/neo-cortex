# Neo-Cortex Demo Capture — Brief A

Real outputs captured against a fresh `demo/setup.sh` database (embedded FalkorDB on 127.0.0.1:6399, daemon on 127.0.0.1:8765, tenant `default` = graph `neo_default`), run on the GPU (`nvidia-smi` showed ~90 MiB baseline; models loaded ~1959 MiB GPU). `source demo/env.sh` then `$NEO` (= `.venv/bin/neo`) for every command. Only `demo/CAPTURE.md` and files under `demo/docs/` were created or edited; `src/`, `tests/`, `eval/`, README untouched. No git commands. No `data/synthetic/WORLD.md` ingested. Loopback only. One heavy job at a time on the GPU. Outputs are real and verbatim (long outputs trimmed with "[...]" and noted).

---

## Scene A — `neo status` (counts)

Command:
```
source demo/env.sh; $NEO status
```
Output:
```
daemon: up at http://127.0.0.1:8765  jobs: pending 0, done 0, errors 0
7 rows: label | n
Chunk | 136   Entity | 134   Document | 102   Memory | 4   Session | 2   Agent | 1
```
Notes: Matches `demo/SCRIPT.md` "Cold open" exactly (`Chunk | 136 Entity | 134 Document | 102 ...`). Counts vary slightly run to run (entity id hashing); this run matches the script's verified numbers. Point at `Chunk | 136  Entity | 134  Document | 102` — one FalkorDB graph holding the synthetic company's docs/tickets/ADRs/chats/sessions.

---

## Scene B — Ingestion of a new document (extraction + gate scene)

Created `demo/docs/handover-note.md` (fictional Pellucid Pay handover note, ~150 words, plain prose, no code blocks) containing:
- ownership fact: "Priya Nair owns invoice-export-service"
- dependency: "invoice-export-service depends on ledger-service"
- hedge: "we might move invoice-export-service to the Payments team next quarter"
- denial: "Mateo Alvarez does not own invoice-export-service"

Command:
```
time $NEO ingest --wait demo/docs/handover-note.md
```
Output:
```
ingested /home/bindesh/neo-cortex/demo/docs/handover-note.md: documents 1, skipped 0, chunks 1, mentions 6, rels 2, errors 0, unsupported 0, new_entities 2

real	0m0.666s
user	0m0.050s
sys	0m0.009s
```
Notes: real ingest wall time ~0.67 s (Scene B timing; reused for Scene D comparison).

Document id (from cypher): `doc_21459436bb463756` (title `docs/handover-note`, kind `doc`).

What the extractor created — Chunks:
Command:
```
$NEO cypher "MATCH (d:Document {id:'doc_21459436bb463756'})-[:HAS_CHUNK]->(c:Chunk) RETURN c.id, c.pos, c.text"
```
Output:
```
1 rows: c.id | c.pos | c.text
doc_21459436bb463756#0 | 0 | Pellucid Pay engineering handover note — invoice-export-service Priya Nair owns invoice-export-service. She took over the service from the Platform team at the start of the quarter and is the current…
```
Notes: chunk text trimmed (it's the full ~150-word note); displayed with trailing ellipsis by the cypher tool.

Entities mentioned (name, type):
Command:
```
$NEO cypher "MATCH (c:Chunk {id:'doc_21459436bb463756#0'})-[:MENTIONS]->(e:Entity) RETURN e.id, e.name, e.type ORDER BY e.name"
```
Output:
```
6 rows: e.id | e.name | e.type
ent_... | Mateo Alvarez | person
ent_... | Platform | team
ent_... | Priya Nair | person
ent_... | invoice-export-service | service
ent_... | ledger-service | service
ent_... | payments API | team
```
Notes: GLiNER extracted both people (Priya Nair, Mateo Alvarez), both services (invoice-export-service, ledger-service), and two teams (Platform, payments API from "Payments team"). Full ids omitted for brevity (they change per run); the shown ids are the real ones from this run with the hex part replaced by "...".

REL edges (type, modality, p_fact, conf):
Command:
```
$NEO cypher "MATCH ()-[r:REL {source_id:'doc_21459436bb463756#0'}]->() RETURN startNode(r).name AS head, r.type AS type, endNode(r).name AS tail, r.modality AS modality, r.p_fact AS p_fact, r.conf AS conf ORDER BY head, type"
```
Output:
```
2 rows: head | type | tail | modality | p_fact | conf
Priya Nair | OWNS | invoice-export-service | fact | 0.9881 | 0.9677
invoice-export-service | DEPENDS_ON | ledger-service | fact | 0.6377 | 0.9914
```
Notes: Both required facts surfaced as current `fact` edges with high `p_fact`/`conf`. Crucially, the DENIAL ("Mateo Alvarez does not own invoice-export-service") produced NO `OWNS` edge for Mateo, and the HEDGE ("might move ... to the Payments team next quarter") produced NO current edge — `payments API` was extracted as a team but no move edge was written. Denials are dropped by the edge gate; hedges/possibilities are not treated as current ownership. `src/neo_cortex/extract.py` `_gate` classifies each source sentence as fact/possibility/denial/plan; denial drops the edge.

`neo who "invoice-export-service"`:
Output:
```
# who: "invoice-export-service" (entities: invoice-export-service), ranked, with evidence
1. [ent_...] Priya Nair score 0.97
   Priya Nair -[OWNS]-> invoice-export-service (src "docs/handover-note" [doc_21459436bb463756] 2026-10-18)
```
Notes: Only Priya Nair is ranked as current owner; Mateo Alvarez (from the denial) is absent — denial edges are not treated as current ownership.

`neo explore "invoice-export-service"`:
Output (trimmed):
```
# [ent_...] invoice-export-service (service)
## Neighbours
- invoice-export-service -[DEPENDS_ON]-> [ent_...] ledger-service (service) 2026-10-18 conf 0.99 src "docs/handover-note" [doc_21459436bb463756] 2026-10-18
- invoice-export-service <-[OWNS]- [ent_...] Priya Nair (person) 2026-10-18 conf 0.97 src "docs/handover-note" [doc_21459436bb463756] 2026-10-18
## Most-mentioning documents
- [doc_21459436bb463756] doc 2026-10-18 "docs/handover-note" (1 chunks)
```
Notes: Neighbourhood shows the dependency and the ownership edge only. No Mateo edge, no hedge/move edge. GLiNER "got wrong": it extracted `payments API` (from "Payments team") and `Platform` as extra team entities (harmless noise), and did not turn the hedge into any edge — which is actually correct behavior (a possibility is not a current fact). Attempt 1 gave a clear demo; no further attempts needed.

---

## Scene C — Classification visible to the viewer

Places GLiNER classification shows:
1. Edge `modality` / `p_fact` (Scene B REL output: `modality fact`, `p_fact 0.9881`, `conf 0.9677`).
2. Memory `kind` from session ingestion (setup ingests `demo/transcripts/history/*.jsonl` via `neo ingest-session`):
Command:
```
$NEO cypher "MATCH (m:Memory) RETURN m.id, m.kind, m.confidence, m.status ORDER BY m.kind, m.id"
```
Output (fresh setup db):
```
4 rows: m.id | m.kind | m.confidence | m.status
mem_7454ea02163d | episodic | 0.4494 | active
mem_a02c82a59514 | episodic | 0.3602 | active
mem_ac05429f51fa | preference | 0.8 | active
mem_e814d2d0f774 | preference | 0.8 | active
```
3. `Judgment` nodes (GLiNER yes/no/choice cache):
Command:
```
$NEO cypher "MATCH (j:Judgment) RETURN j.id, j.question, j.result, j.created_ms ORDER BY j.created_ms"
```
Output:
```
1 rows: j.id | j.question | j.result | j.created_ms
97d3be1eaaa9fe57 |  | {"same": 0.8433, "different": 0.1567} | 1792328810994
```
Command (count):
```
$NEO cypher "MATCH (j:Judgment) RETURN count(j) AS judgment_count"
```
Output:
```
1 rows: judgment_count
1
```
Notes: One `Judgment` node exists on this small db (from entity-resolution during ingest; it's a `same`/`different` entity-merge judgment). On a larger run there would be more. This is the GLiNER classification cache in graph form.

How a Judgment is reused (no second model call): `src/neo_cortex/resolve.py`, `judge()` (lines 28-38):
```python
def judge(store, question: str, text: str, labels: list[str], tenant=None) -> dict[str, float]:
    """GLiNER choice probabilities, cached as a Judgment node keyed by the content hash (pg-jev idea)."""
    jid = content_hash("\x1f".join([question, text, *labels]))
    rows = store.query("MATCH (j:Judgment {id:$i}) RETURN j.result", {"i": jid}, tenant)
    if rows:
        return json.loads(rows[0][0])   # cache hit: returns stored result, GLiNER NOT called again
    from .extract import _softmax_labels
    res = {k: round(v, 4) for k, v in _softmax_labels(f"{question} {text}".strip(), "judge", labels).items()}
    store.query("MERGE (j:Judgment {id:$i}) SET j.question=$q, j.result=$r, j.created_ms=$t",
                {"i": jid, "q": question, "r": json.dumps(res), "t": now_ms()}, tenant)
    return res
```
Cache key: `content_hash("\x1f".join([question, text, *labels]))` — a hash of the question, text, and labels joined by unit separator. On a cache hit the stored `j.result` is returned and GLiNER is not invoked again (pg-jev idea: cached decisions as graph nodes). Only on a miss does `_softmax_labels` (GLiNER) run and the result get `MERGE`d as a new `Judgment`.

---

## Scene D — Direct write vs extraction timing

Command (direct write, no GLiNER):
```
time $NEO remember "The handover note established Priya Nair as current owner of invoice-export-service and its dependency on ledger-service; Mateo Alvarez's denial was correctly dropped by the edge gate." --kind decision --entity "demo/docs/handover-note.md:file" --entity "invoice-export-service:service" --rel "invoice-export-service|DEPENDS_ON|ledger-service"
```
Output:
```
created [mem_0a6765f034fc] decision about: demo/docs/handover-note.md [ent_...], invoice-export-service [ent_...], ledger-service [ent_...]
edge invoice-export-service -[DEPENDS_ON]-> ledger-service: already current since 2026-10-18: [ent_...] invoice-export-service -[DEPENDS_ON]-> [ent_...] ledger-service (nothing written)

real	0m0.152s
user	0m0.051s
sys	0m0.008s
```
Notes: `neo remember` wall time ~0.15 s. Scene B's `neo ingest --wait` (GLiNER extraction + gating) wall time ~0.67 s. Direct agent write is ~4x faster than extractor ingestion (~0.15 s vs ~0.67 s) and runs no GLiNER at all (`kind` + `entities`/`relations` skips extraction, per `src/neo_cortex/AGENTS.md` `write.remember`). The DEPENDS_ON edge already existed from ingestion, so `remember` reported "already current ... (nothing written)" for the relation and only wrote the decision memory.

---

## Scene E — Four ways of searching one question

Question (from `demo/SCRIPT.md` "1:15 to 2:25", where the graph clearly helps):
`Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?`

(1) vector only — the documented `demo/tool.sh recall '{"query":"...","channels":["vector"]}'` interface is NOT exposed:
Command:
```
demo/tool.sh recall '{"query":"Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?","channels":["vector"]}'
```
Output:
```
curl: (22) The requested URL returned error: 400
```
Notes: The HTTP/MCP `recall` tool (`src/neo_cortex/mcp_server.py` line 65) accepts only `query, k, since, until, kinds, max_chars` — there is no `channels` argument on the wire, so isolating a single channel through `neo recall` / `demo/tool.sh recall` is not possible. The internal `src/neo_cortex/tools.recall`/`retrieve.recall` do accept `channels`, but it is not surfaced by the CLI or API. This is a real mismatch (see Problems found).

(2) bm25 only — same limitation; not isolatable via the documented interface (would also 400 with `channels`).

(3) graph+all channels = normal `neo recall` (shows the per-hit `via vector#N, bm25#N, graph#N` tags):
Command:
```
demo/tool.sh recall '{"query":"Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?"}'
```
Output:
```
# recall "Northgate Freight reports their invoice totals in reporting-service are about…": 8 results (id | source | channels#rank)
1. [mem_0a6765f034fc] decision 2026-10-18 | memory claude-code/neo-cortex | via vector#17,bm25#33,graph#35
   The handover note established Priya Nair as current owner of invoice-export-service and its dependency on ledger-service; Mateo Alvarez's denial was correctly dropped by the edge gate.
   path: ledger-service <-[MENTIONS]- mem_0a6765f034fc
2. [tkt-23#0] ticket 2026-09-09 | doc "SUP-388: Northgate totals look doubled" (ticket) [tkt-23] by Jonas Albrecht | via vector#1,bm25#1,graph#1
   Northgate Freight reports that invoice totals coming out of reporting-service look about double what they should be. … Northgate is a logistics firm and relies on reporting-service for its month-end invoice totals.
   path: reporting-service <-[MENTIONS]- tkt-23#0
3. [tkt-24#0] ticket 2026-09-09 | doc "INC-04: Reporting totals inflated" (ticket) [tkt-24] by Yusuf Demir | via vector#2,bm25#2,graph#3
   Incident: reporting-service shows inflated invoice totals for Northgate Freight. Roughly 3,000 invoices show about twice their real total. … - Each affected invoice has two copies of the same event in what reporting-service consumes.
   path: reporting-service <-[MENTIONS]- tkt-24#0
4. [adr-002#0] adr 2026-06-09 | doc "ADR-002: Transactional outbox for ledger events" (adr) [adr-002] by Elif Yildiz | via vector#45,bm25#35,graph#32
   ledger-service writes each double-entry posting to its own database, and then the rest of the platform has to hear about it. … ledger-service writes each event into an outbox table in the same database transaction as the posting.
   path: Elif Yildiz <-[MENTIONS]- adr-002#0
5. [chat-18#0] chat 2026-09-09 | doc "#incidents: Northgate totals" (chat) [chat-18] by Olivia Hartmann | via vector#3,bm25#5,graph#4
   **[2026-09-09 09:10] Olivia Hartmann:** Northgate Freight's month-to-date totals in reporting are about double what the ledger says. … **[2026-09-09 09:27] Anjali Deshpande:** what do I tell Northgate right now?
   path: Anjali Deshpande <-[MENTIONS]- chat-18#0
6. [tkt-25#0] ticket 2026-09-10 | doc "DATA-325: Dedupe backfill executed" (ticket) [tkt-25] by Olivia Hartmann | via vector#5,bm25#3,graph#5
   On 2026-09-10 I ran the dedupe backfill in reporting-service over the affected period. … Re-ran the totals check for Northgate Freight. … Affected scope: about 3,000 invoices had doubled totals.
   path: reporting-service <-[MENTIONS]- tkt-25#0
7. [ses-07#0] session 2026-09-09 | doc "Agent session: diagnose doubled totals" (session) [ses-07] by Olivia Hartmann | via vector#4,bm25#4,graph#10
   Olivia asked: invoice totals shown by reporting-service are about double what ledger-service says. … Queried reporting-service totals against the ledger for a sample of 20 invoices.
   path: reporting-service <-[MENTIONS]- ses-07#0
8. [mtg-05#0] meeting 2026-09-11 | doc "Postmortem: INC-04 duplicate totals" (meeting) [mtg-05] by Yusuf Demir | via vector#8,bm25#9,graph#6
   # Postmortem: INC-04 duplicate totals … - Summary: reporting-service counted some invoice events twice. … It is not: that was a retry bug in notification-service, a different service and a different cause.
   path: reporting-service <-[MENTIONS]- mtg-05#0
```
Notes: Every hit carries `via vector#N, bm25#N, graph#N` tags showing which channels found it (result 2 matched all three at rank 1 — the graph channel clearly helps here; result 1 is the Scene-D decision memory I just wrote). Note result 1 (my Scene-D memory) appears because it was just ingested; on a pristine db it would not be present.

Graph-native follow-ups (all real):

`neo ask "Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?"` — seeds reporting-service + Northgate Freight, bridging facts `reporting-service -[DEPENDS_ON]-> ledger-service`, `Elif Yildiz -[OWNS]-> ledger-service`, `Olivia Hartmann -[OWNS]-> reporting-service`, with cited ticket/postmortem ids (evidence pack; the agent reasons, the tools cite).

`neo impact ledger-service` — 4 depend on it (fraud-scoring, invoice-export-service, reporting-service at hop 1; payment-gateway at hop 2), it needs event-pipeline, owners to tell: Elif Yildiz (ledger-service), Kofi Mensah (fraud-scoring), Olivia Hartmann (reporting-service), Priya Nair (invoice-export-service, from Scene B's handover note), Daniel Kwon (payment-gateway). Every edge cited to its source doc.

`neo who "session cache"` — Mateo Alvarez current owner (doc-14), Lukas Brandt FORMER ended 2026-09-03 (doc-02), plus Platform-team members; current direct OWNS ranked first.

`neo timeline "session.ttl_seconds"` — 2026-06-18 3600→900 (CFG-4380, tkt-05), 2026-08-12 900→300 (ADR-007), each dated and sourced.

`demo/tool.sh connect '{"a":"Olivia Hartmann","b":"Elif Yildiz"}'` — 2 paths: `Olivia Hartmann -[OWNS]-> reporting-service -[DEPENDS_ON]-> ledger-service <-[OWNS]- Elif Yildiz`, each edge with source doc/date.

---

## Scene F — FalkorDB Browser queries (3, nodes+edges, row counts, ready to paste)

All run through `neo cypher` (read-only `GRAPH.RO_QUERY`) and return rows.

(1) Owners of session-cache with dated OWNS edges:
```cypher
MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p, r, s
```
Row count: 4 rows. Returns person/team nodes `p`, the `[:REL {type:'OWNS', ..., modality, p_fact, valid_from_ms}]` edges `r`, and the session-cache node `s`. Shows dated ownership (Platform via chat-15 with `modality: possibility`; Platform via adr-006 fact; Lukas Brandt fact ended via doc-02; Mateo Alvarez fact via doc-14).

(2) Dependency neighbourhood of ledger-service (2 hops):
```cypher
MATCH (a:Entity)-[r:REL*1..2]-(b:Entity {name:'ledger-service'}) RETURN a, r, b LIMIT 20
```
Row count: 19 rows (capped at 20; "...11 more" beyond the displayed 8). Returns neighbour nodes `a`, the variable-length relationship paths `r`, and ledger-service `b`. FalkorDB renders relationships as `<(38)-[336]->(37)>` etc.

(3) The new handover-note document with its chunk, entities, and edges:
```cypher
MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)-[:MENTIONS]->(e:Entity) WHERE d.path ENDS WITH 'handover-note.md' RETURN d, c, e LIMIT 20
```
Row count: 6 rows (document + its 1 chunk + 6 mentioned entities: payments API, Platform, ledger-service, Mateo Alvarez, invoice-export-service, Priya Nair).

and the edges:
```cypher
MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)-[:MENTIONS]->(e:Entity) WHERE d.path ENDS WITH 'handover-note.md' MATCH (e)-[r:REL]->(e2:Entity) WHERE r.source_id = c.id RETURN e, r, e2 LIMIT 20
```
Row count: 2 rows (`Priya Nair -[OWNS]-> invoice-export-service`, `invoice-export-service -[DEPENDS_ON]-> ledger-service`, both `source_id = doc_21459436bb463756#0`, `modality fact`).

Notes: All three return nodes AND relationships (not just properties), suitable for the Browser's graph view. Paste into FalkorDB Browser connected to 127.0.0.1:6399, graph `neo_default`. Row counts prove each returns rows. Ids differ per run but structure is stable.

---

## Scene G — DREAM (memory consolidation)

Created 3 near-duplicate memories and 1 conflicting pair via `neo remember`:
- `neo remember "The retry limit for the payment gateway is set to 3 attempts." --kind semantic --entity "payment-gateway:service"` → `created [mem_123aa706d9cb]`
- `neo remember "The retry limit for the payment gateway is configured to 3 attempts." --kind semantic --entity "payment-gateway:service"` → `reinforced [mem_123aa706d9cb] ... (nothing new written)` (near-duplicate, deduplicated by remember)
- `neo remember "Payment gateway retry limit is 3 attempts." --kind semantic --entity "payment-gateway:service"` → `reinforced [mem_...]` (deduplicated)
- `neo remember "The retry limit for the payment gateway is set to 5 attempts." --kind semantic --entity "payment-gateway:service"` → `created [mem_5993699fa3ff]` plus `conflicts: ... - [mem_123aa706d9cb] sim 0.97 The retry limit ... 3 attempts.` (conflicting pair: differs in number 3 vs 5)

Before-count: `MATCH (m:Memory) RETURN count(m)` → 6 (baseline). After creating the two new memories: 8.

`neo dream --dry-run`:
```
# dream (dry run, nothing written): merged 0, promoted 0, decayed 0, conflicts 3
```
`neo dream` (real run):
```
# dream (dream_ac391b1ae230): merged 0, promoted 0, decayed 0, conflicts 3
```
After-count: `MATCH (m:Memory) RETURN count(m)` → 8 (no merges, nothing deleted).

`neo cypher` DreamRun node:
```
$NEO cypher "MATCH (d:DreamRun) RETURN d.id, d.merged, d.promoted, d.decayed, d.conflicts"
```
Output:
```
1 rows: d.id | d.merged | d.promoted | d.decayed | d.conflicts
dream_ac391b1ae230 | 0 | 0 | 0 | 3
```
MERGED_INTO edges:
```
$NEO cypher "MATCH ()-[r:MERGED_INTO]->() RETURN count(r) AS merged_into_edges"
```
Output:
```
1 rows: merged_into_edges
0
```
CONFLICTS_WITH edges:
```
$NEO cypher "MATCH ()-[r:CONFLICTS_WITH]->() RETURN count(r) AS conflict_edges"
```
Output:
```
1 rows: conflict_edges
3
```
Notes: `merged 0` — this matches `demo/SCRIPT.md`'s documented known gap: "`remember` already reinforces near-duplicates, so only conflicts show." Because `remember` deduplicates near-duplicates (cosine >= 0.92 → reinforce, no separate memory created), there are no separate near-duplicate memories for `dream` to merge, so `MERGED_INTO` = 0. The conflicting pair (3 vs 5 attempts, sim 0.97, differs in a number) IS flagged: `CONFLICTS_WITH` = 3 (one for the new pair plus pre-existing conflicts among baseline memories), logged as `DreamRun dream_ac391b1ae230`. A re-run of `dream` changes nothing (idempotent).

---

## Scene H — RRSI (self-tuning, tuner NOT run)

Read `eval/tune_clean.json` and `eval/tune_distract.json` (no tuner executed). Command:
```
python3 -c "import json
for f in ['eval/tune_clean.json','eval/tune_distract.json']:
    d=json.load(open(f))
    print('===', f, '===')
    print('proposed weights:', d['best'])
    print('score on search questions (odd):', d['odd_score'])
    print('held-out delta (even):', d['even_delta'])
    print('held-out 95% CI:', d['ci'])
    print('accepted:', d['accepted'])
    print()"
```
Real output:
```
=== eval/tune_clean.json ===
proposed weights: {'vector': 1.0, 'bm25': 2.0, 'graph': 0.5, 'temporal': 2.0}
score on search questions (odd): 0.7520833333333333
held-out delta (even): -0.01875
held-out 95% CI: [-0.075, 0.0375]
accepted: False

=== eval/tune_distract.json ===
proposed weights: {'vector': 1.0, 'bm25': 2.0, 'graph': 0.5, 'temporal': 1.0}
score on search questions (odd): 0.7166666666666667
held-out delta (even): 0.0375
held-out 95% CI: [0.0, 0.09375]
accepted: False
```
Notes: Both tuners proposed channel weights (clean: vector 1.0 / bm25 2.0 / graph 0.5 / temporal 2.0; distract: temporal 1.0) but `accepted: false` in both — the acceptance rule rejected them (held-out CI includes 0 / not clearly better, or latency outside the band), which is the RRSI rule working as designed (`docs/judges-guide.md` section 7: "It rejected its own weights, which is the rule working").

---

## Scene I — Cost facts (each with a file path; numbers quoted only from knowledge/models/*.md, docs/judges-guide.md, eval/*.md, or code)

- GLiNER2.5 model size: `knowledge/models/gliner2-5-base.md` Facts table — Parameters: "194M (card); 193,581,591 F32 params (safetensors metadata)"; Weight file: "`model.safetensors` 774,366,564 bytes (F32)"; "Expect roughly 0.77 GB on disk for the default upload" (HF repo `fastino/gliner2.5-base-v1`, Apache-2.0, DeBERTa-v3-base scale).
- GLiNER2.5 per-call latency: `docs/judges-guide.md` line 70 — "GLiNER about 26 ms per call on a 6 GB GPU" (GTX 1660 Ti, this machine).
- EmbeddingGemma size: `knowledge/models/embeddinggemma.md` Facts table — Parameters: "740M total (card); 744,371,512 BF16 (metadata)"; Weight file: "`model.safetensors`, 1,488,915,288 bytes (BF16)"; Native output dimension 768 (text-only load; vision/audio encoders load only when that modality is ingested).
- GPU memory used: observed `1959 MiB` on `nvidia-smi` after `setup.sh` loaded both models on this GTX 1660 Ti (6144 MiB card). `knowledge/models/gliner2-5-base.md` also reports fp16 peak GPU memory halved (1098 -> 589 MB) on the GTX 1660 Ti (opt-in, not default).
- What runs where: all local. `README.md` line 5 — "Everything runs locally: FalkorDB (embedded falkordblite or a Docker server), GLiNER2.5 for extraction, typing and judgments, and EmbeddingGemma for vectors. There is no LLM inside the system." The embedded Store binds to `127.0.0.1` only (`src/neo_cortex/store.py` line 40); daemon serves MCP/HTTP on `127.0.0.1:8765` loopback (`src/neo_cortex/cli.py` DEFAULT_URL).
- No paid API/LLM at ingest or query time: `README.md` line 5 ("There is no LLM inside the system"); `docs/judges-guide.md` line 7 ("There is no LLM inside: two small local models ... do the fast 'System 1' work, and the calling agent (Claude) does the reasoning"). Ingest runs GLiNER2.5 + EmbeddingGemma locally (`src/neo_cortex/extract.py`, `src/neo_cortex/models.py`); query runs the same local models plus BM25 (`bm25s`) and graph channels. No external model endpoint is called in `src/neo_cortex/`.

---

## Scene J — Browser setup research (no Docker run; proposal only, do not edit demo scripts)

Facts gathered by reading `src/neo_cortex/store.py`, `docker-compose.yml`, and README "FalkorDB modes":
- `docker-compose.yml`: service `falkordb` (image `falkordb/falkordb:latest`) binds `127.0.0.1:6379:6379` (DB) and `127.0.0.1:3000:3000` (FalkorDB Browser), loopback only.
- `src/neo_cortex/store.py`: embedded falkordblite binds `127.0.0.1:NEO_PORT` only (demo `NEO_PORT=6399` per `demo/env.sh`); `NEO_FALKORDB_URL` if set makes the Store use an external server and skip embedded; graph per tenant is `neo_<tenant>` → default graph `neo_default`.
- README "FalkorDB modes": Browser can connect to the embedded daemon (`127.0.0.1:6390` in README; demo uses `6399`) or to the Docker server (`127.0.0.1:6379`, Browser `:3000`).

Exact ordered steps to show the FalkorDB Browser on the SAME graph the demo uses (proposal; do not edit demo scripts):

1. Start Docker (it is not running): `sudo systemctl start docker`. (`docker ps` currently fails because the Docker daemon is not running and the user is not in the docker group.)
2. Start FalkorDB + Browser (loopback): `sudo docker compose up -d falkordb` (run from repo root; user not in docker group, so `sudo docker compose`). This serves the DB on `127.0.0.1:6379` and the Browser on `http://127.0.0.1:3000`.
3. Point the demo daemon at the Docker server instead of embedded: `export NEO_FALKORDB_URL=redis://localhost:6379`. Because `demo/env.sh` / `demo/setup.sh` hard-code the embedded server (`NEO_PORT=6399`, embedded Store when `NEO_FALKORDB_URL` is unset), this env override must be set before sourcing `demo/env.sh` and running `demo/setup.sh`; the Store then skips embedded and uses the Docker server. (Do not edit `demo/env.sh`/`demo/setup.sh`; just export the variable in the shell that runs them.)
4. Run `demo/setup.sh` (the demo daemon now writes to the Docker-served graph `neo_default`).
5. Open FalkorDB Browser at `http://127.0.0.1:3000`; connect to host `127.0.0.1`, port `6379`, graph `neo_default` — the same graph the demo daemon uses.

Notes / environment conditions: `docker ps` fails today (Docker daemon not running; user not in the docker group), so the user must run `sudo systemctl start docker` and use `sudo docker compose` (or `sudo usermod -aG docker $USER` and re-login, then plain `docker compose`). The embedded demo server (6399) and the Docker server (6379) are different data stores — pick one as the DB source for the Browser; do not point the Browser at 6399 while the demo uses 6379 or vice versa. The embedded default path (no Docker) also works for the Browser: connect it to `127.0.0.1:6399`, graph `neo_default`, while the demo daemon runs (README: connect Browser to the embedded port while the daemon runs).

---

## Problems found

Mismatches between what `docs/`/`VIDEO.md`/`demo/SCRIPT.md` claim and what I actually saw:

1. **`recall` does not expose `channels` via the CLI/API.** Scene E's prescribed `demo/tool.sh recall '{"query":"...","channels":["vector"]}'` returns HTTP 400. The wire `recall` tool (`src/neo_cortex/mcp_server.py` line 65) accepts only `query, k, since, until, kinds, max_chars`; `channels` exists only on the internal `tools.recall`/`retrieve.recall`. So vector-only and bm25-only searches cannot be isolated through the documented `neo`/`tool.sh` interface. Only the normal all-channels `neo recall` runs, and it does show per-hit `via vector#N, bm25#N, graph#N` tags. (The brief's Scene E assumes `channels` is surfaced; it is not.)

2. **Demo DB persistence across restarts is fragile.** After one `demo/teardown.sh`, `.neo/demo/neo.rdb` shrank from ~464 KB to 8 KB and a subsequent restart showed a degraded graph (15 documents / 29 chunks instead of 102/136), plus a stray queued background job. I had to re-run `demo/setup.sh` to restore a clean state. `shutdown(save=True)` did not appear to fully preserve the falkordblite graph. This is an operational observation, not a claim of a product bug; Falkorblite persistence across `teardown`/`setup` should be verified separately.

3. **Docker environment not ready.** `docker ps` fails because the Docker daemon is not running and the user is not in the docker group (stated in the Brief's Scene J). Scene J is therefore a research proposal only; the Browser-over-Docker steps were not executed.

No mismatch found for Scenes A, B, C, D, F, G, H, I — all matched the documented behavior (Scene G's `merged 0` matches `demo/SCRIPT.md`'s documented known gap that `remember` reinforces near-duplicates, so only conflicts show).

---

Closeout: `demo/teardown.sh` was run and ports 8765 and 6399 confirmed free (see final verification).

DONE

Files created:
- demo/CAPTURE.md (this file)
- demo/docs/handover-note.md (Scene B input document)
