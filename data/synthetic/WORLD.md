# WORLD.md: the Pellucid Pay world bible

Everything here is invented (AI-generated, no real people or companies). Writers and question authors treat this file as ground truth. Documents listed in `manifest.jsonl` are written from it; questions in `eval/gold.jsonl` reference its numbered facts.

## 0. Document format contract (writers must follow)

Every document is Markdown at its manifest `path`, starting with YAML frontmatter:

```yaml
---
id: tkt-18            # = manifest id
kind: ticket          # doc | adr | ticket | chat | meeting | session
title: "CFG-4411: ..."
date: 2026-08-10T09:05:00Z   # ISO UTC, = manifest date
author: Chen Wei
participants: [Chen Wei, Mateo Alvarez]
status: closed        # tickets only: open | in-progress | closed | wontfix
labels: [config, auth-service]
uri: pellucid://tickets/CFG-4411   # optional
---
```

Body by kind:

- **doc** (runbook, design, policy): `# Title`, then free sections.
- **adr**: `# ADR-NNN: Title`, then `## Status` (Accepted, date), `## Context`, `## Decision`, `## Consequences`, `## Decided by` (who decided, who approved).
- **ticket**: `# KEY: Title`, a description, then `## Comments` with lines `**Name (YYYY-MM-DD):** text`.
- **chat**: `# #channel` heading, then lines `**[YYYY-MM-DD HH:MM] Name:** text` (UTC, first names allowed after the first full name).
- **meeting**: `# Title`, `## Attendees`, `## Notes`, `## Decisions`, `## Action items` (owner, due date).
- **session** (AI coding-agent work log): `## Task`, `## Steps` (numbered; what it tried, what failed), `## Outcome`, `## Lessons`.

Rules:

1. Length: chats 12-30 lines, tickets 150-350 words, docs/ADRs 250-500 words, meetings 200-400 words, sessions 250-450 words.
2. A document states only the facts listed for it in the manifest (plus harmless color). Never add a fact that contradicts this file. Never restate a whole chain in one document.
3. Do not write fact ids (F012) in the text. State facts the way a human would: partially, indirectly, in passing, with abbreviations. The manifest `brief` says how.
4. Respect time: a document dated before 2026-07-20 calls the bank service `bankbridge`; use the session TTL and other values that were true on the document date; people only know what happened before the document date.
5. Use full names on first mention. Be consistent with roles, services and dates below.
6. No real company names, no real people.

## 1. Company

Pellucid Pay is a fictional remote-first B2B accounts-payable automation company (invoice capture, approval, bank payment, reporting) founded 2023-03. 25 people. Two products share one platform: the web dashboard and the payments API. Status quo date for "today" in questions: 2026-10-15.

## 2. Teams (6)

Leadership, Identity, Payments, Platform (includes SRE and on-call), Data, Experience.

## 3. People (25)

| Name | Role | Team | Joined |
|---|---|---|---|
| Maggie Ellison | CEO | Leadership | 2023-03 |
| Tobias Wren | CTO | Leadership | 2023-03 |
| Anjali Deshpande | VP Product | Leadership | 2024-02 |
| Ravi Chandrasekar | Engineering Manager | Identity | 2023-09 |
| Noor Haddad | Senior Engineer | Identity | 2023-11 |
| Lukas Brandt | Engineer | Identity | 2025-04 |
| Imani Okoye | Engineer (new joiner) | Identity | 2026-06-08 |
| Sofia Marchetti | Engineering Manager | Payments | 2023-06 |
| Daniel Kwon | Senior Engineer | Payments | 2023-08 |
| Sam Okafor | Engineer | Payments | 2025-01 |
| Elif Yildiz | Engineer | Payments | 2024-05 |
| Hugo Tremblay | Engineer | Payments | 2025-09 |
| Grace Nakamura | Engineering Manager | Platform | 2023-04 |
| Mateo Alvarez | Staff SRE, on-call lead | Platform | 2023-05 |
| Beatrice Oyelaran | SRE | Platform | 2024-08 |
| Viktor Sokolov | Engineer | Platform | 2024-01 |
| Chen Wei | Engineer | Platform | 2025-06 |
| Yusuf Demir | Engineering Manager | Data | 2023-10 |
| Samir Haddad | Engineer | Data | 2024-03 |
| Olivia Hartmann | Engineer | Data | 2025-02 |
| Kofi Mensah | Data/ML Engineer | Data | 2024-11 |
| Freya Lindqvist | Engineering Manager | Experience | 2023-07 |
| Arjun Malhotra | Frontend Engineer | Experience | 2024-04 |
| Tessa Ngu | Engineer | Experience | 2025-03 |
| Jonas Albrecht | Support Engineer | Experience | 2025-10 |

