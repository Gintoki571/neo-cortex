---
type: Research Note
title: 'System 1 models in knowledge-graph pipelines (GLiNER family, label-set classifiers)'
description: 'What fast non-generative encoders (GLiNER, GLiNER2.5, GLiNER-Relex, GLiREL, GLiNER2.5-Decide) do inside knowledge-graph pipelines, by job (extract, type, resolve, verify, route, escalate), with measured numbers kept apart from opinion.'
resource: https://lyonwj.com/blog/gliner-decide-knowledge-graph-extraction
tags: [extraction, system-1, gliner, relation-extraction, entity-resolution, verification, escalation, agent-memory]
status: stable
generated: { by: claude-haiku-5-5/extraction-agent, at: 2026-10-17T05:40:00Z }
stale_after: 2026-11-17T00:00:00Z
sources:
  - id: decide-blog
    resource: https://lyonwj.com/blog/gliner-decide-knowledge-graph-extraction
    title: 'Checking Knowledge Graph Extraction with GLiNER2.5-Decide (William Lyon, 2026-09-24)'
  - id: jev-blog
    resource: https://lyonwj.com/blog/typesafe-jev-knowledge-graph-extraction
    title: 'Jev (TypeSafe) and knowledge graph extraction (William Lyon, 2026-09-17)'
  - id: relex-arxiv
    resource: https://arxiv.org/html/2605.10108v1
    title: 'GLiNER-Relex: unified NER and relation extraction (arXiv 2605.10108v1, 2026-05-11)'
  - id: neo4j-pipeline
    resource: https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/
    title: 'Neo4j Labs agent memory: how entity extraction works'
  - id: fastino-blog
    resource: https://fastino.ai/blog/gliner2-5-span-free-information-extraction
    title: 'GLiNER2.5 span-free information extraction (Fastino, 2026-08-24)'
  - id: fastino-base-card
    resource: https://huggingface.co/fastino/gliner2.5-base-v1
    title: 'fastino/gliner2.5-base-v1 model card'
  - id: fastino-decide-card
    resource: https://huggingface.co/fastino/GLiNER2.5-Decide
    title: 'fastino/GLiNER2.5-Decide model card'
  - id: falkordb-strategies
    resource: https://docs.falkordb.com/graphrag/strategies
    title: 'FalkorDB GraphRAG SDK: strategies (entity resolution, GLiNER band)'
  - id: decodingai-clean
    resource: https://www.decodingai.com/p/keep-knowledge-graph-clean
    title: 'Keep your knowledge graph clean (Decoding AI)'
  - id: knowledgator-cookbook
    resource: https://docs.knowledgator.com/docs/cookbooks/graphrag-system/index.html
    title: 'Knowledgator GraphRAG system cookbook'
evidence:
  - { file: references/evidence/extraction/system1-lyonwj-gliner-decide.md.txt, sha256: e043ff41984b83f22e51aec142e241474fcbcd0e7386ac17fda8ce02d19923b2, retrieved_at: 2026-10-17T04:34:30Z, method: obscura }
  - { file: references/evidence/extraction/system1-lyonwj-typesafe-jev.md.txt, sha256: d1e4a001c8eab138bfda059804b9b2dd2b80e01d20d8fe5a00d3387e5d674791, retrieved_at: 2026-10-17T04:34:30Z, method: obscura }
  - { file: references/evidence/extraction/system1-gliner-relex-arxiv-2605.10108.md.txt, sha256: a2af626a973b8c4a6084af31f6c8a033e5b1cff5897d0495698e589f8b1a76fc, retrieved_at: 2026-10-17T04:34:30Z, method: obscura }
  - { file: references/evidence/extraction/system1-neo4j-labs-extraction-pipeline.md.txt, sha256: d1bc0420efbfbb864c6562d024d8ce8f4aefec41fab8e8bac34ec0cb569fd808, retrieved_at: 2026-10-17T04:34:30Z, method: obscura }
  - { file: references/evidence/extraction/system1-fastino-gliner25-blog.md.txt, sha256: 1e0f2492e04db1ac76ac6bb23a19aaf66adbaf8856404b947839effb18ddaa55, retrieved_at: 2026-10-17T04:34:30Z, method: obscura }
  - { file: references/evidence/extraction/system1-fastino-gliner25-base-card.md.txt, sha256: ace8ffbc78ad4178c817ea80acd273749f17dd9baafa43e3babefbfcb785c536, retrieved_at: 2026-10-17T04:37:44Z, method: obscura }
  - { file: references/evidence/extraction/system1-fastino-gliner25-decide-card.md.txt, sha256: b7273e7e2e3f75956a2c669f22f2c5d30a1ae514f0fac3325d7b81efa70525da, retrieved_at: 2026-10-17T04:37:44Z, method: obscura }
  - { file: references/evidence/extraction/system1-falkordb-graphrag-strategies.md.txt, sha256: 9954469d575fae73871f4358afef95b98571fceb6cb58770fa9e1680a85ce9d4, retrieved_at: 2026-10-17T04:34:30Z, method: obscura }
  - { file: references/evidence/extraction/system1-decodingai-keep-kg-clean.md.txt, sha256: 4c8d0a39adf6d586abb169ab21478bd00f56d298510afb65bb6b3786c0ead032, retrieved_at: 2026-10-17T04:36:43Z, method: obscura }
  - { file: references/evidence/extraction/system1-knowledgator-graphrag-cookbook.md.txt, sha256: 14bfa6aed163d0a73a615648b5b75490be356da9e1c079ff07a2cf5c3b01cc27, retrieved_at: 2026-10-17T04:37:05Z, method: obscura }
