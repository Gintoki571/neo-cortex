---
id: tkt-03
kind: ticket
title: "INC-01: Mass logouts on web-dashboard"
date: 2026-06-16T14:30:00Z
author: Mateo Alvarez
participants: [Mateo Alvarez, Noor Haddad, Beatrice Oyelaran, Lukas Brandt]
status: closed
labels: [incident, web-dashboard, session-cache]
uri: pellucid://tickets/INC-01
---

# INC-01: Mass logouts on web-dashboard

## Description

Incident: web-dashboard users are being logged out over and over. The problem ran for roughly two hours on 2026-06-16. Kilnworth Dental Group raised it first through support (SUP-318). Incident commander: Mateo Alvarez.

## Timeline

- Support reports of forced re-logins start coming in.
- auth-service logs show live sessions that cannot be found when a user makes a request.
- session-cache shows evictions climbing and memory close to its ceiling. The eviction policy is allkeys-lru, which means Redis will drop whatever looks least recently used when memory is full, including sessions that are still active.
- Mitigation is under way on the cache side.

## Root cause

Not known yet. The eviction pattern is clear, but we have not found what is pushing memory up. Noor and Lukas are looking at what has been written into session-cache recently.

## Comments

**Noor Haddad (2026-06-16):** auth-service does not evict anything itself. Every session lives in session-cache, so the eviction numbers are what matter. Checking recent writes now.

**Beatrice Oyelaran (2026-06-16):** The dashboard shows evictions spiking and memory near the ceiling. Sharing the panel link in the channel.

**Lukas Brandt (2026-06-16):** Nothing was deployed to session-cache today. I am going through auth-service changes from the last week.

**Mateo Alvarez (2026-06-16):** Logouts have stopped. Closing the incident. The RCA follows as a separate ticket.
