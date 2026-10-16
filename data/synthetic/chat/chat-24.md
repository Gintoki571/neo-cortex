---
id: chat-24
kind: chat
title: "#random: lunch and DNS"
date: 2026-08-26T12:00:00Z
author: Arjun Malhotra
participants: [Arjun Malhotra, Tessa Ngu, Hugo Tremblay, Kofi Mensah]
labels: [random, social]
---

# #random

**[2026-08-26 12:00] Arjun Malhotra:** lunch at the noodle place or do we want to be adventurous
**[2026-08-26 12:02] Tessa Ngu:** noodles. I'm not doing another salad bowl this week
**[2026-08-26 12:03] Hugo Tremblay:** noodles. Kofi, are you coming or still in the model notebook?
**[2026-08-26 12:05] Kofi Mensah:** coming, give me five minutes. the eval run is slow
**[2026-08-26 12:06] Arjun Malhotra:** did anyone listen to the chess engine podcast from Thursday?
**[2026-08-26 12:08] Tessa Ngu:** first half was great, then they lost me in the opening book section
**[2026-08-26 12:09] Hugo Tremblay:** I skipped to the end. the guest got about four minutes
**[2026-08-26 12:12] Kofi Mensah:** random question from the status page thread: why does the DNS record take minutes to pick up changes? I thought we set it lower
**[2026-08-26 12:14] Arjun Malhotra:** the status page record has a TTL of 300 seconds. that's the cache lifetime, not a bug
**[2026-08-26 12:15] Tessa Ngu:** ok, so if I edit it now people see it in five minutes. fine by me
**[2026-08-26 12:17] Hugo Tremblay:** also my e2e test is flaky again. the "session" it logs in with dies halfway through the run. no idea which session
**[2026-08-26 12:18] Arjun Malhotra:** in the Playwright suite it's usually the fixture, not real sessions. don't spend an hour on it, it's almost always a wait problem
**[2026-08-26 12:20] Kofi Mensah:** wait, which Haddad owns what again? Noor or Samir? I keep swapping them
**[2026-08-26 12:21] Tessa Ngu:** I mix them up too. ask in #eng, someone there will know for sure
**[2026-08-26 12:23] Hugo Tremblay:** lol Kofi, the whole company gets the two Haddads wrong
**[2026-08-26 12:25] Kofi Mensah:** ok, going. noodles at 12:30?
**[2026-08-26 12:26] Arjun Malhotra:** 12:30 works, see you in the lobby
