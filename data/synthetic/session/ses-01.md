---
id: ses-01
kind: session
title: "Agent session: investigate logout complaints"
date: 2026-06-17T08:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez]
labels: [agent-session, session-cache, incident]
---

## Task

Mateo asked: web-dashboard users are being logged out early. Find out what session-cache is doing. Read metrics and config only, and do not change anything in production without asking.

## Steps

1. Pulled the session-cache metrics for the last two days. Connection counts look normal and latency is fine. Nothing alarming at first glance.
2. First guess was the load balancer dropping sticky connections. Checked its config and health checks: nothing wrong. Dead end, noted and discarded.
3. Looked at the eviction counters. Evictions spike in the same windows where users report logouts. Live session keys are among the evicted ones, which a session store should never do.
4. Read the cache config. The maxmemory policy is allkeys-lru, so under memory pressure any key is fair game, live sessions included.
5. Checked memory. The cluster sits at its 4 GB ceiling during the afternoon peak. Recommended raising the ceiling to 8 GB. Mateo agreed and the change was made the same day.

## Outcome

Root cause is memory pressure in session-cache evicting live sessions, not the network. Memory raised to 8 GB on 17 June. The logouts have not been re-checked since the change; Mateo will watch the evictions panel overnight.

## Lessons

- A session store on allkeys-lru will quietly drop live sessions when it runs out of memory. Check the eviction policy before anything else.
- Metrics first, then config. I jumped to the load balancer because it was the newest box on the diagram, and that cost time.
- Evictions are invisible to users until they complain. Alert on the eviction rate, not only on latency.
