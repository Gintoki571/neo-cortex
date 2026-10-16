---
id: tkt-17
kind: ticket
title: "INC-03: Payment authorizations returning 502"
date: 2026-08-10T09:25:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Noor Haddad, Daniel Kwon, Chen Wei]
status: closed
labels: [incident, payment-gateway, auth-service, config]
uri: pellucid://tickets/INC-03
---

# INC-03: Payment authorizations returning 502

## Description

Incident: payment authorizations are returning HTTP 502. Checkout and payment runs failed for Orchard & Vane and Saltmarsh Foods, starting at 09:12 UTC. Impact lasted about 41 minutes.

What we see: payment-gateway checks each incoming request's token with auth-service through token introspection. Those introspection calls from payment-gateway are timing out, and when they time out the gateway returns 502 to the caller.

Suspect change: CFG-4411, a config push made at 09:05 UTC.

Actions:

- Roll back CFG-4411. Mateo Alvarez (on-call) runs the rollback with cfgctl at 09:50 UTC.
- Watch the 502 rate until the error budget panel is back to green.

## Comments

**Noor Haddad (2026-08-10):** Introspection latency is climbing and the timeouts make up most of the errors. auth-service is otherwise healthy.

**Daniel Kwon (2026-08-10):** Gateway retries are not helping and are adding load. I would like the rollback as early as possible.

**Chen Wei (2026-08-10):** The 09:05 change is the one in the config history. I am around to answer questions while you look.

**Mateo Alvarez (2026-08-10):** Rollback is done. The 502s stopped at 09:53 and the panel is green. Closing. Action items will go into a separate ticket.
