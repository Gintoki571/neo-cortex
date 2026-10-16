# Retrieval evaluation

Synthetic Pellucid Pay corpus (102 docs, AI-generated, fictional), 40 gold questions, k=20 chunks collapsed to unique documents, fixed now = 2026-10-16T00:00Z. Hit/Recall/FullCover/MRR are against `gold_docs`; AnswerIn = normalised gold answer found in the retrieved chunk text (full chunk text of the first k unique documents, so it only checks that the answer string was retrieved, not that it is easy to extract).

Ingest: {'skipped': True, 'documents_in_graph': 102, 'first_ingest': {'documents': 102, 'chunks': 136, 'mentions': 676, 'rels': 52, 'errors': 0, 'new_entities': 163, 'seconds': 332.4}}

## recall@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.72 | 1.00 | 0.61 | 0.56 | 0.64 | 0.87 |
| bm25 | 0.66 | 0.88 | 0.64 | 0.50 | 0.64 | 0.67 |
| vector+bm25 | 0.71 | 1.00 | 0.68 | 0.50 | 0.64 | 0.73 |
| vector+bm25+graph | 0.64 | 0.88 | 0.60 | 0.50 | 0.64 | 0.60 |
| vector+bm25+temporal | 0.72 | 1.00 | 0.68 | 0.50 | 0.64 | 0.80 |
| full | 0.66 | 0.88 | 0.64 | 0.50 | 0.64 | 0.67 |
| full-graph | 0.72 | 1.00 | 0.68 | 0.50 | 0.64 | 0.80 |
| auto | 0.65 | 0.88 | 0.64 | 0.50 | 0.64 | 0.60 |

## fullcover@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.55 | 1.00 | 0.25 | 0.50 | 0.43 | 0.80 |
| bm25 | 0.47 | 0.88 | 0.33 | 0.38 | 0.43 | 0.40 |
| vector+bm25 | 0.53 | 1.00 | 0.42 | 0.38 | 0.43 | 0.40 |
| vector+bm25+graph | 0.47 | 0.88 | 0.33 | 0.38 | 0.43 | 0.40 |
| vector+bm25+temporal | 0.55 | 1.00 | 0.42 | 0.38 | 0.43 | 0.60 |
| full | 0.50 | 0.88 | 0.42 | 0.38 | 0.43 | 0.40 |
| full-graph | 0.55 | 1.00 | 0.42 | 0.38 | 0.43 | 0.60 |
| auto | 0.50 | 0.88 | 0.42 | 0.38 | 0.43 | 0.40 |

## answerin@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| bm25 | 0.38 | 0.88 | 0.33 | 0.00 | 0.57 | 0.00 |
| vector+bm25 | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| vector+bm25+graph | 0.38 | 0.75 | 0.33 | 0.00 | 0.71 | 0.00 |
| vector+bm25+temporal | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| full | 0.38 | 0.75 | 0.33 | 0.00 | 0.71 | 0.00 |
| full-graph | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| auto | 0.38 | 0.75 | 0.33 | 0.00 | 0.71 | 0.00 |

## mrr@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.60 | 0.67 | 0.53 | 0.42 | 0.62 | 0.90 |
| bm25 | 0.57 | 0.55 | 0.53 | 0.38 | 0.79 | 0.67 |
| vector+bm25 | 0.55 | 0.46 | 0.60 | 0.41 | 0.59 | 0.70 |
| vector+bm25+graph | 0.56 | 0.51 | 0.57 | 0.47 | 0.52 | 0.80 |
| vector+bm25+temporal | 0.52 | 0.50 | 0.47 | 0.52 | 0.50 | 0.75 |
| full | 0.52 | 0.47 | 0.50 | 0.52 | 0.49 | 0.72 |
| full-graph | 0.52 | 0.50 | 0.47 | 0.52 | 0.50 | 0.75 |
| auto | 0.57 | 0.51 | 0.61 | 0.52 | 0.52 | 0.70 |

## hit@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.88 | 1.00 | 0.92 | 0.62 | 0.86 | 1.00 |
| bm25 | 0.85 | 0.88 | 0.92 | 0.62 | 0.86 | 1.00 |
| vector+bm25 | 0.88 | 1.00 | 0.92 | 0.62 | 0.86 | 1.00 |
| vector+bm25+graph | 0.80 | 0.88 | 0.83 | 0.62 | 0.86 | 0.80 |
| vector+bm25+temporal | 0.88 | 1.00 | 0.92 | 0.62 | 0.86 | 1.00 |
| full | 0.82 | 0.88 | 0.83 | 0.62 | 0.86 | 1.00 |
| full-graph | 0.88 | 1.00 | 0.92 | 0.62 | 0.86 | 1.00 |
| auto | 0.80 | 0.88 | 0.83 | 0.62 | 0.86 | 0.80 |

## recall@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.61 | 0.88 | 0.46 | 0.50 | 0.50 | 0.87 |
| bm25 | 0.54 | 0.88 | 0.43 | 0.40 | 0.50 | 0.57 |
| vector+bm25 | 0.60 | 1.00 | 0.46 | 0.46 | 0.57 | 0.60 |
| vector+bm25+graph | 0.57 | 0.88 | 0.42 | 0.46 | 0.57 | 0.60 |
| vector+bm25+temporal | 0.60 | 1.00 | 0.50 | 0.38 | 0.50 | 0.67 |
| full | 0.54 | 0.88 | 0.42 | 0.38 | 0.50 | 0.60 |
| full-graph | 0.60 | 1.00 | 0.50 | 0.38 | 0.50 | 0.67 |
| auto | 0.54 | 0.88 | 0.42 | 0.38 | 0.50 | 0.60 |

