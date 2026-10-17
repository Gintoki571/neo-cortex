---
type: Hackathon Prizes
title: Graph Hacks judging and prizes
description: Per-track prizes, side prizes, the $20,000 pool, and the only judging guidance published (no weights or scoring rubric found).
resource: https://www.wemakedevs.org/hackathons/falkordb
tags: [hackathon, prizes, judging, tracks]
status: stable
stale_after: 2026-10-19T00:00:00Z
generated: { by: claude-haiku-5-5/hackathon-agent, at: 2026-10-15T19:30:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:30:00Z }
evidence:
  - { name: wemakedevs-falkordb-hackathon.txt, url: "https://www.wemakedevs.org/hackathons/falkordb", sha256: d75c67f09726594c4803d5c143f167e72eba077fb9b9499dcf6c57eb730894f1, retrieved_at: 2026-10-15T19:23:00Z, method: obscura, redistributed: false }
  - { name: wemakedevs-falkordb-rules.txt, url: "https://www.wemakedevs.org/hackathons/falkordb/rules", sha256: 82b7afb355569402b0a01251a916f2805516d31b15817bf8de37e9ebe27a7082, retrieved_at: 2026-10-15T19:23:00Z, method: obscura, redistributed: false }
  - { name: wemakedevs-blog-agent-reasons-over-graph.txt, url: "https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph", sha256: 71038654c4b6ec7420d82d902292d1abff9c5665e713b7205582b31ee44e333a, retrieved_at: 2026-10-15T19:24:00Z, method: obscura, redistributed: false }
sources:
  - id: hackathon-page
    resource: https://www.wemakedevs.org/hackathons/falkordb
    title: Graph Hacks overview page (WeMakeDevs)
  - id: rules-page
    resource: https://www.wemakedevs.org/hackathons/falkordb/rules
    title: Graph Hacks rules page (WeMakeDevs)
  - id: blog-post
    resource: https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph
    title: How to Build an Agent That Reasons Over a Graph (WeMakeDevs blog)
    last_modified: 2026-10-15T00:00:00Z
---

# Prize pool

> "Prize pool: $20,000. One prize for each track, plus two side prizes. Every member of a winning team gets the prize."
> Evidence: [wemakedevs-falkordb-hackathon.txt](https://www.wemakedevs.org/hackathons/falkordb)

> "The prize pool is worth $20,000."
> Evidence: [wemakedevs-falkordb-rules.txt](https://www.wemakedevs.org/hackathons/falkordb/rules)

The published amounts for the side prizes do not add up to a stated total. Only "$20,000 in total" is given.

# Track prizes

| Track | Prize (verbatim) | Winning criterion (verbatim) |
|---|---|---|
| 01 Agents That Act on Connected Data | "iPhone 18 Pro" | "For the best agent that uses a graph to make decisions and take action." |
| 02 Agent Memory and Coordination | "PS5 with GTA VI" | "For the best agents that remember across sessions and share what they know." |
| 03 Company Brain | "M6 Mac Mini" | "For the best agent that understands how a company works and gets work done." |

> "14. ... The best project in each track wins a prize: an iPhone 18 Pro for Agents That Act on Connected Data, a PS5 with GTA VI for Agent Memory and Coordination, and an M6 Mac Mini for Company Brain. Every member of a winning team gets the prize."
> Evidence: [wemakedevs-falkordb-rules.txt](https://www.wemakedevs.org/hackathons/falkordb/rules)

Each track prize is awarded to the "best project in each track" (rules 14). A team that enters more than one track can, in principle, win more than one prize, but the rules do not say so explicitly. See open questions.

# Side prizes

> "Best blog post. Write a blog post about your project. The best post wins a pair of AirPods 5."
> Evidence: [wemakedevs-falkordb-hackathon.txt](https://www.wemakedevs.org/hackathons/falkordb)
> Listed as "AirPods 5 / 1 winner / Best blog post" on the overview page.

> "Top 50 submissions. Every member of the top 50 teams gets a t-shirt, shipped to their address."
> Evidence: [wemakedevs-falkordb-hackathon.txt](https://www.wemakedevs.org/hackathons/falkordb)

The side prizes are not in the rules page's list of prizes (rule 14 names only the three track prizes). Treat them as published on the overview page only.

# Judging criteria

No scoring rubric, weights, judge list or results date was found on any of the pages read. The only judging guidance is the blog section below and the per-track "Key focus" lists.

> "What Judges Are Looking For. In all three tracks the judging comes back to whether the graph is doing work the agent could not do without it. A project where the graph is a store the agent occasionally reads from is a project that any database would have served, and that reads immediately."
> Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

Matching rule 3 of the rules: "The graph has to do real work. A visualisation drawn on top of ordinary storage does not qualify" ([rules](/hackathon/rules.md)).

The overview page also states the brief: "Work the graph has to do", including "Show the path behind an answer."

> "Show the path behind an answer"
> Evidence: [wemakedevs-falkordb-hackathon.txt](https://www.wemakedevs.org/hackathons/falkordb)

## Key focus per track (judging hints, not weighted criteria)

- Track 01: "Multi-hop reasoning", "Graph queries and algorithms as agent tools", "Tool selection through MCP", "Actions based on what the graph shows", "Explainable results".
- Track 02: "Episodic, semantic, and procedural memory", "Persistent conversation history", "Shared state and handoffs between agents", "High-concurrency reads and writes", "Separate memory per user or tenant".
- Track 03: "Knowledge from docs, tickets, and chats in one graph", "Who owns what, and who knows what", "Tracing decisions back to their source", "Keeping knowledge current as things change", "Answers with clear sources".

Evidence for all three lists: [wemakedevs-falkordb-hackathon.txt](https://www.wemakedevs.org/hackathons/falkordb).

# Open questions

- Judging criteria, weights, judge identities, and the results announcement date: not published.
- Whether one team can win more than one track prize: not stated.
- Whether the side prizes (best blog post, top 50) are in addition to the $20,000 pool or inside it: not stated. The overview says "One prize for each track, plus two side prizes" inside a "$20,000 in total" pool.
- Whether a blog post is a separate submission item or an optional part of the submission: not stated. Rule 10 lists the required submission items, and a blog is not among them.

# Related

- [Overview](/hackathon/overview.md)
- [Rules](/hackathon/rules.md)
- [Submission checklist](/hackathon/submission-checklist.md)
