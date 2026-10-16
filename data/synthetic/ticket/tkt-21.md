---
id: tkt-21
kind: ticket
title: "DATA-318: Tighten event-pipeline consumer poll interval"
date: 2026-09-07T09:00:00Z
author: Samir Haddad
participants: [Samir Haddad, Yusuf Demir]
status: closed
labels: [event-pipeline, consumers, config]
uri: pellucid://tickets/DATA-318
---

# DATA-318: Tighten event-pipeline consumer poll interval

## Description

Tighten the event-pipeline consumer poll interval so that stuck consumers are detected faster. Owner: Samir Haddad.

Change: `consumer.max_poll_interval_ms` on event-pipeline goes from 300000 ms to 60000 ms.

Why: a consumer that stops polling currently takes five minutes before the broker gives up on it. A one-minute limit means we find stuck consumers sooner and can restart them before a backlog builds. Lag dashboards already exist for the event-pipeline consumers, so no new monitoring is needed.

Scope: only the consumer poll setting. No producer, schema or consumer code changes, and the broker topics stay as they are. The main thing to watch is whether healthy consumers that are slow to process a batch get flagged as stuck. If that happens we will raise the value a little, not revert the whole change.

Shipped today, 2026-09-07.

## Comments

**Yusuf Demir (2026-09-07):** Good. Let's keep an eye on the consumer dashboards this week.

**Samir Haddad (2026-09-07):** Will do. Shout if anything looks noisy.
