---
id: chat-06
kind: chat
title: "#platform: gateway limit bump"
date: 2026-07-09T10:00:00Z
author: Viktor Sokolov
participants: [Viktor Sokolov, Grace Nakamura, Anjali Deshpande]
labels: [api-gateway, rate-limit]
---

# #platform

**[2026-07-09 10:00] Viktor Sokolov:** announcing: the per-tenant limit on api-gateway goes from 100 to 250 req/s, effective now. this is for Orchard & Vane's seasonal import, they start tomorrow
**[2026-07-09 10:02] Anjali Deshpande:** thank you! they have been asking since last week, they will be relieved
**[2026-07-09 10:03] Grace Nakamura:** keep an eye on auth-service latency for the first few days too, they will all be hitting it harder
**[2026-07-09 10:05] Viktor Sokolov:** yes, I'll watch the gateway dashboards. the old limit of 100 has been fine for a year, so this is a 2.5x bump, not a rewrite
**[2026-07-09 10:06] Anjali Deshpande:** is it just the one tenant or everyone?
**[2026-07-09 10:07] Viktor Sokolov:** only the tenant that asked. the limit is per tenant, so everyone else stays where they are
**[2026-07-09 10:09] Grace Nakamura:** good. Anjali, can you still tell the customer to start the import in smaller batches?
**[2026-07-09 10:10] Anjali Deshpande:** will do. they plan to run it overnight, so they may not need that
**[2026-07-09 10:12] Viktor Sokolov:** fine either way. I'll post the numbers after the first night
**[2026-07-09 10:14] Anjali Deshpande:** thanks Viktor, you're the best
**[2026-07-09 10:15] Grace Nakamura:** agreed, nice work
**[2026-07-09 10:17] Anjali Deshpande:** I'll tell the account team, they will be glad it is sorted
