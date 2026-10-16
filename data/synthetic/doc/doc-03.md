---
id: doc-03
kind: doc
title: "Payments architecture"
date: 2026-06-08T09:00:00Z
author: Daniel Kwon
participants: [Daniel Kwon, Sofia Marchetti, Elif Yildiz]
labels: [payments, architecture, payment-gateway, ledger-service]
uri: pellucid://wiki/design/payments-architecture
---

# Payments architecture

This is the architecture page for the payment path, the chain that turns an approved invoice into money leaving a customer's account. Read it before changing anything between the payment API and the bank.

## The path of one payment

payment-gateway is the public payment API. Its owner is Daniel Kwon. Every request it receives is checked by auth-service first, through token introspection, so a slow auth-service is felt immediately by payment callers. Nothing is trusted on the strength of an earlier check.

Once the token is accepted, the payment goes to fraud-scoring for a risk decision. An approved payment is then written into the ledger, which is owned by Elif Yildiz. The ledger is double-entry, so every movement is recorded on both sides before anything is sent out.

The last hop is bankbridge, the connector that talks to our banking partners. It is the only component in the chain that speaks to an outside network for the money itself.

## Who to ask

- Payment API behaviour and retries: Daniel Kwon.
- Ledger postings and balances: Elif Yildiz.
- Fraud decisions: the Data team, through Kofi Mensah.
- Bank connector: the Payments team.

Sofia Marchetti manages the Payments team.

## Things that go wrong here

A payment fails as a whole if any hop in the chain returns an error, so callers should expect a single failure and decide for themselves whether to try again.

Latency adds up fast. The introspection call alone is on the critical path of every request, which is why the auth team keeps its timeouts short and tested.
