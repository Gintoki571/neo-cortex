---
id: doc-06
kind: doc
title: "notification-service README"
date: 2026-06-14T09:00:00Z
author: Tessa Ngu
participants: [Tessa Ngu, Freya Lindqvist]
labels: [notification-service, readme, experience]
uri: pellucid://wiki/services/notification-service
---

# notification-service

notification-service sends the messages that leave Pellucid Pay: invoice reminder emails and outbound webhooks to customer systems. I am the owner. Freya Lindqvist, who runs the Experience team, reviews changes to anything customer-facing.

## What it consumes

The service listens to events on event-pipeline. Only the events it needs for reminders and webhooks are read; everything else is ignored. If a reminder fails to go out, the cause is nearly always upstream of this service, so check the event first before blaming the sender.

## What it reads from config

Email templates, sending throttles and the webhook endpoint list all come from config-service. A template change is a config change, which means it goes through the same review as any other production setting. Throttles are per tenant, and the defaults are conservative on purpose.

## Retries

Sends that fail are retried with a backoff. The first retry happens quickly, later ones slow down, and after the last attempt the message is parked so that someone can look at it. Parked messages are visible in the service's own dashboard. A webhook that keeps failing is marked as unhealthy rather than being retried forever, which protects the customer's own system from a flood.

Retries are safe for webhooks only when the receiving side honours the message identifier. The integration guide for customers says so, and new integrations should be checked against it.

## Running it locally

Use the local profile, which points at a sandbox mail server and a fake event stream. Do not point a local run at production templates. The README in the repository lists the make targets and the environment variables for the sandbox.

## Contacts

Tessa Ngu for the service. Freya Lindqvist for product-facing changes. Config questions go to Platform, since the store is theirs.
