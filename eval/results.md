# Retrieval evaluation

Synthetic Pellucid Pay corpus, setting clean (102 docs in the graph, AI-generated, fictional), 80 gold questions, k=20 chunks collapsed to unique documents, fixed now = 2026-10-16T00:00Z. Hit/Recall/FullCover/MRR are against `gold_docs`; AnswerIn = normalised gold answer found in the retrieved chunk text (full chunk text of the first k unique documents, so it only checks that the answer string was retrieved, not that it is easy to extract).

Ingest: {'skipped': True, 'documents_in_graph': 102, 'first_ingest': {'documents': 102, 'skipped': 0, 'chunks': 136, 'mentions': 765, 'rels': 40, 'errors': 0, 'unsupported': 0, 'new_entities': 131, 'seconds': 86.2}}

## recall@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.73 | 1.00 | 0.61 | 0.62 | 0.71 | 0.93 |
| bm25 | 0.71 | 0.92 | 0.65 | 0.53 | 0.79 | 0.81 |
| vector+bm25 | 0.75 | 1.00 | 0.65 | 0.66 | 0.76 | 0.85 |
| vector+bm25+graph | 0.75 | 0.92 | 0.69 | 0.66 | 0.74 | 0.89 |
| vector+bm25+temporal | 0.75 | 1.00 | 0.67 | 0.59 | 0.79 | 0.89 |
| full | 0.74 | 1.00 | 0.67 | 0.62 | 0.71 | 0.89 |
| full-graph | 0.75 | 1.00 | 0.67 | 0.59 | 0.79 | 0.89 |
| auto | 0.74 | 0.92 | 0.69 | 0.62 | 0.74 | 0.89 |

## fullcover@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.53 | 1.00 | 0.23 | 0.50 | 0.47 | 0.89 |
| bm25 | 0.55 | 0.92 | 0.38 | 0.38 | 0.65 | 0.67 |
| vector+bm25 | 0.59 | 1.00 | 0.38 | 0.56 | 0.59 | 0.67 |
| vector+bm25+graph | 0.61 | 0.92 | 0.46 | 0.56 | 0.59 | 0.78 |
| vector+bm25+temporal | 0.60 | 1.00 | 0.42 | 0.44 | 0.65 | 0.78 |
| full | 0.59 | 1.00 | 0.42 | 0.50 | 0.53 | 0.78 |
| full-graph | 0.60 | 1.00 | 0.42 | 0.44 | 0.65 | 0.78 |
| auto | 0.60 | 0.92 | 0.46 | 0.50 | 0.59 | 0.78 |

## answerin@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.41 | 0.92 | 0.35 | 0.00 | 0.71 | 0.11 |
| bm25 | 0.40 | 0.92 | 0.35 | 0.00 | 0.65 | 0.11 |
| vector+bm25 | 0.42 | 0.92 | 0.35 | 0.00 | 0.76 | 0.11 |
| vector+bm25+graph | 0.42 | 0.92 | 0.35 | 0.00 | 0.76 | 0.11 |
| vector+bm25+temporal | 0.42 | 0.92 | 0.35 | 0.00 | 0.76 | 0.11 |
| full | 0.42 | 0.92 | 0.35 | 0.00 | 0.76 | 0.11 |
| full-graph | 0.42 | 0.92 | 0.35 | 0.00 | 0.76 | 0.11 |
| auto | 0.42 | 0.92 | 0.35 | 0.00 | 0.76 | 0.11 |

## mrr@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.63 | 0.67 | 0.58 | 0.52 | 0.68 | 0.87 |
| bm25 | 0.60 | 0.62 | 0.59 | 0.36 | 0.75 | 0.76 |
| vector+bm25 | 0.63 | 0.59 | 0.64 | 0.43 | 0.72 | 0.78 |
| vector+bm25+graph | 0.60 | 0.55 | 0.63 | 0.48 | 0.67 | 0.69 |
| vector+bm25+temporal | 0.58 | 0.52 | 0.55 | 0.47 | 0.68 | 0.81 |
| full | 0.63 | 0.51 | 0.67 | 0.50 | 0.68 | 0.75 |
| full-graph | 0.58 | 0.52 | 0.55 | 0.47 | 0.68 | 0.81 |
| auto | 0.63 | 0.55 | 0.68 | 0.50 | 0.67 | 0.69 |

