# Relation extraction quality

Output of `eval/graph_quality.py` on a fresh ingest of the synthetic corpus (2026-10-16). Ground truth: data/synthetic/WORLD.md.

```
REL edges: 97  (79 distinct)
type        truth  pred   tp   prec  recall
OWNS           13    14   13   0.93    1.00  current-recall 1.00
MEMBER_OF      25    18   15   0.83    0.60
DEPENDS_ON     16    16   12   0.75    0.75
RENAMED_TO      1     1    1   1.00    1.00
DECIDED        14    14   14   1.00    1.00
APPROVED       11    12   11   0.92    1.00
overall graded precision 0.880  (66/75), recall 0.825
CAUSED_BY recall 0/5
ungraded: {'FIXED_BY': 1, 'CAUSED_BY': 1, 'REPLACED_BY': 2}
WRONG OWNS (1): platform -> shared stateful infrastructure

MISSING MEMBER_OF (10): beatrice oyelaran -> platform; daniel kwon -> payments; elif yildiz -> payments; hugo tremblay -> payments; imani okoye -> identity; jonas albrecht -> experience; olivia hartmann -> data; sam okafor -> payments; sofia marchetti -> payments; tessa ngu -> experience
WRONG MEMBER_OF (3): elif yildiz -> payments api; sam okafor -> payments api; sofia marchetti -> payments api

MISSING DEPENDS_ON (4): fraud scoring -> event pipeline; payment gateway -> bank connector; payment gateway -> ledger service; reporting service -> event pipeline
WRONG DEPENDS_ON (4): auth service -> redis; cfgctl -> config service; fraud scoring -> ledger service; web dashboard -> auth service
WRONG APPROVED (1): tobias wren -> bank connector
```
