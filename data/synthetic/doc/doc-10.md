---
id: doc-10
kind: doc
title: "Runbook: dedupe and backfill reporting totals"
date: 2026-09-11T09:00:00Z
author: Olivia Hartmann
participants: [Olivia Hartmann, Samir Haddad, Yusuf Demir]
labels: [runbook, reporting-service, reportctl, data]
uri: pellucid://wiki/runbooks/reporting-dedupe
---

# Runbook: dedupe and backfill reporting totals

This runbook explains how to remove duplicate rows from reporting-service totals and rebuild the affected figures. I wrote the reportctl tooling it depends on, and I own reporting-service. Read the whole page before you run anything, because the dedupe is not reversible without a restore.

## When to use it

Use it when a report shows totals that are higher than the underlying invoices can explain, and the cause is a replay of events that were already counted. The replay earlier this week is the case that prompted this page. If you are not sure whether duplicates are the cause, compare a sample of invoice IDs against the ledger before going further.

## The command

Dedupe is run with reportctl over a date range, keyed on the transaction ID:

`reportctl dedupe --from DATE --to DATE --key txn_id`

The dates are inclusive and should cover only the window where duplicates appeared. Keep the range narrow. A wide range takes longer and touches correct data that happens to share a day with the bad data.

## Always dry-run first

Add `--dry-run` to the first run and read the output carefully. It lists how many rows would be removed per day, and the numbers should match what you saw in the report. If they do not, stop. Do not remove rows to make the numbers look right.

Only run the real command after the dry run has been reviewed by a second person. Samir Haddad or Yusuf Demir are the usual reviewers.

## Backfill

Once the dedupe is done, the affected daily totals need to be recalculated. Recalculate the totals for the same date range once the rows are clean, then check a few of them against the ledger.

## Afterwards

Write down the date range, the number of rows removed and the reviewer's name in the data channel. Tell finance which reports changed, so that nobody quotes an old figure in a board pack.
