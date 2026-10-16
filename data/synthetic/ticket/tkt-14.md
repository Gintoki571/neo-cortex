---
id: tkt-14
kind: ticket
title: "CFG-4402: Alias old bankbridge keys, migrate overrides"
date: 2026-07-25T09:00:00Z
author: Chen Wei
participants: [Chen Wei, Sam Okafor]
status: closed
labels: [config, bank-connector, prod]
uri: pellucid://tickets/CFG-4402
---

# CFG-4402: Alias old bankbridge keys, migrate overrides

## Description

Production config change to fix the Tidewater cutoff lookup. Two steps, split between two people.

1. Chen Wei: add an alias mapping in config-service so that reads of the old `bankbridge.*` keys resolve to the matching `bank_connector.*` keys. This lets bank-connector see the Tidewater override straight away, without waiting for the migration.
2. Sam Okafor: migrate the overrides from the old prefix to the new one, confirm that bank-connector picks up the 17:30 ET cutoff for Tidewater, and manually resubmit the Tidewater batches that settled late.

Step 1 goes first so that Tidewater's batches are not waiting on the migration. Step 2 is only complete once the Tidewater cutoff has been checked on a test batch, before anything else is resubmitted.

## Comments

**Sam Okafor (2026-07-25):** Migration is done and bank-connector reads the 17:30 ET cutoff for Tidewater. I resubmitted the late batches by hand and Tidewater has confirmed on their side.

**Chen Wei (2026-07-25):** Alias is live in prod. Closing.
