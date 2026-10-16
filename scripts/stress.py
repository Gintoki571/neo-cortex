"""Concurrency stress test for a running `neo serve` daemon (stdlib only; starts nothing).

Per concurrency level, N clients run for --seconds: 70% reads (recall, who, impact), 30% writes (remember).
Each level tags its writes with its own run id, then counts them in the graph (read-only Cypher).
Lost writes = acknowledged `created` writes not found in the graph; it must be 0. Exit 1 on lost writes or errors.

    python3 scripts/stress.py --url http://127.0.0.1:8791 --clients 1,4,8,16 --seconds 20
"""
import argparse
import json
import math
import random
import secrets
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

RECALL = [
    "who owns api-gateway", "what does auth-service depend on", "session-cache eviction and TTL",
    "payment retries and idempotency keys", "ledger postings and balances", "config-service feature switches",
    "rate limits per tenant at the edge", "notification-service outage incident", "reporting-service data freshness",
    "why was the dashboard migration delayed",
]
WHO = ["api-gateway", "auth-service", "config-service", "ledger-service", "payment-gateway", "session-cache"]
IMPACT = ["auth-service", "config-service", "session-cache", "api-gateway", "ledger-service"]
WRITE_SHARE = 0.3


def post(url, tool, args, timeout):
    # urllib sends Host: 127.0.0.1:<port>, which passes the daemon's loopback guard
    req = urllib.request.Request(f"{url}/api/{tool}", json.dumps(args).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode()


def client(url, cid, run, deadline, timeout):
    rng, recs, seq = random.Random(f"{run}-{cid}"), [], 0
    while time.monotonic() < deadline:
        if rng.random() < WRITE_SHARE:
            seq += 1
            kind = "write"
            tool = "remember"
            args = {"text": f"[nc-stress-{run}] client {cid} write {seq}: checkout-service release {seq * 31 + cid} "
                            f"reached staging and the owner review was logged", "agent": f"stress-{cid}"}
        else:
            kind = "read"
            tool = rng.choice(["recall", "who", "impact"])
            args = {"recall": {"query": rng.choice(RECALL), "k": 8}, "who": {"topic": rng.choice(WHO)},
                    "impact": {"entity": rng.choice(IMPACT)}}[tool]
        t0 = time.perf_counter()
        try:
            body = post(url, tool, args, timeout)
            ok, outcome, detail = True, ("deduped" if kind == "write" and body.startswith("reinforced") else "ok"), ""
        except urllib.error.HTTPError as e:
            ok, outcome, detail = False, "error", f"HTTP {e.code}: {e.read()[:160]!r}"
        except Exception as e:  # timeouts, refused connections, resets
            ok, outcome, detail = False, "error", f"{type(e).__name__}: {e}"[:160]
        recs.append((kind, ok, outcome, time.perf_counter() - t0, detail))
    return recs


def pct(xs, p):
    if not xs:
        return None
    s = sorted(xs)
    return s[max(0, math.ceil(p / 100 * len(s)) - 1)]  # nearest-rank


def ms(x):
    return "-" if x is None else f"{x * 1000:.0f}"


def count_written(url, run, timeout):
    q = f"MATCH (m:Memory) WHERE m.text CONTAINS '[nc-stress-{run}]' RETURN count(m)"
    return int(post(url, "cypher", {"query": q}, timeout).strip().splitlines()[-1])  # raises on a rejected query


def run_level(url, clients, seconds, timeout, base):
    run = f"{base}-c{clients}"
    deadline = time.monotonic() + seconds
    t0 = time.monotonic()
    with ThreadPoolExecutor(max_workers=clients) as ex:
        recs = [r for f in [ex.submit(client, url, cid, run, deadline, timeout) for cid in range(clients)] for r in f.result()]
    elapsed = time.monotonic() - t0
    reads = [r for r in recs if r[0] == "read"]
    writes = [r for r in recs if r[0] == "write"]
    ok_reads = [r[3] for r in reads if r[1]]
    ok_writes = [r[3] for r in writes if r[1]]
    errors = [r for r in recs if not r[1]]
    created = sum(1 for r in writes if r[2] == "ok")
    deduped = sum(1 for r in writes if r[2] == "deduped")
    try:
        found = count_written(url, run, timeout)
        cerr = ""
    except Exception as e:  # daemon down or query rejected: report, don't lose the table
        found, cerr = None, f"count failed: {type(e).__name__}: {e}"[:160]
    row = dict(clients=clients, ops_s=(len(ok_reads) + len(ok_writes)) / elapsed, elapsed=elapsed,
               reads=len(ok_reads), r50=pct(ok_reads, 50), r95=pct(ok_reads, 95), r99=pct(ok_reads, 99),
               writes=len(ok_writes), w50=pct(ok_writes, 50), w95=pct(ok_writes, 95), w99=pct(ok_writes, 99),
               errors=len(errors), deduped=deduped, created=created, found=found,
               lost=max(0, created - found) if found is not None else None, cerr=cerr,
               extra=max(0, found - created) if found is not None else 0,
               sample_errors=sorted({r[4] for r in errors})[:3])
    return row


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default="http://127.0.0.1:8791")
    ap.add_argument("--clients", default="1,4,8,16", help="comma-separated concurrency levels")
    ap.add_argument("--seconds", type=float, default=20.0, help="duration per level")
    ap.add_argument("--timeout", type=float, default=60.0, help="per-request timeout (s)")
    ap.add_argument("--run", default=None, help="run id prefix (default random)")
    a = ap.parse_args(argv)
    url = a.url.rstrip("/")
    try:
        health = json.loads(post_get(url + "/health", a.timeout))
    except Exception as e:
        print(f"daemon not reachable at {url}: {e}", file=sys.stderr)
        return 2
    print(f"daemon ok at {url}: {health}")
    base = a.run or secrets.token_hex(3)
    rows = []
    for n in [int(x) for x in a.clients.split(",") if x.strip()]:
        rows.append(run_level(url, n, a.seconds, a.timeout, base))
        print(f"level {n} done", file=sys.stderr, flush=True)
    print("| clients | ops/s | reads | read p50 ms | read p95 ms | read p99 ms | writes | write p50 ms | write p95 ms | write p99 ms "
          "| errors | deduped | created (acked) | found in graph | lost writes |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        print(f"| {r['clients']} | {r['ops_s']:.1f} | {r['reads']} | {ms(r['r50'])} | {ms(r['r95'])} | {ms(r['r99'])} "
              f"| {r['writes']} | {ms(r['w50'])} | {ms(r['w95'])} | {ms(r['w99'])} | {r['errors']} | {r['deduped']} "
              f"| {r['created']} | {r['found'] if r['found'] is not None else '-'} | {r['lost'] if r['lost'] is not None else '-'} |")
    for r in rows:
        if r["sample_errors"]:
            print(f"clients {r['clients']} sample errors: {r['sample_errors']}")
        if r["cerr"]:
            print(f"clients {r['clients']}: {r['cerr']}")
        if r["extra"]:
            print(f"clients {r['clients']}: {r['extra']} stored writes had no acknowledged response (timeouts that still wrote)")
    bad = any(r["lost"] or r["errors"] or r["cerr"] for r in rows)
    return 1 if bad else 0


def post_get(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode()


if __name__ == "__main__":
    sys.exit(main())
