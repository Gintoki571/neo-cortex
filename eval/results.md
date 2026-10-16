# Retrieval evaluation

Synthetic Pellucid Pay corpus (102 docs, AI-generated, fictional), 40 gold questions, k=20 chunks collapsed to unique documents, fixed now = 2026-10-16T00:00Z. Hit/Recall/FullCover/MRR are against `gold_docs`; AnswerIn = normalised gold answer found in the retrieved chunk text (full chunk text of the first k unique documents, so it only checks that the answer string was retrieved, not that it is easy to extract).

Ingest: {'skipped': True, 'documents_in_graph': 102, 'first_ingest': {'documents': 102, 'chunks': 136, 'mentions': 676, 'rels': 52, 'errors': 0, 'new_entities': 163, 'seconds': 332.4}}

## recall@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.77 | 1.00 | 0.61 | 0.69 | 0.79 | 0.87 |
| bm25 | 0.70 | 0.88 | 0.64 | 0.56 | 0.79 | 0.67 |
| vector+bm25 | 0.76 | 1.00 | 0.68 | 0.62 | 0.79 | 0.73 |
| vector+bm25+graph | 0.77 | 1.00 | 0.72 | 0.62 | 0.79 | 0.73 |
| vector+bm25+temporal | 0.77 | 1.00 | 0.68 | 0.62 | 0.79 | 0.80 |
| full | 0.77 | 1.00 | 0.72 | 0.62 | 0.71 | 0.80 |
| full-graph | 0.77 | 1.00 | 0.68 | 0.62 | 0.79 | 0.80 |
| auto | 0.78 | 1.00 | 0.75 | 0.62 | 0.79 | 0.73 |

## fullcover@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.60 | 1.00 | 0.25 | 0.62 | 0.57 | 0.80 |
| bm25 | 0.50 | 0.88 | 0.33 | 0.38 | 0.57 | 0.40 |
| vector+bm25 | 0.57 | 1.00 | 0.42 | 0.50 | 0.57 | 0.40 |
| vector+bm25+graph | 0.62 | 1.00 | 0.50 | 0.50 | 0.71 | 0.40 |
| vector+bm25+temporal | 0.60 | 1.00 | 0.42 | 0.50 | 0.57 | 0.60 |
| full | 0.62 | 1.00 | 0.50 | 0.50 | 0.57 | 0.60 |
| full-graph | 0.60 | 1.00 | 0.42 | 0.50 | 0.57 | 0.60 |
| auto | 0.65 | 1.00 | 0.58 | 0.50 | 0.71 | 0.40 |

## answerin@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.42 | 0.88 | 0.33 | 0.00 | 0.86 | 0.00 |
| bm25 | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| vector+bm25 | 0.42 | 0.88 | 0.33 | 0.00 | 0.86 | 0.00 |
| vector+bm25+graph | 0.42 | 0.88 | 0.33 | 0.00 | 0.86 | 0.00 |
| vector+bm25+temporal | 0.42 | 0.88 | 0.33 | 0.00 | 0.86 | 0.00 |
| full | 0.42 | 0.88 | 0.33 | 0.00 | 0.86 | 0.00 |
| full-graph | 0.42 | 0.88 | 0.33 | 0.00 | 0.86 | 0.00 |
| auto | 0.42 | 0.88 | 0.33 | 0.00 | 0.86 | 0.00 |

## mrr@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.63 | 0.67 | 0.53 | 0.46 | 0.76 | 0.90 |
| bm25 | 0.60 | 0.55 | 0.53 | 0.40 | 0.93 | 0.67 |
| vector+bm25 | 0.58 | 0.46 | 0.60 | 0.47 | 0.73 | 0.70 |
| vector+bm25+graph | 0.65 | 0.46 | 0.69 | 0.59 | 0.79 | 0.75 |
| vector+bm25+temporal | 0.56 | 0.50 | 0.47 | 0.56 | 0.64 | 0.75 |
| full | 0.62 | 0.51 | 0.62 | 0.59 | 0.69 | 0.75 |
| full-graph | 0.56 | 0.50 | 0.47 | 0.56 | 0.64 | 0.75 |
| auto | 0.66 | 0.46 | 0.72 | 0.59 | 0.79 | 0.75 |