---

# System 1 models in knowledge-graph pipelines

## Summary

- Fast encoders (GLiNER2.5 and relatives) are good at proposing candidates and at checking candidates someone else proposed. They are weak at finding relations across a document, at deciding whether two mentions are the same thing, and at reading hedges without a dedicated label.
- The best-measured pattern is: extract locally and exhaustively, verify each candidate edge with a label-set classifier, and keep the verdict as data. On one 10-document corpus this moved F1 from 0.330 to 0.396 with no recall loss.
- Sending uncertain cases to a bigger LLM did not help on that corpus. What helped is an explicit "not stated" or "ambiguous" outcome that a reviewer sees.
- Every number here comes from one author or one vendor on a small corpus. None was re-run in this pass, so treat absolute values as directional. The adoption plan is in [/extraction/system1-adoption.md](/extraction/system1-adoption.md).

Labels: **Measured** means a number from a stated test. **Opinion** means a design claim or a view without its own test. Quotes are verbatim from the evidence files named beside them.

## Entity extraction and typing

**Measured**

- Raw GLiNER2.5 output on a 10-document synthetic corpus (47 gold triples, 214 mentions, 170 candidate edges): [^decide-blog]
  > "Scored against the gold triples, the raw extraction gets precision 0.279, recall 0.404, F1 0.330."
  (`references/evidence/extraction/system1-lyonwj-gliner-decide.md.txt`)
- Typing the bare surface string instead of the whole sentence agreed with GLiNER's type on 145 of 214 mentions, up from 72: [^decide-blog]
  > "Given only the surface string, it types the mention: across all 214 mentions, agreement with GLiNER's type goes from 72 to 145."

**Opinion**

- Use precise, non-overlapping labels; vague labels make generic entities. [^knowledgator-cookbook]
  > "Use precise, non-overlapping entity types like software_library and api_function rather than vague labels like thing or code."

## Relation extraction

**Measured**

- Relation recall falls with input length. Neo4j Labs states the window rule, and the Fastino base card gives the same figure: [^neo4j-pipeline] [^fastino-base-card]
  > "Relation recall drops sharply past roughly 400 words, so the extractor windows any input longer than `max_words` (default 384"
  > "relation recall still degrades past roughly 400 words"
  Both sources give the same figure, but the Neo4j page may restate the vendor card, so count this as one source.
- A relation whose endpoints fall in different windows is lost: [^neo4j-pipeline]
  > "A relation whose endpoints fall in different windows cannot be decoded, and a windowed extraction never reports `feasible=False`."
- Neo4j's CPU run on the POLE+O gold set with `gliner2.5-base-v1`: entity F1 0.80, relation F1 0.37 lenient and 0.27 strict, about 1.6 docs/s. [^neo4j-pipeline]
  > "| `fastino/gliner2.5-base-v1` | 0.80 | 0.37 / 0.27 | ~1.6 docs/s |"
