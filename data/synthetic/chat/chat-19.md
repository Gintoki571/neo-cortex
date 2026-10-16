---
id: chat-19
kind: chat
title: "#platform: limit now 180"
date: 2026-09-14T10:15:00Z
author: Viktor Sokolov
participants: [Viktor Sokolov, Noor Haddad, Beatrice Oyelaran]
labels: [api-gateway, rate-limit, load-test]
---

# #platform

**[2026-09-14 10:15] Viktor Sokolov:** we lowered the per-tenant limit on api-gateway from 250 to 180 req/s as of now. reason is the load test we ran yesterday
**[2026-09-14 10:16] Noor Haddad:** yeah. at 250 auth-service saturates, we saw latency climb hard in the test. 180 leaves some headroom
**[2026-09-14 10:18] Beatrice Oyelaran:** dashboards look fine for now. is it still only the one tenant on the high limit?
**[2026-09-14 10:19] Viktor Sokolov:** yes, only that tenant. everyone else never moved off the default
**[2026-09-14 10:21] Noor Haddad:** the load test was ugly. at 250 the auth p99 went through the roof
**[2026-09-14 10:22] Viktor Sokolov:** right. so 180 is the number until auth is doing better
**[2026-09-14 10:24] Beatrice Oyelaran:** can we get the test results into the ticket?
**[2026-09-14 10:25] Viktor Sokolov:** yes, I'll attach the graphs this afternoon
**[2026-09-14 10:27] Noor Haddad:** good. ping me when the tenant reports anything
**[2026-09-14 10:28] Viktor Sokolov:** will do
**[2026-09-14 10:30] Beatrice Oyelaran:** nice work, both of you
**[2026-09-14 10:31] Noor Haddad:** I'll check the auth p99 again tomorrow morning and post it here
