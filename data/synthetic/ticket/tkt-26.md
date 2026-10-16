---
id: tkt-26
kind: ticket
title: "PAY-510: Consumer contract test for idempotency keys"
date: 2026-09-17T09:00:00Z
author: Elif Yildiz
participants: [Elif Yildiz, Samir Haddad, Hugo Tremblay]
status: closed
labels: [payments, event-pipeline, testing, idempotency]
uri: pellucid://tickets/PAY-510
---

# PAY-510: Consumer contract test for idempotency keys

## Description

Add a contract test to the consumer suite that fails whenever the idempotency key on a ledger event stops matching the agreed shape. The shape is the plain `txn_id` value and nothing else, and it should never change in place. Samir's ADR from yesterday sets that rule; this ticket makes the build enforce it so nobody has to remember it.

Scope:

- Test fixture: a sample event taken from the ledger outbox, asserted against the key pattern.
- Runs in CI for every consumer that reads the stream (reporting-service and fraud-scoring both do).
- The failure message links to the ADR and tells the author to talk to the Data team before touching the key.

Not in scope: changing the producer. The ledger already emits the right key, so this is a guard, not a fix.

## Comments

**Samir Haddad (2026-09-17):** Fixture is in. I took the key rule straight from the ADR so the two cannot drift apart. Hugo, can you check the fraud-scoring side?

**Hugo Tremblay (2026-09-17):** Fraud-scoring treats the key as an opaque string, so the assertion works for us as written. Merged to the consumer branch.

**Elif Yildiz (2026-09-17):** Lesson for anyone reading this later: a shape change slipped through once and nothing caught it. Never change an idempotency key's shape without a consumer contract test. The test exists now, so the next person gets a red build instead of a quiet surprise.