- Zero-shot end-to-end Micro-F1 (GLiNER-Relex paper, Table 2, entities predicted from raw text). GLiNER-Relex 40.4 / 31.3 / 12.5 / 18.1 on CoNLL04 / DocRED / FewRel / CrossRE, against GPT-5-mini 42.4 / 18.6 / 15.0 / 12.4. [^relex-arxiv]
  > "| GLiNER-Relex (ours) | predicted | 40.4 | 31.3 | 12.5 | 18.1 | 25.6 |"
  The paper's text and its table disagree on the GLiNER2 row. The table gives 32.9 / 11.7 / 20.8 / 6.0 (average 17.8), and the text gives 34.1 / 12.4 / 16.8 / 4.9 (average 17.1). The GLiNER-Relex row agrees in both. The GLiNER-Relex input cap is 2048 words.
- Speed on 50 FineWeb documents (mean 288 words, one L4 GPU, batch 1): [^relex-arxiv]
  > "GLiNER-Relex achieved a mean per-document latency of 0.9 s (throughput 1.11 docs/sec), while GPT-5-mini averaged 64 s per document"
- GLiREL, given gold entities, is narrow: 24.0 on FewRel (sentence level) and 4.5 on CoNLL04. [^relex-arxiv]
  > "| GLiREL† | gold | 4.5 | 2.4 | 24.0 | 1.4 | 8.1 |"
  The text gives DocRED 2.2 and FewRel 23.9. The table is used here.
- Neo-Cortex today (per-sentence windows plus deterministic patterns), from its own graded eval: [/architecture/build-status.md](/architecture/build-status.md)
  > "Final graded quality (`eval/graph_quality.md`): precision 0.880, recall 0.825."

**Opinion**

- Independent decoding gives inconsistent graphs; joint decoding enforces endpoint types. [^fastino-blog]
  > "When entities and relations are scored independently, the combined output is frequently inconsistent."
- Vendor advice: treat relation F1 as a floor. [^fastino-base-card]
  > "Treat relation F1 as a floor to improve with per-relation thresholds."

## Entity resolution (naming is not identity)

**Measured**

- Same-entity judgments with Decide (names only, yes/no, 34 true merges and 11 false merges): 29 of 34 true merges accepted, but also 6 of 11 false merges. [^decide-blog]
  > "| names only, yes/no | 29/34 | 6/11 | 4/6 |"
- Decide's own conclusion: [^decide-blog]
  > "Decide can say what a mention is. It cannot say whether two mentions are the same thing"
- Widening blocking with a second-opinion type (69 clones) took B-cubed recall on the 13 gold alias groups from 0.8972 to 1.0000 at precision 1.0000, with the resolver unchanged. The same widening merged the brand `Halcyon` with the product `Halcyon Buds`. [^decide-blog]
  > "Every step is locally reasonable, and the merge is wrong."

**Opinion**

- Naming (normalise, set a canonical name, keep aliases) and identity (is this the same thing?) are separate steps. [^decodingai-clean]
  > "Similar names are not strong enough evidence that 2 entities are identical."
- Candidate generation matters more than scoring in the Jev runs. [^jev-blog]
  > "the wins came from candidate generation rather than from better scoring"
- FalkorDB's SDK uses an embedding threshold pair. At or above `hard_threshold` the pair merges with no LLM call. Between the two thresholds, an LLM answers yes or no. [^falkordb-strategies]
  > "`similarity >= hard_threshold`: merged immediately, no LLM call"

## Edge verification (the Decide gate)

**Measured**

- Each candidate edge gets two checks over its window (the text between its endpoints): a modality question and a relation-agreement question. [^decide-blog]
  > "Each check alone helps a little. Together they close most of the distance to the hosted gate, at no recall cost"
  > "| plus both: the Decide gate | 49 / 19 | **0.388** | 0.404 | **0.396** |"
  (columns: system, predicted/matched, precision, recall, F1). The hosted Jev gate reaches 0.404 on the same corpus.
- Sensitivity to the task name alone moves F1 between 0.383 and 0.404. The author calls this the error bar on the gate. [^decide-blog]
  > "A spread of 0.383 to 0.404 F1, from a word that carries no information the labels don't, is the honest error bar on the gate, not a knob to turn."
- Label wording: short concept labels (fact, possibility, denial, forecast) caught 11 of 11 traps and kept 5 of 5 controls. A yes/no reword caught 9 of 11 and kept 0 of 5. [^decide-blog]
  > "| Jev's reworded question, as yes/no | 9/11 | 0/5 | 0.56 | 0.24 |"
- Of 170 edge windows on the same corpus, Decide read 123 as fact and the rest as forecast, not stated, possibility or denial. [^decide-blog]
  > "Decide read 123 windows as fact (25 forecast, 12 not stated, 6 possibility, 4 denial)"
