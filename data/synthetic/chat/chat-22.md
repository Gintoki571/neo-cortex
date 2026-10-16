---
id: chat-22
kind: chat
title: "#eng: approval fatigue"
date: 2026-10-05T14:00:00Z
author: Chen Wei
participants: [Chen Wei, Grace Nakamura, Viktor Sokolov, Mateo Alvarez]
labels: [config, approvals, process]
---

# #eng

**[2026-10-05 14:00] Chen Wei:** third prod config change this week stuck waiting on a second approver. the queue is killing me
**[2026-10-05 14:03] Viktor Sokolov:** same here. mine sat for almost four hours yesterday
**[2026-10-05 14:05] Chen Wei:** it isn't the reviewers, it's that nobody is online at the same time as you
**[2026-10-05 14:07] Grace Nakamura:** how long are they really taking? I keep hearing "hours" with no numbers attached
**[2026-10-05 14:10] Mateo Alvarez:** pulled the approval table. median wait under two approvals is 3.5 hours
**[2026-10-05 14:11] Grace Nakamura:** that's a lot for a one-line change. how many of those are actually risky?
**[2026-10-05 14:13] Viktor Sokolov:** most of them aren't. a timeout tweak should not need a second person awake at 9 pm
**[2026-10-05 14:15] Mateo Alvarez:** agree on size. I'd rather validate the file automatically and keep the human look for the risky keys
**[2026-10-05 14:18] Grace Nakamura:** what counts as risky? I don't want a list nobody updates
**[2026-10-05 14:20] Chen Wei:** bounds on the numeric keys would catch most of the dumb mistakes. a validator is cheaper than a reviewer
**[2026-10-05 14:24] Mateo Alvarez:** yes, bounds plus a diff summary on the ticket. then the second approver is a skim, not a hunt
**[2026-10-05 14:27] Grace Nakamura:** ok. I'll take it to Tobias before we change anything. Viktor, can you find the cases where the second approver actually caught something?
**[2026-10-05 14:29] Viktor Sokolov:** will try. not holding my breath
**[2026-10-05 14:31] Grace Nakamura:** fair. thanks all
