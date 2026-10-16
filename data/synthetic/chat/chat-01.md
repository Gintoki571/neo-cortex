---
id: chat-01
kind: chat
title: "#identity: scoping remember device"
date: 2026-06-04T09:00:00Z
author: Anjali Deshpande
participants: [Anjali Deshpande, Ravi Chandrasekar, Lukas Brandt, Noor Haddad]
labels: [identity, mfa, adr]
---

# #identity

**[2026-06-04 09:00] Anjali Deshpande:** morning all. quick one before the ADR meeting. Kilnworth's ops lead emailed again, their staff get the MFA prompt on the dashboard every single day. other enterprise accounts say the same
**[2026-06-04 09:03] Ravi Chandrasekar:** ugh. so is this a remember-this-device thing or do we want something broader?
**[2026-06-04 09:05] Lukas Brandt:** I'd keep it to a device flag, not anything per IP. less surprising for the security folks
**[2026-06-04 09:06] Noor Haddad:** agree on device. the real question is how long the trust lasts. a day is pointless, that is what we have now
**[2026-06-04 09:08] Anjali Deshpande:** they would be happy with weeks I think. but I don't want to promise a number before we talk to security
**[2026-06-04 09:10] Ravi Chandrasekar:** fair. scope it as device-only first and we come back with a number
**[2026-06-04 09:12] Lukas Brandt:** works for me. does the login path need to change for people who never hit MFA? I'd rather not touch that
**[2026-06-04 09:13] Noor Haddad:** it shouldn't. the check only runs when MFA would have been prompted anyway
**[2026-06-04 09:15] Ravi Chandrasekar:** good. so the open bit is the trust window, and whether admins can revoke a device
**[2026-06-04 09:16] Anjali Deshpande:** revoke yes, I'm sure customers will ask for it on day one
**[2026-06-04 09:18] Lukas Brandt:** I can sketch the storage side this week, it's one more record per login, nothing scary
**[2026-06-04 09:19] Noor Haddad:** one more record per login. noted, we should size that properly before it ships
**[2026-06-04 09:21] Ravi Chandrasekar:** ok. let's write the ADR
