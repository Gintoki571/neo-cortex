"""MCP server: one shared Store, 12 tools over stdio or streamable HTTP (127.0.0.1 by default).

Run: python -m neo_cortex.mcp_server --transport http --port 8765   (or --transport stdio)
Sync tools run on SDK worker threads, so a slow ingest does not block other agents.

Also a loopback HTTP API for the `neo` CLI and Claude Code hooks (the embedded DB has one owner, this daemon):
GET /health, POST /api/<tool> (JSON args, returns the tool's text), POST /api/ingest-session (queued when "background").
"""
import argparse
import json
import queue
import sys
import threading
from contextlib import asynccontextmanager

from mcp.server.mcpserver import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from . import tools as T

API_TOOLS = ("brief", "recall", "remember", "ask", "explore", "connect", "who", "timeline", "ingest", "handoff", "cypher", "dream")

INSTRUCTIONS = """Neo-Cortex: shared memory, company knowledge graph and multi-hop evidence. It returns cited evidence; you do the reasoning.
- Start of a session: call brief (pass project/agent) and act on open handoffs.
- Before re-solving or asking the user something: recall(query).
- After finishing a task: remember decisions, lessons and user preferences, one fact per call. If a fact changed, pass supersedes=<memory id> (conflicts are listed when you remember).
- Company or multi-hop questions: ask(question) first, then who (owners/experts), connect (how A relates to B), timeline (what changed), explore (neighbourhood).
- cypher is read-only and a last resort.
- Ids in results ([mem_..], [doc#chunk], [e_..]) can be passed back as arguments. Every tool accepts max_chars; follow "narrow with" hints."""

SCHEMA = ("Nodes: Document{id,kind,title,date_ms,author} -HAS_CHUNK-> Chunk{id,text,date_ms}; Entity{id,name,key,type,mentions}; "
          "Memory{id,text,kind,status,created_ms,agent,project}; Handoff{id,summary,status}; Agent{id,name}. Edges: (Chunk|Memory)-[:MENTIONS]->Entity; "
          "(Entity)-[:REL{type,conf,source_id,valid_from_ms}]->(Entity) with type OWNS|MEMBER_OF|DEPENDS_ON|...; Entity-[:AUTHORED|PARTICIPATED]->Document; "
          "Memory-[:SUPERSEDES]->Memory. Times are epoch ms.")


def make_server(store, on_shutdown=None) -> MCPServer:
    @asynccontextmanager
    async def lifespan(_):
        try:
            yield {}
        finally:
            if on_shutdown:  # uvicorn re-raises SIGTERM after serving, so main()'s finally may never run
                import anyio
                await anyio.to_thread.run_sync(on_shutdown)

    s = MCPServer("neo-cortex", instructions=INSTRUCTIONS, lifespan=lifespan)

    @s.tool()
    def brief(project: str | None = None, agent: str | None = None, max_chars: int = 4000) -> str:
        """Session-start context: open handoffs for you, preferences, decisions, lessons, recent facts and documents."""
        return T.brief(store, project, agent, max_chars)

    @s.tool()
    def recall(query: str, k: int = 8, since: str | None = None, until: str | None = None, kinds: list[str] | None = None,
               max_chars: int = 4000) -> str:
        """Hybrid search over memories and documents. Dates are ISO (2026-03-01); kinds filter by memory/doc kind."""
        return T.recall(store, query, k, since, until, kinds, max_chars)

    @s.tool()
    def remember(text: str, kind: str | None = None, about: list[str] | None = None, supersedes: str | None = None,
                 agent: str | None = None, project: str | None = None, max_chars: int = 4000) -> str:
        """Save one decision, lesson, preference or fact. kind: episodic|semantic|procedural|preference|decision (auto if omitted). supersedes: id of the memory this replaces."""
        return T.remember(store, text, kind, about, supersedes, agent, project, max_chars)

    @s.tool()
    def ask(question: str, max_chars: int = 4000) -> str:
        """Multi-hop evidence pack for a company or code question: linked entities, bridging paths, facts, cited chunks. Does not answer."""
        return T.ask(store, question, max_chars)

    @s.tool()
    def explore(entity: str, hops: int = 1, since: str | None = None, max_chars: int = 4000) -> str:
        """Neighbours of an entity (name or id) with relation, date and source, plus the documents mentioning it most."""
        return T.explore(store, entity, hops, since, max_chars)

    @s.tool()
    def connect(a: str, b: str, max_hops: int = 4, max_chars: int = 4000) -> str:
        """Shortest relation paths between two entities (names or ids), with the source of each edge."""
        return T.connect(store, a, b, max_hops, max_chars)

    @s.tool()
    def who(topic: str, max_chars: int = 4000) -> str:
        """People ranked as owners or experts for a topic, with the path or documents that show it."""
        return T.who(store, topic, max_chars)

    @s.tool()
    def timeline(topic: str, since: str | None = None, until: str | None = None, max_chars: int = 4000) -> str:
        """Dated events about an entity or topic, oldest first: relation changes, documents, superseded memories."""
        return T.timeline(store, topic, since, until, max_chars)

    @s.tool()
    def ingest(path_or_text: str, kind: str | None = None, max_chars: int = 4000) -> str:
        """Add a file, directory or raw text to the knowledge graph. kind (raw text only): doc|adr|ticket|chat|meeting|file."""
        return T.ingest(store, path_or_text, kind, max_chars)

    @s.tool()
    def handoff(to: str | None = None, summary: str | None = None, tasks: list[str] | None = None, from_agent: str | None = None,
                done: str | None = None, max_chars: int = 4000) -> str:
        """Leave work for another agent (shown in its brief), or pass done=<handoff id> to close one."""
        return T.handoff(store, to, summary, tasks, from_agent, done, max_chars)

    @s.tool(description="Read-only Cypher, last resort. " + SCHEMA)
    def cypher(query: str, limit: int = 50, max_chars: int = 4000) -> str:
        return T.cypher(store, query, limit, max_chars)

    @s.tool()
    def dream(dry_run: bool = False, max_chars: int = 4000) -> str:
        """Consolidate memories: merge duplicates, promote repeated episodes, decay unused ones, flag conflicts. dry_run reports only."""
        return T.dream(store, dry_run, max_chars)

    _add_api(s, store)
    return s


