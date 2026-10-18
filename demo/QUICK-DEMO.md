# Quick demo: ONE silent recording, nothing to say, nothing to press

`demo/silent_demo.sh` plays the whole demo by itself: a caption explains each step in plain words, the command types itself, runs, and stays on screen long enough to read. You only start the screen recorder, start the script, and stop the recorder. About 5 minutes. No audio, no OBS, no editing.

The demo database is already built and clean (102 fictional company documents). If you restart your computer or run the demo once, see "Retake" below.

## Steps (5 minutes of work)

1. Open ONE terminal, dark theme, font size 20 or bigger, maximised (fills the screen). Run:
   ```
   cd ~/neo-cortex && clear
   ```
2. Start Spectacle, choose **Record** and **Screen** (or just this terminal window), click **Start**. Wait 2 seconds.
   (Alternative from a second terminal: `spectacle -R screen`, if the Spectacle window gives trouble.)
3. In the big terminal run:
   ```
   demo/silent_demo.sh
   ```
   Leave your hands off the keyboard. Do not scroll. It shows, in order: the project card, what is stored, a new document being added, the verdict for each link (a denied claim is dropped), an agent writing directly, four searches (what breaks if a service stops, how two people are connected, who owned something and until when), memory tidying, the tuning result, and a final card (AI disclosure, repo link, "Team: bindesh (solo)").
4. When the last card ("Neo-Cortex: one graph, three jobs") has been on screen for about 8 seconds, stop the Spectacle recording.
5. Find the file: `ls -t ~/Videos | head` (Spectacle saves there). Play it once to check it is readable. If the host wants MP4: `ffmpeg -i ~/Videos/FILE.webm -c:v libx264 -crf 23 ~/neo-cortex-demo.mp4` (otherwise upload the .webm as it is).
6. Upload as **Unlisted** to YouTube (or any host the form accepts), test the link in a private window.
7. Submit the form (deadline 00:14 local = 18:29 UTC): name all three tracks (01 Agents that act on connected data, 02 Agent memory and coordination, 03 Company brain); paste the text from `docs/submission.md`; add the repo link https://github.com/Gintoki571/neo-cortex and the video link.

It is fine if the video is not perfect. It shows the real project working, which is what the judges asked for.

## If something goes wrong
- **The script says "demo daemon not running":** run `demo/setup.sh`, wait for `ready` (about 2 minutes), then start again from step 2.
- **Retake (the script changes the database: it adds the note and a few memories):** stop the old demo and build a fresh one:
  ```
  demo/teardown.sh; kill -9 $(ss -ltnp | grep ':6399' | grep -o 'pid=[0-9]*' | cut -d= -f2) 2>/dev/null; demo/setup.sh
  ```
  (the `kill -9` clears a leftover database process that can block the restart.) Do not use `demo/reset.sh`; it can fail.
- **Slow output or "falling back to cpu" in setup:** another program is using the graphics card; close it and run setup again, otherwise the recording still works but runs slower.
- **Only a very short check run (no recording):** `demo/silent_demo.sh --fast` (pauses shortened; it also changes the database, so rebuild before the real take).

## Cleanup after you submit
`demo/teardown.sh`, then close the FalkorDB Browser terminal with Ctrl-C.
