---
id: mtg-04
kind: meeting
title: "Leadership: engineering reorg"
date: 2026-08-11T09:00:00Z
author: Tobias Wren
participants: [Tobias Wren, Maggie Ellison, Grace Nakamura, Ravi Chandrasekar]
labels: [reorg, platform, identity, session-cache]
---

# Leadership: engineering reorg

## Attendees

Tobias Wren (chair), Maggie Ellison, Grace Nakamura, Ravi Chandrasekar.

## Notes

- Background: the INC-01 logouts exposed a gap. The cache behind login sessions sits with Identity, and Identity has no on-call coverage for cache operations.
- Platform already runs a 24x7 rotation. Shared stateful infrastructure is a better fit there than inside a feature team.
- Proposal: Platform owns shared stateful infrastructure from here on. The first thing to move is the session cache, from Identity to Platform, effective 1 September.
- Ravi raised the concern that Identity loses a service it knows well. Agreed the handover needs a runbook review first.
- Maggie asked that the announcement wait a week so both teams hear it together.
- Tobias asked for the decision to be written up as an ADR this week.
- Nobody disagreed with the logic. The open question was timing, and the room settled on 1 September because it leaves a full month for the handover.

## Decisions

- Accepted: Platform owns shared stateful infrastructure. The session cache moves to Platform on 1 September.

## Action items

- Grace Nakamura: plan the handover week with Ravi, due 2026-08-18.
- Ravi Chandrasekar: list the session-cache knowledge that only lives in Identity, due 2026-08-25.
- Tobias Wren: circulate the written ADR, due 2026-08-12.
