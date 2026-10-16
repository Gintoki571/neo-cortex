---
id: ses-07
kind: session
title: "Agent session: diagnose doubled totals"
date: 2026-09-09T09:30:00Z
author: Olivia Hartmann
participants: [Olivia Hartmann]
labels: [agent-session, reporting-service, ledger-service]
---

## Task

Olivia asked: invoice totals shown by reporting-service are about double what ledger-service says. Find out why. Read-only investigation, do not change production.

## Steps

1. Queried reporting-service totals against the ledger for a sample of 20 invoices. Reporting is exactly 2x on every affected invoice; unaffected invoices are exact.
2. Suspected a reporting-service query cache returning stale rows. Cleared the cache in a staging copy: no change. Dead end, discarded.
3. Looked at the raw events table. Affected invoices have two events each, written minutes apart on 2026-09-08, which points to the producer republishing after the event-pipeline broker rebalanced that day.
4. Compared the two copies of one event. The ledger-service outbox row in the first copy has key `txn_8841`, the second `txn_8841:2`. Consumers dedupe on the key, so they treated them as different events.
5. Checked git history in ledger-service. Version 3.8, deployed on 2026-09-08 by Elif Yildiz, changed the idempotency key from `txn_id` to `txn_id:attempt`. Before 3.8 the republished event would have had the same key and been dropped.

## Outcome

Root cause: the key format change in ledger-service v3.8 combined with the outbox republishing after the rebalance. Wrote the findings into the incident ticket. Recommended reverting the key format, then a dedupe backfill in reporting-service.

## Lessons

- When a total is exactly 2x, look for duplicates before looking for caches.
- An idempotency key is part of an interface: consumers depend on its shape.
- Check recent ledger-service releases when events look doubled.