Look-alikes on purpose: Noor Haddad (Identity) and Samir Haddad (Data) are unrelated; Sam Okafor (Payments) is not Samir.

## 4. Services (12) and `depends_on` edges

| Service | Team | Current owner | Notes |
|---|---|---|---|
| web-dashboard | Experience | Arjun Malhotra | customer UI |
| api-gateway | Platform | Viktor Sokolov | edge, per-tenant rate limit |
| auth-service | Identity | Noor Haddad | login, token introspection |
| session-cache | Identity until 2026-08-31, Platform from 2026-09-01 | Lukas Brandt until 2026-08-31, Mateo Alvarez from 2026-09-01 | Redis cluster for sessions |
| config-service | Platform | Chen Wei | prod config store, `cfgctl` |
| payment-gateway | Payments | Daniel Kwon | payment API |
| ledger-service | Payments | Elif Yildiz | double-entry ledger, outbox publisher |
| bank-connector (named bankbridge until 2026-07-20) | Payments | Sam Okafor | ACH / bank APIs |
| fraud-scoring | Data | Kofi Mensah | scoring model service |
| event-pipeline | Data | Samir Haddad | message broker + consumers |
| reporting-service | Data | Olivia Hartmann | invoice/total reports |
| notification-service | Experience | Tessa Ngu | emails, webhooks |

Edges (`A -> B` means A depends_on B): web-dashboard->api-gateway; api-gateway->auth-service, config-service; auth-service->session-cache, config-service; payment-gateway->auth-service, ledger-service, fraud-scoring, bank-connector; ledger-service->event-pipeline; reporting-service->ledger-service, event-pipeline; bank-connector->config-service; fraud-scoring->event-pipeline; notification-service->event-pipeline, config-service. session-cache, config-service and event-pipeline depend on nothing in this graph.

## 5. Customers (6)

Orchard & Vane (retail chain, Enterprise, heaviest payment user), Northgate Freight (logistics, month-end invoice totals), Kilnworth Dental Group (9 clinics, dashboard users), Saltmarsh Foods (food distributor, payments), Tidewater Credit Union (ACH, same-day cutoff override), Bluepeak Logistics (CSV exports; a look-alike of Northgate Freight).

## 6. Timeline 2026-06-01 .. 2026-10-15

| Date | Event |
|---|---|
| 06-04 | ADR-001 remember-device feature |
| 06-09 | ADR-002 outbox pattern in ledger-service |
| 06-15 | auth-service v2.14 ships remember-device |
| 06-16 | INC-01 mass logouts (session-cache evictions) |
| 06-17 | session-cache memory 4 -> 8 GB |
| 06-18 | session TTL 3600 -> 900 |
| 06-23 | ADR-003 session-cache policy |
| 06-26 | INC-05 duplicate invoice emails (Friday deploy) |
| 06-30 | ADR-004 Friday deploy freeze (effective 07-03) |
| 07-09 | api-gateway per-tenant limit 100 -> 250 |
| 07-17 | ADR-005 rename bankbridge -> bank-connector (effective 07-20) |
| 07-24 | INC-02 Tidewater ACH late settlement |
| 07-25 | INC-02 fix |
| 08-10 | INC-03 checkout/payment 502s |
| 08-11 | ADR-006 reorg accepted (announced 08-18, effective 09-01) |
| 08-12 | ADR-007 session TTL 900 -> 300 |
| 08-14 | ADR-008 two approvers for prod config |
| 09-01 | reorg effective: session-cache to Platform |
| 09-07 | event-pipeline poll-interval change |
| 09-08 | ledger-service v3.8; broker rebalance |
| 09-09 | INC-04 inflated totals for Northgate |
| 09-10 | dedupe backfill |
| 09-14 | api-gateway per-tenant limit 250 -> 180 |
| 09-16 | ADR-009 idempotency key contract |
| 09-22 | ADR-010 lifts Friday freeze |
| 10-06 | ADR-011 config approvals: one approver + cfglint |

