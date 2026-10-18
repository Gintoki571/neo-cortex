# START HERE: how to record the Neo-Cortex demo video

This is the only file you need. The other files in `demo/` are tools this guide uses; you never have to open them.

**What the video must do (about 5 minutes):** show that the project really works, explain it so a beginner understands, name the three tracks, and say that AI coding tools were used. Judges watch many videos, so keep it calm, simple and honest.

**How you will record:** you switch between three windows (slides, terminal, FalkorDB Browser) and talk. One short clip per scene, then join the clips. If you stumble, redo only that clip.

---

## Part 1. Preparation (about 20 minutes, camera off)

| # | What you do | Why | What it does |
|---|---|---|---|
| 1 | Close other apps, browsers, and any other Claude Code or OpenCode window. Run `ss -ltn \| grep -E ':(8765\|6399)'` (it must print nothing) and `nvidia-smi` (memory used should be tiny). | The demo needs the graphics card (about 2 GB) and two network ports. Another background copy of Neo-Cortex would block them and force a slow fallback. | Makes sure the demo is fast and the timings you quote are real. |
| 2 | `cd ~/neo-cortex && demo/setup.sh` (wait about 2 minutes until it prints `ready`). | The video needs a clean demo company ("Pellucid Pay", fictional) already loaded. | Starts Neo-Cortex, loads 102 fictional company documents into a fresh FalkorDB graph, and saves a snapshot so you can reset later. |
| 3 | Start the FalkorDB Browser (see box below). Log in with host `127.0.0.1`, port `6399`, username `default`, no password, then pick graph `neo_default`. Close the "What's new" popup. Set dark theme and browser zoom 110-125%. | The Browser draws the graph as dots and lines: the most convincing picture for judges. | A web page on your own computer that shows what is inside FalkorDB. |
| 4 | Open the slides: `file:///home/bindesh/neo-cortex/demo/slides/index.html` in a browser window. Press `F` for fullscreen. Keys: Right/Space = next, Left = back, `0`-`9` = jump to slide. | Slides carry the pictures and analogies so you do not have to explain everything with code. | An animated deck, one idea per slide. Each press of Right reveals the next part. |
| 5 | Open a terminal: dark theme, font size 18 or bigger, then `cd ~/neo-cortex && source demo/env.sh && alias neo=$NEO && clear`. | Judges must be able to read the text. `env.sh` points the commands at the demo database. | Prepares the terminal. |
| 6 | Open OBS Studio: scene "Screen capture (PipeWire)", 1920x1080, 30 fps, MP4, microphone on, desktop audio off. Do Not Disturb on. Record 10 seconds and play it back. | Catches bad audio or private notifications before the real take. | Records your screen and voice. |

**Starting the Browser (step 3), copy and paste:**
```
# one time only (skip if the folder exists):
mkdir -p /tmp/claude-1000/browser-work && git clone --depth 1 https://github.com/FalkorDB/falkordb-browser /tmp/claude-1000/browser-work/falkordb-browser && cd /tmp/claude-1000/browser-work/falkordb-browser && npm ci --no-audit --no-fund
# every time:
cd /tmp/claude-1000/browser-work/falkordb-browser
AUTH_URL=http://127.0.0.1:3000/ AUTH_SECRET="$(openssl rand -hex 32)" ENCRYPTION_KEY="$(openssl rand -hex 32)" ALLOWED_ORIGINS=http://127.0.0.1:3000 npm run dev -- -H 127.0.0.1 -p 3000
```
Then open http://127.0.0.1:3000. (The Browser source is third-party code; it runs only on your own computer.) If it fails, record scene 1 and 3 with the terminal only; the story still works.

**Important rules while recording:** record the scenes in order (scene 6 shows something added in scene 3). To retake everything from the start, run `demo/reset.sh`. Do not run `demo/teardown.sh` between takes (the demo data can be lost; if that happens run `demo/setup.sh` again). Never read ids like `mem_...` aloud.

---

## Part 2. The nine scenes

How each scene is laid out: **Screen** (what the viewer sees), **Do** (your exact steps), **Why**, **What it does**, **Say** (what to talk about, with a beginner-friendly example you can use in your own words).

Terminal scenes use the guided player: `demo/video_runner.sh N`. It prints a title, then waits. Press ENTER, it types the command, press ENTER again, it runs it. So you never mistype and you control the speed.

