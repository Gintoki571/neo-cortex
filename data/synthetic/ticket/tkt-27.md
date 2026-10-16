---
id: tkt-27
kind: ticket
title: "SUP-401: Bluepeak CSV export timing out"
date: 2026-08-20T09:00:00Z
author: Jonas Albrecht
participants: [Jonas Albrecht, Olivia Hartmann]
status: closed
labels: [support, reporting-service, csv-export]
uri: pellucid://tickets/SUP-401
---

# SUP-401: Bluepeak CSV export timing out

## Description

Bluepeak Logistics reports that their CSV export from reporting-service times out when they pick a long date range. Shorter ranges, a few weeks at most, download fine, so this looks like the query and not the file writer.

Customer context: Bluepeak pulls CSV exports on a schedule and drops them into their own month-close spreadsheets. When an export times out they download it in pieces by hand, which takes their finance team most of a morning.

Steps so far:

- Reproduced with a 13-month range on the staging copy. The request ran past the timeout.
- Pulled the query plan. It scans every invoice line for the account and applies the date filter last, instead of using the date index first.
- The customer confirmed the range they actually need is the full financial year, so shorter ranges are not a workaround.

## Comments

**Olivia Hartmann (2026-08-20):** Got it. The date filter was being applied after the join, which is why it gets worse the longer the range. The fix is a small move plus an index hint. Testing against a copy of their data now.

**Jonas Albrecht (2026-08-20):** Thanks Olivia. I told the customer the fix is in review and they should keep doing the manual downloads until it lands. Will send them the new file once it does.

**Olivia Hartmann (2026-08-20):** Verified on the copy: the 13-month export finishes well under the limit and the row count matches the old result for a shorter range. Deployed to production, closing this.
