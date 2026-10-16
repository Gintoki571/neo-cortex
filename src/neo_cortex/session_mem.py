"""Candidate memories from a Claude Code transcript. Deterministic patterns pick and normalise the candidates;
GLiNER (`worth_keeping`, `classify_memory`) only scores and types them. Pure functions plus `select`; `write.ingest_session` stores them.

A memory must be a self-contained statement a future agent can act on without the transcript, so fragments, planning
chatter, questions, headings and dangling "It/This ..." sentences never become candidates."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from . import extract as X

MAX_MEMORIES, MAX_PREFS = 15, 5
MIN_WORDS, MAX_WORDS = 8, 60
OUTCOME_WORTH = 0.55  # outcomes need this GLiNER worth_keeping; patterns (preference/decision/lesson) do not
_NOISE = re.compile(r"<(system-reminder|local-command-[a-z]+|command-[a-z]+|task-notification|agent-message)[^>]*>.*?</\1>", re.S)
_CODE = re.compile(r"```.*?```", re.S)


def _ts(v) -> int | None:
    try:
        return int(datetime.fromisoformat(str(v).replace("Z", "+00:00")).astimezone(timezone.utc).timestamp() * 1000)
    except ValueError:
        return None


# ---------------------------------------------------------------- transcript -> events

def read_transcript(path: Path) -> tuple[dict, list[dict]]:
    """(meta, events). Event kinds: user, assistant (text blocks), tool (tool_use), error (failed tool_result), ok (tool_result).
    Meta, sidechain, thinking, hook/command noise and sub-agent hand-backs are dropped. A line with bad JSON or a field of
    an unexpected type is skipped whole."""
    meta, ev, calls = {}, [], {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        new = []  # committed only when the whole line parses
        try:
            d = json.loads(line)
            for k, f in (("session_id", "sessionId"), ("cwd", "cwd")):
                if d.get(f) and k not in meta:
                    meta[k] = d[f]
            if d.get("timestamp") and "started" not in meta:
                meta["started"] = d["timestamp"]
            m, t = d.get("message"), d.get("type")
            if t not in ("user", "assistant") or d.get("isMeta") or d.get("isSidechain") or not isinstance(m, dict):
                continue
            c, ts = m.get("content"), _ts(d.get("timestamp"))
            for b in [{"type": "text", "text": c}] if isinstance(c, str) else [b for b in c or [] if isinstance(b, dict)]:
                bt = b.get("type")
                if bt == "text":
                    s = _CODE.sub("\n", _NOISE.sub("\n", b.get("text") or "")).strip()
                    if s and not s.startswith(("[Request interrupted", "Another Claude session", "Caveat:")):
                        new.append({"k": t, "text": s, "ts": ts})
                elif bt == "tool_use":
                    inp = b.get("input") or {}
                    calls[b.get("id")] = str(inp.get("command") or inp.get("file_path") or inp.get("pattern") or b.get("name"))
                    new.append({"k": "tool", "ts": ts})
                elif bt == "tool_result":
                    body = b.get("content")
                    body = "\n".join(x.get("text", "") for x in body if isinstance(x, dict)) if isinstance(body, list) else str(body or "")
                    new.append({"k": "error" if b.get("is_error") else "ok", "text": body, "ts": ts,
                                "cmd": calls.get(b.get("tool_use_id"), "")})
        except (ValueError, TypeError, AttributeError):  # bad JSON, or a field of an unexpected type
            continue
        ev += new
    return meta, ev


# ---------------------------------------------------------------- text -> sentence units

_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z`\"'(\[])")
_ABBR = re.compile(r"(?:\b(?:e\.g|i\.e|vs|approx|cf)\.|\b[A-Z]\.)$")
_IMPERATIVE_START = re.compile(r"(?:add|use|run|try|consider|see|note|make|set|keep|restart|install|open|ask|tell|pass|call)\b", re.I)
_PRONOUN = re.compile(r"\b(?:i|me|my|it|its|this|that|these|those|both|they|them|their|you|your|following|above|below)\b", re.I)
_DANGLING = re.compile(r"(?:since then|after that|meanwhile|afterwards|in the meantime|to unblock|it|its|this|that|these|those|they|them|their|both|also|and|but|so|then|however|which|such|"
                       r"the (?:latter|former|same|above|first|second|other|worker|workers|subagent|subagents)|another)\b", re.I)


def _clean(s: str) -> str:
    s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\*\*|__", "", s)
    s = re.sub(r"(?<![\w*])\*(\S[^*]*?)\*(?![\w*])", r"\1", s)
    return re.sub(r"\s+", " ", s).strip(" \t>")


def _split(s: str) -> list[str]:
    out = []
    for p in _SPLIT.split(s):
        if out and _ABBR.search(out[-1]):
            out[-1] += " " + p
        else:
            out.append(p)
    return out


def _items(text: str) -> list[tuple[str, str]]:
    """(kind, text) per heading, bullet or paragraph; tables and rules are dropped."""
    items, cur = [], None
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("|") or re.fullmatch(r"[-=*_ ]{3,}", s):
            cur = None
            continue
        if m := re.match(r"#{1,6}\s+(.*)", s):
            items.append(["head", m[1]])
            cur = None
        elif m := re.match(r"(?:[-*•]|\d+[.)])\s+(.*)", s):
            items.append(["bullet", m[1]])
            cur = items[-1]
        elif cur:
            cur[1] += " " + s
        else:
            items.append(["para", s])
            cur = items[-1]
    return [(k, s) for k, s in items]


def units(text: str) -> list[str]:
    """Sentence units that read on their own: a lead-in ending with ':' is merged into its bullets, a dangling sentence
    ('It sits alongside ...') takes the previous sentence, and what cannot be made standalone is dropped. Headings are dropped."""
    out, lead, lead_bad = [], None, False
    for kind, raw in _items(text):
        s = _clean(raw)
        if not s:
            continue
        if kind == "head" or s.endswith(":") or (kind == "para" and len(s.split()) <= 6 and not s.endswith((".", "!", "?"))):
            lead = None  # headings and short labels are dropped
            if kind != "head" and s.endswith(":"):  # a lead-in that points at something unseen ("it adds:") cannot be merged, its bullets are dropped
                lead = s.rstrip(":")
                lead_bad = bool(_PRONOUN.search(lead)) or not 3 <= _words(lead) <= 25
            continue
        if kind == "para":
            lead = None
        if kind == "bullet" and lead and (lead_bad or not _VERB.search(s)):  # a bare noun phrase under a lead-in is a fragment
            continue
        sents = []
        for x in _split(s):  # a short label sentence ("No LLM inside the system.") belongs to its elaboration
            if sents and _words(sents[-1]) < 5 and not _CHATTER.match(sents[-1]):
                sents[-1] += " " + x
            else:
                sents.append(x)
        for i, u in enumerate(sents):
            if _DANGLING.match(u):  # its antecedent can only be the previous sentence, and only if that one stands alone
                if not i or _DANGLING.match(sents[i - 1]):
                    continue
                u = sents[i - 1] + " " + u
            elif i == 0 and kind == "bullet" and lead and not lead_bad:
                u = lead + ": " + u
            out.append(u)
    return out


def _words(s: str) -> int:
    return len(s.split())


def _trim(u: str) -> str | None:
    """Cap at 60 words by cutting at the last clause boundary before the cap (a cut under 12 words is rejected)."""
    if _words(u) <= MAX_WORDS:
        return u
    cut = " ".join(u.split()[:MAX_WORDS])
    k = max(cut.rfind("; "), cut.rfind(", "))
    return cut[:k].rstrip(" ,;") + "." if k > 0 and _words(cut[:k]) >= 12 else None


# ---------------------------------------------------------------- filters and rewriting

_CHATTER = re.compile(r"(?:i'll|i will|i'm (?:going|now|about|still|checking|running|waiting)|i am (?:going|now)|i can|i should|i need|"
                      r"i want|i'd|let me|let's|lets|now\b|next\b|first,|okay|ok\b|sure\b|great|good\b|thanks|thank you|here(?:'s| is| are)|"
                      r"looking|checking|running|waiting|launching|setting uping|reading|updating|re-?running|still (?:running|waiting)|"
                      r"done\b|all (?:set|done)|status:|now,)", re.I)
_EPHEMERAL = re.compile(r"\b(?:still (?:running|waiting|to come)|(?:is|are) (?:now |currently )?(?:running|working|waiting|being)|until it lands|as soon as|"
                        r"will (?:review|come|report|start|use)|when both report|here is the summary|come once|not done yet|so far|"
                        r"(?:is|are) on schedule|behind the plan)\b|/tmp/", re.I)
_UNRESOLVED = re.compile(r"\b(?:them|they|their|these|those|the (?:old|new|other) one|the latter|the former|me)\b", re.I)
_ADDRESSED = re.compile(r"\b(?:you|you're|you'll|let me know|want me to|shall i|feel free|sorry)\b", re.I)
_CONCRETE = re.compile(r"\d|[\w./-]+\.(?:py|md|json|toml|ya?ml|sh|ts|rdb|jsonl)\b|`[^`]+`|(?<=\s)/[\w.-]+|[A-Za-z]+[-_][A-Za-z]+|(?<=[a-z,;)] )[A-Z][a-zA-Z0-9]{2,}")


_VERB = re.compile(r"\b(?:is|are|was|were|be|been|has|have|had|does|do|did|can|could|will|would|should|must|may|\w{3,}ed|ran|wrote|found|"
                   r"made|got|built|took|kept|left|chose|"
                   r"(?:come|work|return|run|use|take|give|need|mean|make|find|show|keep|get|set|read|write|fail|pass|support|require|handle|send|"
                   r"load|store|ignore|beat|read|sit|add|go|cause|let|start|build|check|honor|wipe|reload)s?)\b", re.I)


def _standalone(u: str) -> bool:
    return bool(_VERB.search(u)) and not re.match(r"(?:why|how|what|which|who|when|where)\b", u, re.I) and not (u.endswith(("?", ":")) or "?" in u or _words(u) < MIN_WORDS or sum(not c.isalnum() and c not in " .,'-`/_" for c in u) > len(u) * 0.2)


_PAST = re.compile(r"(?:\w+ed|did|didn't|did not|was|wasn't|ran|wrote|found|made|saw|set|read|got|built|took|kept|left|put|chose|"
                   r"switched|used|had|hadn't|couldn't|could|would|measured|"
                   r"have|haven't|am|will|won't|can|can't|cannot)\b")


def _third_person(u: str) -> str | None:
    """The agent authors assistant text: 'I added X' -> 'The agent added X'. A present-tense 'I think/understand' is
    dropped (None) because 'the agent understand' would be wrong and such sentences are opinion anyway."""
    for m in re.finditer(r"\bI\b(?!')\s+(?:(?:also|then|still|now|just|already|only|first|later|never)\s+)*(\w+)", u):
        if not _PAST.match(m[1]):
            return None
    for a, b in ((r"I've", "has"), (r"I'm", "is"), (r"I'd", "would"), (r"I'll", "will")):
        u = re.sub(rf"^{a}\b", "The agent " + b, u)
        u = re.sub(rf"\b{a}\b", "the agent " + b, u)
    u = re.sub(r"^I\b", "The agent", u)
    u = re.sub(r"\bI\b", "the agent", u)
    u = re.sub(r"\bmy\b", "the agent's", re.sub(r"\bour\b", "the project's", u))
    return re.sub(r"\byour\b", "the user's", u)


def _sentence(u: str) -> str:
    u = re.sub(r"(?:\s*\.)+$", ".", u.strip())
    if re.match(r"[a-z]+\b(?![-_./`(])", u):  # "use X" -> "Use X", but identifiers such as pg-jev keep their case
        u = u[:1].upper() + u[1:]
    return u + ("" if u.endswith((".", "!", "`", ")")) else ".")


def features(u: str) -> float:
    return 0.1 * bool(re.search(r"\d", u)) + 0.1 * bool(re.search(r"[\w-]+\.\w{2,4}\b|/\w", u)) + 0.1 * ("`" in u) \
        + 0.05 * bool(re.search(r"[a-z,] [A-Z][A-Za-z]{2,}", u))


# ---------------------------------------------------------------- pattern candidates

_FILLER = re.compile(r"^(?:okay|ok|also|and|so|then|please|now|well|btw|just|i think|i want you to|i also want you to|"
                     r"i would like you to|you need to|you should|you must|we should|remember to|remember that)\b[,\s]*", re.I)
_PREF = re.compile(r"\b(?:(?<!it )(?<!they )(?<!that )always|never|(?:i|we) (?:want|would like|prefer)|don'?t|do not|doesn'?t|stop|avoid|prefer|rather than|instead of|only (?:when|if|use)|absolutely|"
                   r"must not|mustn'?t|shouldn'?t|no more|make sure|be sure|keep in mind|from now on|going forward|every time|by default|"
                   r"act as|and not|but not|without)\b", re.I)
_IMPERATIVE = re.compile(r"^(?:use|keep|prefer|stick to|ensure|follow|avoid|remember|treat|tell the)\b", re.I)
_CORRECT = re.compile(r"^(?:no\b|nope|not |wrong|that'?s (?:not|wrong)|actually|wait|you (?:should|shouldn'?t|forgot|didn'?t|missed)|stop|instead)", re.I)
_DECISION = re.compile(r"\b(?:decided|decision (?:is|was)|chose|chosen|go(?:ing)? (?:with|for)|settled on|opted (?:for|to)|"
                       r"switched to|dropped|we(?:'ll| will) use)\b", re.I)
_REASON_IN = re.compile(r"\b(?:because|since|so that|to avoid|as it|which (?:is|keeps|avoids|lets))\b", re.I)
_REASON_NEXT = re.compile(r"^(?:because|since|reason|this (?:is|keeps|avoids|lets|means)|that (?:way|is why)|it (?:needs|avoids|keeps))\b", re.I)
_LESSON = re.compile(r"\b(?:the (?:root )?cause (?:was|is)|root cause|the (?:issue|problem|bug) (?:was|is)|turned out|fixed (?:it )?by|"
                     r"the fix (?:is|was)|workaround|(?:failed|fails|failing|broke|broken) because|doesn'?t work (?:because|unless))\b", re.I)
_EXPLAIN = re.compile(r"\b(?:because|cause|issue|problem|missing|wrong|not (?:found|installed|available|supported)|doesn'?t|isn'?t|"
                      r"needs?|must|instead|requires?)\b", re.I)


_PAST_EVENT = re.compile(r"\b(?:\w{3,}ed|was|were|ran|wrote|made|found|chose|got|built|took|kept|left|did|had|began|went|came|gave|sent)\b", re.I)


def _cand(text, kind, ts, role, conf, rank):
    return {"text": text, "kind": kind, "ts": ts, "role": role, "conf": conf, "rank": rank}


def user_candidates(ev: list[dict]) -> list[dict]:
    """Preferences and corrections, in the user's words (fillers stripped, capitalised, ending in a full stop)."""
    out = []
    for i, e in enumerate(ev):
        if e["k"] != "user":
            continue
        prev_action = i and ev[i - 1]["k"] in ("assistant", "tool", "ok", "error")
        us = [u for u in units(e["text"]) if "?" not in u]
        if prev_action and _words(e["text"]) <= 40 and _CORRECT.match(e["text"].strip()) and "?" not in e["text"]:
            us = [" ".join(_split(_clean(e["text"]))[:2])]  # a correction right after an assistant action
        for u in us:
            n = _FILLER.sub("", u)
            n = _FILLER.sub("", n)
            if not 4 <= _words(n) <= 40 or "http" in n or re.match(r"(?:your|the) (?:goal|task|job)\b", n, re.I) or not (_PREF.search(n) or _IMPERATIVE.match(n) or _CORRECT.match(u)) or (t := _trim(_sentence(n))) is None:
                continue
            out.append(_cand(t, "preference", e["ts"], "user", 0.8, 0))
    return out


