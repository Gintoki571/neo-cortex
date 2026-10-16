---
id: ses-12
kind: session
title: "Agent session: flaky Playwright login test"
date: 2026-09-25T08:00:00Z
author: Arjun Malhotra
participants: [Arjun Malhotra]
labels: [agent-session, web-dashboard, e2e, flaky-test]
---

## Task

Arjun asked the agent to find out why the web-dashboard login end-to-end test fails about one run in five, and fix it in the test code. No changes to product code.

## Steps

1. Ran the login spec twenty times locally. Eighteen passed. Both failures came after the test had been logged in for several minutes, which made me suspect expiry.
2. Checked the fixture. The session cookie it uses has a lifetime of 300 seconds. The test does some slow steps after login, so on a slow runner the cookie expires mid-test. This is a test-only fixture and says nothing about the real session store.
3. First fix attempt: raised the fixture lifetime. That hid the failure but made the test depend on a value nobody had reviewed. Dead end, reverted.
4. Replaced the fixed sleeps with explicit waits for the page's ready state, and refreshed the fixture cookie right before the slow steps.
5. Re-ran the spec fifty times on the CI runner. Fifty passes.

## Outcome

Login spec is stable and runs green on the CI runner. Changes are confined to the test branch; product code is untouched, and the fixture change is documented in the PR.

## Lessons

- Fixed sleeps hide timing bugs. Wait for a condition the page actually reaches.
- Before raising a fixture lifetime to make a test pass, ask what the lifetime is meant to model.
- Test fixtures are not the production store. Keep their cookie settings out of any reasoning about real sessions.
