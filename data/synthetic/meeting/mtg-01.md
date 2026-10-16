---
id: mtg-01
kind: meeting
title: "INC-01 and INC-05 postmortem review"
date: 2026-06-29T15:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Noor Haddad, Lukas Brandt, Tessa Ngu, Grace Nakamura, Ravi Chandrasekar]
labels: [postmortem, session-cache, notification-service, deploys]
---

# INC-01 and INC-05 postmortem review

## Attendees

Mateo Alvarez (chair, incident commander for the logouts), Noor Haddad, Lukas Brandt, Tessa Ngu, Grace Nakamura, Ravi Chandrasekar.

## Notes

- Logouts: web-dashboard users kept getting bounced to the login page earlier this month. Session-cache was dropping live sessions once memory got tight, because its eviction policy treats every key as fair game.
- The memory pressure traces back to the remember-device change in auth-service v2.14, which shipped on 15 June. Each login now writes an extra device-trust record into session-cache, so the number of entries roughly doubled.
- The feature did what it was meant to do. The side effect on cache size is what we missed in review.
- INC-05: the notification-service deploy on Friday 26 June sent duplicate invoice reminders to about 400 recipients. Tessa fixed it over the weekend.
- The Friday part is the real problem. A late-Friday deploy turned into weekend work for one engineer, and that is exactly the pattern we want to stop.

## Decisions

- Proposal, not yet agreed: no production deploys on Fridays, starting 3 July. Mateo writes it up for sign-off.

## Action items

- Mateo Alvarez: write the Friday deploy proposal, due 2026-07-01.
- Noor Haddad: list every other shared store the v2.14 login path writes to, due 2026-07-06.
- Tessa Ngu: write up what the duplicate reminder bug actually was for the team wiki, due 2026-07-03.
