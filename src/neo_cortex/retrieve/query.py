"""Query parsing: GLiNER entities and soft intent, regex time windows."""
import datetime as dt
import re

from .. import models
from ..util import now_ms as _now_ms

# Descriptive labels: bare labels misroute (spike 2026-10-16). Keys are the contract entity types.
ENTITY_LABELS = {
    "person": "a person's name", "team": "a team, group or department", "service": "a software service, API or system",
    "component": "a module, library, cache or database", "file": "a file path or file name",
    "config_setting": "a configuration setting or environment variable", "ticket": "a ticket, issue or pull request id",
    "customer": "a customer or client company", "product": "a product or feature", "tool": "a developer tool or platform",
    "incident": "an outage, incident or failure event", "decision": "a decision or architecture decision record",
}
INTENT_LABELS = {
    "fact": "asks for a single fact or definition",
    "connection": "asks how two or more things are connected or related",
    "temporal": "asks what changed over time, or when something happened",
    "owner": "asks who is responsible, owns, approved or knows most about something",
    "howto": "asks how to do a task or follow a procedure",
}

_MON = "january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec"
_MONTHS = {m: i for i, m in enumerate(_MON.split("|")[:12], 1)}
_MONTHS.update({"jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8, "sept": 9, "sep": 9, "oct": 10, "nov": 11, "dec": 12})
_EXPR = re.compile(
    rf"\b(?:(?P<mod>since|after|from|before|until|till|in)\s+)?(?:(?P<iso>\d{{4}}-\d{{2}}-\d{{2}})"
    rf"|(?P<rel>yesterday|last\s+(?:week|month|year)|(?:last|past)\s+\d+\s+(?:day|week|month|year)s?)"
    rf"|(?P<mon>{_MON})(?:\s+(?P<yr>\d{{4}}))?)\b", re.I)
_BETWEEN = re.compile(r"\bbetween\s+(\d{4}-\d{2}-\d{2})\s+and\s+(\d{4}-\d{2}-\d{2})\b", re.I)
_DAY = 86_400_000
_UNIT = {"day": 1, "week": 7, "month": 30, "year": 365}


def _ms(d: dt.date) -> int:
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp() * 1000)


def parse_time(q: str, now_ms: int | None = None) -> tuple[int | None, int | None]:
    """Window [since, until) in epoch ms from ISO dates, 'since/before/after <date>', 'in <Month> [year]',
    'last week/month/year', 'last N days', 'yesterday'. Several expressions intersect. "today/now/current/latest" are
    recency cues for the temporal channel (`channels.RECENT_RE`), never windows."""
    now = now_ms if now_ms is not None else _now_ms()
    today = _ms(dt.datetime.fromtimestamp(now / 1000, dt.timezone.utc).date())
    since, until = [], []
    if m := _BETWEEN.search(q):
        since.append(_ms(dt.date.fromisoformat(m[1])))
        until.append(_ms(dt.date.fromisoformat(m[2])) + _DAY)
        q = q[:m.start()] + q[m.end():]
    for m in _EXPR.finditer(q):
        mod = (m["mod"] or "").lower()
        if m["iso"]:
            try:
                s = _ms(dt.date.fromisoformat(m["iso"]))
            except ValueError:
                continue
            u = s + _DAY
        elif m["rel"]:
            r = m["rel"].lower().split()
            if r[0] == "yesterday":
                s, u = today - _DAY, today
            else:
                n, unit = (1, r[1]) if r[1] in _UNIT else (int(r[1]), r[2].rstrip("s"))
                s, u = now - n * _UNIT[unit] * _DAY, now
        else:
            if not mod and not m["yr"]:  # bare "may" is a verb
                continue
            mon = _MONTHS[m["mon"].lower()]
            nd = dt.datetime.fromtimestamp(now / 1000, dt.timezone.utc)
            yr = int(m["yr"]) if m["yr"] else nd.year - (mon > nd.month)
            s = _ms(dt.date(yr, mon, 1))
            u = _ms(dt.date(yr + (mon == 12), mon % 12 + 1, 1))
        if mod in ("since", "from"):
            since.append(s)
        elif mod == "after":
            since.append(u)
        elif mod in ("before", "until", "till"):
            until.append(s)
        else:
            since.append(s)
            until.append(u)
    return (max(since) if since else None, min(until) if until else None)


def _conf(x):
    return x["confidence"] if isinstance(x, dict) else 1.0


def _text(x):
    return x["text"] if isinstance(x, dict) else x


def parse_query(q: str, now_ms: int | None = None, nlp: bool = True) -> dict:
    """{entities: [{name, type, conf}], intent: {fact|connection|temporal|owner|howto: conf}, since_ms, until_ms}.
    Intent confidences are independent (multi-label sigmoid), used as soft channel weights. nlp=False skips GLiNER."""
    since, until = parse_time(q, now_ms)
    ents, intent = [], {}
    if nlp:
        g = models.gliner()
        labels = {t.replace("_", " "): d for t, d in ENTITY_LABELS.items()}
        r = g.extract_entities(q, labels, threshold=0.35, include_confidence=True)["entities"]
        seen = set()
        for label, items in r.items():
            for it in items:
                name = _text(it).strip()
                if name.lower() not in seen:
                    seen.add(name.lower())
                    ents.append({"name": name, "type": label.replace(" ", "_"), "conf": float(_conf(it))})
        back = {d: k for k, d in INTENT_LABELS.items()}
        r = g.classify_text(q, {"intent": {"labels": list(INTENT_LABELS.values()), "multi_label": True, "cls_threshold": 0.0}},
                            include_confidence=True)["intent"]
        for it in (r if isinstance(r, list) else [r]):
            intent[back[it["label"]]] = float(it["confidence"])
    return {"entities": ents, "intent": intent, "since_ms": since, "until_ms": until}