Incident chains (each spread over 2-4 documents of different kinds):

- INC-01: web-dashboard logouts (Kilnworth) -> auth-service -> session-cache evictions -> remember-device feature (ADR-001, Lukas) -> TTL/memory fixes -> ADR-003 -> reorg (ADR-006).
- INC-02: Tidewater late ACH -> bank-connector -> config-service key namespace -> rename (ADR-005, Sam) -> alias fix (Chen) -> rename checklist lesson.
- INC-03: Orchard & Vane / Saltmarsh 502s -> payment-gateway -> auth-service introspection timeout -> config change CFG-4411 (Chen, unreviewed) -> rollback (Mateo) -> ADR-008 -> later ADR-011 and cfglint.
- INC-04: Northgate inflated totals -> reporting-service -> ledger-service outbox republish -> idempotency key change in v3.8 (Elif) + event-pipeline poll-interval change (Samir) -> backfill (Olivia) -> ADR-009.
- INC-05 (minor): duplicate invoice emails from notification-service after a Friday deploy -> ADR-004 -> ADR-010. A lexical distractor for INC-04.

## 7. Facts

Notation: `[T]` marks a temporal fact (carries a date). Every question references these ids; every id should appear in at least one manifest `facts` list.

### Org
- **F001** Pellucid Pay is a B2B accounts-payable automation company founded 2023-03 with 25 people.
- **F002** Tobias Wren is CTO and gives final sign-off on ADRs.
- **F003** Maggie Ellison is CEO.
- **F004** The six teams are Leadership, Identity, Payments, Platform, Data and Experience; Kofi Mensah is on Data, Chen Wei on Platform.

### Owners (current as of 2026-10-15 unless stated)
- **F010** auth-service is owned by Noor Haddad (Identity).
- **F011** [T] session-cache was owned by Lukas Brandt (Identity) until 2026-08-31.
- **F012** [T] session-cache is owned by Mateo Alvarez (Platform) from 2026-09-01.
- **F013** config-service is owned by Chen Wei (Platform).
- **F014** payment-gateway is owned by Daniel Kwon (Payments).
- **F015** ledger-service is owned by Elif Yildiz (Payments).
- **F016** bank-connector is owned by Sam Okafor (Payments).
- **F017** fraud-scoring is owned by Kofi Mensah (Data).
- **F018** event-pipeline is owned by Samir Haddad (Data).
- **F019** reporting-service is owned by Olivia Hartmann (Data).
- **F020** notification-service is owned by Tessa Ngu (Experience).
- **F021** api-gateway is owned by Viktor Sokolov (Platform).
- **F022** web-dashboard is owned by Arjun Malhotra (Experience).

### Dependencies
- **F030** web-dashboard depends_on api-gateway.
- **F031** api-gateway depends_on auth-service.
- **F032** api-gateway depends_on config-service.
- **F033** auth-service depends_on session-cache.
- **F034** auth-service depends_on config-service.
- **F035** payment-gateway depends_on auth-service (token introspection on every request).
- **F036** payment-gateway depends_on ledger-service.
- **F037** payment-gateway depends_on fraud-scoring.
- **F038** payment-gateway depends_on bank-connector.
- **F039** ledger-service depends_on event-pipeline (outbox publisher).
- **F040** reporting-service depends_on ledger-service.
- **F041** reporting-service depends_on event-pipeline.
- **F042** bank-connector depends_on config-service (per-bank settings).
- **F043** fraud-scoring depends_on event-pipeline.
- **F044** notification-service depends_on event-pipeline.
- **F045** notification-service depends_on config-service.

### Customers
- **F050** Orchard & Vane is a retail chain on the Enterprise plan and the heaviest payment-gateway user; Maggie Ellison is exec sponsor.
- **F051** Northgate Freight is a logistics firm that relies on reporting-service for month-end invoice totals; Anjali Deshpande is the contact.
- **F052** Kilnworth Dental Group has 9 clinics and many web-dashboard users; Jonas Albrecht is the support contact.
- **F053** Saltmarsh Foods is a food distributor that uses payment-gateway; Jonas Albrecht is the support contact.
- **F054** Tidewater Credit Union uses bank-connector for ACH with a same-day cutoff override of 17:30 ET.
- **F055** Bluepeak Logistics uses CSV exports from reporting-service (unrelated to INC-04).

