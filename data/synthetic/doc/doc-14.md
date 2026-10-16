---
id: doc-14
kind: doc
title: "Engineering handbook: teams and ownership"
date: 2026-09-03T09:00:00Z
author: Grace Nakamura
participants: [Grace Nakamura, Tobias Wren]
labels: [handbook, ownership, teams, process]
uri: pellucid://wiki/handbook/teams-and-ownership
---

# Engineering handbook: teams and ownership

Pellucid Pay is a remote-first B2B accounts-payable automation company, and engineering is organised into six teams. This page is the current map of who does what. When it disagrees with a service README, this page wins and the README should be fixed.

## Teams

- Leadership: Maggie Ellison (CEO) and Tobias Wren (CTO), with Anjali Deshpande on product.
- Identity: login, sessions and everything a user needs to prove who they are.
- Payments: the payment path from the API to the bank.
- Platform: shared infrastructure, configuration and on-call.
- Data: event handling, fraud scoring and reporting.
- Experience: the web dashboard, notifications and customer support tooling.

Kofi Mensah works on the Data team and Chen Wei on Platform. Please use the team channel for requests to a team rather than messaging individuals directly.

## Decision rights

Architecture decisions are written up as ADRs. Tobias Wren gives final sign-off on every ADR, and nothing is considered decided until he has approved it. Teams propose; the CTO decides.

## Service ownership

Each service has one named owner. The owner is responsible for its runbook, its dashboards and the answers to questions about it.

| Service | Team | Owner |
|---|---|---|
| session-cache | Platform | Mateo Alvarez |

The session-cache entry changed on 1 September 2026. Anyone who still lists a different owner for it is working from an old copy of this page.

## Changing this page

Ask Grace Nakamura. Ownership changes are announced in the engineering channel before the page is updated, so the page should never be the first place someone hears about a move.

## Onboarding

New joiners should read this page, the platform overview and the on-call process in that order. Week one ends with a shadow shift on the on-call rota, which is always supervised.
