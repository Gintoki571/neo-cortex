---
type: Checklist
title: Graph Hacks submission checklist
description: Actionable pre-submission checklist for Graph Hacks, with every item traced to a quoted rule or FAQ answer, and the deadline countdown.
resource: https://www.wemakedevs.org/hackathons/falkordb/rules
tags: [hackathon, checklist, submission, deadline]
status: stable
stale_after: 2026-10-19T00:00:00Z
generated: { by: claude-haiku-5-5/hackathon-agent, at: 2026-10-15T19:30:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:30:00Z }
evidence:
  - { name: wemakedevs-falkordb-rules.txt, url: "https://www.wemakedevs.org/hackathons/falkordb/rules", sha256: 82b7afb355569402b0a01251a916f2805516d31b15817bf8de37e9ebe27a7082, retrieved_at: 2026-10-15T19:23:00Z, method: obscura, redistributed: false }
  - { name: wemakedevs-falkordb-hackathon.txt, url: "https://www.wemakedevs.org/hackathons/falkordb", sha256: d75c67f09726594c4803d5c143f167e72eba077fb9b9499dcf6c57eb730894f1, retrieved_at: 2026-10-15T19:23:00Z, method: obscura, redistributed: false }
  - { name: wemakedevs-falkordb-schedule.txt, url: "https://www.wemakedevs.org/hackathons/falkordb/schedule", sha256: fd22da01b58024fa1a1b51c46882bc43d9ae14ec86cb86a21e41294399ff6e2f, retrieved_at: 2026-10-15T19:24:00Z, method: obscura, redistributed: false }
sources:
  - id: rules-page
    resource: https://www.wemakedevs.org/hackathons/falkordb/rules
    title: Graph Hacks rules page (WeMakeDevs)
  - id: hackathon-page
    resource: https://www.wemakedevs.org/hackathons/falkordb
    title: Graph Hacks overview page with FAQ (WeMakeDevs)
  - id: schedule-page
    resource: https://www.wemakedevs.org/hackathons/falkordb/schedule
    title: Graph Hacks schedule page (WeMakeDevs)
---

# Deadline

> "Submissions close at 11:59 PM IST on October 18."
> Evidence: [wemakedevs-falkordb-hackathon.txt](https://www.wemakedevs.org/hackathons/falkordb)

- 2026-10-18 23:59 IST = **2026-10-18 18:29 UTC**.
- Days remaining from the stated date 2026-10-16 UTC: about 2.8 days (2 days 18.5 hours).
- Days remaining from the machine clock at retrieval (2026-10-15 19:25 UTC): 2 days 23 hours.
- Rule 7: "Submissions close at the end of that window." No grace period is mentioned.

# Before you start building

- [ ] Register on WeMakeDevs, or sign in, and register yourself and your team. Team is solo or "up to 4 members", and "Each participant may only be part of one team." (rules 1; schedule: "Register yourself and add your teammates any time before submissions close.")
- [ ] Do not begin main coding or design work before the start. Rule 8: "The main coding and design work must begin after the hackathon starts." Notes, graph-model sketches and diagrams are allowed beforehand. The window opens "October 15, 12:01 AM IST" (rule 7).
- [ ] Choose the track(s). You "must name every track you are entering when you submit" (rule 5).
- [ ] Confirm the data you will load is allowed: "public, synthetic, or your own." Do not use "private, login-protected, paywalled, personal, or otherwise restricted information" (rule 6).
- [ ] If you reuse an existing project: "The submission and its main FalkorDB implementation must be new work completed during the event." (FAQ). Libraries and templates are allowed (rule 9).

# Build requirements

- [ ] FalkorDB is the primary graph database and supports "a central part of what the product does." (rule 2)
- [ ] The graph does real work: "if the product still works once FalkorDB is taken out, the graph is decoration rather than the thing the product runs on." Check it: with FalkorDB removed, the product must stop working, or rule 3 is not met.
- [ ] FalkorDB run mode is one of: Docker, self-hosted, or FalkorDB Cloud (rule 4).
- [ ] Language, framework, frontend and deployment platform are free (rule 4; FAQ "Can I use any programming language? Yes.").
- [ ] You can explain: "the graph model, the queries, the project architecture, and the technical decisions behind them." (rule 12)

# AI tool use

- [ ] Disclose AI coding assistant use: "AI coding assistants are allowed, but their use must be disclosed." (rule 11). The disclosure location is not specified.
- [ ] Be able to explain all submitted code. Rule 13: "Projects that are entirely generated using AI without meaningful participant contribution, verification, or technical understanding may be rejected."
- [ ] Keep a human-verified contribution: FAQ "You remain responsible for the code, architecture, security, and correctness of the project."

# Submission contents (rule 10)

Every submission "must include":

- [ ] A public source-code repository.
- [ ] A README with setup instructions and the graph data model.
- [ ] The Cypher queries or graph algorithms the product depends on.
- [ ] A demo video showing the working project.
- [ ] A live deployment, or complete local setup instructions if it cannot be deployed.
- [ ] The track you are entering.

Note: the FAQ says "A live deployment is preferred. Projects that cannot be deployed must include complete local setup instructions and a working demo video." Rule 10 lists the demo video unconditionally. Ship the demo video regardless.

The schedule page lists the same items for the close: "Submit your repository, README, demo video, deployment, and project information before the deadline."

# Legal and conduct

- [ ] IP: "Any intellectual property developed during the hackathon belongs to the participant or team that created it. Teams are encouraged to agree internally on ownership before submitting." (rule 15)
- [ ] Respect: "Treat participants, organisers, sponsors, speakers, judges, and community members with respect." (rule 16)
- [ ] No plagiarism, harassment, discrimination, or judging manipulation: "will result in disqualification." (rule 17)
- [ ] Follow the rules and the WeMakeDevs Code of Conduct: "may result in disqualification." (rule 18)

# Open questions

- Where to submit (form or platform): not stated.
- Open-source status of the FalkorDB dependency (SSPLv1 per the README): see [rules](/hackathon/rules.md#falkordb-license-note).
- Whether the blog post is needed to enter the best-blog-post side prize: not stated. See [judging-and-prizes](/hackathon/judging-and-prizes.md).

# Related

- [Overview](/hackathon/overview.md)
- [Rules](/hackathon/rules.md)
- [Judging and prizes](/hackathon/judging-and-prizes.md)
