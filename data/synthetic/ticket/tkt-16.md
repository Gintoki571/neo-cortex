---
id: tkt-16
kind: ticket
title: "SUP-357: Checkout failing for Orchard & Vane"
date: 2026-08-10T09:15:00Z
author: Jonas Albrecht
participants: [Jonas Albrecht, Mateo Alvarez, Anjali Deshpande, Maggie Ellison]
status: closed
labels: [support, urgent, checkout, orchard-and-vane]
uri: pellucid://tickets/SUP-357
---

# SUP-357: Checkout failing for Orchard & Vane

## Description

Urgent. Orchard & Vane reports that checkout is failing. Customers reaching the payment step are getting an error page, and the payment calls behind it are returning HTTP 502. The first errors were seen at about 09:12 UTC today.

Orchard & Vane is a retail chain on our Enterprise plan and the heaviest user of payment-gateway. Maggie Ellison is their exec sponsor and is copied on this ticket.

Saltmarsh Foods may be seeing the same thing. Their finance team has just called to say their payment runs are failing. Saltmarsh is a food distributor that pays through payment-gateway, and I am their support contact, so I am taking that report on this ticket.

We need a status note to the customer within fifteen minutes, even if the note is only "we are on it."

## Comments

**Maggie Ellison (2026-08-10):** I am escalating this as their exec sponsor. I want an update every fifteen minutes until checkout is green.

**Mateo Alvarez (2026-08-10):** On-call and investigating. The failures are in the payment path and I am looking at it now. I will post more once I have a cause.

**Jonas Albrecht (2026-08-10):** Saltmarsh has confirmed the same error on their side. Adding them to the thread.

**Anjali Deshpande (2026-08-10):** Holding statement has gone to Orchard & Vane.

**Mateo Alvarez (2026-08-10):** Errors stopped as of 09:53 UTC. Closing this ticket. The incident ticket has the details.
