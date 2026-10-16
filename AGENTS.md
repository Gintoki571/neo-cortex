# DOX framework

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## User Preferences

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md

## Project Context

- Neo-Cortex: entry for the WeMakeDevs "Graph Hacks: Context for AI Agents" hackathon (FalkorDB). Submissions close 2026-10-18 18:29 UTC.
- Planned stack (user decision, see `knowledge/architecture/project-plan.md` for evidence and risks): Python; falkordblite as the DB; GLiNER2.5 (`fastino/gliner2.5-base-v1`) for extraction and classification, with a LangExtract-style pipeline as fallback; anydoc for Office-to-Markdown; EmbeddingGemma for embeddings (falkordblite vector support is verified).
- Entering all three tracks with one system: agent memory + company brain + GraphRAG reasoning, exposed as an MCP server (plus a `neo` CLI for Claude Code hooks). Current plan: `knowledge/architecture/unified-plan.md` (draft).
- Design rules from the plan: no LLM inside the system (GLiNER extracts, classifies and judges; the calling agent reasons); hybrid retrieval = vector + BM25 (`bm25s`) + graph + temporal fused with RRF; EmbeddingGemma loads text-only, vision/audio encoders only when that modality is ingested; graphrag-sdk is dropped from the core (user decision 2026-10-16). Demo data: a synthetic company (gold eval) plus a public open-source org (real data).
- All compiled project knowledge lives in `knowledge/` as an OKF v0.2 bundle.

## Child DOX Index

- `knowledge/AGENTS.md` - OKF knowledge bundle: research areas, evidence protocol, conformance check. Owns everything under `knowledge/`.
- `src/neo_cortex/AGENTS.md` - Python package: FalkorDB store, schema, graph data model contract, local models, write/retrieval/MCP modules. Owns `src/neo_cortex/`; `tests/`, `scripts/bench_models.py` and `pyproject.toml` follow it.
- `data/` - eval and demo corpora: `data/synthetic/` (fictional Pellucid Pay company, AI-generated from `WORLD.md`, format contract in its section 0), `data/public/` (public FalkorDB GitHub data, fetched by `scripts/fetch_public.py`). No local AGENTS.md.
- `eval/` - 40-question gold set (`gold.jsonl`) and `check_dataset.py`; see `eval/README.md`. No local AGENTS.md.
- `.claude/skills/` - third-party agent skills (obscura-web, web-search, opensrc, repomix, codegraph, quality-and-security); tooling, not project code, no local AGENTS.md.
