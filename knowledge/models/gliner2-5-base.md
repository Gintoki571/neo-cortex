---
type: Model
title: GLiNER2.5 Base (fastino/gliner2.5-base-v1)
description: English boundary-architecture GLiNER2.5 checkpoint for schema-driven NER, classification, records and relations, runnable locally through the gliner2 package.
resource: https://huggingface.co/fastino/gliner2.5-base-v1
tags: [model, gliner2, gliner2.5, information-extraction, ner, classification, relation-extraction, cpu]
status: stable
generated: { by: claude-haiku-5-5/models-agent, at: 2026-10-15T19:30:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:30:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: gliner25-hf-card
    resource: https://huggingface.co/fastino/gliner2.5-base-v1
    title: 'fastino/gliner2.5-base-v1 model card'
    last_modified: 2026-10-08T18:52:12Z
  - id: gliner25-hf-api
    resource: https://huggingface.co/api/models/fastino/gliner2.5-base-v1
    title: 'HF API metadata (tags, license, sha, files)'
    last_modified: 2026-10-08T18:52:12Z
  - id: gliner2-pip-check
    resource: https://pypi.org/project/gliner2/2.1.0/
    title: 'gliner2 2.1.0 package source (throwaway venv, read only)'
    last_modified: 2026-10-09T17:49:12Z
  - id: gliner2-github-readme
    resource: https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md
    title: 'fastino-ai/GLiNER2 README (main)'
    last_modified: 2026-10-09T17:53:44Z
  - id: gliner2-pypi
    resource: https://pypi.org/pypi/gliner2/json
    title: 'gliner2 on PyPI (2.1.0)'
    last_modified: 2026-10-09T17:49:12Z
evidence:
  - { name: gliner2.5-api.json, url: "https://huggingface.co/api/models/fastino/gliner2.5-base-v1", url_basis: inferred, sha256: a84548dd9a1a2b4004c8076f11d88ec625a3476072ea6db7514ed64d6ea11cea, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2.5-README.txt, url: "https://huggingface.co/fastino/gliner2.5-base-v1/raw/main/README.md", url_basis: inferred, sha256: 1b023a4786371699477e0b635d2a148f10fe5c23ab1e9d36211ff58754289bbe, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2.5-config.json, url: "https://huggingface.co/fastino/gliner2.5-base-v1/raw/main/config.json", url_basis: inferred, sha256: d6b515c21ae2100c12267fb42a3f02c1e99ad87580366aebedb161efd74441c7, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2.5-tree.json, url: "https://huggingface.co/api/models/fastino/gliner2.5-base-v1/tree/main", url_basis: inferred, sha256: 42e89697abecda303149b1d5f4a58628eb911a136cc7ff5c3f7524521950be68, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: gliner2_readme.txt, url: "https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md", sha256: 78f50ae3c773afe07941adea199311d6527a6001111b660f4110223f938feeae, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { name: pypi_gliner2.json, url: "https://pypi.org/pypi/gliner2/json", sha256: c133c8aafac94bfe3c18668127f6b102b6b85632ea569442e04fcade029bb02e, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
  - { file: references/evidence/models/gliner2-pip-api-check.txt, sha256: c79df201c53c0311f4e32dd16d8dc2a3733608df41700405ae3d959c794a654a, retrieved_at: 2026-10-15T19:28:00Z, method: command }
  - { name: gh_gliner2_repo.json, url: "https://api.github.com/repos/fastino-ai/GLiNER2", sha256: 705d251b6c293f2ad6319106eac69cdff1d0f311578855b506ee80a415ea5e26, retrieved_at: 2026-10-15T19:28:00Z, method: curl, redistributed: false }
---

# Summary

GLiNER2.5 Base is the English checkpoint of the GLiNER2.5 family. It is a schema-conditioned encoder: you pass the labels at call time instead of training a new head. The card describes it as:

> GLiNER2.5 Base is the English boundary checkpoint at DeBERTa-v3-base scale. It is the everyday English model for schema-driven NER, classification, records, and relations.[^gliner25-hf-card]

Evidence: [gliner2.5-README.txt](https://huggingface.co/fastino/gliner2.5-base-v1/raw/main/README.md).

Family and paper history are in [gliner2-family-and-paper](/models/gliner2-family-and-paper.md). Classifier options that matter for a decision role are in [system1-classifier-candidates](/models/system1-classifier-candidates.md).

# Facts (retrieved 2026-10-15)

| Item | Value | Source |
|---|---|---|
| HF repo | `fastino/gliner2.5-base-v1`, not gated, not private | [API JSON](https://huggingface.co/api/models/fastino/gliner2.5-base-v1) |
| Repo sha | `54785d51df8d86a0d8f2eb212fec15871aad2c4d` | API JSON `sha` |
| Last modified (HF) | 2026-10-08T18:52:12Z | API JSON `lastModified` |
| Downloads / likes | 108,784 / 39 (snapshot) | API JSON |
| License | Apache-2.0 | API tag `license:apache-2.0`, card |
| Languages | English (`en`) | API `cardData.language` |
| Parameters | 194M (card); 193,581,591 F32 params (safetensors metadata) | card, API `safetensors` |
| Weight file | `model.safetensors` 774,366,564 bytes (F32) | API `siblings` with `blobs=true` |
| Encoder | `microsoft/deberta-v3-base` | card |
| Max span length | `max_len=4096` window | card |
| Architecture | `Gliner2ForSchemaExtraction`, `architecture: boundary` | API `config`, [config.json](https://huggingface.co/fastino/gliner2.5-base-v1/raw/main/config.json) |
| Pipeline tag | `schema-extraction` | API `cardData` |

## Disk size: card and files disagree

The card says:

> - **Weights:** ~407 MB (mostly FP16)[^gliner25-hf-card]

The repo file listing says the safetensors file is 774,366,564 bytes, and the safetensors metadata says all 193,581,591 parameters are F32 (the metadata is the more direct source). The discrepancy is recorded here rather than resolved. Expect roughly 0.77 GB on disk for the default upload, plus tokenizer files (8.3 MB `tokenizer.json`). Source: [gliner2.5-tree.json](https://huggingface.co/api/models/fastino/gliner2.5-base-v1/tree/main)[^gliner25-hf-api].

## Tasks supported

Tags on the repo: Text classification, Named Entity Recognition, Relation Extraction, Intent classification, Sentiment Analysis, Topic classification, Structured extraction, Json extraction, boundary-extraction, schema-extraction.[^gliner25-hf-api]

The card lists the following methods (all verbatim from the README):

- Entities: `model.extract_entities(text, labels, include_confidence=True, include_spans=True)`
- Classification: `model.classify_text(text, {"sentiment": [...]})`, plus `Classifier` for cross-task constraints
- Relations: `model.extract_relations(...)` or schema `.relations(...)`
- Records (structured extraction): `.structure("purchase", mode="natural", anchor="buyer")`
- Span attributes: `AttributeGroup(...)` applied to entity spans
- Joint IE with typed graph search: `JointIE`

Quote on the constraint limit:

> Use `gliner2.classification.Classifier` when labels on one task legally constrain another. `classify_text` will not enforce those rules.[^gliner25-hf-card]

Quote on relation typing:

> Independent extraction does **not** guarantee that `works_for` heads are people and tails are organizations.[^gliner25-hf-card]

Hierarchical structure: the card documents record structures with one anchor field and `required_one` / list cardinality. I did not find a separate "hierarchical" claim beyond this.

## Loading and usage (exact API from card)

Install (quote from card):

> Python 3.10 or newer is required. The `[local]` extra pulls in PyTorch so you can load Hub checkpoints.[^gliner25-hf-card]

```bash
pip install "gliner2[local]"
```

```python
from gliner2 import AutoExtractor

model = AutoExtractor.from_pretrained("fastino/gliner2.5-base-v1")

print(type(model).__name__)
print(model.config.architecture)
# BoundaryExtractor
# boundary
```

Quote on the loader trap:

> Always use `AutoExtractor` for GLiNER2.5. `GLiNER2.from_pretrained(...)` is the legacy **span** loader and will not dispatch this checkpoint.[^gliner25-hf-card]

Device flags on the card: `map_location="cuda"` (or `"cpu"`, `"mps"`), `quantize=True` (fp16 weights on GPU), `compile=True`.[^gliner25-hf-card]

Verified in the installed package (gliner2 2.1.0, source read, no weights downloaded): `AutoExtractor.from_pretrained` reads the saved `architecture` field and raises `ArchitectureMismatchError` when a requested architecture differs from the saved one; `BoundaryExtractor` is defined in `gliner2/models/boundary/model.py`.[^gliner2-pip-check]

## Thresholds and output

- Remote client and local runtime `classify_text` both default to `threshold: float = 0.5`.[^gliner2-pip-check]
- Classification config can carry `cls_threshold` per task (card example uses `0.4` for multi-label aspects).[^gliner25-hf-card]
- `extract_entities` returns half-open character offsets: "Returned offsets are half-open character spans into the original string: `text[start:end] == entity["text"]`."[^gliner25-hf-card]
- Constrained classification returns `feasible` and per-task `probabilities`; the card example shows `{"_meta": {"feasible": True, "decoder": "exact"}}`.[^gliner25-hf-card]
- Joint IE: "Always check `result.feasible`. `False` means the hard constraints could not be satisfied (distinct from "the text contains no facts")."[^gliner25-hf-card]

## Context length

Quote from card: "`extract(...)` with `max_len` **truncates**." Long-context helpers chunk text:

> A span is kept only if its start and end fall in the **same chunk**.[^gliner25-hf-card]

The card gives `max_len=4096` as the encoded window. The `gliner2` config default is `max_len: int = None` (no value fixed in the file I read).[^gliner2-pip-check]

## CPU vs GPU

- Card: "Local inference: CPU, CUDA, or MPS through `gliner2[local]` — no external API required"[^gliner2-github-readme]
- Repo README: "**CPU first**: fast local inference on standard hardware — no GPU required".[^gliner2-github-readme] This is a vendor claim with no number attached.
- The `gliner2.5-small-v1` row in the same README is labelled "Fast CPU / edge".[^gliner2-github-readme]
- The card gives no latency or throughput number for the base model. Vendor speed claims are **unverified** here.

## Benchmarks

- The model card for 2.5 Base has no benchmark table (checked the README text in [gliner2.5-README.txt](https://huggingface.co/fastino/gliner2.5-base-v1/raw/main/README.md)).
- The GLiNER2 paper's numbers are for the v1 span model, not 2.5. See [gliner2-family-and-paper](/models/gliner2-family-and-paper.md).
- Lyon's KG experiment uses GLiNER2.5 base on a synthetic corpus and reports precision/recall/F1; that is one third-party run, not a benchmark. See [jev-typesafe-claim-check](/models/jev-typesafe-claim-check.md).

## Known limitations (from the card)

- English only: "Language: English".[^gliner25-hf-card]
- Do not load with `GLiNER2` / `SpanExtractor`.
- Word splitter: "Changing a pretrained model's word boundaries can affect quality unless the model was trained with the same splitter."[^gliner2-github-readme]
- Long spans cannot cross chunks in long-context mode.

## Pip package

- PyPI latest version `2.1.0`, `requires_python >=3.10`, upload 2026-10-09T17:49:12. Project URLs point to the GitHub repo.[^gliner2-pypi]
- Base install needs only pydantic, requests, tqdm, urllib3. `[local]` adds torch, transformers, peft, safetensors, numpy.[^gliner2-pypi]
- The GitHub repo `fastino-ai/GLiNER2` is Apache-2.0, default branch `main`, `pushed_at` 2026-10-09T17:53:44Z, 2,374 stars at retrieval (one API snapshot, [gh_gliner2_repo.json](https://api.github.com/repos/fastino-ai/GLiNER2)).

## Not run

Model weights were not downloaded (about 0.77 GB), so no inference run and no timing was done. The only executed step was installing `gliner2==2.1.0` in a throwaway venv and reading its source.

# Open questions

- Actual CPU latency and memory for `gliner2.5-base-v1` on this machine. Not measured.
- Whether the card's "~407 MB (mostly FP16)" is stale or refers to a different artifact. Not resolved.
- Whether `max_len` default is 4096 at load time. The card states the encoded window; the package default was not confirmed.
- F1 or accuracy numbers for 2.5 Base on any public benchmark. None found in the card or README.

# Related

- [gliner2-family-and-paper](/models/gliner2-family-and-paper.md)
- [system1-classifier-candidates](/models/system1-classifier-candidates.md)
- [jev-typesafe-claim-check](/models/jev-typesafe-claim-check.md)
- [index](/models/index.md)

[^gliner25-hf-card]: fastino/gliner2.5-base-v1 model card, https://huggingface.co/fastino/gliner2.5-base-v1
[^gliner25-hf-api]: HF API JSON, https://huggingface.co/api/models/fastino/gliner2.5-base-v1
[^gliner2-github-readme]: fastino-ai/GLiNER2 README, https://raw.githubusercontent.com/fastino-ai/GLiNER2/main/README.md
[^gliner2-pypi]: PyPI JSON, https://pypi.org/pypi/gliner2/json
[^gliner2-pip-check]: Throwaway venv, `pip install gliner2==2.1.0`, source read. Evidence [gliner2-pip-api-check.txt](/references/evidence/models/gliner2-pip-api-check.txt)
