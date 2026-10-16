---
id: chat-12
kind: chat
title: "#incidents: rollback and root cause"
date: 2026-08-10T09:55:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Chen Wei, Noor Haddad]
labels: [incident, config]
---

# #incidents

**[2026-08-10 09:50] Mateo Alvarez:** rolling back the 09:05 config push now. `cfgctl rollback` is in, give it 30 s
**[2026-08-10 09:51] Noor Haddad:** introspection p99 is dropping, timeouts falling off a cliff
**[2026-08-10 09:52] Mateo Alvarez:** 502s are gone on my side. keeping the channel open until the error budget panel is green
**[2026-08-10 09:53] Mateo Alvarez:** green. all clear 09:53
**[2026-08-10 09:54] Chen Wei:** that was me. CFG-4411. I meant 800 -> 1000 and typed 80, one zero short
**[2026-08-10 09:54] Noor Haddad:** 80 ms is far below p50 for introspection under load, so everything timed out. not a bug in auth-service
**[2026-08-10 09:55] Chen Wei:** nobody looked at it before it went out, I pushed it myself. config-service lets you do that
**[2026-08-10 09:56] Mateo Alvarez:** yeah. that is the thing to fix, not you. we'll talk in the postmortem
**[2026-08-10 09:57] Chen Wei:** sorry everyone
**[2026-08-10 09:58] Noor Haddad:** you caught it fast once we looked. let's get a validator in somewhere
**[2026-08-10 09:59] Mateo Alvarez:** writing the ticket now. thanks both
