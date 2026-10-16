---
id: tkt-20
kind: ticket
title: "SEC-9: SOC 2 finding AF-12 (idle sessions)"
date: 2026-08-04T09:00:00Z
author: Ravi Chandrasekar
participants: [Ravi Chandrasekar, Noor Haddad, Tobias Wren]
status: open
labels: [security, compliance, soc2, session-cache]
uri: pellucid://tickets/SEC-9
---

# SEC-9: SOC 2 finding AF-12 (idle sessions)

## Description

Our SOC 2 Type II audit is being run by Ashgrove Assurance. They have raised finding AF-12, and this ticket tracks our response.

The finding: sessions on payment-capable accounts remain valid after being idle for longer than five minutes. The auditors want the idle limit brought within their threshold, or a compensating control documented and tested.

Current position: no decision yet on the approach. Identity needs to size the impact of a shorter idle limit on users and on session-cache memory, and then we bring a recommendation to Tobias.

Not part of this finding: audit-log retention, which is 900 days and is handled under a different control.

## Comments

**Ravi Chandrasekar (2026-08-04):** Flagging to Identity. Noor, can you size the impact of a shorter idle limit?

**Noor Haddad (2026-08-04):** Yes. I will bring numbers to the next Identity review.

**Tobias Wren (2026-08-04):** Keep this high on the list. The audit checkpoint is coming up and I want a decision before it.
