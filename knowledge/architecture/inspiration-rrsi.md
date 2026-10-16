---
type: Design Proposal
title: RRSI (Regularized Recursive Self-Improvement) as an inspiration for memory self-improvement
description: What google-research/rrsi does (a regularized search that edits an agent harness against a benchmark, no model training), which parts could transfer to a falkordblite agent-memory graph without training, and a recommendation with effort estimate.
resource: https://github.com/google-research/rrsi
tags: [architecture, self-improvement, rrsi, agent-memory, retrieval-tuning, draft, inspiration]
status: draft
generated: { by: claude-haiku-5-5/self-improvement-agent, at: 2026-10-16T08:22:00Z }
verified: { by: process:cross-check, at: 2026-10-16T08:22:00Z }
stale_after: 2026-10-18T18:29:00Z
sources:
  - id: repo
    resource: https://github.com/google-research/rrsi
    title: google-research/rrsi GitHub repository
    last_modified: 2026-10-16T05:58:24Z
  - id: readme
    resource: https://raw.githubusercontent.com/google-research/rrsi/main/README.md
    title: rrsi README (main branch)
  - id: license
    resource: https://raw.githubusercontent.com/google-research/rrsi/main/LICENSE
    title: rrsi LICENSE (Apache 2.0)
  - id: arxiv
    resource: https://arxiv.org/abs/2609.24972
    title: "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses (arXiv 2609.24972)"
    last_modified: 2026-10-04T00:00:00Z
  - id: arxiv-v1
    resource: https://arxiv.org/html/2609.24972v1
    title: arXiv 2609.24972 v1 HTML (superseded)
  - id: project
    resource: https://regularized-rsi.com/
    title: RRSI project page
  - id: selection
    resource: https://raw.githubusercontent.com/google-research/rrsi/main/rrsi/selection.py
    title: rrsi/selection.py (acceptance rule)
  - id: schedule
    resource: https://raw.githubusercontent.com/google-research/rrsi/main/rrsi/schedule.py
    title: rrsi/schedule.py (annealed edit budget)
  - id: critic
    resource: https://raw.githubusercontent.com/google-research/rrsi/main/rrsi/critic.py
    title: rrsi/critic.py (leakage screen)
  - id: judging
    resource: /hackathon/judging-and-prizes.md
    title: Graph Hacks judging and prizes (bundle)
  - id: rules
    resource: /hackathon/rules.md
    title: Graph Hacks rules (bundle)
