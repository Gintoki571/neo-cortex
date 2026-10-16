import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
import metrics as M  # noqa: E402


def item(d):
    return {"source": {"doc_id": d}}


def test_unique_docs_order_and_memories():
    assert M.unique_docs([item("a"), item("b"), item("a"), {"source": {"source_id": "x"}}, item("c")]) == ["a", "b", "c"]


def test_rank_metrics():
    r, g = ["x", "a", "y", "b"], ["a", "b"]
    assert M.hit(r, g, 1) == 0 and M.hit(r, g, 2) == 1
    assert M.recall_at(r, g, 2) == 0.5 and M.recall_at(r, g, 4) == 1
    assert M.full_cover(r, g, 3) == 0 and M.full_cover(r, g, 4) == 1
    assert M.mrr(r, g, 10) == 0.5 and M.mrr(["x"], g, 5) == 0


def test_answer_in_normalisation_and_word_boundary():
    assert M.answer_in("TTL is 300 seconds.", "300 seconds") == 1
    assert M.answer_in("range 200-5000 ms", "200 to 5000 ms") == 0
    assert M.answer_in("range 200 - 5000 ms", "200 5000 ms") == 1
    assert M.answer_in("value 1300", "300") == 0
    assert M.answer_in("anything", "") == 0


def test_question_metrics_and_aggregate():
    m = M.question_metrics(["a", "b"], ["b"], {"a": "foo", "b": "bar baz"}, "baz", ks=(1, 2))
    assert (m["hit@1"], m["hit@2"], m["answerin@1"], m["answerin@2"], m["mrr@2"]) == (0, 1, 0, 1, 0.5)
    assert M.aggregate([{"x": 1.0}, {"x": 0.0}]) == {"x": 0.5} and M.aggregate([]) == {}


def test_people_split():
    assert M.people("Viktor Sokolov, with Noor Haddad") == ["Viktor Sokolov", "Noor Haddad"]
    assert M.people("Mateo Alvarez") == ["Mateo Alvarez"]


def test_bootstrap_deterministic_and_sign():
    a, b = [1.0] * 30, [0.0] * 30
    r = M.paired_bootstrap(a, b)
    assert r["delta"] == 1 and r["lo"] == 1 and r["significant"]
    assert M.paired_bootstrap(a, b, seed=3) == M.paired_bootstrap(a, b, seed=3)
    z = M.paired_bootstrap([1, 0] * 20, [0, 1] * 20)
    assert not z["significant"] and z["lo"] < 0 < z["hi"]
