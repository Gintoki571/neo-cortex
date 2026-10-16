---
id: tkt-18
kind: ticket
title: "CFG-4411: Tune auth introspection timeout"
date: 2026-08-10T09:05:00Z
author: Chen Wei
participants: [Chen Wei, Beatrice Oyelaran]
status: closed
labels: [config, auth-service, prod]
uri: pellucid://tickets/CFG-4411
---

# CFG-4411: Tune auth introspection timeout

## Description

Production config change through config-service.

- Key: `auth.introspection_timeout_ms`
- From: 800
- To: 80
- Environment: prod, all regions
- Reviewer: none (single-engineer push, per current Platform policy)
- Pushed: 2026-08-10 09:05 UTC

Motivation: introspection calls from the gateway tier were holding connections longer than I like during the morning peak, so I want a much tighter timeout to fail fast and shed load.

## Comments

**Beatrice Oyelaran (2026-08-10):** Just noticed this while updating the dashboard. Is 80 right? The old value was 800. Not the web-dashboard client timeout, that one is 80 *seconds* and lives elsewhere.

**Chen Wei (2026-08-10):** It is what I typed. Will check the graphs.
