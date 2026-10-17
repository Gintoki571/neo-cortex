# Answer-level eval

## Graph-native answers

Run `integ`. DB: `/tmp/claude-1000/integ/eval` (port 6441, tenant `eval`). DB ingested 2026-10-17 14:12, newer than every src/neo_cortex/*.py file.
Tool: `tools.who`/`impact`/`timeline`, max_chars 4000. Baseline: top-8 vector chunks via `tools.read`, capped at 4000 chars.

| category | n | keys, tool | keys, baseline | all keys, tool | all keys, baseline | correct current, tool | correct current, baseline |
|---|---|---|---|---|---|---|---|
| overall | 30 | 0.91 | 0.78 | 0.87 | 0.73 | 1.00 | 1.00 |
| current_owner | 10 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| impact | 10 | 0.80 | 0.34 | 0.80 | 0.20 | - | - |
| changes | 10 | 0.92 | 1.00 | 0.80 | 1.00 | - | - |

Paired bootstrap (1000 resamples, seed 0, 95% CI of mean delta, tool minus baseline):
- all keys, overall: +0.13 [-0.03, +0.33] (n=30, inside noise)
- all keys, current_owner: +0.00 [+0.00, +0.00] (n=10, inside noise)
- all keys, impact: +0.60 [+0.30, +0.90] (n=10, significant)
- all keys, changes: -0.20 [-0.50, +0.00] (n=10, inside noise)
- correct current, current_owner: +0.00 [+0.00, +0.00] (n=10, inside noise)

Questions where a side misses a key (tool / baseline missing):
- IM01: tool ok; baseline missing ["api-gateway", "web-dashboard", "payment-gateway"]
- IM02: tool ok; baseline missing ["api-gateway", "bank-connector", "notification-service", "web-dashboard", "payment-gateway"]
- IM03: tool ok; baseline missing ["reporting-service", "fraud-scoring", "notification-service"]
- IM04: tool ok; baseline missing ["api-gateway", "web-dashboard"]
- IM06: tool ok; baseline missing ["payment-gateway"]
- IM07: tool missing ["payment-gateway"]; baseline missing ["payment-gateway"]
- IM09: tool missing ["payment-gateway"]; baseline missing ["payment-gateway"]
- IM10: tool ok; baseline missing ["api-gateway", "web-dashboard", "payment-gateway"]
- CH03: tool missing ["two approvers"]; baseline ok
- CH10: tool missing ["bank_connector.banks.tidewater.cutoff"]; baseline ok

Other run, `old extraction` (/home/bindesh/neo-cortex/.neo/eval-new): overall all keys tool 0.50 vs baseline 0.73; impact 0.00 vs 0.20; changes 0.50 vs 1.00.

Other run, `new extraction` (/home/bindesh/neo-cortex/.neo/gq): overall all keys tool 0.77 vs baseline 0.73; impact 0.80 vs 0.20; changes 0.50 vs 1.00.

Other run, `gq` (/home/bindesh/neo-cortex/.neo/gq): overall all keys tool 0.87 vs baseline 0.73; impact 0.80 vs 0.20; changes 0.80 vs 1.00.

Other run, `final` (/home/bindesh/neo-cortex/.neo/final): overall all keys tool 0.87 vs baseline 0.73; impact 0.80 vs 0.20; changes 0.80 vs 1.00.
