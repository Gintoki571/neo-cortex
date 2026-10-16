---
id: chat-20
kind: chat
title: "#data: idempotency key rules"
date: 2026-09-16T10:00:00Z
author: Samir Haddad
participants: [Samir Haddad, Elif Yildiz, Sofia Marchetti, Yusuf Demir]
labels: [data, idempotency, adr]
---

# #data

**[2026-09-16 10:00] Samir Haddad:** before I write the ADR, quick check. I'm proposing the event key is just txn_id, nothing appended. the INC-04 lesson is clear to me
**[2026-09-16 10:02] Elif Yildiz:** agreed, no suffixes. the attempt counter is what broke the consumers. I'd rather not have any counter in the key at all
**[2026-09-16 10:04] Yusuf Demir:** what is the failure mode we are protecting against? I want it written down
**[2026-09-16 10:05] Samir Haddad:** consumers dedupe on the key. if the key changes shape, a republished event looks new and gets counted twice. that is what happened
**[2026-09-16 10:07] Sofia Marchetti:** ok. and what stops this next time? a comment in the code won't do it
**[2026-09-16 10:08] Samir Haddad:** agreed. a consumer contract test that fails if the shape changes. that is the lesson I want written in the ADR
**[2026-09-16 10:10] Sofia Marchetti:** agree. the contract test is the bit that counts
**[2026-09-16 10:11] Elif Yildiz:** I can write the test once the ADR is in. it's a small one
**[2026-09-16 10:13] Yusuf Demir:** ok. and it's immutable? once it is set, it doesn't change
**[2026-09-16 10:14] Samir Haddad:** yes, immutable. I'll put that in the decision
**[2026-09-16 10:16] Sofia Marchetti:** good. draft it today and I'll review tonight
**[2026-09-16 10:17] Yusuf Demir:** thanks, that was quick
**[2026-09-16 10:18] Samir Haddad:** cool, drafting now
