---
id: tkt-15
kind: ticket
title: "PAY-462: Rename checklist follow-up"
date: 2026-07-26T09:00:00Z
author: Sam Okafor
participants: [Sam Okafor, Daniel Kwon, Sofia Marchetti]
status: closed
labels: [payments, process, rename, checklist]
uri: pellucid://tickets/PAY-462
---

# PAY-462: Rename checklist follow-up

## Description

Follow-up from INC-02. The checklist we used for the bankbridge rename covered code, dashboards, docs and alerts. It did not cover config namespaces. The Tidewater override was stored under the old prefix, so the renamed service could not find it, and nothing on the checklist would have caught that.

The rename checklist template needs to include:

- Config namespaces, including every key prefix the service reads or writes.
- Alerts and dashboards, checked against the new name.
- Docs and the service catalogue, as it does today.

Sam Okafor updates the template and walks the Payments team through it before the next rename.

## Comments

**Daniel Kwon (2026-07-26):** Agreed. Put the namespace step first, not last. It is the one people skip.

**Sofia Marchetti (2026-07-26):** Please make the step apply to any service that reads config, not only the ones being renamed.

**Sam Okafor (2026-07-26):** Template is updated and linked from the Payments runbook. Closing.
