---
id: tkt-11
kind: ticket
title: "PAY-455: Rename bankbridge to bank-connector"
date: 2026-07-10T09:00:00Z
author: Sam Okafor
participants: [Sam Okafor, Daniel Kwon, Chen Wei]
status: closed
labels: [payments, rename, bank-connector]
uri: pellucid://tickets/PAY-455
---

# PAY-455: Rename bankbridge to bank-connector

## Description

Rename the bankbridge service to bank-connector everywhere it is referenced. The Payments team owns the service, and I will run the rename.

The new name is meant to match the other connector services, which all end in a noun and then "-connector". The old name has been confusing people who are new to the codebase.

Checklist for the rename:

- [ ] Code: repository name, imports, build targets and deployment manifests
- [ ] Dashboards: every Grafana panel that mentions the service
- [ ] Docs: runbooks and the service catalogue entry
- [ ] Alerts: rule names, routes and the on-call links they carry

Target date for the cut-over is 2026-07-20. Until then the service keeps the bankbridge name in production, so this ticket does not change any running behaviour.

## Comments

**Daniel Kwon (2026-07-10):** Checklist looks complete to me. Let's run it on the 20th, when the maintenance window opens.

**Chen Wei (2026-07-11):** I can take the dashboard panels once the code has been renamed.

**Sam Okafor (2026-07-20):** Rename is done today. Code, dashboards, docs and alerts are all checked off. Closing.
