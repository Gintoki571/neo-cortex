# Design proposals

* [Build status](build-status.md) - what was actually built versus the unified plan: done/changed/cut with reasons, key design changes (PPR graph channel, graph-native answer tools), final eval numbers, open risks (stable)
* [Unified build plan](unified-plan.md) - the current plan: one system for all three tracks, data model, hybrid RRF retrieval, MCP tools, eval, timeline (draft)
* [Stack de-risking spike](spike-2026-10-16.md) - first real runs of GLiNER2.5, EmbeddingGemma 2, falkordblite full-text/temporal/algorithms and MCP SDK 2.x
* [Stack decisions and risks](project-plan.md) - proposed stack checked against verified findings, blockers, fallbacks, 2.9-day order of work
* [Fast-classifier use cases](classification-usecases.md) - where a small probability-returning model can make graph micro-decisions, and how to test them
* [pg-jev inspiration](inspiration-pg-jev.md) - what the Jev-judged Postgres extension does, and a narrow adapt-don't-port recommendation for falkordblite (draft)
* [RRSI inspiration](inspiration-rrsi.md) - Google's regularized harness self-improvement loop (no training): what transfers to memory tuning, recommendation (adapt, ~7 h), open questions
* [Dream-RSI and memory consolidation](inspiration-dream-rsi.md) - what Dream-RSI is, whether its replay-simulator idea fits the agent memory graph without training, and a scoped consolidation recommendation