### Scene 1: The problem (0:00-0:35)
- **Screen:** slide 1, then the terminal, then the FalkorDB Browser.
- **Do:** show slide 1 (press Right until the picture is complete). Terminal: `demo/video_runner.sh 1` (it runs `neo status`). Switch to the Browser, paste this query and run it:
  `MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p, r, s`
- **Why:** judges need the problem and a first picture in 30 seconds.
- **What it does:** `neo status` prints how much is stored (102 documents, 136 pieces of text, 134 things). The Browser query draws who owns the "session cache" (a software component): dots for people and the team, lines for ownership, with dates.
- **Say (example):** "An AI assistant is great for one afternoon, then it forgets everything. A company is no better: the facts about one piece of software are scattered over tickets, chats and documents. Imagine a detective's board: every person or service is a card, every relationship is a string between cards. That is a knowledge graph. Neo-Cortex keeps the whole board in one database, called FalkorDB, so nothing is forgotten. Here is the real board: these are the people who owned this component, and when."

### Scene 2: One graph, three jobs, no bills (0:35-1:10)
- **Screen:** slide 2, then the terminal (`neo --help`).
- **Do:** show slide 2 (press Right twice). Terminal: `demo/video_runner.sh 2`.
- **Why:** this is the cost and architecture pitch, the thing that makes the project different.
- **What it does:** `neo --help` lists the commands an agent can use (recall, ask, who, impact, timeline, remember, dream...). The slide shows the three jobs and the two numbers: about 26 thousandths of a second per reading, about 2 GB of graphics memory.
- **Say (example):** "One graph does three jobs: an agent's long-term memory, a company's brain built from its documents, and answers to questions that need several steps. An agent can use it through fifteen ready-made tools, using a standard called MCP, or by typing the `neo` command. And there is no big AI model inside. Two small programs run on your own computer: one reads text, the other turns text into numbers that capture meaning. So there is no bill per question, no internet needed, and your data never leaves your machine. The thinking is done by the agent that calls it. It is like using a calculator instead of hiring a consultant for every question."

### Scene 3: How a document becomes a graph (1:10-2:00)
- **Screen:** slide 3, the terminal, then the Browser.
- **Do:** show slide 3 (Right until complete). Terminal: `cat demo/docs/handover-note.md` so viewers see the four sentences, then `demo/video_runner.sh 3` (runs `neo ingest --wait demo/docs/handover-note.md`; takes under a second). Browser: run
  `MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)-[:MENTIONS]->(e:Entity) WHERE d.path ENDS WITH 'handover-note.md' RETURN d, c, e LIMIT 20`
- **Why:** it shows an ordinary file becoming structured knowledge, live, with no human labelling and no big model.
- **What it does:** the note is cut into pieces, a small reading program (GLiNER) picks out the people, services and teams and the links between them, and everything is written into the graph. Expected output: `documents 1, chunks 1, mentions 6, rels 2`. The Browser draws the note and its six things.
- **Say (example):** "A file goes in. It is turned into plain text and cut into small pieces. Each piece gets meaning numbers, like GPS coordinates for sentences: similar sentences land close together. Then a small reading program, called GLiNER, acts like a highlighter: it marks the people, the services and the teams, and how they are linked. That is extraction. It also asks of each sentence: is this a fact, a maybe, a denial, or a plan? That is classification. All of it becomes cards and strings in FalkorDB, in less than a second."

### Scene 4: The judge who writes down every verdict (2:00-2:35)
- **Screen:** slide 4, then the terminal.
- **Do:** show slide 4 (Right until complete). Terminal: `demo/video_runner.sh 4` (three commands: the two relationships that were stored, `neo who "invoice-export-service"`, and the saved verdict record).
- **Why:** this proves the system does not make things up: a sentence that says "does NOT own" cannot turn into "owns".
- **What it does:** the note contained four claims. Only two became links, both marked `fact` with a probability (0.9881 for "Priya Nair owns..."). The denial ("Mateo Alvarez does not own...") and the "might move next quarter" were not stored as current ownership, so `neo who` lists only Priya. The last command shows a saved verdict `{"same": 0.8433, "different": 0.1567}`.
- **Say (example):** "Here is the clever part. The reading program does not write a paragraph, it gives a probability, like a weather forecast: ninety-eight percent sure this is a fact. Our note also said Mateo does not own the service, and that the service might move next quarter. Neither became an ownership link; the denial is thrown away, and a maybe is never treated as a current fact. Only the real owner is listed. When the program is unsure whether two names are the same thing, it gives its odds, here eighty-four percent, and the verdict is saved in the graph, so the same judgment is reused instead of asked again. It is like a judge who writes down every verdict. This idea comes from a project called pg-jev (github.com/realZachi/pg-jev), and we use it inside FalkorDB."

