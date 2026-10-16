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


# hyphenated service names the model sometimes misses: <word>-service, api-gateway, bank-connector ...
_SVC = re.compile(r"\b[a-z][a-z0-9]+(?:-[a-z0-9]+)*-(?:service|gateway|cache|pipeline|connector|dashboard|scoring|bridge)\b")
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


# generic phrases ("Platform engineer", "other services", "config file", "new file") are descriptions, not named things
_GEN_HEAD = {"other", "new", "old", "same", "this", "that", "some", "all", "each", "every", "any", "current", "main", "enterprise"}
_GEN_TAIL = {"channel", "engineer", "engineers", "manager", "managers", "file", "files", "note", "notes", "harness", "services",
             "customers", "accounts", "handbook", "record", "records", "page", "pages", "doc", "docs", "policy", "rules", "rule",
             "issue", "issues", "request", "requests", "process", "workflow", "team", "teams", "group", "layer", "side", "path"}


def _junk(name: str, etype: str = "other") -> bool:
    k = normalize_key(name)
    ws = k.split()
    if len(k) < 2 or k in _JUNK or k.isdigit() or len(ws) > 4 or (etype in _STRICT and not _proper(name)):
        return True
    if etype in ("person", "ticket", "incident", "decision", "customer"):
        return False
    return ws[0] in _GEN_HEAD or (len(ws) > 1 and ws[-1] in _GEN_TAIL and "." not in name and "/" not in name)


def _schema(m, entities: bool):
    sch = m.create_schema()
    if entities:
        return sch.entities({k: d for k, (_, d) in ENTITY_LABELS.items()})
    return sch.relations({k: d for k, (_, d) in REL_LABELS.items()})


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


def _ctx_entity(title: str) -> dict | None:
    """The document's own ADR/ticket/incident id from its title ("ADR-005: ..."), used as the target of "Decided by"."""
    for pat, etype in _IDS:
        mt = pat.search(title or "")
        if mt:
            return {"name": mt.group(), "type": etype, "conf": 0.95}


def _entities(raw: dict, text: str, title: str = "") -> dict[str, dict]:
    ents: dict[str, dict] = {}
    for pat, etype in _IDS:
        for mt in pat.findall(text):
            ents[normalize_key(mt)] = {"name": mt, "type": etype, "conf": 0.95}
    ctx = _ctx_entity(title)
    if ctx:
        ents[normalize_key(ctx["name"])] = ctx
    for mt in _SVC.findall(text):
        ents.setdefault(normalize_key(mt), {"name": mt, "type": "service", "conf": 0.9})
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
    if ctx:
        ents[normalize_key(ctx["name"])] = ctx
    for who, thing, ttype in _table_owners(text):
        for n, t in ((who, "person"), (thing, ttype)):
            ents[normalize_key(n)] = {"name": n, "type": t, "conf": 0.95}
    return ents


def _windows(text: str) -> list[str]:
    """Sentence-sized relation windows: GLiNER pairs entities far better inside one or two sentences than in a chunk."""
    out = []
    for line in text.splitlines():
        line = re.sub(r"^\s*(?:[-*>#]+|\d+\.)\s*", "", line.strip())
        line = re.sub(r"^\*\*\[[^\]]*\]\s*[^:*]*:\*\*\s*|\*\*|`", "", line)  # chat "**[time] Name:**" prefix, bold, ticks
        if not line or line.startswith("|") or line.startswith("---"):
            continue
        cur = ""
        for sen in _SENT.split(line):
            if cur and len((cur + " " + sen).split()) > 40:
                out.append(cur)
                cur = ""
            cur = (cur + " " + sen).strip()
        if cur:
            out.append(cur)
    return [w for w in out if len(w.split()) >= 3]


