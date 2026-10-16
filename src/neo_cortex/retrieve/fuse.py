"""Weighted reciprocal rank fusion and intent-conditioned channel weights."""
BASE = {"vector": 1.0, "bm25": 1.0, "graph": 1.0, "temporal": 0.5}
# weight_c = BASE_c * (1 + sum_i conf_i * BOOST[i][c]); intent confidences are soft, so a misroute only nudges
BOOST = {
    "fact": {"bm25": 0.5, "vector": 0.25},
    "connection": {"graph": 1.0},
    "temporal": {"temporal": 2.0},
    "owner": {"graph": 1.0},
    "howto": {"vector": 0.5, "bm25": 0.25},
}


def channel_weights(intent: dict) -> dict:
    return {c: w * (1 + sum(conf * BOOST.get(i, {}).get(c, 0) for i, conf in intent.items())) for c, w in BASE.items()}


def rrf(lists: dict, weights: dict | None = None, k: int = 60) -> list:
    """lists {channel: [(id, score)] best first}; returns [(id, score, {channel: rank})] sorted by fused score.
    score = sum_c w_c / (k + rank_c), ranks 1-based."""
    sc, ranks = {}, {}
    for c, lst in lists.items():
        w = (weights or {}).get(c, 1.0)
        for r, (i, _) in enumerate(lst, 1):
            sc[i] = sc.get(i, 0.0) + w / (k + r)
            ranks.setdefault(i, {})[c] = r
    return sorted(((i, s, ranks[i]) for i, s in sc.items()), key=lambda x: -x[1])
