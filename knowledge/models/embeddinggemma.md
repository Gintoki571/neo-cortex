---
type: Model
title: EmbeddingGemma 2 (google/embeddinggemma-2) and EmbeddingGemma 300M
description: Google DeepMind's open multimodal embedding model; google/embeddinggemma-2 exists and is ungated, the 300M predecessor is gated. Dimensions, prompts, precision and vendor MTEB numbers.
resource: https://huggingface.co/google/embeddinggemma-2
tags: [model, embeddings, embeddinggemma, google, sentence-transformers, matryoshka, retrieval]
status: stable
generated: { by: claude-haiku-5-5/models-agent, at: 2026-10-15T19:30:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: egemma2-card
    resource: https://huggingface.co/google/embeddinggemma-2
    title: 'google/embeddinggemma-2 model card'
    last_modified: 2026-10-06T15:29:23Z
  - id: egemma2-hf-api
    resource: https://huggingface.co/api/models/google/embeddinggemma-2?blobs=true
    title: 'HF API metadata for google/embeddinggemma-2 (files, sizes, license tag)'
    last_modified: 2026-10-06T15:29:23Z
  - id: egemma-300m-hf-api
    resource: https://huggingface.co/api/models/google/embeddinggemma-300m
    title: 'HF API metadata for google/embeddinggemma-300m (gated: manual)'
    last_modified: 2025-09-25T15:11:17Z
  - id: egemma-300m-card
    resource: https://huggingface.co/google/embeddinggemma-300m
    title: 'google/embeddinggemma-300m (card page, returned 401 gated stub)'
    last_modified: 2025-09-25T15:11:17Z
evidence:
  - { name: card_google_embeddinggemma-2.txt, url: "https://huggingface.co/google/embeddinggemma-2", sha256: b677a0ee2818c36f091b65fd3d9b4baea9f04d53b02b49cae916c74bf9682037, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_google_embeddinggemma-2.json, url: "https://huggingface.co/api/models/google/embeddinggemma-2", sha256: 3958fb0b148794bc3037c6b628088c852f86c49408a7768024baef9f3efe937d, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_embeddinggemma-2_blobs.json, url: "https://huggingface.co/api/models/google/embeddinggemma-2?blobs=true", sha256: 28d9e7e5d095bfe387d1cd6c2bf07f4a081e718b77fd3a40c893d86c9bcc6e82, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: api_google_embeddinggemma-300m.json, url: "https://huggingface.co/api/models/google/embeddinggemma-300m", sha256: c2ec6c9bb7ae75024b428924575a4102ccdcad10d56fc1db22768ecb9908d056, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: card_google_embeddinggemma-300m.txt, url: "https://huggingface.co/google/embeddinggemma-300m", sha256: 340dda0e070bd01e5a655e0200e765080045baaa197d8576155baed3bcc12ca5, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
---

# Does the repo exist?

Yes. `google/embeddinggemma-2` returns HTTP 200 for the model page, the model card and the HF API. The API record: `createdAt` 2026-09-14T14:53:42Z, `lastModified` 2026-10-06T15:29:23Z, 144,280 downloads and 2,383 likes at retrieval, `gated: false`, sha `914f7f89142e33e77833254d9c9b90c3cef7303b`.[^egemma2-hf-api]

The name in the brief was checked as given. The 300M predecessor exists too, as `google/embeddinggemma-300m`. It is gated (see below).

# Facts

| Item | Value | Source |
|---|---|---|
| Native output dimension | 768 | card "Native Output Dimension" |
| Matryoshka sizes | 128, 256, 512, 768 | card "MRL Truncation Dimensions" (128/256/512 listed in table; 768 native) |
| Context window | 8,192 tokens (card: "8K token context window") | card |
| Parameters | 740M total (card); 744,371,512 BF16 (metadata) | card, API |
| Text backbone | 270M (130M transformer + 140M embedder) | card |
| Vision / audio encoders | 170M / 300M, loadable separately | card |
| Modalities | Text, images, video, audio | card, API tags |
| Languages | "understands 100+ languages" (card), `language: multilingual` (tag) | card |
| Pooling | mean pooling; projection 512→768 | card "Model Overview" |
| Weight file | `model.safetensors`, 1,488,915,288 bytes (BF16) | API `blobs=true` |
| Quantized / ONNX / GGUF files in repo | none in listing | API `siblings` |
| Library | `transformers`, sentence-transformers tag | API |
| Gated | no (`gated: false`) | API |
| Licence | `license:apache-2.0` (API tag and card header) | API, card |

## Licence wording to check

The card header says `license: apache-2.0`, but the card's own link under "License" reads "Apache 2.0" and points to `https://ai.google.dev/gemma/docs/gemma_4_license`. The card text is:

> **License**: <a href="https://ai.google.dev/gemma/docs/gemma_4_license" target="_blank">Apache 2.0</a> | <b>Authors</b>: <a href="https://deepmind.google/models/gemma/" target="_blank">Google DeepMind</a>[^egemma2-card]

The header says `apache-2.0` while the linked text names a Gemma-4 licence URL. Read the linked licence before shipping. This is an open question, not a settled fact.

## Gating: 2 is open, 300M is gated

- `google/embeddinggemma-2`: `gated: false`.[^egemma2-hf-api]
- `google/embeddinggemma-300m`: `gated: "manual"`, licence `gemma`, the API `extra_gated_prompt` says the user is "required to review and agree to Google" usage license terms. The card page returned this stub (HTTP 401):

> Access to model google/embeddinggemma-300m is restricted. You must have access to it and be authenticated to access it. Please log in.[^egemma-300m-card]

The 300M model card was not retrieved past the stub, so its benchmark and prompt details are not in this note.

# Usage with sentence-transformers (card quick start)

Install (quote):

```bash
pip install -U sentence-transformers transformers
```

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("google/embeddinggemma-2")

query = "What causes the northern lights?"
document = "The northern lights are caused by charged particles from the sun."

query_emb = model.encode(query, prompt_name="SearchQuery")
doc_emb = model.encode(document, prompt_name="Document")
print(model.similarity(query_emb, doc_emb))
```

Source: card "Quick Start".[^egemma2-card]

## Prompt prefixes

The card says: "EmbeddingGemma 2 is trained with short task instruction prefixes prepended to text inputs. Using the right prefix improves quality; omitting it still works but reduces precision."[^egemma2-card]

| Use case | Type | Prompt name | Query instruction | Document instruction |
|---|---|---|---|---|
| Web / document search | Asymmetric | SearchQuery | `task: search result \| query: {query}` | `title: {title} \| text: {content}` |
| Question answering | Asymmetric | QuestionAnswering | `task: question answering \| query: {question}` | `title: {title} \| text: {passage}` |
| Fact checking | Asymmetric | FactChecking | `task: fact checking \| query: {claim}` | `title: {title} \| text: {evidence}` |
| Code search | Asymmetric | CodeRetrieval | `task: code retrieval \| query: {query}` | `title: {title or filename} \| text: {code}` |
| Classification | Symmetric | Classification | `task: classification \| query: {content}` | N/A |
| Clustering | Symmetric | Clustering | `task: clustering \| query: {content}` | N/A |
| Similarity | Symmetric | SentenceSimilarity | `task: sentence similarity \| query: {content}` | N/A |

Card note: "`prompt_name="Document"` applies `title: none`; titled documents must still be formatted manually, like `model.encode(f"title: {title} | text: {document}")`."[^egemma2-card]

## Matryoshka truncation

Quote: "The supported dimensions are 768, 512, 256, and 128. Shorter vectors reduce storage and speed up similarity search at some cost to quality."[^egemma2-card]

Quote on renormalisation: "The shortened vector must be L2-normalized before it is used for cosine similarity. Skipping this step degrades ranking quality silently—it produces plausible-looking scores rather than an error."[^egemma2-card]

Code from card:

```python
query_emb = model.encode(
   query,
   truncate_dim=128, # or 512, 256
   normalize_embeddings=True,
)
```

## Precision (important for CPU)

Quote: "Run inference in `bfloat16` or `float32`. Do not use `float16`."[^egemma2-card]

Quote: "Use `float32` elsewhere, including on most CPUs."[^egemma2-card]

So on a CPU box, load in float32, not fp16 and not the BF16 default if the CPU lacks native bf16.

## Memory footprint by modality

Card table (text-only drops the vision and audio encoders): text only 270M effective, text + image 440M, text + audio 570M, full 740M.[^egemma2-card] The sibling `model.safetensors` is 1.49 GB in BF16 for the full model, so text-only loading should be much smaller. The card does not give a text-only file size.

## Context budget for multimodal input

Text: 1 token per subword, max 8,192. Image: 280 tokens per image by default (about 29 images). Video: 140 tokens per frame by default. Audio: 25 tokens per second (about 327 seconds).[^egemma2-card] Only text is relevant to the Neo-Cortex pipeline.

# MTEB and benchmark numbers (vendor claims)

The card table, full precision, 768d:

> | *Text* | Massive Text Embedding Benchmark (MTEB, multilingual, v2) | Mean(Task), Multiple | 61.36 | 61.15 |

EmbeddingGemma 1 is 61.15 on the same row. Code (MTEB code v1, NDCG@10): 78.68 for 2, 68.76 for 1.[^egemma2-card]

Truncation (MTEB multilingual v2 Mean(Task)): 768d 61.36, 512d 61.17, 256d 60.41, 128d 57.89. English v2: 768d 68.46, 128d 65.68.[^egemma2-card]

These are the vendor's numbers. No independent re-run was done. The card itself says 128d "is best suited to text-only workloads" and that multimodal quality degrades at 128d.[^egemma2-card]

# CPU suitability

- The card says: "Designed to run on consumer hardware such as mobile devices and laptops, EmbeddingGemma 2 delivers low-latency semantic representations for on-device applications".[^egemma2-card] Vendor claim, no latency number on the card.
- No ONNX or quantized variant is in the repo listing, so CPU runs would use the safetensors file in float32.
- Speed on this machine was not measured (no weights downloaded).

# Open questions

- Licence: Apache 2.0 (tag and header) vs the linked Gemma-4 licence page. Needs a read of the linked licence text.
- Whether a quantized or ONNX build is published under another Google or community repo. None found in this repo's listing.
- Text-only file size for the 270M backbone (not stated).
- Independent (non-vendor) MTEB numbers.

# Related

- [system1-classifier-candidates](/models/system1-classifier-candidates.md) (embedding models are not a classifier; listed for context only)
- [index](/models/index.md)

[^egemma2-card]: google/embeddinggemma-2 model card, https://huggingface.co/google/embeddinggemma-2. Evidence [card_google_embeddinggemma-2.txt](https://huggingface.co/google/embeddinggemma-2)
[^egemma2-hf-api]: HF API, https://huggingface.co/api/models/google/embeddinggemma-2. Evidence [api_google_embeddinggemma-2.json](https://huggingface.co/api/models/google/embeddinggemma-2), [api_embeddinggemma-2_blobs.json](https://huggingface.co/api/models/google/embeddinggemma-2?blobs=true)
[^egemma-300m-card]: https://huggingface.co/google/embeddinggemma-300m (401 gated). Evidence [card_google_embeddinggemma-300m.txt](https://huggingface.co/google/embeddinggemma-300m)
