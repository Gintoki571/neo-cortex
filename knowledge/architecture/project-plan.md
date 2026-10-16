---
type: Design Proposal
title: Neo-Cortex stack decisions and risks
description: Proposed stack (falkordblite, graphrag-sdk, GLiNER2.5, EmbeddingGemma, anydoc, OKF) checked against the verified findings, with blockers, fallbacks and a 2.9-day order of work.
tags: [architecture, plan, risks, hackathon, draft]
status: draft
generated: { by: claude-sonnet-5-5/orchestrator, at: 2026-10-15T20:30:00Z }
stale_after: 2026-10-18T18:29:00Z
sources:
  - id: hack-rules
    resource: /hackathon/rules.md
    title: Hackathon rules
  - id: fl-test
    resource: /falkordblite/capabilities-test.md
    title: falkordblite capability test
  - id: fl-limits
    resource: /falkordblite/limitations-and-open-issues.md
    title: falkordblite limitations
  - id: grag-conn
    resource: /graphrag-sdk/db-connectivity.md
    title: GraphRAG-SDK DB connectivity
  - id: grag-plug
    resource: /graphrag-sdk/pluggability.md
    title: GraphRAG-SDK pluggability
  - id: gliner
    resource: /models/gliner2-5-base.md
    title: GLiNER2.5 base
  - id: egemma
    resource: /models/embeddinggemma.md
    title: EmbeddingGemma
  - id: lx
    resource: /extraction/langextract-pipeline-design.md
    title: LangExtract pipeline design
  - id: anydoc
    resource: /extraction/anydoc-test-results.md
    title: anydoc test results
---

# Status

Design proposal. Each claim links to the concept that holds its evidence. Deadline: submissions close 2026-10-18 18:29 UTC.[^hack-rules]

# Decisions and what the evidence says

| Choice | Verdict | Evidence |
|--------|---------|----------|
| falkordblite as the DB | Works. Vector index, fulltext, weighted `algo.SPpaths`, persistence and restart all passed. Core is 4.18.3, Python >=3.12, no Windows wheel.[^fl-test] | verified by running |
| Is an embedded DB "FalkorDB" for the hackathon rule? | Likely fine but not named. Rule 4: "Run FalkorDB however suits you. Docker, a self-hosted instance, and FalkorDB Cloud are all accepted". falkordblite bundles a real FalkorDB module, but confirm with organisers.[^hack-rules] | ask on Discord, keep a Docker path ready |
| graphrag-sdk 1.4.0 on falkordblite | Works unmodified if the embedded server is started with a TCP port bound to 127.0.0.1 and `ConnectionConfig` points at it. Full ingest, finalize, retrieve and completion passed.[^grag-conn] | verified by running |
| Custom extractor and embedder in graphrag-sdk | Interfaces exist (`EntityExtractor`, `Embedder`, strategy ABCs); a regex NER and a hash embedder ran end to end. The relation step still needs an LLM.[^grag-plug] | verified by running |
| GLiNER2.5 for extraction | Model exists (Apache-2.0, 194M). Not yet run by anyone here. No published benchmarks in its card.[^gliner] | untested |
| EmbeddingGemma for embeddings | `google/embeddinggemma-2` exists, ungated, 768-d, Matryoshka. Licence text is inconsistent. No ONNX or quantised files.[^egemma] | card only, not run |
| anydoc for Office to Markdown | Local, keyless, docx and xlsx tested clean. pptx, odt, epub untested; image PDFs need OCR.[^anydoc] | verified by running |
| LangExtract | Reuse its chunker, data classes and grounding idea. Do not use its LLM-centric provider seam for GLiNER.[^lx] | source read, one bug reproduced |

# Blockers and fallbacks

1. **Version drift.** The released GraphRAG-SDK 1.4.0 ranks vector results wrongly (exact match comes last, issue #294), fixed on main. Install from main or patch the ordering. Also, FalkorDB 6.0.2 rejects `createNodeIndex` (issue #344), so pin the 4.x core that falkordblite bundles.
2. **Hosted LLM still needed.** GraphRAG-SDK's relation extraction and answer generation need an LLM. Pick a provider early; the hackathon rules ask for AI-use disclosure.
3. **Network exposure.** The embedded server listens on all interfaces by default when TCP is on. Always set `bind` to 127.0.0.1.
4. **Orphan processes and 3.2 s shutdown** in falkordblite. Wrap start and stop in one helper and kill the child on exit.
5. **License questions** (SSPL plus Elastic text in FalkorDB, unclear licence in falkordblite). State them in the README; do not guess.

# Suggested order of work (superseded)

Superseded on 2026-10-16 by the [unified build plan](/architecture/unified-plan.md). GLiNER2.5 and EmbeddingGemma have now been run; see the [spike](/architecture/spike-2026-10-16.md). The unified plan removes the hosted-LLM dependency (blocker 2).

Original order:


1. Day 1 morning: repo skeleton, one `Store` class that starts falkordblite on 127.0.0.1 and hands out a graphrag-sdk `ConnectionConfig`. Ingest one markdown file end to end.
2. Day 1 afternoon: run GLiNER2.5 on this bundle's own text and on one real agent session. Decide go/no-go on it versus an LLM extractor, using the gold-set method in [classification use cases](/architecture/classification-usecases.md).
3. Day 2: add anydoc ingestion, EmbeddingGemma embeddings (check dimension, prompt prefixes), and two System 1 decisions (assertion gating and entity resolution).
4. Day 2 evening: the agent demo that makes the graph do visible work (rule: graph must do real work), plus OKF export of the graph back to a bundle.
5. Day 3: README (setup, data model, Cypher and algorithms used), demo video, AI-use disclosure, submit before the deadline with margin.

# Open questions

- Does the hackathon accept an embedded FalkorDB? (Ask organisers.)
- Which LLM provider and key will be used, and does it fit the free credits, if any?
- Does GLiNER2.5 handle long, messy agent sessions? Unknown until run.

[^hack-rules]: Hackathon rules
[^fl-test]: falkordblite capability test
[^grag-conn]: GraphRAG-SDK DB connectivity
[^grag-plug]: GraphRAG-SDK pluggability
[^gliner]: GLiNER2.5 base
[^egemma]: EmbeddingGemma
[^anydoc]: anydoc test results
[^lx]: LangExtract pipeline design