## fullcover@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.40 | 0.88 | 0.00 | 0.38 | 0.29 | 0.80 |
| bm25 | 0.33 | 0.88 | 0.17 | 0.12 | 0.14 | 0.40 |
| vector+bm25 | 0.40 | 1.00 | 0.08 | 0.25 | 0.43 | 0.40 |
| vector+bm25+graph | 0.35 | 0.88 | 0.00 | 0.25 | 0.43 | 0.40 |
| vector+bm25+temporal | 0.38 | 1.00 | 0.08 | 0.25 | 0.29 | 0.40 |
| full | 0.33 | 0.88 | 0.00 | 0.25 | 0.29 | 0.40 |
| full-graph | 0.38 | 1.00 | 0.08 | 0.25 | 0.29 | 0.40 |
| auto | 0.33 | 0.88 | 0.00 | 0.25 | 0.29 | 0.40 |

## answerin@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.38 | 0.88 | 0.25 | 0.00 | 0.71 | 0.00 |
| bm25 | 0.38 | 0.88 | 0.33 | 0.00 | 0.57 | 0.00 |
| vector+bm25 | 0.38 | 0.88 | 0.33 | 0.00 | 0.57 | 0.00 |
| vector+bm25+graph | 0.35 | 0.75 | 0.33 | 0.00 | 0.57 | 0.00 |
| vector+bm25+temporal | 0.38 | 0.88 | 0.33 | 0.00 | 0.57 | 0.00 |
| full | 0.35 | 0.75 | 0.33 | 0.00 | 0.57 | 0.00 |
| full-graph | 0.38 | 0.88 | 0.33 | 0.00 | 0.57 | 0.00 |
| auto | 0.35 | 0.75 | 0.33 | 0.00 | 0.57 | 0.00 |

## mrr@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.59 | 0.65 | 0.53 | 0.42 | 0.60 | 0.90 |
| bm25 | 0.56 | 0.55 | 0.51 | 0.38 | 0.79 | 0.64 |
| vector+bm25 | 0.53 | 0.46 | 0.59 | 0.41 | 0.57 | 0.67 |
| vector+bm25+graph | 0.55 | 0.51 | 0.57 | 0.47 | 0.50 | 0.80 |
| vector+bm25+temporal | 0.52 | 0.50 | 0.47 | 0.50 | 0.48 | 0.75 |
| full | 0.52 | 0.47 | 0.50 | 0.50 | 0.48 | 0.70 |
| full-graph | 0.52 | 0.50 | 0.47 | 0.50 | 0.48 | 0.75 |
| auto | 0.56 | 0.51 | 0.61 | 0.50 | 0.50 | 0.70 |

## hit@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.82 | 0.88 | 0.92 | 0.62 | 0.71 | 1.00 |
| bm25 | 0.78 | 0.88 | 0.75 | 0.62 | 0.86 | 0.80 |
| vector+bm25 | 0.80 | 1.00 | 0.83 | 0.62 | 0.71 | 0.80 |
| vector+bm25+graph | 0.78 | 0.88 | 0.83 | 0.62 | 0.71 | 0.80 |
| vector+bm25+temporal | 0.82 | 1.00 | 0.92 | 0.50 | 0.71 | 1.00 |
| full | 0.75 | 0.88 | 0.83 | 0.50 | 0.71 | 0.80 |
| full-graph | 0.82 | 1.00 | 0.92 | 0.50 | 0.71 | 1.00 |
| auto | 0.75 | 0.88 | 0.83 | 0.50 | 0.71 | 0.80 |

## Latency (ms per query, recall k=20)

| config | mean | p95 |
|---|---|---|
| vector | 213 | 106 |
| bm25 | 6 | 6 |
| vector+bm25 | 87 | 105 |
| vector+bm25+graph | 609 | 666 |
| vector+bm25+temporal | 480 | 534 |
| full | 535 | 661 |
| full-graph | 480 | 542 |
| auto | 588 | 754 |

## Paired bootstrap (1000 resamples, seed 0, 95% CI of mean delta)

- all questions, recall@10: `full` vs `vector`: delta -0.054 [-0.150, +0.021] (n=40, inside noise)
- all questions, fullcover@10: `full` vs `vector`: delta -0.050 [-0.200, +0.075] (n=40, inside noise)
- multi+ownership, recall@10: `full` vs `vector`: delta +0.018 [-0.088, +0.132] (n=19, inside noise)
- multi+ownership, fullcover@10: `full` vs `vector`: delta +0.105 [-0.053, +0.316] (n=19, inside noise)

## Tools

- `ask` evidence pack, gold answer string present: multi 0.17 (n=12), ownership 0.43 (n=7); mean 897 ms
- `who` (topic = whole question): gold person in top 3 (any) 0.57, all gold people 0.43 (n=7)
- `who` (topic = gold non-person entity): gold person in top 3 (any) 0.86, all gold people 0.86 (n=7)
