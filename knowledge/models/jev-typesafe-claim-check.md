---
type: Claim Check
title: Jev (TypeSafe AI) claim check
description: Checks the user's claim that TypeSafe's Jev returns Boolean, Choice and Score probabilities for GraphRAG micro-decisions. Jev exists; the question-type names differ; the 'Dual-Engine GraphRAG' name was not found.
resource: https://typesafe.ai/blog/introducing-system-one-models-and-jev
tags: [model, jev, typesafe, system-one, graphrag, claim-check, decision-model]
status: stable
generated: { by: claude-haiku-5-5/models-agent, at: 2026-10-15T19:30:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:30:00Z }
stale_after: 2026-11-15T00:00:00Z
sources:
  - id: typesafe-blog
    resource: https://typesafe.ai/blog/introducing-system-one-models-and-jev
    title: 'Introducing System One Models & Jev (TypeSafe AI blog)'
    last_modified: 2026-09-15T00:00:00Z
  - id: typesafe-primitives-docs
    resource: https://docs.typesafe.ai/primitives
    title: 'TypeSafe docs, Primitives (Choice, Score, Noul)'
    last_modified: 2026-10-15T00:00:00Z
  - id: typesafe-intro-docs
    resource: https://docs.typesafe.ai/introduction
    title: 'TypeSafe docs, Introduction'
    last_modified: 2026-10-15T00:00:00Z
  - id: pydantic-typesafe
    resource: https://pydantic.dev/docs/ai/models/typesafe/
    title: 'TypeSafe (Jev) | Pydantic Docs'
    last_modified: 2026-10-15T00:00:00Z
  - id: pydantic-decision
    resource: https://pydantic.dev/docs/ai/models/decision/
    title: 'Decision models | Pydantic Docs'
    last_modified: 2026-10-15T00:00:00Z
  - id: langchain-jev
    resource: https://www.langchain.com/blog/building-a-harness-with-jev
    title: 'What Is Jev? A Guide to TypeSafe AI''s System One Model (LangChain)'
    last_modified: 2026-10-15T00:00:00Z
  - id: lyon-kg-jev
    resource: https://lyonwj.com/blog/typesafe-jev-knowledge-graph-extraction
    title: 'Typed Judgments for Knowledge Graph Extraction with TypeSafe''s Jev (William Lyon)'
    last_modified: 2026-09-17T00:00:00Z
  - id: awesome-jev
    resource: https://github.com/AbdelStark/awesome-typesafe-jev
    title: 'Awesome Jev (third-party field guide)'
    last_modified: 2026-10-15T00:00:00Z
  - id: gliner2-decide-card
    resource: https://huggingface.co/fastino/GLiNER2.5-Decide
    title: 'fastino/GLiNER2.5-Decide model card (JevK5 row)'
    last_modified: 2026-10-08T20:47:53Z
  - id: tds-graphrag
    resource: https://towardsdatascience.com/graphrag-with-typesafe-jev-a-system-one-approach-to-scalable-knowledge-graphs/
    title: 'GraphRAG with TypeSafe Jev (Towards Data Science, not retrieved: Cloudflare block)'
  - id: calibrated-laya-graphrag
    resource: https://calibrateddecisions.com/projects/laya-jev-graphrag
    title: 'laya-jev-GraphRAG | Calibrated Decisions (third-party directory)'
    last_modified: 2026-09-25T00:00:00Z
