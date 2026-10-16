---
id: tkt-19
kind: ticket
title: "PLAT-690: INC-03 action items"
date: 2026-08-11T09:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Grace Nakamura, Chen Wei]
status: in-progress
labels: [incident, action-items, platform, config]
uri: pellucid://tickets/PLAT-690
---

# PLAT-690: INC-03 action items

## Description

Action items from the INC-03 review. The review is blameless. The failure was a production config value that went out with no second pair of eyes on it, and no input validation caught it. The fix is in how we change config, not in one engineer's judgement.

Action items:

1. Require a second approver for production config changes. Mateo Alvarez writes the rule up for config-service and it will be recorded as ADR-008.
2. Add input validation for config values, with sensible bounds for numeric settings. Owner: Chen Wei.
3. Add a short entry to the on-call handbook describing how a config rollback is done and who to tell.
4. Grace Nakamura checks how the new approval step affects Platform turnaround time over the next month.

Hard rule from this review: a production config change needs a second pair of eyes and a validation step before it goes out. Emergency rollbacks stay one step.

## Comments

**Grace Nakamura (2026-08-11):** Thanks, everyone. Let's make sure the second approver does not slow down the on-call path. A rollback should stay a single action.

**Chen Wei (2026-08-11):** I will take the validation item. Happy to pair on the rules with anyone who knows the numbers.

**Mateo Alvarez (2026-08-11):** Good. Action items are assigned. We will review progress at the next Platform sync.
