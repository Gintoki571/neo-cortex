---
id: chat-05
kind: chat
title: "#eng: do we freeze Fridays?"
date: 2026-06-28T13:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Grace Nakamura, Tessa Ngu, Tobias Wren]
labels: [deploys, process]
---

# #eng

**[2026-06-28 13:00] Mateo Alvarez:** I'll say it plainly. I think we stop production deploys on Fridays. the Friday evening deploy on the 26th cost us the whole weekend
**[2026-06-28 13:02] Grace Nakamura:** I hear you, but a freeze means fixes wait until monday. what if the fix is urgent?
**[2026-06-28 13:04] Mateo Alvarez:** then the fix is urgent and we deploy it with someone on call who is not on a plane. the default should just be no
**[2026-06-28 13:05] Tessa Ngu:** mild objection from me. some of our notification changes are small and low risk, and a blanket ban feels heavy. could we do the exceptions by hand?
**[2026-06-28 13:07] Grace Nakamura:** exceptions by hand sounds like how we ended up with no rule at all
**[2026-06-28 13:08] Tessa Ngu:** fair. I'm not fighting it, I just don't want the small stuff stuck
**[2026-06-28 13:10] Mateo Alvarez:** small stuff can go Monday to Thursday. that is most of the week
**[2026-06-28 13:12] Tobias Wren:** I'm fine with a freeze if it is written down. Mateo, can you write it up as an ADR so we can point at it next time?
**[2026-06-28 13:14] Mateo Alvarez:** will do. I'll draft it this week
**[2026-06-28 13:15] Grace Nakamura:** put the canary requirement in it too, we keep skipping that part
**[2026-06-28 13:17] Tobias Wren:** agreed. and a rollback step while you're at it
**[2026-06-28 13:20] Tessa Ngu:** ok, I'll stop arguing. the weekend was rough for all of us
**[2026-06-28 13:21] Mateo Alvarez:** appreciated. thanks for pushing back, it made the proposal better
