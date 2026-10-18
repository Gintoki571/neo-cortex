# Neo-Cortex: one FalkorDB graph that gives AI agents a memory and a company a brain

*Built solo for the WeMakeDevs x FalkorDB "Graph Hacks" hackathon, all three tracks: agents that act on connected data, agent memory and coordination, company brain.*

## The problem

AI agents are brilliant for one afternoon and then they forget. A session ends, the useful decision disappears into a transcript, and tomorrow you explain everything again. Companies have the same problem in a different shape: the answer to "who owns this service, and what breaks if it goes down?" is spread over a design note, a ticket, a chat thread and a meeting page. A search box finds similar text. It cannot tell you *who owns it now*, *what changed*, or *what depends on it*.

Neo-Cortex puts all of that in one place: a graph, stored in FalkorDB, that works as an agent's long-term memory, a company's brain built from its documents, and a way to answer questions that need several steps. Agents use it through 15 MCP tools or a small `neo` command line. Code: https://github.com/Gintoki571/neo-cortex

## The picture to keep in mind

Think of a detective's string board. Every person, service, ticket or decision is a **card**. Every relationship ("owns", "depends on", "replaced by") is a **string** between two cards, with a date on it. When something changes, the old string is not thrown away; it gets an end date, so the board remembers history.

## How it works, in plain words

**1. Getting knowledge in.** A file is converted to text and cut into small pieces. A small reading model, GLiNER2.5, finds the people, services and teams and how they are linked, and asks of each sentence: is this a fact, a maybe, a denial, or a plan? A second small model, EmbeddingGemma, turns each piece into "meaning numbers" so similar text can be found. Both run on your own computer. **There is no big language model inside**, so there is no per-question bill and nothing leaves your machine. The agent that calls Neo-Cortex does the thinking.

**2. A judge who writes down every verdict.** The reading model returns a probability, like a weather forecast, not a paragraph. We store that verdict on the link. A sentence like "Mateo does not own the export service" is dropped; "we might move it next quarter" is never treated as current. In a test with a short handover note, only the real owner was returned. This idea comes from [pg-jev](https://github.com/realZachi/pg-jev), and the verdicts are cached as nodes in the graph.

**3. Agents can write straight into the graph.** When an agent has just done the work it already knows the facts, so it writes cards and strings itself with `remember` and `relate`: about 0.15 seconds, no reading step, nothing to misread.

**4. Four searches at once.** A question is answered by four searches merged into one list: by words (BM25), by meaning (vector), by connections (the graph), and by time (what was true when). Connections are the star: the graph starts at the things in the question, follows the strings, finds the shortest path between two entities, and counts what breaks if a service stops.

**5. Memory that tidies itself.** `neo dream` is an offline tidy-up inspired by [Dream-RSI](https://github.com/zhengkid/Dream-RSI): it merges duplicates, promotes things seen repeatedly, fades old notes, flags clashing notes (retry limit 3 versus 5) and writes a log node. A tuning rule inspired by [RRSI](https://github.com/google-research/rrsi) ([paper](https://arxiv.org/abs/2609.24972)) accepts new search settings only if they also win on questions it has not seen.

## How we used FalkorDB

FalkorDB is the only database. One graph per team (`neo_<tenant>`), embedded through falkordblite so there is nothing to install, or a Docker server with the same Cypher.

- **Vector indexes** (cosine, 768 dimensions) on chunks, memories and entities for the "by meaning" search, entity linking and duplicate checks.
- **`algo.SPpaths`** for the bridging paths in `connect` and `ask`.
- **Variable-length paths** such as `(person)-[:REL*1..2]->(thing)` for "who owns or knows this" and "what breaks if this stops".
- **Time on edges** (`valid_from_ms`, `valid_to_ms`) for supersession: a new owner closes the old `OWNS` edge instead of deleting it, so `timeline` can show history.
- **`GRAPH.RO_QUERY`** for the agent's read-only Cypher tool.
- **Audit nodes in the same graph**: `Judgment` (cached verdicts), `DreamRun` (tidy-up logs), `TuneRun` (tuning trials).

The Cypher and algorithms are listed in [docs/cypher.md](cypher.md) and in the README.

## What we measured (honestly)

- **Where the graph wins:** on "what breaks if this service stops?" questions the graph gave the full answer for 0.80 of questions, plain text search 0.20 (30 questions, difference +0.60 with a 95% interval of +0.30 to +0.90).
- **Where it only ties:** on finding the right document, vector search scored 0.73 recall@10, words 0.71, and all four searches together 0.76. A tie within noise, and we say so.
- **It works as a tool:** 15 of 15 MCP tools pass end to end; 16 clients at once gave no errors and no lost writes.
- **Real documents are harder:** on this repository's own 72 documents the right document was in the top 5 for 0.50 of questions, and the reading model found only 5 relationships in plain prose. That is why agents write relationships directly.

## What we learned

1. **Measure every idea you borrow.** We built seven retrieval and name-merging ideas from other open memory systems (agentmemory, graphify, Hindsight) behind switches and tested them on two collections. None beat our default, so they stay off. One of them wrongly merged "FalkorDB" into "falkordblite". A wrong merge is worse than a duplicate.
2. **A rejected result is a good result.** Our self-tuning rule tried new search settings, did better on practice questions (0.648 to 0.752), slightly worse on unseen ones, and rejected them. The check cannot be fooled, which is the point.
3. **Small models are enough for the fast work.** Reading a sentence takes about 26 ms on a 6 GB graphics card, so extraction, verdicts and routing can run on a laptop. We tested a bigger specialised model for the verdicts and it was no better than the base model plus a simple negation rule.
4. **Let the agent write what it knows.** Extraction from real prose is sparse; the agent that did the work is the best source of structure.

## What FalkorDB could improve

- A **personalized** `algo.pageRank` (a restart vector). We needed it for retrieval and had to compute it in numpy over a fetched subgraph.
- A real **BM25** option in the full-text index. We kept a separate BM25 index next to FalkorDB.
- falkordblite: a **cleaner shutdown** (we saw orphaned server processes), and the package version reports `0.0.0`.
- Clearer docs for vector query results (a distance, where smaller is nearer) and for `algo.SPpaths` output shape.
- Clear license metadata on the main repository (GitHub's API reports `NOASSERTION`).

## Try it

```
git clone https://github.com/Gintoki571/neo-cortex && cd neo-cortex
uv sync && uv run --no-sync neo serve --port 8765 --warm
```

Full setup, data model and every number with its source file are in the [README](../README.md). Built with Claude Code and other AI coding agents; I directed, reviewed and verified the work. The system itself contains no large language model.
