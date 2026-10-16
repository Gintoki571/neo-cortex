---
id: doc-08
kind: doc
title: "Runbook: roll back a config change"
date: 2026-08-11T10:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Chen Wei, Grace Nakamura]
labels: [runbook, config-service, cfgctl, on-call]
uri: pellucid://wiki/runbooks/config-rollback
---

# Runbook: roll back a config change

Use this when a production config change looks wrong and you need it reverted now. The rollback is the fastest safe move you have, so reach for it before you start digging into why the change went bad.

## The command

Roll one key back to a known version with:

`cfgctl rollback <key> --to <version>`

Use the last version that was known to be good for that key. Rolling back does not delete the bad version, so the record of what happened stays intact.

## How long it takes

A rollback takes effect in about 30 seconds across the fleet. Services pick up the new value on their next read, so you should see the effect in dashboards within a minute. If you do not, check that the key you rolled back is the one the service actually reads.

## Tell on-call

Whenever you roll back, tell on-call straight away, even if the rollback looks clean. On-call may be watching a related alert, and they should know that a setting moved under them. Post in the on-call channel with the key, the version you rolled back to and the time.

## Who can push

Today any Platform engineer can still push production config alone. That makes the rollback your safety net rather than a formality. If you push a change, be ready to roll it back yourself, and do not assume someone else will catch it.

## When the rollback does not help

If the problem persists after the rollback, the change was probably not the cause, or the bad value was copied somewhere else. Look at what else changed in the same window, page on-call if payments are affected, and keep the affected keys frozen until someone has reviewed them.

## Notes

- Always pass `--to` explicitly, so you know exactly what the key goes back to.
- Keep a note of the key and version in the ticket, so the change is traceable later.
