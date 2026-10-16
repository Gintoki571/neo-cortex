---
id: tkt-07
kind: ticket
title: "INC-05: Duplicate invoice reminder emails"
date: 2026-06-27T08:00:00Z
author: Tessa Ngu
participants: [Tessa Ngu, Mateo Alvarez, Freya Lindqvist]
status: closed
labels: [incident, notification-service, email]
uri: pellucid://tickets/INC-05
---

# INC-05: Duplicate invoice reminder emails

## Description

Minor incident. On Friday 2026-06-26 at about 16:40 UTC we deployed a notification-service release. Soon after, invoice reminder emails started going out more than once. About 400 recipients got a second copy of the reminder.

The cause was a retry bug in notification-service. When a send was retried, the template step ran again. The first attempt had already gone out, so the retry produced a second email. The invoice data itself was fine.

I patched the retry path and the fix went out over the weekend.

Customer note: the support team has a short holding reply for any recipient who asks about the second email.

## Comments

**Freya Lindqvist (2026-06-27):** Thanks for taking the weekend on, Tessa. Let's do a proper review on Monday, focused on the process and not on who pressed deploy.

**Mateo Alvarez (2026-06-27):** Late-Friday deploys are worth a look in that review. Let's include the timing.

**Tessa Ngu (2026-06-27):** Fix is merged and deployed. Closing.