def pattern_candidates(ev: list[dict]) -> list[dict]:
    """Decisions (either side) with their reason, lessons from 'the cause was / fixed by', and tool-error explanations."""
    out = []
    for i, e in enumerate(ev):
        if e["k"] in ("user", "assistant"):
            us = units(e["text"])
            for j, u in enumerate(us):
                if "?" in u or _words(u) < 6:
                    continue
                src = _third_person(u) if e["k"] == "assistant" else u
                if src is None:
                    continue
                if _DECISION.search(u) and not _ADDRESSED.search(u):
                    if not _REASON_IN.search(u) and j + 1 < len(us) and _REASON_NEXT.match(us[j + 1]):
                        src += " " + ((_third_person(us[j + 1]) or "") if e["k"] == "assistant" else us[j + 1])
                    if t := _trim(_sentence(src)):
                        out.append(_cand(t, "decision", e["ts"], e["k"], 0.8, 1))
                elif e["k"] == "assistant" and _LESSON.search(u) and not _ADDRESSED.search(u):
                    if j + 1 < len(us) and re.match(r"(?:the )?fix\b|fixed\b", us[j + 1], re.I):
                        src += " " + (_third_person(us[j + 1]) or "")
                    if t := _trim(_sentence(src)):
                        out.append(_cand(t, "procedural", e["ts"], "assistant", 0.7, 1))
        elif e["k"] == "error":
            t = _error_lesson(ev, i)
            if t:
                out.append(_cand(t, "procedural", e["ts"], "assistant", 0.6, 1))
    return out


