---
type: Reference
title: FalkorDBLite overview
description: Embedded, zero-config FalkorDB for Python. The wheel bundles redis-server 8.6.2 and the FalkorDB 4.18.3 module and runs them as a child process on a unix socket.
resource: https://github.com/FalkorDB/falkordblite
tags: [falkordb, falkordblite, graph-database, embedded, python, cypher]
status: current
stale_after: 2026-11-15T00:00:00Z
generated: { by: claude-haiku-5-5/falkordblite-agent, at: 2026-10-15T19:35:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:35:00Z }
sources:
  - id: readme
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/README.md
    title: FalkorDBLite README (master)
  - id: gh-repo
    resource: https://api.github.com/repos/FalkorDB/falkordblite
    title: GitHub repository metadata
    last_modified: 2026-10-14T13:24:03Z
  - id: gh-release
    resource: https://api.github.com/repos/FalkorDB/falkordblite/releases/latest
    title: Latest GitHub release v0.10.0
    last_modified: 2026-05-02T13:09:05Z
  - id: gh-releases
    resource: https://api.github.com/repos/FalkorDB/falkordblite/releases
    title: GitHub releases list
  - id: pypi
    resource: https://pypi.org/pypi/falkordblite/json
    title: PyPI JSON for falkordblite
    last_modified: 2026-05-02T13:12:29Z
  - id: wheel-metadata
    resource: https://pypi.org/project/falkordblite/0.10.0/
    title: falkordblite 0.10.0 wheel METADATA (installed copy)
  - id: redislite-client
    resource: https://pypi.org/project/falkordblite/0.10.0/
    title: redislite/client.py as shipped in falkordblite 0.10.0 wheel
  - id: versions-cfg
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/versions.cfg
    title: versions.cfg (master)
  - id: license-txt
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/LICENSE.txt
    title: LICENSE.txt (master)
  - id: local-run
    resource: references/evidence/falkordblite/capabilities-run-all-output.txt
    title: Local install and capability run, throwaway venv
  - id: gh-commits
    resource: https://api.github.com/repos/FalkorDB/falkordblite/commits
    title: GitHub commits list (master)
  - id: gh-pulls
    resource: https://api.github.com/repos/FalkorDB/falkordblite/pulls?state=open
    title: GitHub open pull requests
  - id: license-404
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/LICENSE
    title: LICENSE on master (HTTP 404)
  - id: redislite-config
    resource: https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/configuration.py
    title: redislite/configuration.py (master)

evidence:
  - { name: readme-raw.txt, url: "https://raw.githubusercontent.com/FalkorDB/falkordblite/master/README.md", sha256: 668d42ad26430520bc50891f1bc36c69efd3549281bd6504c020a461115513b2, retrieved_at: 2026-10-15T19:23:42Z, method: curl, redistributed: false }
  - { name: gh-repo.json, url: "https://api.github.com/repos/FalkorDB/falkordblite", sha256: 7484d5d52e455fe623782471129b8c9d676c38168106d344d8516915400a848e, retrieved_at: 2026-10-15T19:23:44Z, method: curl, redistributed: false }
  - { name: gh-releases-latest.json, url: "https://api.github.com/repos/FalkorDB/falkordblite/releases/latest", url_basis: inferred, sha256: e03200681ca5b2f0b9d832779aaa68bf5d2f74667b866e5f78bfdf3b896297bf, retrieved_at: 2026-10-15T19:23:45Z, method: curl, redistributed: false }
  - { name: gh-releases.json, url: "https://api.github.com/repos/FalkorDB/falkordblite/releases", url_basis: inferred, sha256: a54bd00f387864837d7ed217a7b630bfabdd6ff90a270c33ce4eb1f30057b7d2, retrieved_at: 2026-10-15T19:23:46Z, method: curl, redistributed: false }
  - { name: pypi-falkordblite.json, url: "https://pypi.org/pypi/falkordblite/json", sha256: 97ceafd4f0cd8e4e4f79dc68de4593ed420d08928db3e4c4b25fb5abf366b070, retrieved_at: 2026-10-15T19:23:47Z, method: curl, redistributed: false }
  - { file: references/evidence/falkordblite/pypi-digests.txt, sha256: f9e0a90f68672ccb478faa52ce36878b27454d5c82f2c47e91f5bf3b856dcdfe, retrieved_at: 2026-10-15T19:28:00Z, method: command }
  - { file: references/evidence/falkordblite/wheel-sha256.txt, sha256: 6f647746676757327ca8ac85b4f5cf028c3988dd25896027e494463a30e54eb5, retrieved_at: 2026-10-15T19:27:00Z, method: command }
  - { name: wheel-falkordblite-0.10.0-METADATA.txt, url: "https://pypi.org/project/falkordblite/0.10.0/", url_basis: inferred, sha256: 97ab0e6fee2876049ca0848a493daca8ceda5610432e34a35bd00d0ddc12ed8f, retrieved_at: 2026-10-15T19:29:15Z, method: command, redistributed: false }
  - { name: versions.cfg, url: "https://raw.githubusercontent.com/FalkorDB/falkordblite/master/versions.cfg", url_basis: inferred, sha256: b622797cb9f431a5c40866d58115931f8cfbe33e64c303a91d8a69a2b54ac3f6, retrieved_at: 2026-10-15T19:24:24Z, method: curl, redistributed: false }
  - { name: src__LICENSE.txt, url: "https://raw.githubusercontent.com/FalkorDB/falkordblite/master/LICENSE.txt", url_basis: inferred, sha256: bff2923b7403b23bafd97e6e974b2e3b5bceb84e25b8df92eeeaec2b736e78c1, retrieved_at: 2026-10-15T19:23:50Z, method: curl, redistributed: false }
  - { file: references/evidence/falkordblite/license-404-body.txt, sha256: d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed, retrieved_at: 2026-10-15T19:24:30Z, method: curl }
  - { file: references/evidence/falkordblite/runtime-versions.txt, sha256: 7a52c8abf8ef5b91f53e58e2506225ccd5a33a5ef99be2cb37666edf33ce347b, retrieved_at: 2026-10-15T19:27:36Z, method: command }
  - { file: references/evidence/falkordblite/pip-install-output.txt, sha256: db34c934d3bc166e73b9ca6b2cb66b47e9a5d61196000d50e0a211df89b080a2, retrieved_at: 2026-10-15T19:26:00Z, method: command }
