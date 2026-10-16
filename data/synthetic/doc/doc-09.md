---
id: doc-09
kind: doc
title: "Runbook: resubmitting an ACH batch"
date: 2026-07-27T09:00:00Z
author: Sam Okafor
participants: [Sam Okafor, Daniel Kwon, Jonas Albrecht]
labels: [runbook, bank-connector, ach, payments]
uri: pellucid://wiki/runbooks/ach-resubmit
---

# Runbook: resubmitting an ACH batch

This covers what to do when an ACH batch has missed its settlement window and needs to go again the same business day. I own bank-connector, so this is my runbook, but anyone on Payments can use it. Last week's late batches are the reason it was written down.

## Before you touch anything

Work out which customer the batch belongs to, and find the cutoff that applies to them. Most customers use the default same-day ACH cutoff of 14:00 ET. Tidewater Credit Union has its own override of 17:30 ET, so a batch that looks late for the default may still be in time for them.

A same-day resubmission is only allowed before the cutoff for that customer. After it, the batch goes out next business day, and forcing it earlier will not help and will confuse the bank.

## Getting the customer's agreement

Do not resubmit until the customer contact has acknowledged that the batch should go same day. Jonas Albrecht on support usually handles that conversation. Ask for the acknowledgement in writing and keep it with the batch record.

## Resubmitting

The command is:

`bankctl resubmit --batch <id> --same-day`

Run it only when both conditions hold: the customer has acknowledged, and it is still before their cutoff. Once the cutoff has passed, do not try to force the batch through.

## After it goes

Check the batch status in the bank console until it shows as accepted by the bank. Then post the batch ID and the time in the Payments channel so the account team can tell the customer. If the batch is rejected, do not resubmit again on your own; raise it with Daniel Kwon, who owns the payment path.

## Common mistakes

- Using the default cutoff for a customer with an override.
- Resubmitting before the customer has said yes.
- Forgetting the `--same-day` flag, which sends the batch to the next business day instead.
