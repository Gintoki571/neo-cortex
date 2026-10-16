---
id: mtg-06
kind: meeting
title: "Engineering all-hands: Friday freeze review"
date: 2026-09-21T16:00:00Z
author: Grace Nakamura
participants: [Grace Nakamura, Mateo Alvarez, Tobias Wren, Tessa Ngu, Freya Lindqvist]
labels: [deploys, freeze, all-hands]
---

# Engineering all-hands: Friday freeze review

## Attendees

Grace Nakamura (chair), Mateo Alvarez, Tobias Wren, Tessa Ngu, Freya Lindqvist. Open to all of engineering.

## Notes

- Agenda item: the Friday deploy freeze. It has been in force since 3 July. The point of it was to keep Friday risk down.
- The cost has been slower fixes. Anything that needs to ship on a Friday now waits for Monday, and that has hurt us a few times.
- Proposal on the table: lift the freeze and allow Friday production deploys before 14:00 UTC, each one behind a canary. The canary tooling is now solid enough to rely on.
- Freya asked how we would know a canary had gone bad at 14:00 on a Friday. Mateo: the canary has an abort rule, and whoever is deploying watches it.
- Views are mixed. Tessa is still nervous about the weekend. Tobias is open to it but wants a vote, not a show of hands.
- Vote tomorrow, in the same channel as this thread.

## Decisions

- None yet. The vote is tomorrow.

## Action items

- Mateo Alvarez: write up the canary abort rule for the proposal, due 2026-09-22.
- Freya Lindqvist: collect questions from the teams before the vote, due 2026-09-21.
- Grace Nakamura: post the vote result in #eng, due 2026-09-22.