---

# What it is

FalkorDBLite is a Python package that ships a graph database you can use without installing a server. The README describes it this way:

> FalkorDBLite is a self-contained Python interface to the FalkorDB graph database.

[^readme]

It is a fork of Yahoo's redislite. GitHub reports the parent as `yahoo/redislite`:

> `"fork": true,`

[^gh-repo]

The repository has `"full_name": "yahoo/redislite"` as its parent, and its `redislite/` package keeps the upstream names. The import name is `redislite`, not `falkordblite`. See [python-api](/falkordblite/python-api.md).

# How it is embedded

It is a separate OS process, not a library linked into Python. Each `FalkorDB(...)` object starts a bundled `redis-server` with the FalkorDB module loaded. Source, `redislite/client.py` (wheel copy):

> `            command.extend(['--loadmodule', __falkordb_module__])`

[^redislite-client]

- Binaries inside the wheel: `redislite/bin/redis-server`, `redislite/bin/redis-cli`, `redislite/bin/falkordb.so` (about 53 MB). The Linux wheel also bundles `libgomp`, `libssl` and `libcrypto` under `falkordblite.libs/`. Source: [capabilities-test](/falkordblite/capabilities-test.md) (install step).
- Transport is a unix socket. The client sets up a private temp directory and a socket inside it:

> `            self.redis_dir = tempfile.mkdtemp()`

[^redislite-client]

- TCP is off by default. The default config has `'port': '0'`:

> `    'port': '0',`

[^redislite-config]

