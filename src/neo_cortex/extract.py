"""GLiNER2.5 extraction and classification with descriptive labels (short labels misroute, see the spike note).

`extract` returns entities typed per the data-model contract and relations from its whitelist. Nothing here calls an LLM.
"""
import re

import torch

from .models import gliner
from .util import normalize_key

# GLiNER label -> (contract type, description). The description is what steers the model.
ENTITY_LABELS = {
    "person": ("person", "the full name of a human being, such as Noor Haddad or Mateo Alvarez"),
    "team": ("team", "a named team or department of the company, such as Identity, Platform, Payments, Data or Experience"),
    "service": ("service", "a deployed software service of the platform, written lowercase and hyphenated, such as auth-service, api-gateway or session-cache"),
    "component": ("component", "a technical part inside a service: a library, module, feature, queue, database, cache policy or endpoint"),
    "file": ("file", "a file name or file path, such as config/ci.yaml or auth/login_test.py"),
    "config setting": ("config_setting", "a configuration setting, limit or parameter name such as SESSION_TTL or maxmemory"),
    "ticket": ("ticket", "an issue or ticket key such as IDN-212, CFG-4411 or #3209"),
    "customer": ("customer", "a named customer company or organisation that buys and uses the product"),
    "product": ("product", "a named product or product feature of a company"),
    "tool": ("tool", "a named command-line tool or software tool, such as cfgctl, Redis, Terraform or pytest"),
    "incident": ("incident", "a named production incident or outage, such as INC-01"),
    "decision": ("decision", "a recorded decision or architecture decision record, such as ADR-006"),
}

# GLiNER relation label -> (contract type, description)
REL_LABELS = {
    "owns": ("OWNS", "a person or team owns, maintains or is responsible for a service or component"),
    "member of": ("MEMBER_OF", "a person belongs to or is on a team"),
    "depends on": ("DEPENDS_ON", "a service calls, reads from or needs another service"),
    "caused by": ("CAUSED_BY", "an incident or bug was caused by a component, change or setting"),
    "fixed by": ("FIXED_BY", "an incident or bug was fixed by a person, change or ticket"),
    "approved": ("APPROVED", "a person approved a decision, change or ticket"),
    "decided": ("DECIDED", "a person or team made a decision"),
    "part of": ("PART_OF", "a component or service is part of a larger service or system"),
    "works on": ("WORKS_ON", "a person works on a ticket, service or feature"),
    "reported": ("REPORTED", "a person reported an incident, bug or ticket"),
    "replaced by": ("REPLACED_BY", "something was replaced by something else"),
    "renamed to": ("RENAMED_TO", "something was renamed to a new name"),
}  # RELATED_TO is in the whitelist but never extracted: it is a noise magnet.

MEMORY_KINDS = {
    "something that happened in a session (an episode, an event, a fix that was made)": "episodic",
    "a general fact about the system or the world": "semantic",
    "step-by-step procedure or lesson on how to do a task": "procedural",
    "a user preference about how they like to work": "preference",
    "a decision that was made, with a reason": "decision",
}

_KEEP = ["a durable fact about the system", "a lesson or rule to follow in future", "a decision with a reason",
         "a user preference"]
_DROP = ["a question or request", "narration of an action in progress", "greeting or acknowledgement"]

# per-type entity confidence: names of people and services are crisp, the fuzzy types need more evidence
ENTITY_CONF = {"person": 0.6, "team": 0.8, "service": 0.7, "component": 0.85, "file": 0.7, "config_setting": 0.8,
               "ticket": 0.7, "customer": 0.8, "product": 0.85, "tool": 0.8, "incident": 0.8, "decision": 0.85}
REL_CONF = {"OWNS": 0.6, "MEMBER_OF": 0.6, "DEPENDS_ON": 0.6, "CAUSED_BY": 0.6, "FIXED_BY": 0.6, "APPROVED": 0.6,
            "DECIDED": 0.6, "PART_OF": 0.7, "WORKS_ON": 0.7, "REPORTED": 0.6, "REPLACED_BY": 0.6, "RENAMED_TO": 0.6}
MAX_WORDS = 384  # GLiNER chunk size in words (inference.extract_long default); longer texts are split with overlap

