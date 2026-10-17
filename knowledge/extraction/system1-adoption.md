---
type: Design Proposal
title: 'System 1 adoption plan for Neo-Cortex (ranked ideas)'
description: 'Ranked, deadline-aware proposals for using System 1 encoders in Neo-Cortex extraction, resolution, verification and retrieval, each with expected impact, effort, its supporting source and the file it would touch.'
resource: /extraction/system1-models-in-graphs.md
tags: [extraction, system-1, design, proposal, neo-cortex, gliner, resolution, verification]
status: draft
generated: { by: claude-haiku-5-5/extraction-agent, at: 2026-10-17T05:50:00Z }
stale_after: 2026-10-18T18:29:00Z
sources:
  - id: concept
    resource: /extraction/system1-models-in-graphs.md
    title: 'System 1 models in knowledge-graph pipelines (this bundle)'
  - id: build-status
    resource: /architecture/build-status.md
    title: 'Neo-Cortex build status (eval numbers, design changes)'
---

# System 1 adoption plan for Neo-Cortex

This is a draft. The evidence is in [/extraction/system1-models-in-graphs.md](/extraction/system1-models-in-graphs.md), and each number is quoted there with its evidence file. Code facts below were read from `src/neo_cortex/` on 2026-10-17 at the line numbers given. Nothing here was run: the machine is short on RAM, and no model or test was executed for this note.

Submissions close 2026-10-18 18:29 UTC. Ideas 1 and 2 need only unit tests with fake models. Ideas 3, 4 and 6 need one eval run each. Idea 7 is post-deadline.

## What Neo-Cortex already does

- **Entities:** GLiNER2.5 base with descriptive labels, per-type confidence floors (`extract.py`).
- **Relations:** per-sentence GLiNER relations (windows of at most 40 words) plus about 40 deterministic patterns at confidence 0.9. `RELATED_TO` is whitelisted but never extracted. Relation floors are 0.6 and 0.7 (`extract.py`).
- **Negation:** a 40-character lookbehind `_NEG` (`extract.py:387`) blocks "not / never / no longer / n't / without" within three words before a pattern match, and it is applied in `_relations` (`extract.py:549`).
- **Classification:** `classify_memory` and `worth_keeping` read the full softmax, not just the winner (`extract.py`, `session_mem.py`).
- **Resolution:** exact key, alias, lone person name, then vector neighbours with `_guard`. `HARD` is 0.92 and `SOFT` is 0.85. Judge results are cached as `Judgment` nodes (`resolve.py`).
- **Agent-direct writes:** `remember(entities=, relations=)` skips GLiNER and writes through `_edge`. `relate(end=)` closes edges (`tools.py`, `write.py`).
- **Consolidation:** dream merges, promotes, decays and flags conflicts with no LLM and never deletes (`dream.py`).
- **Retrieval:** Personalized PageRank graph channel, with soft intent weights in `channel_weights` (`retrieve/channels.py`).

## Gaps found in this pass

- **G1, judge direction.** `resolve.py:121` merges a soft-band pair (0.85 to 0.92) when the judge's `same` is at least 0.5. The comment at `resolve.py:16` and `src/neo_cortex/AGENTS.md` say the judge may only veto. The code lets the judge create the merge. The base judge is a GLiNER choice model that the code's own comment calls close to chance on bare names. The concept note's Decide measurement (6 of 11 false merges for a names-only judge) points the same way, though it is a different model.
- **G2, hedges.** `_NEG` covers negators only. It does not catch hedges or forecasts without a negator ("expects to", "may", "plans to"). Pattern edges are stored at confidence 0.9 regardless.
- **G3, agent-written relations.** `remember(relations=)` and `relate()` do not pass through the extraction checks, and the docs do not say they should.
- **G4, cross-sentence relations.** Relation windows are sentence-scoped, so a relation across two sentences is never a candidate. `build-status` reports CAUSED_BY recall 0 of 5 ([/architecture/build-status.md](/architecture/build-status.md)).

## Ranked ideas

