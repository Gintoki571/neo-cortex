"""GLiNER2.5 extraction and classification with descriptive labels (short labels misroute, see the spike note).

`extract` returns entities typed per the data-model contract and relations from its whitelist. Nothing here calls an LLM.
"""
import re
from datetime import datetime, timezone

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
validator dependency interface identifier override eviction memory cutoff batches freeze totals checkout sre""".split())
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
    if len(k) < 2 or k in _JUNK or k == "on call" or k.isdigit() or len(ws) > 4 or (etype in _STRICT and not _proper(name)):
        return True
    if etype in ("person", "ticket", "incident", "decision", "customer"):
        return False
    if etype == "team" and name.isupper():  # "SRE" is a role
        return True
    return ws[0] in _GEN_HEAD or (len(ws) > 1 and ws[-1] in _GEN_TAIL and "." not in name and "/" not in name)


def _schema(m, entities: bool):
    sch = m.create_schema()
    if entities:
        return sch.entities({k: d for k, (_, d) in ENTITY_LABELS.items()})
    return sch.relations({k: d for k, (_, d) in REL_LABELS.items()})


_NAME = re.compile(r"[A-Z][\w'.-]+(?: [A-Z][\w'.-]+)+")
_SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+")


def _table_facts(text: str) -> list[tuple[str, str, str, str, str]]:
    """Markdown tables row by row: (head, relation, tail, head type, tail type). The first cell is the subject; columns are
    read by header word: owner -> OWNS, team (row about a person) -> MEMBER_OF, depends/upstream/calls/uses -> DEPENDS_ON."""
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
        first = cells[0]
        if not first:
            continue
        svc = bool(_SLUG.fullmatch(first))
        team = next((cells[i] for i, h in enumerate(hdr) if h in ("team", "department") and i < len(cells)), "")
        for i, h in enumerate(hdr[1:], 1):
            c = cells[i] if i < len(cells) else ""
            if not c:
                continue
            if "owner" in h:
                who = _NAME.search(c)
                if who:
                    out.append((who.group(), "OWNS", first, "person", "service" if svc else "other"))
                    if svc and team and _NAME.search(c) and re.fullmatch(r"[A-Z][a-z]+", team):  # the owner of a team's row is on that team
                        out.append((who.group(), "MEMBER_OF", team, "person", "team"))
            elif h in ("team", "department") and _NAME.fullmatch(first):
                out.append((first, "MEMBER_OF", c, "person", "team"))
            elif svc and re.search(r"depend|upstream|calls|uses|needs|reads", h):
                out += [(first, "DEPENDS_ON", d, "service", "service") for d in
                        (x.strip(" `*") for x in re.split(r"[,;/]| and ", c)) if _SLUG.fullmatch(d)]
    return out


def _ctx_entity(title: str) -> dict | None:
    """The document's own ADR/ticket/incident id from its title ("ADR-005: ..."), used as the target of "Decided by"."""
    for pat, etype in _IDS:
        mt = pat.search(title or "")
        if mt:
            return {"name": mt.group(), "type": etype, "conf": 0.95}


_TEAM = re.compile(r"\b(?:[Tt]he )?([A-Z][a-z]+) (?:team|squad)\b")
_NOT_TEAM = {"The", "This", "That", "Our", "Each", "Every", "Other", "Same", "New", "Whole", "Whole", "Your", "My", "A", "An", "Any", "Which"}


_PAREN_TEAM = re.compile(r"\b[A-Z][a-z]+ [A-Z][a-z]+ \((?:[^()]*, )([A-Z][a-z]+)\)")      # "Sofia Marchetti (Engineering Manager, Payments)"
_LIST_TEAM = re.compile(r"^\W*([A-Z][a-z]+): (?:.*?[A-Z][a-z]+ [A-Z][a-z]+ \([^)]*\)){2,}", re.M)  # "Leadership: A B (CEO) and C D (CTO)"


