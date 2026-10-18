# Recording the demo video: step by step

Target: 3 minutes, one take per scene, screen plus your voice. The scene list, exact commands, what to point at and the voice-over are in [VIDEO.md](VIDEO.md); every output in it was verified in [SCRIPT.md](SCRIPT.md). This file is only the procedure.

## 0. Before you record (15 minutes, no camera)

1. Free the machine: close browsers, editors and anything on the GPU. The demo needs about 1.5 GB of GPU memory and falls back to CPU by itself. Nothing may listen on ports 8765 or 6399.
2. Build the demo database (fresh, takes about 2 minutes on the GPU):
   ```bash
   cd ~/neo-cortex && demo/setup.sh
   ```
   It starts a daemon on 127.0.0.1:8765, ingests the synthetic company (never `WORLD.md`) and takes a snapshot.
3. Rehearse once with the helper: `source demo/env.sh`, then run each command from VIDEO.md. Anything that differs from the "Point at" lines is a bug to tell me about before you record, not to improvise around.
4. Reset between takes: `demo/reset.sh` (restores the snapshot, so the write scenes start clean each time).
5. Scene 2 shows the graph. Safest: `neo cypher "MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p.name, r.valid_from_ms, r.valid_to_ms LIMIT 10"` in the terminal. Optional: FalkorDB Browser (`docker compose up -d falkordb`, http://127.0.0.1:3000) shows the picture, but a Browser inside Docker cannot reach the host's 127.0.0.1:6399 unless the container runs with host networking; I have not verified that setup here, so test it during rehearsal and fall back to the terminal if it fails.

## 1. Screen setup

- Terminal: dark theme, font size 18 or larger (judges watch on small players), 100 columns wide, history cleared (`clear`). Hide notifications (Do Not Disturb).
- Recorder: OBS Studio (Linux), scene = "Screen capture (PipeWire)", 1920x1080, 30 fps, MP4 (Settings, Output, Recording Format mp4), microphone on, desktop audio off.
- Do a 10-second test recording and play it back: is the text readable, is your voice clear, is there any notification or personal tab on screen?

## 2. Recording order (matches VIDEO.md)

| Time | Scene | Notes |
|---|---|---|
| 0:00-0:20 | Problem, `neo status` | say the one-line pitch; do not read the whole VIDEO.md text |
| 0:20-0:40 | One graph, three jobs (Browser or `neo cypher`) | mention 15 MCP tools and the neo CLI |
| 0:40-1:00 | `neo impact ledger-service` | the measured win: 0.80 vs 0.20 |
| 1:00-1:30 | `neo who`, `neo timeline` | ownership is an edge with a validity window |
| 1:30-1:55 | `neo ask`, `connect` | seeds, bridging path, cited evidence |
| 1:55-2:20 | agent writes the graph (`relate --supersede`, `remember --entity/--rel`, `handoff`) | no extractor in the loop |
| 2:20-2:40 | hooks: session end, session start | memory without discipline |
| 2:40-3:00 | the honest close | what we measured and did not adopt; repo link; explainer link |

Record each scene separately (a 20-40 second clip is easy to redo), then join them. Any simple editor works (Kdenlive, Shotcut, or `ffmpeg -f concat`). No music is needed; if you add some, it must be royalty-free.

## 3. What to say about AI use (rule 11 of the hackathon)

One sentence near the end: "Neo-Cortex was built with Claude Code and other AI coding agents; we directed, reviewed and verified the work, and the system itself contains no LLM." The README has the full disclosure.

## 4. Export and upload

- Export MP4 (H.264), 1080p, under 3 minutes if you can; check the file size against the form's limit.
- Upload to YouTube as **Unlisted** (or Loom) and paste the link into the submission form. Open the link in a private window to confirm it plays without logging in.

## 5. Before pressing Submit

- [ ] Public repo opens without logging in: https://github.com/Gintoki571/neo-cortex
- [ ] README top shows tracks, setup, data model, Cypher queries and graph algorithms (all in README.md)
- [ ] Explainer link works (GitHub Pages, if you enabled it)
- [ ] Form: name all three tracks (01 Agents that act on connected data, 02 Agent memory and coordination, 03 Company brain)
- [ ] Form text pasted from `docs/submission.md`
- [ ] Video link works in a private window
- [ ] AI-use disclosure present (README section "AI use disclosure")

## 6. Afterwards

`demo/teardown.sh` stops the demo daemon and frees the ports.
