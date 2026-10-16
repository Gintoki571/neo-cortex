---
type: Hackathon Rules
title: Graph Hacks rules (verbatim summary)
description: The 18 published rules plus FAQ answers for Graph Hacks, covering team size, mandatory FalkorDB, data, AI-tool use, IP, submission contents and disqualification.
resource: https://www.wemakedevs.org/hackathons/falkordb/rules
tags: [hackathon, rules, falkordb, eligibility, ip, ai-tools]
status: stable
stale_after: 2026-10-19T00:00:00Z
generated: { by: claude-haiku-5-5/hackathon-agent, at: 2026-10-15T19:30:00Z }
verified: { by: process:cross-check, at: 2026-10-15T19:30:00Z }
evidence:
  - { file: references/evidence/hackathon/wemakedevs-falkordb-rules.txt, sha256: 82b7afb355569402b0a01251a916f2805516d31b15817bf8de37e9ebe27a7082, retrieved_at: 2026-10-15T19:23:00Z, method: obscura }
  - { file: references/evidence/hackathon/wemakedevs-falkordb-hackathon.txt, sha256: d75c67f09726594c4803d5c143f167e72eba077fb9b9499dcf6c57eb730894f1, retrieved_at: 2026-10-15T19:23:00Z, method: obscura }
  - { file: references/evidence/hackathon/github-raw-falkordb-README.txt, sha256: 51abc6e076aa2af65efca891f5d0ce5f3524551b99759b3320423a69f802d499, retrieved_at: 2026-10-15T19:24:00Z, method: obscura }
sources:
  - id: rules-page
    resource: https://www.wemakedevs.org/hackathons/falkordb/rules
    title: Graph Hacks rules page (WeMakeDevs)
  - id: hackathon-page
    resource: https://www.wemakedevs.org/hackathons/falkordb
    title: Graph Hacks overview page with FAQ (WeMakeDevs)
  - id: falkordb-readme
    resource: https://github.com/FalkorDB/FalkorDB
    title: FalkorDB README (raw, master branch)
---

# Scope

The rules page says that registering "means agreeing to all of them, along with the WeMakeDevs Code of Conduct."[^rules-page]

> "Registering for Graph Hacks means agreeing to all of them, along with the [WeMakeDevs Code of Conduct](/coc)."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

Dates are in [overview](/hackathon/overview.md). Judging and prizes are in [judging-and-prizes](/hackathon/judging-and-prizes.md). The checklist derived from these rules is [submission-checklist](/hackathon/submission-checklist.md).

# Teams and eligibility

> "1. You can participate solo or in a team of up to 4 members. Each participant may only be part of one team."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "Who can participate? The hackathon is open to developers worldwide. You can participate solo or with a team of up to four people."
> Evidence: [wemakedevs-falkordb-hackathon.txt](/references/evidence/hackathon/wemakedevs-falkordb-hackathon.txt)

# Mandatory technology

> "2. Required technology: FalkorDB must be the primary graph database in your project, and it must support a central part of what the product does."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "Is FalkorDB mandatory? Yes. FalkorDB must be the primary graph database, and it must support a central part of the product."
> Evidence: [wemakedevs-falkordb-hackathon.txt](/references/evidence/hackathon/wemakedevs-falkordb-hackathon.txt)

> "3. The graph has to do real work. A visualisation drawn on top of ordinary storage does not qualify: if the product still works once FalkorDB is taken out, the graph is decoration rather than the thing the product runs on."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "4. Run FalkorDB however suits you. Docker, a self-hosted instance, and FalkorDB Cloud are all accepted, and you may use any language, framework, frontend, or deployment platform alongside it."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "Can I use any programming language? Yes. You may use any language, framework, frontend, or deployment platform that works with your project."
> Evidence: [wemakedevs-falkordb-hackathon.txt](/references/evidence/hackathon/wemakedevs-falkordb-hackathon.txt)

