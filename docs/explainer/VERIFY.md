# How the explainer was checked

The page was written by CodeBuddy (GLM-5.3-Flash, max effort, `archify` skill); its own verification run was cut off by a rate limit (HTTP 429), so the orchestrator checked it on 2026-10-18 with obscura (headless browser, `obscura fetch file://...`):

- Loads from disk, title "Neo-Cortex — interactive explainer", 11 inline SVG diagrams, 12 sections, no external URLs in the file.
- All 12 navigation tabs switch to exactly one visible section; clicking a diagram node fills the side panel.
- Every `../../` file path used for node links exists in the repo.
- All 59 decimal numbers on the page (for example 0.87, 0.903, 0.94, +0.23) also appear in README.md, docs/*.md, eval/* or knowledge/architecture/*.md.
- Desktop screenshot reviewed. Not checked: the 400 px layout in a real browser (CSS has `@media` rules, but obscura cannot resize its viewport).

2026-10-18 (second pass): added tab 6 "FalkorDB & Cypher" (feature table plus a viewer for 8 queries copied from docs/cypher.md) and paper/code links on the lineage cards; re-checked with obscura: 13 tabs each show exactly one section, the query viewer switches queries, 11 links on the lineage cards, arXiv IDs 2507.18546, 2609.24972, 2405.14831, 2502.14802 and 2407.03618 resolved to the expected titles.
