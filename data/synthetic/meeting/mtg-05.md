---
id: mtg-05
kind: meeting
title: "Postmortem: INC-04 duplicate totals"
date: 2026-09-11T15:00:00Z
author: Yusuf Demir
participants: [Yusuf Demir, Olivia Hartmann, Elif Yildiz, Samir Haddad, Sofia Marchetti]
labels: [postmortem, event-pipeline, reporting]
---

# Postmortem: INC-04 duplicate totals

## Attendees

Yusuf Demir (chair), Olivia Hartmann, Elif Yildiz, Samir Haddad, Sofia Marchetti.

## Notes

- Summary: reporting-service counted some invoice events twice. The duplicates were events that the ledger-service outbox republished after a broker rebalance on 2026-09-08; the consumers could not tell they had seen them already.
- Someone noted the republished events carried a different key format from the originals. We agreed to come back to who and why offline, because the point is the missing safety net, not the person.
- Olivia's dedupe backfill ran on 2026-09-10 and the key format was reverted the day before, 2026-09-09. Totals are correct again.
- Sofia asked whether this is the same thing as the duplicate reminder emails in June. It is not: that was a retry bug in notification-service, a different service and a different cause.
- Elif and Samir agreed the contract between producer and consumer is only implicit today.

## Decisions

- Write an ADR that fixes the event idempotency key contract, so the same incident cannot recur by accident (ADR-009).
- Never change an idempotency key's shape without a consumer contract test.

## Action items

- Samir Haddad: draft ADR on the idempotency key contract, due 2026-09-16.
- Elif Yildiz: consumer contract test, due 2026-09-17.
- Olivia Hartmann: publish the dedupe runbook, due 2026-09-11.
