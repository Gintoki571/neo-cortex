---
id: tkt-13
kind: ticket
title: "INC-02: Tidewater same-day ACH missed cutoff"
date: 2026-07-24T17:30:00Z
author: Sam Okafor
participants: [Sam Okafor, Chen Wei, Daniel Kwon]
status: in-progress
labels: [incident, bank-connector, config, tidewater]
uri: pellucid://tickets/INC-02
---

# INC-02: Tidewater same-day ACH missed cutoff

## Description

Incident: Tidewater Credit Union same-day ACH batches missed their cutoff on 2026-07-24 and settled the next business day. This is the problem reported in SUP-341.

What we know so far:

- bank-connector applied the default same-day cutoff of 14:00 ET to the Tidewater batches. The 17:30 ET override that Tidewater has in their agreement did not take effect.
- The override does exist in config-service, but under the old key prefix `bankbridge.banks.tidewater.cutoff`. bank-connector reads `bank_connector.banks.tidewater.cutoff`, finds nothing there, and falls back to the default.
- Batches submitted after 14:00 ET but before 17:30 ET were therefore treated as next-day.

Next steps: get the override readable under the key bank-connector actually reads, verify it on a test batch, and then work out with Tidewater how to resubmit the late batches.

## Comments

**Chen Wei (2026-07-24):** I can see the old prefix in config-service. Do you want me to add an alias, or do you want to migrate the keys yourself?

**Sam Okafor (2026-07-24):** Both, in that order. I will do the migration once the alias is live.

**Daniel Kwon (2026-07-24):** Let's update Tidewater every hour until the batches are settled.
