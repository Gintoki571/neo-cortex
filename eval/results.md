# Retrieval evaluation

Synthetic Pellucid Pay corpus, setting clean (102 docs in the graph, AI-generated, fictional), 80 gold questions, k=20 chunks collapsed to unique documents, fixed now = 2026-10-16T00:00Z. Hit/Recall/FullCover/MRR are against `gold_docs`; AnswerIn = normalised gold answer found in the retrieved chunk text (full chunk text of the first k unique documents, so it only checks that the answer string was retrieved, not that it is easy to extract).

Ingest: {'documents': 102, 'skipped': 0, 'chunks': 136, 'mentions': 835, 'rels': 97, 'errors': 0, 'unsupported': 0, 'new_entities': 130, 'seconds': 85.5, 'documents_in_graph': 102}

## recall@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.73 | 1.00 | 0.61 | 0.62 | 0.71 | 0.93 |
| bm25 | 0.71 | 0.92 | 0.63 | 0.53 | 0.79 | 0.81 |
| vector+bm25 | 0.75 | 1.00 | 0.65 | 0.66 | 0.76 | 0.85 |
| vector+bm25+graph | 0.74 | 1.00 | 0.60 | 0.66 | 0.76 | 0.85 |
| vector+bm25+temporal | 0.75 | 1.00 | 0.65 | 0.56 | 0.82 | 0.89 |
| full | 0.76 | 1.00 | 0.67 | 0.56 | 0.82 | 0.89 |
| full-graph | 0.75 | 1.00 | 0.65 | 0.56 | 0.82 | 0.89 |
| auto | 0.74 | 1.00 | 0.65 | 0.56 | 0.79 | 0.85 |

## fullcover@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.53 | 1.00 | 0.23 | 0.50 | 0.47 | 0.89 |
| bm25 | 0.54 | 0.92 | 0.35 | 0.38 | 0.65 | 0.67 |
| vector+bm25 | 0.59 | 1.00 | 0.38 | 0.56 | 0.59 | 0.67 |
| vector+bm25+graph | 0.55 | 1.00 | 0.27 | 0.56 | 0.59 | 0.67 |
| vector+bm25+temporal | 0.59 | 1.00 | 0.38 | 0.38 | 0.71 | 0.78 |
| full | 0.60 | 1.00 | 0.42 | 0.38 | 0.71 | 0.78 |
| full-graph | 0.59 | 1.00 | 0.38 | 0.38 | 0.71 | 0.78 |
| auto | 0.56 | 1.00 | 0.38 | 0.38 | 0.65 | 0.67 |

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
| vector | 0.64 | 0.67 | 0.59 | 0.52 | 0.68 | 0.87 |
| bm25 | 0.61 | 0.62 | 0.60 | 0.36 | 0.75 | 0.76 |
| vector+bm25 | 0.63 | 0.59 | 0.65 | 0.43 | 0.72 | 0.78 |
| vector+bm25+graph | 0.65 | 0.70 | 0.69 | 0.46 | 0.73 | 0.69 |
| vector+bm25+temporal | 0.61 | 0.58 | 0.60 | 0.51 | 0.65 | 0.81 |
| full | 0.65 | 0.61 | 0.66 | 0.51 | 0.68 | 0.81 |
| full-graph | 0.61 | 0.58 | 0.60 | 0.51 | 0.65 | 0.81 |
| auto | 0.66 | 0.70 | 0.69 | 0.51 | 0.72 | 0.67 |

## hit@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.93 | 1.00 | 0.96 | 0.75 | 0.94 | 1.00 |
| bm25 | 0.89 | 0.92 | 0.92 | 0.69 | 0.94 | 1.00 |
| vector+bm25 | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |
| vector+bm25+graph | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |
| vector+bm25+temporal | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |
| full | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |
| full-graph | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |
| auto | 0.91 | 1.00 | 0.92 | 0.75 | 0.94 | 1.00 |

## recall@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.61 | 0.83 | 0.45 | 0.53 | 0.62 | 0.87 |
| bm25 | 0.57 | 0.92 | 0.42 | 0.39 | 0.65 | 0.70 |
| vector+bm25 | 0.65 | 1.00 | 0.48 | 0.51 | 0.71 | 0.78 |
| vector+bm25+graph | 0.65 | 1.00 | 0.49 | 0.51 | 0.71 | 0.81 |
| vector+bm25+temporal | 0.62 | 1.00 | 0.50 | 0.44 | 0.62 | 0.81 |
| full | 0.62 | 1.00 | 0.49 | 0.44 | 0.62 | 0.81 |
| full-graph | 0.62 | 1.00 | 0.50 | 0.44 | 0.62 | 0.81 |
| auto | 0.63 | 1.00 | 0.49 | 0.44 | 0.68 | 0.81 |