_THING = {"service", "component", "file", "config_setting", "ticket", "product", "tool", "incident", "decision", "other"}
_WHO = {"person", "team"}
# relation type -> (allowed head types, allowed tail types): cheap type constraints remove most wrong pairs
REL_TYPES = {
    "OWNS": (_WHO, {"service", "component", "file", "product", "tool", "other"}),
    "MEMBER_OF": ({"person"}, {"team"}),
    "DEPENDS_ON": ({"service", "component", "tool"}, {"service", "component", "tool"}),
    "CAUSED_BY": (_THING, _THING | _WHO),
    "FIXED_BY": (_THING, _THING | _WHO),
    "APPROVED": (_WHO, {"decision", "ticket", "component", "service", "other"}),
    "DECIDED": (_WHO, {"decision", "other"}),
    "PART_OF": (_THING, _THING | {"team"}),
    "WORKS_ON": ({"person"}, {"ticket", "service", "component", "product", "incident"}),
    "REPORTED": ({"person"}, {"incident", "ticket", "other"}),
    "REPLACED_BY": (_THING, _THING),
    "RENAMED_TO": (_THING, _THING),
}

_JUNK = set("""i me my we us our you your he she him her his they them their it its this that these those who which
what one someone anyone everyone user users team teams service services system systems component components file files
ticket tickets customer customers product tool tools incident decision config setting settings cache api code issue
bug fix change changes feature release project company engineer engineers people person limits switches device storage
side image adr readme history laptop rollback retries reviewers commanders prod staging cli dashboards alerts keys
validator dependency interface identifier override eviction memory cutoff batches freeze totals checkout""".split())
# deterministic ids: precise, so they override GLiNER's type
_IDS = [(re.compile(r"\bADR-\d+\b"), "decision"), (re.compile(r"\bINC-\d+\b"), "incident"),
        (re.compile(r"\b(?!ADR|INC)[A-Z]{2,5}-\d{1,5}\b"), "ticket")]


_VERSION = re.compile(r"\s+v?\d+(\.\d+)+$")
_ROLE_TAIL = re.compile(r"\s+(team|teams)$", re.I)
# fuzzy types need a proper-noun shape (capital letter, or a - _ . / digit inside); plain lowercase words are noise
_STRICT = {"component", "config_setting", "other", "product", "team", "customer", "decision", "incident"}


def _clean(name: str) -> str:
    name = re.split(r"\s\(", name)[0]  # "Maggie Ellison (CEO" -> name only
    name = re.sub(r"^(the|a|an)\s+", "", name.strip(" \t\n\"'`*_.,;:()[]"), flags=re.I)
    name = re.sub(r"'s$", "", name)
    return re.sub(r"\s+", " ", _VERSION.sub("", name))


def _proper(name: str) -> bool:
    return any(c.isupper() or c in "-_./" or c.isdigit() for c in name)


def _junk(name: str, etype: str = "other") -> bool:
    k = normalize_key(name)
    return (len(k) < 2 or k in _JUNK or k.isdigit() or len(k.split()) > 4
            or (etype in _STRICT and not _proper(name)))


def _schema(m):
    return (m.create_schema()
            .entities({k: d for k, (_, d) in ENTITY_LABELS.items()})
            .relations({k: d for k, (_, d) in REL_LABELS.items()}))


_NAME = re.compile(r"[A-Z][\w'.-]+(?: [A-Z][\w'.-]+)+")


