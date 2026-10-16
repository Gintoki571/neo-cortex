---
id: tkt-25
kind: ticket
title: "DATA-325: Dedupe backfill executed"
date: 2026-09-10T15:00:00Z
author: Olivia Hartmann
participants: [Olivia Hartmann, Yusuf Demir]
status: closed
labels: [reporting-service, backfill, data]
uri: pellucid://tickets/DATA-325
---

# DATA-325: Dedupe backfill executed

## Description

Record of the dedupe backfill I ran for the INC-04 duplicates. Owner: Olivia Hartmann.

Steps taken:

1. On 2026-09-09 the idempotency key format change in ledger-service was reverted, so new events carry the original key format again.
2. On 2026-09-10 I ran the dedupe backfill in reporting-service over the affected period. I did a dry run first, checked its output against a sample of invoices, and then ran it for real.
3. Re-ran the totals check for Northgate Freight. The totals now match the ledger.

Affected scope: about 3,000 invoices had doubled totals. The backfill removed the duplicate contributions for each of them and left every other invoice untouched.

Nothing was deleted from the ledger. All changes were made inside reporting-service.

## Comments

**Yusuf Demir (2026-09-10):** Thanks, Olivia. Please send the numbers to Anjali for the Northgate note.

**Olivia Hartmann (2026-09-10):** Sent. Totals match on the sample and on the full month.