_SENT = re.compile(r"(?<=[.!?])\s+")
_H, _T = r"(?P<h>§\d+§)", r"(?P<t>§\d+§)"
_DET = r"(?:the |its |their )?(?:current |new |old |previous |former |sole )?"
# deterministic patterns over a window whose entity mentions are replaced by §i§; (regex, relation type)
_PATTERNS = [(re.compile(p, re.I), r) for p, r in [
    (_H + r",? (?:now |still |also |currently |will )?(?:owns|own|maintains|is responsible for|is on the hook for|took over|takes over|has taken over|is taking over|inherits) " + _T, "OWNS"),
    (_H + r" (?:is|was|becomes|became|is now|stays|remains) " + _DET + r"(?:owner|maintainer|point person|steward) (?:of|for) " + _T, "OWNS"),
    (_T + r" (?:is |was |now )?(?:owned|maintained) by " + _H, "OWNS"),
    (r"owner of " + _T + r" (?:is|was|becomes|became|will be|changes to|moves to) " + _H, "OWNS"),
    (_T + r" (?:owner|maintainer)(?: is|:| =|,)? " + _H, "OWNS"),
    (_T + r" (?:moves|moved|is moving|transfers|transferred|is transferred|is handed over|handed over|hands over) from §\d+§ to " + _H, "OWNS"),
    (_H + r" (?:now |still |also |will )?(?:depends on|relies on|calls|reads (?:its |the |all )?(?:\w+ )?(?:settings|config|configuration|values|keys) from|reads from|talks to|authenticates (?:via|through|against|with)|consumes from|publishes (?:events )?to|needs|requires) " + _T, "DEPENDS_ON"),
    (r"(?:rename|renamed|renaming|renames) " + _H + r" (?:to|as|into) " + _T, "RENAMED_TO"),
    (_H + r" (?:was |is |has been |gets |will be |is being )?renamed (?:to|as|into) " + _T, "RENAMED_TO"),
    (_T + r" \((?:formerly|previously|was|ex-|née|aka|also known as|renamed from)[ :]*(?:called |named |known as )?" + _H + r"\)", "RENAMED_TO"),
    (_T + r",? (?:formerly|previously|which was|which used to be|used to be|was formerly|was previously|was called|was named)[ :]*(?:called |named |known as )?" + _H, "RENAMED_TO"),
    (_H + r" (?:is |was |has been |gets |will be )?(?:replaced|superseded) by " + _T, "REPLACED_BY"),
    (_H + r" (?:has |have )?(?:approved|signed off on|signed off|okayed|ok'd|accepted|green-?lit|gave (?:the )?(?:go-?ahead|approval) (?:for|to|on)) " + _T, "APPROVED"),
    (_T + r" (?:was |were |is |got )?(?:approved|signed off|accepted) by " + _H, "APPROVED"),
]]


_SELF = [(re.compile(p, re.I), r) for p, r in [
    (_H + r" (?:made|took) the (?:final )?decision", "DECIDED"),
    (_H + r" (?:decided|ruled)(?: on it|\b)", "DECIDED"),
    (_H + r" (?:has |have )?(?:approved|signed off on|signed off|accepted|okayed) (?:it|this|that|the (?:decision|change|proposal|rename|request|plan|record))", "APPROVED"),
]]


def _locate(win: str, ents: dict[str, dict]) -> tuple[str, list[str]]:
    """Replace entity mentions in `win` by §i§ placeholders (longest first); persons also match by first name."""
    names = {e["name"]: k for k, e in ents.items()}
    for k, e in ents.items():
        if e["type"] == "person" and " " in e["name"]:
            names.setdefault(e["name"].split()[0], k)
    tails = {}
    for k, e in ents.items():  # "the gateway" for api-gateway, when that tail word is unambiguous
        t = k.split()[-1]
        if e["type"] in ("service", "component", "tool") and len(k.split()) > 1 and len(t) >= 4 and t not in _JUNK:
            tails.setdefault(t, []).append(k)
    names.update({t: ks[0] for t, ks in tails.items() if len(ks) == 1 and t not in names})
    keys: list[str] = []
    for n in sorted(names, key=len, reverse=True):
        if len(n) < 3:
            continue
        pat = re.compile(r"(?<![\w§-])" + re.escape(n) + r"(?![\w§-])", 0 if " " not in n and n[0].isupper() else re.I)
        def sub(_m, k=names[n]):
            keys.append(k)
            return f"§{len(keys) - 1}§"
        win = pat.sub(sub, win)
    return re.sub(r"\b(?:the|its|their|our|this|that) (§\d+§)", r"\1", win, flags=re.I), keys


def _find(ents: dict, text: str) -> str | None:
    """Entity key for a relation endpoint: exact key, else the unique person whose first/last name it is."""
    k = normalize_key(text)
    if k in ents:
        return k
    hit = [c for c, e in ents.items() if (e["type"] == "person" and k in (c.split()[0], c.split()[-1]))
           or (e["type"] in ("service", "component", "tool") and len(k) >= 4 and c.endswith(" " + k))]
    return hit[0] if len(hit) == 1 else None