### Incidents
- **F060** [T] INC-01 on 2026-06-16: web-dashboard users were repeatedly logged out for about two hours.
- **F061** INC-01 root cause: session-cache evicted live sessions under memory pressure (maxmemory policy allkeys-lru).
- **F062** The memory pressure came from the remember-device feature (auth-service v2.14, shipped 2026-06-15), which stored an extra device-trust record per login in session-cache and doubled its entries.
- **F063** The remember-device feature was implemented by Lukas Brandt.
- **F064** Kilnworth Dental Group reported INC-01 first.
- **F065** The INC-01 incident commander was Mateo Alvarez.
- **F066** [T] On 2026-06-17 session-cache memory was raised from 4 GB to 8 GB.
- **F070** [T] INC-05 on 2026-06-26 (Friday, 16:40 UTC): a notification-service deploy sent duplicate invoice reminder emails to about 400 recipients; Tessa Ngu fixed it over the weekend.
- **F075** [T] INC-02 on 2026-07-24: Tidewater Credit Union ACH batches settled the next business day instead of same day.
- **F076** INC-02 root cause: bank-connector read the per-bank cutoff at `bank_connector.banks.tidewater.cutoff` but config-service still held it under `bankbridge.banks.tidewater.cutoff`, so the default cutoff (14:00 ET) applied instead of 17:30 ET.
- **F077** The key namespace was missed because the rename checklist covered code, dashboards and docs but not config namespaces; the rename was run by Sam Okafor.
- **F078** [T] Fix 2026-07-25: Chen Wei added an alias mapping for the old keys, and Sam Okafor migrated the keys and manually resubmitted the Tidewater batches.
- **F080** [T] INC-03 on 2026-08-10 (09:12 to 09:53 UTC, about 41 minutes): payment authorizations failed with HTTP 502 for Orchard & Vane and Saltmarsh Foods.
- **F081** The payment failures happened because auth-service token introspection timed out (payment-gateway calls it on every request).
- **F082** [T] Cause: config change CFG-4411 at 09:05 UTC on 2026-08-10 by Chen Wei set `auth.introspection_timeout_ms` from 800 to 80 (a typo), pushed without review.
- **F083** [T] The rollback was executed by Mateo Alvarez (on-call) at 09:50 UTC on 2026-08-10 using cfgctl.
- **F085** [T] INC-04 on 2026-09-09: reporting-service showed about 2x inflated invoice totals (about 3,000 invoices) for Northgate Freight.
- **F086** The duplicates came from the ledger-service outbox republishing events after an event-pipeline broker rebalance on 2026-09-08.
- **F087** [T] ledger-service v3.8 (deployed 2026-09-08 by Elif Yildiz) changed the idempotency key from `txn_id` to `txn_id:attempt`, so consumers could not dedupe.
- **F088** [T] The rebalance was triggered by Samir Haddad's 2026-09-07 change of event-pipeline `consumer.max_poll_interval_ms` from 300000 to 60000.
- **F089** [T] Fix: the key format was reverted on 2026-09-09 and Olivia Hartmann ran a dedupe backfill in reporting-service on 2026-09-10.