## fullcover@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.39 | 0.83 | 0.08 | 0.38 | 0.35 | 0.78 |
| bm25 | 0.36 | 0.92 | 0.15 | 0.19 | 0.35 | 0.56 |
| vector+bm25 | 0.44 | 1.00 | 0.12 | 0.31 | 0.53 | 0.67 |
| vector+bm25+graph | 0.44 | 1.00 | 0.12 | 0.31 | 0.53 | 0.67 |
| vector+bm25+temporal | 0.40 | 1.00 | 0.12 | 0.31 | 0.35 | 0.67 |
| full | 0.40 | 1.00 | 0.12 | 0.31 | 0.35 | 0.67 |
| full-graph | 0.40 | 1.00 | 0.12 | 0.31 | 0.35 | 0.67 |
| auto | 0.42 | 1.00 | 0.12 | 0.31 | 0.47 | 0.67 |

## answerin@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.36 | 0.92 | 0.23 | 0.00 | 0.65 | 0.11 |
| bm25 | 0.39 | 0.92 | 0.31 | 0.00 | 0.65 | 0.11 |
| vector+bm25 | 0.40 | 0.92 | 0.35 | 0.00 | 0.65 | 0.11 |
| vector+bm25+graph | 0.41 | 0.92 | 0.35 | 0.00 | 0.71 | 0.11 |
| vector+bm25+temporal | 0.39 | 0.92 | 0.35 | 0.00 | 0.59 | 0.11 |
| full | 0.39 | 0.92 | 0.35 | 0.00 | 0.59 | 0.11 |
| full-graph | 0.39 | 0.92 | 0.35 | 0.00 | 0.59 | 0.11 |
| auto | 0.41 | 0.92 | 0.35 | 0.00 | 0.71 | 0.11 |

## mrr@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.62 | 0.64 | 0.57 | 0.51 | 0.67 | 0.87 |
| bm25 | 0.59 | 0.62 | 0.57 | 0.35 | 0.75 | 0.74 |
| vector+bm25 | 0.62 | 0.59 | 0.65 | 0.42 | 0.72 | 0.76 |
| vector+bm25+graph | 0.65 | 0.70 | 0.69 | 0.45 | 0.73 | 0.69 |
| vector+bm25+temporal | 0.61 | 0.58 | 0.60 | 0.48 | 0.64 | 0.81 |
| full | 0.64 | 0.61 | 0.66 | 0.48 | 0.67 | 0.81 |
| full-graph | 0.61 | 0.58 | 0.60 | 0.48 | 0.64 | 0.81 |
| auto | 0.65 | 0.70 | 0.69 | 0.48 | 0.72 | 0.67 |

## hit@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.84 | 0.83 | 0.85 | 0.69 | 0.88 | 1.00 |
| bm25 | 0.79 | 0.92 | 0.73 | 0.56 | 0.94 | 0.89 |
| vector+bm25 | 0.86 | 1.00 | 0.88 | 0.69 | 0.88 | 0.89 |
| vector+bm25+graph | 0.89 | 1.00 | 0.92 | 0.69 | 0.88 | 1.00 |
| vector+bm25+temporal | 0.86 | 1.00 | 0.92 | 0.56 | 0.88 | 1.00 |
| full | 0.86 | 1.00 | 0.92 | 0.56 | 0.88 | 1.00 |
| full-graph | 0.86 | 1.00 | 0.92 | 0.56 | 0.88 | 1.00 |
| auto | 0.86 | 1.00 | 0.92 | 0.56 | 0.88 | 1.00 |

## Latency (ms per query, recall k=20)

| config | mean | p95 |
|---|---|---|
| vector | 36 | 37 |
| bm25 | 6 | 6 |
| vector+bm25 | 40 | 42 |
| vector+bm25+graph | 130 | 183 |
| vector+bm25+temporal | 88 | 92 |
| full | 140 | 198 |
| full-graph | 89 | 92 |
| auto | 139 | 197 |