evidence:
  - { file: references/evidence/self-improvement/rrsi/api-repo.json, sha256: b3d9ff36867c601aa73087fa28071a6f0394cfcc5225b2de20c31cdbeb26c7e3, retrieved_at: 2026-10-16T08:19:57Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/api-releases-latest.json, sha256: d9e37600354c1839f6b22cebde497e9d14750d2401a06c9a51b1619baf991613, retrieved_at: 2026-10-16T08:19:57Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/api-contents.json, sha256: 62def5fe90aaa218b669717873313d5fc9d2e61648e5fccc3b5351b75d2893e0, retrieved_at: 2026-10-16T08:19:57Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/api-license.json, sha256: a7e97fd14c887611b6d04401a215641d6247bf6a3f898368875765a1deab5950, retrieved_at: 2026-10-16T08:19:57Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/raw-main-README.md.txt, sha256: 4aa475cf0dea8b281fae48ae12f8c201e05fbdb1f55b8b3d87ff3dee0dcf8a93, retrieved_at: 2026-10-16T08:19:57Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/raw-main-LICENSE.txt, sha256: cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30, retrieved_at: 2026-10-16T08:19:57Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/arxiv-abs-2609.24972.html, sha256: 8f109d006d8610683c42045fd463a0fd0f8edfdd5dfd4b89706d58077fe81e16, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/arxiv-html-2609.24972.html, sha256: 462119b1de52574679d8785d7902f865f0406f78b07758ee7fc13b2995b67750, retrieved_at: 2026-10-16T08:20:45Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/arxiv-html-text.txt, sha256: cc3b2f0a0ec0009d97719960533fa1aba8a17360a53b3ee781ab1d8c9236b32c, retrieved_at: 2026-10-16T08:20:45Z, method: command }
  - { file: references/evidence/self-improvement/rrsi/project-page.html, sha256: 66ec164d089c0c45f74a37e9de1b695edffb9b37ddcc8f5b0fe9903fe9de4d32, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/project-page-text.txt, sha256: bc02dd72add7812751f7ecb1e26da2dd24c50c0d7e45e1af48553977b7cbbb66, retrieved_at: 2026-10-16T08:20:11Z, method: command }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi-selection.py.txt, sha256: 5142043947117e3a28167fdbdddf824293e7a79bdb5f7e90a4ebc908bed7d663, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi-schedule.py.txt, sha256: fc2b5e5367b34a776c5088ed822ffcfd80f20bfe08e4864d027bea1599a4762f, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi-history.py.txt, sha256: afa808909ff873fc3e07e4d8239da57fd0bddd4be7014b8e0c63c35f04246b11, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi-critic.py.txt, sha256: 96524e4d4af1723f479b3a5ca699a685612cf9bb95e7cbd4291d17c952488afe, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi-propose.py.txt, sha256: f90aab99ef698121001477461b4d8f8fee17b5104fcbc33b0e6ec137468a7946, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi-analyst.py.txt, sha256: 2178f77361ab6e33be6ea9b594828ff99cb9642cf94638f9329b39a77dbaedb5, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi-evaluate.py.txt, sha256: e361eb0de5c56a70493757bf1036290b230ab7cacfe88f3ac86b5a36cbfead2f, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi-components.py.txt, sha256: 4b76dcfadb8bbf50e4244c25cb9354c6891db2a2e08ae782f1ef63babb7e066a, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-rrsi.py.txt, sha256: c7a7c53801686ca16e4b12df873c52753cd58f3683b155424dc99b9e13e48f5f, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/src-pyproject.toml.txt, sha256: bd637e87f27fa2a3b89ace2e34dd7b2fdad9562e8ba3b716ca1a95932666677a, retrieved_at: 2026-10-16T08:20:11Z, method: curl }
  - { file: references/evidence/self-improvement/rrsi/web-search-rrsi.txt, sha256: 154ebe7943154c8dc8a0a8177b3325660edde0dc71433871d9f2fb42cccf4172, retrieved_at: 2026-10-16T08:20:45Z, method: web-search }
  - { file: references/evidence/self-improvement/rrsi/fetch-log.txt, sha256: 4dee7fe230eb6da387c51a182d9411f65a70a37cfa6e3f74a0ee24dee357a55f, retrieved_at: 2026-10-16T08:20:45Z, method: command }
---

# What it is

RRSI is a Python search loop released by Google Research under Apache 2.0 that evolves the harness of an LLM agent (its prompts, control flow, tools, memory and context management) against a benchmark, while a regularizer limits overfitting. The repo README says: `Apache 2.0; see [LICENSE](LICENSE).`[^license] The paper's abstract describes the harness as: "An LLM agent's capability is largely magnified by its harness, namely the prompts, control flow, tooling, memory, and context management surrounding the frozen backbone model."[^arxiv]

Facts from the repo API, observed 2026-10-16 (evidence: [api-repo.json](/references/evidence/self-improvement/rrsi/api-repo.json)):

- Repo `google-research/rrsi`, public, not a fork or archive, language Python, default branch `main`.
- 1523 stars, 146 forks, 13 open issues, `pushed_at` 2026-09-23T22:16:25Z.
- No GitHub release exists: `/releases/latest` returned 404 (evidence: [api-releases-latest.json](/references/evidence/self-improvement/rrsi/api-releases-latest.json)). Use the git commit, not a tag.
- Core dependency is `anthropic[vertex]>=0.40`. Agentic benchmark runners add `litellm`, `fastmcp`, `mcp` and `pymupdf`; the coding instance uses `harbor` and Docker (evidence: [src-pyproject.toml.txt](/references/evidence/self-improvement/rrsi/src-pyproject.toml.txt), [raw-main-README.md.txt](/references/evidence/self-improvement/rrsi/raw-main-README.md.txt)).

Paper: arXiv 2609.24972, "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses", submitted 21 Sep 2026, "last revised 4 Oct 2026 (this version, v3)"[^arxiv]. Authors are from Google Cloud AI Research, UNC-Chapel Hill, Stanford and WashU per the project page[^project].

## Results as published

The README table reports, for Claude Opus 4.8 as frozen policy, H_0 vs RRSI on eight benchmarks. The coding evolve split goes from 74.2 to 80.2 (+6.0), and the OOD deltas are +1.8, +4.7, +3.5, +3.7 and +4.3 (evidence: [raw-main-README.md.txt](/references/evidence/self-improvement/rrsi/raw-main-README.md.txt)[^readme]).

