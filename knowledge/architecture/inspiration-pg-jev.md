---
type: Research Finding
title: pg-jev (realZachi) and Jev-judged rows
description: What pg-jev is (a PostgreSQL extension that judges table rows with TypeSafe's Jev), how its batching, cache and typed probability functions work, and whether a scoped version fits falkordblite and the Neo-Cortex hackathon build.
resource: https://github.com/realZachi/pg-jev
tags: [inspiration, self-improvement, jev, typesafe, falkordblite, graphrag, calibrated-probabilities, caching, draft]
status: draft
generated: { by: claude-haiku-5-5/self-improvement-agent, at: 2026-10-16T08:22:00Z }
stale_after: 2026-10-18T18:29:00Z
sources:
  - id: pgjev-repo-api
    resource: https://api.github.com/repos/realZachi/pg-jev
    title: 'GitHub API, realZachi/pg-jev repository metadata'
    last_modified: 2026-10-06T13:55:50Z
  - id: pgjev-readme
    resource: https://github.com/realZachi/pg-jev
    title: 'realZachi/pg-jev README (master)'
    last_modified: 2026-10-06T13:55:50Z
  - id: pgjev-changelog
    resource: https://github.com/realZachi/pg-jev/blob/master/CHANGELOG.md
    title: 'realZachi/pg-jev CHANGELOG.md'
  - id: pgjev-license
    resource: https://github.com/realZachi/pg-jev/blob/master/LICENSE
    title: 'realZachi/pg-jev LICENSE'
  - id: pgjev-sql
    resource: https://github.com/realZachi/pg-jev/blob/master/sql/jev--0.2.1.sql
    title: 'realZachi/pg-jev sql/jev--0.2.1.sql (extension source)'
  - id: pgjev-how-it-works
    resource: https://github.com/realZachi/pg-jev/blob/master/.agents/skills/pgjev/references/how-it-works.md
    title: 'realZachi/pg-jev how-it-works.md (agent skill reference)'
  - id: stuntd-readme
    resource: https://github.com/bladedevoff/stuntd
    title: 'bladedevoff/stuntd README (local Jev-compatible proxy)'
  - id: stuntd-api
    resource: https://api.github.com/repos/bladedevoff/stuntd
    title: 'GitHub API, bladedevoff/stuntd repository metadata'
    last_modified: 2026-10-11T08:33:38Z
  - id: hackathon-rules
    resource: https://www.wemakedevs.org/hackathons/falkordb/rules
    title: 'Graph Hacks rules page (WeMakeDevs), via hackathon/judging-and-prizes.md'
  - id: jev-check
    resource: /models/jev-typesafe-claim-check.md
    title: 'Jev (TypeSafe AI) claim check (internal)'
  - id: gliner25-note
    resource: /models/gliner2-5-base.md
    title: 'GLiNER2.5 Base note (internal)'
  - id: project-plan
    resource: /architecture/project-plan.md
    title: 'Neo-Cortex stack decisions and risks (internal)'
  - id: judging-note
    resource: /hackathon/judging-and-prizes.md
    title: 'Graph Hacks judging and prizes (internal)'
  - id: cypher-note
    resource: /falkordb/cypher-support.md
    title: 'FalkorDB Cypher support (internal)'
evidence:
  - { file: references/evidence/self-improvement/pg-jev/gh_commits.json, sha256: ae1c1988a3a90eb7779a996337ce5c60510fa70ef715f0ebe2e1f81b00439227, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_contents_root.json, sha256: ce526197f10acd708fa7b83db27f26be91314c7baed65a4ec6ecd9a056d49de1, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_languages.json, sha256: 16dac921ebc1a681116b6830c8838bb0890ac07bbd294d11fddcd0781a96c681, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_license.json, sha256: 89773f3a2a8071a941df0081d06e24a6326bdd24faec7ddc874a74409cb70ad3, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_releases_latest.json, sha256: b83ce06316d88085129b54f25b9d5db7276bc72c2eabb14dfa9d0c8b2421580b, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_repo.json, sha256: cd19a58704057e860e64d5e4e8e12e44007ee470a5ef153c1024fe83b1d094d9, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_stuntd_repo.json, sha256: 4da647b1f4e32b0e5c8df3e2688317ee8897aa7f37572dcbc44338527a6931a0, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_tags.json, sha256: e3e5ea4f1cf92ca17318106a2aabff65a9b1b0bf15ff081c83e1c0852b8486b6, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_tree_docs.json, sha256: 7da8cf97febbe328e031a4892820fa8ccd59a99d8a21289a97fc37027b678118, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_tree_.github.json, sha256: af87ec5bf1b232a02ddaf610c7492e3e772e4a3514a0fc1bb11b922995d1d025, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_tree_master_recursive.json, sha256: e592d5e5087d2cd0951a0212c42c7a4c3fef11bbc3d89b36d50314a3a3e343b6, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_tree_sql.json, sha256: 119063d82916fb33982ac4ed7926a0936f04ad6d61db3a6b690652479d409383, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/gh_tree_test.json, sha256: 8d25a163e9fdd86f3f8ab56b38bc7eb29c3b88a8664e5fe9c33e4fbb3f4c10a0, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/raw_AGENTS.md.txt, sha256: 487ec32c86cb3486eb5cb26cdec1f1fbd89b43bd3350b21d9c95862e5c903005, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/raw_CHANGELOG.md.txt, sha256: c34f3bbac1ecba1e1fb263a7ee02e4ac0a6115586828b4233a1f30b742ad96ee, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/raw_CONTRIBUTING.md.txt, sha256: 2fc954863363b47b8ed2ec6d778b0df7815e123d7654d958d56483c5eaf9ca86, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/raw_Dockerfile, sha256: dfec0b5aa3c4ddc3f8a3d9f6ec233576de7be525488560bbc9385004d7acfe05, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/raw_LICENSE.txt, sha256: cde1e15caffcf2859f51bf56566b1f26c58d4151334ceb7d6247ebc70c7b1414, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/raw_Makefile, sha256: e592b8562610fbad81c7aa555a02805b609b1b08e09080af890d72193f6fc1fb, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/raw_META.json, sha256: 5e8357ec4df23520c1fdf668686eda4bdd10170a5a69109a7b9222f521d2e5c6, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/readme_README.txt, sha256: e98b6dfe50b695b02ddf4331171e2563a58271d4e383bf39f1365e0fb8c2318d, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/repo_files/agents_skills_pgjev_references_functions.md.txt, sha256: 5c93caad36a8862a93ff68e07058cdff9ab5740b3886e9362c1814d7d68c7494, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/repo_files/agents_skills_pgjev_references_how-it-works.md.txt, sha256: 4be2c5ab1008a6303b824d8430d279c1dd7ee50fe578e2f2504212e2a480b10c, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/repo_files/agents_skills_pgjev_references_settings.md.txt, sha256: d92cf2e568f06c01b13d58b187a2d41d7240c2c77b23489c3e20f4af69cc107d, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/repo_files/docs_PUBLISHING.md.txt, sha256: 12a46673e406b264e8dc66e2fb98ff2d08d80730f54681ee6386d29daaed9d8a, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/repo_files/github_workflows_ci.yml.txt, sha256: 76a4e8a9a3e5524d8a4ac4a5deac80a36c7fe91c75b2a1705a4fc5419e336f8c, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/repo_files/jev.control.txt, sha256: d849003c28fca73946b6cdef5e922739f34a3f784d9f4ad392c4360c49c28245, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/repo_files/sql_jev--0.2.1.sql.txt, sha256: f82cd059a9588fcc5a7f3c9f22eb0f0d449498c74d0742728aa1e349ce709948, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/repo_files/test_mock_api.py.txt, sha256: 32004b83e6f44b336aba3f09efeb803162d4fa114c3876c7dd89d001ed77fe22, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
  - { file: references/evidence/self-improvement/pg-jev/stuntd_README.txt, sha256: d9a91c829f52618315161f1b8289aeabeda43431789e41eb5086494680a9f293, retrieved_at: 2026-10-16T08:19:50Z, method: curl }
---

# What it is

pg-jev is a PostgreSQL extension, installed as `jev`, that filters, ranks and classifies table rows from a plain-language condition. Each row is judged by TypeSafe's Jev. The repo describes itself as:

> Ask your Postgres tables questions in plain language. A PostgreSQL extension powered by TypeSafe's Jev.

Evidence: `gh_repo.json` [^pgjev-repo-api]

The README adds that the model is "a System One model that returns calibrated probabilities instead of generated text. No index, no embeddings, no vector column." [^pgjev-readme] Evidence: `readme_README.txt`.

Repository facts, as observed 2026-10-16 (GitHub API, raw JSON lines):

```
"created_at": "2026-09-17T20:04:00Z",
"pushed_at": "2026-10-06T13:55:50Z",
"stargazers_count": 1179,
"forks_count": 95,
"open_issues_count": 3,
"default_branch": "master",
```

Evidence: `gh_repo.json` [^pgjev-repo-api]

- Latest release in the changelog: "## [0.2.1] - 2026-10-03". Evidence: `raw_CHANGELOG.md.txt` [^pgjev-changelog]. Earlier entries are 0.2.0 and 0.1.0 (2026-09-17). The tags list has one entry, `"name": "v0.2.1"`. Evidence: `gh_tags.json`.
- Licence: the LICENSE file is the PostgreSQL License, starting with "PostgreSQL License". Evidence: `raw_LICENSE.txt` [^pgjev-license]. The GitHub API licence field reads `"spdx_id": "NOASSERTION"` (GitHub's detector did not classify the file). Evidence: `gh_repo.json`.
- Languages (GitHub, bytes): `"Shell": 9902`, `"Python": 3411`, Makefile and Dockerfile also present. Evidence: `gh_languages.json`.
- Maturity: about one month old, one listed owner, 0.x versioning, a CI workflow (`github_workflows_ci.yml.txt`) and a regression suite (`test/`, `test_mock_api.py.txt`). The suite uses a mock API, so it never calls the live model.

# How it works

Three layers.

1. **SQL surface.** Functions such as `jev(row, condition)`, `jev_prob`, `jev_choice`, `jev_score`, `jev_eval`, `jev_stats`. The README says "`jev()` is an ordinary boolean function, so it composes with everything else in SQL". Evidence: `readme_README.txt` [^pgjev-readme]. The functions are declared in `sql_jev--0.2.1.sql.txt` [^pgjev-sql].
2. **PL/Python core.** `_jev_eval` is `LANGUAGE plpython3u`. It serialises the row, reads ahead the table in physical order, batches rows, and sends HTTPS requests from the database server.
3. **Remote model.** One POST per batch. The request body is built as follows (verbatim from the SQL):

```
return json.dumps({"model": cfg["model"], "state": state,
                   "questions": {("r%d" % i): build_question(i) for i in range(len(rows))}}).encode()
```

Evidence: `sql_jev--0.2.1.sql.txt` [^pgjev-sql]

Batching is the central design choice. The README says:

> Rows are packed `jev.batch_size` (20) per request into one shared *state*

> Jev evaluates all questions over one state in parallel, which amortises the ~270-token request overhead

Evidence: `readme_README.txt` [^pgjev-readme]

The author also reports that position-indexed answers degrade with batch size:

> Jev has to find `rows[i]` by position in the array, and that gets unreliable in long arrays.

> batches of 1–20 rows were 100 % correct, batches of 40 were 92–98 % and batches of 80 were 77–94 %

Evidence: `readme_README.txt` [^pgjev-readme]. These are the author's own tests against ground truth from structured columns (400 rows each). They were not independently reproduced.

Caching and cost:

> Answers are cached per row content and question for the backend session

Evidence: `readme_README.txt` [^pgjev-readme]. Threshold changes and sorting by probability re-use the cache.

> Measured on a 2,000-row table from Europe (~190 ms to the API): first run ≈ 3.5 s in 100 requests, ≈ 296k input tokens, ≈ $0.012

Evidence: `readme_README.txt` [^pgjev-readme]. This is the author's measurement at TypeSafe list price. It was not re-run here.

Full scan and privacy limits:

> This is a full scan by design: every row the executor asks about goes to the API.

> Row contents are sent to a third-party API. Do not use it on data you may not share.

Evidence: `readme_README.txt` [^pgjev-readme]

Local endpoint option. The README says `jev.api_url` "can point at any server that speaks the same `POST /v1/systemone` contract, so rows never leave". Evidence: `readme_README.txt` [^pgjev-readme]. The changelog adds: "Local Jev-compatible servers work without an API key." Evidence: `raw_CHANGELOG.md.txt` [^pgjev-changelog]. The named local server is stuntd, which the README describes as a proxy that "records the typed decisions your app already makes and learns to answer them itself". Evidence: `stuntd_README.txt` [^stuntd-readme]. Its README also says "TypeSafe's Jev is an early-access API at the time of writing, and there are no published weights." Evidence: `stuntd_README.txt` [^stuntd-readme]. stuntd is Apache-2.0, 70 stars, created 2026-09-23, pushed 2026-10-11, and distils heads on a frozen Laya encoder. Evidence: `gh_stuntd_repo.json` [^stuntd-api].

Requirements: "Requirements: PostgreSQL 14–17 with `plpython3u`", a superuser, and a TypeSafe API key, unless the endpoint is local. Evidence: `readme_README.txt` [^pgjev-readme]

> `plpython3u` is an untrusted language: only superusers can create the extension, and functions run with the server's OS privileges.

Evidence: `readme_README.txt` [^pgjev-readme]

# Fit assessment

What transfers to falkordblite and what does not:

| Idea from pg-jev | Fit for Neo-Cortex | Why |
|---|---|---|
| Typed judgments (yes/no, choice, ordinal) stored as probabilities | Good | Matches the two System 1 decisions already planned in [project-plan](/architecture/project-plan.md) (assertion gating, entity resolution). |
| Judgments cached by row content and question | Good | Cheap to build; re-thresholding and re-ranking then cost nothing. |
| Batching many rows per request | Only for an LLM-style API | pg-jev's win is amortising per-request token overhead. A local encoder such as GLiNER2.5 has no such overhead. Not tested. |
| Calling the judge from inside a Cypher query | Unknown, probably no | The [cypher note](/falkordb/cypher-support.md) records the FalkorDB docs as contradictory on user-defined functions. Untested here. |
| Hosted Jev as the judge | No | Early access, paid, rows leave the machine, no weights. See [jev-check](/models/jev-typesafe-claim-check.md). |
| pg-jev as code | No | It is a Postgres extension. Neo-Cortex runs on falkordblite. |
| stuntd as local Jev | No, for now | Adds a second model family (Laya) whose licence and size were not checked. |

Local option with GLiNER2.5. The [GLiNER2.5 note](/models/gliner2-5-base.md) lists "Classification: `model.classify_text(text, {"sentiment": [...]})`". That covers a labelled-choice question. It is not a Jev-compatible Noul, Choice or Score API. Its scores are not shown to be calibrated for our tasks. The local route therefore needs a gold-set check before the numbers are presented as probabilities.

Hackathon value. The judging note quotes the track criteria, for example "For the best agent that uses a graph to make decisions and take action." [^judging-note] and "For the best agents that remember across sessions and share what they know." [^judging-note]. A Postgres extension has no graph content, so pg-jev itself earns no credit. The transferable point (judgments as typed, calibrated, cached graph data with provenance) can support a Track 01 or 02 story. It is not a feature that wins the track on its own.

Timing. The hackathon closes 2026-10-18 18:29 UTC, about two days after this note was written.

# Recommendation

**Adapt the idea, narrowly. Do not adopt the code or the hosted API. Skip the rest.**

- Build one Python helper over falkordblite. It takes a question and a batch of nodes or edges, returns per-label probabilities, caches by content hash, and writes results as properties. Cypher then filters on thresholds. Estimate: 4 to 6 hours including one test.
- Use it for the assertion-gating and entity-resolution decisions already in [project-plan](/architecture/project-plan.md). Estimate: 2 to 3 hours for a gold-set check with GLiNER2.5. If calibration is poor, present the output as a ranking score, not a probability.
- Do not port pg-jev, host Jev, run stuntd, or build a Cypher UDF. A UDF spike is a 1 to 2 hour option only if the helper is finished early.
- Total on top of the existing plan: about 6 to 9 hours. If the plan's day-2 System 1 work does not start, skip the helper and cite pg-jev as inspiration in the write-up only.

# Open questions

- Does FalkorDB support user-defined functions callable inside Cypher? The docs are contradictory, and this was not tested.
- Do GLiNER2.5 `classify_text` scores track correctness on our gold set for yes/no and choice decisions? Not tested.
- Are the author's accuracy-by-batch-size figures reproducible on other data or models? Not checked.
- Price: the $0.012 figure is the author's measurement at list price. TypeSafe's pricing page was not checked.
- The pgjev.com documentation was not fetched. Only the README, changelog, SQL and skill reference in the repo were read.
- The Laya encoder used by stuntd: licence, size and quality were not checked.
- The GitHub API reports the licence as NOASSERTION, but the LICENSE file is the PostgreSQL License. This note relies on the file text.
- Maturity risk: one month old, one listed owner, version 0.2.1. Not assessed beyond the repo metadata.
- Nothing was installed or run. The extension was read, not executed, and no API key was used.

# Related

- [Jev (TypeSafe AI) claim check](/models/jev-typesafe-claim-check.md)
- [GLiNER2.5 Base](/models/gliner2-5-base.md)
- [Neo-Cortex stack decisions and risks](/architecture/project-plan.md)
- [Fast-classifier use cases](/architecture/classification-usecases.md)
- [Graph Hacks judging and prizes](/hackathon/judging-and-prizes.md)
- [FalkorDB Cypher support](/falkordb/cypher-support.md)
- [Architecture index](/architecture/index.md)

[^pgjev-repo-api]: GitHub API, https://api.github.com/repos/realZachi/pg-jev. Evidence `gh_repo.json`, `gh_languages.json`, `gh_tags.json`.
[^pgjev-readme]: https://github.com/realZachi/pg-jev (README on master). Evidence `readme_README.txt`.
[^pgjev-changelog]: https://github.com/realZachi/pg-jev/blob/master/CHANGELOG.md. Evidence `raw_CHANGELOG.md.txt`.
[^pgjev-license]: https://github.com/realZachi/pg-jev/blob/master/LICENSE. Evidence `raw_LICENSE.txt`.
[^pgjev-sql]: https://github.com/realZachi/pg-jev/blob/master/sql/jev--0.2.1.sql. Evidence `repo_files/sql_jev--0.2.1.sql.txt`.
[^stuntd-readme]: https://github.com/bladedevoff/stuntd. Evidence `stuntd_README.txt`.
[^stuntd-api]: https://api.github.com/repos/bladedevoff/stuntd. Evidence `gh_stuntd_repo.json`.
[^judging-note]: [Graph Hacks judging and prizes](/hackathon/judging-and-prizes.md), which cites the WeMakeDevs rules page.
