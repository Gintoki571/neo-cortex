---
id: tkt-28
kind: ticket
title: "PLAT-715: Update CODEOWNERS after reorg"
date: 2026-09-02T09:00:00Z
author: Grace Nakamura
participants: [Grace Nakamura, Mateo Alvarez, Lukas Brandt]
status: closed
labels: [platform, codeowners, session-cache]
uri: pellucid://tickets/PLAT-715
---

# PLAT-715: Update CODEOWNERS after reorg

## Description

The session-cache handover went live yesterday, but the CODEOWNERS file still routes reviews for that code to the old Identity owner. Update the entry for `services/session-cache/` so Mateo Alvarez is the primary reviewer from today.

Details:

- Path: `services/session-cache/`
- New primary reviewer: Mateo Alvarez (Platform)
- Previous primary: Lukas Brandt (Identity)
- Effective: 2026-09-02

Lukas is moving teams but is not leaving the sharding layer behind. He has agreed to stay on as an informal reviewer for changes to that code, so don't drop him from the list of people who look at the module. We can make him a formal secondary reviewer later if it turns out we need that.

## Comments

**Mateo Alvarez (2026-09-02):** Merged. I also asked Beatrice to make sure the on-call runbook links to the new owner.

**Lukas Brandt (2026-09-02):** Happy to keep reviewing the sharding code. Ping me on anything that touches the slot mapping.

**Grace Nakamura (2026-09-02):** The change is on main. Lukas, thanks for staying on. Closing this.