## hit@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.93 | 1.00 | 0.96 | 0.75 | 0.94 | 1.00 |
| bm25 | 0.89 | 0.92 | 0.92 | 0.69 | 0.94 | 1.00 |
| vector+bm25 | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |
| vector+bm25+graph | 0.89 | 0.92 | 0.92 | 0.75 | 0.88 | 1.00 |
| vector+bm25+temporal | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |
| full | 0.90 | 1.00 | 0.92 | 0.75 | 0.88 | 1.00 |
| full-graph | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |
| auto | 0.89 | 0.92 | 0.92 | 0.75 | 0.88 | 1.00 |

## recall@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.60 | 0.83 | 0.43 | 0.53 | 0.62 | 0.87 |
| bm25 | 0.59 | 0.92 | 0.50 | 0.39 | 0.65 | 0.70 |
| vector+bm25 | 0.65 | 1.00 | 0.50 | 0.51 | 0.71 | 0.78 |
| vector+bm25+graph | 0.62 | 0.92 | 0.52 | 0.51 | 0.62 | 0.69 |
| vector+bm25+temporal | 0.63 | 1.00 | 0.52 | 0.41 | 0.65 | 0.81 |
| full | 0.61 | 0.92 | 0.52 | 0.46 | 0.62 | 0.69 |
| full-graph | 0.63 | 1.00 | 0.52 | 0.41 | 0.65 | 0.81 |
| auto | 0.61 | 0.92 | 0.54 | 0.46 | 0.62 | 0.69 |

## fullcover@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.38 | 0.83 | 0.04 | 0.38 | 0.35 | 0.78 |
| bm25 | 0.40 | 0.92 | 0.27 | 0.19 | 0.35 | 0.56 |
| vector+bm25 | 0.45 | 1.00 | 0.15 | 0.31 | 0.53 | 0.67 |
| vector+bm25+graph | 0.39 | 0.92 | 0.15 | 0.31 | 0.41 | 0.44 |
| vector+bm25+temporal | 0.41 | 1.00 | 0.15 | 0.25 | 0.41 | 0.67 |
| full | 0.39 | 0.92 | 0.15 | 0.31 | 0.41 | 0.44 |
| full-graph | 0.41 | 1.00 | 0.15 | 0.25 | 0.41 | 0.67 |
| auto | 0.40 | 0.92 | 0.19 | 0.31 | 0.41 | 0.44 |

## answerin@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.36 | 0.92 | 0.23 | 0.00 | 0.65 | 0.11 |
| bm25 | 0.39 | 0.92 | 0.31 | 0.00 | 0.65 | 0.11 |
| vector+bm25 | 0.40 | 0.92 | 0.35 | 0.00 | 0.65 | 0.11 |
| vector+bm25+graph | 0.40 | 0.83 | 0.35 | 0.00 | 0.71 | 0.11 |
| vector+bm25+temporal | 0.39 | 0.92 | 0.35 | 0.00 | 0.59 | 0.11 |
| full | 0.39 | 0.83 | 0.35 | 0.00 | 0.65 | 0.11 |
| full-graph | 0.39 | 0.92 | 0.35 | 0.00 | 0.59 | 0.11 |
| auto | 0.40 | 0.83 | 0.35 | 0.00 | 0.71 | 0.11 |