## hit@10

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.93 | 1.00 | 0.92 | 0.75 | 1.00 | 1.00 |
| bm25 | 0.90 | 0.88 | 0.92 | 0.75 | 1.00 | 1.00 |
| vector+bm25 | 0.93 | 1.00 | 0.92 | 0.75 | 1.00 | 1.00 |
| vector+bm25+graph | 0.90 | 1.00 | 0.92 | 0.75 | 0.86 | 1.00 |
| vector+bm25+temporal | 0.93 | 1.00 | 0.92 | 0.75 | 1.00 | 1.00 |
| full | 0.90 | 1.00 | 0.92 | 0.75 | 0.86 | 1.00 |
| full-graph | 0.93 | 1.00 | 0.92 | 0.75 | 1.00 | 1.00 |
| auto | 0.90 | 1.00 | 0.92 | 0.75 | 0.86 | 1.00 |

## recall@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.66 | 0.88 | 0.46 | 0.62 | 0.64 | 0.87 |
| bm25 | 0.58 | 0.88 | 0.43 | 0.46 | 0.64 | 0.57 |
| vector+bm25 | 0.65 | 1.00 | 0.46 | 0.58 | 0.71 | 0.60 |
| vector+bm25+graph | 0.68 | 1.00 | 0.50 | 0.58 | 0.71 | 0.67 |
| vector+bm25+temporal | 0.63 | 1.00 | 0.50 | 0.44 | 0.64 | 0.67 |
| full | 0.67 | 1.00 | 0.50 | 0.54 | 0.71 | 0.67 |
| full-graph | 0.63 | 1.00 | 0.50 | 0.44 | 0.64 | 0.67 |
| auto | 0.67 | 1.00 | 0.50 | 0.54 | 0.71 | 0.67 |

## fullcover@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.45 | 0.88 | 0.00 | 0.50 | 0.43 | 0.80 |
| bm25 | 0.35 | 0.88 | 0.17 | 0.12 | 0.29 | 0.40 |
| vector+bm25 | 0.45 | 1.00 | 0.08 | 0.38 | 0.57 | 0.40 |
| vector+bm25+graph | 0.45 | 1.00 | 0.08 | 0.38 | 0.57 | 0.40 |
| vector+bm25+temporal | 0.40 | 1.00 | 0.08 | 0.25 | 0.43 | 0.40 |
| full | 0.45 | 1.00 | 0.08 | 0.38 | 0.57 | 0.40 |
| full-graph | 0.40 | 1.00 | 0.08 | 0.25 | 0.43 | 0.40 |
| auto | 0.45 | 1.00 | 0.08 | 0.38 | 0.57 | 0.40 |

## answerin@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.40 | 0.88 | 0.25 | 0.00 | 0.86 | 0.00 |
| bm25 | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| vector+bm25 | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| vector+bm25+graph | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| vector+bm25+temporal | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| full | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| full-graph | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |
| auto | 0.40 | 0.88 | 0.33 | 0.00 | 0.71 | 0.00 |

## mrr@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.62 | 0.65 | 0.53 | 0.46 | 0.74 | 0.90 |
| bm25 | 0.59 | 0.55 | 0.51 | 0.40 | 0.93 | 0.64 |
| vector+bm25 | 0.57 | 0.46 | 0.59 | 0.47 | 0.71 | 0.67 |
| vector+bm25+graph | 0.65 | 0.46 | 0.69 | 0.59 | 0.79 | 0.75 |
| vector+bm25+temporal | 0.55 | 0.50 | 0.47 | 0.54 | 0.62 | 0.75 |
| full | 0.62 | 0.51 | 0.62 | 0.59 | 0.69 | 0.75 |
| full-graph | 0.55 | 0.50 | 0.47 | 0.54 | 0.62 | 0.75 |
| auto | 0.66 | 0.46 | 0.72 | 0.59 | 0.79 | 0.75 |