evidence:
  - { file: references/evidence/models/jev_typesafe_blog.html, sha256: 71b8ae6a6a0d80511d6c6b6796a5d541dca1f629d54697b900c5ffe7a8c3bf10, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
  - { file: references/evidence/models/jev_typesafe_blog.txt, sha256: 6fbda0a3d2d947811a45415fabe153e7bef65b2a28d243eb9d41de502b059f65, retrieved_at: 2026-10-15T19:28:00Z, method: command }
  - { file: references/evidence/models/jev_typesafe_primitives.html, sha256: 9964da676aa55455fcd81f0730b3a615331f52e25bfc6913cdfd0f0b4e95507c, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
  - { file: references/evidence/models/jev_typesafe_intro.html, sha256: e60679ab518b3c20afd686d4d830d2ab4b2013e103460c1b5aeef62c8b58c307, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
  - { file: references/evidence/models/jev_pydantic_decision.txt, sha256: cf84b1abae2dcadc2a6830c1204e47ab9ba0d362faffd7ddd708d1fcb1a93324, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
  - { file: references/evidence/models/jev_pydantic_docs.txt, sha256: 1db515c8b08a9296fd0515e02bbe06ab3cbd2f2a15c4fab9d048bd3aabf9fb89, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
  - { file: references/evidence/models/jev_langchain.txt, sha256: 336bc74eaf1e4569a35d6d69ff8794705249ea963abd97cac6e773a7be3b73dc, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
  - { file: references/evidence/models/jev_lyonwj.txt, sha256: 5947f729e27a66e203659af70cc5a8c84834a9c5b6c5af227ae5603345eb3808, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
  - { file: references/evidence/models/jev_awesome_readme.txt, sha256: 8a6b6b564d7787e3e5a991d9b0fa695c0249ddc65839b9cbdb14d5921e4e4ae0, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
  - { file: references/evidence/models/jev_calibrated_laya_graphrag.txt, sha256: d5c6ef43fd5f32359c806ee121fcfb2ad1c7ed0691adca380bf4815db97c4a77, retrieved_at: 2026-10-15T19:28:00Z, method: obscura }
  - { file: references/evidence/models/jev_tds_graphrag.txt, sha256: 821cef6112a3e8ce3db612cc4c59613a3b26109bbd09343289073325f61feefa, retrieved_at: 2026-10-15T19:28:00Z, method: obscura }
  - { file: references/evidence/models/hf_search_jev.json, sha256: 24d9f4a41246118df1e91a5336741f19d845990c0d69e2e6ddbeed513a1f0dc4, retrieved_at: 2026-10-15T19:28:00Z, method: curl }
---

# Verdict

- **Jev exists.** TypeSafe AI's "System One" decision model, announced in its blog on 2026-09-15 and open in "early access". Confirmed by the vendor blog, the vendor docs, Pydantic AI docs, LangChain, and two third-party write-ups.[^typesafe-blog][^typesafe-primitives-docs][^pydantic-typesafe][^langchain-jev][^lyon-kg-jev]
- **The three question types exist, but the vendor's names are Choice, Score and Noul.** The yes/no type is called "Noul" in the vendor docs and most third-party write-ups. Mastra (search snippet only) says "boolean" and Pydantic's docs say "bool". The brief's "Boolean" is the same concept under a different label.[^typesafe-primitives-docs][^langchain-jev][^pydantic-decision]
- **"Dual-Engine GraphRAG" was not found as a name.** An exact-phrase search returned only profile pages. The closest real project is `laya-jev-GraphRAG`, which describes "swappable System One decision models (local Laya / cloud Jev)".[^calibrated-laya-graphrag]
- **Jev is a hosted API, not a downloadable model.** The docs say it is accessed through an API key, and third-party SDKs send inputs to TypeSafe. No TypeSafe-owned Hugging Face repo was found. Weights are not public as far as the retrieved sources show.[^awesome-jev]
- **Of the six micro-decisions in the brief, three have a source, two have partial support, and one has none.** See the table below.

# What Jev returns (verified)

Vendor blog, verbatim:

> Think of Jev as a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out.[^typesafe-blog]

> Type-safe structured values. Possible outputs and structure are defined in advance . The model never makes type errors. All answers are accompanied with calibrated probabilities and confidence scores.[^typesafe-blog]

Note the blog's own caveat about the claim: "No type errors : This would be an easy thing to falsify with just a single counter-example, but it is mathematically impossible." That sentence is the vendor's own claim, not an independent test.[^typesafe-blog]

Question types, from the vendor primitives page and the Pydantic docs:

| Type (brief's name) | Vendor name | What it returns | Source |
|---|---|---|---|
| Boolean | **Noul** | "a single probability of yes, between 0 and 1" (Lyon, quoting the table) | [^lyon-kg-jev] |
| Choice | Choice | "the chosen label, a probability for every option, and a confidence" | [^lyon-kg-jev] |
| Score | Score | "an expected position, a probability per level, a legend, and a confidence" | [^lyon-kg-jev] |

LangChain's version: "There are three types of supported questions : Choice: Pick from a set of options. Returns a probability for each option and an overall confidence score. Score: Rate an input against ordered levels, such as low, medium, and high. Returns a continuous score, the underlying distribution, and a confidence value. Noul: Answer a yes-or-no question. Returns the probability that a statement is true."[^langchain-jev]

Pydantic AI's mapping for the same three shapes: "a bool is a yes or no, a Literal or Enum is one label out of several, a list of labels is a yes or no per label, a bounded float is the probability of yes itself, and a set of described levels is a score against a rubric."[^pydantic-decision]

Parallelism: "System One models evaluate every question in a request in parallel. Adding questions barely changes the response time and costs only the tokens for the extra questions, which are cheap."[^langchain-jev]

## Claimed speed and cost (vendor, not verified)

- Blog: "End-to-end response time is 70ms-500ms for TypeSafe."[^typesafe-blog]
- Blog: "This is where the claims of 193.6x faster, 444.6x cheaper on our home page come from, and we expect that these are on the higher end of real world gains."[^typesafe-blog]
- Blog caveat: "our published evals are generally run from our laptops on the West Coast".[^typesafe-blog]
- Blog: "We can't prove it isn't subsidized".[^typesafe-blog]

No independent timing was done.

# The six micro-decisions in the brief

| Micro-decision | Status | Evidence |
|---|---|---|
| Assertion gating | **Supported by one third-party write-up** | Lyon uses two questions per extracted edge: a yes/no "supported" (Noul) and a Choice over "four assertion statuses" for "how does the document present the claim?". Gating result: precision 0.279 to 0.404, recall unchanged.[^lyon-kg-jev] |
| Ontology-bound relation selection | **Partial** | Lyon: GLiNER2.5 "does joint entity and relation extraction against an ontology you supply at runtime"; the post's thesis includes "where relation selection beats relation generation".[^lyon-kg-jev] Jev's role here is Lyon's pipeline stage, not a TypeSafe feature. |
| Entity resolution | **Supported by one third-party write-up** | Lyon's corpus has "13 gold alias groups for entity resolution" and a section on "why a perfect entity-resolution judge can be worth nothing".[^lyon-kg-jev] |
| Subgraph pruning | **Not found** | No retrieved Jev source (vendor, third-party or search snippet) mentions subgraph pruning. |
| Query routing | **Supported in vendor material** | LangChain: "Model-routing middleware lets Jev assess the request and choose a model based on criteria you define".[^langchain-jev] The vendor docs nav lists "Confidence-gated routing" and "Intent routing" patterns.[^typesafe-primitives-docs] |
| Grounding / verification checks | **Vendor use case, no grounding study found** | Blog: "Verify everything. Score, judge, verify, guardrail, and detect jailbreaks of LLM prompts, reasoning traces, and/or outputs."[^typesafe-blog] Third-party `grounded-ai` library has a `JevEvaluator` that "asks hosted Jev or a local Strands Decider Noul, Choice, and Score questions".[^awesome-jev] |

## Caveats on the Lyon evidence

- One author, one synthetic corpus ("ten documents about a handful of fictional companies, with 47 gold triples").[^lyon-kg-jev]
- The gating result counts edges and triples; the post says: "Of the 56 edges the gate removed, not one was a gold triple."[^lyon-kg-jev]
- Lyon's numbers came from cache replay: "the numbers below come from a run with no key set at all, replaying the cache."[^lyon-kg-jev]
- The corpus is labelled by the author, so this measures agreement with that labelling, not with an external benchmark.

## Known third-party GraphRAG-shaped projects

- `laya-jev-GraphRAG`: "Agentic GraphRAG engine using swappable System One decision models (local Laya / cloud Jev). Features a complete 4-phase pipeline (Ingestion, Pre-Retrieval, Traversal, Post-Retrieval) and evaluation across Neo4j, Memgraph, Apache AGE, and Kùzu driven by a custom A* traversal algorithm."[^calibrated-laya-graphrag] The directory page says "Not affiliated with TypeSafe AI and Jev".
- A Towards Data Science article "GraphRAG with TypeSafe Jev: A System One Approach to Scalable Knowledge Graphs" (Towards Data Science URL) exists in search results. Fetching it returned a Cloudflare challenge, so its content is not in this evidence set.[^tds-graphrag]

# Disputed or unclear items

- The vendor blog says Jev "gives up string generation" and "can't hallucinate". Both are vendor claims. The claim about "can't hallucinate" is about type-valid output, not factual correctness.
- The name "Noul" is used by the vendor primitives page, by LangChain, and by Lyon. Pydantic's docs say "bool" and Mastra's search snippet says "boolean". No retrieved source explains the name. Not resolved.
- A "JevK5" row appears on the GLiNER2.5-Decide benchmark (57.6%). A Hugging Face model named `alibiserikbay/JevK5` exists. Whether it has any relation to TypeSafe is not established.[^gliner2-decide-card]

# Open questions

- Which TypeSafe API version the user has access to (early access; waitlist per blog).
- Whether TypeSafe publishes a public benchmark on GraphRAG tasks. The blog has "workflow evals" and a separate site; I did not retrieve that site.
- Whether the "Dual-Engine GraphRAG" name refers to a private project or a post not indexed by the search tool used.
- Pricing: the blog gives "from $0.20 to $10 / MTok" for input; not checked on the pricing page.

# Related

- [system1-classifier-candidates](/models/system1-classifier-candidates.md)
- [gliner2-5-base](/models/gliner2-5-base.md)
- [gliner2-family-and-paper](/models/gliner2-family-and-paper.md)
- [index](/models/index.md)

[^typesafe-blog]: TypeSafe AI blog, https://typesafe.ai/blog/introducing-system-one-models-and-jev (page dated Sep 15, 2026). Evidence [jev_typesafe_blog.html](/references/evidence/models/jev_typesafe_blog.html), [jev_typesafe_blog.txt](/references/evidence/models/jev_typesafe_blog.txt)
[^typesafe-primitives-docs]: TypeSafe docs, https://docs.typesafe.ai/primitives. Evidence [jev_typesafe_primitives.html](/references/evidence/models/jev_typesafe_primitives.html)
[^pydantic-typesafe]: Pydantic AI docs, https://pydantic.dev/docs/ai/models/typesafe/. Evidence [jev_pydantic_docs.txt](/references/evidence/models/jev_pydantic_docs.txt)
[^pydantic-decision]: Pydantic AI decision models, https://pydantic.dev/docs/ai/models/decision/. Evidence [jev_pydantic_decision.txt](/references/evidence/models/jev_pydantic_decision.txt)
[^langchain-jev]: LangChain blog, https://www.langchain.com/blog/building-a-harness-with-jev. Evidence [jev_langchain.txt](/references/evidence/models/jev_langchain.txt)
[^lyon-kg-jev]: William Lyon, https://lyonwj.com/blog/typesafe-jev-knowledge-graph-extraction (Sep 17, 2026). Evidence [jev_lyonwj.txt](/references/evidence/models/jev_lyonwj.txt)
[^awesome-jev]: https://github.com/AbdelStark/awesome-typesafe-jev, README. Evidence [jev_awesome_readme.txt](/references/evidence/models/jev_awesome_readme.txt)
[^calibrated-laya-graphrag]: https://calibrateddecisions.com/projects/laya-jev-graphrag. Evidence [jev_calibrated_laya_graphrag.txt](/references/evidence/models/jev_calibrated_laya_graphrag.txt)
[^tds-graphrag]: https://towardsdatascience.com/graphrag-with-typesafe-jev-a-system-one-approach-to-scalable-knowledge-graphs/ returned "Attention Required! | Cloudflare" on obscura fetch. Evidence [jev_tds_graphrag.txt](/references/evidence/models/jev_tds_graphrag.txt)
[^gliner2-decide-card]: fastino/GLiNER2.5-Decide card. Evidence [card_fastino_GLiNER2.5-Decide.txt](/references/evidence/models/card_fastino_GLiNER2.5-Decide.txt)