- Cost on CPU: 340 texts in 33.7 s (72.1 ms per text), model load 5.7 s after a 1.9 GB first download. [^decide-blog]
  > "5.7 s, after a 1.9 GB first download"
- The Decide model is a 340M English classifier that takes the label set at call time and returns a probability per label. [^fastino-decide-card]
  > "The 340M English classification model in the GLiNER2.5 family."

**Opinion**

- Keep the verdicts as data, so the gate becomes a filter. [^jev-blog]
  > "Store the raw judgments."

## Retrieval and routing

**Measured**

- Intent and priority on eight support threads: GLiNER was near chance on intent and at chance on priority. This is a very small test. [^jev-blog]
  > "GLiNER classifies the intent of the repo's eight customer-support threads near chance and their priority at chance"
- Neo-Cortex's own eval shows the graph channel ties text retrieval on document finding, with the confidence interval including zero. [/architecture/build-status.md](/architecture/build-status.md)
  > "delta -0.002 [-0.031, +0.031] (n=80, inside noise)"

**Opinion**

- A band of extractor scores just below threshold can go to a later step as "Unknown" instead of being dropped. [^falkordb-strategies]
  > are kept as "Unknown" for the step-2 LLM to re-type or

## System 1 and System 2 escalation

**Measured** (Jev post; the escalation model was Claude Haiku; 31 of 170 edges sent)

- Escalation did not help. Recall never moved and precision fell as more edges were escalated. [^jev-blog]
  > "| cascade: uncertain edges to Haiku | 0.396 | 0.404 | 0.400 |"
  > "| Haiku on every edge | 0.373 | 0.404 | 0.388 |"
  > "Recall never moves; precision falls as escalation rises."
- On six gold-same pairs (for example `Northwind` and `Northwind Logistics Inc.`), Haiku got none right: it called two different and four unsure. [^jev-blog]
  > "Zero of six."
- A confident answer can come back wrong. Three denial traps scored 0.66, 0.71 and 0.74 on a question that did not mean what the author intended. [^jev-blog]
  > "The three come back at 0.66, 0.71 and 0.74, a confident answer to the reading I did not mean"

**Opinion**

- Low confidence means the source is ambiguous, and a bigger model does not resolve that. The review step is for a person. [^jev-blog]
  > "a bigger model doesn't resolve ambiguity that's in the source."
  > "The review level exists so that a person with a reference to hand can look, and a larger language model is not that person."

## Agent-written graphs

**Opinion** (no measured result in the sources)

- Extract locally and exhaustively, judge selectively, and keep the judgments as data. [^jev-blog]
  > "Extract locally and exhaustively, judge selectively, keep the judgments as data."
- In Neo-Cortex, relations passed to `remember(relations=)` skip GLiNER and are written through the `_edge` helper (`src/neo_cortex/AGENTS.md`). `relate()` is the other agent-direct write. The extraction-side checks (the negation and former-state lookbehinds in `extract.py` `_relations`) are not documented for either path. See the adoption plan.

## Open questions

- Unsaved or snippet-only claims, not used as fact: a Reddit self-benchmark (GLiNER relation F1 0.520 against about 0.315 for a GPT-4o pipeline, r/LocalLLaMA, 2026-03-23, as recorded in the research notes); a Reddit snippet that noisy entities "amplify the noise" in a graph (page did not load); Cognee running GLiNER by default (GitHub and X snippets); a reported NER fine-tuning lift from 87.0 to 93.4 F1 (Hugging Face case study, 2024-12-03, different domain).
- Pointers not read in full: ReLiK (arXiv 2408.00103), LazyGraphRAG and Query-Centric Graph RAG (arXiv 2509.21237), KGGen (arXiv 2502.09956), GLinker (`knowledgator/gliner-linker-large-v1.0`).
- Source conflicts, recorded and not resolved: the GLiNER-Relex GLiNER2 row (table against text) and the GLiREL DocRED value (table 2.4, text 2.2). A separate research draft gave the Decide gate as 0.404, which is the hosted Jev gate; the saved source gives 0.396.
- Not tested: whether the GLiNER2.5 base classification head reproduces the Decide gate, and whether the gate holds on the Neo-Cortex synthetic corpus (`data/synthetic/`). All Decide numbers come from the separate Decide model.
- The Neo4j page: a research draft reported a 503 on a later direct fetch. The saved copy is the full page and is used here, not re-fetched.
