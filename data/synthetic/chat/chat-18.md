---
id: chat-18
kind: chat
title: "#incidents: Northgate totals"
date: 2026-09-09T09:10:00Z
author: Olivia Hartmann
participants: [Olivia Hartmann, Elif Yildiz, Yusuf Demir, Anjali Deshpande]
labels: [incident, reporting, northgate]
---

# #incidents

**[2026-09-09 09:10] Olivia Hartmann:** Northgate Freight's month-to-date totals in reporting are about double what the ledger says. around 3,000 invoices look affected. checking the sample now
**[2026-09-09 09:12] Anjali Deshpande:** oh no. Northgate's finance team exports these every morning, they will notice
**[2026-09-09 09:13] Yusuf Demir:** is it the reporting side? did we change anything in reporting this week?
**[2026-09-09 09:15] Olivia Hartmann:** no changes on my side. I checked the query cache, it is not stale. the events themselves look duplicated
**[2026-09-09 09:17] Elif Yildiz:** duplicated how? show me one
**[2026-09-09 09:19] Olivia Hartmann:** two events per invoice, minutes apart. the second one has a different key ending in ":2"
**[2026-09-09 09:22] Elif Yildiz:** ...that's me. v3.8 went out yesterday and I changed the idempotency key to txn_id:attempt. so the consumers can't match the two copies
**[2026-09-09 09:24] Yusuf Demir:** ok. how sure are we? I don't want to revert on a guess
**[2026-09-09 09:25] Elif Yildiz:** sure. I can see the diff in the release. the key format is the only change that matters here
**[2026-09-09 09:27] Anjali Deshpande:** what do I tell Northgate right now?
**[2026-09-09 09:28] Olivia Hartmann:** that totals are wrong for a window and we are correcting them. no numbers yet
**[2026-09-09 09:31] Yusuf Demir:** ok. Elif, revert the key format. Olivia, prepare the dedupe. we check the totals afterwards
**[2026-09-09 09:40] Elif Yildiz:** reverted and deployed. thank god. Olivia, all yours
**[2026-09-09 09:42] Olivia Hartmann:** phew. ok, dedupe next. not a fun morning
