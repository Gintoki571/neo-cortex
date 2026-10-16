---
type: Design Proposal
title: Fast-classifier ("System 1") use cases for Neo-Cortex
description: Brainstormed places where a small, probability-returning classifier can make graph micro-decisions, ranked by value for the hackathon, with what each needs and how to test it.
tags: [architecture, classification, graphrag, gliner2, draft]
status: draft
generated: { by: claude-sonnet-5-5/orchestrator, at: 2026-10-15T19:50:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: jev-check
    resource: /models/jev-typesafe-claim-check.md
    title: Jev / TypeSafe claim check
  - id: s1-candidates
    resource: /models/system1-classifier-candidates.md
    title: System 1 classifier candidates
  - id: gliner25
    resource: /models/gliner2-5-base.md
    title: GLiNER2.5 base
  - id: lx-design
    resource: /extraction/langextract-pipeline-design.md
    title: LangExtract pipeline design
  - id: fl-test
    resource: /falkordblite/capabilities-test.md
    title: falkordblite capability test
---

# Status of this document

This is a design proposal, not a finding. Nothing here has been run. The facts it leans on are linked and carry their own evidence. Every threshold below is a starting guess to be calibrated on a gold set (see "How to test").

# The idea in one paragraph

Use an LLM only for open-ended synthesis ("System 2"). Use a small model that returns a label plus a score ("System 1") for the high-frequency yes/no/choice decisions inside ingestion and retrieval. The user's brief describes this with TypeSafe's Jev. Jev is real but is a hosted API with early access and no downloadable weights, and only some of the claimed uses have any published support.[^jev-check] So the plan is to code against a tiny `decide()` interface and back it with GLiNER2.5 classification first (local, Apache-2.0),[^gliner25] with Jev or an NLI cross-encoder swappable behind it.[^s1-candidates]

# Interface

```python
decide(kind: "boolean" | "choice" | "score", question: str, context: str, labels: list[str] | None) -> Decision(label, score, backend)
```

Store `score`, `backend`, and a version on the graph element the decision touched, so decisions are auditable and re-runnable.

# Use cases, ranked

| # | Use case | Stage | Decision type | Support found | Needs |
|---|----------|-------|---------------|---------------|-------|
| 1 | Assertion gating: asserted / negated / hypothetical / conditional on each extracted relation | ingest | choice | one third-party write-up, single synthetic corpus, precision 0.279 to 0.404 (see Jev check) | extractor spans plus the sentence |
| 2 | Ontology-bound relation selection: pick one predefined edge type | ingest | choice | partial, same write-up | fixed ontology in `labels` |
| 3 | Entity resolution: embedding nearest neighbours propose pairs, classifier decides merge | ingest | boolean | same write-up | vector index (verified in falkordblite) |
| 4 | Query routing: vector, graph, both, or none | query | choice | vendor material only | a tiny labelled query set |
| 5 | Subgraph pruning: score candidate nodes of a k-hop expansion against the question | query | score | NOT found in any Jev source; our own idea | Cypher expansion plus batch scoring |
| 6 | Grounding check: is each answer sentence supported by retrieved facts | answer | boolean | vendor use case, no study | answer sentences and the retrieved subgraph |
| 7 | Weighted pathfinding: store scores as edge weights, run shortest paths | query | score | mechanism verified in falkordblite, quality unknown | `algo.SPpaths` with `weightProp`[^fl-test] |

# Extra ideas specific to agent sessions and documents

These are not in the brief. They fit a "memory for agents" product, which is where this project sits.

1. **Turn typing** for agent sessions: decision, error, fix, user preference, TODO, chit-chat. Cheap first pass that decides what is worth extracting at all.
2. **Memory-worthiness**: score whether a candidate fact is durable or ephemeral, so the graph does not fill with noise.
3. **Supersession**: when a new fact conflicts with an older one about the same entity, classify `same / contradicts / refines / unrelated` and mark the old edge `deprecated`. This maps directly onto OKF `status` and `stale_after`.
4. **Ingest routing**: classify the document type (code, spec, chat log, table) to pick the extraction recipe, before touching GLiNER or an LLM.
5. **Source trust**: derive OKF-style trust tier from signals (author, recency, verification) instead of storing a verdict.
6. **Escalation gate**: if the System 1 score is in a band near its threshold, escalate that single item to the LLM. This makes the cost/quality trade-off explicit and measurable.

# Risks to state in the submission

- GLiNER scores are model confidences, not calibrated probabilities. Calibrate per task before using fixed thresholds like 0.92.
- GLiNER2.5 has no published benchmark numbers in its card, and its quality on long, messy agent sessions is untested.[^gliner25]
- Subgraph-pruning and "90% fewer tokens" style claims are unverified for any model.

# How to test (small and honest)

1. Build a gold set of about 100 items per use case from this bundle's own text.
2. For each use case, compare: GLiNER2.5, an NLI cross-encoder, and an LLM baseline.
3. Report precision/recall at the chosen threshold plus latency per item on this machine's CPU.
4. Keep only the use cases that beat the no-classifier baseline. Ship two or three, not seven.

[^jev-check]: Jev / TypeSafe claim check
[^s1-candidates]: System 1 classifier candidates
[^gliner25]: GLiNER2.5 base
[^lx-design]: LangExtract pipeline design
[^fl-test]: falkordblite capability test