_BY = re.compile(r"^(?:decided|approved|signed off|accepted)( by)?:?\s", re.I)


def _relations(ents: dict, windows: list[str], gl: list[dict], title: str = "") -> list[dict]:
    rels: dict[tuple, dict] = {}

    def add(hk, rtype, tk, conf):
        heads, tails = REL_TYPES[rtype]
        if hk == tk or hk not in ents or tk not in ents or ents[hk]["type"] not in heads or ents[tk]["type"] not in tails:
            return
        if rtype == "DEPENDS_ON":  # a dependency endpoint is a service whatever else it was called
            ents[hk]["type"] = ents[tk]["type"] = "service"
        key = (hk, rtype, tk)
        if key not in rels or conf > rels[key]["conf"]:
            rels[key] = {"head": ents[hk]["name"], "type": rtype, "tail": ents[tk]["name"], "conf": round(conf, 4)}

    for raw in gl:  # GLiNER relations, windowed
        for label, items in raw.get("relation_extraction", {}).items():
            rtype = REL_LABELS[label][0]
            for it in items:
                if it["confidence"] >= REL_CONF[rtype]:
                    hk, tk = _find(ents, _clean(it["head"]["text"])), _find(ents, _clean(it["tail"]["text"]))
                    if hk and tk:
                        add(hk, rtype, tk, it["confidence"])
    ctx = _ctx_entity(title)
    ck = normalize_key(ctx["name"]) if ctx else None
    for win in windows:  # deterministic patterns
        marked, keys = _locate(win, ents)
        by = _BY.match(win)
        if by and ck and by.group(1):  # ADR sections "Decided by: A (CTO)" / "Approved by: B": the target is the document itself
            rtype = "DECIDED" if win.lower().startswith("decided") else "APPROVED"
            for i in re.findall(r"§(\d+)§", marked.split("(")[0]):
                add(keys[int(i)], rtype, ck, 0.9)
        if ck:  # "A made the decision", "B approved it": the target is the document's own decision or ticket
            for pat, rtype in _SELF:
                for mt in pat.finditer(marked):
                    add(keys[int(mt["h"][1:-1])], rtype, ck, 0.9)
        for pat, rtype in _PATTERNS:
            for mt in pat.finditer(marked):
                add(keys[int(mt["h"][1:-1])], rtype, keys[int(mt["t"][1:-1])], 0.9)
    return list(rels.values())


def extract_batch(texts: list[str], titles: list[str] | None = None) -> list[dict]:
    """Entities per text (GLiNER, batched), then relations per sentence window (GLiNER plus patterns, batched)."""
    if not texts:
        return []
    m = gliner()

    def run(ts, schema, bs, **kw):
        try:
            return m.batch_extract_long(ts, schema, batch_size=bs, threshold=0.4, include_confidence=True,
                                        chunk_size=MAX_WORDS, **kw)
        except torch.cuda.OutOfMemoryError:  # a long batch can exceed a 6 GB card: retry one text at a time
            torch.cuda.empty_cache()
            return [m.batch_extract_long([t], schema, batch_size=1, threshold=0.4, include_confidence=True,
                                         chunk_size=MAX_WORDS)[0] for t in ts]

    titles = titles or [""] * len(texts)
    ents = [_entities(r, t, ti) for r, t, ti in zip(run(texts, _schema(m, True), 4), texts, titles)]
    wins = [_windows(t) for t in texts]
    flat = [w for ws in wins for w in ws]
    glr = run(flat, _schema(m, False), 16) if flat else []
    out, i = [], 0
    for e, ws, t, ti in zip(ents, wins, texts, titles):
        rels = _relations(e, ws, glr[i:i + len(ws)], ti)
        i += len(ws)
        seen = {(normalize_key(r["head"]), r["type"], normalize_key(r["tail"])) for r in rels}
        for who, thing, _ in _table_owners(t):
            if (normalize_key(who), "OWNS", normalize_key(thing)) not in seen:
                rels.append({"head": who, "type": "OWNS", "tail": thing, "conf": 0.9})
        out.append({"entities": list(e.values()), "relations": rels})
    return out


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
