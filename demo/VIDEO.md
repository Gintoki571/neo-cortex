# Neo-Cortex demo video plan (about 5 minutes, plain language)

Audience: a judge or a beginner who has never seen a knowledge graph. Rule: no jargon; when a technical word is unavoidable, say the plain meaning first and the word once. Analogies carry the explanation: the detective's string board, the judge who writes down every verdict, sleeping and tidying.

Every command and output below is real, captured on the GPU on 2026-10-18 (`demo/CAPTURE.md`, scenes A to J) or verified earlier in `demo/SCRIPT.md`. Ids such as `mem_...` change per run: never read them aloud. Fictional company: Pellucid Pay (`data/synthetic`). Procedure for recording and uploading: `demo/RECORDING.md`. Showing the FalkorDB Browser: `demo/BROWSER.md`.

## Before you hit record

1. Free the machine (nothing else on the GPU; nothing on ports 8765 or 6399). Build the demo database: `demo/setup.sh` (about 2 minutes on the GPU).
2. Start the FalkorDB Browser (recipe in `demo/BROWSER.md`), log in with host `127.0.0.1`, port `6399`, graph `neo_default`. Dismiss its "What's new" popup, zoom 110-125 percent, dark theme.
3. Terminal: dark theme, font 18 or larger, `source demo/env.sh`, `alias neo=$NEO`, `clear`.
4. Record the scenes in the order below, on ONE database, because scene 6 shows the handover note from scene 3 inside the blast-radius answer (4 services depend on ledger-service instead of 3). Between full takes use `demo/reset.sh` (restores the snapshot). Do NOT run `demo/teardown.sh` between takes: the capture found that a teardown followed by a restart can lose the data; if it happens, run `demo/setup.sh` again.
5. Rehearse once. Anything that differs from the "Point at" lines is a bug to tell me about, not to improvise around.
6. Fallback if a live command misbehaves: `demo/run_cli_demo.sh --pause` (same story, terminal only).

---

## Scene 1: The problem, and the board that never forgets (0:00-0:35)

**Show:** terminal, `neo status`. Then the FalkorDB Browser with this query typed and run:

```cypher
MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p, r, s
```

**Real output (`neo status`):** `Chunk | 136   Entity | 134   Document | 102   Memory | 4   Session | 2   Agent | 1`

**Point at:** the counts; then the picture: people (dots) joined to the session cache by strings labelled OWNS (4 rows: Mateo Alvarez and Lukas Brandt as people, Platform as a team, ownership edges with dates).

**Say:** "An AI assistant that can do tasks on its own, we call it an agent, is brilliant for one afternoon, and then it forgets everything. Tomorrow you explain it all again. A company's knowledge is no better: the facts about one piece of software are scattered over tickets, documents, chats and meeting notes. Picture a detective's string board: every person, service and decision is a card, and every relationship is a string between two cards. That board is called a knowledge graph. Neo-Cortex keeps the whole board in one graph database, called FalkorDB, so nothing is forgotten, and you can see it right here."

**Why this scene:** the problem and the product in half a minute; the picture makes "graph" concrete before any tool appears.

**Source:** README.md (intro, tracks); demo/CAPTURE.md scenes A and F.

## Scene 2: One graph, three jobs, no bills (0:35-1:10)

**Show:** a simple slide or the README "Tracks entered" list (agent memory, company brain, multi-step questions); then in the terminal `neo --help` (the list of commands).

**Say:** "One graph, three jobs. It is an agent's long-term memory. It is a company's brain, built from its documents. And it answers questions that need several steps, like a librarian who knows not only the books but how the shelves connect. Agents reach it in two ways: fifteen ready-made actions, offered through a connection standard called MCP, or by typing the neo command. And here is the surprise: there is no big AI model inside. Two small programs trained on text run on your own computer. One reads a piece of text and picks out what it says in about twenty-six thousandths of a second; the other turns text into numbers that capture its meaning. Together they use about two gigabytes of the graphics card's memory. So there is no per-question bill, no internet needed, and your data never leaves the machine. The thinking is done by the agent that calls it."

**Why this scene:** cost and architecture are what judges weigh; "no big model inside" is the sharpest edge.

**Source:** README.md intro ("There is no LLM inside the system", everything local); docs/judges-guide.md sections 1 and 7 (about 26 ms per call on a 6 GB GPU); eval/mcp_smoke.md (15 of 15 tools pass); demo/CAPTURE.md scene I (models about 1,959 MiB of GPU memory in this run; GLiNER2.5 about 194M parameters, EmbeddingGemma about 740M).

## Scene 3: How a document becomes a graph (1:10-2:00)

