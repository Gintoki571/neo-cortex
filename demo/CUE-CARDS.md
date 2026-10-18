# Neo-Cortex video cue cards

## Before you start
1. Free ports `8765` and `6399`; check the GPU with `nvidia-smi`.
2. Run `demo/setup.sh` and wait for the fresh database.
3. Start the FalkorDB Browser using the recipe in `BROWSER.md`.
4. Log in to `127.0.0.1:6399`, graph `neo_default`; dismiss the popup.
5. Set the Browser to dark theme and zoom 110–125%.
6. Open `file:///home/bindesh/neo-cortex/demo/slides/index.html`.
7. Set the terminal dark, font 18+, then source `demo/env.sh` and clear it.
8. Open OBS with the screen-capture scene and microphone on.
9. Make a short test recording; confirm text, voice, and no private notices.

## S0 — Title
**SCREEN** — slide S0 / terminal runner command: none / Browser query: none  
**DO** — Press `F` for fullscreen; pause before speaking.  
**SAY** — “Neo-Cortex: the detective’s board that never forgets.”  
**CHECK** — The title fills the screen and is readable.  
**IF WRONG** — Press `0`, then `F`, and record this clip again.

## S1 — The problem and the board
**SCREEN** — slide S1 / terminal `demo/video_runner.sh 1` / Browser query: `MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'}) RETURN p, r, s`  
**DO** — Show the status counts; switch to the Browser; run the query.  
**SAY** — “An agent can forget yesterday’s work, and a company’s facts can be scattered everywhere. Picture a detective’s string board: blue cards are things and orange strings are relationships. Neo-Cortex keeps that board in FalkorDB so you can see it.”  
**CHECK** — Counts appear, then the Browser shows people and a team linked to the session cache.  
**IF WRONG** — Restart the query and capture the status and graph as two short clips.

## S2 — One graph, three jobs
**SCREEN** — slide S2 / terminal `demo/video_runner.sh 2` / Browser query: none  
**DO** — Show the slide; switch to the terminal; press `ENTER` when the runner pauses.  
**SAY** — “One graph does three jobs: agent memory, a company brain, and questions that need several steps. Fifteen ready-made tools and the `neo` command let agents reach it. Small local programs read text and make meaning numbers, so there is no per-question bill and the thinking stays with the calling agent.”  
**CHECK** — The three jobs, local setup, and no-big-model message are visible.  
**IF WRONG** — Return to slide S2 and rerun `demo/video_runner.sh 2`.

## S3 — A document becomes a graph
**SCREEN** — slide S3 / terminal `demo/video_runner.sh 3` / Browser query: `MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)-[:MENTIONS]->(e:Entity) WHERE d.path ENDS WITH 'handover-note.md' RETURN d, c, e LIMIT 20`  
**DO** — Show the note; press `ENTER` for ingest; switch to the Browser and run the query.  
**SAY** — “A file is cut into small pieces and given meaning numbers. A small reading program picks out people, services, teams, and their links. It keeps facts, not maybes or denials, as blue cards and orange strings.”  
**CHECK** — The ingest says one document, one chunk, six mentions, and two relationships; the Browser shows the note and its cards.  
**IF WRONG** — Reset the demo, then rerun scene 3 from its first pause.

## S4 — The judge who records verdicts
**SCREEN** — slide S4 / terminal `demo/video_runner.sh 4` / Browser query: none  
**DO** — Press `ENTER` through the owner and verdict commands; point slowly at `fact` and the probabilities.  
**SAY** — “The reader gives each link a confidence, like a weather forecast. The denial is rejected and the maybe is not treated as today’s fact. When two names may be the same, the green verdict is saved so the same judgment can be reused.”  
**CHECK** — Only Priya owns the service, the denied Mateo line is absent, and the saved verdict is visible.  
**IF WRONG** — Rerun `demo/video_runner.sh 4` and wait for each output to settle.

## S5 — An agent writes directly
**SCREEN** — slide S5 / terminal `demo/video_runner.sh 5` / Browser query: none  
**DO** — Press `ENTER`; let the `neo remember` command finish; point at the created card and string.  
**SAY** — “An agent that already knows a fact can write it straight into the graph. It names the blue cards and orange string itself, so no reader can misread it. That direct write takes a fraction of a second.”  
**CHECK** — A typed memory and relationship are marked created, with the direct-write timing visible.  
**IF WRONG** — Reset before rerunning scene 5 so the relation is new.

## S6 — Four searches at once
**SCREEN** — slide S6 / terminal `demo/video_runner.sh 6` / Browser query: none  
**DO** — Press `ENTER` for recall, impact, connect, who, and timeline; point at channel tags and the path.  
**SAY** — “The graph searches by words, meaning, connections, and time, then merges the results. Orange strings reveal a path between people and show what breaks if a service fails. Purple time keeps a former owner and earlier settings from being mistaken for today’s truth.”  
**CHECK** — Recall tags, the Olivia-to-Elif path, former owner, and dated timeline are visible.  
**IF WRONG** — Reset and rerun scene 6; keep the handover note from scene 3 in the same take.

## S7 — Memory tidies itself
**SCREEN** — slide S7 / terminal `demo/video_runner.sh 7` / Browser query: none  
**DO** — Press `ENTER` through both memories, `neo dream`, and the final query; point at the red conflict.  
**SAY** — “The graph sleeps and tidies memories: repeats are combined, old notes fade without deletion, and disagreements are flagged. Here, three and five attempts become a red conflict, and the run writes a record of the check. This is a small, repeatable version of the sleeping idea from Dream-RSI.”  
**CHECK** — The conflict and the `DreamRun` record are visible; nothing is silently deleted.  
**IF WRONG** — Reset and rerun scene 7 from the first memory.

## S8 — Tuning that cannot fool itself
**SCREEN** — slide S8 / terminal `demo/video_runner.sh 8` / Browser query: none  
**DO** — Press `ENTER`; point at the practice score, held-out change, and `False`.  
**SAY** — “The search weights were tried on one set of questions and checked on questions they never saw. They looked better first, then did worse on the unseen set, so the green gate rejected them. That ‘no’ means the safety check is working.”  
**CHECK** — `0.752`, `0.648`, the negative held-out change, and `False` are visible.  
**IF WRONG** — Rerun scene 8 without editing the result file.

## S9 — The honest close
**SCREEN** — slide S9 / terminal `demo/video_runner.sh 9` / Browser query: public repository and explainer pages  
**DO** — Show the rejected-ideas table; switch to the repository and explainer; return to the closing slide.  
**SAY** — “We tried seven more ideas and kept them off when they did not beat the defaults across both test collections. Where the graph ties plain search, we say so. One graph, three jobs: connected data for agents, memory, and a company brain.”  
**CHECK** — The rejected ideas, public pages, and AI-use sentence are readable.  
**IF WRONG** — Return to slide S9 and record the close again, without improvising new claims.

## After
1. Stop the demo and Browser; check for a stray daemon.
2. Cut and join the clips, export the final video, and watch it once.
3. Upload it as unlisted and test the link in a private window.
4. Complete the submit checklist, including the README `Team:` line.