| # | Idea | Expected impact | Effort | Supporting source | File(s) it touches |
|---|---|---|---|---|---|
| 1 | Make the soft-band judge match its documented role (veto-only, or a documented create rule) and test guard-passing soft-band pairs | High: wrong merges spread to every linked fact; direction is a contradiction, not a tuning choice | Low: one branch and tests | [/extraction/system1-models-in-graphs.md](/extraction/system1-models-in-graphs.md) (entity resolution: names-only judge 6 of 11 false merges; Decide: "It cannot say whether two mentions are the same thing") and gaps G1 | `src/neo_cortex/resolve.py` (lines 16, 119 to 123), `tests/test_resolve.py`, `src/neo_cortex/AGENTS.md` (resolver paragraph) |
| 2 | Extend the lookbehind from negation to hedges and forecasts on pattern edges ("expects to", "may", "plans to") | Medium: fewer hedged claims stored as facts at confidence 0.9 | Low: a short word list and controls | Concept, edge verification (Decide window counts: 25 forecast, 12 not stated, 6 possibility, 4 denial of 170 edges; a different corpus) and gap G2 | `src/neo_cortex/extract.py` (`_NEG`, `hit` in `_relations`), `tests/test_write.py` |
| 3 | Store a modality verdict and P(fact) on each edge; filter the graph channel and the `impact`/`ask` paths on it | High on the one measured case: F1 0.330 to 0.396 on the 10-document corpus with no gold triple lost | Medium: a 340M English classifier (about 1.9 GB, 72 ms per text on CPU); needs an eval run and RAM | Concept, edge verification; Jev post (store the verdicts, the gate becomes a filter) and gap G3 | `src/neo_cortex/extract.py`, `write.py` (`_edge`, `remember` relations), `retrieve/channels.py`, `src/neo_cortex/AGENTS.md` (REL properties contract) |
| 4 | Add two-sentence relation candidates capped well under the ~400-word effect; measure against the current eval | Medium, unknown: recall is 0.825 and CAUSED_BY is 0 of 5, which this would test | Low to medium: a window builder change plus one eval run | Concept, relation extraction (400-word effect; a relation across windows cannot be decoded) and [/architecture/build-status.md](/architecture/build-status.md) (recall 0.825, precision 0.880) and gap G4 | `src/neo_cortex/extract.py` (window builder near line 288), `eval/graph_quality.py` (read only) |
| 5 | Surface ambiguity as a review list (soft-band pairs, not-stated or forecast edges) returned by an existing read tool; the calling agent resolves it with `remember(supersedes=)` or `relate(end=)` | Medium: keeps ambiguity visible instead of silently split or merged; fits the no-LLM-inside rule | Medium | Concept, escalation (the Haiku cascade gained nothing; "a larger language model is not that person"); FalkorDB's Unknown band (opinion) | `src/neo_cortex/resolve.py` (return review pairs without merging), `src/neo_cortex/tools.py` (`brief` or `ask` output; keep it to counts and the top N) |
| 6 | Gate the graph channel on seed quality: give PPR weight only when a query entity links at 0.65 or more without the mention-only fallback | Medium: the graph channel currently ties text retrieval; the interval includes zero | Low | [/architecture/build-status.md](/architecture/build-status.md) (delta -0.002 [-0.031, +0.031], n=80) | `src/neo_cortex/retrieve/channels.py` (`link_entities`, `graph`, `channel_weights`); keep only if the paired bootstrap in `eval/results.md` moves |
| 7 | Benchmark GLiNER-Relex on the eval set, as a benchmark only | Unknown: a document-level result on DocRED (31.3, against 11.7 or 12.4 for GLiNER2) but a different domain; FewRel is weak | Medium: DeBERTa-v3-large, RAM-heavy | Concept, relation extraction (GLiNER-Relex paper; the text and table disagree on GLiNER2) | `scripts/bench_models.py` (benchmark only; no loader in `src/` until it wins) |

Ranking logic: ideas 1 and 2 are cheap and fix a risk in code that already runs. Idea 3 has the largest measured lift, but it needs a second model and a clean label set first. Ideas 4 and 6 need one eval each. Idea 7 is an experiment for after the deadline.

## Do not adopt

- **LLM escalation inside the system** for uncertain edges. The Jev cascade gave 0.400 against 0.404 with no escalation, and Haiku got 0 of 6 gold-same pairs right. Use the review list in idea 5 instead.
- **Classifier relation selection over all co-occurring pairs.** Decide selection reached F1 0.133 against 0.330 for GLiNER's joint output. Use the verifier only on candidates GLiNER proposed.
- **GLiREL for multi-sentence company text.** The table gives 2.4 on DocRED and 1.4 on CrossRE, even with gold entities.
- **A System-1 same-entity judge that creates merges.** See G1.
- **Second-opinion typing to widen blocking.** The Decide recall gain came from type-scoped blocking. Neo-Cortex's vector candidate query is not type-scoped (`resolve.py:117` queries all Entities, and type enters only through `_guard`), so that gain does not apply here. The same widening produced a wrong merge in the Decide corpus.
- **Yes/no phrasing for modality checks.** It kept 0 of 5 controls in the Decide test. If idea 3 goes ahead, use short concept labels.

## Open questions

- Whether the GLiNER2.5 base checkpoint's own classification head can reproduce the Decide gate. All Decide numbers come from the separate Decide model.
- Whether `_NEG` also applies to GLiNER-proposed edges. This pass read `_relations` only, and did not confirm the path.
- How many soft-band merges the current graph contains (idea 1 needs this count before and after).
- Whether a one-word name tail-merges into a longer name in practice, for example a generic `gateway` merging into `payments gateway` when the judge says same. The guard allows tail matches by design. Test it before deciding.
- The evaluation numbers quoted above come from one author's corpus of 10 documents (47 gold triples). Re-measure on the Neo-Cortex eval set (`eval/`) before quoting any of them.
