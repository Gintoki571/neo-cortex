---
id: doc-12
kind: doc
title: "On-call and incident process"
date: 2026-06-03T09:00:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Beatrice Oyelaran, Viktor Sokolov, Grace Nakamura]
labels: [on-call, incident, process, sre]
uri: pellucid://wiki/process/on-call
---

# On-call and incident process

This page describes how on-call works at Pellucid Pay: who is on the hook, when the rota changes hands, and how an incident is run from the first page to the review. Keep it short enough to read at 2 a.m.

## The rota and the handover

On-call hands over every Monday at 10:00 UTC. The outgoing engineer writes a short note covering open alerts, anything half-finished and any customer who is waiting on a reply. The incoming engineer reads the note and confirms it in the channel before the handover is complete.

## Incident commanders

The incident commander is the person who runs the response, not necessarily the person who fixes the problem. Commanders rotate among Mateo Alvarez, Beatrice Oyelaran and Viktor Sokolov. If none of them is available, the on-call engineer takes the role until one of them is.

## Severity

SEV1 means payments are down. For a SEV1, page the on-call immediately; do not wait to confirm the scope first. A payments outage is always SEV1 whether or not the cause is known.

Lower severities go through the normal alert channel. If you are unsure which level applies, treat it as the higher one and downgrade it once you know more.

## During an incident

- The commander opens an incident channel and posts the severity and the first facts.
- One person writes the timeline as things happen. Times are UTC.
- Fixes go through the same review as any other change, unless the commander explicitly waives it for a rollback.

## After an incident

Every SEV1 gets a written review within a week. The review states what happened, what the team did, and what will change. Blame is not part of the format. Action items get an owner and a date, and Grace Nakamura checks that they close.