**Show:** the new note on screen (`cat demo/docs/handover-note.md`): four plain sentences (an owner, a dependency, a "might move", a "does not own"). Then:

```bash
neo ingest --wait demo/docs/handover-note.md
```

**Real output:** `ingested ...handover-note.md: documents 1, skipped 0, chunks 1, mentions 6, rels 2, errors 0, unsupported 0, new_entities 2` (about 0.67 seconds). Then in the Browser:

```cypher
MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)-[:MENTIONS]->(e:Entity) WHERE d.path ENDS WITH 'handover-note.md' RETURN d, c, e LIMIT 20
```

**Point at:** six cards are connected to the new document (two of them brand new, the rest already on the board): Priya Nair and Mateo Alvarez (person), invoice-export-service and ledger-service (service), Platform and "payments API" (team).

**Say:** "So how does a file become a graph? Watch. The file is converted to plain text and cut into small pieces. Each piece gets a set of meaning numbers, like coordinates on a map where similar things sit close together. Then a small reading model, called GLiNER, reads every sentence and picks out the people, the services and the teams, and the relationships between them. That is called extraction. It also asks each sentence a simple question: is this a fact, a maybe, a denial, or a plan? That is called classification. Everything is then written into FalkorDB as cards and strings. Less than a second, one new document, and the board has new cards and strings."

**Why this scene:** judges must see an ordinary file turned into structured knowledge with no labelling work and no big model.

**Source:** docs/judges-guide.md section 4 (pipeline, chunking, GLiNER2.5, fact/maybe/denial/plan gate); demo/CAPTURE.md scene B.

## Scene 4: The judge who writes down every verdict (2:00-2:35)

**Show:** the two strings that were written, from the terminal:

```bash
neo cypher "MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk) WHERE d.path ENDS WITH 'handover-note.md' MATCH (a:Entity)-[r:REL]->(b:Entity) WHERE r.source_id = c.id RETURN a.name, r.type, b.name, r.modality, r.p_fact ORDER BY r.type"
neo who "invoice-export-service"
```

**Real output:**
`invoice-export-service | DEPENDS_ON | ledger-service | fact | 0.6377`
`Priya Nair | OWNS | invoice-export-service | fact | 0.9881`
`# who: "invoice-export-service" ... 1. Priya Nair score 0.97` (nobody else is listed). Then the saved verdict:

```bash
neo cypher "MATCH (j:Judgment) RETURN j.result"
```
Real output: `{"same": 0.8433, "different": 0.1567}`

On screen, one line of credit: "the verdict idea: github.com/realZachi/pg-jev".

**Point at:** `fact` and the probability on each string; the missing Mateo line even though the note mentions him; the verdict record.

**Say:** "Now the clever part. The reading model does not write a paragraph; it gives a probability, like a weather forecast: ninety-eight percent sure this is a fact. Look at our note. It also said Mateo does not own the service, and that the service might move next quarter. Neither became an ownership line on the board. The denial was thrown away at the door, and a maybe is never treated as a current fact. Only the real owner is listed. And when the model is unsure whether two names are the same thing, it gives its odds, here eighty-four percent, and that verdict is saved in the graph as a little record, so the same judgment is reused instead of asked again. That idea, a judge who writes down every verdict, comes from a project called pg-jev, and we use it inside FalkorDB."

**Why this scene:** correctness. A denied or hedged sentence cannot turn into a false fact, and every decision is stored and auditable.

**Source:** demo/CAPTURE.md scenes B and C (the edge gate dropped the denial and wrote no edge for the hedge; `Judgment` cache keyed by a hash of question, text and labels, `src/neo_cortex/resolve.py judge()`); docs/lineage.md section 1 (pg-jev); README "System 1 decisions, measured" (trap probe 17/25 for the model alone, 20/25 with the rule).

## Scene 5: An agent can write straight into the graph (2:35-2:55)

**Show:**

```bash
time neo remember "Mateo Alvarez now works on billing reconciliation after handing the export service to Priya Nair." --kind decision --entity "Mateo Alvarez:person" --entity "billing reconciliation:component" --rel "Mateo Alvarez|WORKS_ON|billing reconciliation"
```

**Real timings (GPU):** one direct write about 0.15 seconds (re-measured: 0.148 s, printing `created ...` and `edge ... created`); ingesting the note through the reading model about 0.67 seconds.

**Point at:** the "created" line with typed names and the edge; the two stopwatch numbers.

**Say:** "The reading model is for documents nobody has read yet. But an agent that has just finished a job already knows the facts. So it can write them straight into the graph, naming the things and the links itself. The reading step is skipped, so there is no misreading, and it takes a fraction of a second."

**Why this scene:** the memory loop closes: the agent that did the work records the result for the next agent, immediately and exactly.