The headline numbers differ between sources:

> "Across eight benchmarks spanning coding, agentic workspace and engineering design tasks, RRSI gains up to 6.0 points on the split it evolves against and up to 4.3 points on the five out-of-distribution benchmarks, while producing a harness that runs on 30% fewer policy tokens than the unregularized evolution."
> Evidence: [arxiv-abs-2609.24972.html](/references/evidence/self-improvement/rrsi/arxiv-abs-2609.24972.html) (v3 abstract)

> "...it gains up to 14.1 points on the evolving split and improves all six held-out splits, by up to 4.7 points out of distribution..."
> Evidence: [arxiv-html-text.txt](/references/evidence/self-improvement/rrsi/arxiv-html-text.txt) (v1, superseded)

> "+4.0 pts average gain on the three benchmarks the harness evolves against"
> Evidence: [project-page-text.txt](/references/evidence/self-improvement/rrsi/project-page-text.txt)[^project]

The token saving is also stated two ways: "30% fewer policy tokens" in the abstract, and "−36% tokens" on the project page. The v1 paper gives a comparison point: "AHE is the extreme case, at 3.82 million tokens per trial, 58% more than ours, for 4.4 points less out of distribution." (evidence: [arxiv-html-text.txt](/references/evidence/self-improvement/rrsi/arxiv-html-text.txt)).

## How the loop works (code)

Method table in the README maps paper to code (evidence: [raw-main-README.md.txt](/references/evidence/self-improvement/rrsi/raw-main-README.md.txt)[^readme]). The key pieces, read from source:

1. **Propose.** A Claude coding agent edits the harness in place in a git worktree, tagging each edit with a component and a hypothesis. The paper's budget schedule caps edits per candidate. From `schedule.py`: "Early rounds may bundle several coordinated edits in one candidate; late rounds become sparse and attributable." (evidence: [src-rrsi-schedule.py.txt](/references/evidence/self-improvement/rrsi/src-rrsi-schedule.py.txt)[^schedule])
2. **Screen.** The critic reads the diff before any evaluation. From `critic.py`: "1. Deterministic pre-checks: a generic denylist (credentials, infra names) plus the domain's own patterns (grader paths, task ids, judge references)." and "2. LLM review (Claude Opus 4.8) of intent and content, not style." (evidence: [src-rrsi-critic.py.txt](/references/evidence/self-improvement/rrsi/src-rrsi-critic.py.txt)[^critic])
3. **Evaluate.** Full evolve-set runs of each surviving candidate.
4. **Select.** A candidate is admissible only if it clears a noise-adjusted floor (S' >= S* - delta), passes a cost rule, and passes domain guards. The winner is the argmax of admissible scores, or the incumbent stays. Noise band delta is fixed per instance: the README lists "0.017 / 0.004 / 0.020" (evidence: [raw-main-README.md.txt](/references/evidence/self-improvement/rrsi/raw-main-README.md.txt)). The cost rule, from the `selection.py` docstring: "c = [Delta C <= beta0 + beta1 Delta S] if Delta S > delta", and otherwise "[w_s Delta S - w_c Delta C + w_n nu(l') > 0]" (evidence: [src-rrsi-selection.py.txt](/references/evidence/self-improvement/rrsi/src-rrsi-selection.py.txt)[^selection]).
5. **Ledger and prune.** Every edit is a history record (component, hypothesis, measured delta). Components whose recent measured gain is <= 0 go into a prune set. Stalled runs are steered to untried components (evidence: [src-rrsi-history.py.txt](/references/evidence/self-improvement/rrsi/src-rrsi-history.py.txt)).

## Does it need training or GPUs?

No training. The model is frozen throughout. The search only rewrites text and code around it. The README says the proposer, analyst, critic and frozen policy are Claude Opus 4.8 on Vertex AI, and any LiteLLM model string works[^readme]. The evaluation is many full benchmark trials per candidate, so it is expensive in model calls. The sources read here give no dollar cost. Token counts per trial are the only cost measure published. No GPU or training code appeared in the files read. Docker is needed for the coding instance.

# Fit for a falkordblite agent memory

What transfers, in increasing order of effort:

