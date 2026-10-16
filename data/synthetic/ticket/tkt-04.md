---
id: tkt-04
kind: ticket
title: "INC-01 RCA: session-cache memory pressure"
date: 2026-06-17T10:00:00Z
author: Noor Haddad
participants: [Noor Haddad, Lukas Brandt, Mateo Alvarez, Ravi Chandrasekar]
status: closed
labels: [rca, session-cache, auth-service]
uri: pellucid://tickets/INC-01-RCA
---

# INC-01 RCA: session-cache memory pressure

## Description

This is the root cause note for the mass logouts on 2026-06-16. The review is blameless. We are trying to explain the mechanism so it does not happen again, not to decide whose fault it was.

Mechanism: auth-service keeps login sessions in session-cache. The auth-service v2.14 release on 2026-06-15 added remember-device, and that feature writes a second record for every login. The number of entries in session-cache roughly doubled. The capacity we had planned for was based on one entry per login, so memory filled up sooner than expected. When it was full, the eviction policy removed sessions that were still live, and those users were sent back to the login page.

Contributing factors: the capacity model did not account for per-login records, and the cache had 4 GB of memory, which left little room once the entry count grew.

Mitigation: session-cache memory went from 4 GB to 8 GB on 2026-06-17. We will keep the eviction panel on the on-call screen for the next few days.

Follow-up: the capacity model needs to count per-login records. That is tracked as IDN-230.

## Comments

**Ravi Chandrasekar (2026-06-17):** Thanks Noor. Please make sure IDN-230 is linked so the capacity work does not get lost.

**Mateo Alvarez (2026-06-17):** The memory change went in this morning. The eviction panel is on the on-call screen from now on.

**Lukas Brandt (2026-06-17):** I have read through the mechanism section and agree with it.