## hit@5

| config | overall | single | multi | temporal | ownership | procedural |
|---|---|---|---|---|---|---|
| vector | 0.88 | 0.88 | 0.92 | 0.75 | 0.86 | 1.00 |
| bm25 | 0.82 | 0.88 | 0.75 | 0.75 | 1.00 | 0.80 |
| vector+bm25 | 0.85 | 1.00 | 0.83 | 0.75 | 0.86 | 0.80 |
| vector+bm25+graph | 0.90 | 1.00 | 0.92 | 0.75 | 0.86 | 1.00 |
| vector+bm25+temporal | 0.88 | 1.00 | 0.92 | 0.62 | 0.86 | 1.00 |
| full | 0.90 | 1.00 | 0.92 | 0.75 | 0.86 | 1.00 |
| full-graph | 0.88 | 1.00 | 0.92 | 0.62 | 0.86 | 1.00 |
| auto | 0.90 | 1.00 | 0.92 | 0.75 | 0.86 | 1.00 |

## Latency (ms per query, recall k=20)

| config | mean | p95 |
|---|---|---|
| vector | 217 | 94 |
| bm25 | 6 | 7 |
| vector+bm25 | 94 | 112 |
| vector+bm25+graph | 694 | 721 |
| vector+bm25+temporal | 546 | 590 |
| full | 659 | 760 |
| full-graph | 564 | 615 |
| auto | 592 | 745 |

## Paired bootstrap (1000 resamples, seed 0, 95% CI of mean delta)

- all questions, recall@10: `full` vs `vector`: delta +0.000 [-0.079, +0.079] (n=40, inside noise)
- all questions, fullcover@10: `full` vs `vector`: delta +0.025 [-0.125, +0.175] (n=40, inside noise)
- odd questions, recall@10: `full` vs `vector`: delta -0.058 [-0.150, +0.025] (n=20, inside noise)
- odd questions, fullcover@10: `full` vs `vector`: delta -0.050 [-0.200, +0.100] (n=20, inside noise)
- even questions, recall@10: `full` vs `vector`: delta +0.058 [-0.075, +0.192] (n=20, inside noise)
- even questions, fullcover@10: `full` vs `vector`: delta +0.100 [-0.150, +0.350] (n=20, inside noise)
- multi+ownership, recall@10: `full` vs `vector`: delta +0.044 [-0.061, +0.158] (n=19, inside noise)
- multi+ownership, fullcover@10: `full` vs `vector`: delta +0.158 [-0.053, +0.368] (n=19, inside noise)
- all questions, recall@10: `auto` vs `vector`: delta +0.013 [-0.062, +0.083] (n=40, inside noise)
- all questions, fullcover@10: `auto` vs `vector`: delta +0.050 [-0.100, +0.175] (n=40, inside noise)
- odd questions, recall@10: `auto` vs `vector`: delta -0.033 [-0.108, +0.033] (n=20, inside noise)
- odd questions, fullcover@10: `auto` vs `vector`: delta +0.000 [-0.150, +0.150] (n=20, inside noise)
- even questions, recall@10: `auto` vs `vector`: delta +0.058 [-0.058, +0.175] (n=20, inside noise)
- even questions, fullcover@10: `auto` vs `vector`: delta +0.100 [-0.150, +0.350] (n=20, inside noise)
- multi+ownership, recall@10: `auto` vs `vector`: delta +0.088 [-0.018, +0.184] (n=19, inside noise)
- multi+ownership, fullcover@10: `auto` vs `vector`: delta +0.263 [+0.053, +0.474] (n=19, significant)

## Tools

- `ask` evidence pack, gold answer string present: multi 0.25 (n=12), ownership 0.86 (n=7); mean 721 ms
- `who` (topic = whole question): gold person in top 3 (any) 0.57, all gold people 0.43 (n=7)
- `who` (topic = gold non-person entity): gold person in top 3 (any) 0.86, all gold people 0.86 (n=7)
