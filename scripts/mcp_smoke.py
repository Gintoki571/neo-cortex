"""End-to-end MCP smoke test for neo-cortex.

Connects to a running daemon over streamable HTTP and calls every tool once with
realistic arguments for the Pellucid Pay demo corpus. For each call it records
ok/error, latency (ms), output length (chars), whether the output stayed within
max_chars, and the first 200 characters. It also lists every tool with its
description length (chars) and estimated tokens (chars/4), plus the total
description+schema token estimate (the context cost an agent pays every session).

Exits non-zero if any call errors.

Usage:
    uv run --no-sync python scripts/mcp_smoke.py [--url http://127.0.0.1:8789/mcp]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
from pathlib import Path

from mcp.client import Client

MAX_CHARS = 4000
RESULTS_PATH = Path("/tmp/mcp_smoke_results.json")

# Every tool, once, with realistic arguments for the Pellucid Pay demo corpus.
# `read` is filled in from a recall result id at run time.
TOOL_CALLS = [
    ("brief", {"project": "Pellucid Pay", "agent": "claude-code"}),
    ("recall", {"query": "session cache", "k": 8}),
    ("remember", {
        "text": "The auth-service session cache holds per-device trust records next to each login session; session TTL is 3600 s.",
        "kind": "semantic",
        "about": ["auth-service", "session-cache"],
    }),
    ("ask", {"question": "What is the root cause of the incident where customers said the login felt broken?"}),
    ("explore", {"entity": "auth-service", "hops": 1}),
    ("connect", {"a": "web-dashboard", "b": "bank-connector", "max_hops": 4}),
    ("who", {"topic": "session cache"}),
    ("timeline", {"topic": "session TTL", "since": "2026-06-01"}),
    ("impact", {"entity": "auth-service", "max_hops": 3}),
    ("relate", {
        "head": "smoke-test-entity",
        "type": "RELATED_TO",
        "tail": "auth-service",
        "source": "scripts/mcp_smoke.py",
        "agent": "claude-code",
    }),
    ("handoff", {
        "to": "codex",
        "summary": "MCP smoke test baseline",
        "tasks": ["verify all tools respond"],
        "from_agent": "claude-code",
    }),
    ("dream", {"dry_run": True}),
    ("cypher", {"query": "MATCH (n) RETURN count(n)", "limit": 50}),
    ("ingest", {
        "path_or_text": "---\nkind: doc\ntitle: MCP smoke test note\ndate: 2026-06-01T00:00:00Z\nauthor: smoke\n---\nPellucid Pay MCP smoke test ingest note.",
        "kind": "doc",
    }),
]

# `read` is not in TOOL_CALLS because its `id` argument comes from a recall result.
READ_PLACEHOLDER = ("read", {})


def output_text(result) -> str:
    """Concatenate the text content blocks of a CallToolResult."""
    parts = []
    for block in (result.content or []):
        text = getattr(block, "text", None)
        if text is not None:
            parts.append(text)
    return "".join(parts)


async def main() -> int:
    ap = argparse.ArgumentParser(description="MCP smoke test for neo-cortex")
    ap.add_argument("--url", default="http://127.0.0.1:8789/mcp",
                    help="MCP streamable-http endpoint (default http://127.0.0.1:8789/mcp)")
    args = ap.parse_args()

    results = []
    tool_meta = {}
    any_error = False
    recall_id = None

    async with Client(args.url) as client:
        tl = {t.name: t for t in (await client.list_tools()).tools}

        # --- context cost: description + input schema, per tool and total ---
        total_ctx_tokens = 0.0
        print("=== tools (context cost per session) ===")
        for name in sorted(tl):
            t = tl[name]
            desc = t.description or ""
            desc_chars = len(desc)
            desc_tokens = desc_chars / 4
            schema_chars = len(json.dumps(t.input_schema or {}, sort_keys=True))
            schema_tokens = schema_chars / 4
            total_ctx_tokens += desc_tokens + schema_tokens
            tool_meta[name] = {"desc_chars": desc_chars, "desc_tokens": round(desc_tokens, 1),
                               "schema_chars": schema_chars, "schema_tokens": round(schema_tokens, 1)}
            print(f"{name}: desc_chars={desc_chars} desc_tokens={desc_tokens:.1f} "
                  f"schema_chars={schema_chars} schema_tokens={schema_tokens:.1f}")
        print(f"TOTAL description+schema token estimate: {total_ctx_tokens:.1f}")
        print()

        # --- call every tool once ---
        for name, arguments in TOOL_CALLS + [READ_PLACEHOLDER]:
            if name == "read":
                if recall_id is None:
                    print("read: SKIPPED (no id parsed from recall output)", file=sys.stderr)
                    continue
                arguments = {"id": recall_id}

            t0 = time.perf_counter()
            error = None
            ok = False
            out = ""
            try:
                result = await client.call_tool(name, arguments)
                dt_ms = (time.perf_counter() - t0) * 1000
                out = output_text(result)
                ok = not bool(getattr(result, "is_error", False))
                if not ok:
                    error = "is_error=true"
            except Exception as e:  # noqa: BLE001 - any call failure is a smoke-test error
                dt_ms = (time.perf_counter() - t0) * 1000
                error = f"{type(e).__name__}: {e}"
                ok = False
                out = ""

            within = len(out) <= MAX_CHARS
            if not ok:
                any_error = True

            results.append({
                "tool": name,
                "ok": ok,
                "error": error,
                "latency_ms": round(dt_ms, 1),
                "output_chars": len(out),
                "within_max_chars": within,
                "first_200": out[:200],
                "max_chars": MAX_CHARS,
            })

            status = "OK" if ok else "ERROR"
            print(f"[{status}] {name}  {dt_ms:.1f}ms  out={len(out)}ch "
                  f"within_max_chars={within}  error={error}")
            if out:
                print(f"    first200: {out[:200]!r}")

            # Capture an id from recall output for the `read` call.
            if name == "recall" and ok and recall_id is None:
                m = re.search(r"\d+\.\s*\[([^\]]+)\]", out)
                if m:
                    recall_id = m.group(1)
                    print(f"    -> will read id {recall_id!r}")

    # --- write machine-readable results ---
    RESULTS_PATH.write_text(json.dumps({
        "url": args.url,
        "total_context_tokens": round(total_ctx_tokens, 1),
        "tools": tool_meta,
        "any_error": any_error,
        "results": results,
    }, indent=2))

    print()
    print("=== summary ===")
    n_ok = sum(1 for r in results if r["ok"])
    print(f"calls: {len(results)}  ok: {n_ok}  errors: {len(results) - n_ok}")
    print(f"total context tokens (description+schema): {total_ctx_tokens:.1f}")
    if any_error:
        print("SMOKE TEST FAILED: one or more calls errored", file=sys.stderr)
        return 1
    print("SMOKE TEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