def _add_api(s, store):
    jobs, stats = queue.Queue(), {"queued": 0, "done": 0, "errors": 0}

    def worker():  # one at a time: sessions share the GPU and the Store
        while True:
            args = jobs.get()
            try:
                from . import write
                write.ingest_session(store, **args)
                stats["done"] += 1
            except Exception as e:
                stats["errors"] += 1
                print(f"ingest-session {args.get('transcript_path')}: {e!r}", file=sys.stderr, flush=True)

    def guard(req: Request):
        # CSRF / DNS rebinding: a web page can POST to localhost, but not with a JSON content type nor a foreign Host
        if req.headers.get("host", "").rsplit(":", 1)[0] not in ("127.0.0.1", "localhost", "[::1]"):
            return PlainTextResponse("bad host", 403)
        if not req.headers.get("content-type", "").startswith("application/json"):
            return PlainTextResponse("content-type must be application/json", 415)

    @s.custom_route("/health", methods=["GET"])
    async def health(req: Request):
        return JSONResponse({"ok": True, **stats, "pending": jobs.qsize()})

    @s.custom_route("/api/{tool}", methods=["POST"])
    async def api(req: Request):
        import anyio
        if (bad := guard(req)):
            return bad
        tool = req.path_params["tool"]
        try:
            args = await req.json()
            assert isinstance(args, dict)
        except Exception:
            return PlainTextResponse("body must be a JSON object", 400)
        if tool == "ingest-session":
            if "transcript_path" not in args:
                return PlainTextResponse("transcript_path required", 400)
            if args.pop("background", False):
                if not stats["queued"]:
                    threading.Thread(target=worker, daemon=True).start()
                stats["queued"] += 1
                jobs.put(args)
                return JSONResponse({"queued": args["transcript_path"]})
            from . import write
            fn = lambda **a: json.dumps(write.ingest_session(store, **a), separators=(",", ":"))  # noqa: E731
        elif tool in API_TOOLS:
            fn = lambda **a: getattr(T, tool)(store, **a)  # noqa: E731
        else:
            return PlainTextResponse(f"unknown tool {tool}", 404)
        try:
            return PlainTextResponse(await anyio.to_thread.run_sync(lambda: fn(**args)))
        except TypeError as e:  # bad argument names
            return PlainTextResponse(f"bad arguments: {e}", 400)
        except Exception as e:
            return PlainTextResponse(f"{tool} failed: {e!r}", 500)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="neo_cortex.mcp_server")
    ap.add_argument("--transport", choices=["stdio", "http"], default="http")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--warm", action="store_true", help="load GLiNER and EmbeddingGemma at start instead of on first use")
    a = ap.parse_args(argv)
    from .store import Store
    store = Store()
    lock, closed = threading.Lock(), []

    def close():
        with lock:
            if not closed:
                closed.append(1)
                store.close()

    if a.warm:
        from . import models
        threading.Thread(target=lambda: (models.embed_query("warm"), models.gliner()), daemon=True).start()
    server = make_server(store, close)
    try:
        if a.transport == "stdio":
            server.run("stdio")
        else:
            server.run("streamable-http", host=a.host, port=a.port)
    finally:
        close()


if __name__ == "__main__":
    main()
