---
id: mtg-03
kind: meeting
title: "Postmortem: INC-02 and INC-03"
date: 2026-08-13T15:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Chen Wei, Sam Okafor, Grace Nakamura, Tobias Wren, Daniel Kwon]
labels: [postmortem, config, bank-connector, payments]
---

# Postmortem: INC-02 and INC-03

## Attendees

Mateo Alvarez (chair), Chen Wei, Sam Okafor, Grace Nakamura, Tobias Wren, Daniel Kwon.

## Notes

- INC-02, Tidewater Credit Union ACH: same-day batches settled the next business day. The bank connector looked up the Tidewater cutoff under its new key prefix, but the value was still stored under the old service name. The lookup came back empty, so the default 14:00 ET cutoff applied instead of the 17:30 ET override.
- The rename itself was reasonable. The gap is the stale prefix, and that is what we need to close.
- INC-03, 10 August: payment authorizations failed for a stretch that morning. CFG-4411 changed the auth introspection timeout from 800 to 80, a typo in the value, and it went to production without review.
- Chen owned it quickly, which helped. This did not turn into a blame session and should not.
- Tobias's point: the fix is validation and a second pair of eyes on production config, not better typing.
- Daniel asked for an alert on the payment side of authorization, so the next one shows up in minutes and not after a customer calls.

## Decisions

- Production config changes need automated validation and a second reviewer before they go out.
- Mateo drafts the proposal for who approves and what the validator checks. Tobias makes the call.

## Action items

- Mateo Alvarez: draft the approval proposal, due 2026-08-14.
- Chen Wei: list the config keys that gate payment and auth behaviour, due 2026-08-20.
- Daniel Kwon: add a latency alert on the payment side of authorization, due 2026-08-21.
- Sam Okafor: close the remaining bank connector rename tasks with Platform, due 2026-08-18.