- A TCP listener can be enabled with `serverconfig={"port": "6399"}`. Tested: a pure `falkordb-py` client connected over TCP and read the data. See [capabilities-test](/falkordblite/capabilities-test.md#concurrency-and-connection-paths).

Running process list during a test (`ps`), showing the child process and its socket:

> `redis-server unixsocket:/tmp/tmpn6unc0bt/redis.socket`

Source: [limitations-and-open-issues](/falkordblite/limitations-and-open-issues.md#orphaned-server-processes) (orphaned server processes).

# Install

Command from the README:

> `$ pip install falkordblite`

[^readme]

Measured: a fresh venv on Python 3.14.7, Linux x86_64, installed `falkordblite==0.10.0` in 8.9 s wall clock. The dependencies pulled in were `falkordb 1.8.0`, `redis 8.1.0`, `psutil 7.2.2`, `setuptools 84.0.0`, `python-dateutil`, `six`. [^local-run]

# Versions, Python and platforms

- Latest on PyPI: `0.10.0`. PyPI `releases` contains 0.1.0 (2025-11-21) through 0.10.0 (2026-05-02). [^pypi]
- Latest GitHub release: `v0.10.0`, published `2026-05-02T13:09:05Z`. [^gh-release]
- Python requirement, from the wheel METADATA:

> `Requires-Python: >=3.12.0`

[^wheel-metadata]

- Wheels on PyPI for 0.10.0 are CPython 3.12, 3.13 and 3.14 only, for macOS (x86_64 and arm64), Linux `manylinux_2_39` aarch64 and x86_64, plus an sdist. No Windows wheel is listed. [^pypi]
- Sizes from PyPI: macOS wheel 17,752,268 bytes; Linux aarch64 34,579,293 bytes; Linux x86_64 36,154,066 bytes; sdist 23,675,620 bytes. [^pypi]
- The Linux x86_64 cp314 wheel that was tested has sha256 `b36665ebd9e2d5e38b401b34f7ba6f0b22e5b88cbc817971c8c1d71a8ad305f7`, matching the PyPI digest. [^pypi] [^local-run]
- macOS needs OpenMP at runtime:

> **Important:** The FalkorDB module requires the OpenMP runtime library (`libomp`).

[^readme]

Bundled server versions:

- Redis: `REDIS_VERSION=8.6.2`. [^versions-cfg]
- FalkorDB: `FALKORDB_VERSION=v4.18.3`. [^versions-cfg]
- Runtime check: `redis-server --version` returned `Redis server v=8.6.2`, and `MODULE LIST` returned the graph module with `'ver': 41803`. The encoding (major*10000 + minor*100 + patch) matches 4.18.3. Source: [capabilities-test](/falkordblite/capabilities-test.md).

# License

- PyPI and wheel metadata: `License: BSD License`. [^wheel-metadata]
- GitHub API: `"spdx_id": "NOASSERTION"`, name `Other`. [^gh-repo]
- The `LICENSE` path returns 404. The file that exists is `https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/LICENSE`, which is the upstream redislite text (copyright Yahoo, 2015):

> Copyright (c) 2015, Yahoo Inc.

[^license-txt] [^license-404]

This is an open question for legal review. See [limitations-and-open-issues](/falkordblite/limitations-and-open-issues.md#license-ambiguity).

# Maintenance activity

Observed on 2026-10-15 (UTC):

- Repository created `2025-10-12T18:35:54Z`, last push `2026-10-14T13:24:03Z`. Stars 62, forks 4, open issues plus PRs 24 (`open_issues_count`). [^gh-repo]
- Latest commit on `master` at fetch time was dated 2026-05-02, and the last commit before that was the 0.10.0 release. [^gh-commits] Pushes after that are PRs merged or open.
- Open PR `#116 chore(release): bump version to 0.11.0` (opened 2026-10-14) and `#115 feat: install hiredis by default` (opened 2026-10-14) are not released. Version 0.11.0 is not on PyPI yet. [^gh-pulls]
- Many Dependabot bumps. See [limitations-and-open-issues](/falkordblite/limitations-and-open-issues.md).

# Open questions

- Is the bundled `falkordb.so` a byte-for-byte build of upstream FalkorDB v4.18.3? The repo pins the tag and the module reports 41803, but no upstream artifact hash was compared.
- The `https://github.com/FalkorDB/GraphRAG-SDK/blob/35e67a0/pyproject.toml` and `setup.py` on `master` belong to the upstream redislite layout (for example `setup.py` header: `# Copyright (c) 2015, Yahoo Inc.`). Whether the PyPI sdist is built from them was not checked.
- Windows support: no wheel and no sdist test was run. The closed issue `#60 Bug on windows` was not read in full.

[^readme]: FalkorDBLite README (master) at https://raw.githubusercontent.com/FalkorDB/falkordblite/master/README.md, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/README.md`.
[^gh-repo]: GitHub repository metadata at https://api.github.com/repos/FalkorDB/falkordblite, evidence `https://api.github.com/repos/FalkorDB/falkordblite`.
[^gh-release]: Latest release at https://api.github.com/repos/FalkorDB/falkordblite/releases/latest, evidence `https://api.github.com/repos/FalkorDB/falkordblite/releases/latest`.
[^gh-commits]: Commit list at https://api.github.com/repos/FalkorDB/falkordblite/commits, evidence `https://api.github.com/repos/FalkorDB/falkordblite/commits`.
[^gh-pulls]: Open PR list at https://api.github.com/repos/FalkorDB/falkordblite/pulls?state=open, evidence `https://api.github.com/repos/FalkorDB/falkordblite/pulls?state=open`.
[^pypi]: PyPI JSON at https://pypi.org/pypi/falkordblite/json, evidence `https://pypi.org/pypi/falkordblite/json` and `pypi-digests.txt`.
[^wheel-metadata]: Wheel METADATA of falkordblite 0.10.0, evidence `https://pypi.org/project/falkordblite/0.10.0/`.
[^redislite-client]: `redislite/client.py` from the installed 0.10.0 wheel, evidence `https://pypi.org/project/falkordblite/0.10.0/`.
[^redislite-config]: `redislite/configuration.py` at master, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/redislite/configuration.py`.
[^versions-cfg]: `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/versions.cfg` at master, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/versions.cfg`.
[^license-txt]: `https://raw.githubusercontent.com/FalkorDB/GraphRAG-SDK/main/LICENSE` at master, evidence `https://raw.githubusercontent.com/FalkorDB/falkordblite/master/LICENSE.txt`.
[^license-404]: `LICENSE` at master returned HTTP 404, evidence `references/evidence/falkordblite/license-404-body.txt`.
[^local-run]: Local install and runs in a throwaway venv, evidence `references/evidence/falkordblite/pip-install-output.txt`, `runtime-versions.txt`, `capabilities-run-all-output.txt`.
