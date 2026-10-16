---
id: chat-02
kind: chat
title: "#incidents: web-dashboard logouts (live)"
date: 2026-06-16T14:20:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Jonas Albrecht, Noor Haddad, Beatrice Oyelaran]
labels: [incident, session-cache, auth-service]
---

# #incidents

**[2026-06-16 14:20] Mateo Alvarez:** ok we have a live one. web-dashboard users getting kicked to login over and over, started around 12:20 UTC, so about two hours now
**[2026-06-16 14:22] Jonas Albrecht:** tickets piling up, mostly "why am I logged out every five min". can we give cs a line to send?
**[2026-06-16 14:23] Mateo Alvarez:** sure: "we are looking into a sign-in problem, please log in again, sorry". post to the status page once Noor confirms scope
**[2026-06-16 14:25] Noor Haddad:** scope looks like all tenants, not one. auth logs show session lookups coming back empty for sessions that were valid ten min ago
**[2026-06-16 14:27] Beatrice Oyelaran:** the evictions panel on the session-cache dash is up, look at it. evicted keys/sec went from zero to a wall around 12:10
**[2026-06-16 14:28] Mateo Alvarez:** thats the one. redis is at its memory ceiling, policy is allkeys-lru so it drops live sessions to make room. makes sense
**[2026-06-16 14:30] Noor Haddad:** why is memory up though? we shipped auth yesterday but I don't see how that alone fills it
**[2026-06-16 14:31] Beatrice Oyelaran:** key counts per prefix would tell us. entries per login look way up to me, i'll check
**[2026-06-16 14:33] Mateo Alvarez:** ok do that. don't touch the shards until we know why, a restart just moves the problem
**[2026-06-16 14:35] Jonas Albrecht:** a big enterprise customer is asking for an ETA. what do I say
**[2026-06-16 14:36] Mateo Alvarez:** honest answer: we know roughly where it is, fix in progress, no ETA yet. don't promise a time
**[2026-06-16 14:38] Noor Haddad:** beatrice?
**[2026-06-16 14:41] Beatrice Oyelaran:** key count per login is way up since yesterday's release. not sure yet which key family. still digging
**[2026-06-16 14:44] Mateo Alvarez:** good. ping when you know. keeping this channel open
**[2026-06-16 14:46] Noor Haddad:** logouts still coming in. not getting worse, not better
**[2026-06-16 14:48] Jonas Albrecht:** cs has the line now. about forty tickets so far
