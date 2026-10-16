# Public data: FalkorDB

Fetched 2026-10-16 09:27 UTC by `scripts/fetch_public.py` via `gh api` (REST).

Public data from public GitHub repos (FalkorDB org). No private repos, no credentials.

- Repos: FalkorDB/FalkorDB, FalkorDB/falkordb-py, FalkorDB/GraphRAG-SDK
- Docs: FalkorDB/docs (cap 60 files; prefers cypher/, algorithms/, indexing, getting-started/)
- Tickets: last 80 issues and 40 PRs per repo, first 30 comments each; PRs list first 30 changed files
- People: top 15 contributors per repo in `falkordb/people.jsonl`

## Counts

| kind | repo | files |
|---|---|---|
| doc | FalkorDB/FalkorDB | 1 |
| doc | FalkorDB/docs | 60 |
| ticket | FalkorDB/FalkorDB | 120 |
| ticket | FalkorDB/GraphRAG-SDK | 120 |
| ticket | FalkorDB/falkordb-py | 104 |
| people | all | 40 rows |

Failures: 0

## Re-run

    python3 scripts/fetch_public.py

Needs `gh` logged in. Takes several minutes (about 0.2 s sleep per call). Overwrites `falkordb/`.
