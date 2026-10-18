# Ideas Neo-Cortex builds on

For each outside idea: the source, what we took, where it lives in the code, what we left out, and the measured result. Code was read from `src/neo_cortex/`. Numbers are copied from `eval/`. Planned but unbuilt work is marked **not built**.

| # | Idea | Source | What we built | Status |
|---|---|---|---|---|
| 1 | Cached typed judgments | [realZachi/pg-jev](https://github.com/realZachi/pg-jev) | Judgment cache + assertion gate on every extracted relation (fact / possibility / denial / plan; `modality` and `p_fact` stored on the edge) | Built: cached decisions + assertion gating |
| 2 | Held-out acceptance for tuning | [google-research/rrsi](https://github.com/google-research/rrsi) | `eval/tune.py`, odd/even split | Built. Its weights were **rejected** |
| 3 | Offline consolidation | [zhengkid/Dream-RSI](https://github.com/zhengkid/Dream-RSI) | Deterministic `neo dream` | Built, adapted |
| 4 | Personalized PageRank | HippoRAG, HippoRAG 2 (arXiv 2405.14831, 2502.14802) | Graph channel `ppr()` | Built, in numpy |
| 5 | Small encoders, no LLM | [fastino/gliner2.5-base-v1](https://huggingface.co/fastino/gliner2.5-base-v1) | GLiNER for extraction, typing, judging, intent | Built. Decide checkpoint **not built** |
| 6 | Text-only embeddings | [google/embeddinggemma-2](https://huggingface.co/google/embeddinggemma-2) | Text-only loader | Built. No eval number |
| 7 | Lexical search and fusion | bm25s; reciprocal rank fusion | BM25 channel, weighted RRF | Built |
| 8 | Office and PDF to Markdown | [firecrawl/anydoc](https://github.com/firecrawl/anydoc) | Non-text ingest | Built. HTML unsupported |
| 9 | Bundle and agent contracts | [OKF](https://github.com/GoogleCloudPlatform/open-knowledge-format); DOX AGENTS.md | `knowledge/` bundle, AGENTS.md hierarchy | Built (docs only) |

Links checked with obscura on 2026-10-18: HippoRAG [2405.14831](https://arxiv.org/abs/2405.14831), HippoRAG 2 [2502.14802](https://arxiv.org/abs/2502.14802), BM25S [2407.03618](https://arxiv.org/abs/2407.03618), RRSI [2609.24972](https://arxiv.org/abs/2609.24972) ([project page](https://regularized-rsi.com/)), GLiNER2 [2507.18546](https://arxiv.org/abs/2507.18546), Dream-RSI [paper PDF](https://github.com/zhengkid/Dream-RSI/blob/main/papers/Dream-RSI.pdf) ([dream-rsi.com](https://www.dream-rsi.com); its repo says the arXiv posting is in progress). pg-jev ([pgjev.com](https://pgjev.com)) has no paper; its model card points to the GLiNER2 paper. RRF: Cormack, Clarke and Buettcher, SIGIR 2009 (not re-fetched).

## 1. pg-jev

- **Took:** judgments stored as data, with probabilities, cached by content; plus assertion gating on every extracted relation (fact / possibility / denial / plan on its source sentence; `modality` and `p_fact` stored on the edge; current-state tools and the graph walk read facts only; agent-written edges are facts).
- **Code:** `resolve.py` `judge()` caches the GLiNER choice distribution as a `Judgment` node, keyed by a hash of question, text and labels. `resolve_entity()` calls it only for borderline matches (similarity 0.85 to 0.92). `extract.py` `_gate` classifies each relation on its sentence: default gate = base GLiNER2.5 + a negation-cue rule.
- **Not taken:** the Postgres extension. GLiNER2.5-Decide (`fastino/GLiNER2.5-Decide`, Apache-2.0) scores 20/25 on the trap probe too — same as model + rule — but is a second ~1.9 GB model about 6x slower, so it was not adopted.
- **Known gap:** `resolve.py` line 148 lets a judge answer of "same" (>= 0.5) create a merge. The docstring and `src/neo_cortex/AGENTS.md` say the judge may only veto.
- **Result:** trap probe of 25 hand-labelled sentences: model only 17/25, model + rule 20/25. Synthetic fact-only relations: precision 0.880 -> 0.903, recall 0.825 -> 0.812 (neutral F1 0.852 -> 0.855). The published gain (edge F1 0.330 -> 0.396 on one author's 10-doc corpus with Decide) did not reproduce here.

## 2. RRSI

- **Took:** the acceptance rule, not the harness search. Search on odd questions, accept only on even questions, and only if the paired-bootstrap 95% CI lower bound is above 0 and latency is within 20%.
- **Code:** `eval/tune.py` `main()` tries 36 weight combinations (bm25 x graph x temporal) by patching `channel_weights`. `ledger()` writes a `TuneRun` node per trial.
- **Not taken:** LLM-driven harness edits and the regularizer. The product has no LLM.
- **Result:** `eval/tune_clean.json` picked bm25 x2, graph x0.5, temporal x2. Odd-split score 0.752 against 0.648 for defaults, but even-split delta -0.019, CI [-0.075, +0.038]: `accepted: false`. `eval/tune_distract.json` gave even delta +0.038, CI [0.000, +0.094]. The lower bound is not above 0, so also rejected. The product ships the default weights.

## 3. Dream-RSI

- **Took:** an offline, deterministic, idempotent consolidation pass, with a run log. The adaptation follows `knowledge/architecture/inspiration-dream-rsi.md`.
- **Code:** `dream.py` `dream()` runs `_plan_merge` (cosine >= 0.92, never across a differing number or negation), `_plan_promote` (episodic cluster seen in >= 3 sessions becomes semantic), `_plan_decay` (confidence x0.9 per idle 30 days, floor 0.1; preferences and decisions exempt) and `_plan_conflicts` (flags only). Each run writes a `DreamRun` node. Surfaces: `neo dream` (`cli.py`) and the `dream` MCP tool.
- **Not taken:** the replay simulator and policy search. The Dream-RSI repo has no released code. LLM reflection is not taken. **Hypothesis-edge promotion is not built.**
- **Result:** no eval number. `tests/test_dream.py` covers merge, promote, decay, conflicts, idempotence and dry runs.

## 4. HippoRAG

- **Took:** Personalized PageRank from query-linked entities over an entity-and-chunk graph, so chunks two or three hops away gain mass.
- **Code:** `retrieve/channels.py` `ppr()` (restart 0.5, at most 3 hops, 500 nodes, numpy). `graph()` drops weak links unless an anchor supports them, and returns nothing when seed strength is below `SEED_FLOOR` (0.2). `retrieve/__init__.py` `recall()` scales the graph's RRF weight by that strength.
- **Not taken:** LLM-based information extraction.
- **Result:** the graph adds nothing on documents. `eval/results.md` gives recall@10 0.74 for vector+bm25+graph against 0.75 for vector+bm25, and fullcover 0.55 against 0.59. On impact questions, `eval/answers.md` gives all-keys 0.80 against a 0.20 baseline (delta +0.60 [+0.30, +0.90]).

## 5. GLiNER2.5 as System 1

- **Took:** a small non-generative encoder as extractor, typer, classifier and judge. No LLM SDK is imported under `src/neo_cortex/`. fp16 loading is opt-in (`NEO_GLINER_FP16=1`): on the GTX 1660 Ti it halves peak GPU memory (1098 -> 589 MB) but is ~2.4x slower per call.
- **Code:** `extract.py` `extract_batch()` (entities, then per-sentence relations plus patterns) and `_softmax_batch()` (labelled distributions for `worth_keeping_batch` and `classify_memory_batch`). `_gate` classifies each relation on its source sentence (fact / possibility / denial / plan; `modality` and `p_fact` stored on the edge). `session_mem.py` scores and types candidates. `resolve.py` `judge()`. `retrieve/query.py` `parse_query()`. `models.py` `gliner()` loads the checkpoint. `joint.py` implements `NEO_EXTRACT` paths `split` (default), `combined` and `joint` (JointIE greedy decoding).
- **Compared and not adopted:** GLiNER2.5-Decide (`fastino/GLiNER2.5-Decide`, Apache-2.0) matches model + rule at 20/25 on the trap probe but is a second ~1.9 GB model ~6x slower. JointIE (`joint`) and the combined schema (`combined`) were measured behind `NEO_EXTRACT`: precision 0.719 and 0.774 vs 0.880 for split, and slower on real documents (222 s and 140 s vs 92 s synthetic ingest), so the default stays split. The edge-verification gate from lyonwj (F1 0.330 to 0.396 on a 10-document corpus) did not reproduce here.
- **Result:** `eval/graph_quality.md` gives relation precision 0.880 (66/75) and recall 0.825. CAUSED_BY recall is 0 of 5. With the fact-only gate, synthetic relations are precision 0.903, recall 0.812 (neutral F1 0.855). On the repo's own 69 docs GLiNER produced only 12 relation edges (`eval/real_check.md`), so agents also write relations directly.

## 6. EmbeddingGemma, text-only

- **Took:** the text tower only.
- **Code:** `models.py` `_embedder()` sets `vision_config` and `audio_config` to `None` and loads float32. `embed_docs()` and `embed_query()` use it. `embed_images()` exists, but no ingest path calls it, and `write.py` skips images (`_SKIP_EXT`).
- **Result:** no eval number for memory or quality beyond retrieval. Licence is ambiguous (`knowledge/models/embeddinggemma.md`).

## 7. bm25s and RRF

- **Took:** a BM25 lexical channel and weighted reciprocal rank fusion.
- **Code:** `retrieve/channels.py` `bm25()` and `_bm25_index()` (bm25s, English stemmer, identifiers split on `_ - . / :`). `retrieve/fuse.py` `rrf()` (k=60) and `channel_weights()`. `retrieve/__init__.py` `recall()` fuses.
- **Not taken:** learned fusion, and the tuned weights (rejected in idea 2). The BM25 index is fully rebuilt when the corpus changes, a stated shortcut.
- **Result:** `eval/results.md` gives recall@10 0.71 for bm25, 0.73 for vector and 0.75 for vector+bm25. Mean latency is 6 ms for bm25 and 40 ms for vector+bm25.

## 8. anydoc

- **Took:** anydoc for any file that is not Markdown, text or Python.
- **Code:** `write.py` `_load()` reads `.md`, `.markdown` and `.txt` directly and chunks `.py` by definition. Everything else goes to `anydoc.to_markdown()`. `ingest_path()` counts `UnsupportedError` as unsupported, other failures as errors, and continues. Dependency: `firecrawl-anydoc` in `pyproject.toml`, unpinned.
- **Not taken:** anydoc's hosted OCR. A scanned PDF exits 3 and is counted as an error.
- **Result:** no retrieval number. `knowledge/extraction/anydoc-test-results.md` (anydoc 0.2.4) shows that text PDF, docx and xlsx convert, and a scanned PDF is refused. `tests/test_anydoc_ingest.py` runs the real write path: docx, xlsx, pptx, pdf, rtf and csv become one document each; html, json and eml count as unsupported; scanned and encrypted PDFs count as errors; a directory batch survives every bad file. HTML is converted by a built-in standard-library converter because anydoc has no HTML reader.

## 9. OKF and DOX

- **Took:** the OKF v0.2 layout for `knowledge/`: an index, a log, and per-page frontmatter (`type`, `title`, `description`, `resource`, `status`, `stale_after`, `sources`). The DOX AGENTS.md hierarchy: the root file, plus local contracts for `knowledge/`, `src/neo_cortex/` and `demo/`.
- **Code:** none. This is process. The bundle is checked by `knowledge/references/evidence/okf/validate_okf.py`.
- **Result:** none measured.
