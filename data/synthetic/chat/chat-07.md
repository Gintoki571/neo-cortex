---
id: chat-07
kind: chat
title: "#payments: rename naming bikeshed"
date: 2026-07-17T14:00:00Z
author: Sam Okafor
participants: [Sam Okafor, Daniel Kwon, Sofia Marchetti, Elif Yildiz]
labels: [naming, bank-connector]
---

# #payments

**[2026-07-17 14:00] Sam Okafor:** ok, proposal: rename bankbridge to bank-connector. it matches our other services and we stop being the odd one out
**[2026-07-17 14:02] Daniel Kwon:** I'm against keeping bankbridge. the name collides with bankbridge-sim, the test mock. every time someone greps for it they get the mock too
**[2026-07-17 14:04] Elif Yildiz:** the sim has been called bankbridge-sim since forever, we are not renaming a mock to fix a name
**[2026-07-17 14:05] Sam Okafor:** right, that is the main reason I'm pushing. and bank-connector follows the noun-connector pattern we use for the rest
**[2026-07-17 14:06] Elif Yildiz:** bankbridge sounds like a bluetooth pairing thing lol
**[2026-07-17 14:07] Daniel Kwon:** haha. ok I can live with bank-connector
**[2026-07-17 14:08] Sam Okafor:** great. I'll do the repo and the docs first
**[2026-07-17 14:09] Sofia Marchetti:** ok let's decide. bank-connector it is, I'll sign the ADR today, effective the 20th
**[2026-07-17 14:10] Daniel Kwon:** give us a few days to update our stuff. nothing blocking?
**[2026-07-17 14:11] Sam Okafor:** nothing blocking. I'll post a list of what changes so you can check your own bits
**[2026-07-17 14:13] Elif Yildiz:** I'll celebrate the name with a coffee
**[2026-07-17 14:14] Sofia Marchetti:** Tobias will sign off on it, don't worry about that part
