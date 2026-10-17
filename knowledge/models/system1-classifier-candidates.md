---
type: Comparison
title: System 1 classifier candidates (GLiNER2.5 vs NLI cross-encoder vs tiny LLM)
description: Side-by-side of three local options for a small, fast "System 1" classifier that returns probabilities for graph micro-decisions, built only from retrieved model cards, API metadata and papers.
resource: https://huggingface.co/fastino/GLiNER2.5-Decide
tags: [model, classifier, system-1, comparison, gliner2, nli, cross-encoder, llm]
status: draft
generated: { by: claude-haiku-5-5/models-agent, at: 2026-10-15T19:30:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: gliner25-decide-card
    resource: https://huggingface.co/fastino/GLiNER2.5-Decide
    title: 'fastino/GLiNER2.5-Decide model card'
    last_modified: 2026-10-08T20:47:53Z
  - id: gliner2-paper
    resource: https://arxiv.org/abs/2507.18546
    title: 'GLiNER2 paper (arXiv 2507.18546, v1)'
    last_modified: 2026-10-15T19:24:24Z
  - id: gliner2-github-readme
    resource: https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md
    title: 'fastino-ai/GLiNER2 README'
    last_modified: 2026-10-09T17:53:44Z
  - id: nli-deberta-v3-base-card
    resource: https://huggingface.co/cross-encoder/nli-deberta-v3-base
    title: 'cross-encoder/nli-deberta-v3-base model card'
    last_modified: 2025-04-11T09:56:48Z
  - id: nli-deberta-v3-small-api
    resource: https://huggingface.co/api/models/cross-encoder/nli-deberta-v3-small?blobs=true
    title: 'HF API metadata, cross-encoder/nli-deberta-v3-small'
    last_modified: 2025-04-15T08:18:25Z
  - id: zeroshot-v2-card
    resource: https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0
    title: 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0 model card'
    last_modified: 2024-04-11T13:42:07Z
  - id: qwen25-05b-card
    resource: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
    title: 'Qwen/Qwen2.5-0.5B-Instruct model card'
    last_modified: 2024-09-25T12:32:56Z
  - id: awesome-jev
    resource: https://github.com/AbdelStark/awesome-typesafe-jev
    title: 'Awesome Jev (third-party list, README)'
  - id: typesafe-blog
    resource: https://typesafe.ai/blog/introducing-system-one-models-and-jev
    title: 'Introducing System One Models & Jev (TypeSafe AI blog)'
    last_modified: 2026-09-15T00:00:00Z
evidence:
  - { name: card_fastino_GLiNER2.5-Decide.txt, url: "https://huggingface.co/fastino/GLiNER2.5-Decide", sha256: 09a9705ee8c30392bb5a82ac503c01b889ff7e957a4c96bf7249f05acde709a3, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_GLiNER2.5-Decide.json, url: "https://huggingface.co/api/models/fastino/GLiNER2.5-Decide", sha256: 44c2ef4c7487f312c1dfd15f5ee847be65e3de8ce1349a607193a8b28e7d51d9, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_GLiNER2.5-multi-Decide.json, url: "https://huggingface.co/api/models/fastino/GLiNER2.5-multi-Decide", sha256: 270d129ca25200cfdff231130c7e99578286a5ac8b919e1b7cc1cf8d7d0852af, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: arxiv_2507.18546.xml, url: "https://arxiv.org/abs/2507.18546", sha256: 3ca195851e93df137fde4a9409d8966d5b96e77f591c74705b6d7b9daf52e1b6, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2_arxiv_html.txt, url: "https://arxiv.org/html/2507.18546", url_basis: inferred, sha256: f320e9717473fea9ad0645cb1533c2e8bf6d2de9a3e3bedd59dafaae57711d1f, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2_readme.txt, url: "https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md", sha256: 78f50ae3c773afe07941adea199311d6527a6001111b660f4110223f938feeae, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: card_cross-encoder_nli-deberta-v3-base.txt, url: "https://huggingface.co/cross-encoder/nli-deberta-v3-base", sha256: b6a6dd82d5fee7036e3b815ce1d28458df294d8525fc234fb7e7277b6b79d878, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_cross-encoder_nli-deberta-v3-small.json, url: "https://huggingface.co/api/models/cross-encoder/nli-deberta-v3-small?blobs=true", sha256: 7bb25b5dbd1f49391e196a9158d798f043a776a54f3b566283d620d24370b0e4, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_cross-encoder_nli-deberta-v3-base.json, url: "https://huggingface.co/api/models/cross-encoder/nli-deberta-v3-base", sha256: 3f8d25411fcc82913ba1669a3daaabc0ec575fba919947f2e72e541df61ce345, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: card_MoritzLaurer_deberta-v3-base-zeroshot-v2.0.txt, url: "https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0", sha256: bd974d885c91d90f96183e86803e80b080ad365cb65307f2ebd9169d2646f08f, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_MoritzLaurer_deberta-v3-base-zeroshot-v2.0.json, url: "https://huggingface.co/api/models/MoritzLaurer/deberta-v3-base-zeroshot-v2.0", sha256: ea573ad7a2fb9c2a716c49289be28b1d75f1d54e195de2e9d90bed85f5c01b76, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: card_Qwen_Qwen2.5-0.5B-Instruct.txt, url: "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct", sha256: b19c806a904db6dc878a0462e70b551f6b7ac78dfbb88c2eb966ca2b9109ae15, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_Qwen_Qwen2.5-0.5B-Instruct.json, url: "https://huggingface.co/api/models/Qwen/Qwen2.5-0.5B-Instruct", sha256: f0c42a745c1b55f2d01098f455b4d40badf2f40dab38378e9a86f17ef1857f2a, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: jev_typesafe_blog.txt, url: "https://typesafe.ai/blog/introducing-system-one-models-and-jev", sha256: 6fbda0a3d2d947811a45415fabe153e7bef65b2a28d243eb9d41de502b059f65, retrieved_at: 2026-10-15T19:28:00Z, method: command, redistributed: false }
  - { name: jev_awesome_readme.txt, url: "https://github.com/AbdelStark/awesome-typesafe-jev", sha256: 8a6b6b564d7787e3e5a991d9b0fa695c0249ddc65839b9cbdb14d5921e4e4ae0, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
---

# Question

Which small local model should act as the "System 1" classifier for graph micro-decisions (assertion gating, relation selection, entity-resolution yes/no, query routing, grounding checks), returning a label and a probability per decision?

Jev, the hosted candidate the brief mentions, is covered in [jev-typesafe-claim-check](/models/jev-typesafe-claim-check.md). It is not local, so it is out of the table.

# Comparison

Only facts retrieved in this run are in the table. "not retrieved" means I looked and found nothing usable.

| Criterion | A. GLiNER2.5 classification (Decide / classify_text) | B. Cross-encoder / NLI (zero-shot) | C. Tiny LLM (Qwen2.5-0.5B-Instruct) |
|---|---|---|---|
| Concrete candidate | `fastino/GLiNER2.5-Decide` (English); `fastino/GLiNER2.5-multi-Decide` (multilingual); base `gliner2.5-base-v1` also has `classify_text` | `cross-encoder/nli-deberta-v3-small` / `-base`; `MoritzLaurer/deberta-v3-base-zeroshot-v2.0` | `Qwen/Qwen2.5-0.5B-Instruct` |
| Size (params, metadata) | 486,444,053 (Decide, card says 340M); 287,355,159 (multi-Decide) | 141,897,731 (nli-small); 184,424,963 (nli-base); 184,423,682 (zeroshot-v2.0) | 494,032,768 |
| Weight file | Decide `model.safetensors` 1,945,828,140 bytes; multi-Decide 1,149,461,028 bytes | nli-small `model.safetensors` 567,605,820 bytes, ONNX int8 variants about 172 MB; nli-base `model.safetensors` 737,726,552 bytes; zeroshot-v2.0 368,871,908 bytes | `model.safetensors` 988,097,824 bytes |
| Licence | Apache-2.0 (card and tag) | nli models Apache-2.0; zeroshot-v2.0 MIT | Apache-2.0 |
| Output shape | Label(s) with probability; `classify_text` default `threshold: float = 0.5`; per-task `probabilities` on Classifier | Three scores per pair (contradiction / entailment / neutral); zero-shot via hypothesis, `multi_label` flag | Free text; probability only if you read answer-token logits |
| Multi-label / constraints | Yes; multi-label by threshold; `Classifier` enforces cross-task constraints and returns `feasible` | Multi-label by independent scoring; no cross-label constraints | None built in |
| Context length | Encoder window (`max_len=4096` on the 2.5 base card) | 512 tokens for zeroshot-v2.0 ("The other models can process up to 512.") | 32,768 tokens |
| Accuracy evidence | Decide card: 60.2% exact-match average on `fast-decisions` (17 domains, 300 examples each, vendor-run). | nli-base card: "Accuracy on SNLI-test dataset: 92.38", "Accuracy on MNLI mismatched set: 90.04". zeroshot-v2.0 card: f1_macro over 28 tasks; "all datasets mean" row gives 0.497 for bart-large-mnli and 0.619 for the -c variant (vendor table). | not retrieved |
| Latency evidence | Paper (v1 span model, CPU): "( 6.8× slower with 20 labels)" for DeBERTa per-label scoring. No number for 2.5 retrieved. | Per-label forward pass: the paper says DeBERTa zero-shot "performs a separate forward pass for each label". No ms figure retrieved. | not retrieved |
| CPU suitability | Card: "Runs on: CPU or GPU, through `gliner2`". | ONNX int8 variants exist for nli-small and nli-base (file names only). | Not retrieved; 0.49B params, bf16 safetensors. |
| Where it fits the brief | Single forward pass for many labels; probabilities per label; can return several answers from one schema. | Strong, well-known NLI baseline for yes/no judgments ("entailment" vs "contradiction"). | Only if output is parsed and validated; no native probabilities. |

# Notes per candidate

## A. GLiNER2.5 classification

- Quote from the Decide card: "Pass any label set at call time: intent, routing, sentiment, priority, policy, and multi-label tags, in a single forward pass. No prompt template. No generated tokens."[^gliner25-decide-card]
- The paper's efficiency claim is for v1 (span), not 2.5: "GLiNER2 processes all labels simultaneously in a single forward pass, maintaining consistent performance regardless of label..." (text cut off in the source extract).[^gliner2-paper]
- The Decide card says it is a specialist that "does not reason, explain, or answer open questions", which matters for grounding checks that need reasoning.[^gliner25-decide-card]
- Yes/no questions are supported in the classify API, so an assertion or entity-resolution yes/no can use the same call; the Decide card says it "also answers a question about a passage".[^gliner25-decide-card]
- Known gaps: the Decide card's parameter count (340M) and metadata (486M) disagree; "JevK5" appears as a row on its benchmark and is not identified.

## B. Cross-encoder / NLI

- The nli-base card: "For a given sentence pair, it will output three scores corresponding to the labels: contradiction, entailment, neutral."[^nli-deberta-v3-base-card]
- The zero-shot card: "These models can do one universal classification task: determine whether a hypothesis is "true" or "not true" given a text".[^zeroshot-v2-card]
- The zero-shot card lists its context limit: "The `bge-m3` models can process up to 8192 tokens. The other models can process up to 512."[^zeroshot-v2-card]
- Licensing: nli models are Apache-2.0 (API tags `license:apache-2.0`); zeroshot-v2.0 is MIT, but its training data licences vary: "The licenses of the training data vary depending on the model".[^zeroshot-v2-card]
- The nli-small API lists an ONNX int8 build (`onnx/model_qint8_avx512_vnni.onnx`), which is the closest thing to a CPU-optimised artefact among the candidates. Its speed was not measured.[^nli-deberta-v3-small-api]

## C. Tiny LLM

- Qwen card: "Number of Parameters: 0.49B" and "Context Length: Full 32,768 tokens and generation 8192 tokens".[^qwen25-05b-card]
- A decision from an LLM is text. TypeSafe's blog argues this is a problem for software: "Strings are flexible and can be anything: chat responses, code, hallucinations, refusals, or even type-safe structured values. To be used by software, responses need to be parsed + validated."[^typesafe-blog] This is a vendor opinion, but it describes the design trade-off.
- Probabilities from an LLM: the awesome-jev list mentions a local backend that "reads answer-token probabilities without generating text, and its calibration is caller-configured rather than established for every task".[^awesome-jev] That source is third-party, not a measurement of Qwen2.5-0.5B.
- No accuracy or latency number for Qwen2.5-0.5B on classification was retrieved. This row stays "not retrieved" on purpose.

# Recommendation (provisional)

- For a fast, local, many-label yes/no or label decision with probabilities, **A (GLiNER2.5 Decide or base classify_text)** has the most direct match in retrieved sources. Its evidence is still the vendor's.
- **B (NLI cross-encoder)** is the strongest independent baseline. It needs one pass per label, so cost grows with label count, and it has a 512-token limit on zeroshot-v2.0.
- **C (tiny LLM)** is the weakest fit here because its output is text. Use it only with constrained decoding or logit reads, and measure before use.
- None of these was benchmarked on this project's graph data. The recommendation is a hypothesis to test, not a finding.

# Open questions

- Latency and memory for GLiNER2.5-Decide and nli-deberta-v3-small on this machine (not measured; no weights were downloaded).
- An accuracy number for each candidate on a task like assertion gating or entity resolution. None retrieved.
- Whether GLiNER2.5-base's `classify_text` matches the Decide model on the same labels.
- Whether any credible independent benchmark exists for GLiNER2.5-Decide.

# Related

- [jev-typesafe-claim-check](/models/jev-typesafe-claim-check.md)
- [gliner2-5-base](/models/gliner2-5-base.md)
- [gliner2-family-and-paper](/models/gliner2-family-and-paper.md)
- [embeddinggemma](/models/embeddinggemma.md)
- [index](/models/index.md)

[^gliner25-decide-card]: fastino/GLiNER2.5-Decide card, https://huggingface.co/fastino/GLiNER2.5-Decide. Evidence [card_fastino_GLiNER2.5-Decide.txt](https://huggingface.co/fastino/GLiNER2.5-Decide)
[^gliner2-paper]: arXiv 2507.18546 HTML, https://arxiv.org/html/2507.18546. Evidence [gliner2_arxiv_html.txt](https://arxiv.org/html/2507.18546)
[^nli-deberta-v3-base-card]: cross-encoder/nli-deberta-v3-base card, https://huggingface.co/cross-encoder/nli-deberta-v3-base. Evidence [card_cross-encoder_nli-deberta-v3-base.txt](https://huggingface.co/cross-encoder/nli-deberta-v3-base)
[^nli-deberta-v3-small-api]: HF API, https://huggingface.co/api/models/cross-encoder/nli-deberta-v3-small?blobs=true. Evidence [api_cross-encoder_nli-deberta-v3-small.json](https://huggingface.co/api/models/cross-encoder/nli-deberta-v3-small?blobs=true)
[^zeroshot-v2-card]: MoritzLaurer/deberta-v3-base-zeroshot-v2.0 card, https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0. Evidence [card_MoritzLaurer_deberta-v3-base-zeroshot-v2.0.txt](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0)
[^qwen25-05b-card]: Qwen/Qwen2.5-0.5B-Instruct card, https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct. Evidence [card_Qwen_Qwen2.5-0.5B-Instruct.txt](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
[^typesafe-blog]: TypeSafe AI blog, https://typesafe.ai/blog/introducing-system-one-models-and-jev. Evidence [jev_typesafe_blog.txt](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
[^awesome-jev]: https://github.com/AbdelStark/awesome-typesafe-jev, README (third-party list). Evidence [jev_awesome_readme.txt](https://github.com/AbdelStark/awesome-typesafe-jev)