def team_names(text: str) -> set[str]:
    """Team names a text gives away by its shape: "the Payments team", "Name Name (Role, Team)", "Team: A B (CEO) and C D (CTO)"."""
    found = set(_TEAM.findall(text)) | set(_PAREN_TEAM.findall(text)) | set(_LIST_TEAM.findall(text))
    return found - _NOT_TEAM


def _entities(raw: dict, text: str, title: str = "", author: str = "", teams=()) -> dict[str, dict]:
    ents: dict[str, dict] = {}
    for pat, etype in _IDS:
        for mt in pat.findall(text):
            ents[normalize_key(mt)] = {"name": mt, "type": etype, "conf": 0.95}
    ctx = _ctx_entity(title)
    if ctx:
        ents[normalize_key(ctx["name"])] = ctx
    for mt in _SVC.findall(text):
        ents.setdefault(normalize_key(mt), {"name": mt, "type": "service", "conf": 0.9})
    for mt in team_names(text) | {t for t in teams if re.search(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", text)}:
        ents.setdefault(normalize_key(mt), {"name": mt, "type": "team", "conf": 0.85})
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
    if author:
        ents[normalize_key(author)] = {"name": author, "type": "person", "conf": 0.95}
    for who, _, thing, wt, tt in _table_facts(text):
        for n, t in ((who, wt), (thing, tt)):
            ents[normalize_key(n)] = {"name": n, "type": t, "conf": 0.95}
    return ents


_SENT = re.compile(r"(?<=[.!?])\s+")
# "**[2026-07-17 14:00] Sam Okafor:** text" (chat) and "**Chen Wei (2026-07-25):** text" (ticket comment): the speaker is "I"
_SPK = re.compile(r"^\W*\*\*(?:\[[^\]]*\]\s*)?([^:*()\[\]]+?)(?:\s*\([^)]*\))?:\*\*\s*")


def _windows(text: str) -> tuple[list[str], list[str | None]]:
    """Sentence-sized relation windows (GLiNER pairs entities far better inside one or two sentences than in a chunk) and the
    speaker of each (chat/comment lines only)."""
    out, spk = [], []
    for line in text.splitlines():
        who = None
        m = _SPK.match(line)
        if m:
            who, line = m.group(1).strip(), line[m.end():]
        line = re.sub(r"^\s*(?:[-*>#]+|\d+\.)\s*", "", line.strip())
        line = re.sub(r"\*\*|`", "", line)
        if not line or line.startswith("|") or line.startswith("---"):
            continue
        cur = ""
        for sen in _SENT.split(line):
            if cur and len((cur + " " + sen).split()) > 40:
                out.append(cur)
                spk.append(who)
                cur = ""
            cur = (cur + " " + sen).strip()
        if cur:
            out.append(cur)
            spk.append(who)
    keep = [i for i, w in enumerate(out) if len(w.split()) >= 3]
    return [out[i] for i in keep], [spk[i] for i in keep]


_H, _T = r"(?P<h>§\d+§)", r"(?P<t>§\d+§)"
_DET = r"(?:the |its |their )?(?:current |new |old |previous |former |sole |primary |main )?"
_ADV = r"(?:(?:now|still|also|currently|will|always|only|directly|then|already|both|each|first|just|mostly|usually|typically) )*"
_GAP = r"(?:[\w'-]+ ){0,2}?"          # up to two plain words between a verb and its object
_FAR = r"[^§.;]{0,40}?"               # a short stretch with no entity in it
_CALLS = (r"(?:depends? on|relies on|rely on|calls?|asks|queries|consults|talks? (?:to|with)|speaks? to|uses?|needs?|requires?|"
          r"waits? for|hits|reads?|consumes?|fetches|pulls|sits in front of|sits on top of|is built on|runs on|is backed by|"
          r"is served by|authenticates? (?:via|through|against|with)|checks? (?:[\w'-]+ ){0,4}?(?:against|with|through|via|using)|"
          r"forwards? (?:[\w'-]+ ){0,3}?to|routes? (?:[\w'-]+ ){0,3}?to|passes? (?:[\w'-]+ ){0,3}?to|proxies to)")
_IO = (r"(?:reads?|writes?|stores?|keeps?|publishes?|listens?|consumes?|subscribes?|pushes|pulls|fetches|loads|sends?|"
       r"persists|caches|looks up|gets)")
_NO_REACH = r"(?:cannot|can't|can not|could not|fails? to|is unable to|unable to) (?:reach|connect to|talk to|call|read from|get)"
# deterministic patterns over a sentence whose entity mentions are replaced by §i§; (regex, relation type), named groups h and t
_PATTERNS = [(re.compile(p, re.I), r) for p, r in [
    # ownership
    (_H + r",? ?(?:who |which |that )?" + _ADV + r"(?:owns|own|maintains|maintain|is responsible for|are responsible for|is on the hook for|took over|takes over|has taken over|is taking over|inherits|looks after) " + _GAP + _T, "OWNS"),
    (_H + r" (?:takes|took|taking|has taken|will take) (?:over )?(?:the )?(?:ownership|responsibility) (?:of|for) " + _T, "OWNS"),
    (_H + r" (?:is|becomes|became|am|'m|is now|stays|remains) " + _DET + r"(?:owner|maintainer|point person|steward) (?:of|for) " + _T, "OWNS"),
    (_T + r" (?:is |now |are )?(?:owned|maintained) by " + _H, "OWNS"),
    (r"(?:the )?owner of " + _T + r" (?:is|becomes|became|will be|changes to|moves to|:) ?" + _H, "OWNS"),
    (_T + r"(?:'s)?[^§\n.]{0,30}?\b(?:owner|maintainer)s?\b[^§\n.]{0,8}?" + _H, "OWNS"),
    (_T + r" (?:moves|moved|is moving|transfers|transferred|is transferred|is handed over|handed over|hands over|goes) from §\d+§ to " + _H, "OWNS"),
    (_T + r" (?:is |was |gets |got )?(?:handed|passed|transferred|assigned) (?:over )?to " + _H, "OWNS"),
    # dependencies
    (_H + r"(?:,? (?:which|that))? " + _ADV + _CALLS + r" " + _GAP + _T, "DEPENDS_ON"),
    (_H + r"(?:,? (?:which|that))? " + _ADV + _IO + r"(?: [^§.;]{0,40}?)? (?:from|to|in|into|on|via|through) " + _T, "DEPENDS_ON"),
    (_H + r" " + _NO_REACH + r" " + _T, "DEPENDS_ON"),
    (_H + _FAR + r" (?:is|are|was|were) (?:[\w'-]+ )?(?:checked|vouched for|validated|verified|authenticated|served|backed|queried|consulted) (?:first )?(?:by|against|with) " + _T, "DEPENDS_ON"),
    (_T + r" (?:is|are) (?:called|used|read|queried|consumed|consulted|needed|required) by " + _H, "DEPENDS_ON"),
    (_T + r"[^§.;]{0,50}?\b(?:holds|stores|keeps|serves|backs|feeds|supplies|provides)\b[^§.;]{0,40}?\bfor " + _H, "DEPENDS_ON"),
    (_T + r" (?:is|are) (?:an? |the )?(?:upstream|dependency|backend) (?:of|for) " + _H, "DEPENDS_ON"),
    (_H + r" (?:is|are) (?:an? |the )?(?:downstream|consumer|client|caller)s? of " + _T, "DEPENDS_ON"),
    (_T + r"[^§.;]{0,60}? (?:(?:that|which) )?" + _H + r" (?:consults?|calls?|uses?|reads?|needs?|depends on|relies on|queries|checks?) ", "DEPENDS_ON"),
    (_H + r"(?:'s)? (?:only |sole |single |main |direct )?(?:upstream|dependency|dependencies|backend)(?: service)? (?:is|are|:) ?" + _T, "DEPENDS_ON"),
    (_H + r" has " + _T + r" as (?:an? |its |the )?(?:upstream|dependency|backend)", "DEPENDS_ON"),
    (r"(?:settings|config\w*|keys|values|overrides|limits|templates) (?:for|of) " + _H + r" (?:live|lives|are stored|are kept|are held|come|comes) (?:in|under|from) " + _T, "DEPENDS_ON"),
    # rename and replacement
    (r"(?:rename|renamed|renaming|renames) " + _H + r" (?:to|as|into) " + _T, "RENAMED_TO"),
    (_H + r" (?:was |is |has been |gets |will be |is being )?renamed (?:to|as|into) " + _T, "RENAMED_TO"),
    (_H + r" (?:(?:is|was|has been|gets|will be) )?now (?:called|known as|named) " + _T, "RENAMED_TO"),
    (r"(?:as of (?:today|now)|from (?:today|now on)),? " + _H + r" (?:is|becomes) " + _T, "RENAMED_TO"),
    (_T + r" is the new name (?:of|for) " + _H, "RENAMED_TO"),
    (_H + r"'s new name is " + _T, "RENAMED_TO"),
    (_T + r" \((?:formerly|previously|was|ex-|née|aka|also known as|renamed from|named)[ :]*(?:called |named |known as )?" + _H + r"(?: until [^)]*)?\)", "RENAMED_TO"),
    (_T + r",? (?:formerly|previously|which was|which used to be|used to be|was formerly|was previously|was called|was named)[ :]*(?:called |named |known as )?" + _H, "RENAMED_TO"),
    (_H + r" (?:is |was |has been |gets |will be )?(?:replaced|superseded) by " + _T, "REPLACED_BY"),
    (_T + r" (?:was |is |were )?decided by " + _H, "DECIDED"),
    # approval, causes, fixes, reports
    (_H + r" (?:has |have )?(?:approved|signed off on|signed off|okayed|ok'd|accepted|green-?lit|gave (?:the )?(?:go-?ahead|approval) (?:for|to|on)) " + _T, "APPROVED"),
    (_T + r" (?:was |were |is |got )?(?:approved|signed off|accepted) by " + _H, "APPROVED"),
    (_H + r" (?:was |were |is |had been )?(?:caused|triggered|started|set off|introduced|broken|resulted|brought on) (?:directly )?by " + _T, "CAUSED_BY"),
    (_H + r" (?:came|stems?|resulted) from " + _T, "CAUSED_BY"),
    (_T + r" (?:caused|triggered|broke|led to) " + _H, "CAUSED_BY"),
    (_H + r" (?:was |is |got |has been )?(?:fixed|resolved|mitigated|rolled back|reverted|corrected) by " + _T, "FIXED_BY"),
    (_T + r" (?:fixed|resolved|mitigated|rolled back|reverted) " + _H, "FIXED_BY"),
    (_H + r" (?:reported|raised|filed|flagged) " + _T, "REPORTED"),
    # team membership
    (_H + r" \((?:[^()§]*?, ?)?" + _T + r"\)", "MEMBER_OF"),
    (_H + r" (?:works|is working|worked|sits|is based) (?:on|in|with) (?:the )?" + _T, "MEMBER_OF"),
    (_H + r" (?:is|was|joined|joins) (?:a |an |the )?(?:member of |part of |on |in |to )(?:the )?" + _T, "MEMBER_OF"),
    (_H + r" (?:is |are |am |was |has been )?(?:currently |now )?(?:the |our )?on[- ]call (?:for|of) " + _T, "OWNS"),
    (_H + r"(?:,? (?:who|which))? (?:manages|leads|heads|runs) (?:the )?" + _T, "MEMBER_OF"),
    (_H + r" (?:is|was) (?:the |our )?(?:[\w-]+ ){0,2}(?:manager|lead|head|director) (?:for|of) (?:the )?" + _T, "MEMBER_OF"),
    (_H + r",? (?:of|from) (?:the )?" + _T, "MEMBER_OF"),
    (_H + r" on (?:the )?" + _T, "MEMBER_OF"),
    (_T + r"'s (?:member |engineer |manager |lead )" + _H, "MEMBER_OF"),
]]
# the head is the document's own incident/decision (title id) or the incident named in the sentence
_INC = [(re.compile(p, re.I), r) for p, r in [
    (r"(?:root cause|cause|trigger)(?: of [^§]*§\d+§)?(?: was| is| were|:| =)\s*(?:an? |the )?(?:[\w'-]+ ){0,3}?" + _T, "CAUSED_BY"),
    (r"(?:because of|due to|caused by|triggered by) " + _GAP + _T, "CAUSED_BY"),
    (r"(?:fixed|resolved|mitigated|rolled back|reverted) by " + _T, "FIXED_BY"),
]]
_SELF = [(re.compile(p, re.I), r) for p, r in [
    (_H + r" (?:made|took) the (?:final )?decision", "DECIDED"),
    (_H + r" (?:decided|ruled)(?: on it|\b)", "DECIDED"),
    (_H + r" (?:has |have )?(?:approved|signed off on|signed off|accepted|okayed) (?:it|this|that|the (?:decision|change|proposal|rename|request|plan|record))", "APPROVED"),
    (r"(?:sign-?off|approval) (?:was )?(?:given |granted )?(?:by|from) " + _H, "APPROVED"),
]]
# "Email templates ... all come from config-service": the subject is the chunk's topic
_FROM = re.compile(r"^[^§]*\b(?:settings|config\w*|keys|values|overrides|limits|templates?)\b[^§]*?\b(?:come|comes|live|lives|are read|are loaded|are stored|are kept) (?:from|in) " + _T, re.I)
_OWN_SELF = re.compile(_H + r" (?:is|was|am|'m|are) (?:also )?(?:the |its )?(?:current |new |sole |primary )?(?:owner|maintainer)\b(?! (?:of|for))", re.I)
_NEG = re.compile(r"\b(?:not|never|no longer|n't|without|nothing|nobody|isn't|doesn't|don't|won't)\W+(?:\w+\W+){0,3}$", re.I)
# a mention of a former state ("the previous owner was Lukas", "Lukas handed it over") never asserts ownership or membership
_FORMER = re.compile(r"\b(?:former|formerly|previous(?:ly)?|used to|until|no longer|stepped down|prior|earlier|ex-|"
                     r"old(?:er)? (?:\w+ )?(?:owner|maintainer|team)|was (?:the )?(?:owner|maintainer)|handed (?:\w+ )?(?:over|off)(?! to))\b", re.I)
_FORMER_TEAM = re.compile(r"\b(?:former|formerly|used to|no longer|until|stepped down|ex-)\b", re.I)
_CUE = re.compile(r"\b(?:own\w*|maintain\w*|responsib\w*|on the hook|steward|took over|takes over|inherit\w*|handover|moves? to|"
                  r"assigned|manag\w*|leads?|members?|teams?|works? on|joined|part of|on call)\b", re.I)
_MON = "jan feb mar apr may jun jul aug sep oct nov dec".split()
_MONTH = r"(?:" + "|".join(m + r"[a-z]*" for m in _MON) + r")"
_DATE = (r"(?P<iso>\d{4}-\d{2}-\d{2})|(?P<dmy>\d{1,2})(?:st|nd|rd|th)? (?P<m1>" + _MONTH + r"),? (?P<y1>\d{4})|"
         r"(?P<m2>" + _MONTH + r") (?P<d2>\d{1,2})(?:st|nd|rd|th)?,? (?P<y2>\d{4})")
_EFF = re.compile(r"\b(?:effective(?: from| on)?|from|starting(?: on| from)?|starts? on|beginning(?: on)?|takes effect on|as of|since) (?:" + _DATE + ")", re.I)


def _eff_ms(sen: str) -> int | None:
    """The date the asserted state starts ("effective 2026-09-01", "from 1 September 2026") if the sentence has exactly one."""
    out = set()
    for m in _EFF.finditer(sen):
        try:
            if m["iso"]:
                y, mo, d = map(int, m["iso"].split("-"))
            elif m["dmy"]:
                y, mo, d = int(m["y1"]), _MON.index(m["m1"][:3].lower()) + 1, int(m["dmy"])
            else:
                y, mo, d = int(m["y2"]), _MON.index(m["m2"][:3].lower()) + 1, int(m["d2"])
            out.add(int(datetime(y, mo, d, tzinfo=timezone.utc).timestamp() * 1000))
        except ValueError:
            pass
    return out.pop() if len(out) == 1 else None


_SUFFIX = {"service"}
_PRON = re.compile(r"\b(?:it|this service|the service|that service|the component)\b|^\W*its\b", re.I)
_I = re.compile(r"\bI\b")


def _locate(win: str, ents: dict[str, dict], roles: dict[str, str] | None = None) -> tuple[str, list[str]]:
    """Replace entity mentions in `win` by §i§ placeholders (longest first); persons also match by first name.
    `roles` maps a role noun phrase ("the broker") to the entity key the document defines it by."""
    names = {e["name"]: k for k, e in ents.items()}
    names.update(roles or {})
    for k, e in ents.items():
        if e["type"] == "person" and " " in e["name"]:
            names.setdefault(e["name"].split()[0], k)
    tails, stems = {}, {}
    for k, e in ents.items():  # "the gateway" for api-gateway, when that tail word is unambiguous; "the ledger" for ledger-service
        w = k.split()
        if e["type"] in ("service", "component", "tool") and len(w) > 1:
            if len(w[-1]) >= 4 and w[-1] not in _JUNK:
                tails.setdefault(w[-1], []).append(k)
            if len(w) == 2 and w[1] in _SUFFIX and len(w[0]) >= 4 and w[0] not in _JUNK:
                stems.setdefault("the " + w[0], []).append(k)
    names.update({t: ks[0] for t, ks in {**tails, **stems}.items() if len(ks) == 1 and t not in names})
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
    hit = [c for c, e in ents.items() if c and ((e["type"] == "person" and k in (c.split()[0], c.split()[-1]))
           or (e["type"] in ("service", "component", "tool") and len(k) >= 4 and c.endswith(" " + k)))]
    return hit[0] if len(hit) == 1 else None


# passive or subject-less dependency: the head is the chunk's main service ("is written into §ledger§" in a payment-gateway doc)
_PASS = re.compile(r"(?:\b(?:is|are|was|were|gets?|got)\s+(?:then\s+|also\s+|now\s+)?(?:written|sent|published|pushed|forwarded|"
                   r"passed|stored|saved|routed|handed)\s+(?:into|to|onto|via|through)|\b(?:goes|go|went)\s+(?:to|through|via)|"
                   r"\b(?:hands?|handed|sends?|sent|publish(?:es)?|published) (?:[\w']+ ){0,2}?(?:to|onto)|"
                   r"\b(?:reads?|consumes?|subscribes? to)\s+(?:from\s+)?)\s*(?P<t>§\d+§)")
_STATE = {"OWNS", "MEMBER_OF"}          # single-valued relations whose edges are closed by a later document
_EFFECTIVE = _STATE | {"RENAMED_TO"}    # relations that carry the stated effective date as valid_from_ms
_BY = re.compile(r"^(?:decided|approved|signed off|accepted)( by)?:?\s", re.I)
_SVCT = ("service", "component", "tool")
_TASK_KINDS = ("ticket", "meeting", "chat")  # their "Owner:" / action-item lines name the task's owner, never a service's


def _relations(ents: dict, windows: list[str], gl: list[dict], title: str = "", author: str = "",
               speakers: list | None = None, main: str | None = None, kind: str = "") -> list[dict]:
    rels: dict[tuple, dict] = {}

    def add(hk, rtype, tk, conf, eff=None):
        heads, tails = REL_TYPES[rtype]
        if hk == tk or hk not in ents or tk not in ents or ents[hk]["type"] not in heads or ents[tk]["type"] not in tails:
            return
        if rtype == "DEPENDS_ON":  # a dependency endpoint is a service whatever else it was called
            ents[hk]["type"] = ents[tk]["type"] = "service"
        key = (hk, rtype, tk)
        if key not in rels or conf > rels[key]["conf"]:
            rels[key] = {"head": ents[hk]["name"], "type": rtype, "tail": ents[tk]["name"], "conf": round(conf, 4)}
            if eff and rtype in _EFFECTIVE:
                rels[key]["valid_from_ms"] = eff

    for raw, win in zip(gl, windows):  # GLiNER relations, windowed
        for label, items in raw.get("relation_extraction", {}).items():
            rtype = REL_LABELS[label][0]
            for it in items:
                if it["confidence"] >= REL_CONF[rtype]:
                    if rtype in _STATE and (_FORMER.search(win) or not _CUE.search(win)):
                        continue  # ownership/membership only from a sentence that asserts it, not a passing mention
                    hk, tk = _find(ents, _clean(it["head"]["text"])), _find(ents, _clean(it["tail"]["text"]))
                    if hk and tk:
                        add(hk, rtype, tk, it["confidence"], _eff_ms(win))
    ctx = _ctx_entity(title)
    ck = normalize_key(ctx["name"]) if ctx else None
    inc_ents = [k for k, e in ents.items() if e["type"] == "incident"]
    doc_inc = ck if ctx and ctx["type"] == "incident" else (inc_ents[0] if len(inc_ents) == 1 else None)
    ak = normalize_key(author) if author else None
    # "event-pipeline is the message broker": in this document "the broker" names that service
    brokers = {k for k, e in ents.items() if e["type"] == "service" and any(
        re.search(re.escape(e["name"]) + r" is (?:the |a )?(?:message )?broker\b", w, re.I) for w in windows)}
    roles = {"the broker": next(iter(brokers))} if len(brokers) == 1 else None
    located = [_locate(w, ents, roles) for w in windows]
    if main is None:  # the chunk's main service: its most mentioned service-like entity (first one on a tie)
        cnt: dict[str, int] = {}
        for _, keys in located:
            for k in keys:
                if ents[k]["type"] in _SVCT:
                    cnt[k] = cnt.get(k, 0) + 1
        main = max(cnt, key=cnt.get) if cnt else None
    topic = main
    for i, (win, (marked, keys)) in enumerate(zip(windows, located)):
        spk = (speakers[i] if speakers else None)
        sk = _find(ents, spk) if spk else None
        me = sk or ak
        for sen in _SENT.split(marked):
            keys2 = list(keys)

            def ph(k):
                keys2.append(k)
                return f"§{len(keys2) - 1}§"
            first = re.match(r"\W*§(\d+)§", sen)
            sen2 = sen
            if me:
                sen2 = _I.sub(lambda _m: ph(me), sen2)
            if topic:
                sen2 = _PRON.sub(lambda _m: ph(topic), sen2)
            by = _BY.match(sen2)
            if by and ck and by.group(1):  # ADR sections "Decided by: A (CTO) and B (EM, Data)": the target is the document itself
                rtype = "DECIDED" if sen2.lower().startswith("decided") else "APPROVED"
                for j in re.findall(r"§(\d+)§", re.sub(r"\([^)]*\)", "", sen2)):
                    add(keys2[int(j)], rtype, ck, 0.9)

            eff = _eff_ms(sen2)

            def hit(mt, rtype):
                before = sen2[:mt.start()]
                if rtype != "MEMBER_OF" and _NEG.search(before[-40:]) and not mt.group().lower().startswith(("can", "could")):
                    return
                if rtype in _STATE and (_FORMER if rtype == "OWNS" else _FORMER_TEAM).search(sen2[max(0, mt.start() - 40):mt.end()]):
                    return
                add(keys2[int(mt["h"][1:-1])], rtype, keys2[int(mt["t"][1:-1])], 0.9, eff)
            if ck:  # "A made the decision", "B approved it": the target is the document's own decision or ticket
                for pat, rtype in _SELF:
                    for mt in pat.finditer(sen2):
                        add(keys2[int(mt["h"][1:-1])], rtype, ck, 0.9)
            for pat, rtype in _PATTERNS:
                for mt in pat.finditer(sen2):
                    hit(mt, rtype)
            inc = next((k for k in (keys2[int(j)] for j in re.findall(r"§(\d+)§", sen2)) if ents[k]["type"] == "incident"), doc_inc)
            if inc:
                for pat, rtype in _INC:
                    for mt in pat.finditer(sen2):
                        add(inc, rtype, keys2[int(mt["t"][1:-1])], 0.9)
            ro = re.match(r"\W*§(\d+)§:(.*)", sen2)
            if ro and ents[keys2[int(ro.group(1))]]["type"] == "team":  # "Leadership: Maggie Ellison (CEO) and Tobias Wren (CTO)"
                for j in re.findall(r"§(\d+)§", ro.group(2)):
                    add(keys2[int(j)], "MEMBER_OF", keys2[int(ro.group(1))], 0.9)
            # "Owner: Lukas Brandt" owns a service only on a line that names one, or in a non-task doc whose main service is `topic`
            ow = re.match(r"\W*(?:owner|maintainer)s?\s*:\s*§(\d+)§", sen2, re.I)
            if ow and not _FORMER.search(sen2):
                svc = next((keys2[int(j)] for j in re.findall(r"§(\d+)§", sen2) if ents[keys2[int(j)]]["type"] in _SVCT), None)
                if svc is None and topic and kind not in _TASK_KINDS:
                    svc = topic
                if svc:
                    add(keys2[int(ow.group(1))], "OWNS", svc, 0.9, eff)
            if topic:
                for mt in _PASS.finditer(sen):  # on the sentence before its subject became the topic: no head entity before the verb
                    if "§" not in sen[:mt.start()]:
                        add(topic, "DEPENDS_ON", keys2[int(mt["t"][1:-1])], 0.9)
                for mt in _FROM.finditer(sen2):
                    add(topic, "DEPENDS_ON", keys2[int(mt["t"][1:-1])], 0.9)
                for mt in _OWN_SELF.finditer(sen2):
                    if not _FORMER.search(sen2[max(0, mt.start() - 40):mt.end()]):
                        add(keys2[int(mt["h"][1:-1])], "OWNS", topic, 0.9, eff)
            if first and ents[keys[int(first.group(1))]]["type"] in _SVCT:
                topic = keys[int(first.group(1))]
    return list(rels.values())


def extract_batch(texts: list[str], titles: list[str] | None = None, authors: list[str] | None = None,
                  teams=(), kind: str = "") -> list[dict]:
    """Entities per text (GLiNER, batched), then relations per sentence window (GLiNER plus patterns, batched). `titles` and
    `authors` give each text's document context (`teams`: team names already known): "Decided by" targets the title's ADR id, "I own X" names the author."""
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
    authors = authors or [""] * len(texts)
    raw = run(texts, _schema(m, True), 4)
    # team names are crisp once known: the ones this batch (one document) gives away, plus those the caller already knows
    known = set(teams or ()) | set().union(*(team_names(t) for t in texts))
    known |= {i["text"] for r in raw for i in r.get("entities", {}).get("team", [])
              if i["confidence"] >= ENTITY_CONF["team"] and re.fullmatch(r"[A-Z][a-z]+", i["text"])} - _NOT_TEAM
    ents = [_entities(r, t, ti, a, known) for r, t, ti, a in zip(raw, texts, titles, authors)]
    for e in ents:  # "Kofi" alone is a first name, whatever else the model made of it
        names = {w for k, x in e.items() if x["type"] == "person" for w in k.split()}
        for k in [k for k, x in e.items() if x["type"] == "team" and k in names]:
            del e[k]
    wins = [_windows(t) for t in texts]
    flat = [w for ws, _ in wins for w in ws]
    glr = run(flat, _schema(m, False), 16) if flat else []
    out, i = [], 0
    for e, (ws, sp), t, ti, a in zip(ents, wins, texts, titles, authors):
        rels = _relations(e, ws, glr[i:i + len(ws)], ti, a, sp, kind=kind)
        i += len(ws)
        seen = {(normalize_key(r["head"]), r["type"], normalize_key(r["tail"])) for r in rels}
        for who, rt, thing, _, _ in _table_facts(t):
            if (normalize_key(who), rt, normalize_key(thing)) not in seen:
                rels.append({"head": who, "type": rt, "tail": thing, "conf": 0.9})
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
