---
id: tkt-12
kind: ticket
title: "SUP-341: Tidewater ACH settled next business day"
date: 2026-07-24T16:45:00Z
author: Jonas Albrecht
participants: [Jonas Albrecht, Sam Okafor, Anjali Deshpande]
status: in-progress
labels: [support, ach, tidewater]
uri: pellucid://tickets/SUP-341
---

# SUP-341: Tidewater ACH settled next business day

## Description

Tidewater Credit Union reports that their same-day ACH batches are settling a business day late. Batches that were sent before the cutoff are showing up as next-day settlements.

Tidewater runs ACH through bank-connector, and our agreement with them includes a same-day cutoff override of 17:30 ET. That is the number they are holding us to. Their operations lead was polite on the call, but was clear that a late settlement is a service failure under the agreement. They want a straight answer on what happened and when their members' money will land.

I am their support contact. I have told them we are investigating and will update them within the hour.

## Comments

**Anjali Deshpande (2026-07-24):** Tidewater is an important account for us. Sam, can you own the investigation?

**Sam Okafor (2026-07-24):** On it. I am checking the cutoff configuration first.

**Jonas Albrecht (2026-07-24):** Sent Tidewater an acknowledgement. They have asked for a call tomorrow morning.
