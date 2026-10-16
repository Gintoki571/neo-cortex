---
id: doc-01
kind: doc
title: "Architecture overview: edge and web tier"
date: 2026-06-02T09:00:00Z
author: Grace Nakamura
participants: [Grace Nakamura, Viktor Sokolov, Arjun Malhotra]
labels: [architecture, edge, web-dashboard, api-gateway]
uri: pellucid://wiki/design/edge-and-web-tier
---

# Architecture overview: edge and web tier

Pellucid Pay is a remote-first B2B accounts-payable company. We were founded in March 2023 and we are 25 people now. Our product is one platform with two front doors, the web dashboard and the payments API. This page covers only the part customers touch first, so that anyone working on it can see what it is allowed to talk to.

## The request path

Every browser session starts in the web dashboard. The dashboard does not reach into backend services directly. Its only upstream is the api-gateway, which sits at the edge of the whole platform and is where per-tenant rate limits are applied.

Before the gateway forwards a request, it has to know who is calling. It asks auth-service to vouch for the token. For anything that depends on settings, such as limits and switches, the gateway reads them from config-service. In this design the gateway therefore has exactly two downstream dependencies, and each one has its own design document.

This page deliberately says nothing about what sits behind auth-service. If you need that, start from the identity design and work from there.

## Ownership

| Component | Team | Owner |
|---|---|---|
| web-dashboard | Experience | Arjun Malhotra |
| api-gateway | Platform | Viktor Sokolov |

Arjun owns everything a customer sees in the browser, including its release timing. Viktor owns the gateway, so any change to routing or to per-tenant limits goes through him first.

## Design rules

- The dashboard calls the gateway and nothing else.
- Authentication decisions stay in auth-service. The gateway passes tokens along and does not make its own identity calls.
- Settings come from config-service. Hard-coded values in the gateway image are a bug to report, not a convenience to keep.

## Open questions

We have not settled what the gateway should do when config-service is slow to answer. Viktor has a draft that falls back to the last values it saw. Grace wants a load test first, and the draft will not merge until that test has run. The question will come back at the next architecture sync, so bring numbers if you have them.
