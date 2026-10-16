---
id: chat-03
kind: chat
title: "#incidents: found it"
date: 2026-06-16T16:30:00Z
author: Noor Haddad
participants: [Noor Haddad, Lukas Brandt, Mateo Alvarez]
labels: [incident, auth-service, session-cache]
---

# #incidents

**[2026-06-16 16:30] Noor Haddad:** found the doubling. every login now writes a device-trust record into session-cache next to the session itself. so two entries per login instead of one
**[2026-06-16 16:31] Lukas Brandt:** ...that is the remember-device work. I'm sorry, I should have sized it against the cache before we shipped
**[2026-06-16 16:32] Mateo Alvarez:** no worries. staging only has forty test users, we would never see this there. the capacity model is the gap, not you
**[2026-06-16 16:33] Noor Haddad:** the device record is short lived but it still counts against memory. cache hits the ceiling, lru evicts the live sessions. matches the graph shape exactly
**[2026-06-16 16:35] Lukas Brandt:** yeah. the device record sits under the same key prefix so it hides in the counts. the key dashboard looked fine but it counts per user, not per entry
**[2026-06-16 16:37] Mateo Alvarez:** ok. short term we need headroom, long term the capacity model has to count those records. Beatrice, can you give us a number for how much memory the cache needs?
**[2026-06-16 16:39] Noor Haddad:** I'd rather cut the duplicate, but the feature needs a record per login. let's talk tomorrow
**[2026-06-16 16:41] Lukas Brandt:** I'll write up what the device record is actually used for, so we know whether it can be smaller
**[2026-06-16 16:43] Mateo Alvarez:** thanks both. don't beat yourself up lukas, this one is easy to miss. we'll go through it properly in the postmortem
**[2026-06-16 16:44] Noor Haddad:** agreed. first thing tomorrow then
**[2026-06-16 16:46] Lukas Brandt:** I'll also check whether the device record can expire faster without breaking the remember window
**[2026-06-16 16:48] Noor Haddad:** good. that is the question to answer tomorrow
