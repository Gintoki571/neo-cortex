---
id: tkt-09
kind: ticket
title: "PLAT-702: Gateway load test results"
date: 2026-09-12T09:00:00Z
author: Beatrice Oyelaran
participants: [Beatrice Oyelaran, Viktor Sokolov, Noor Haddad]
status: closed
labels: [load-test, api-gateway, auth-service]
uri: pellucid://tickets/PLAT-702
---

# PLAT-702: Gateway load test results

## Description

Report from the load test we ran against api-gateway this week.

Context: api-gateway sits in front of auth-service, and it calls auth-service on every request it forwards. The gateway ceiling therefore decides how much introspection load auth-service has to carry.

Setup: synthetic tenant traffic, ramped in steps. The test ran against the current per-tenant ceiling of 250 req/s.

Results:

- Below the ceiling, auth-service latency stays flat through the whole ramp.
- At the top step, the per-tenant ceiling of 250 req/s is enough to saturate auth-service. CPU is pinned and the connection pool fills up, and introspection latency climbs steeply.
- The gateway itself shows no trouble at that rate. The bottleneck is entirely downstream.

This ticket does not change any setting. A decision about the ceiling will go into a follow-up ticket. Raw graphs are in the load-test folder.

## Comments

**Viktor Sokolov (2026-09-12):** Saw the saturation at the top step. Do you want to rerun at a lower ceiling?

**Noor Haddad (2026-09-12):** Yes, but let's agree on the number from the data, not from the current value. I want the rerun before we pick one.

**Beatrice Oyelaran (2026-09-12):** The report is done. Closing this one; the decision goes to a new ticket.