### Scene 5: An agent can write straight into the graph (2:35-2:55)
- **Screen:** slide 5, then the terminal.
- **Do:** show slide 5. Terminal: `demo/video_runner.sh 5` (one `neo remember ...` command; it prints `created ...` and `edge ... created`, and the time, about 0.15 seconds).
- **Why:** the reading program is for documents nobody has read. When the agent just did the work, it already knows the facts, so it can write them directly: faster and exact.
- **What it does:** stores a memory with named things and a relationship (Mateo Alvarez works on billing reconciliation) without running the reading program.
- **Say (example):** "The reading program is for documents nobody has read yet. But when an agent has just finished a job, it already knows the facts. So it can write them straight into the graph, naming the cards and the string itself. That skips the reading step, so there is nothing to misread, and it takes a fraction of a second: about 0.15 seconds, compared with about 0.67 seconds to read a document. It is the difference between dictating a note and handing someone a stack of paper to read."

### Scene 6: Four searches, one answer (2:55-4:00)  *(the most important scene)*
- **Screen:** slide 6, then the terminal.
- **Do:** show slide 6 (Right until complete). Terminal: `demo/video_runner.sh 6` (five commands: `recall`, `neo impact ledger-service`, `connect` between two people, `neo who "session cache"`, `neo timeline "session.ttl_seconds"`). Pause on each output and point with the mouse.
- **Why:** this is the main claim: the graph does work that plain text search cannot.
- **What it does:** `recall` answers a question and tags each result with which searches found it (`vector#1, bm25#1, graph#1`). `impact` lists what breaks if `ledger-service` stops (4 services depend on it) and which owners to call, including Priya from the note you just added. `connect` prints the chain of links between two people (Olivia Hartmann, owner of reporting-service, and Elif Yildiz, owner of ledger-service). `who` shows the current owner and a former owner with an end date. `timeline` shows a setting that changed on dated days.
- **Say (example):** "How do we find things? FalkorDB does four kinds of searching and merges them into one answer: by words, by meaning, by connections, and by time. Think of four detectives: one matches words, one understands meaning, one follows the strings between things, one knows the dates. The tags after each result say which detective found it. Words and meaning are what any search tool does. The star is connections. Starting from the things in your question, the graph follows the strings. It can find the fewest steps between two people. And it can answer: if this piece of software stops working, what is affected? It walks the 'depends on' strings backwards, and tells you which owners to call. We measured it: on questions about what is affected when something fails, the graph gives the full answer eighty percent of the time, plain text search twenty percent. Following connections is exactly what a text search cannot do. Time works too: here the owner is marked former, with an end date."

### Scene 7: Memory that tidies itself (4:00-4:25)
- **Screen:** slide 7, then the terminal.
- **Do:** show slide 7. Terminal: `demo/video_runner.sh 7` (four commands: two notes "retry limit is 3 attempts" and "... 5 attempts", then `neo dream`, then a query showing the log record).
- **Why:** agent memory has to stay clean over weeks; this shows it maintaining itself (track 02).
- **What it does:** the second note makes Neo-Cortex print a `conflicts:` warning because it clashes with the first (same subject, different number). `neo dream` runs the tidy-up: it merges duplicates, promotes repeated notes, fades old ones, flags clashes, and writes a log record. Expected: `merged 0, promoted 0, decayed 0, conflicts 2` (the exact count may differ by one; say "conflicts flagged", not the number).
- **Say (example):** "Memories need tidying, and nobody likes chores, so the graph sleeps. One command, `neo dream`, tidies up: identical notes are combined, something remembered across three separate sessions is promoted from 'this happened' to 'this is true', old unused notes slowly fade (nothing is deleted), and notes that disagree are flagged for the agent to settle. We told it the retry limit is three, then five. It noticed the clash, flagged it, and wrote a log record. Nothing needed merging today, because repeated notes are already combined when they are written. The idea comes from a research project called Dream-RSI (github.com/zhengkid/Dream-RSI); we built a simple, repeatable version."

