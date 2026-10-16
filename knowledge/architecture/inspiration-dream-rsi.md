---
type: Research Finding
title: Dream-RSI and dreaming for the agent memory graph
description: What Dream-RSI (zhengkid/Dream-RSI, arXiv 2609.14858) is, whether its history-as-replay-simulator idea fits a falkordblite agent memory graph without training, and a scoped recommendation.
resource: https://github.com/zhengkid/Dream-RSI
tags: [inspiration, self-improvement, memory, consolidation, draft]
status: draft
generated: { by: claude-haiku-5-5/self-improvement-agent, at: 2026-10-16T08:20:18Z }
stale_after: 2026-10-18T18:29:00Z
verified: { by: process:cross-check, at: 2026-10-16T08:20:18Z }
sources:
  - id: readme
    resource: https://raw.githubusercontent.com/zhengkid/Dream-RSI/main/README.md
    title: Dream-RSI README
  - id: repo-api
    resource: https://api.github.com/repos/zhengkid/Dream-RSI
    title: GitHub repository metadata
  - id: repo-tree
    resource: https://api.github.com/repos/zhengkid/Dream-RSI/git/trees/HEAD?recursive=1
    title: GitHub repository file tree
  - id: releases
    resource: https://api.github.com/repos/zhengkid/Dream-RSI/releases/latest
    title: GitHub latest release (404)
  - id: citation
    resource: https://raw.githubusercontent.com/zhengkid/Dream-RSI/main/CITATION.cff
    title: CITATION.cff
  - id: paper
    resource: https://github.com/zhengkid/Dream-RSI/blob/main/papers/Dream-RSI.pdf
    title: Dream-RSI paper (PDF in repo)
  - id: arxiv-abs
    resource: https://arxiv.org/abs/2609.14858
    title: arXiv 2609.14858 abstract page
  - id: arxiv-api
    resource: http://export.arxiv.org/api/query?id_list=2609.14858
    title: arXiv API entry for 2609.14858
  - id: project-page
    resource: https://www.dream-rsi.com
    title: Dream-RSI project page
  - id: hack-tracks
    resource: /hackathon/judging-and-prizes.md
    title: Graph Hacks judging and prizes (bundle)