## Paired bootstrap (1000 resamples, seed 0, 95% CI of mean delta)

- all questions, recall@10: `full` vs `vector+bm25`: delta +0.006 [-0.029, +0.040] (n=80, inside noise)
- all questions, fullcover@10: `full` vs `vector+bm25`: delta +0.013 [-0.062, +0.087] (n=80, inside noise)
- odd questions, recall@10: `full` vs `vector+bm25`: delta +0.025 [-0.013, +0.075] (n=40, inside noise)
- odd questions, fullcover@10: `full` vs `vector+bm25`: delta +0.050 [-0.025, +0.150] (n=40, inside noise)
- even questions, recall@10: `full` vs `vector+bm25`: delta -0.013 [-0.062, +0.042] (n=40, inside noise)
- even questions, fullcover@10: `full` vs `vector+bm25`: delta -0.025 [-0.150, +0.100] (n=40, inside noise)
- multi+ownership, recall@10: `full` vs `vector+bm25`: delta +0.039 [-0.004, +0.089] (n=43, inside noise)
- multi+ownership, fullcover@10: `full` vs `vector+bm25`: delta +0.070 [-0.023, +0.163] (n=43, inside noise)
- all questions, recall@10: `auto` vs `vector+bm25`: delta -0.010 [-0.044, +0.023] (n=80, inside noise)
- all questions, fullcover@10: `auto` vs `vector+bm25`: delta -0.025 [-0.087, +0.037] (n=80, inside noise)
- odd questions, recall@10: `auto` vs `vector+bm25`: delta +0.013 [-0.025, +0.062] (n=40, inside noise)
- odd questions, fullcover@10: `auto` vs `vector+bm25`: delta +0.025 [-0.050, +0.125] (n=40, inside noise)
- even questions, recall@10: `auto` vs `vector+bm25`: delta -0.033 [-0.083, +0.017] (n=40, inside noise)
- even questions, fullcover@10: `auto` vs `vector+bm25`: delta -0.075 [-0.175, +0.025] (n=40, inside noise)
- multi+ownership, recall@10: `auto` vs `vector+bm25`: delta +0.016 [-0.027, +0.062] (n=43, inside noise)
- multi+ownership, fullcover@10: `auto` vs `vector+bm25`: delta +0.023 [-0.070, +0.116] (n=43, inside noise)

## Tools vs vector-only baselines

- `ask` evidence pack vs top-8 vector chunk text, gold answer keys present: tools.ask multi 0.65 / ownership 0.76 (n=26/17); baseline multi 0.85 / ownership 0.82; mean size 3810 vs 9932 chars; ask 205 ms
- `who` (topic = whole question): gold person in top 3 (any) 0.82, all gold people 0.71 (n=17)
- `who` (topic = gold non-person entity): gold person in top 3 (any) 0.94, all gold people 0.88 (n=17)
- `timeline` on the gold entity (n=8 temporal questions with an old to new value): both values listed 1.00, old before new 0.88, both on dated lines 1.00; baseline top-8 vector text: both values 0.75, both values and at least two ISO dates 0.75
- `who` baseline (people of the top-10 vector-only docs, scored by 1/rank): any 0.71, all 0.65 (n=17)

### Paired bootstrap, tool minus baseline

- multi+ownership, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.140 [-0.256, -0.023] (n=43, significant)
- multi, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.192 [-0.385, +0.000] (n=26, inside noise)
- ownership, answer-in-output: `tools.ask` vs `vector top-8 text`: delta -0.059 [-0.176, +0.000] (n=17, inside noise)
- ownership, who top3 any (question topic): `tools.who` vs `vector top-10 people`: delta +0.118 [-0.118, +0.353] (n=17, inside noise)
- ownership, who top3 all (question topic): `tools.who` vs `vector top-10 people`: delta +0.059 [-0.235, +0.353] (n=17, inside noise)
- ownership, who top3 any (entity topic): `tools.who` vs `vector top-10 people`: delta +0.235 [+0.000, +0.471] (n=17, inside noise)
- ownership, who top3 all (entity topic): `tools.who` vs `vector top-10 people`: delta +0.235 [-0.059, +0.529] (n=17, inside noise)
- temporal, both old+new value present: `tools.timeline` vs `vector top-8 text`: delta +0.250 [+0.000, +0.500] (n=8, inside noise)
