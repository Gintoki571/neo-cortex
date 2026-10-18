# demo

## Purpose

- Demo kit for the hackathon video: a fresh demo DB and daemon, the shot lists (`VIDEO.md`, `SCRIPT.md`) for the three tracks, a prepared agent transcript, the Claude Code prompts and MCP config, and a neo CLI replay of the whole story.

## Ownership

- Owns everything under `demo/`. Read-only on `src/`, `data/`, `eval/`: the demo calls the product, it never changes it.

## Local Contracts

- `env.sh` is sourced by every script: demo `NEO_HOME` (`.neo/demo`), DB port `NEO_PORT` 6399, `NEO_DEVICE` (default cuda; `setup.sh` falls back to cpu on OOM), daemon on `127.0.0.1:8765`, pid file `.neo/demo-daemon.pid`, log `.neo/demo-daemon.log`.
- `setup.sh [--public]` builds a fresh DB: only `data/synthetic/{doc,adr,ticket,chat,meeting,session}` (never `WORLD.md` or `manifest.jsonl`), `transcripts/history/*.jsonl` as agent-a's earlier sessions, then a baseline snapshot (`.neo/demo-baseline`). `--public` adds `data/public/falkordb` one file per call (`neo ingest <dir>` times out after 300 s). `reset.sh` restores the baseline; `teardown.sh` stops the daemon and kills only an orphan `redis-server` on the demo DB port. `tool.sh <tool> '<json>'` calls any daemon tool (`connect`, `explore` have no CLI command).
- `run_cli_demo.sh [--pause]` replays the story with neo calls and requires the post-setup state (exits with a message otherwise). `SCRIPT.md` holds the shot list with real, trimmed outputs: re-run `run_cli_demo.sh` and update them when the product output changes.
- `transcripts/agent_a.jsonl` (live session, ingested on camera) and `transcripts/history/` are fictional Pellucid Pay work in Claude Code JSONL form; the story depends on the memory texts they yield (the "not confirmed" and "suggested a 1 percent" semantic memories). Re-check with `neo ingest-session` after changing them.
- `START-HERE.md` is the single guide for the person recording the video (preparation, nine scenes with what to do, why, what it does and what to say with beginner examples, troubleshooting, submission); everything else in this folder is a tool or reference it uses.
- `VIDEO.md` is the current video plan (about 5 minutes, plain language; every output was captured for real in `CAPTURE.md`); `RECORDING.md` is the recording and upload procedure; `BROWSER.md` is the verified recipe for showing the FalkorDB Browser without Docker; `docs/handover-note.md` is the fictional note ingested on camera in scene 3. `slides/index.html` is the animated full-screen slide deck shown between terminal and Browser shots (keys: Right/Space, Left, 0-9, F; one idea per slide; every number comes from VIDEO.md, CAPTURE.md or eval/); `video_runner.sh <scene 1-9> [--fast] [--notes] [--dry]` is the guided terminal player that types each scene's exact commands on ENTER; `CUE-CARDS.md` has one card per scene (screen, do, say, check, if wrong). Keep slides, runner and cue cards in step with `VIDEO.md`. `SCRIPT.md` remains the older 3-4 minute shot list with verified outputs. Re-capture `CAPTURE.md` when product output changes.
- `prompts/` are the exact Claude Code prompts, `mcp.json` is the http MCP config. Generated and untracked: `claude-settings.json`, `work/` (project dirs whose basename is the hook's project name).

## Work Guidance

- Questions in the script must be verified against the demo DB first. Known weak spots (sparse `REL` edges, 240-character snippets, `timeline "session cache"`) are listed at the end of `SCRIPT.md`; avoid them on camera.

## Verification

- `demo/setup.sh && demo/run_cli_demo.sh` exits 0 and prints no error; `demo/teardown.sh` leaves no `redis-server` on port 6399.

## Child DOX Index

- None.
