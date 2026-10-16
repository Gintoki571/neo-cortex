---
id: chat-13
kind: chat
title: "#identity: 300 seconds it is"
date: 2026-08-12T10:30:00Z
author: Noor Haddad
participants: [Noor Haddad, Ravi Chandrasekar, Tobias Wren]
labels: [session, security, compliance]
---

# #identity

**[2026-08-12 10:30] Noor Haddad:** heads up, the auditors' finding on idle sessions is forcing our hand. session TTL is 300 seconds as of about ten minutes ago, not 900
**[2026-08-12 10:32] Ravi Chandrasekar:** ok. what is the finding in plain words? I need to explain it to product
**[2026-08-12 10:33] Noor Haddad:** sessions on payment-capable accounts stay logged in when idle for longer than five minutes. the auditors say that is an exception we cannot justify
**[2026-08-12 10:35] Tobias Wren:** I signed off on this one, Noor wrote it up well. it should close the finding at the next checkpoint
**[2026-08-12 10:36] Ravi Chandrasekar:** UX impact? people who step away for a coffee will land on the login page
**[2026-08-12 10:38] Noor Haddad:** yes. activity still refreshes the session, so people actually using the dashboard won't see it. it is the walk-away case only
**[2026-08-12 10:40] Ravi Chandrasekar:** ok. support will need a canned reply, I'll get that going
**[2026-08-12 10:41] Noor Haddad:** thanks. the reply should just say the session timed out after inactivity, nothing more
**[2026-08-12 10:43] Tobias Wren:** good. Noor, please add the change to the session-cache runbook page too
**[2026-08-12 10:45] Noor Haddad:** will do
**[2026-08-12 10:46] Ravi Chandrasekar:** any risk on the memory side?
**[2026-08-12 10:47] Noor Haddad:** lower, if anything. shorter TTL means fewer live entries. good news for the cache
**[2026-08-12 10:49] Tobias Wren:** great, thanks all
