# FalkorDB Browser, without Docker

This is the verified screen-recording recipe for running the FalkorDB Browser
from source against the Neo-Cortex embedded database. It does not use Docker or
sudo. Keep the Browser bound to loopback: it is a development server and
should not be exposed on a LAN.

## Prerequisites

- Node.js `>=24.0.0` and npm. Verified here with Node `v26.10.0` and npm
  `12.2.0`.
- Python 3.12 with the project environment and `falkordblite` installed. The
  demo database is started separately by the demo setup process.
- The Browser source is kept outside this repository at
  `/tmp/claude-1000/browser-work/falkordb-browser`.

## One-time Browser install

Run these commands once. The clone and its dependencies are untrusted
third-party code; keep them in this dedicated temporary directory.

```bash
mkdir -p /tmp/claude-1000/browser-work
git clone --depth 1 \
  https://github.com/FalkorDB/falkordb-browser \
  /tmp/claude-1000/browser-work/falkordb-browser
cd /tmp/claude-1000/browser-work/falkordb-browser
npm ci --no-audit --no-fund
```

The checkout is Browser `2.7.0`. On this machine `npm ci` took about **43
seconds** and completed successfully. It printed only npm deprecation warnings
and notices that optional install scripts were blocked; no fix was needed.

The source uses `npm run dev` (`next dev`). The production alternatives are
`npm run build` and `npm run start`. The repository's `next.config.js` permits
`127.0.0.1`; pass the host explicitly anyway.

## Start the Browser each time

The Browser needs a session secret and, for a login, a 64-hex-character
`ENCRYPTION_KEY`. Generate a key once if desired and keep it local; the value
below is only an example:

```bash
cd /tmp/claude-1000/browser-work/falkordb-browser
AUTH_URL=http://127.0.0.1:3000/ \
AUTH_SECRET="$(openssl rand -hex 32)" \
ENCRYPTION_KEY="$(openssl rand -hex 32)" \
ALLOWED_ORIGINS=http://127.0.0.1:3000 \
npm run dev -- -H 127.0.0.1 -p 3000
```

For repeated recordings, put stable local values in
`/tmp/claude-1000/browser-work/falkordb-browser/.env.local` instead, and run:

```bash
cd /tmp/claude-1000/browser-work/falkordb-browser
npm run dev -- -H 127.0.0.1 -p 3000
```

Open <http://127.0.0.1:3000>. The dev server was ready in under one second in
the verification run. `NEXTAUTH_URL` is also accepted by the Browser as a
fallback; `AUTH_URL` is the current template name.

## Connect the screen-recording demo

Start the Neo-Cortex demo database first. It owns `127.0.0.1:6399`; do not
start another server on that port. In the Browser login form choose **Manual
Configuration** and enter:

| Field | Value |
|---|---|
| Host | `127.0.0.1` |
| Port | `6399` |
| Username | `default` |
| Password | leave empty |
| TLS | off |

The graph is `neo_default`; select it after signing in. The Browser login
form has Host, Port, Username, Password, and TLS fields. Although the UI help
says localhost credentials may be omitted, the verified local login used
username `default` and an empty password.

Paste these queries into the editor one at a time:

```cypher
MATCH (n) RETURN n LIMIT 100
```

```cypher
MATCH (a)-[r]->(b) RETURN a,r,b
```

```cypher
MATCH (p:Entity)-[r:REL {type:'OWNS'}]->(s:Entity {key:'session cache'})
RETURN p, r, s
```

The final query is the ownership shot requested for the interim recipe.
`demo/CAPTURE.md` section F was not present when this document was written, so
replace the first two queries with the finished section-F queries once that
capture document exists.

## Recording tips

- Use browser zoom **110–125%**.
- Choose the dark theme.
- Hide the left sidebar for the graph shot.
- Set node captions to the `name` property.
- Run the query, wait for the graph count/result to settle, then capture the
  graph rather than the loading state.
- Dismiss the first-run tutorial and the “What's new” dialog before recording.

## Docker alternative (not verified here)

If Docker is available, the requested host-networking alternative is:

```bash
sudo docker run --network host --rm falkordb/falkordb-browser:latest
```

This was **not run or verified**: the Docker daemon was not running, and this
recipe intentionally used no sudo. Host networking makes the container's
Browser available on its configured port; keep the database and Browser on
loopback as appropriate for the recording.

## Stop everything

- In the Browser terminal, press `Ctrl-C`.
- Stop the Neo-Cortex demo with its normal demo teardown command; it owns port
  `6399` and the daemon on `127.0.0.1:8765`.
- Confirm the Browser and any throwaway test server are gone:

```bash
ss -ltn '( sport = :3000 or sport = :6401 )'
```

An empty result means both ports are free. Do not kill processes by name; stop
the terminal that owns each server or use its specific PID.

## Verification record

Verified on 2026-10-18:

- Source clone, README, `package.json`, `.env.local.template`, and
  `next.config.js` were inspected.
- `npm ci --no-audit --no-fund` completed in about 43 seconds.
- No production build was attempted; the verified path is the development
  server. The first login attempt failed because `ENCRYPTION_KEY` was unset;
  restarting with a 64-character hex key fixed it.
- The Browser ran on `127.0.0.1:3000` with `npm run dev -- -H 127.0.0.1
  -p 3000`.
- A throwaway `falkordblite` server was started from the project Python
  environment on `127.0.0.1:6401` in a temporary directory. It contained
  `demo_test` with three `Person` nodes and two `KNOWS` edges.
- Login succeeded with host `127.0.0.1`, port `6401`, username `default`, and
  an empty password after setting `ENCRYPTION_KEY`.
- `MATCH (a)-[r]->(b) RETURN a,r,b` ran successfully. The Browser reported
  **Nodes: 3** and **Edges: 2**, and the graph picture rendered. The captured
  screenshot was `/tmp/claude-1000/browser-work/shot.png`.
- `obscura fetch --eval` and `obscura fetch --screenshot` were used against the
  loopback Browser as requested. This obscura build could fetch and screenshot
  the page but did not expose reliable interactive form controls through
  `--eval`; the login, query, and final screenshot were therefore completed
  with the locally installed Playwright Chromium against the same
  `127.0.0.1:3000` page. `obscura serve`/MCP interaction was not needed.
- The demo database on `6399`, its `neo_default` graph, and the three final
  capture queries were not verified in this run because the other demo agent
  starts that database later and `demo/CAPTURE.md` section F was not available.
