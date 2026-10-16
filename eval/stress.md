# Concurrency stress test

`scripts/stress.py` (stdlib only) hammers a running `neo serve` daemon: per concurrency level, N clients run for 20 s with a 70/30 read/write mix (reads: `recall` with varied queries, `who`, `impact`; writes: `remember` with a unique text per op, tagged with a per-level run id). Afterwards it counts the written Memory nodes in the graph via a read-only `cypher` query; lost writes = acknowledged writes not found in the graph, must be 0.

## Repro

```
cd /home/bindesh/neo-cortex
NEO_HOME=/tmp/claude-1000/stress-home NEO_PORT=6354 uv run --no-sync neo serve --port 8791 &   # background
# wait until: curl -s http://127.0.0.1:8791/health  -> 200 {"ok":true,...}
NEO_DAEMON_URL=http://127.0.0.1:8791 uv run --no-sync neo ingest --wait data/synthetic/doc
python3 scripts/stress.py --url http://127.0.0.1:8791 --clients 1,4,8,16 --seconds 20
kill <daemon pid>   # then check: ss -ltn | grep :6354  (no redis-server left; kill if there is)
```

2026-10-17 run: `/tmp/claude-1000/stress-home` already contained the 16 synthetic docs (ingest reported `documents 0, skipped 16`); daemon and embedded DB started fresh. GPU device (GTX 1660 Ti). First-request latency includes GLiNER/EmbeddingGemma model load.

## Results

| clients | ops/s | reads | read p50 ms | read p95 ms | read p99 ms | writes | write p50 ms | write p95 ms | write p99 ms | errors | deduped | created (acked) | found in graph | lost writes |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.1 | 11 | 8 | 452 | 452 | 12 | 389 | 14909 | 14909 | 0 | 0 | 12 | 12 | 0 |
| 4 | 8.1 | 114 | 10 | 915 | 1057 | 54 | 996 | 1470 | 1511 | 0 | 0 | 54 | 54 | 0 |
| 8 | 8.2 | 114 | 11 | 1938 | 2079 | 58 | 1819 | 2688 | 2802 | 0 | 0 | 58 | 58 | 0 |
| 16 | 13.1 | 216 | 11 | 3280 | 3589 | 68 | 2011 | 3667 | 5232 | 0 | 0 | 68 | 68 | 0 |

- All 4 levels: 0 errors, 0 lost writes. Every acknowledged `created` write was found in the graph afterwards; nothing was written without an acknowledgement.
- The daemon shut down cleanly on SIGTERM; no `redis-server` was left listening on 127.0.0.1:6354.
- No concurrency bug observed: no errors, no lost writes, no deadlock at 16 concurrent clients.

## Reading the numbers

- Write latency dominates (`remember` runs GLiNER extraction + classification + one embedding per text on the GPU): ~0.4-2 s at p50, growing with concurrency. Read p50 stays flat (~8-11 ms) while read p95/p99 grow roughly linearly with clients — reads queue behind the GPU-bound writes on the daemon's single Store.
- The `clients=1` write p95/p99 (14.9 s) is the first write of the run paying model load (warm-up), not steady-state cost; subsequent writes at that level are ~0.4-1.5 s.
- Throughput is write-bound: ops/s rises with clients (1.1 → 13.1) because writes pipeline on the GPU, but total write count per 20 s level stays roughly flat (~12-68 with the mix sending ~30% of ops to writes).
