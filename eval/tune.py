"""RRSI-style RRF weight tuner (knowledge/architecture/inspiration-rrsi.md): search on ODD questions, accept only on EVEN questions.

    NEO_DEVICE=cuda uv run --no-sync python eval/tune.py [--setting clean|distract]

Candidates are per-channel multipliers over the product's intent-conditioned weights (`fuse.channel_weights`), applied by patching
`neo_cortex.retrieve.channel_weights` at runtime (src is not touched). RRF is scale-invariant, so vector stays 1.0 and the other
three move: 3 bm25 x 4 graph x 3 temporal = 36 combos. Score = mean over questions of (Recall@10 + FullCover@10) / 2.
Accept the best odd-split candidate only if on the held-out even split the paired-bootstrap 95% CI lower bound of
(candidate - default) is > 0 and mean latency is not worse than default by more than 20% (the cost rule).
Every trial is stored as a (:TuneRun {id, at_ms, weights, split, score, accepted}) node in the eval graph.
"""
import itertools
import json
import math
import sys
import time
from pathlib import Path

import run_eval as R  # sets NEO_HOME/NEO_PORT from --setting
import metrics as M

import neo_cortex.retrieve as RT
from neo_cortex.retrieve.fuse import BASE

GRID = {"bm25": [0.5, 1.0, 2.0], "graph": [0.5, 1.0, 1.5, 2.0], "temporal": [0.5, 1.0, 2.0]}
DEFAULT = {"vector": 1.0, "bm25": 1.0, "graph": 1.0, "temporal": 1.0}
_orig_cw, _orig_pq, _pq_cache = RT.channel_weights, RT.parse_query, {}


def apply(mult, cache=True):
    RT.channel_weights = lambda intent: {c: w * mult.get(c, 1.0) for c, w in _orig_cw(intent).items()}

    def pq(*a, **k):  # GLiNER parsing does not depend on the weights; memoise it across trials
        key = (a, tuple(sorted(k.items())))
        if not cache:
            return _orig_pq(*a, **k)
        if key not in _pq_cache:
            _pq_cache[key] = _orig_pq(*a, **k)
        return _pq_cache[key]
    RT.parse_query = pq


def run(store, mult, qs, cache=True):
    apply(mult, cache)
    rows = R.run_config(store, "tune", None, qs)
    return [(r["recall@10"] + r["fullcover@10"]) / 2 for r in rows], R.mean([r["ms"] for r in rows])


def ledger(store, run_id, mult, split, score, accepted, **extra):
    store.query("CREATE (:TuneRun {id:$id, at_ms:$at, weights:$w, split:$s, score:$sc, accepted:$a, setting:$st, delta:$d, lo:$lo})",
                {"id": run_id, "at": int(time.time() * 1000), "w": json.dumps(mult), "s": split, "sc": float(score), "a": accepted,
                 "st": R.SETTING, "d": extra.get("delta", 0.0), "lo": extra.get("lo", 0.0)}, R.TENANT)


def main():
    R.K = 20
    gold = [json.loads(l) for l in open(R.ROOT / "eval" / "gold.jsonl") if l.strip()]
    odd = [q for q in gold if int(q["id"][1:]) % 2 == 1]
    even = [q for q in gold if int(q["id"][1:]) % 2 == 0]
    from neo_cortex.store import Store
    t0 = time.time()
    with Store() as store:
        tag = f"tune-{R.SETTING}-{int(t0)}"
        combos = [{"vector": 1.0, "bm25": b, "graph": g, "temporal": t} for b, g, t in itertools.product(*GRID.values())]
        assert DEFAULT in combos and len(combos) <= 60
        trials = []
        for i, m in enumerate(combos):
            sc, ms = run(store, m, odd)
            trials.append((R.mean(sc), m))
            ledger(store, f"{tag}-odd-{i}", m, "odd", R.mean(sc), False)
            print(f"odd {i + 1}/{len(combos)} {m} score {R.mean(sc):.4f} {ms:.0f} ms/q", flush=True)
        dflt_odd = next(s for s, m in trials if m == DEFAULT)
        # ties go to the combo nearest the defaults
        best_score, best = max(trials, key=lambda x: (round(x[0], 6), -sum(abs(math.log(v)) for v in x[1].values())))
        print(f"best odd {best_score:.4f} {best} vs default {dflt_odd:.4f}", flush=True)
        run(store, DEFAULT, even)  # warm-up: models and caches
        d_sc, c_sc, d_ms, c_ms = None, None, [], []
        for _ in range(2):  # uncached parse_query so latency includes GLiNER, like the product
            d_sc, d = run(store, DEFAULT, even, cache=False)
            c_sc, c = run(store, best, even, cache=False)
            d_ms.append(d)
            c_ms.append(c)
        d_sc, _ = run(store, DEFAULT, even)
        c_sc, _ = run(store, best, even)
        boot = M.paired_bootstrap(c_sc, d_sc)
        lat_d, lat_c = min(d_ms), min(c_ms)
        accepted = best != DEFAULT and boot["lo"] > 0 and lat_c <= 1.2 * lat_d
        ledger(store, f"{tag}-even-default", DEFAULT, "even", R.mean(d_sc), False)
        ledger(store, f"{tag}-even-best", best, "even", R.mean(c_sc), accepted, delta=boot["delta"], lo=boot["lo"])
        out = {"setting": R.SETTING, "n_odd": len(odd), "n_even": len(even), "combos": len(combos), "best": best, "odd_score": best_score,
               "odd_default": dflt_odd, "even_score": R.mean(c_sc), "even_default": R.mean(d_sc), "even_delta": boot["delta"],
               "ci": [boot["lo"], boot["hi"]], "latency_ms": {"default": lat_d, "best": lat_c}, "accepted": accepted,
               "seconds": round(time.time() - t0, 1), "trials": [{"weights": m, "odd_score": s} for s, m in trials]}
        (R.ROOT / "eval" / f"tune_{R.SETTING}.json").write_text(json.dumps(out, indent=1))
        print(json.dumps({"accepted": accepted, "multipliers": best,
                          "BASE": {c: BASE[c] * best[c] for c in BASE}} if accepted else {"accepted": False, "multipliers": best}, indent=1))
        print(f"odd {best_score:.4f} (default {dflt_odd:.4f}); even delta {boot['delta']:+.4f} CI [{boot['lo']:+.4f}, {boot['hi']:+.4f}]; "
              f"latency {lat_c:.0f} vs {lat_d:.0f} ms; accepted={accepted}; {out['seconds']} s")


if __name__ == "__main__":
    main()
