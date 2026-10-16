---
id: tkt-01
kind: ticket
title: "IDN-212: Implement remember-device trust records"
date: 2026-06-12T09:30:00Z
author: Lukas Brandt
participants: [Lukas Brandt, Noor Haddad, Ravi Chandrasekar]
status: closed
labels: [identity, auth-service, feature]
uri: pellucid://tickets/IDN-212
---

# IDN-212: Implement remember-device trust records

## Description

Build the remember-device flow in auth-service so that a returning browser can skip the MFA prompt on the next login. Assignee: Lukas Brandt.

After a successful MFA challenge, write a device-trust record next to the session the login already creates. On the next login from the same browser, check for that record before prompting. Keep the change inside the existing login path. No new endpoints.

Acceptance:

- The device-trust record is written on successful MFA and read on the next login.
- Session handling stays as it is today. The session TTL is still 3600 s in every environment and this ticket does not touch it.
- Unit tests cover expired and revoked device records.

Target is the next auth-service minor release.

## Comments

**Noor Haddad (2026-06-12):** Keep the record small, please. The login path is hot and every extra write shows up in the latency graphs.

**Lukas Brandt (2026-06-12):** Understood. I will start with the storage shape, then the login hook.

**Ravi Chandrasekar (2026-06-13):** Good for the v2.14 train. Ping me when the tests are green.

**Lukas Brandt (2026-06-15):** v2.14 is out with remember-device enabled. Closing.
