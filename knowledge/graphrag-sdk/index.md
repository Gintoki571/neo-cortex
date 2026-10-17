# GraphRAG SDK (FalkorDB) concepts

- [overview](/graphrag-sdk/overview.md): what graphrag-sdk is, latest release 1.4.0 (2026-08-10), Python >=3.10, Apache-2.0, extras, maintenance, API generations, vendor benchmark claims.
- [architecture](/graphrag-sdk/architecture.md): facade, 9-step ingestion pipeline, ontology (manual and discovered), extraction, resolution, FalkorDB storage layout, retrieval summary, what "chat sessions" means.
- [pluggability](/graphrag-sdk/pluggability.md): base classes and signatures for LLM, embedder, NER (GLiNER or any non-LLM extractor), chunker, loader, resolver, retriever, reranker. Which swaps were run.
- [db-connectivity](/graphrag-sdk/db-connectivity.md): how the SDK builds its FalkorDB client, injection points, falkordblite compatibility (TCP route and in-process route, both verified; raw driver fails), vector and fulltext index syntax, 1.4.0 vector-ordering bug, FalkorDB 6.x issue.
- [retrieval-strategies](/graphrag-sdk/retrieval-strategies.md): MultiPathRetrieval (default) steps and parameters, LocalRetrieval, text-to-Cypher opt-in, reranking, vendor benchmark numbers with caveats.
- [docs-site-map](/graphrag-sdk/docs-site-map.md): the 20 pages under docs.falkordb.com/graphrag, what each covers, lastmod, and which pages conflict with the 1.4.0 release.

Third-party fetches and source snapshots (docs, 1.4.0 and main source, falkordblite source) are not redistributed; URL, sha256 and retrieved_at are in each concept's frontmatter. Own run outputs and the exact commands are in `references/evidence/graphrag-sdk/runs/` (`runs/commands.txt`).
