---
type: Reference
title: '"How to Build an Agent That Reasons Over a Graph" (WeMakeDevs blog)'
description: Official Graph Hacks blog post teaching a graph-backed on-call agent (Blast Radius) built on FalkorDB, Cypher, MCP tools and a verification step; includes verbatim code and the source links.
resource: https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph
tags: [hackathon, falkordb, cypher, mcp, agents, graphrag, blog]
status: stable
stale_after: 2026-10-19T00:00:00Z
generated: { by: claude-haiku-5-5/hackathon-agent, at: 2026-10-15T19:30:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:30:00Z }
evidence:
  - { name: wemakedevs-blog-agent-reasons-over-graph.txt, url: "https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph", sha256: 71038654c4b6ec7420d82d902292d1abff9c5665e713b7205582b31ee44e333a, retrieved_at: 2026-10-15T19:24:00Z, method: obscura, redistributed: false }
  - { name: falkordb-docs-algorithms-sppath.txt, url: "https://docs.falkordb.com/algorithms/sppath", sha256: cb9ba2707190b67e0f79c27add40fa67519ccb65d493fb67f6648f9bdd9b9def, retrieved_at: 2026-10-15T19:24:00Z, method: obscura, redistributed: false }
  - { name: falkordb-docs-algorithms-pagerank.txt, url: "https://docs.falkordb.com/algorithms/pagerank", sha256: a879b051ea27e1535d7c4da684631e17eba41dae545368a483bc8e9958ad63f4, retrieved_at: 2026-10-15T19:24:00Z, method: obscura, redistributed: false }
  - { name: falkordb-docs-known-limitations.txt, url: "https://docs.falkordb.com/cypher/known-limitations", sha256: 2a97b10da09db8ee7eef8ae40f819c1cb2f65936878d5d015e104168c5cad783, retrieved_at: 2026-10-15T19:24:00Z, method: obscura, redistributed: false }
  - { name: github-api-falkordb-repo.json, url: "https://api.github.com/repos/FalkorDB/FalkorDB", sha256: f91b66969ebd41e390333b9af9e58f0f175970d726c66663193fb4221aeab580, retrieved_at: 2026-10-15T19:24:00Z, method: curl, redistributed: false }
sources:
  - id: blog-post
    resource: https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph
    title: How to Build an Agent That Reasons Over a Graph
    author: Aayush Sharma, COO, WeMakeDevs
    last_modified: 2026-10-15T00:00:00Z
  - id: falkordb-sppath-docs
    resource: https://docs.falkordb.com/algorithms/sppath
    title: "FalkorDB docs: algo.SPpaths"
  - id: falkordb-pagerank-docs
    resource: https://docs.falkordb.com/algorithms/pagerank
    title: "FalkorDB docs: algo.pageRank"
  - id: falkordb-limitations-docs
    resource: https://docs.falkordb.com/cypher/known-limitations
    title: "FalkorDB docs: Known limitations (relationship uniqueness)"
  - id: falkordb-repo
    resource: https://github.com/FalkorDB/FalkorDB
    title: FalkorDB GitHub repository
---

# What the post is

A tutorial by WeMakeDevs COO Aayush Sharma. It frames the Graph Hacks challenge and then builds one example project, "Blast Radius", an on-call agent over a service dependency graph.[^blog-post]

> "I have built a demo application called Blast Radius which is an on-call agent over a service dependency graph. You tell it a service is down, and it tells you what else breaks, who is on call for each of those things, and what changed in the last few hours. Every answer comes back with the hops it walked to get there."
> Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

The post's design claim:

> "The design decision worth copying is that the agent never writes a query. It chooses from a fixed set of tools, a person wrote the Cypher inside each one, and the arguments are checked against the graph before anything runs."
> Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

Related: [overview](/hackathon/overview.md), [judging and prizes](/hackathon/judging-and-prizes.md).

# Architecture

> "One database, six tools, and a model that never touches the query language."
> Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

Stack, as the post's prerequisites table gives it:

| Requirement | Why (verbatim) |
|---|---|
| Docker | "Runs FalkorDB locally, which is the whole of the infrastructure" |
| Python 3.12 | "The tools, the agent loop and the tests" |
| The `falkordb` client | "`pip install falkordb`, the official Python client" |
| An LLM endpoint | "Any provider. The model picks tools and writes one sentence" |

The post names no specific model. It says "Any provider." The stack has no named LLM, so model choice is an open question.

Components table from the post (verbatim, abridged):