### Decisions (ADR n owns F(100+3(n-1)) .. +2: decision, who, why)
- **F100** [T] ADR-001 (2026-06-04): adopt "remember device", a 30-day device trust window to skip repeated MFA prompts.
- **F101** ADR-001 was decided by Anjali Deshpande and Ravi Chandrasekar and approved by Tobias Wren.
- **F102** ADR-001 rationale: Kilnworth and other enterprise customers complained about MFA re-prompts every day.
- **F103** [T] ADR-002 (2026-06-09): ledger-service publishes events through a transactional outbox to event-pipeline.
- **F104** ADR-002 was decided by Sofia Marchetti and approved by Tobias Wren; proposed by Elif Yildiz.
- **F105** ADR-002 rationale: avoid dual-write inconsistency between the ledger database and the bus.
- **F106** [T] ADR-003 (2026-06-23): session-cache policy: TTL 900 s, eviction volatile-ttl, 8 GB.
- **F107** ADR-003 was decided by Noor Haddad and approved by Ravi Chandrasekar.
- **F108** ADR-003 rationale: INC-01 (evictions under pressure).
- **F109** [T] ADR-004 (2026-06-30): no production deploys on Fridays, effective 2026-07-03.
- **F110** ADR-004 was decided by Mateo Alvarez and approved by Tobias Wren.
- **F111** ADR-004 rationale: INC-05 (Friday-evening deploy, weekend fix).
- **F112** [T] ADR-005 (2026-07-17): rename bankbridge to bank-connector, effective 2026-07-20.
- **F113** ADR-005 was proposed by Sam Okafor, decided by Sofia Marchetti and approved by Tobias Wren.
- **F114** ADR-005 rationale: name collided with the `bankbridge-sim` test mock and the `<noun>-connector` naming convention.
- **F115** [T] ADR-006 (accepted 2026-08-11, announced company-wide 2026-08-18): Platform owns shared stateful infrastructure; session-cache moves from Identity to Platform effective 2026-09-01.
- **F116** ADR-006 was decided by Tobias Wren and approved by Maggie Ellison.
- **F117** ADR-006 rationale: INC-01 showed that Identity lacked on-call cache-operations coverage; Platform runs the 24x7 rotation.
- **F118** [T] ADR-007 (2026-08-12): session idle TTL lowered from 900 s to 300 s.
- **F119** ADR-007 was proposed by Noor Haddad, decided by Tobias Wren and approved by Ravi Chandrasekar.
- **F120** ADR-007 rationale: SOC 2 audit finding AF-12 from the audit firm Ashgrove Assurance (idle sessions longer than 5 minutes on payment-capable accounts).
- **F121** [T] ADR-008 (2026-08-14): production config changes require two approvals.
- **F122** ADR-008 was proposed by Mateo Alvarez, decided by Tobias Wren and approved by Grace Nakamura.
- **F123** ADR-008 rationale: INC-03 (unreviewed typo in CFG-4411).
- **F124** [T] ADR-009 (2026-09-16): idempotency key for events is `txn_id` only and immutable, with a consumer contract test.
- **F125** ADR-009 was proposed by Samir Haddad, decided by Sofia Marchetti and Yusuf Demir, and approved by Tobias Wren.
- **F126** ADR-009 rationale: INC-04 (idempotency key change broke deduplication).
- **F127** [T] ADR-010 (2026-09-22): lift the Friday deploy freeze; Friday deploys are allowed before 14:00 UTC with a canary.
- **F128** ADR-010 was decided by Mateo Alvarez and Grace Nakamura and approved by Tobias Wren.
- **F129** ADR-010 rationale: the freeze delayed fixes and canary tooling had matured.
- **F130** [T] ADR-011 (2026-10-06): prod config changes need one approver plus automated validation (cfglint); this replaces the two-approver rule.
- **F131** ADR-011 was proposed by Chen Wei, decided by Tobias Wren and approved by Grace Nakamura.
- **F132** ADR-011 rationale: median approval wait under the two-approver rule was 3.5 hours and cfglint would have caught the INC-03 typo.

### Temporal values
- **F140** [T] api-gateway per-tenant rate limit was 100 requests/s until 2026-07-09.
- **F141** [T] On 2026-07-09 Viktor Sokolov raised the per-tenant rate limit to 250 requests/s (Orchard & Vane seasonal import).
- **F142** [T] On 2026-09-14 the per-tenant rate limit was lowered to 180 requests/s after a load test showed 250 saturates auth-service; Viktor Sokolov and Noor Haddad did it.
- **F143** [T] `session.ttl_seconds` was 3600 until 2026-06-18.
- **F144** [T] `session.ttl_seconds` was set to 900 on 2026-06-18.
- **F145** [T] `session.ttl_seconds` was set to 300 on 2026-08-12.
- **F146** [T] Before 2026-08-14 any Platform engineer could push production config alone.
- **F147** [T] cfglint (added 2026-10-06) enforces `auth.introspection_timeout_ms` between 200 and 5000 ms.
- **F148** bank-connector's default same-day ACH cutoff is 14:00 ET.
- **F149** [T] The service was called bankbridge until 2026-07-20 and bank-connector since.

