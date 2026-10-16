---
id: doc-02
kind: doc
title: "Identity and session design"
date: 2026-06-05T09:00:00Z
author: Noor Haddad
participants: [Noor Haddad, Lukas Brandt, Ravi Chandrasekar]
labels: [identity, auth-service, session-cache, design]
uri: pellucid://wiki/design/identity-and-sessions
---

# Identity and session design

This page describes auth-service: how logins are checked, how other services verify a token, and where session state actually lives. It is written for engineers joining Identity and for whoever is on call for it.

## What auth-service does

auth-service handles login and token introspection. Any service that needs to know whether a request is authenticated asks auth-service rather than trying to parse tokens on its own. I own the service, so questions about its behaviour come to me first.

The service reads its own settings from config-service, the same store the gateway and the other platform services use. Nothing about configuration is compiled into the binary, so a settings change does not need a release.

## Where sessions live

Session state is kept in session-cache, the Redis cluster that auth-service writes to after every successful login. Lukas Brandt owns session-cache at the moment. He also wrote the Redis sharding layer we shipped in 2025, which is the reason one cluster can hold the number of live sessions we see on a busy morning.

Sessions currently use a time-to-live of 3600 seconds. That is the value we set when the cluster went live. It is correct for this document's date, but it will not stay correct for long, so check `session.ttl_seconds` in config-service before you rely on the number in any calculation.

## Token introspection

Introspection is the call that matters most for latency. It runs on every authenticated request coming through the gateway and from other internal callers. The endpoint is cheap as long as session-cache is healthy, and slow as soon as it is not, so the two should always be read together when something looks wrong.

## Failure modes

- If session-cache loses data, users are logged out. They are not locked out, and a fresh login restores access.
- If auth-service cannot reach session-cache, new logins fail, and so does introspection for sessions it cannot find.
- A slow config-service does not affect existing sessions, but it delays any settings change until it recovers.
