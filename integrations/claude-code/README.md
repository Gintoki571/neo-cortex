# Neo-Cortex for Claude Code

Memory that works even when the agent forgets to call `remember`: hooks inject the brief at session start and send the
transcript to the daemon at session end and before compaction.

1. **Start the daemon** (the only process that may open the DB; keep it running, loopback only):
   `uv run neo serve --warm` (MCP at `http://127.0.0.1:8765/mcp`, hook API at `/api`, health at `/health`).
2. **Install the CLI where hooks can find it** (a hook must start in milliseconds, so no `uv run` per call):
   `uv tool install --editable .` and check `neo --version`. `neo install-claude` writes the venv's absolute path instead if `neo` is not on PATH.
3. **Connect the MCP tools**: `claude mcp add --transport http --scope user neo-cortex http://127.0.0.1:8765/mcp`
   (`neo install-claude` prints this command; it never runs it).
4. **Enable the hooks**: `neo install-claude --scope user --yes` merges them into `~/.claude/settings.json`
   (`--scope project` for `./.claude/settings.json`; without `--yes` it only prints). Or copy `settings.hooks.json` by hand.

What the hooks do (`neo hook <event>`, hook JSON on stdin):

| Event | Action |
| --- | --- |
| `SessionStart` | prints the brief for the project (basename of `cwd`) as `additionalContext` |
| `SessionEnd`, `PreCompact` | asks the daemon to ingest `transcript_path` in a background thread and returns at once |

Hooks never fail the session: with no daemon they exit 0 silently. Agent identity is `$NEO_AGENT` or `claude-code:<session_id[:8]>`;
`$NEO_DAEMON_URL` points the CLI at another daemon. Check with `neo status`; query by hand with `neo recall "..."`.