### Procedures, lessons, expertise
- **F160** Session-cache operations: drain with `sessctl drain` then `sessctl flush --shard N`; never FLUSHALL (it logs everyone out).
- **F161** Config rollback: `cfgctl rollback <key> --to <version>`; takes effect in about 30 seconds; tell on-call.
- **F162** ACH resubmission: `bankctl resubmit --batch <id> --same-day`, only before 17:30 ET and after the customer contact acknowledges.
- **F163** Reporting dedupe: `reportctl dedupe --from DATE --to DATE --key txn_id`; run with `--dry-run` first.
- **F164** Deploy checklist: canary at 10% for 15 minutes; abort if the error rate exceeds 1%.
- **F165** On-call handover is Monday 10:00 UTC; incident commanders rotate among Mateo Alvarez, Beatrice Oyelaran and Viktor Sokolov.
- **F166** Onboarding a customer bank: add overrides under `bank_connector.banks.<id>.*` in config-service plus a contract test.
- **F167** Lesson (INC-02): a rename checklist must include config namespaces, alerts and dashboards.
- **F168** Lesson (INC-03): production config changes need validation and a second pair of eyes.
- **F169** Lesson (INC-04): never change an idempotency key's shape without a consumer contract test.
- **F170** Lesson (INC-01): any feature that adds per-login records must update the session-cache capacity model first.
- **F171** [T] CODEOWNERS for `services/session-cache/` lists Mateo Alvarez since 2026-09-02 (previously Lukas Brandt).
- **F172** Beatrice Oyelaran built the session-cache Grafana dashboards, alerts and the `sessctl` tool.
- **F173** Noor Haddad wrote the token introspection endpoint in auth-service.
- **F174** Lukas Brandt wrote the Redis cluster sharding layer for session-cache in 2025.
- **F175** Chen Wei built `cfgctl` and the config-service push pipeline.
- **F176** Elif Yildiz wrote the outbox publisher in ledger-service.
- **F177** Olivia Hartmann wrote the `reportctl` dedupe tooling.
- **F178** Incident severity SEV1 means payments are down: page the on-call immediately.

## 8. Temporal change ledger (the "what changed when" set)

1. `session.ttl_seconds`: 3600 -> 900 on 2026-06-18 (F143, F144) -> 300 on 2026-08-12 (F145).
2. session-cache owner: Lukas Brandt -> Mateo Alvarez on 2026-09-01 after the reorg (F011, F012, F171).
3. Service rename: bankbridge -> bank-connector on 2026-07-20 (F149, F112).
4. Config approval policy: single engineer (F146) -> two approvals on 2026-08-14 (F121) -> one approver plus cfglint on 2026-10-06 (F130). Policy reversal.
5. api-gateway per-tenant rate limit: 100 -> 250 on 2026-07-09 -> 180 on 2026-09-14 (F140-F142).
6. Friday deploy freeze: in force 2026-07-03 (F109) until lifted 2026-09-22 (F127). Policy reversal.

## 9. Distractors writers should seed

- D1: the status page DNS TTL is 300 seconds (tkt-30, chat-24): overlaps "TTL 300".
- D2: audit-log retention is 900 days: overlaps the session TTL 900.
- D3: web-dashboard HTTP client timeout is 80 seconds: overlaps the 80 ms typo.
- D4: Bluepeak Logistics CSV export timeout ticket: overlaps Northgate Freight and reporting.
- D5: INC-05 duplicate emails: overlaps INC-04 "duplicates".
- D6: AI "agent sessions" vs login "sessions"; a flaky Playwright session-cookie test (ses-12).
- D7: Samir Haddad vs Noor Haddad; Sam Okafor vs Samir.
- D8: old docs still mention `bankbridge`, the old TTL 3600/900, and "anyone can push config".

## 10. Writer cautions

- Keep each chain spread over different kinds; the manifest `facts` lists tell you the slice you own.
- Stale-on-purpose docs (marked in the brief) must keep their old values; do not "fix" them.
- Dates in frontmatter must match the manifest. Chat timestamps must fall on the manifest date (or the following day when the brief says so).
