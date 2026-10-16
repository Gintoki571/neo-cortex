---
id: tkt-06
kind: ticket
title: "IDN-230: Capacity model must count per-login records"
date: 2026-06-19T09:00:00Z
author: Ravi Chandrasekar
participants: [Ravi Chandrasekar, Imani Okoye, Lukas Brandt]
status: in-progress
labels: [identity, session-cache, capacity]
uri: pellucid://tickets/IDN-230
---

# IDN-230: Capacity model must count per-login records

## Description

Follow-up from INC-01. Any feature that adds per-login records to session-cache has to update the session-cache capacity model before it ships. The remember-device work doubled the number of entries per login, and the capacity model still assumed one record per login, which is why nobody saw the memory problem coming.

Tasks:

- Add a per-login record count to the capacity sheet.
- Add a line to the identity release checklist asking whether a change writes per-login data.
- Write a short note in the identity wiki on how to estimate entries per login.

Picked up by Imani Okoye. This is her first ticket on the team, so please be patient with questions and point her at the runbook where it helps.

## Comments

**Imani Okoye (2026-06-19):** Thanks Ravi. I will start with the capacity sheet and send a draft by Monday.

**Lukas Brandt (2026-06-19):** Happy to walk you through how the device record gets written. Ping me when you get to that part.

**Ravi Chandrasekar (2026-06-19):** Good. The sheet lives in the identity folder. Ask if anything is unclear.
