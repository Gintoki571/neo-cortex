---
id: chat-23
kind: chat
title: "#platform: cfglint bounds"
date: 2026-10-06T11:00:00Z
author: Chen Wei
participants: [Chen Wei, Beatrice Oyelaran, Mateo Alvarez]
labels: [config, validation, platform]
---

# #platform

**[2026-10-06 11:00] Chen Wei:** pushed the first cut of the bounds check for config-service. auth.introspection_timeout_ms now has to sit between 200 and 5000 ms (cfglint), anything outside fails validation
**[2026-10-06 11:02] Mateo Alvarez:** good. why 200 as the floor?
**[2026-10-06 11:04] Chen Wei:** below 200 ms the introspection call times out on a normal busy morning, so allowing it is pointless
**[2026-10-06 11:06] Beatrice Oyelaran:** nice. does it run on every push or only on prod keys?
**[2026-10-06 11:07] Chen Wei:** every push that touches auth config. it runs in the pipeline before anything reaches a region
**[2026-10-06 11:09] Beatrice Oyelaran:** question on alerting: if the check rejects a push, does anything page? at minimum I'd like a counter so we see how often people hit it
**[2026-10-06 11:12] Chen Wei:** right now it just fails the job and tells the author. a metric is a good idea, I'll look at it
**[2026-10-06 11:14] Mateo Alvarez:** put the metric in the same change. cfgctl is what people push with, so that's where I'd want the signal
**[2026-10-06 11:15] Chen Wei:** fair. the push pipeline is mine anyway, so I know where the hooks go
**[2026-10-06 11:18] Beatrice Oyelaran:** ok. add a test for a value that is way too small, that's the kind of mistake that's easy to make
**[2026-10-06 11:19] Chen Wei:** already on it. anything under 200 fails, verified locally
**[2026-10-06 11:21] Mateo Alvarez:** nice. write the bounds into the runbook too
**[2026-10-06 11:22] Beatrice Oyelaran:** will do after the alert is in