_ERRLINE = re.compile(r"error|exception|traceback|not found|no such|failed|denied|syntax|invalid|unexpected|cannot|can't|refused|timed? ?out|unknown|unrecognized|not (?:a|an|supported|installed)", re.I)
_GENERIC = {"that", "this", "with", "from", "when", "which", "there", "their", "error", "failed", "because", "should", "would", "could", "have",
            "what", "does", "doesn't", "isn't", "needs", "must", "instead", "problem", "issue", "cause", "missing", "wrong", "requires", "command"}


def _error_lesson(ev: list[dict], i: int) -> str | None:
    """'When `cmd` failed with "err", <explanation>' when the assistant explains the failure within the next few events
    (the explanation shares a word with the command or error, so it is about this failure) and a later step succeeded.
    Bare exit codes, plain stdout and user rejections are not lessons."""
    err = next((ln.strip() for ln in ev[i]["text"].splitlines() if _ERRLINE.search(ln) and len(ln) < 160), "")
    if not err or re.search(r"doesn't want|rejected|interrupted|permission", err, re.I):
        return None
    j = i + 1
    while j < len(ev) and ev[j]["k"] == "assistant":  # the explanation comes right after the failure, before the next tool call
        j += 1
    window, rest = ev[i + 1:j], ev[j:j + 8]
    if not any(w["k"] == "ok" for w in rest[:next((n for n, w in enumerate(rest) if w["k"] == "user"), len(rest))]):
        return None
    segs = [x.strip() for x in re.split(r"&&|;|\n|\|", ev[i]["cmd"]) if x.strip() and not re.match(r"(?:(?:cd|export|mkdir|echo|set|source)\b|\w+=)", x.strip())]
    cmd = segs[0][:60] if segs else ""
    ctx = {w for w in re.findall(r"[a-z][\w.-]{3,}", (cmd + " " + err).lower()) if w not in _GENERIC and "/" not in w}
    for w in window:
        if w["k"] != "assistant":
            continue
        for u in units(w["text"]):
            if _EXPLAIN.search(u) and _words(u) >= 6 and "?" not in u and not _ADDRESSED.search(u) and not _CHATTER.match(u) \
                    and ctx & {x for x in re.findall(r"[a-z][\w.-]{3,}", u.lower()) if x not in _GENERIC} and (tp := _third_person(u)):
                return _trim(_sentence(f"When `{cmd or 'a command'}` failed with \"{err[:80]}\", {tp[:1].lower() + tp[1:]}"))
    return None


