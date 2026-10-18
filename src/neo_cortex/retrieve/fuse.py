"""Weighted reciprocal rank fusion and intent-conditioned channel weights."""
import math

DAY_MS = 86400000
BASE = {"vector": 1.0, "bm25": 1.0, "graph": 1.0, "temporal": 0.5}
# weight_c = BASE_c * (1 + sum_i conf_i * BOOST[i][c]); intent confidences are soft, so a misroute only nudges
BOOST = {
    "fact": {"bm25": 0.5, "vector": 0.25, "graph": -0.3},  # single-hop facts: text channels already find them, keep graph noise down
    "connection": {"graph": 1.0},
    "temporal": {"temporal": 2.0},
    "owner": {"graph": 1.0},
    "howto": {"vector": 0.5, "bm25": 0.25},
}


# intent -> (node kinds it prefers, boost): a node of such a kind scores x (1 + conf x boost). Memory.kind "decision",
# Chunk.kind "adr" (a decision-record document). Soft like BOOST, so a misrouted intent only nudges the order.
KIND_ROUTE = {"decision": ({"decision", "adr"}, 1.0)}


def kind_factor(intent: dict, kind) -> float:
    return 1 + sum(conf * KIND_ROUTE[i][1] for i, conf in intent.items() if i in KIND_ROUTE and kind in KIND_ROUTE[i][0])


def channel_weights(intent: dict) -> dict:
    return {c: w * (1 + sum(conf * BOOST.get(i, {}).get(c, 0) for i, conf in intent.items())) for c, w in BASE.items()}


def rrf(lists: dict, weights: dict | None = None, k: int = 60, norm: bool = False) -> list:
    """lists {channel: [(id, score)] best first}; returns [(id, score, {channel: rank})] sorted by fused score.
    score = sum_c w_c / (k + rank_c), ranks 1-based. norm (agentmemory hybrid-search.ts:196): divide each weighted
    sum by the best attainable weighted score over the channels that actually returned results (a silent channel
    costs nothing), then multiply by 1 + 0.05 x (number of channels that found the item - 1) (agreement bonus)."""
    sc, ranks = {}, {}
    for c, lst in lists.items():
        w = (weights or {}).get(c, 1.0)
        for r, (i, _) in enumerate(lst, 1):
            sc[i] = sc.get(i, 0.0) + w / (k + r)
            ranks.setdefault(i, {})[c] = r
    out = [(i, s, ranks[i]) for i, s in sc.items()]
    if norm:
        active = sum((weights or {}).get(c, 1.0) for c, lst in lists.items() if lst)
        if active > 0:
            best = active / (k + 1)
            out = [(i, s / best * (1 + 0.05 * (len(r) - 1)), r) for i, s, r in out]
    return sorted(out, key=lambda x: -x[1])


def recency(date_ms, now_ms) -> float:
    """365-day linear decay from the item's date into [0, 1]; 0.5 when there is no date."""
    if not date_ms:
        return 0.5
    return max(0.0, 1.0 - max(0.0, now_ms - date_ms) / (365 * DAY_MS))


def proximity(date_ms, since_ms, until_ms, now_ms) -> float | None:
    """1 - |days from the window's mid| / (window/2), clamped to [0, 1]; None when the query has no window.
    A one-sided window is closed with now (since given) or a 365-day lookback (until given)."""
    if since_ms is None and until_ms is None:
        return None
    if not date_ms:
        return 0.5
    s = since_ms if since_ms is not None else (until_ms - 365 * DAY_MS if until_ms is not None else 0)
    u = until_ms if until_ms is not None else now_ms
    half = (u - s) / 2
    if half <= 0:
        return 1.0
    return min(1.0, max(0.0, 1.0 - abs(date_ms - (s + u) / 2) / half))


def proof_norm(count) -> float:
    """0.5 + ln(count)/10 clamped to [0, 1]; 0.5 (neutral) for a zero or missing count."""
    if not count or count <= 0:
        return 0.5
    return min(1.0, max(0.0, 0.5 + math.log(count) / 10))


def boost_factor(date_ms, now_ms, since_ms=None, until_ms=None, count=0) -> float:
    """Bounded multiplicative secondary boosts after fusion (hindsight apply_combined_scoring):
    recency and (when the query has a time window) temporal proximity at 1 + 0.2 x (x - 0.5),
    evidence count at 1 + 0.1 x (proof - 0.5). Every factor is neutral at 0.5, so the product stays in [~0.85, ~1.28]."""
    f = 1 + 0.2 * (recency(date_ms, now_ms) - 0.5)
    p = proximity(date_ms, since_ms, until_ms, now_ms)
    if p is not None:
        f *= 1 + 0.2 * (p - 0.5)
    return f * (1 + 0.1 * (proof_norm(count) - 0.5))
