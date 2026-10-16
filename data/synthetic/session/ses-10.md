---
id: ses-10
kind: session
title: "Agent session: set rate limit 180"
date: 2026-09-14T08:30:00Z
author: Viktor Sokolov
participants: [Viktor Sokolov]
labels: [agent-session, api-gateway, rate-limit]
---

## Task

Viktor asked the agent to lower the api-gateway per-tenant rate limit from its current 250 requests per second to 180, using cfgctl, following the load test results.

## Steps

1. Read the load test summary. At 250 requests/s per tenant, auth-service saturates. 180 keeps it under the threshold with some margin.
2. Wrote the cfgctl change against `gateway.per_tenant.rate_limit`. Wrong key name: cfgctl found no such key and changed nothing.
3. Listed the keys under the gateway namespace, found the correct one, and re-ran the change. The diff shows only the limit value changing, from 250 to 180.
4. Noor reviewed the diff as the second approver before the push went out.
5. Checked the gateway rate-limit metrics for the next few minutes. Rejections for the tenant rose at the new ceiling and load on auth-service came down.

## Outcome

Per-tenant limit set to 180 requests/s. Auth-service load is lower under the load test profile. Nothing else in the gateway config was touched. The first attempt used the wrong key name and was corrected before anything changed. The ticket records the approval and the load test numbers.

## Lessons

- List the keys before writing a change. A wrong key name is cheap to find and expensive to guess.
- The second approver should review the diff itself, not only the ticket.
- Load tests should cover the exact limit being set, not an earlier one.
- Write the old and new value side by side in the PR, so the review is one glance.
