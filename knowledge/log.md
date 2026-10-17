# Directory Update Log

## 2026-10-17
* **Creation**: Added [System 1 models in knowledge-graph pipelines](/extraction/system1-models-in-graphs.md) (type: Research Note, stable): GLiNER-family and label-set classifier results by job (extract, type, relate, resolve, verify, escalate, agent-written graphs), measured numbers kept apart from opinion, source conflicts listed. Ten sources copied to `references/evidence/extraction/system1-*` with sha256 in the note's frontmatter and `SHA256SUMS.txt`. Copies are the research pass's obscura fetches; `retrieved_at` is the research pass's save time (UTC), not a fresh fetch. Quotes checked against the copies; no fact is marked `verified` because nothing was re-run or independently confirmed.
* **Creation**: Added draft [System 1 adoption plan](/extraction/system1-adoption.md) (type: Design Proposal): seven ranked ideas for Neo-Cortex with impact, effort, source and file; what `src/neo_cortex/` already does; gaps found in code (soft-band judge can create merges at `src/neo_cortex/resolve.py:121`, against the comment at line 16 and the package doc; hedges are not covered by `_NEG`; agent-written relations skip extraction checks); do-not-adopt list.
* **Update**: [extraction index](/extraction/index.md) lists both notes, System 1 headline findings and source conflicts.
* **Correction**: the Relex paper's Table 2 and its text disagree on the GLiNER2 row (table 32.9 / 11.7 / 20.8 / 6.0; text 34.1 / 12.4 / 16.8 / 4.9) and on GLiREL DocRED (table 2.4, text 2.2); the note cites the table and records both. The Decide gate F1 is 0.396; an earlier research draft's 0.404 is the hosted Jev gate.

## 2026-10-16
* **Creation**: Added [build status](/architecture/build-status.md) (type: Status Report, stable): what was actually built versus the [unified plan](/architecture/unified-plan.md), key design changes (graph channel became Personalized PageRank; product pivoted to graph-native answer tools impact/who/timeline/relate after document retrieval tied text; relation recall 0.41 -> 0.83; session extraction deterministic-first; RRSI tuner built but rejected its own weights), final eval numbers copied from `eval/results.md` / `eval/answers.md` / `eval/graph_quality.md` / `eval/stress.md`, and open risks. Unified plan now points to it under its Status section.

## 2026-10-16
* **Creation**: Added [stack spike](/architecture/spike-2026-10-16.md) (executed; evidence in `references/evidence/architecture/spike-2026-10-16/`) and draft [unified build plan](/architecture/unified-plan.md), which supersedes the order of work in [project plan](/architecture/project-plan.md).
* **Creation**: Added draft [Dream-RSI inspiration](/architecture/inspiration-dream-rsi.md) with sha256-recorded evidence under `references/evidence/self-improvement/dream-rsi/`; indexed in [architecture](/architecture/index.md).
* **Creation**: Added draft [RRSI inspiration](/architecture/inspiration-rrsi.md) with evidence under `references/evidence/self-improvement/rrsi/` (repo, paper, source files, sha256 in SHA256SUMS.txt).

## 2026-10-16
* **Creation**: Added draft [pg-jev inspiration](/architecture/inspiration-pg-jev.md) with sha256-recorded evidence in `references/evidence/self-improvement/pg-jev/`. Recommendation: adapt narrowly (cached probability properties on falkordblite), not port.

## 2026-10-15
* **Creation**: Initialised the bundle with the [research protocol](/references/research-protocol.md) and the OKF v0.2 spec copy.
* **Creation**: Seven research passes added [hackathon](/hackathon/index.md), [falkordblite](/falkordblite/index.md), [falkordb](/falkordb/index.md), [graphrag-sdk](/graphrag-sdk/index.md), [models](/models/index.md), [extraction](/extraction/index.md) and [okf](/okf/index.md), with sha256-recorded evidence.
* **Update**: Orchestrator fixed unparseable frontmatter (hackathon), date-only `stale_after` values (graphrag-sdk), an empty evidence hash (falkordblite), and renamed `.md` evidence files to `.md.txt`.
* **Creation**: Added draft [project plan](/architecture/project-plan.md) and [classification use cases](/architecture/classification-usecases.md).
