---
id: doc-07
kind: doc
title: "Runbook: session-cache operations"
date: 2026-06-20T09:00:00Z
author: Beatrice Oyelaran
participants: [Beatrice Oyelaran, Mateo Alvarez, Noor Haddad]
labels: [runbook, session-cache, on-call]
uri: pellucid://wiki/runbooks/session-cache
---

# Runbook: session-cache operations

Owner of this page: Beatrice Oyelaran (SRE). Reviewed by Mateo Alvarez and Noor Haddad. Written after INC-01 so the next on-call does not have to rediscover any of this at 2 a.m.

## What it is

session-cache is the Redis cluster that holds login sessions for auth-service. If it loses data, every logged-in user is bounced to the login page. If it is slow, every authenticated request is slow.

## Current settings

- `session.ttl_seconds` is **900**. It was lowered on 2026-06-18; the old default was far too generous for our memory budget.
- Memory is 8 GB per cluster (raised from 4 GB on 2026-06-17). Eviction pressure above 80% memory pages the on-call.

## Dashboards and tools

I built the Grafana dashboard "session-cache / memory and evictions" and the alerts behind it (`sc-mem-high`, `sc-evictions-rate`). I also wrote `sessctl`, the small CLI used below. If an alert fires and you do not recognise it, the alert text links back to this page.

## Draining or flushing a shard

1. `sessctl drain --shard N` stops new sessions landing on shard N and lets live ones expire naturally (up to one TTL).
2. If the shard must be emptied now, run `sessctl flush --shard N`. Users whose session lived on that shard have to log in again; everyone else is untouched.
3. Check the evictions panel for five minutes afterwards.

**Never run `FLUSHALL`** (directly in redis-cli or through any wrapper). It empties every shard and logs out every user at once. If you think you need it, page Mateo first.

## Escalation

SEV1 (users cannot log in at all) pages the on-call; SEV2 goes to #platform. The on-call process page has the rotation.

## Notes

- The status page DNS record has its own TTL; do not confuse it with `session.ttl_seconds`.
- Capacity numbers in the dashboard assume one session record per login.
