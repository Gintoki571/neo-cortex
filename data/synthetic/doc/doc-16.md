---
id: doc-16
kind: doc
title: "Config change policy"
date: 2026-10-07T09:00:00Z
author: Chen Wei
participants: [Chen Wei, Grace Nakamura]
labels: [policy, config-service, cfglint, cfgctl]
uri: pellucid://wiki/policies/config-change
---

# Config change policy

This page sets out how production configuration is changed at Pellucid Pay. It applies to every key in config-service, and it replaces any earlier guidance on who may push a change. I wrote the tooling this policy relies on, and Grace Nakamura approves it.

## The rule

A production config change needs one approver and a passing run of automated validation before it is applied. The approver must be someone other than the author. Validation is done by cfglint, which runs as part of the push and refuses a change that breaks a rule.

## What cfglint checks

cfglint checks values against bounds that Platform has agreed. For example, the token introspection timeout in auth-service must be between 200 and 5000 milliseconds, and a value outside that range is rejected before it reaches the store. Other keys have their own bounds, and the full list lives in the linter's rule file.

If a change is rejected, fix the value. Do not work around the linter by editing the rule, and do not push the change through a different path.

## Making a change

1. Write the change with cfgctl.
2. Ask one engineer to review it, and record their approval on the change.
3. Let cfglint run as part of the push. Read its output even when the push succeeds.
4. Tell the Platform channel what changed and why.

## Rollback

A bad change is rolled back with cfgctl, which takes effect in about 30 seconds. When in doubt, roll back first and discuss afterwards.

## Why this shape

Validation catches the errors that a tired reviewer will miss, such as an extra digit in a timeout. A second person catches the errors the validator cannot know about. Together they are cheaper than either one applied alone with the risk left to chance.

## Questions

Questions about a specific rule go to the Platform channel. Questions about the policy itself go to Grace.