### Scene 8: Tuning that cannot fool itself (4:25-4:45)
- **Screen:** slide 8, then the terminal.
- **Do:** show slide 8. Terminal: `demo/video_runner.sh 8` (prints one line from a saved result file).
- **Why:** judges respect honest results; a rejected idea shown proudly beats a suspiciously perfect one.
- **What it does:** prints the search settings the tuner proposed, its score on practice questions (0.752 against 0.648 for the current settings), the small drop on unseen questions (-0.01875) and `False` (not accepted). The tuner was run earlier; this only reads its result.
- **Say (example):** "Could the search settings be tuned automatically? We built the rule that makes that safe. It is like studying with practice questions and then sitting a new exam: you only keep the new study method if you also do better on the exam you have never seen. The new settings looked better on the practice questions, 0.65 up to 0.75, then did slightly worse on the unseen ones, so the rule rejected them and the old settings stay. That 'no' is the feature working: a check that cannot be fooled. The idea is from a research project called RRSI (github.com/google-research/rrsi, arXiv 2609.24972)."

### Scene 9: The honest close (4:45-5:10)
- **Screen:** slide 9, then the GitHub page and the explainer page.
- **Do:** show slide 9. Open https://github.com/Gintoki571/neo-cortex (and the explainer page if you enabled GitHub Pages).
- **Why:** honesty is the last impression, and rule 11 requires you to disclose AI tool use.
- **What it does:** shows what you tried and did not adopt (`eval/flags.md`), where the repo and explainer are.
- **Say (example):** "One more thing: what we measured and did not adopt. We tried seven more ideas for searching and for merging names, and none beat our default across both of our test collections, so they stay switched off. Where the graph only ties plain text search, we say so. The numbers, the code and a visual explainer are in the public repository. Neo-Cortex was built with Claude Code and other AI coding agents; I directed, reviewed and verified the work, and the system itself contains no big language model. One graph, three jobs: agents that act on connected data, agent memory, and a company brain. Neo-Cortex: the detective's board that never forgets."

---

## Part 3. Words to avoid, and what to say instead

| Instead of | Say |
|---|---|
| knowledge graph | detective's string board (cards = things, strings = relationships); name the term once |
| embedding / vector | meaning numbers, like GPS coordinates for sentences |
| BM25 | searching by words |
| rank fusion | merging four searches into one answer |
| entity resolution | deciding whether two names are the same thing |
| LLM | a big language model (the thinking stays with the agent) |
| MCP | "a standard way for agents to plug in" (say the name once) |

## Part 4. If something goes wrong

- **A command prints something different:** stop, do not improvise. Run `demo/reset.sh`, redo that scene. Note it and tell me.
- **A scene went badly:** just redo that scene's clip (a 20-60 second clip is easy to redo).
- **Browser will not start:** record scenes 1 and 3 with the terminal only.
- **Everything is slow, or `setup.sh` says "falling back to cpu":** something else uses the graphics card. Close it and run `demo/setup.sh` again; slow CPU timings would make your 0.15 s and 0.67 s numbers wrong.

## Part 5. After recording, then submit

1. Join the clips (Kdenlive or Shotcut; or `ffmpeg -f concat -safe 0 -i clips.txt -c copy neo-cortex-demo.mp4` with one line `file '/path/clip.mp4'` per clip). Export H.264 MP4, 1080p, about 5 minutes.
2. Upload to YouTube as **Unlisted** (or Loom); open the link in a private window to confirm it plays.
3. Stop everything: `demo/teardown.sh`, then Ctrl-C in the Browser window.
4. In the submission form: name **all three tracks** (01 Agents that act on connected data, 02 Agent memory and coordination, 03 Company brain); paste the project text from `docs/submission.md`; add the repo link https://github.com/Gintoki571/neo-cortex, the video link, and the explainer link; the AI-use disclosure is in the README and in scene 9.
5. Before pressing Submit: repo opens without logging in; README shows your team name; video link works.
