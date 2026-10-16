---
id: tkt-24
kind: ticket
title: "INC-04: Reporting totals inflated"
date: 2026-09-09T09:30:00Z
author: Yusuf Demir
participants: [Yusuf Demir, Olivia Hartmann, Elif Yildiz, Samir Haddad]
status: in-progress
labels: [incident, reporting-service, ledger-service, event-pipeline]
uri: pellucid://tickets/INC-04
---

# INC-04: Reporting totals inflated

## Description

Incident: reporting-service shows inflated invoice totals for Northgate Freight. Roughly 3,000 invoices show about twice their real total. Invoices that were not affected show exact totals, so the problem is specific to a subset.

Findings so far:

- Each affected invoice has two copies of the same event in what reporting-service consumes.
- The duplicate events were published by the ledger-service outbox after the event-pipeline broker rebalanced on 2026-09-08.
- The reporting-service consumers did not recognise the second copy as one they had already processed, so they counted it again.

We have not yet established why the second copies carry a different identifier from the originals. That is the next question for Elif and the ledger-service side.

Immediate aim: stop the double counting from getting worse, then correct the totals once the source is fixed.

## Comments

**Olivia Hartmann (2026-09-09):** Confirmed on a sample of affected invoices. I will prepare a dedupe run for after the source fix.

**Elif Yildiz (2026-09-09):** Checking the outbox behaviour on the ledger side. Will report back.

**Samir Haddad (2026-09-09):** I will pull the broker logs for the 8th and look at consumer lag over the same window.
