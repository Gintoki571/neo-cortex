---
id: mtg-08
kind: meeting
title: "Config policy review"
date: 2026-10-05T16:00:00Z
author: Grace Nakamura
participants: [Grace Nakamura, Chen Wei, Mateo Alvarez, Tobias Wren]
labels: [config, approvals, policy]
---

# Config policy review

## Attendees

Grace Nakamura (chair), Chen Wei, Mateo Alvarez, Tobias Wren.

## Notes

- Review of the two-approver rule for production config, in force since 14 August. Grace pulled the numbers: the median wait for the second approval is 3.5 hours. Most of that wait is people not being online at the same time as the author.
- Chen says the rule is fine for big changes and painful for one-line ones.
- Mateo's proposal: one approver, plus automated validation of the change before it can be pushed. He wants the validator to be the thing that catches mistakes, with people looking at what the validator cannot judge.
- Mateo noted a validator is only as good as its bounds. Chen agreed to keep the bounds list short and reviewed.
- Open question: whether a second approver should still be required for keys that touch login.
- Grace wants a clear answer for the wider team. Tobias will decide tomorrow.

## Decisions

- No decision today. Tobias decides tomorrow.

## Action items

- Mateo Alvarez: write the one-page proposal with the validation steps, due 2026-10-05.
- Grace Nakamura: send Tobias the approval data and the proposal, due 2026-10-05.
- Chen Wei: draft the validator bounds for the numeric config keys, due 2026-10-06.
