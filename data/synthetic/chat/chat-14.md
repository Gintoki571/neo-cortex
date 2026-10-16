---
id: chat-14
kind: chat
title: "#eng: two approvers for config"
date: 2026-08-14T15:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Grace Nakamura, Chen Wei, Viktor Sokolov]
labels: [config, policy]
---

# #eng

**[2026-08-14 15:00] Mateo Alvarez:** new rule as of today: production config changes need two approvals before they go out, and config-service will enforce it. I proposed it, Tobias signed it off, Grace approved
**[2026-08-14 15:02] Viktor Sokolov:** two approvals for a one-line change? ok, but yeah, we used to push alone. this is a big change for us
**[2026-08-14 15:03] Grace Nakamura:** it is a big change for Platform, that is the point. nobody should be able to ship prod config solo, not even me
**[2026-08-14 15:05] Viktor Sokolov:** fair. I just did not expect to see it land so suddenly
**[2026-08-14 15:06] Chen Wei:** ok. I'll follow the new process
**[2026-08-14 15:07] Mateo Alvarez:** thanks Chen. this is not about anyone in particular
**[2026-08-14 15:08] Viktor Sokolov:** yeah, until now any of us on Platform could push a config change alone and nobody batted an eye. that is a habit to break
**[2026-08-14 15:10] Grace Nakamura:** agreed. the approval flow is already in config-service, it just needs a second approver id
**[2026-08-14 15:12] Mateo Alvarez:** I'll post the steps in the platform channel today so nobody gets stuck
**[2026-08-14 15:13] Chen Wei:** makes sense
**[2026-08-14 15:14] Grace Nakamura:** good. questions to me or Mateo, we're both around this afternoon
**[2026-08-14 15:16] Viktor Sokolov:** fine by me. I'd rather go slow for a while than rush the next change
