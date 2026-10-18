# Recording the demo video: step by step

Target: about 5 minutes, one clip per scene, screen plus your voice. The scenes, exact commands, what to point at and the voice-over are in [VIDEO.md](VIDEO.md); every output in it was captured for real ([CAPTURE.md](CAPTURE.md)). Showing the FalkorDB Browser: [BROWSER.md](BROWSER.md). This file is only the procedure.

## 0. Before you record (20 minutes, no camera)

1. Free the machine: close browsers, editors and other Claude Code or OpenCode sessions (a Claude Code session can start its own `neo serve` in the background through the installed hooks). Check: `ss -ltn | grep -E ':(8765|6399)'` must print nothing, and `nvidia-smi` should show almost no memory in use. The demo needs about 2 GB of GPU memory and falls back to CPU (slow, so the timings in scene 5 would not be representative).
2. Build the demo database (fresh, about 2 minutes on the GPU): `cd ~/neo-cortex && demo/setup.sh`. It starts a daemon on 127.0.0.1:8765, ingests the synthetic company (never `WORLD.md`) and takes a snapshot.
3. Start the FalkorDB Browser (once; recipe and login in BROWSER.md): host 127.0.0.1, port 6399, graph `neo_default`. Dismiss its "What's new" popup.
4. Terminal: dark theme, font size 18 or larger, 100 columns, `source demo/env.sh`, `alias neo=$NEO`, `clear`; Do Not Disturb on.
5. Rehearse the whole video once with the commands in VIDEO.md. Anything that differs from the "Point at" lines is a bug to tell me about, not to improvise around.
6. Between full takes run `demo/reset.sh` (restores the snapshot, so the handover note and the memories written on camera disappear). Do not run `demo/teardown.sh` between takes: after a teardown and a restart the demo data can be lost (found during the capture); if that happens run `demo/setup.sh` again.

## 1. Screen setup

- Recorder: OBS Studio, scene "Screen capture (PipeWire)", 1920x1080, 30 fps, MP4, microphone on, desktop audio off.
- Make a 10-second test recording and play it back: is the text readable, is your voice clear, is anything personal or any notification on screen?

## 2. Recording

Record scene by scene in the order of VIDEO.md (the scenes share one database: scene 6 shows the handover note from scene 3). A 20-60 second clip is easy to redo. Join the clips with any editor (Kdenlive, Shotcut, or `ffmpeg -f concat`). No music is needed.

## 3. AI use (hackathon rule 11)

Scene 9 says one sentence about it; the README has the full disclosure.

## 4. Export and upload

- Export MP4 (H.264), 1080p, about 5 minutes or less; check the file size against the form's limit.
- Upload to YouTube as **Unlisted** (or Loom) and paste the link into the form. Open the link in a private window to confirm it plays without logging in.

## 5. Before pressing Submit

- [ ] Public repo opens without logging in: https://github.com/Gintoki571/neo-cortex
- [ ] README: the `Team:` line is filled in (it was an empty placeholder)
- [ ] README top shows tracks, setup, data model, Cypher queries and graph algorithms
- [ ] Explainer link works (GitHub Pages, if you enabled it)
- [ ] Form: name all three tracks (01 Agents that act on connected data, 02 Agent memory and coordination, 03 Company brain)
- [ ] Form text pasted from `docs/submission.md`
- [ ] Video link works in a private window
- [ ] AI-use disclosure present (README section "AI use disclosure")

## 6. Afterwards

`demo/teardown.sh` stops the demo daemon and frees the ports; stop the Browser with Ctrl-C.
