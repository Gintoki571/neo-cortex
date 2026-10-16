---
id: chat-17
kind: chat
title: "#data: consumer rebalance noise"
date: 2026-09-08T11:00:00Z
author: Samir Haddad
participants: [Samir Haddad, Olivia Hartmann, Elif Yildiz]
labels: [event-pipeline, alerts]
---

# #data

**[2026-09-08 11:00] Samir Haddad:** heads up, the broker is rebalancing consumers right now, so you will see the consumer group rebalance alerts. that comes from my poll interval change yesterday, I dropped max poll interval to 60 s
**[2026-09-08 11:02] Olivia Hartmann:** ok. are the reporting consumers fine?
**[2026-09-08 11:03] Samir Haddad:** think so, the lag graphs look normal. rebalances are normal noise after a change like that
**[2026-09-08 11:05] Elif Yildiz:** ledger is fine on my side, the outbox is publishing normally
**[2026-09-08 11:07] Olivia Hartmann:** fraud-scoring also consumes from the same broker, right? they will get the same bump
**[2026-09-08 11:08] Samir Haddad:** yes, fraud-scoring, notifications and a few others. they will rebalance too, that is expected
**[2026-09-08 11:10] Olivia Hartmann:** ok. I'll keep an eye on the reporting totals anyway, they should match yesterday
**[2026-09-08 11:12] Elif Yildiz:** maybe hold the broker work until after lunch?
**[2026-09-08 11:13] Samir Haddad:** I'll wait for the rebalance to settle first, then decide
**[2026-09-08 11:15] Olivia Hartmann:** fine by me. ping me if the lag goes up
**[2026-09-08 11:16] Samir Haddad:** will do. it is usually back in ten minutes
**[2026-09-08 11:18] Elif Yildiz:** if the lag graph spikes I'll tell you straight away, not after the fact