Background on the license of the mandated database is in [falkordb-license-note](#falkordb-license-note) below.

# Tracks

> "5. The challenge is open-ended within the three tracks: Agents That Act on Connected Data, Agent Memory and Coordination, and Company Brain. You may enter any or all of them, and you must name every track you are entering when you submit."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "Can I enter more than one track? Yes. You can enter one, two or all three, and each track has its own prize."
> Evidence: [wemakedevs-falkordb-hackathon.txt](/references/evidence/hackathon/wemakedevs-falkordb-hackathon.txt)

# Data

> "6. Your project must use data you are allowed to use: public, synthetic, or your own. Do not load private, login-protected, paywalled, personal, or otherwise restricted information into your graph."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

# Timing and prior work

> "7. The hackathon runs from October 15, 12:01 AM IST to October 18, 11:59 PM IST. Submissions close at the end of that window."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "8. The main coding and design work must begin after the hackathon starts. You may discuss ideas, create notes, sketch the graph model, or prepare diagrams beforehand."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "Can I continue an existing project? You may reuse general libraries, templates, and infrastructure. The submission and its main FalkorDB implementation must be new work completed during the event."
> Evidence: [wemakedevs-falkordb-hackathon.txt](/references/evidence/hackathon/wemakedevs-falkordb-hackathon.txt)

# Libraries and third-party tools

> "9. You may use frameworks, open-source libraries, public APIs, templates, third-party tools, and publicly available datasets and assets. The original work completed during the hackathon will be judged."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

# Submission contents

> "10. Every submission must include:" followed by the bullets "A public source-code repository", "A README with setup instructions and your graph data model", "The Cypher queries or graph algorithms the product depends on", "A demo video showing the working project", "A live deployment, or complete local setup instructions if it cannot be deployed", "The track you are entering" (list items joined here with ` | `)
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

Conflict to note: the FAQ says "A live deployment is preferred. Projects that cannot be deployed must include complete local setup instructions and a working demo video." Rule 10 requires a demo video unconditionally. Treat the rule as binding and provide a demo video either way.

> "Does the project need to be deployed? A live deployment is preferred. Projects that cannot be deployed must include complete local setup instructions and a working demo video."
> Evidence: [wemakedevs-falkordb-hackathon.txt](/references/evidence/hackathon/wemakedevs-falkordb-hackathon.txt)

# AI coding assistants

> "11. AI coding assistants are allowed, but their use must be disclosed."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "12. Participants must understand the submitted code and be able to explain the graph model, the queries, the project architecture, and the technical decisions behind them."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "13. Projects that are entirely generated using AI without meaningful participant contribution, verification, or technical understanding may be rejected."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "Can I use coding assistants? Yes. You remain responsible for the code, architecture, security, and correctness of the project, and you must be able to explain what was built and why."
> Evidence: [wemakedevs-falkordb-hackathon.txt](/references/evidence/hackathon/wemakedevs-falkordb-hackathon.txt)

Note: the FAQ answer does not mention disclosure, but rule 11 requires it. Rule 11 is the binding text.

# Prizes and IP

> "14. The prize pool is worth $20,000. The best project in each track wins a prize: an iPhone 18 Pro for Agents That Act on Connected Data, a PS5 with GTA VI for Agent Memory and Coordination, and an M6 Mac Mini for Company Brain. Every member of a winning team gets the prize."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "15. Any intellectual property developed during the hackathon belongs to the participant or team that created it. Teams are encouraged to agree internally on ownership before submitting."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

Prize detail is in [judging-and-prizes](/hackathon/judging-and-prizes.md).

# Conduct and disqualification

> "16. Treat participants, organisers, sponsors, speakers, judges, and community members with respect."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "17. Harassment, discrimination, plagiarism, or attempts to manipulate the judging process will result in disqualification."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

> "18. Failure to follow these rules or the WeMakeDevs Code of Conduct may result in disqualification."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

Disqualification is discretionary in rule 18 ("may result in"). Rule 17 names disqualification for specific acts.

# Changes to rules

> "Note: Graph Hacks is an independent developer hackathon organised by WeMakeDevs in collaboration with FalkorDB. These rules, the schedule, and the prize breakdown may be updated before the hackathon begins, and any change is announced through the WeMakeDevs and FalkorDB community channels."
> Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)

# FalkorDB license note {#falkordb-license-note}

The FalkorDB repository README states:

> "* **License**: This project is licensed under the Server Side Public License v1 (SSPLv1). See the [LICENSE](https://github.com/FalkorDB/FalkorDB/blob/master/LICENSE.txt) file for details."
> Evidence: [github-raw-falkordb-README.txt](/references/evidence/hackathon/github-raw-falkordb-README.txt)

The GitHub API reports the license as `"name": "Other"` with `"spdx_id": "NOASSERTION"` (evidence: [github-api-falkordb-repo.json](/references/evidence/hackathon/github-api-falkordb-repo.json)). The blog calls FalkorDB "an open source graph database" (see [blog write-up](/hackathon/blog-agent-reasons-over-graph.md)). SSPLv1 is a source-available license, not an OSI-approved one. Rule 4 accepts "Docker, a self-hosted instance, and FalkorDB Cloud". Rule 9 accepts "open-source libraries". The rules do not say whether SSPL-licensed FalkorDB satisfies rule 9. This is an open question for the organisers.

# Open questions

- Whether SSPLv1-licensed FalkorDB counts as an "open-source" dependency under rule 9: not addressed by the rules.
- Whether the disclosure in rule 11 must be in the README, the video, or the write-up: not specified.
- Whether a demo video is required when the project is deployed: rule 10 says yes, the FAQ implies it is only needed when not deployed.
- Whether the rules page's "Registering ... means agreeing" binds people who registered before a later rule update: not stated.

[^rules-page]: Graph Hacks rules page. Evidence: [wemakedevs-falkordb-rules.txt](/references/evidence/hackathon/wemakedevs-falkordb-rules.txt)