## mrr@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.62 | 0.64 | 0.56 | 0.51 | 0.67 | 0.87 |
| bm25 | 0.59 | 0.62 | 0.56 | 0.35 | 0.75 | 0.74 |
| vector+bm25 | 0.62 | 0.59 | 0.64 | 0.42 | 0.72 | 0.76 |
| vector+bm25+graph | 0.60 | 0.55 | 0.63 | 0.47 | 0.67 | 0.68 |
| vector+bm25+temporal | 0.58 | 0.52 | 0.55 | 0.44 | 0.67 | 0.81 |
| full | 0.62 | 0.50 | 0.67 | 0.48 | 0.68 | 0.73 |
| full-graph | 0.58 | 0.52 | 0.55 | 0.44 | 0.67 | 0.81 |
| auto | 0.62 | 0.55 | 0.68 | 0.48 | 0.67 | 0.68 |

## hit@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.84 | 0.83 | 0.85 | 0.69 | 0.88 | 1.00 |
| bm25 | 0.80 | 0.92 | 0.77 | 0.56 | 0.94 | 0.89 |
| vector+bm25 | 0.86 | 1.00 | 0.88 | 0.69 | 0.88 | 0.89 |
| vector+bm25+graph | 0.85 | 0.92 | 0.92 | 0.69 | 0.82 | 0.89 |
| vector+bm25+temporal | 0.86 | 1.00 | 0.92 | 0.56 | 0.88 | 1.00 |
| full | 0.84 | 0.92 | 0.92 | 0.62 | 0.82 | 0.89 |
| full-graph | 0.86 | 1.00 | 0.92 | 0.56 | 0.88 | 1.00 |
| auto | 0.84 | 0.92 | 0.92 | 0.62 | 0.82 | 0.89 |

## Latency (ms per query, recall k=20)

| config | mean | p95 |
|---|---|---|
| vector | 104 | 49 |
| bm25 | 5 | 5 |
| vector+bm25 | 41 | 43 |
| vector+bm25+graph | 193 | 215 |
| vector+bm25+temporal | 83 | 87 |
| full | 160 | 223 |
| full-graph | 89 | 96 |
| auto | 173 | 261 |

## Paired bootstrap (1000 resamples, seed 0, 95% CI of mean delta)

- all questions, recall@10: `full` vs `vector+bm25+temporal`: delta -0.010 [-0.042, +0.025] (n=80, inside noise)
- all questions, fullcover@10: `full` vs `vector+bm25+temporal`: delta -0.013 [-0.075, +0.050] (n=80, inside noise)
- odd questions, recall@10: `full` vs `vector+bm25+temporal`: delta -0.033 [-0.083, +0.025] (n=40, inside noise)
- odd questions, fullcover@10: `full` vs `vector+bm25+temporal`: delta -0.050 [-0.150, +0.050] (n=40, inside noise)
- even questions, recall@10: `full` vs `vector+bm25+temporal`: delta +0.013 [-0.025, +0.050] (n=40, inside noise)
- even questions, fullcover@10: `full` vs `vector+bm25+temporal`: delta +0.025 [-0.050, +0.100] (n=40, inside noise)
- multi+ownership, recall@10: `full` vs `vector+bm25+temporal`: delta -0.031 [-0.089, +0.027] (n=43, inside noise)
- multi+ownership, fullcover@10: `full` vs `vector+bm25+temporal`: delta -0.047 [-0.163, +0.070] (n=43, inside noise)
- all questions, recall@10: `auto` vs `vector+bm25+temporal`: delta -0.013 [-0.054, +0.027] (n=80, inside noise)
- all questions, fullcover@10: `auto` vs `vector+bm25+temporal`: delta +0.000 [-0.075, +0.075] (n=80, inside noise)
- odd questions, recall@10: `auto` vs `vector+bm25+temporal`: delta -0.058 [-0.133, +0.004] (n=40, inside noise)
- odd questions, fullcover@10: `auto` vs `vector+bm25+temporal`: delta -0.075 [-0.175, +0.025] (n=40, inside noise)
- even questions, recall@10: `auto` vs `vector+bm25+temporal`: delta +0.033 [+0.000, +0.071] (n=40, inside noise)
- even questions, fullcover@10: `auto` vs `vector+bm25+temporal`: delta +0.075 [+0.000, +0.150] (n=40, inside noise)
- multi+ownership, recall@10: `auto` vs `vector+bm25+temporal`: delta -0.012 [-0.066, +0.043] (n=43, inside noise)
- multi+ownership, fullcover@10: `auto` vs `vector+bm25+temporal`: delta +0.000 [-0.116, +0.116] (n=43, inside noise)

