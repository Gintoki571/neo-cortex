---
id: tkt-22
kind: ticket
title: "PAY-501: Release ledger-service v3.8"
date: 2026-09-08T09:00:00Z
author: Elif Yildiz
participants: [Elif Yildiz, Sofia Marchetti, Hugo Tremblay]
status: closed
labels: [release, ledger-service, payments]
uri: pellucid://tickets/PAY-501
---

# PAY-501: Release ledger-service v3.8

## Description

Release ledger-service v3.8 to production. Owner: Elif Yildiz.

Scope:

- Outbox publisher: the idempotency key on outbox events changes from `txn_id` to `txn_id:attempt`. The reason is retry visibility, so that a republished event is easier to trace back to the attempt that produced it.
- No API changes and no schema changes.
- The key change is internal to the outbox. Consumers read the key as an opaque string, so nothing else should need to change to accept it.

Testing: the outbox publisher tests were updated for the new key and the release went through a staging soak before it was booked.

Deploy: 2026-09-08 during the Payments window, following the deploy checklist. Canary first, then full traffic.

Rollback: redeploy the previous release.

## Comments

**Sofia Marchetti (2026-09-08):** Approved for release from the Payments side. Hugo, can you give the diff a second read?

**Hugo Tremblay (2026-09-08):** Reviewed the diff. The key change is small and the tests cover it. Approved.

**Elif Yildiz (2026-09-08):** Deploying after the canary. Closing once it is at full traffic.
