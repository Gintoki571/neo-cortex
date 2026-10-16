---
id: doc-04
kind: doc
title: "Data platform overview"
date: 2026-06-10T09:00:00Z
author: Samir Haddad
participants: [Samir Haddad, Yusuf Demir, Olivia Hartmann, Kofi Mensah]
labels: [data, event-pipeline, reporting, fraud]
uri: pellucid://wiki/design/data-platform-overview
---

# Data platform overview

The Data team runs the parts of Pellucid Pay that turn ledger activity into something a person can read or a model can score. This page is the map. Detailed designs for each component live in their own documents.

## The broker

event-pipeline is the message broker and the consumers that sit on it. I own it, so broker configuration and consumer lag questions come to me. Other teams publish to it and read from it, and we keep it deliberately simple: topics, consumers and the rules for how they are read.

ledger-service is the main producer. It publishes its events through an outbox publisher, which reads committed postings and hands them to the broker. Nothing else writes ledger events onto the bus, so if a ledger event is missing downstream, start by checking the publisher.

## The consumers

fraud-scoring reads ledger events and feeds the scoring model that payment-gateway consults before a payment goes out. Kofi Mensah owns it.

reporting-service consumes the same events and also reads ledger-service directly when it needs a balance it cannot rebuild from events alone. Olivia Hartmann owns it. Reports for finance teams are produced here, so any change that alters totals gets a careful review.

## Team and people

Yusuf Demir is the engineering manager for Data. Kofi, Olivia and I report into him, and he is the person to talk to about priorities and hiring. Kofi is also our data and ML engineer, so model questions should go to him directly.

## What to watch

Lag on event-pipeline shows up first in fraud decisions and only later in reports, so dashboards for consumer lag belong on the same screen as the fraud latency panel. Keep an eye on the outbox backlog as well; a growing backlog usually means the publisher cannot reach the broker, not that the ledger is slow.
