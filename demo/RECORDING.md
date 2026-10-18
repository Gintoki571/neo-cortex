# Recording the Neo-Cortex demo

The words are in [VIDEO.md](VIDEO.md). The per-scene actions are in
[CUE-CARDS.md](CUE-CARDS.md). Record one clip per scene, in order, on one
database.

## Screen layout

- **Slides:** open `file:///home/bindesh/neo-cortex/demo/slides/index.html` in a
  browser, use fullscreen, and keep the large dark slides readable at 720p.
- **Terminal:** use a dark theme, font 18 or larger, and the guided
  `demo/video_runner.sh` script.
- **Browser:** use the FalkorDB Browser from [BROWSER.md](BROWSER.md), dark
  theme, and zoom 110–125%. Connect to `127.0.0.1`, port `6399`, graph
  `neo_default`.
- Switch windows with `Alt+Tab`. Pause for 1 second after every switch before
  speaking. Move the mouse slowly when pointing.

## Before recording

1. Close unrelated apps and sessions. Check that ports `8765` and `6399` are
   free with `ss -ltn | grep -E ':(8765|6399)'`, and check `nvidia-smi`.
2. Run `demo/setup.sh`; it builds the fresh database and starts the daemon.
3. Start the Browser as described in `BROWSER.md`, log in, and dismiss its
   first-run popups.
4. Prepare the terminal with `source demo/env.sh`, `alias neo=$NEO`, and
   `clear`. Turn on Do Not Disturb.
5. Set up the slides and OBS, then make a short test recording.

## OBS and visual rules

- Use OBS Studio, scene “Screen capture (PipeWire)”, 1920x1080, 30 fps, MP4.
- Record the microphone; turn desktop audio off. Check the test for clear voice,
  readable text, and no private notifications.
- Show one idea per screen. Blue means cards/things, orange means
  strings/relationships, green means verdicts/safety checks, red means
  warnings/rejected items, and purple means time.
- Do not leave command output on screen longer than needed. Do not cover text
  with the cursor. Pause, point, and speak plainly.

## Recording and editing

Run scenes 1–9 in the order of [VIDEO.md](VIDEO.md); scene 6 depends on the
handover note from scene 3. Between full takes run `demo/reset.sh`. Do not run
`demo/teardown.sh` between takes: a teardown followed by a restart can lose the
demo data, so run `demo/setup.sh` again if that happens.

For a verified local `ffmpeg`, put one line per clip in `clips.txt`,
such as `file '/absolute/path/scene-1.mp4'`, then run:

```bash
ffmpeg -f concat -safe 0 -i clips.txt -c copy neo-cortex-demo.mp4
```

Kdenlive or Shotcut is fine instead. Cut pauses and mistakes, but keep the
voice and the screen change together. No music is needed.

## Export and submit

- Export H.264 MP4, 1080p, about 5 minutes or less; check the form’s size limit.
- Upload to YouTube as **Unlisted** (or Loom), then test the link in a private
  window without logging in.
- [ ] Public repo opens without logging in:
  `https://github.com/Gintoki571/neo-cortex`
- [ ] README: the `Team:` line is filled in.
- [ ] README top shows tracks, setup, data model, Cypher queries, and graph algorithms.
- [ ] Explainer link works (GitHub Pages, if enabled).
- [ ] Form names all three tracks: 01 Agents that act on connected data,
  02 Agent memory and coordination, 03 Company brain.
- [ ] Form text is pasted from `docs/submission.md`.
- [ ] Video link works in a private window.
- [ ] AI-use disclosure is present in the README.

## After

Run `demo/teardown.sh`, stop the Browser with `Ctrl-C`, and check for a stray
daemon or occupied demo port. Keep the final export and the unlisted link
ready for submission.