> "FalkorDB | Holds services, teams, people, changes and findings in one graph"
> "Cypher | Every tool's query, parameterised"
> "FalkorDB algorithms | Shortest path and PageRank as agent tools"
> "MCP | How the agent sees the six tools"
> "FalkorDB Browser | Inspecting the model while you build"
> Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

Graph schema the demo uses (from the post):

```
(:Service {name, tier})-[:DEPENDS_ON {kind, weight}]->(:Service)
(:Team)-[:OWNS]->(:Service)
(:Person)-[:MEMBER_OF]->(:Team)
(:Person)-[:ONCALL_FOR {from, to}]->(:Team)
(:Person)-[:WORKED_ON {commits}]->(:Service)
(:Change {sha, at, author})-[:TOUCHED]->(:Service)
(:Incident {id, at, summary})-[:AFFECTED]->(:Service)
(:Finding {text, at, session})-[:ABOUT]->(:Service)
```

Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

# Step-by-step flow

1. **Start the database.** Quoted command block: `docker run --rm -p 6379:6379 -p 3000:3000 falkordb/falkordb:latest` then `pip install falkordb`, `python seed.py`, `uvicorn app:api --reload`. Port 3000 is FalkorDB Browser.
2. **Write and read a graph** with `select_graph` and `ro_query` (snippet below).
3. **Traverse** with a variable-length pattern to compute blast radius (Problem 1).
4. **Lock the tools.** Six named tools with typed arguments, exposed over MCP. Each name is resolved against the graph before any query runs (Problem 2).
5. **Use algorithms as tools.** `algo.SPpaths` and `algo.pageRank` (Problem 3).
6. **Write memory back** as `Finding` nodes and read them first in the next session (Problem 4).
7. **Return the path with the answer** and validate the generated sentence against the result (Problem 5).

Four answer outcomes the agent must distinguish:

> "Answered with a path"; "Answered from memory"; "Not in the graph"; "Unknown service"
> Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

# Key code (verbatim from the post)

The post wraps each block in stray backticks. The inner code is quoted below.

Starter graph (`select_graph`, `ro_query`):

```python
from falkordb import FalkorDB
db = FalkorDB(host="localhost", port=6379)
g = db.select_graph("ops")
g.query("""
    CREATE (:Service {name: 'checkout-web'})
           -[:DEPENDS_ON {weight: 1}]->
           (:Service {name: 'payments-api'})
""")
rows = g.ro_query("""
    MATCH (a:Service)-[:DEPENDS_ON]->(b:Service)
    RETURN a.name AS upstream, b.name AS downstream
""").result_set
print(rows)
# [['checkout-web', 'payments-api']]
```

Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

Blast radius (Problem 1):

```cypher
MATCH path = (upstream:Service)-[:DEPENDS_ON*1..$depth]->(s:Service {name: $name})
RETURN DISTINCT upstream.name AS service,
       length(path)          AS hops,
       [n IN nodes(path) | n.name] AS via
ORDER BY hops, service
```

Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

Parallel-edge workaround (Problem 1). The docs confirm this behaviour:

```cypher
MATCH (a)-[e]->(b) WHERE ID(e) >= 0 RETURN COUNT(b)
```

> "When a relation in a match pattern is not referenced elsewhere in the query, FalkorDB will only verify that at least one matching relation exists (rather than operating on every matching relation)."
> Evidence: [falkordb-docs-known-limitations.txt](https://docs.falkordb.com/cypher/known-limitations)

Tool catalogue (Problem 2):

```python
TOOLS = {
    "blast_radius":   {"args": {"service": "service_name", "depth": "int<=4"}},
    "who_to_wake":    {"args": {"service": "service_name", "depth": "int<=4"}},
    "recent_changes": {"args": {"service": "service_name", "hours": "int<=168"}},
    "path_between":   {"args": {"from": "service_name", "to": "service_name"}},
    "load_bearing":   {"args": {"limit": "int<=20"}},
    "recall":         {"args": {"service": "service_name"}},
}
```

Name resolution (Problem 2):

```python
def resolve_service(graph, name: str) -> str | None:
    rows = graph.ro_query(
        "MATCH (s:Service {name: $name}) RETURN s.name AS name",
        {"name": name},
    ).result_set
    return rows[0][0] if rows else None
```

Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)