- **Noise-aware acceptance.** Do not accept a memory-retrieval change unless its gain clears the noise band of the evaluation. This is the cheapest and most defensible idea in RRSI.
- **Cost-aware acceptance.** Require retrieval latency or token cost growth to be paid for by measured gain.
- **Edit ledger in the graph.** Store each tuning trial as a FalkorDB node (component, value, score, delta, verdict). This makes the self-improvement auditable and gives the graph real work to do, which the hackathon rule asks for ("The graph has to do real work"[^rules]).
- **Held-out split.** Keep a set of memory queries that the tuner never sees, to catch overfitting to one project's sessions. RRSI's main result is that evolved harnesses overfit without this.

What does not transfer as-is: the harness-rewriting loop. It needs a benchmark with a verifier, a frozen policy LLM for every trial, and Docker benchmark runners. None of these exist in Neo-Cortex yet. A rewrite of prompts and tools per candidate would burn the hackathon budget before the core pipeline works.

Minimal version on falkordblite, with no model training:

1. **Labeled set.** About 30-40 queries from real agent sessions, each with the expected node or fact ids. Split into an evolve set and a held-out set.
2. **Retrieval weight tuner.** Search the RRF channel weights (graph, vector, BM25, temporal) and the temporal half-life on the evolve set. Accept a candidate only if its gain exceeds a noise band estimated by bootstrap over queries, and its latency stays within a budget. Write each trial to the graph as a `:TuneRun` node. Report the held-out score for the winner.
3. **Optional, if time remains.** Procedure memory: record a successful session's steps as a `:Procedure` node and boost it when a similar task comes up. Track 02 names "Episodic, semantic, and procedural memory" as a key focus[^judging].

Consolidation by LLM reflection (an agent proposing merges and supersessions of graph facts, with a critic and an undo path) is the closest match to "self-critique loops that rewrite the graph". It is also the riskiest part: it can corrupt memory, and it needs provenance and reversible soft-supersede edges. It is out of scope for this hackathon.

# Recommendation

**Adapt, do not adopt.** Take the acceptance rule (noise band, cost rule, held-out split) and the graph-stored ledger. Do not port the harness-rewriting loop.

Hackathon fit: track 02, "Agent Memory and Coordination", says it will judge "the best agents that remember across sessions and share what they know"[^judging]. A self-tuning retrieval layer whose trials live in FalkorDB supports a memory story. It does not by itself show the graph doing much work, and judges look for "whether the graph is doing work the agent could not do without it"[^judging]. So the tuner is a supporting feature, not the centerpiece. RRSI has no published results on memory QA, so none of its numbers transfer to this use.

Effort, given about 58 hours until submissions close (2026-10-18 18:29 UTC):

- Labeled set (30-40 queries) and bootstrap noise band: about 2 hours.
- Weight tuner with cost check and held-out report: about 3 hours.
- `:TuneRun` ledger writes and a read-back query for the demo: about 1.5 hours.
- Test for the acceptance rule: about 0.5 hours.
- Total: about 7 hours. Schedule it after the core retrieval and MCP server work, and cut it first if the core is late.
- Not recommended: LLM reflection and consolidation (about 10 or more hours plus risk), and porting the RRSI loop (more than 20 hours, no benchmark).

# Open questions

- The headline gains differ between sources: 6.0 and 4.3 (v3 abstract), 14.1 and 4.7 (v1 HTML), and 4.0 and 3.4 (project page average). The v3 abstract's "up to 4.3" OOD conflicts with the README table, where the OOD maximum is +4.7 (JobBench). Not resolved; quote the README table for numbers.
- Token saving: "30% fewer" (abstract) vs "−36%" (project page). Not resolved.
- Dollar cost and wall-clock per run are not published in any source read here. Required before estimating a budget for the Neo-Cortex tuner.
- The v3 paper HTML was not fetched; only the v3 abstract and the v1 HTML were. Result tables in v3 may differ from the README.
- Whether "Claude Opus 4.8" is available to this project's Vertex or API account is not checked.
- The repo's code was read, not run. Tests (`pytest tests`) were not executed.
- Whether a hackathon judge would treat a self-tuning memory as qualifying for track 02 is not stated in the rules[^judging].

[^license]: rrsi LICENSE (Apache 2.0)
[^arxiv]: RRSI arXiv 2609.24972 (abstract page)
[^project]: RRSI project page
[^readme]: rrsi README (main branch)
[^schedule]: rrsi/schedule.py
[^critic]: rrsi/critic.py
[^selection]: rrsi/selection.py
[^judging]: Graph Hacks judging and prizes (bundle)
[^rules]: Graph Hacks rules (bundle)
