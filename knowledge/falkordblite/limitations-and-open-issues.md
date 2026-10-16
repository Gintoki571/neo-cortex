---
type: Risk Register
title: FalkorDBLite limitations and open issues
description: Limits seen in code, tests and GitHub issues that matter for GraphRAG use of falkordblite, including orphaned server processes, all-interface TCP when enabled, Cypher constraint gaps and SSpaths behaviour.
resource: https://github.com/FalkorDB/falkordblite/issues
tags: [falkordblite, limitations, risks, graphrag, open-issues]
status: current
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/falkordblite-agent, at: 2026-10-15T19:35:00Z }
sources:
  - id: gh-issues
    resource: https://api.github.com/repos/FalkorDB/falkordblite/issues?state=all
    title: GitHub issues and PRs list (state=all, first 100)
    last_modified: 2026-10-14T13:24:03Z
  - id: gh-pulls
    resource: https://api.github.com/repos/FalkorDB/falkordblite/pulls?state=open
    title: GitHub open pull requests
  - id: readme
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/README.md
    title: FalkorDBLite README (master)
  - id: license-txt
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/LICENSE.txt
    title: LICENSE.txt (master)
  - id: setup-master
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/setup.py
    title: setup.py (master)
  - id: redislite-client
    resource: https://pypi.org/project/falkordblite/0.10.0/
    title: redislite/client.py as shipped in falkordblite 0.10.0 wheel
  - id: redislite-config
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/configuration.py
    title: redislite/configuration.py (master)
  - id: local-run
    resource: references/evidence/falkordblite/capabilities-run-all-output.txt
    title: Local probe runs in throwaway venv
  - id: api
    resource: references/evidence/falkordblite/api-connection-probe-output.txt
    title: Connection, threading and async probe output
  - id: constraints
    resource: references/evidence/falkordblite/constraints-command-probe-output.txt
    title: Constraint syntax probe output
  - id: listen-probe
    resource: references/evidence/falkordblite/listen-probe-output.txt
    title: TCP listen address probe output
  - id: orphan
    resource: references/evidence/falkordblite/orphan-server-driver-output.txt
    title: Orphaned server probe output
  - id: sp-probe
    resource: references/evidence/falkordblite/sp-probe-output.txt
    title: Shortest-path probe output
  - id: sspaths
    resource: references/evidence/falkordblite/sspaths-rowcount-output.txt
    title: SSpaths row-count probe output
  - id: timing
    resource: references/evidence/falkordblite/timing-probe-output.txt
    title: Open/query/close timing probe output
  - id: wheel
    resource: https://pypi.org/project/falkordblite/0.10.0/
    title: falkordblite 0.10.0 wheel METADATA