def _table_owners(text: str) -> list[tuple[str, str, str]]:
    """Markdown tables with an Owner column are structured ownership facts: (owner, thing, thing_type)."""
    out, hdr = [], None
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            hdr = None
            continue
        cells = [c.strip(" `*") for c in line.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        if hdr is None:
            hdr = [c.lower() for c in cells]
            continue
        oi = next((i for i, c in enumerate(hdr) if "owner" in c), None)
        if oi is None or oi >= len(cells) or not cells[0]:
            continue
        who = _NAME.search(cells[oi])
        if who:
            kind = "service" if re.fullmatch(r"[a-z][a-z0-9]*(-[a-z0-9]+)+", cells[0]) else "other"
            out.append((who.group(), cells[0], kind))
    return out


def _shape(raw: dict, text: str = "") -> dict:
    ents: dict[str, dict] = {}
    for pat, etype in _IDS:
        for mt in pat.findall(text):
            ents[normalize_key(mt)] = {"name": mt, "type": etype, "conf": 0.95}
    for label, items in raw.get("entities", {}).items():
        etype = ENTITY_LABELS[label][0]
        for it in items:
            name, conf = _clean(it["text"]), it["confidence"]
            k = normalize_key(name)
            if etype == "team":
                name = _ROLE_TAIL.sub("", name)
                k = normalize_key(name)
            if conf < ENTITY_CONF[etype] or _junk(name, etype) or (k in ents and ents[k]["conf"] == 0.95):
                continue
            if k not in ents or conf > ents[k]["conf"]:
                ents[k] = {"name": name, "type": etype, "conf": round(conf, 4)}
    rels: dict[tuple, dict] = {}
    for label, items in raw.get("relation_extraction", {}).items():
        rtype = REL_LABELS[label][0]
        heads, tails = REL_TYPES[rtype]
        for it in items:
            h, t = _clean(it["head"]["text"]), _clean(it["tail"]["text"])
            hk, tk = normalize_key(h), normalize_key(t)
            if it["confidence"] < REL_CONF[rtype] or hk == tk or hk not in ents or tk not in ents:
                continue  # both ends must be entities that survived typing and the junk filter
            if ents[hk]["type"] not in heads or ents[tk]["type"] not in tails:
                continue
            if rtype == "DEPENDS_ON":  # a dependency endpoint is a service whatever else it was called
                for k in (hk, tk):
                    ents[k]["type"] = "service"
            key = (hk, rtype, tk)
            if key not in rels or it["confidence"] > rels[key]["conf"]:
                rels[key] = {"head": ents[hk]["name"], "type": rtype, "tail": ents[tk]["name"],
                             "conf": round(it["confidence"], 4)}
    for who, thing, ttype in _table_owners(text):
        for n, t in ((who, "person"), (thing, ttype)):
            ents[normalize_key(n)] = {"name": n, "type": t, "conf": 0.95}
        rels[(normalize_key(who), "OWNS", normalize_key(thing))] = {"head": who, "type": "OWNS", "tail": thing, "conf": 0.9}
    return {"entities": list(ents.values()), "relations": list(rels.values())}


def extract_batch(texts: list[str]) -> list[dict]:
    """One batched GLiNER pass (entities + relations) per text; long texts are split by the library."""
    if not texts:
        return []
    m = gliner()
    run = lambda ts, bs: m.batch_extract_long(ts, _schema(m), batch_size=bs, threshold=0.4,  # noqa: E731
                                              include_confidence=True, chunk_size=MAX_WORDS)
    try:
        raws = run(texts, 4)
    except torch.cuda.OutOfMemoryError:  # a long chunk batch can exceed a 6 GB card: retry one text at a time
        torch.cuda.empty_cache()
        raws = [run([t], 1)[0] for t in texts]
    return [_shape(r, t) for r, t in zip(raws, texts)]


def extract(text: str) -> dict:
    return extract_batch([text])[0]


def _softmax_batch(texts: list[str], task: str, labels: list[str]) -> list[dict[str, float]]:
    m = gliner()
    # multi_label + threshold 0 + softmax returns the whole distribution instead of only the top label
    s = m.create_schema().classification(task, labels, multi_label=True, cls_threshold=0.0, class_act="softmax")
    out = m.batch_extract(texts, s, batch_size=16, include_confidence=True)
    return [{r["label"]: r["confidence"] for r in o[task]} for o in out]


def _softmax_labels(text: str, task: str, labels: list[str]) -> dict[str, float]:
    return _softmax_batch([text], task, labels)[0]


def classify_memory(text: str) -> tuple[str, float]:
    return classify_memory_batch([text])[0]


_NARRATION = re.compile(r"^(let me|let's|i'll|i will|now |sure|ok\b|okay|looks good|thanks|thank you|running|reading|checking)", re.I)
_CUES = re.compile(r"\b(always|never|must|because|decided|root cause|lesson|prefer|should|instead of|rather than|fixed|requires?)\b", re.I)


def worth_keeping_batch(texts: list[str]) -> list[float]:
    """P(durable knowledge) from GLiNER label mass, nudged by cheap surface cues (the base model alone is ~70% right)."""
    out = []
    for text, p in zip(texts, _softmax_batch(texts, "worth", _KEEP + _DROP)):
        s, t = sum(p[k] for k in _KEEP), text.strip()
        if t.endswith("?") or _NARRATION.match(t):
            s *= 0.4
        if _CUES.search(t):
            s = min(1.0, s + 0.15)
        if len(t.split()) < 4:
            s *= 0.5
        out.append(round(s, 4))
    return out


def worth_keeping(text: str) -> float:
    return worth_keeping_batch([text])[0]


def classify_memory_batch(texts: list[str]) -> list[tuple[str, float]]:
    res = []
    for p in _softmax_batch(texts, "memory_type", list(MEMORY_KINDS)):
        best = max(p, key=p.get)
        res.append((MEMORY_KINDS[best], round(p[best], 4)))
    return res
