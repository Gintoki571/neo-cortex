---
id: chat-04
kind: chat
title: "#platform: TTL change applied"
date: 2026-06-18T11:00:00Z
author: Beatrice Oyelaran
participants: [Beatrice Oyelaran, Noor Haddad, Mateo Alvarez]
labels: [session-cache, config]
---

# #platform

**[2026-06-18 11:00] Beatrice Oyelaran:** heads up, session.ttl_seconds is now 900. it was 3600 until a few minutes ago, change went through config-service
**[2026-06-18 11:01] Noor Haddad:** nice. so sessions now expire after fifteen minutes instead of an hour
**[2026-06-18 11:02] Beatrice Oyelaran:** yes. the point is to free memory under the eviction pressure, not to log people out faster
**[2026-06-18 11:03] Mateo Alvarez:** did anyone check the sliding refresh still works? active users should not get bumped
**[2026-06-18 11:05] Beatrice Oyelaran:** checked on staging. active sessions refresh on each call like before. I tried it with two browser tabs open
**[2026-06-18 11:06] Noor Haddad:** login metrics look healthy so far. success rate is flat and no spike in re-logins
**[2026-06-18 11:08] Mateo Alvarez:** good. keep an eye on the evictions panel for the afternoon
**[2026-06-18 11:09] Beatrice Oyelaran:** already on it. the eviction line dropped a lot in the last twenty minutes
**[2026-06-18 11:12] Noor Haddad:** sweet. I'll post again after lunch
**[2026-06-18 11:13] Mateo Alvarez:** thanks beatrice
**[2026-06-18 11:15] Beatrice Oyelaran:** anytime. I'll update the runbook page once it has been stable for a bit
**[2026-06-18 11:17] Noor Haddad:** I'll watch the auth dashboards too, they take the hit whenever sessions churn