evidence:
  - { file: references/evidence/falkordblite/gh-issues-open.json, sha256: adf4f503f3d1bae939a7ce98b106d6d6c2b96f5c555e5a8d168cc27fe10ee5c4, retrieved_at: 2026-10-15T19:24:11Z, method: curl }
  - { file: references/evidence/falkordblite/gh-pulls-open.json, sha256: 9ab0a7381be1b16fd9abc6945f1d5df047a703973b0ec4976903261dc2eb19f9, retrieved_at: 2026-10-15T19:24:18Z, method: curl }
  - { file: references/evidence/falkordblite/readme-raw.txt, sha256: 668d42ad26430520bc50891f1bc36c69efd3549281bd6504c020a461115513b2, retrieved_at: 2026-10-15T19:23:42Z, method: curl }
  - { file: references/evidence/falkordblite/src__LICENSE.txt, sha256: bff2923b7403b23bafd97e6e974b2e3b5bceb84e25b8df92eeeaec2b736e78c1, retrieved_at: 2026-10-15T19:23:50Z, method: curl }
  - { file: references/evidence/falkordblite/setup-master-raw.py, sha256: 056618ffe2099f682b9a14206d1707b8b0593af91c42667b5e62478c845c0660, retrieved_at: 2026-10-15T19:23:45Z, method: curl }
  - { file: references/evidence/falkordblite/src__redislite_configuration.py, sha256: 6d48aaabd251ab17b251dd55f1a0d057271de650d2759d6c0e13d3577d228b0f, retrieved_at: 2026-10-15T19:23:48Z, method: curl }
  - { file: references/evidence/falkordblite/wheel-redislite-client.py.txt, sha256: b1dba5d9f35c0de1df504b23c148058c247c2f95cf521cdab13becdc4670db9b, retrieved_at: 2026-10-15T19:29:15Z, method: command }
  - { file: references/evidence/falkordblite/orphan-server-driver-output.txt, sha256: fa57433a89da6689f4e254ff16acd8b2a04bb1e3f10a3c167b02f17f20f48cde, retrieved_at: 2026-10-15T19:30:23Z, method: command }
  - { file: references/evidence/falkordblite/listen-probe-output.txt, sha256: ad80d05d668cf6dad0a8bca4a531ad765810258f19c62a0feda3f3088112c8da, retrieved_at: 2026-10-15T19:31:20Z, method: command }
  - { file: references/evidence/falkordblite/wheel-falkordblite-0.10.0-METADATA.txt, sha256: 97ab0e6fee2876049ca0848a493daca8ceda5610432e34a35bd00d0ddc12ed8f, retrieved_at: 2026-10-15T19:29:15Z, method: command }
  - { file: references/evidence/falkordblite/timing-probe-output.txt, sha256: 4df99ef91f74a1971167cfeae4238b8ea6bd520f4a1fb76bb3b04eb72e3ac0e3, retrieved_at: 2026-10-15T19:31:03Z, method: command }
  - { file: references/evidence/falkordblite/constraints-command-probe-output.txt, sha256: 790b1b026574c7c00f164e52bf63af4ae9cd084505cc0ae911d4934df17ad9e5, retrieved_at: 2026-10-15T19:28:30Z, method: command }
  - { file: references/evidence/falkordblite/sspaths-rowcount-output.txt, sha256: c00dd109fba0bcc4e0422514f0afc0b5a3936baa6f6dfa40a56384fbcc979694, retrieved_at: 2026-10-15T19:27:50Z, method: command }
  - { file: references/evidence/falkordblite/sp-probe-output.txt, sha256: 5ac6313aa3df47cd6e13f7cf552b95ee95c92bc93245b984c3351eb7187fce33, retrieved_at: 2026-10-15T19:27:36Z, method: command }
  - { file: references/evidence/falkordblite/api-connection-probe-output.txt, sha256: 4d4750d52c4d377e06f183e8a85cc34477c156b843d9221dbecf429ff650d385, retrieved_at: 2026-10-15T19:27:50Z, method: command }
---

# Top risks for GraphRAG use

