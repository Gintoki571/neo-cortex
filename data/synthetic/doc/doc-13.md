---
id: doc-13
kind: doc
title: "Onboarding a customer bank to bank-connector"
date: 2026-08-03T09:00:00Z
author: Sam Okafor
participants: [Sam Okafor, Chen Wei]
labels: [how-to, bank-connector, config-service, onboarding]
uri: pellucid://wiki/howto/onboard-bank
---

# Onboarding a customer bank to bank-connector

This how-to walks through adding a new customer bank to bank-connector, so that payments and ACH batches for that bank are sent with the right settings. I own the service. Chen Wei is the second pair of eyes on config work, so loop him in when the store behaves unexpectedly.

## What a bank needs

Each bank that we send money to has a set of settings: its identifier, its same-day ACH cutoff and any override for a specific customer. The defaults apply unless the bank has its own values. For same-day ACH the default cutoff is 14:00 ET, so only write an override where the bank really differs.

## Step 1: add the overrides

Per-bank settings live in config-service under the bank's own prefix:

`bank_connector.banks.<id>.*`

Choose an identifier that is short, lowercase and stable, because it becomes part of every key for that bank. Add only the keys the bank needs. Each key you add is a value someone else will have to understand later.

## Step 2: add a contract test

Every bank needs a contract test before it goes live. The test sends a sample batch through the connector and checks that the settings you wrote are the ones that get used. Run it against the sandbox first, then against the bank's test endpoint if it has one.

## Step 3: review

Changes to bank settings are sensitive because they decide when money moves. Ask Payments for a review, and wait for it. Plan bank changes for a working day when the reviewers are around.

## Note on the name

The connector was formerly bankbridge. Its old name still shows up in some logs and in older tickets, so search for both when you investigate a payment from before the rename.

## Checklist

- Settings written under the bank's prefix.
- Contract test passing in the sandbox.
- Review from Payments recorded.
- Onboarding noted in the customer's account sheet.
