# eval/

Gold set for Neo-Cortex over the synthetic Pellucid Pay corpus (AI-generated, fictional; see `data/synthetic/WORLD.md`).

## Files

- `gold.jsonl`: 40 questions. Fields: `id, type, question, answer, gold_docs, gold_entities, facts, hops`.
- `check_dataset.py`: stdlib consistency check. Run `python3 eval/check_dataset.py` (exit 1 on error).
- Corpus: `data/synthetic/manifest.jsonl` (102 docs) and `data/synthetic/<kind>/<id>.md`.

## Question types

| type | n | what it tests |
|---|---|---|
| single | 8 | one fact in one document (control; vector or BM25 should win) |
| multi | 12 | 2-3 hops: facts spread across several documents of different kinds, so no single document or keyword match answers |
| temporal | 8 | current vs previous value, what changed when, what was true on a date |
| ownership | 7 | who should review / who knows most; owner and expertise facts live in different documents |
| procedural | 5 | how to do X, lessons learned |

Questions avoid the wording of the source documents (for example "login-state cache" for session-cache, "sign-out" for logout) so lexical match alone is weak.

## How manifest, facts and questions link

- `WORLD.md` numbers every atomic fact (`F001`...). Facts marked `[T]` are temporal and carry a date.
- Each manifest line lists the `facts` its document states (partially or indirectly).
- Each question lists the `facts` its answer needs and the `gold_docs` that together contain them. The check enforces: every question fact is in some manifest doc; every gold doc exists; gold docs cover all question facts; for `multi` and `ownership` questions no single manifest document contains all the facts (so the graph channel is required).
- Scoring: retrieval recall@k against `gold_docs`; answer match against `answer`; per-type breakdown feeds the ablation table.

## Regenerating

The manifest and gold files are the source of truth; edit them directly and re-run the check. Documents under `data/synthetic/<kind>/` are written from the manifest briefs; the six exemplars (doc-07, adr-007, tkt-18, chat-12, mtg-05, ses-07) show the target style.

## Running the retrieval eval

```
NEO_HOME=.neo/eval NEO_PORT=6395 uv run --no-sync python eval/run_eval.py [--reingest] [--configs full,vector+bm25] [--k 20] [--no-tools]
```

- Ingests `data/synthetic/{doc,adr,ticket,chat,meeting,session}` into tenant `eval` once (resumes if partial; aborts on ingest errors, for example GPU OOM when another process holds the GPU, so use `NEO_DEVICE=cpu` on a shared GPU). `--reingest` wipes the tenant first.
- Fixed `now` = 2026-10-16T00:00Z. Configs (ablation via `channels=`): vector, bm25, vector+bm25, vector+bm25+graph, vector+bm25+temporal, full (all four, intent weights), full-graph, auto (product default routing).
- Metrics (`metrics.py`, unit-tested in `tests/test_eval_metrics.py`): Hit, Recall, FullCover, MRR, AnswerIn at k=5 and 10 over unique doc ids; plus `ask` AnswerInAsk and `who` top-3 checks.
- `metrics.paired_bootstrap(a, b, n=1000, seed=0)` gives the mean delta and 95% CI over questions; the tuner reuses it as its noise band.
- Output: `results.md` (tables), `results.json` (per-question rankings for failure analysis).