evidence:
  - { file: references/evidence/self-improvement/dream-rsi/repo-readme.txt, sha256: 88d12a26bc683b49b74824488d40661ea91ad28feac25566aa4d1ef8fa064747, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/repo-api.json, sha256: c6475a444c053fb10ea67f48e46d195b8dde1a3db4797c61440ca76de1a80f06, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/repo-tree.json, sha256: c604206ac99249a50b8b7ec3a5981abe25f4013a49ddab314de6033326d401ef, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/repo-contents-root.json, sha256: 30c5c335a2c3a9c333c35bf9fccb0a8041d6b184d06a71a2275282ffe81d25d6, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/repo-releases-latest.json, sha256: 3be3b9547eef51cc49a1de5d482554e118735d9b860dd24f5cf1b6eccc3ab69e, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/repo-citation.cff, sha256: fefb67e343b06255c91876c3ad5dd765bebe43c7017cef2a4fa8a2f2571d8e52, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/repo-paper.pdf, sha256: 5701649cd9793b29cd5fb32d727d101ad21fb23639c0d9f33c9adef826194342, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/paper-extracted.txt, sha256: 6064d1ce7f60eaf6609931538fc6c759c1bc9aa652950df84fab9d54c8f57f68, retrieved_at: 2026-10-16T08:20:18Z, method: command }
  - { file: references/evidence/self-improvement/dream-rsi/arxiv-2609.14858-abs.html, sha256: c002e325483579fa807c204175013cb54133c9388578b7846746260a9a71d3bc, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/arxiv-2609.14858-api.xml, sha256: 3e7c052cf1b8168fec17d23de2458cf5c603140153d27a56417c38b0a8cb2d0d, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
  - { file: references/evidence/self-improvement/dream-rsi/project-page.html, sha256: 1266046c2ab5a5a78ee764676c494bdf3e71d2cdd9c3760fb9c449a7c8872963, retrieved_at: 2026-10-16T08:20:18Z, method: curl }
---

# What it is

Dream-RSI is a research framework and paper from Google, Google DeepMind, University of Maryland and University of Virginia. The repository is the paper's companion. It contains only a README, a CITATION file, the paper PDF and figure assets. The README says:

> "Code is being prepared for release. See [Release plan](#release-plan)."

Its release table marks "Full codebase", "Discovered programs" and "Reproduction scripts" as "⏳ Being prepared" (evidence: `readme`). There is no source code, no LICENSE file and no GitHub release (`repo-tree`, `releases` returned 404). The repository is not a usable library.

Repository facts observed 2026-10-16 (evidence: `repo-api`): created 2026-09-13, last pushed 2026-09-16, 1458 stars, 127 forks, 5 open issues, `language: null`, `license: null`, no topics.

Paper: arXiv 2609.14858, submitted 14 Sep 2026, primary category cs.CL, 11 pages, latest version v2 (evidence: `arxiv-api`, `arxiv-abs`). The arXiv abstract says:

> "Dream-RSI is a framework for scalable and recursively self-improving exploration."

Scope of the work: it improves the exploration policy of an LLM coding agent that searches for code (algorithm engineering, math optimization, GPU kernels). It does not touch memory, retrieval or a knowledge graph (evidence: `paper`).

# How it works

The core claim, quoted from the README and paper:

> "Our key insight is that accumulated discovery history can serve as a replay simulator over the realized search space."

The loop has three stages (evidence: `readme`, `paper`):

1. Online explore. The current exploration policy drives a fixed coding agent and logs a discovery tree of attempts and scores.
2. Construct replay simulator. The tree is stored as a reusable "world".
3. Dreaming-based policy improvement. An LLM "policy-development agent" revises the exploration-policy code. Each candidate is replayed over the recorded trees at zero new executions and scored by a replay objective (paper Eq. 1: best quality minus execution cost plus a parallelism bonus). The best version is deployed online, which adds a new tree to the pool.

The paper states the replay is cheap because outcomes are already stored:

> "Because all execution outcomes are already saved in the tree, evaluating a new strategy requires only reading past records without rerunning the underlying discovery agent or evaluator."

Training: none. The paper says "Zero gradient steps on the coding agent" (evidence: `readme`, stats alt text). It does use LLM calls: the coding agent and the policy-development agent are Gemini models (Gemini-3.1 Pro, Gemini-3.7-Flash) run through the Gemini CLI, with discovery budgets of 110 to 640 agent calls per round (evidence: `paper`).

Results, as reported by the authors (not independently checked):

> "Dream-RSI outperforms standard libraries like sklearn and strong baselines while reducing agent calls by up to 162× over SimpleTES and 1.7× over fixed-exploration baselines."

Counts disagree across the sources. The README badge (rendered text "8 tasks across 3 domains"), the paper introduction says "8 scientific discovery tasks spanning three distinct domains", and the arXiv abstract says "Across 9 tasks in 4 domains" (evidence: `readme`, `paper`, `arxiv-api`). Treat the task count as unresolved.

# Fit for the Neo-Cortex memory graph

## What transfers

- The idea of logging a structured history of decisions with their outcomes, then evaluating alternative policies offline over that log, is general. A memory graph has the same raw material: episodes, the facts extracted from them, and later retrieval uses.
- A "dream" job can be cheap and deterministic. It needs no training.

## What does not transfer

- The paper's replay is exact only because the recorded tree already holds the outcome of every action an alternative policy might take. Memory consolidation has no such record. If the dream job merges two nodes or promotes a fact, there is no recorded outcome for the path not taken. Counterfactuals are therefore not free. Any evaluation needs fresh labels, such as held-out queries.
- Dream-RSI's objective is a scalar code-execution score. A memory graph has no such score. Its quality signal would be retrieval relevance or agent usefulness, and that must be labelled.
- The policy-improvement step depends on repeated LLM revisions of executable code. That is expensive and out of scope for a hackathon.
- No code is released and the repo has no license, so the implementation cannot be reused. Only the idea can be.

## Fit with hackathon tracks

Track 02 is judged on "best agents that remember across sessions and share what they know" (evidence: `hack-tracks`). Its key focus includes "Episodic, semantic, and procedural memory" (evidence: `hack-tracks`). Consolidation of episodic memory into semantic facts with provenance addresses that directly. Track 03 lists "Keeping knowledge current as things change" (evidence: `hack-tracks`), which decay and supersession also serve.

Judging hints say "the graph is doing work the agent could not do without it" (evidence: `hack-tracks`). Promoted fact nodes with `SUPPORTED_BY` edges and decay on the graph meet that. Dream-RSI's exploration-policy evolution does not.

# Recommendation

ADAPT the idea, scoped to a deterministic consolidation job. SKIP the Dream-RSI policy-evolution loop and the paper's replay objective.

Minimal version on falkordblite (illustrative, not verified against the falkordblite API):

1. Select `Episode` nodes added since the last dream run.
2. Near-duplicate merge: vector nearest-neighbour pairs above a similarity threshold, merged with provenance kept.
3. Promotion: a fact (entity-relation triple) seen in at least 3 distinct sessions becomes a `Fact` node with `SUPPORTED_BY` edges to its episodes.
4. Decay: facts with no re-observation for N days lose a confidence value. Nothing is deleted.
5. Hypotheses: co-occurring entities with high embedding similarity but no direct edge become `status: hypothesis` edges. They are promoted only when re-observed in a later session. This is the "invent and test" step, and the test is re-observation.
6. Reflection (optional): one LLM call per dream run writes a `Reflection` node linked to its source episodes.

Effort estimate, with about 2.4 days left (deadline 2026-10-18 18:29 UTC, per `hack-tracks` and the bundle checklist):

- Steps 1 to 4 with asserts: about 5 to 7 hours.
- Step 5 and the MCP trigger: about 2 hours.
- A before/after demo on a small seeded dataset: about 2 hours.
- Total: about 9 to 11 hours. Do it only after the core retrieval and session extraction path works. Drop step 5 first if time is short.

The demo should show a query whose answer changes after a dream run, not a claim that "the memory improves itself." Describe it as consolidation, not recursive self-improvement, in the submission.

# Open questions

- Does falkordblite's vector index support the nearest-neighbour query needed for step 2 at the expected memory size? Check against the falkordblite notes in this bundle before building.
- Track 02 judges may treat "memory improves itself" as a claim. Whether the judges accept consolidation as sufficient is not stated in the bundle (see `hack-tracks`, which says the scoring rubric was not published).
- The paper's task count is inconsistent (8 across 3 domains vs 9 across 4). Only the authors can resolve it. Do not cite a number in the submission without that.
- The code release is "being prepared". If a license and code appear, re-check whether the replay objective is worth adapting. Re-check on or after 2026-10-18.
- Whether the author-reported results (162×, 2.09×) hold under independent reproduction is unknown. Nothing here was run.

# Evidence

Stored in `references/evidence/self-improvement/dream-rsi/`. Method: `curl` for raw GitHub and API, `curl` for arXiv abs and API, `curl` for the project page, `pdftotext -layout` to derive `paper-extracted.txt` from the PDF. The hashes were recorded together at 2026-10-16T08:20:18Z.

- `repo-readme.txt` — sha256 88d12a26bc683b49b74824488d40661ea91ad28feac25566aa4d1ef8fa064747
- `repo-api.json` — sha256 c6475a444c053fb10ea67f48e46d195b8dde1a3db4797c61440ca76de1a80f06
- `repo-tree.json` — sha256 c604206ac99249a50b8b7ec3a5981abe25f4013a49ddab314de6033326d401ef
- `repo-contents-root.json` — sha256 30c5c335a2c3a9c333c35bf9fccb0a8041d6b184d06a71a2275282ffe81d25d6
- `repo-releases-latest.json` — sha256 3be3b9547eef51cc49a1de5d482554e118735d9b860dd24f5cf1b6eccc3ab69e (404 response; recorded as a finding, not an error)
- `repo-citation.cff` — sha256 fefb67e343b06255c91876c3ad5dd765bebe43c7017cef2a4fa8a2f2571d8e52
- `repo-paper.pdf` — sha256 5701649cd9793b29cd5fb32d727d101ad21fb23639c0d9f33c9adef826194342
- `paper-extracted.txt` — sha256 6064d1ce7f60eaf6609931538fc6c759c1bc9aa652950df84fab9d54c8f57f68
- `arxiv-2609.14858-abs.html` — sha256 c002e325483579fa807c204175013cb54133c9388578b7846746260a9a71d3bc
- `arxiv-2609.14858-api.xml` — sha256 3e7c052cf1b8168fec17d23de2458cf5c603140153d27a56417c38b0a8cb2d0d
- `project-page.html` — sha256 1266046c2ab5a5a78ee764676c494bdf3e71d2cdd9c3760fb9c449a7c8872963

The `SHA256SUMS.txt` file in the same directory lists these hashes.
