---
id: chat-11
kind: chat
title: "#incidents: checkout 502s"
date: 2026-08-10T09:20:00Z
author: Jonas Albrecht
participants: [Jonas Albrecht, Mateo Alvarez, Daniel Kwon, Anjali Deshpande]
labels: [incident, payments, checkout]
---

# #incidents

**[2026-08-10 09:20] Jonas Albrecht:** checkout is throwing 502s. Orchard & Vane first, now Saltmarsh Foods too. customers are reporting failed payments
**[2026-08-10 09:21] Mateo Alvarez:** saw the alert. which ones? all payment calls or some?
**[2026-08-10 09:22] Jonas Albrecht:** all of the calls from those two accounts. the other customers look normal so far
**[2026-08-10 09:23] Daniel Kwon:** payment-gateway logs show it waiting on auth for token introspection on every request, then timing out and returning a 502
**[2026-08-10 09:24] Mateo Alvarez:** so auth is where to look. is Noor on it already?
**[2026-08-10 09:25] Daniel Kwon:** she's in the auth channel. I'll keep watching the gateway
**[2026-08-10 09:26] Anjali Deshpande:** how bad is it right now? I need a number for the exec thread
**[2026-08-10 09:27] Jonas Albrecht:** Saltmarsh is a food distributor and they run a lot of payments in the morning. they are pretty upset
**[2026-08-10 09:28] Mateo Alvarez:** tell them we're on it and will have an update soon. not giving numbers until we have them
**[2026-08-10 09:29] Daniel Kwon:** the gateway error rate just doubled. checkout is basically down for those two
**[2026-08-10 09:31] Anjali Deshpande:** ok. Jonas, keep the account managers in the loop
**[2026-08-10 09:32] Jonas Albrecht:** on it
**[2026-08-10 09:34] Mateo Alvarez:** calling it an incident now, opening the bridge. everyone with a view on auth, please join
