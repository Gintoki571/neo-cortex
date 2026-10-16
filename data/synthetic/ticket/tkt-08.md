---
id: tkt-08
kind: ticket
title: "PLAT-640: Raise api-gateway per-tenant rate limit for Orchard & Vane"
date: 2026-07-08T09:00:00Z
author: Viktor Sokolov
participants: [Viktor Sokolov, Anjali Deshpande, Noor Haddad]
status: closed
labels: [api-gateway, rate-limit, orchard-and-vane]
uri: pellucid://tickets/PLAT-640
---

# PLAT-640: Raise api-gateway per-tenant rate limit for Orchard & Vane

## Description

Request for a higher per-tenant rate limit on api-gateway for Orchard & Vane.

Orchard & Vane is a retail chain on our Enterprise plan. They are the heaviest user of payment-gateway, and Maggie Ellison is their exec sponsor. They are about to run a large seasonal import through the API, and they expect their calls to hit the tenant limit while it runs.

- Current per-tenant limit: 100 requests per second.
- Requested: 250 requests per second for the Orchard & Vane tenant, for the length of the import.

Risk: a higher ceiling sends more traffic past the gateway, and the gateway checks every request against auth-service. Noor will watch introspection latency during the import. If it climbs, we drop the limit back down.

## Comments

**Anjali Deshpande (2026-07-08):** Yes, please go ahead. Tell Orchard & Vane's team once it is live.

**Noor Haddad (2026-07-08):** I will watch introspection latency through the import window and flag it straight away if it moves.

**Viktor Sokolov (2026-07-09):** Applied this morning. The limit is now 250 req/s for that tenant. Closing; I will check the graphs after the import.
