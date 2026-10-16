---
id: tkt-10
kind: ticket
title: "CFG-4463: Lower per-tenant rate limit to 180"
date: 2026-09-14T09:00:00Z
author: Viktor Sokolov
participants: [Viktor Sokolov, Noor Haddad, Mateo Alvarez]
status: closed
labels: [config, api-gateway, rate-limit, prod]
uri: pellucid://tickets/CFG-4463
---

# CFG-4463: Lower per-tenant rate limit to 180

## Description

Production config change for the api-gateway per-tenant rate limit.

- Setting: per-tenant request rate limit on api-gateway
- From: 250 requests per second
- To: 180 requests per second
- Environment: prod
- Applied: 2026-09-14
- Reviewer: Noor Haddad
- Basis: the load test in PLAT-702, which showed that 250 req/s is enough to saturate auth-service.

Reason: a single tenant running at the old ceiling can push auth-service into saturation, and every other tenant pays for it. 180 leaves a margin under the level where the test showed trouble, while still giving the largest tenants room to work.

Expected effect: a tenant that goes past 180 req/s is throttled at the gateway, and auth-service sees less peak introspection load.

Rollback: set the limit back to 250 through the normal config path and tell on-call.

## Comments

**Noor Haddad (2026-09-14):** Reviewed. The number matches the test results. Approved.

**Mateo Alvarez (2026-09-14):** Noted in the on-call channel. Please tell support if any customer starts seeing throttling.

**Viktor Sokolov (2026-09-14):** Applied at 180 req/s. Closing.