## Tools vs vector-only baselines

- `ask` evidence pack vs top-8 vector chunk text, gold answer keys present: tools.ask multi 0.77 / ownership 0.76 (n=26/17); baseline multi 0.85 / ownership 0.82; mean size 3788 vs 9950 chars; ask 256 ms
- `who` (topic = whole question): gold person in top 3 (any) 0.82, all gold people 0.71 (n=17)
- `who` (topic = gold non-person entity): gold person in top 3 (any) 1.00, all gold people 0.88 (n=17)
- `timeline` on the gold entity (n=8 temporal questions with an old to new value): both values listed 0.50, old before new 0.50, both on dated lines 0.50; baseline top-8 vector text: both values 0.75, both values and at least two ISO dates 0.75
- `who` baseline (people of the top-10 vector-only docs, scored by 1/rank): any 0.71, all 0.65 (n=17)

### Paired bootstrap, tool minus baseline

- multi+ownership, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.070 [-0.163, +0.023] (n=43, inside noise)
- multi, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.077 [-0.231, +0.077] (n=26, inside noise)
- ownership, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.059 [-0.176, +0.000] (n=17, inside noise)
- ownership, who top3 any (question topic): `tools.who` vs `vector top-10 people`: delta +0.118 [+0.000, +0.294] (n=17, inside noise)
- ownership, who top3 all (question topic): `tools.who` vs `vector top-10 people`: delta +0.059 [-0.176, +0.294] (n=17, inside noise)
- ownership, who top3 any (entity topic): `tools.who` vs `vector top-10 people`: delta +0.294 [+0.118, +0.529] (n=17, significant)
- ownership, who top3 all (entity topic): `tools.who` vs `vector top-10 people`: delta +0.235 [-0.059, +0.529] (n=17, inside noise)
- temporal, both old+new value present: `tools.timeline` vs `vector top-8 text`: delta -0.250 [-0.625, +0.250] (n=8, inside noise)

## Clean vs distract

Distract = the synthetic tenant plus data/public/falkordb docs and tickets in the same tenant (507 documents in the graph vs 102 clean). Same 80 questions, same gold docs. R = Recall@10, FC = FullCover@10, M+O = multi + ownership questions (n=43).

| config | clean R | clean FC | clean M+O R | clean M+O FC | distract R | distract FC | distract M+O R | distract M+O FC | ms/q clean / distract |
|---|---|---|---|---|---|---|---|---|---|
| vector | 0.73 | 0.53 | 0.65 | 0.33 | 0.71 | 0.51 | 0.65 | 0.33 | 104 / 108 |
| bm25 | 0.71 | 0.55 | 0.71 | 0.49 | 0.70 | 0.53 | 0.69 | 0.47 | 5 / 25 |
| vector+bm25 | 0.75 | 0.59 | 0.69 | 0.47 | 0.75 | 0.57 | 0.71 | 0.47 | 41 / 60 |
| vector+bm25+graph | 0.75 | 0.61 | 0.71 | 0.51 | 0.73 | 0.55 | 0.67 | 0.42 | 193 / 322 |
| vector+bm25+temporal | 0.75 | 0.60 | 0.72 | 0.51 | 0.74 | 0.55 | 0.70 | 0.44 | 83 / 101 |
| full | 0.74 | 0.59 | 0.69 | 0.47 | 0.73 | 0.56 | 0.66 | 0.42 | 160 / 269 |
| full-graph | 0.75 | 0.60 | 0.72 | 0.51 | 0.74 | 0.55 | 0.70 | 0.44 | 89 / 106 |
| auto | 0.74 | 0.60 | 0.71 | 0.51 | 0.73 | 0.56 | 0.67 | 0.44 | 173 / 302 |

