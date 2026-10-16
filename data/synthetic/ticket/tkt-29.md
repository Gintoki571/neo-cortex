---
id: tkt-29
kind: ticket
title: "PLAT-742: Roll out cfglint"
date: 2026-10-06T10:00:00Z
author: Chen Wei
participants: [Chen Wei, Grace Nakamura, Mateo Alvarez]
status: closed
labels: [config, cfglint, platform, policy]
uri: pellucid://tickets/PLAT-742
---

# PLAT-742: Roll out cfglint

## Description

Wire cfglint into the config push pipeline so every production change is validated before it reaches config-service. Today's policy change makes this the main control. Production config changes now need one approver plus an automated check, and the automated check is cfglint. The second approval requirement goes away with this.

Rules shipping in the first version:

- `auth.introspection_timeout_ms` must be between 200 and 5000 ms. Anything outside that range is refused at push time.
- Other keys are unchanged in this release. More bounds will be added to the same rules file over time.
- A failed check blocks the push and prints the key, the value and the allowed range.

The approver still has to read the diff. cfglint does not replace judgement; it catches values that are obviously wrong before a person has to notice them.

## Comments

**Grace Nakamura (2026-10-06):** Reviewed the bounds with Mateo. 200 to 5000 ms feels right for this timeout. Approving the policy side.

**Mateo Alvarez (2026-10-06):** Agreed. I'd like the check to also run in the dry-run path so people see the failure before they hit push.

**Chen Wei (2026-10-06):** Added the dry-run hook. Rolled out to the push pipeline just now, so the policy is live. Happy to take feedback on the wording of the error message.