def outcome_candidates(ev: list[dict]) -> list[dict]:
    """Concrete statements from the assistant's closing text of each turn (the text after its last tool call)."""
    out = []
    for i, e in enumerate(ev):
        if e["k"] != "assistant":
            continue
        nxt = next((x["k"] for x in ev[i + 1:] if x["k"] != "assistant"), "user")
        if nxt != "user" and _words(e["text"]) < 60:  # mid-turn text is narration unless it is a summary
            continue
        for u in units(e["text"]):
            if _standalone(u) and not _CHATTER.match(u) and not _ADDRESSED.search(u) and not _EPHEMERAL.search(u) and not _UNRESOLVED.search(u) and not _IMPERATIVE_START.match(u) and _CONCRETE.search(u):
                if (tp := _third_person(u)) and (x := _trim(_sentence(tp))):
                    out.append(_cand(x, "episodic", e["ts"], "assistant", 0.0, 2))
    return out


# ---------------------------------------------------------------- selection

def _tok(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2}


def _same(a: set[str], b: set[str]) -> bool:
    return bool(a and b) and len(a & b) / min(len(a), len(b)) >= 0.75


def select(ev: list[dict]) -> list[dict]:
    """Best candidates: user preferences first (up to 5), then the highest-scored decisions, lessons and outcomes (15 in total).
    Near-duplicates keep the higher-ranked one; each candidate gets `score` and, for outcomes, a GLiNER-typed `kind`."""
    cands = user_candidates(ev) + pattern_candidates(ev) + outcome_candidates(ev)
    if not cands:
        return []
    texts = [c["text"] for c in cands]
    for c, w in zip(cands, X.worth_keeping_batch(texts)):
        c["score"] = round(w + features(c["text"]) + (0.3 if c["kind"] == "preference" else 0.15 if c["rank"] == 1 else 0), 4)
        c["worth"] = w
    cands = [c for c in cands if c["worth"] + features(c["text"]) >= (OUTCOME_WORTH if c["rank"] == 2 else 0.3 if c["rank"] == 1 else 0)]
    kept, seen = [], []
    for c in sorted(cands, key=lambda c: (c["rank"] > 0 and c["kind"] != "preference", c["rank"], -c["score"])):
        tk = _tok(c["text"])
        if not any(_same(tk, s) for s in seen):
            kept.append(c)
            seen.append(tk)
    prefs = [c for c in kept if c["kind"] == "preference"][:MAX_PREFS]
    rest = sorted((c for c in kept if c["kind"] != "preference"), key=lambda c: -c["score"])[:MAX_MEMORIES - len(prefs)]
    out = prefs + rest
    typed = [c for c in out if c["rank"] == 2]
    for c, (k, conf) in zip(typed, X.classify_memory_batch([c["text"] for c in typed])):
        # an event needs a past-tense marker; a present-tense statement is a fact whatever GLiNER says
        c["kind"], c["conf"] = (k, conf) if k in ("semantic", "procedural") else ("episodic" if _PAST_EVENT.search(c["text"]) else "semantic", conf)
    return out
