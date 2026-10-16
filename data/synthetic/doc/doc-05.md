---
id: doc-05
kind: doc
title: "config-service guide"
date: 2026-06-12T09:00:00Z
author: Chen Wei
participants: [Chen Wei, Grace Nakamura, Viktor Sokolov]
labels: [config-service, cfgctl, platform, guide]
uri: pellucid://wiki/guides/config-service
---

# config-service guide

config-service is the production configuration store for Pellucid Pay. Services read their settings from it at runtime, so a change here reaches live traffic without a deploy. That is convenient and also the reason to be careful. I own the service and wrote the tooling around it.

## The pieces

cfgctl is the command-line client. I built it along with the push pipeline that moves a change from a reviewed file into the store. Use cfgctl for every change rather than editing the store by hand.

Each setting has a key, a value and a version. Keys are grouped by component, so the settings for each service live under that service's own prefix. Read the key list before adding one, and check whether a suitable key already exists.

## Who can change production config

Right now any Platform engineer can push production config on their own. There is no second approver, so the discipline has to come from the person making the change. Please write the change in a pull request, describe its effect in one line, and tell the rest of Platform when it is going out.

## Bank settings

The per-bank settings for bankbridge live in config-service as well. Bank cutoffs and overrides are the most sensitive values in the store, because a wrong cutoff changes when money moves. Ask Payments before touching them, and keep the contract test for each bank up to date.

## Working with the store

- Describe each change in its pull request before it is pushed.
- Pushed changes are live within moments, so check the result straight away.
- If something looks wrong, roll back first and investigate second. The rollback command is covered in the runbook for config changes.

## Questions

Grace Nakamura runs Platform and decides the rules for production changes. Viktor Sokolov is the best person to ask about how the gateway reads its limits from the store.