- Bootstrap, clean (paired, 95% CI of mean delta vs the best non-graph config):
  - all questions, recall@10: `full` vs `vector+bm25+temporal`: delta -0.010 [-0.042, +0.025] (inside noise)
  - all questions, fullcover@10: `full` vs `vector+bm25+temporal`: delta -0.013 [-0.075, +0.050] (inside noise)
  - multi+ownership, recall@10: `full` vs `vector+bm25+temporal`: delta -0.031 [-0.089, +0.027] (inside noise)
  - multi+ownership, fullcover@10: `full` vs `vector+bm25+temporal`: delta -0.047 [-0.163, +0.070] (inside noise)
  - all questions, recall@10: `auto` vs `vector+bm25+temporal`: delta -0.013 [-0.054, +0.027] (inside noise)
  - all questions, fullcover@10: `auto` vs `vector+bm25+temporal`: delta +0.000 [-0.075, +0.075] (inside noise)
  - multi+ownership, recall@10: `auto` vs `vector+bm25+temporal`: delta -0.012 [-0.066, +0.043] (inside noise)
  - multi+ownership, fullcover@10: `auto` vs `vector+bm25+temporal`: delta +0.000 [-0.116, +0.116] (inside noise)
- Bootstrap, distract (paired, 95% CI of mean delta vs the best non-graph config):
  - all questions, recall@10: `full` vs `vector+bm25`: delta -0.021 [-0.052, +0.010] (inside noise)
  - all questions, fullcover@10: `full` vs `vector+bm25`: delta -0.013 [-0.062, +0.037] (inside noise)
  - multi+ownership, recall@10: `full` vs `vector+bm25`: delta -0.047 [-0.105, +0.000] (inside noise)
  - multi+ownership, fullcover@10: `full` vs `vector+bm25`: delta -0.047 [-0.140, +0.047] (inside noise)
  - all questions, recall@10: `auto` vs `vector+bm25`: delta -0.019 [-0.044, +0.006] (inside noise)
  - all questions, fullcover@10: `auto` vs `vector+bm25`: delta -0.013 [-0.050, +0.025] (inside noise)
  - multi+ownership, recall@10: `auto` vs `vector+bm25`: delta -0.035 [-0.081, +0.012] (inside noise)
  - multi+ownership, fullcover@10: `auto` vs `vector+bm25`: delta -0.023 [-0.093, +0.047] (inside noise)

- Tools, clean: ask answer-in-output multi 0.77 / ownership 0.76 vs vector top-8 text 0.85 / 0.82; who top-3 (question topic) any 0.82 / all 0.71, (entity topic) 1.00 / 0.88, vector baseline 0.71 / 0.65; timeline both values 0.50, ordered 0.50, dated 0.50 vs vector both 0.75 / with dates 0.75 (n=8)
  - multi+ownership, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.070 [-0.163, +0.023] (inside noise)
  - ownership, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.059 [-0.176, +0.000] (inside noise)
  - ownership, who top3 any (question topic): `tools.who` vs `vector top-10 people`: delta +0.118 [+0.000, +0.294] (inside noise)
  - ownership, who top3 all (question topic): `tools.who` vs `vector top-10 people`: delta +0.059 [-0.176, +0.294] (inside noise)
  - ownership, who top3 any (entity topic): `tools.who` vs `vector top-10 people`: delta +0.294 [+0.118, +0.529] (significant)
  - ownership, who top3 all (entity topic): `tools.who` vs `vector top-10 people`: delta +0.235 [-0.059, +0.529] (inside noise)
  - temporal, both old+new value present: `tools.timeline` vs `vector top-8 text`: delta -0.250 [-0.625, +0.250] (inside noise)
