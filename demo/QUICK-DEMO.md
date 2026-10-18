# Quick demo: record a working demo in about 20 minutes, no OBS needed

Goal: about 2.5 to 3 minutes showing the project working, with your voice. You do not need slides, the Browser, or editing software. The demo database is already running (check with `neo status`).

## What you need (all already installed)
- **Spectacle** records the screen (it cannot record sound, so we record your voice separately).
- **pw-record** records your microphone (tested: it works on this machine).
- **ffmpeg** glues voice and screen together at the end.

## Step 1: prepare the terminal (2 minutes)
Open ONE terminal window, dark theme, font size 18 or bigger, maximised. Run:
```
cd ~/neo-cortex && source demo/env.sh && alias neo=$NEO && clear
```
Open a SECOND small terminal (you will not film it) for the microphone.

## Step 2: start recording (1 minute)
1. In the small terminal: `pw-record --target alsa_input.pci-0000_00_1f.3.analog-stereo ~/voice.wav` (it starts recording your voice; leave it running).
2. Start Spectacle, choose the **Record** mode, **Screen** (or the terminal window only), and click **Start**. Wait 3 seconds, then speak.

## Step 3: do this and say this (about 3 minutes)
Press ENTER twice for each command (first ENTER types it, second runs it). Speak while it runs. Short sentences. Pause one second after each output.

| You run | You say (example, put it in your own words) |
|---|---|
| `demo/video_runner.sh 1 --fast` | "This is Neo-Cortex. AI assistants forget everything between sessions, and a company's knowledge is scattered across documents and chats. Neo-Cortex keeps all of it in one graph database, FalkorDB. This is a fictional company, Pellucid Pay: 102 documents, already in the graph." |
| `demo/video_runner.sh 3 --fast` | "Now I add a new document. A small reading program picks out the people, services and teams and how they are linked. It took under a second: six things found, two links created. There is no big AI model inside, so no per-question bill." |
| `demo/video_runner.sh 4 --fast` | "Each link has a verdict and a probability. The note also said Mateo does not own this service, and that it might move next quarter. Neither became an ownership link: a denial is dropped and a maybe is never treated as a fact. Only the real owner, Priya, is listed. This idea comes from a project called pg-jev." |
| `demo/video_runner.sh 6 --fast` | "Now the questions. The graph searches by words, by meaning, by connections and by time. The tags show which search found each result. If this service stops, what breaks? Four other services depend on it, and it tells me which owners to call. This path shows how two people are connected. On questions like this the graph gives the full answer 80 percent of the time, plain text search 20 percent." |
| `demo/video_runner.sh 7 --fast` | "Memory tidies itself. I tell it the retry limit is three, then five. It flags the clash, and the dream command tidies the memory and writes a log. This idea is from a research project called Dream-RSI." |

Closing sentence (just talk, nothing to run): "Neo-Cortex covers all three tracks: agents that act on connected data, agent memory, and a company brain. It was built with Claude Code and other AI coding agents; I directed, reviewed and verified the work. The code is at github.com/Gintoki571/neo-cortex."

If a command fails or you stumble badly, press Ctrl-C in the recording terminal, stop both recorders, and start again from Step 2. Do not run `demo/teardown.sh`. To restore the database before a retake: `demo/reset.sh`.

## Step 4: stop and glue (3 minutes)
1. Stop Spectacle recording first (its stop button or the tray icon). Then press Ctrl-C in the small terminal to stop `pw-record`.
2. Run this once (it finds the newest screen recording in `~/Videos` and lines up the voice by the end):
```
cd ~; V=$(ls -t ~/Videos/*.webm ~/Videos/*.mp4 2>/dev/null | head -1); echo "screen: $V"
vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V"); ad=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ~/voice.wav)
ss=$(python3 -c "print(max(0, $ad - $vd))"); echo "voice starts $ss s into the audio"
ffmpeg -y -i "$V" -ss $ss -i ~/voice.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 23 -c:a aac -shortest ~/neo-cortex-demo.mp4
```
3. Play `~/neo-cortex-demo.mp4` and check you can hear yourself and read the text. If the voice is slightly early or late (it is lined up by the end, so it should be within a second), that is fine for this submission.

## Step 5: upload and submit
1. Upload `~/neo-cortex-demo.mp4` to YouTube as **Unlisted** (or any video host the form accepts). Test the link in a private window.
2. In the form: name all three tracks (01 Agents that act on connected data, 02 Agent memory and coordination, 03 Company brain), paste the text from `docs/submission.md`, add the repo link https://github.com/Gintoki571/neo-cortex and the video link.
3. The deadline is 00:14 local time (18:29 UTC). Submit before that; do not wait for a perfect video.

## Cleanup when done
`demo/teardown.sh`, then close the FalkorDB Browser terminal with Ctrl-C.
