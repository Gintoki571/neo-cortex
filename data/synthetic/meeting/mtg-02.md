---
id: mtg-02
kind: meeting
title: "Platform weekly sync"
date: 2026-07-15T16:00:00Z
author: Grace Nakamura
participants: [Grace Nakamura, Mateo Alvarez, Viktor Sokolov, Beatrice Oyelaran, Chen Wei]
labels: [platform, weekly, rate-limit, bank-connector]
---

# Platform weekly sync

## Attendees

Grace Nakamura (chair), Mateo Alvarez, Viktor Sokolov, Beatrice Oyelaran, Chen Wei.

## Notes

- Rate limits: Viktor raised the gateway's per-tenant limit to 250 requests/s on the 9th, for the Orchard & Vane seasonal import. Anyone touching gateway limits should check with him first.
- Bank service rename lands on Monday the 20th. Payments is driving it. Platform's part is mostly the on-call links and the runbook pointers.
- Chen asked what the rename touches on our side. Answer from the room: dashboards and runbooks, and we should not assume that is the whole list.
- Beatrice and Viktor disagreed about whether the gateway dashboard needs a new panel for limit hits. Left open until someone looks at the numbers.
- Grace reminded everyone the on-call rota for the next four weeks goes out this week.

## Decisions

- Bank rename proceeds on the 20th as planned.
- No further change to gateway limits until the next load review.

## Action items

- Beatrice Oyelaran: check dashboards and alert rules for any panel still using the old service name, due 2026-07-17.
- Chen Wei: review the config-service push pipeline for anything the rename touches, due 2026-07-17.
- Viktor Sokolov: add the Orchard & Vane limit change to the gateway runbook, due 2026-07-22.
- Mateo Alvarez: post the on-call rota for the next four weeks, due 2026-07-16.