- Tools, distract: ask answer-in-output multi 0.81 / ownership 0.76 vs vector top-8 text 0.85 / 0.82; who top-3 (question topic) any 0.41 / all 0.41, (entity topic) 1.00 / 0.88, vector baseline 0.71 / 0.65; timeline both values 0.50, ordered 0.50, dated 0.50 vs vector both 0.75 / with dates 0.75 (n=8)
  - multi+ownership, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.047 [-0.140, +0.047] (inside noise)
  - ownership, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.059 [-0.176, +0.000] (inside noise)
  - ownership, who top3 any (question topic): `tools.who` vs `vector top-10 people`: delta -0.294 [-0.588, +0.000] (inside noise)
  - ownership, who top3 all (question topic): `tools.who` vs `vector top-10 people`: delta -0.235 [-0.471, +0.000] (inside noise)
  - ownership, who top3 any (entity topic): `tools.who` vs `vector top-10 people`: delta +0.294 [+0.118, +0.529] (significant)
  - ownership, who top3 all (entity topic): `tools.who` vs `vector top-10 people`: delta +0.235 [-0.059, +0.529] (inside noise)
  - temporal, both old+new value present: `tools.timeline` vs `vector top-8 text`: delta -0.250 [-0.625, +0.250] (inside noise)

## Graph-native answers

Run `new extraction`. DB: `/home/bindesh/neo-cortex/.neo/gq` (port 6365, tenant `eval`). no eval_ingest.json under /home/bindesh/neo-cortex/.neo/gq; build time unknown
Tool: `tools.who`/`impact`/`timeline`, max_chars 4000. Baseline: top-8 vector chunks via `tools.read`, capped at 4000 chars.

| category | n | keys, tool | keys, baseline | all keys, tool | all keys, baseline | correct current, tool | correct current, baseline |
|---|---|---|---|---|---|---|---|
| overall | 30 | 0.82 | 0.78 | 0.77 | 0.73 | 0.90 | 1.00 |
| current_owner | 10 | 1.00 | 1.00 | 1.00 | 1.00 | 0.90 | 1.00 |
| impact | 10 | 0.80 | 0.34 | 0.80 | 0.20 | - | - |
| changes | 10 | 0.67 | 1.00 | 0.50 | 1.00 | - | - |

Paired bootstrap (1000 resamples, seed 0, 95% CI of mean delta, tool minus baseline):
- all keys, overall: +0.03 [-0.17, +0.27] (n=30, inside noise)
- all keys, current_owner: +0.00 [+0.00, +0.00] (n=10, inside noise)
- all keys, impact: +0.60 [+0.30, +0.90] (n=10, significant)
- all keys, changes: -0.50 [-0.80, -0.20] (n=10, significant)
- correct current, current_owner: -0.10 [-0.30, +0.00] (n=10, inside noise)

Questions where a side misses a key (tool / baseline missing):
- IM01: tool ok; baseline missing ["api-gateway", "web-dashboard", "payment-gateway"]
- IM02: tool ok; baseline missing ["api-gateway", "bank-connector", "notification-service", "web-dashboard", "payment-gateway"]
- IM03: tool ok; baseline missing ["reporting-service", "fraud-scoring", "notification-service"]
- IM04: tool ok; baseline missing ["api-gateway", "web-dashboard"]
- IM06: tool ok; baseline missing ["payment-gateway"]
- IM07: tool missing ["payment-gateway"]; baseline missing ["payment-gateway"]
- IM09: tool missing ["payment-gateway"]; baseline missing ["payment-gateway"]
- IM10: tool ok; baseline missing ["api-gateway", "web-dashboard", "payment-gateway"]
- CH03: tool missing ["two approvers"]; baseline ok
- CH06: tool missing ["4 GB"]; baseline ok
- CH08: tool missing ["txn_id:attempt", "txn_id"]; baseline ok
- CH09: tool missing ["800", "80"]; baseline ok
- CH10: tool missing ["bank_connector.banks.tidewater.cutoff"]; baseline ok

Other run, `old extraction` (/home/bindesh/neo-cortex/.neo/eval-new): overall all keys tool 0.50 vs baseline 0.73; impact 0.00 vs 0.20; changes 0.50 vs 1.00.
