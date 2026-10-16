"""Pure metric functions for the retrieval eval (no DB). Shared with the later weight tuner."""
import random
import re


def norm(s: str) -> str:
    """Lowercase, punctuation to spaces, collapsed whitespace; so '200-5000 ms' and '200 5000 ms' compare equal."""
    return " ".join(re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).split())


def unique_docs(items) -> list[str]:
    """Doc ids of retrieved items in rank order, first occurrence only (Memories without a doc are skipped)."""
    out = []
    for it in items:
        d = (it.get("source") or {}).get("doc_id")
        if d and d not in out:
            out.append(d)
    return out


def hit(ranked, gold, k):
    return float(bool(set(ranked[:k]) & set(gold)))


def recall_at(ranked, gold, k):
    return len(set(ranked[:k]) & set(gold)) / len(gold)


def full_cover(ranked, gold, k):
    return float(set(gold) <= set(ranked[:k]))


def mrr(ranked, gold, k):
    for i, d in enumerate(ranked[:k], 1):
        if d in gold:
            return 1 / i
    return 0.0


def answer_in(text: str, answer: str) -> float:
    """Normalised gold answer appears as a whole-word substring of text."""
    a = norm(answer)
    return float(bool(a) and f" {a} " in f" {norm(text)} ")


def hit_answer(text: str, q: dict) -> float:
    """Containment used for `ask` and its vector baseline: every short `keys` string present when the question has them
    (the verbose `answer` of multi-part questions rarely matches verbatim), else the whole normalised `answer`."""
    ks = q.get("keys")
    return float(all(f" {norm(k)} " in f" {norm(text)} " for k in ks)) if ks else answer_in(text, q["answer"])


def question_metrics(ranked, gold, texts_by_doc, answer, ks=(5, 10)) -> dict:
    """Metrics per k for one question. texts_by_doc: doc id -> concatenated retrieved chunk text."""
    m = {}
    for k in ks:
        m[f"hit@{k}"] = hit(ranked, gold, k)
        m[f"recall@{k}"] = recall_at(ranked, gold, k)
        m[f"fullcover@{k}"] = full_cover(ranked, gold, k)
        m[f"mrr@{k}"] = mrr(ranked, gold, k)
        m[f"answerin@{k}"] = answer_in(" ".join(texts_by_doc.get(d, "") for d in ranked[:k]), answer)
    return m


def aggregate(rows: list[dict]) -> dict:
    """Mean of every metric over per-question dicts."""
    return {k: sum(r[k] for r in rows) / len(rows) for k in rows[0]} if rows else {}


def people(answer: str) -> list[str]:
    """Names in a gold ownership answer, e.g. 'Viktor Sokolov, with Noor Haddad'."""
    return [p.strip() for p in re.split(r",\s*(?:with\s+)?|\s+(?:and|with)\s+", answer) if p.strip()]


def paired_bootstrap(a, b, n=1000, seed=0, level=0.95) -> dict:
    """Paired bootstrap over questions of mean(a - b). a, b: per-question scores in the same order.
    Returns mean delta, CI bounds, and 'significant' (CI excludes 0). The tuner reuses this as its noise band."""
    assert len(a) == len(b) and a, "paired non-empty score lists required"
    d = [x - y for x, y in zip(a, b)]
    rng = random.Random(seed)
    means = sorted(sum(d[rng.randrange(len(d))] for _ in d) / len(d) for _ in range(n))
    lo, hi = means[int((1 - level) / 2 * n)], means[min(n - 1, int((1 + level) / 2 * n))]
    return {"delta": sum(d) / len(d), "lo": lo, "hi": hi, "n": len(d), "significant": lo > 0 or hi < 0}