Shortest path (Problem 3). Call syntax matches the FalkorDB docs ([sppath](https://docs.falkordb.com/algorithms/sppath)), which show `CALL algo.SPpaths({ sourceNode: a, targetNode: g, relTypes: ['Road'], weightProp: 'dist' })` and `YIELD path, pathWeight`:

```cypher
MATCH (a:Service {name: $from}), (b:Service {name: $to})
CALL algo.SPpaths({
  sourceNode:   a,
  targetNode:   b,
  relTypes:     ['DEPENDS_ON'],
  relDirection: 'outgoing',
  weightProp:   'weight',
  pathCount:    1
})
YIELD path, pathWeight
RETURN [n IN nodes(path) | n.name] AS hops, pathWeight
```

PageRank (Problem 3). Matches the docs form `CALL algo.pageRank('Paper', 'CITES') YIELD node, score` ([pagerank](https://docs.falkordb.com/algorithms/pagerank)):

```cypher
CALL algo.pageRank('Service', 'DEPENDS_ON')
YIELD node, score
RETURN node.name AS service, score
ORDER BY score DESC
LIMIT $limit
```

Memory write and read (Problem 4):

```cypher
MATCH (s:Service {name: $name})
CREATE (f:Finding {text: $text, at: $at, session: $session})
CREATE (f)-[:ABOUT]->(s)
```

```cypher
MATCH (f:Finding)-[:ABOUT]->(s:Service {name: $name})
RETURN f.text AS finding, f.at AS at
ORDER BY f.at DESC
LIMIT 5
```

Tenant isolation (Problem 4):

```python
graph = db.select_graph(f"ops:{tenant_id}")
```

Answer assembly and validation (Problem 5):

```python
answer = {
    "outcome": "answered_with_path",
    "services": [r["service"] for r in rows],
    "paths":    [r["via"] for r in rows],
    "oncall":   oncall_rows,
    "changes":  change_rows,
}
```

```python
NAME = re.compile(r"\b[a-z][a-z0-9]*(?:-[a-z0-9]+)+\b")

def accepts(sentence: str, answer: dict) -> tuple[bool, str]:
    known = set(answer["services"]) | {h for p in answer["paths"] for h in p}
    invented = set(NAME.findall(sentence)) - known
    if invented:
        return False, f"named services not in the result: {sorted(invented)}"
    if not answer["services"] and "no " not in sentence.lower():
        return False, "claimed impact when the traversal was empty"
    return True, "ok"
```

Evidence for the Problem 4 and 5 snippets: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph).

# Repos and links the post gives

| Link | Kind | Note |
|---|---|---|
| https://github.com/FalkorDB/FalkorDB | Code repo | Database. Metadata in [github-api-falkordb-repo.json](https://api.github.com/repos/FalkorDB/FalkorDB). Stars 10154, default branch `main`, pushed 2026-10-15T14:25:40Z, license "Other" (SSPLv1 per README). |
| https://docs.falkordb.com | Docs | Hub. |
| https://docs.falkordb.com/cypher, /cypher/known-limitations | Docs | Cypher and the parallel-edge note. |
| https://docs.falkordb.com/algorithms | Docs | Algorithm list. |
| https://docs.falkordb.com/browser | Docs | FalkorDB Browser. |
| https://docs.falkordb.com/graphrag | Docs | GraphRAG-SDK. |
| https://app.falkordb.cloud | Hosted | FalkorDB Cloud. |
| https://github.com/FalkorDB/GraphRAG-SDK | Code repo | Named in the resources page, not the blog. |

Not linked: no repository for "Blast Radius" is given. The post shows no URL to its code. See open questions.

# Claims in the post, and their status

- Verified against docs: the `algo.SPpaths` and `algo.pageRank` call syntax (see sources above).
- Verified against docs: the parallel-relationship counting behaviour in [known limitations](https://docs.falkordb.com/cypher/known-limitations).
- Not verified (marketing or design claims, not run): "Traversals are fast enough to run on every step of an agent loop"; "one instance holds a graph per tenant"; "`docker pull falkordb/falkordb:latest`" as the install path (the FalkorDB README gives `docker run -p 6379:6379 -p 3000:3000 -it --rm -v ./data:/var/lib/falkordb/data falkordb/falkordb`, which is the same image).
- Not run: none of the Python in this post was executed by the research agent. The seed script and the `app:api` FastAPI app are not published.

# Open questions

- Source code for Blast Radius: not linked.
- Which LLM and which MCP server implementation the post uses: not named ("Any provider").
- The `seed.py` and `app:api` files it refers to: not published.
- Whether the FalkorDB Cloud free tier or credits exist for hackathon use: not stated in this post.

[^blog-post]: WeMakeDevs blog. Evidence: [wemakedevs-blog-agent-reasons-over-graph.txt](https://www.wemakedevs.org/blogs/how-to-build-an-agent-that-reasons-over-a-graph)
