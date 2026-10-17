# MCP smoke test

`scripts/mcp_smoke.py` against a fresh daemon (`NEO_HOME=/tmp/... neo serve --port 8789`, GPU, GTX 1660 Ti) after ingesting the six synthetic kind folders with `neo ingest --wait`. Run 2026-10-17 on commit bc62cc8. Every tool is called once over streamable HTTP.

Result: 15 of 15 tools OK. Tool descriptions plus input schemas cost about 2077.0 tokens (chars/4) of agent context per session.

| tool | ok | latency ms | output chars |
|---|---|---|---|
| brief | OK | 37.8 | 389 |
| recall | OK | 153.2 | 3540 |
| remember | OK | 39.9 | 108 |
| ask | OK | 225.5 | 3896 |
| explore | OK | 7.6 | 2060 |
| connect | OK | 5.7 | 1634 |
| who | OK | 11.4 | 1596 |
| timeline | OK | 170.1 | 1559 |
| impact | OK | 9.6 | 1579 |
| relate | OK | 40.5 | 155 |
| handoff | OK | 4.1 | 124 |
| dream | OK | 7.3 | 80 |
| cypher | OK | 3.0 | 20 |
| ingest | OK | 168.1 | 157 |
| read | OK | 6.2 | 2335 |

Per-tool context cost (description + schema tokens):

- ask: 31.5 + 52.8
- brief: 26.5 + 82.0
- connect: 22.5 + 76.5
- cypher: 121.0 + 67.0
- dream: 30.8 + 51.0
- explore: 26.8 + 91.0
- handoff: 22.5 + 161.2
- impact: 33.5 + 69.0
- ingest: 28.2 + 79.8
- read: 32.2 + 48.5
- recall: 25.8 + 143.0
- relate: 81.0 + 159.0
- remember: 57.5 + 259.2
- timeline: 25.5 + 99.2
- who: 22.0 + 50.5

Reproduce: start a daemon on a scratch NEO_HOME, ingest data/synthetic/{doc,adr,ticket,chat,meeting,session} with --wait (never WORLD.md), then `uv run --no-sync python scripts/mcp_smoke.py --url http://127.0.0.1:8789/mcp`.
