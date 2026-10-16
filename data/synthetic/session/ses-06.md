---
id: ses-06
kind: session
title: "Agent session: enforce two approvals in cfgctl"
date: 2026-08-15T08:00:00Z
author: Chen Wei
participants: [Chen Wei]
labels: [agent-session, cfgctl, approvals]
---

## Task

Chen asked the agent to make cfgctl refuse a production push unless two different people have approved it, per the rule that took effect yesterday. Add unit tests. Do not change the approvals table schema.

## Steps

1. Read cfgctl's push path. The push command has no approval check at all and writes straight to the store.
2. Added a check that counts approvals for the change before the write. Tests for zero, one and two approvals: zero and one are refused, two passes.
3. First attempt at finding the approvers used git blame on the config file to see who had edited the key. Wrong people came back, because blame shows commit authors, not approvers. Dead end.
4. Switched to the approvals table. Joined the change to its approval rows and excluded the author's own approval. Added a test for self-approval; it is refused.
5. Ran the cfgctl test suite. All new tests and the existing ones pass.

## Outcome

cfgctl now refuses production pushes with fewer than two distinct approvals. The change is ready for review and ships with the next cfgctl release. The reviewer should check the self-approval case first, since that is where a bypass would show up.

## Lessons

- Git history tells you who edited a file, not who approved a change. Use the approvals table as the source of truth.
- Write the self-approval test first. It is the case people will try.
- Keep the rule in one place so the CLI and the reviewers see the same definition.
