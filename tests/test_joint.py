"""NEO_EXTRACT dispatch, JointResult -> batch_extract_long shape mapping, and the fp16 load flag. Fakes only (no model)."""
import sys
import types
from types import SimpleNamespace

import pytest

from neo_cortex import extract, joint, models
from neo_cortex.extract import REL_LABELS, REL_TYPES


def _fake_result(feasible=True):
    """A JointResult-like object: one OWNS relation between a person and a service, as JointIE would return it."""
    ents = [SimpleNamespace(id="e0", type="person", text="Noor Haddad", start=0, end=11, confidence=0.99),
            SimpleNamespace(id="e1", type="service", text="session-cache", start=17, end=30, confidence=0.98)]
    rels = [SimpleNamespace(type="owns", head="e0", tail="e1", confidence=0.95)]
    return SimpleNamespace(entities=ents, relations=rels, feasible=feasible)


def test_mode_defaults_to_split_and_rejects_unknown(monkeypatch):
    monkeypatch.delenv("NEO_EXTRACT", raising=False)
    assert joint.mode() == "split"
    for m in ("combined", "joint"):
        monkeypatch.setenv("NEO_EXTRACT", m)
        assert joint.mode() == m
    monkeypatch.setenv("NEO_EXTRACT", "both")
    with pytest.raises(ValueError):
        joint.mode()


def test_dispatch_picks_mode_without_touching_split_model(monkeypatch):
    """With a non-split mode extract_batch never builds the split path's GLiNER handle."""
    def no_split_model():
        raise AssertionError("split path ran")
    monkeypatch.setattr(models, "gliner", no_split_model)
    calls = []

    def fake_joint(flat):
        calls.append(("joint", list(flat)))
        return [joint._raw(_fake_result()) for _ in flat]

    def fake_combined(flat):
        calls.append(("combined", list(flat)))
        return [joint._raw(_fake_result()) for _ in flat]

    monkeypatch.setattr(joint, "_joint", fake_joint)
    monkeypatch.setattr(joint, "_combined", fake_combined)
    text = "Noor Haddad owns session-cache."
    for m in ("combined", "joint"):
        monkeypatch.setenv("NEO_EXTRACT", m)
        out = extract.extract_batch([text])
        assert calls[-1][0] == m
        assert calls[-1][1] == [text]  # the sentence window, one per sentence


def test_joint_result_maps_to_the_extract_batch_shape(monkeypatch):
    monkeypatch.setenv("NEO_EXTRACT", "joint")
    monkeypatch.setattr(joint, "_joint", lambda flat: [joint._raw(_fake_result()) for _ in flat])
    (out,) = extract.extract_batch(["Noor Haddad owns session-cache."])
    assert set(out) == {"entities", "relations"}
    ents = {e["name"]: e for e in out["entities"]}
    assert ents["Noor Haddad"]["type"] == "person" and ents["session-cache"]["type"] == "service"
    assert all(set(e) == {"name", "type", "conf"} for e in out["entities"])
    (rel,) = out["relations"]
    assert (rel["head"], rel["type"], rel["tail"]) == ("Noor Haddad", "OWNS", "session-cache")
    assert {"head", "type", "tail", "conf"} <= set(rel)


def test_raw_drops_relations_with_unknown_endpoints():
    res = _fake_result()
    res.relations.append(SimpleNamespace(type="owns", head="e0", tail="missing", confidence=0.9))
    raw = joint._raw(res)
    assert list(raw["relation_extraction"]) == ["owns"]
    assert len(raw["relation_extraction"]["owns"]) == 1


def test_joint_schema_endpoints_are_rel_types_as_labels():
    """Every relation's endpoint labels are exactly the GLiNER labels whose contract type rel_ok allows."""
    js = joint._joint_schema()
    label_of = {ct: lbl for lbl, (ct, _) in extract.ENTITY_LABELS.items()}
    specs = {s.name: s for s in js.relation_specs}
    assert set(specs) == set(REL_LABELS)
    for lbl, (rt, _) in REL_LABELS.items():
        heads, tails = REL_TYPES[rt]
        assert set(specs[lbl].head) == {label_of[t] for t in heads if t in label_of}
        assert set(specs[lbl].tail) == {label_of[t] for t in tails if t in label_of}


def test_fp16_flag_follows_device_and_env(monkeypatch):
    """quantize (GLiNER fp16) is opt-in on cuda (NEO_GLINER_FP16=1); the CPU build (OOM fallback) is always fp32."""
    seen = []
    fake = types.ModuleType("gliner2")
    fake.AutoExtractor = SimpleNamespace(from_pretrained=lambda path, **kw: seen.append(kw) or object())
    monkeypatch.setitem(sys.modules, "gliner2", fake)
    monkeypatch.setattr(models, "_cache", {})
    monkeypatch.setattr(models, "_cpu", set())
    for env, device, want in [(None, "cuda", False), ("1", "cuda", True), ("0", "cuda", False), (None, "cpu", False), ("1", "cpu", False)]:
        monkeypatch.setattr(models, "_cache", {})
        monkeypatch.setenv("NEO_DEVICE", device)
        if env is None:
            monkeypatch.delenv("NEO_GLINER_FP16", raising=False)
        else:
            monkeypatch.setenv("NEO_GLINER_FP16", env)
        models.gliner()
        assert seen[-1]["quantize"] is want, (env, device)
        assert seen[-1]["map_location"] == device
