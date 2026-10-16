# GraphRAG SDK (FalkorDB) concepts

- [overview](/graphrag-sdk/overview.md): what graphrag-sdk is, latest release 1.4.0 (2026-08-10), Python >=3.10, Apache-2.0, extras, maintenance, API generations, vendor benchmark claims.
- [architecture](/graphrag-sdk/architecture.md): facade, 9-step ingestion pipeline, ontology (manual and discovered), extraction, resolution, FalkorDB storage layout, retrieval summary, what "chat sessions" means.
- [pluggability](/graphrag-sdk/pluggability.md): base classes and signatures for LLM, embedder, NER (GLiNER or any non-LLM extractor), chunker, loader, resolver, retriever, reranker. Which swaps were run.
- [db-connectivity](/graphrag-sdk/db-connectivity.md): how the SDK builds its FalkorDB client, injection points, falkordblite compatibility (TCP route and in-process route, both verified; raw driver fails), vector and fulltext index syntax, 1.4.0 vector-ordering bug, FalkorDB 6.x issue.
- [retrieval-strategies](/graphrag-sdk/retrieval-strategies.md): MultiPathRetrieval (default) steps and parameters, LocalRetrieval, text-to-Cypher opt-in, reranking, vendor benchmark numbers with caveats.
- [docs-site-map](/graphrag-sdk/docs-site-map.md): the 20 pages under docs.falkordb.com/graphrag, what each covers, lastmod, and which pages conflict with the 1.4.0 release.

Evidence lives in `references/evidence/graphrag-sdk/` (raw fetches, source snapshots of 1.4.0 and main, falkordblite source, run outputs under `runs/`, and `runs/commands.txt` with the exact commands).
