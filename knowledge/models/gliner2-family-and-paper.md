---
type: Reference
title: GLiNER2 family, versions and paper
description: What the GLiNER2 paper covers, how the span-based GLiNER2 differs from the boundary-based GLiNER2.5, and the sibling checkpoints with their sizes and licences.
resource: https://arxiv.org/abs/2507.18546
tags: [model, gliner2, gliner2.5, paper, family, arxiv]
status: stable
generated: { by: claude-haiku-5-5/models-agent, at: 2026-10-15T19:30:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: gliner2-arxiv
    resource: https://arxiv.org/abs/2507.18546
    title: 'GLiNER2: An Efficient Multi-Task Information Extraction System with Schema-Driven Interface (arXiv 2507.18546)'
    last_modified: 2026-10-15T19:24:24Z
  - id: gliner2-github-readme
    resource: https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md
    title: 'fastino-ai/GLiNER2 README (main)'
    last_modified: 2026-10-09T17:53:44Z
  - id: gliner2-github-api
    resource: https://api.github.com/repos/fastino-ai/GLiNER2
    title: 'GitHub repo metadata for fastino-ai/GLiNER2'
    last_modified: 2026-10-09T17:53:44Z
  - id: gliner2-hf-api-family
    resource: https://huggingface.co/api/models/fastino/gliner2.5-small-v1
    title: 'HF API metadata for GLiNER2 family members (fetched per model)'
    last_modified: 2026-10-08T18:52:15Z
  - id: gliner2-decide-card
    resource: https://huggingface.co/fastino/GLiNER2.5-Decide
    title: 'fastino/GLiNER2.5-Decide model card'
    last_modified: 2026-10-08T20:47:53Z
evidence:
  - { name: arxiv_2507.18546.xml, url: "https://arxiv.org/abs/2507.18546", sha256: 3ca195851e93df137fde4a9409d8966d5b96e77f591c74705b6d7b9daf52e1b6, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2_arxiv_html.txt, url: "https://arxiv.org/html/2507.18546", url_basis: inferred, sha256: f320e9717473fea9ad0645cb1533c2e8bf6d2de9a3e3bedd59dafaae57711d1f, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2_arxiv_html.html, url: "https://arxiv.org/html/2507.18546", url_basis: inferred, sha256: 0c18ba66425665242d6d2128e4a1d19416333ccc8b41c3abc1f219e2fbba836b, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2_readme.txt, url: "https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md", sha256: 78f50ae3c773afe07941adea199311d6527a6001111b660f4110223f938feeae, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gh_gliner2_repo.json, url: "https://api.github.com/repos/fastino-ai/GLiNER2", sha256: 705d251b6c293f2ad6319106eac69cdff1d0f311578855b506ee80a415ea5e26, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gh_gliner2_release.json, url: "https://api.github.com/repos/fastino-ai/GLiNER2/releases/408188242", sha256: 8b16c218112b7df6d3409c8d7d5583e12eefb4f49d496f979bc81cb79729af00, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_gliner2-base-v1.json, url: "https://huggingface.co/api/models/fastino/gliner2-base-v1", sha256: 2cf59e40981277e80756cff7e07ce0c6d105bf123ac71073561b00545b707c1b, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_gliner2-base.json, url: "https://huggingface.co/api/models/fastino/gliner2-base", sha256: 2cf59e40981277e80756cff7e07ce0c6d105bf123ac71073561b00545b707c1b, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_gliner2-large-v1.json, url: "https://huggingface.co/api/models/fastino/gliner2-large-v1", sha256: ee813b598c568d40b01ae59cb776cfacc24b621571413deba1324bd57953f165, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_gliner2-large.json, url: "https://huggingface.co/api/models/fastino/gliner2-large", sha256: 65842e3d84e6b7f62a470c85204e80b953bb8f944e9b69813130a9d7f3eaa1d8, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_gliner2-multi-v1.json, url: "https://huggingface.co/api/models/fastino/gliner2-multi-v1", sha256: 88f40c7340343d9c3050e64c8abf2e65fac0a79ae12c9f5df02515cfdd74e5b7, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_gliner2.5-small-v1.json, url: "https://huggingface.co/api/models/fastino/gliner2.5-small-v1", sha256: 67d737929fb5c6bd192d60e0bd779d0d7982997f5137c3d31d63c365b200cd2d, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_gliner2.5-multi-v1.json, url: "https://huggingface.co/api/models/fastino/gliner2.5-multi-v1", sha256: fbceb1e16ebe6dcf03a58fd971a411237968bc184a734676757a98888a96ff00, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_GLiNER2.5-Decide.json, url: "https://huggingface.co/api/models/fastino/GLiNER2.5-Decide", sha256: 44c2ef4c7487f312c1dfd15f5ee847be65e3de8ce1349a607193a8b28e7d51d9, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_fastino_GLiNER2.5-multi-Decide.json, url: "https://huggingface.co/api/models/fastino/GLiNER2.5-multi-Decide", sha256: 270d129ca25200cfdff231130c7e99578286a5ac8b919e1b7cc1cf8d7d0852af, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: card_fastino_GLiNER2.5-Decide.txt, url: "https://huggingface.co/fastino/GLiNER2.5-Decide", sha256: 09a9705ee8c30392bb5a82ac503c01b889ff7e957a4c96bf7249f05acde709a3, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { file: references/evidence/models/gliner2-pip-api-check.txt, sha256: c79df201c53c0311f4e32dd16d8dc2a3733608df41700405ae3d959c794a654a, retrieved_at: 2026-10-15T19:28:00Z, method: command }
---

# Summary

GLiNER2 is a schema-conditioned encoder family from Fastino AI. Two extraction architectures now sit behind one loader, `AutoExtractor`:

> - **`span`** (`GLiNER2` / `SpanExtractor`) — fixed-width span grid; legacy checkpoints and specialty fine-tunes (GLiGuard, PII).
> - **`boundary`** (`BoundaryExtractor`, **GLiNER2.5**) — sparse start/end pairing; any span length within the encoded window.[^gliner2-github-readme]

The paper describes the first (span) system. The 2.5 boundary models are a later release. Per-model facts are in [gliner2-5-base](/models/gliner2-5-base.md).

# The paper (arXiv 2507.18546)

- Title: "GLiNER2: An Efficient Multi-Task Information Extraction System with Schema-Driven Interface". Authors: Urchade Zaratiana, Gil Pasternak, Oliver Boyd, George Hurn-Maloney, Ash Lewis (Fastino AI).[^gliner2-arxiv]
- Published 2025-07-24 (v1). The arXiv HTML I fetched is `v1 [cs.CL] 24 Jul 2025`, licence CC BY 4.0. The arXiv API's `updated` field is 2026-10-15, but the text I read is v1, so later revisions are not covered.
- Abstract, verbatim: "We present GLiNER2, a unified framework that enhances the original GLiNER architecture to support named entity recognition, text classification, and hierarchical structured data extraction within a single efficient model."[^gliner2-arxiv]
- Abstract, verbatim: "GLiNER2 maintains CPU efficiency and compact size while introducing multi-task composition through an intuitive schema-based interface."[^gliner2-arxiv]
- The abstract also says: "We release GLiNER2 as an open-source library available through pip, complete with pre-trained models and comprehensive documentation."[^gliner2-arxiv]

## Results the paper reports (v1 span model)

- CrossNER zero-shot F1 (Table 3): "GLiNER2 closely matches GPT-4o in overall F1 score (0.590 vs. 0.599)". The GLiNER-M average in the same table is 0.615.[^gliner2-arxiv]
- Classification: "GLiNER2 achieves the highest average accuracy among open-source baselines, outperforming GLiClass on five datasets and DeBERTa-v3 on three."[^gliner2-arxiv]
- Latency (Table 4, CPU): the paper says "The key advantage becomes evident when comparing against DeBERTa, which performs a separate forward pass for each label, resulting in linear scaling with the number of labels and substantially higher latency ( 6.8× slower with 20 labels)."[^gliner2-arxiv] The numbers in Table 4 did not survive the text extraction cleanly, so only this ratio is quoted.
- Sentiment: "On sentiment benchmarks, GLiNER2 scores 0.86–0.87, close to DeBERTa-v3's 0.89–0.92 and within 10 points of GPT-4o."[^gliner2-arxiv]

These are the paper's numbers. They are not evidence about GLiNER2.5.

## What the paper does not cover

- The string "boundary" does not appear in the arXiv HTML text. The 2.5 boundary head, its training, and its benchmark numbers are not in this paper.
- No 2.5 numbers were found in the 2.5 base card (see [gliner2-5-base](/models/gliner2-5-base.md)).

# Family table (verified against HF API and README)

| Repo | Architecture | Size (card) | Params (HF metadata) | Notes |
|---|---|---|---|---|
| `fastino/gliner2-base-v1` | span | 205M (README) | 208,476,821 | Default span checkpoint, licence Apache-2.0 |
| `fastino/gliner2-base` | span | (alias) | 208,476,821 | HF API returns the `gliner2-base-v1` record |
| `fastino/gliner2-large-v1` | span | 340M (README) | 486,444,053 | DeBERTa-v3-large encoder |
| `fastino/gliner2-multi-v1` | span | ~205M (README) | 307,098,645 | Multilingual; card and metadata disagree |
| `fastino/gliner2-large` | not found | n/a | n/a | HF API returned 401 "Invalid username or password." |
| `fastino/gliner2.5-small-v1` | boundary | 74M | 73,881,879 | "Fast CPU / edge" per README |
| `fastino/gliner2.5-base-v1` | boundary | 194M | 193,581,591 | English default |
| `fastino/gliner2.5-multi-v1` | boundary | 287M | 287,355,159 | Multilingual default |
| `fastino/GLiNER2.5-Decide` | span | 340M (card) | 486,444,053 | Classification specialist; span per README |
| `fastino/GLiNER2.5-multi-Decide` | boundary | 287M | 287,355,159 | Multilingual classification specialist |

Sources: HF API JSON in the [evidence folder](/references/evidence/models/) (one file per repo), and the family table in [gliner2_readme.txt](https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md).[^gliner2-hf-api-family]

Quote on the loader cheat sheet:

> | Text classification (English) | `fastino/GLiNER2.5-Decide` |[^gliner2-github-readme]

Quote on Decide:

> Decide checkpoints are tuned for classification: use `classify_text` / `batch_classify_text` (or `Classifier`). Both load with `AutoExtractor`; note that `GLiNER2.5-Decide` is a span checkpoint despite the 2.5 name, so `GLiNER2.from_pretrained` also loads it, while `GLiNER2.5-multi-Decide` is boundary-only.[^gliner2-github-readme]

## Inconsistencies found

- `gliner2-base-v1` card says 205M; the HF metadata gives 208.5M parameters. Within rounding, not a contradiction.
- `gliner2-multi-v1` README says "~205M"; HF metadata gives 307M. Not resolved.
- `GLiNER2.5-Decide` card says "340M"; HF metadata gives 486,444,053 parameters (F32). Not resolved. The same discrepancy shows in the Decide card's own header, which says "The 340M English classification model".[^gliner2-decide-card]
- `gliner2-large` (no `-v1`) returns 401 from the HF API. Treated as not resolvable; the real large checkpoint is `gliner2-large-v1`.

## Decide benchmark (vendor)

The Decide card lists an exact-match average on `fastino/fast-decisions` (17 domains, 300 held-out examples each). Values quoted from the card:

> | **GLiNER2.5-Decide (340M)** | **60.2%** |

Other rows on the same card: `GLiNER2.5-Decide-1B` 59.6%, `JevK5` 57.6%, `GLiNER2.5-multi-Decide (287M)` 56.7%, `SemIf (Qwen3.5-4B)` 56.4%, `GLiFormer large-v1` 49.0%, `Laya Router` 46.6%.[^gliner2-decide-card] This is a vendor benchmark on the vendor's own dataset. Treat it as a claim. The "JevK5" row is not identified on the card; I did not establish whether it has any link to TypeSafe's Jev (see [jev-typesafe-claim-check](/models/jev-typesafe-claim-check.md)).

# What changed in 2.5 (from the README and card)

1. **Architecture.** Span (GLiNER2 v1) uses a fixed-width span grid. 2.5 (boundary) uses sparse start/end pairing. The README states this directly (see Summary).[^gliner2-github-readme]
2. **Loader.** `AutoExtractor.from_pretrained` dispatches on the saved `architecture` field. The legacy `GLiNER2.from_pretrained` does not load boundary checkpoints.[^gliner2-github-readme]
3. **New sizes.** A 74M small English model appeared (`gliner2.5-small-v1`).[^gliner2-github-readme]
4. **Constrained decoding.** `Classifier` and `JointIE` were documented for 2.5. The GitHub README says they are the way to get "cross-task label rules" and "typed entity-relation graphs".[^gliner2-github-readme]
5. **Span attributes.** `AttributeGroup` and `entity_attributes` are documented under "GLiNER2.5".[^gliner2-github-readme]

Whether these are new in 2.5 or already in span models was not established. The README places them under the "Advanced decoding (GLiNER2.5)" heading.

# Repo and release

- GitHub `fastino-ai/GLiNER2`: Apache-2.0, default branch `main`, created 2025-07-07, `pushed_at` 2026-10-09T17:53:44Z, 2,374 stars at retrieval.[^gliner2-github-api]
- Latest release `v2.1.0`, published 2026-10-09T17:53:44Z.[^gliner2-github-api]
- PyPI `gliner2` 2.1.0 (see [gliner2-5-base](/models/gliner2-5-base.md) for details).
- Design docs linked from the README (`docs/boundary_architecture.md`, `docs/gliner2_5_boundary_architecture.md`) returned 404 from `raw.githubusercontent.com` on `main` when I fetched them, so the architecture details are only as good as the README.[^gliner2-github-api]

# Open questions

- Whether the paper will get a 2.5 revision that describes the boundary architecture. The arXiv listing shows an update date of 2026-10-15, but the text I fetched is v1.
- Which of the sizes is correct for `gliner2-multi-v1` and `GLiNER2.5-Decide` (README/card vs HF metadata).
- Identity of "JevK5" on the Decide benchmark table.
- Whether `gliner2-large` (no suffix) was ever published; the API response suggests it is not public.

[^gliner2-arxiv]: arXiv 2507.18546 abs and HTML, https://arxiv.org/abs/2507.18546 and https://arxiv.org/html/2507.18546. Evidence [gliner2_arxiv_html.txt](https://arxiv.org/html/2507.18546)
[^gliner2-github-readme]: fastino-ai/GLiNER2 README, https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md. Evidence [gliner2_readme.txt](https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md)
[^gliner2-github-api]: GitHub REST API, https://api.github.com/repos/fastino-ai/GLiNER2 and /releases/latest. Evidence [gh_gliner2_repo.json](https://api.github.com/repos/fastino-ai/GLiNER2), [gh_gliner2_release.json](https://api.github.com/repos/fastino-ai/GLiNER2/releases/408188242)
[^gliner2-hf-api-family]: HF API JSON per repo, e.g. https://huggingface.co/api/models/fastino/gliner2-large-v1
[^gliner2-decide-card]: fastino/GLiNER2.5-Decide model card, https://huggingface.co/fastino/GLiNER2.5-Decide. Evidence [card_fastino_GLiNER2.5-Decide.txt](https://huggingface.co/fastino/GLiNER2.5-Decide)

# Related

- [gliner2-5-base](/models/gliner2-5-base.md)
- [system1-classifier-candidates](/models/system1-classifier-candidates.md)
- [index](/models/index.md)
