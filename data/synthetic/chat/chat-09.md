---
id: chat-09
kind: chat
title: "#incidents: Tidewater settlements"
date: 2026-07-24T17:50:00Z
author: Jonas Albrecht
participants: [Jonas Albrecht, Sam Okafor, Daniel Kwon, Anjali Deshpande]
labels: [incident, ach, tidewater]
---

# #incidents

**[2026-07-24 17:50] Jonas Albrecht:** urgent. Tidewater Credit Union called, their ACH batches from today settled on the next business day. they expected same-day and they are furious
**[2026-07-24 17:52] Anjali Deshpande:** how many batches, and is it all of their clients or one?
**[2026-07-24 17:53] Jonas Albrecht:** they said several batches, all flagged same-day. I've asked for the batch ids
**[2026-07-24 17:55] Daniel Kwon:** is this the cutoff thing again? they have a custom cutoff with us, right?
**[2026-07-24 17:56] Jonas Albrecht:** yes, they have an override on the cutoff time, 17:30 Eastern. that is why they were on same-day in the first place
**[2026-07-24 17:58] Sam Okafor:** I'm on it. checking the bank-connector logs first, not guessing
**[2026-07-24 18:00] Anjali Deshpande:** please keep Tidewater posted. Jonas, tell them we are investigating and will give an update within the hour
**[2026-07-24 18:01] Jonas Albrecht:** will do
**[2026-07-24 18:04] Daniel Kwon:** Sam, do you need a hand? I'm free until seven
**[2026-07-24 18:05] Sam Okafor:** maybe later. I want to see the logs first
**[2026-07-24 18:08] Sam Okafor:** confirmed the batches are tagged same-day. the connector is not treating them that way. still working out why
**[2026-07-24 18:10] Anjali Deshpande:** ok. good that we know where to look. thanks
**[2026-07-24 18:12] Jonas Albrecht:** calling them back now