1. **Embedded server is a child process, not a library.** Each `FalkorDB(...)` starts `redis-server`. If the Python process exits while another client is still connected, the server stays up. See [orphaned server processes](#orphaned-server-processes).
2. **Shutdown is slow.** Measured close time was about 3.2 s per instance. Open issue `#113` reports the same. Per-request open and close will hurt.
3. **TCP exposure is all-interface when enabled.** Only if you ask for it, but the redislite defaults set no password (no `requirepass` in `configuration.py`). See [TCP exposure](#tcp-exposure).
4. **Cypher uniqueness constraints are not created with `CREATE CONSTRAINT`.** Use `GRAPH.CONSTRAINT` after an exact-match index. See [constraints](#constraints).
5. **`algo.SSpaths` returned one path in every test.** Do not use it for all-targets output without a check against upstream. See [shortest paths](#shortest-paths).
6. **License is unclear.** See [license ambiguity](#license-ambiguity).

# Packaging and naming

- The PyPI distribution is `falkordblite` but the import path is `redislite`, and `redislite.__version__` reports `0.0.0` in the 0.10.0 wheel. Observed in [capabilities-test](/falkordblite/capabilities-test.md). [^local-run]
- Open issue `#85 Documentation improvements: import path, testing patterns, Python 3.12+ requirement` covers the import-path gap. [^gh-issues]
- The repo is a fork of `yahoo/redislite`. On `master`, `setup.py` still begins with:

> `# Copyright (c) 2015, Yahoo Inc.`

[^setup-master]

# License ambiguity

Three sources disagree or are incomplete:

- PyPI and wheel metadata say `License: BSD License`. [^local-run]
- GitHub API says the license is `Other`, with `"spdx_id": "NOASSERTION"`. [^gh-issues]
- The README says `FalkorDBLite is Free software under the New BSD license, see LICENSE.txt for details.` [^readme]
- The `LICENSE` path returns 404. `LICENSE.txt` is the upstream redislite text, which opens with `Redislite license and trademark information` and copyright `2015, Yahoo Inc.`. [^license-txt]

Action: a legal read is needed before this is used in a product. For the hackathon the risk is low, but the notice must still carry the Yahoo copyright if the code is redistributed.

# Platforms

- No Windows wheel is published (PyPI wheels: macOS and Linux only). Windows was not tested. [^local-run]
- macOS needs OpenMP at runtime:

> **Important:** The FalkorDB module requires the OpenMP runtime library (`libomp`).

[^readme]

- Linux wheels carry the tag `manylinux_2_39`. This is read from the filename. A system with an older glibc will most likely fall back to the sdist build. This was not tested.
- The Linux wheel bundles `libgomp`, `libssl` and `libcrypto` in `falkordblite.libs/`. [^local-run]

# Networking and exposure

## TCP exposure

Default: `'port': '0'`, so no TCP listener. [^redislite-config]

When a port is requested through `serverconfig`, the server listened on all interfaces, not loopback:

> `LISTEN 0      511          0.0.0.0:6398       0.0.0.0:*`
> `LISTEN 0      511             [::]:6398          [::]:*`

[^listen-probe]

The redislite defaults set `'bind': None` and no `requirepass` line appears in `configuration.py`. Authentication was not tested. Treat any enabled TCP port as open to the network unless you set a bind address and a password yourself. Pass them through `serverconfig`, for example `serverconfig={"port": "6399", "bind": "127.0.0.1"}`. The `bind` override was not tested.

## Unix socket

Default. Socket permission is `700` in the defaults. [^redislite-config] The README says the default is accessible only by the creating user. [^readme]

# Orphaned server processes

`close()` only stops the server when no other client is connected. From the client source:

> `            if self._connection_count() <= 1:`

[^redislite-client]

Test: open a database, add a second raw `redis.Redis(unix_socket_path=...)` client, let the Python process exit without closing it. The `redis-server` child kept running after the process exited. Output in `orphan-server-driver-output.txt`:

> `114152 /home/bindesh/.claude/jobs/f6d15fef/tmp/falkordblite/venv/lib/python3.14/site-packages/redislite/bin/redis-server unixsocket:/tmp/tmpdu0_ijmq/redis.socket`

[^orphan]

The same thing happened in the TCP probe: a pure falkordb-py client was still referenced when `close()` ran, and one server was left running. The test killed it by hand. [^local-run]

Mitigation for GraphRAG code: close every client (including ad-hoc `redis.Redis` connections) before exit. Do not rely on `atexit`.

# Shutdown latency

- Measured in one run: open server `0.134 s`, one query `0.0030 s`, close `3.245 s`. [^timing]
- Open issue `#113` reports the same pattern: "Opening a connection, running a query and exiting takes ~4.4s, of which only ~0.2s is actual work. The rest is process exit." [^gh-issues]
- Impact: a short-lived script pays about 3 s on exit. A long-lived process that opens one `FalkorDB` object and keeps it is not affected much.

# Constraints

- `CREATE CONSTRAINT ON (x:Persona) ASSERT x.name IS UNIQUE` is rejected:

> `Invalid constraint command use the GRAPH.CONSTRAINT command instead`

[^constraints]

- `CREATE CONSTRAINT FOR (x:Persona) REQUIRE x.name IS UNIQUE` is rejected as a syntax error.
- The working form needs an exact-match index first:

```python
g.query("CREATE INDEX FOR (x:Persona) ON (x.name)")
db.client.execute_command("GRAPH.CONSTRAINT", "CREATE", "cons2", "UNIQUE", "NODE", "Persona", "PROPERTIES", "1", "name")
```

Result: `PENDING`, then duplicate insert rejected with `unique constraint violation on node of type Persona`. [^constraints]
- Open issue `#34 Creating constraints` asks the same question and is still open. [^gh-issues]

# Shortest paths

- `algo.SPpaths` with `weightProp` picked the two-hop route with lower total weight in a test graph. [^sp-probe]
- `algo.SSpaths` returned exactly one row in both the weighted and the unweighted tree test. [^sspaths]
- `YIELD weight` is not available on `algo.SPpaths` or `algo.SSpaths`. Error: `Procedure \`algo.SPpaths\` does not yield output \`weight\``. [^local-run]
- Unknown config keys are silently accepted. `notAKey: 1` in the `algo.SPpaths` map returned a path. [^sp-probe]

# Procedures and config

- `CALL db.procedures()` is not registered. Use `CALL dbms.procedures()`. [^local-run]
- `GRAPH.CONFIG GET VERSION` returns `Unknown configuration field`. The module version is available from `MODULE LIST` instead. [^local-run]

# Async and warnings

- Test runs printed `RuntimeWarning: coroutine 'AsyncManagementCommands.shutdown' was never awaited` from `redislite/client.py:112`. Open issue `#61 Warnings in tests` tracks this. [^api] [^gh-issues]

# Vector and full-text limits

- Only small graphs were tested: 4 nodes, dimension 4, cosine similarity. No scale, recall or latency test was done.
- Index defaults shown in the index listing: `M: 16`, `efConstruction: 200`, `efRuntime: 10`. [^local-run]
- Not tested: dimension mismatch, updates and deletes of vectors, euclidean index, fulltext options, and stemming.

# Concurrency and durability

- 20 threads sharing one handle wrote 20 nodes with no error. [^api]
- A second process that opened the same file while the first was alive attached to the running server. [^api]
- Not tested: concurrent writes from two processes, behaviour when the first process closes while the second is attached, and crash durability (a kill with no `SAVE`).
- `close()` saves: `self.shutdown(save=True, now=True, force=True)`. [^redislite-client] A crash may lose data written since the last save. Not tested.

# Dependencies and maintenance

- The wheel requires `redis>=4.5` and `falkordb>=1.2.0`. [^wheel]
- Open PRs bump these: `#112` moves falkordb to `>=1.7.1`, `#110` moves redis to `>=8.1.0`. [^gh-pulls]
- `#115 feat: install hiredis by default for faster reply parsing` and `#116 chore(release): bump version to 0.11.0` are open. No 0.11.0 release is on PyPI yet. [^gh-pulls]
- `#49 Automate syncing FalkorDB upstream releases into falkordblite (daily PR)` is open. The FalkorDB pin is manual today. [^gh-issues]

# Open issues snapshot

Open issues at fetch time (9 of the first 100 items, excluding PRs):

| # | Title | Relevance |
|---|---|---|
| 113 | Process shutdown takes ~4s while the actual work takes ~0.2s | high |
| 34 | Creating constraints | medium |
| 85 | Documentation improvements: import path, testing patterns, Python 3.12+ requirement | medium |
| 49 | Automate syncing FalkorDB upstream releases into falkordblite (daily PR) | medium |
| 61 | Warnings in tests | low |
| 114 | Install hiredis by default for faster reply parsing | low |
| 30 | Refactor CI and configuration set global settings | low |
| 80 | Optimize CI Pipeline to Reduce Runtime | low |
| 25 | The name of the whl files should be fixed | low |

[^gh-issues]

# Open questions

- Is `SSpaths` returning one row a bug upstream, or a usage issue (for example it needs an explicit target)?
- Does `serverconfig={"bind": "127.0.0.1"}` restrict the TCP listener, and is `requirepass` configurable through `serverconfig`? Not tested.
- Does a crash lose data? Not tested.
- Are the closed Windows and WSL2 issues (`#60`, `#74`) still relevant? Only their titles were read.

[^local-run]: `references/evidence/falkordblite/capabilities-run-all-output.txt`, `runtime-versions.txt`.
[^wheel]: Wheel METADATA of falkordblite 0.10.0, evidence `references/evidence/falkordblite/wheel-falkordblite-0.10.0-METADATA.txt`.
[^readme]: FalkorDBLite README, evidence `references/evidence/falkordblite/readme-raw.txt`.
[^gh-issues]: GitHub issues list, evidence `references/evidence/falkordblite/gh-issues-open.json`.
[^gh-pulls]: GitHub open PRs, evidence `references/evidence/falkordblite/gh-pulls-open.json`.
[^setup-master]: `setup.py` on master, evidence `references/evidence/falkordblite/setup-master-raw.py`.
[^license-txt]: `LICENSE.txt` on master, evidence `references/evidence/falkordblite/src__LICENSE.txt`.
[^redislite-config]: `redislite/configuration.py`, evidence `references/evidence/falkordblite/src__redislite_configuration.py`.
[^redislite-client]: `redislite/client.py` from the 0.10.0 wheel, evidence `references/evidence/falkordblite/wheel-redislite-client.py.txt`.
[^listen-probe]: `references/evidence/falkordblite/listen-probe-output.txt`, script `listen-probe.py`.
[^orphan]: `references/evidence/falkordblite/orphan-server-driver-output.txt`, scripts `orphan-server-driver.sh` and `orphan-server-probe.py`.
[^timing]: `references/evidence/falkordblite/timing-probe-output.txt`, script `timing-probe.py`.
[^constraints]: `references/evidence/falkordblite/constraints-command-probe-output.txt`, scripts `constraints-probe.py` and `constraints-command-probe.py`.
[^sp-probe]: `references/evidence/falkordblite/sp-probe-output.txt`, script `capabilities-shortest-path-probe.py`.
[^sspaths]: `references/evidence/falkordblite/sspaths-rowcount-output.txt`, script `sspaths-rowcount-probe.py`.
[^api]: `references/evidence/falkordblite/api-connection-probe-output.txt`, script `api-connection-probe.py`.
