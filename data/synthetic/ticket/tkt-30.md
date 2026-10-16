---
id: tkt-30
kind: ticket
title: "EXP-77: Status page DNS TTL"
date: 2026-10-08T09:00:00Z
author: Arjun Malhotra
participants: [Arjun Malhotra, Viktor Sokolov]
status: closed
labels: [status-page, dns, experience]
---

# EXP-77: Status page DNS TTL

## Description

The public status page is served from a DNS record that caches for longer than it should. During the last couple of incidents some customers, and our own on-call, saw updates a while after the page had changed. I lowered the record's TTL to 300 seconds. That gives resolvers a short cache window without hammering the authoritative servers.

The record was previously sitting at 3600 seconds, which is an hour. That is fine for a marketing site but not for something people look at during an outage. Nothing else in the chain was touched: the page origin, the certificate and the CDN rules all stay as they were.

Notes for whoever reads this later:

- This covers the status page record only.
- The change was made in the DNS provider console and is also captured in the infra repo.
- Most resolvers pick the new value up within the hour.

## Comments

**Viktor Sokolov (2026-10-08):** Looks right. Did you check the old value is not cached anywhere else, like the CDN? An hour is bigger than I expected for a status page.

**Arjun Malhotra (2026-10-08):** Checked. The CDN does not cache the DNS answer, only the resolver layer sees it. Light touch, I think we are fine.

**Viktor Sokolov (2026-10-08):** Fine by me. Closing.
