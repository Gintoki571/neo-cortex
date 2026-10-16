---
id: tkt-05
kind: ticket
title: "CFG-4380: Lower session.ttl_seconds from 3600 to 900"
date: 2026-06-18T09:00:00Z
author: Beatrice Oyelaran
participants: [Beatrice Oyelaran, Noor Haddad, Mateo Alvarez]
status: closed
labels: [config, session-cache, prod]
uri: pellucid://tickets/CFG-4380
---

# CFG-4380: Lower session.ttl_seconds from 3600 to 900

## Description

Production config change record for the session idle timeout on session-cache.

- Key: `session.ttl_seconds`
- From: 3600
- To: 900
- Environment: prod
- Applied: 2026-06-18, 09:00 UTC
- Reviewer: Noor Haddad (one reviewer)

Reason: the old value kept idle login sessions alive for an hour. That is far too generous for the memory budget after INC-01, because every idle session keeps an entry in the cache. A shorter idle window means fewer entries sit in memory at once. This is meant as a stopgap while we work out the longer-term session policy.

Expected effect: lower steady-state memory on session-cache. Users who step away for more than fifteen minutes will need to sign in again.

Monitoring: we will compare the eviction rate and the logout count for the next two days against the week before.

## Comments

**Mateo Alvarez (2026-06-18):** Fine by me. Watch the logout graph for the next hour.

**Beatrice Oyelaran (2026-06-18):** Applied. The logout graph is flat so far.

**Noor Haddad (2026-06-18):** Reviewed the change. The number matches what we discussed. Closing.
