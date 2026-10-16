---
id: doc-11
kind: doc
title: "Deploy checklist and Friday policy"
date: 2026-07-01T09:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Grace Nakamura]
labels: [runbook, deploy, release, policy]
uri: pellucid://wiki/runbooks/deploy-checklist
---

# Deploy checklist and Friday policy

Every production deploy follows this checklist. It exists so that a bad release is caught by a small slice of traffic instead of all of it. Mateo Alvarez maintains it; Grace Nakamura approves changes to it.

## Before the deploy

- Confirm the change has been reviewed and that its tests passed in CI.
- Check that the on-call engineer knows the deploy is happening and when.
- Confirm there is no open incident on the services the change touches.

## The canary

Send the new version to 10% of traffic first, and hold it there for 15 minutes. Watch the error rate and the latency panels for the whole window, not just the first minute, because some problems take a few minutes to show.

Abort the rollout if the error rate goes above 1% at any point during the canary. Aborting means returning all traffic to the previous version. Do not try to fix forward while the canary is failing.

If the canary holds, move to full traffic and keep watching for another 15 minutes.

## Friday policy

No production deploys happen on Fridays. The policy took effect on 3 July 2026 and applies to every service in production. Non-production work on a Friday is fine.

Anything urgent that comes up on a Friday needs the on-call lead and the CTO to agree on an exception before anyone touches production.

## After the deploy

Post the version, the time and any anomalies in the release channel. If you aborted a canary, write a short note explaining why, even if the cause seems obvious. The note is how the next person learns what to look for.

## Keeping this page current

Changes to the checklist go through Mateo and are announced to the engineering channel. Please flag anything you find that does not match what actually happens during a deploy.
