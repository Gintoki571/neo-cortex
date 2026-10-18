# Ideas taken from open memory systems, measured (2026-10-18)

Seven small retrieval/resolution changes inspired by agentmemory, graphify and Hindsight were added behind environment flags (default off) and measured on two corpora: the synthetic company (80 questions, `eval/run_eval.py --configs full,auto`) and this repository's own docs (30 questions, `eval/real_check.py`, one shared graph). Same code, same graph, only the flag changes. n is small (30 real questions), so differences of 0.03-0.07 are one or two questions and inside the noise band.

| Flag(s) | Idea (source) | Synthetic recall@10 full (base 0.75) | Synthetic multi fullcover@10 (base 0.38) | Real Hit@5 / MRR / out5 / chunk5 (base 0.50 / 0.41 / 0.43 / 0.70) | Verdict |
|---|---|---|---|---|---|
| `NEO_FUSE_NORM` + `NEO_FUSE_BOOST` | normalise ranks before RRF, bounded recency/window/proof boosts (agentmemory) | 0.73 | 0.35 | 0.57 / 0.38 / 0.47 / 0.73 | Off: no gain |
| `NEO_BM25_COVER` + `NEO_WHY_TIER` | squared term-coverage BM25 rescore, why-question tier (graphify) | 0.74 | 0.31 | 0.60 / 0.37 / 0.50 / 0.80 | Off: real Hit@5 +0.10 but MRR -0.04, synthetic -0.01 to -0.07 |
| `NEO_SEED_PER_TERM` + `NEO_HUB_SKIP` | per-term graph seeds, skip hub entities (graphify) | 0.74 | 0.38 | 0.50 / 0.41 / 0.43 / 0.70 | Off: no change |
| `NEO_TEMPORAL_2PHASE` | two-phase temporal: candidates first, then date ordering (Hindsight) | 0.75 | 0.27 | 0.50 / 0.41 / 0.43 / 0.70 | Off: temporal fullcover 0.44 -> 0.56 but multi-hop 0.38 -> 0.27 |
| all retrieval flags together | | n/a | n/a | 0.60 / 0.37 / 0.50 / 0.83 | Off |
| `NEO_RESOLVE_JW` | Jaro-Winkler entity merge plus shared-neighbour boost (graphify) | n/a (ingest time) | n/a | 0.57 / 0.41 / 0.47 / 0.77; 594 -> 573 entities | Off: it merged `FalkorDB` into `falkordblite`, two different things |

What this says:
- On the synthetic corpus no flag beats the default overall; the temporal flag trades multi-hop for temporal questions.
- On real docs the lexical flags help Hit@5 and answer-in-chunks by 0.07-0.13 but lower MRR (the right document is in the top 5 more often and first less often). With 30 questions this is not a reliable win, so the product default is unchanged.
- The entity-resolution flag removes 21 duplicate entities but made a wrong merge of two products; a wrong merge is worse than a duplicate (it corrupts owners and impact), so it stays off.
- The flags remain in the code as opt-in experiments with unit tests (`tests/test_retrieve.py`, `tests/test_resolve.py`).

Raw per-run reports are not kept; to reproduce: `NEO_BM25_COVER=1 uv run --no-sync python eval/real_check.py` on an ingested `real` tenant, and the same for `eval/run_eval.py`.