**Source:** docs/judges-guide.md section 4; demo/CAPTURE.md scene D. Use a relation that is not in the graph yet (the capture's own example repeated an existing one and printed "already current ... (nothing written)").

## Scene 6: Asking questions, four searches at once (2:55-4:00)

**Show:**

```bash
demo/tool.sh recall '{"query":"Northgate Freight reports their invoice totals in reporting-service are about double. What is the root cause?"}'
neo impact ledger-service
demo/tool.sh connect '{"a":"Olivia Hartmann","b":"Elif Yildiz"}'
neo who "session cache"
neo timeline "session.ttl_seconds"
```

**Real output (recall):** on a fresh database the top hit is the ticket "SUP-388: Northgate totals look doubled" with `via vector#1,bm25#1,graph#1`; the design note "ADR-002: Transactional outbox for ledger events" comes second although each single search ranked it low (`vector#43,bm25#34,graph#30`: agreement between the searches pulled it up); the incident ticket INC-04 follows with `via vector#2,bm25#2,graph#3`.
**Real output (impact):** 4 depend on ledger-service (fraud-scoring, invoice-export-service and reporting-service directly; payment-gateway through another service), with the owners to tell, including Priya Nair from the note we just added.
**Real output (connect):** `Olivia Hartmann -[OWNS]-> reporting-service -[DEPENDS_ON]-> ledger-service <-[OWNS]- Elif Yildiz`, each string with its source.
**Real output (who):** Mateo Alvarez is the current owner; Lukas Brandt is marked FORMER with an end date.
**Real output (timeline):** `session.ttl_seconds` 3600 to 900 on 2026-06-18 (CFG-4380), then 900 to 300 on 2026-08-12 (ADR-007), each change dated and sourced. This is the time search at work (the recall tags show the other three).

**Point at:** the tags after each result, naming which searches found it; the path that walks from one person to another; the former owner.

**Say:** "Now, how do we find things? FalkorDB does four kinds of searching and merges them into one answer: by words, by meaning, by connections, and by time. Words and meaning are what any search tool does; look at the tags, they say which search found each result. Time means the graph remembers what was true then and what has changed, like this owner, who is marked former. But the star is connections. The graph starts at the things in your question, follows the strings, finds the shortest path between two people, and the fewest steps between two people. It can also answer: if this piece of software stops working, what is affected? It walks the 'depends on' strings backwards, and tells you which owners to call. And that is measured: on questions about what is affected when something fails, the graph gives the full answer eighty percent of the time; plain text search, twenty. Following connections is the one thing a plain text search cannot do. Words and meaning, connections, and time: that is the four."

**Why this scene:** the graph doing work the agent could not do without it; the central claim, shown live and backed by 0.80 vs 0.20.

**Source:** eval/answers.md (impact: all expected keys 0.80 with the graph vs 0.20 with text search, significant); README "Retrieval" (four channels, merged); demo/CAPTURE.md scene E. Note: the live recall shows three tags (words, meaning, connections); the time search shows in `neo timeline` and when a question carries a date. The command line cannot switch single searches off (the wire tool has no channel argument), so this scene shows the per-result tags instead of a side-by-side; for the numbers say "vector 0.73, words 0.71, all four 0.76 recall@10 (eval/results.md): graph ties text at finding documents and wins at following connections".

## Scene 7: Memory that tidies itself (4:00-4:25)

**Show:**

```bash
neo remember "The retry limit for the payment gateway is set to 3 attempts." --kind semantic --entity "payment-gateway:service"
neo remember "The retry limit for the payment gateway is set to 5 attempts." --kind semantic --entity "payment-gateway:service"
neo dream
neo cypher "MATCH (d:DreamRun) RETURN d.id, d.merged, d.promoted, d.decayed, d.conflicts"
```

On screen, one line of credit: "the sleeping idea: github.com/zhengkid/Dream-RSI".

**Real output:** the second note prints a `conflicts:` line (similarity 0.97, differs in a number: 3 versus 5); `neo dream` prints `merged 0, promoted 0, decayed 0, conflicts 2` on the full demo database the count was 2 on a fresh `demo/setup.sh` (the demo data already holds one other conflicting pair; the number can differ by one or two, so say "conflicts flagged", not the number); the log record `dream_... | 0 | 0 | 0 | 2`.

**Point at:** the conflict line when the second note is written; the log record in the graph.

**Say:** "Memories need tidying, and nobody wants chores, so the graph sleeps. One command, neo dream, tidies up: identical notes are combined into one, something remembered across at least three separate sessions is promoted from 'this happened' to 'this is true', old unused notes slowly fade (nothing is deleted), and two notes that disagree are flagged for the agent to settle. Here we told it the retry limit is three, then five. It noticed the clash, flagged it, and wrote down that it did, a log record in the graph. Nothing needed merging today, because repeated notes are already combined the moment they are written. This idea comes from a research project called Dream-RSI, and we built a simple, repeatable version of it."

**Why this scene:** consolidation is track 02's headline; the system maintains itself and leaves an audit trail.

**Source:** demo/CAPTURE.md scene G (merged 0 is honest: `remember` already reinforces near-duplicates, as noted in demo/SCRIPT.md); README "Memory lifecycle"; docs/lineage.md section 3.

## Scene 8: Tuning that cannot fool itself (4:25-4:45)

**Show:**

```bash
python3 -c "import json; d=json.load(open('eval/tune_clean.json')); print(d['best'], round(d['odd_score'],3), round(d['odd_default'],3), d['even_delta'], d['ci'], d['accepted'])"
```

On screen, one line of credit: "the tuning idea: github.com/google-research/rrsi (arXiv 2609.24972)".

**Real output:** `{'vector': 1.0, 'bm25': 2.0, 'graph': 0.5, 'temporal': 2.0} 0.752 0.648 -0.01875 [-0.075, 0.0375] False` (the tuner is `eval/tune.py`; it was run earlier and its result file is shown, not re-run on camera)

**Point at:** 0.752 on the practice questions (0.648 for the default settings), the negative change on unseen questions, and `False`.

**Say:** "Could the search be tuned automatically? We built the rule that makes that safe, and ran it offline. The rule: try new search weights on half of the test questions, and keep them only if they also win on questions the tuning never saw. This time the new weights looked better on the first half, then did slightly worse on the unseen half, so the rule rejected them and the old weights stay. That 'no' is the feature working: a check that cannot be fooled. The idea is from a research project called RRSI."

**Why this scene:** judges reward honest self-evaluation; a rejection shown proudly is stronger than a suspiciously perfect result.

**Source:** eval/tune_clean.json (odd-split score 0.752 vs 0.648 for the defaults; held-out change -0.019, interval [-0.075, +0.038], accepted false); demo/CAPTURE.md scene H; docs/lineage.md section 2.

## Scene 9: The honest close (4:45-5:10)

**Show:** the table in `eval/flags.md` (seven ideas tried and not adopted); then the public repository page and the explainer page in the browser; then the AI-use sentence on screen.

**Say:** "One more thing: what we measured and did not adopt. We tried seven more ideas for searching and for merging names, and none beat our default across both of our test collections, so they stay switched off. Where the graph only ties plain text search, we say so. The numbers, the code and a visual explainer are all in the public repository. Neo-Cortex was built with Claude Code and other AI coding agents; people directed, reviewed and verified the work, and the system itself contains no big language model. One graph, three jobs: agents acting on connected data, agent memory, and a company brain. Neo-Cortex, the detective's board that never forgets."

**Why this scene:** honesty is the last impression: rejected ideas, a tie reported as a tie, and the AI-use rule satisfied in one sentence.

**Source:** eval/flags.md; README "AI use disclosure"; README Table B (document finding is a tie within noise).

---

## Scene, track, time

| Scene | Track(s) shown | Time |
|---|---|---|
| 1 The problem and the board | framing | 0:00-0:35 |
| 2 One graph, three jobs, no bills | 01, 02, 03 | 0:35-1:10 |
| 3 How a document becomes a graph | 03 | 1:10-2:00 |
| 4 The judge who writes down verdicts | 01, 03 | 2:00-2:35 |
| 5 An agent writes straight in | 02 | 2:35-2:55 |
| 6 Four searches at once | 01, 03 | 2:55-4:00 |
| 7 Memory that tidies itself | 02 | 4:00-4:25 |
| 8 Tuning that cannot fool itself | 01 | 4:25-4:45 |
| 9 The honest close | all three | 4:45-5:10 |

## Words we avoid, and what we say instead

| Avoided | Plain replacement |
|---|---|
| knowledge graph | detective's string board: cards for things, strings for relationships (the term is named once, with its meaning) |
| embedding, vector | meaning numbers, coordinates on a map of meanings |
| BM25 | searching by words |
| rank fusion | merging four searches into one answer |
| PageRank | following the strings from each starting card (not named) |
| Cypher | the query typed into the Browser (not named) |
| MCP | fifteen ready-made tools, "a plug standard called MCP" (said once) |
| entity resolution | whether two names are the same thing |
| modality | fact, maybe, denial, plan |
| System 1 | the fast reading model (not named) |
| supersede | the old one is closed, not deleted; history stays |
| LLM | a big language model; "the thinking stays with the agent" |
