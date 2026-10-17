"""Entity resolution: exact key, alias, vector nearest neighbour, then a cached GLiNER yes/no judge for borderline pairs.

Finding: GLiNER2.5-base is close to chance as a same-entity judge on bare names (it says "same" for Noor/Samir Haddad), so
a fuzzy merge needs a lexical guard first (same words up to plurals, or a head/tail name part) and the judge may only veto.
"""
import json
import re

import numpy as np

from .models import embed_docs
from .util import content_hash, new_id, normalize_key, now_ms

HARD = 0.92   # vector similarity at or above which a lexically guarded pair merges without asking
SOFT = 0.85   # between SOFT and HARD the cached judge decides
JUDGE_NO = 0.5  # the base model is a weak judge: it may only veto a borderline merge, never create one
_RANK = {"person": 9, "team": 8, "customer": 7, "service": 6, "ticket": 6, "incident": 6, "decision": 6, "tool": 5,
         "config_setting": 4, "file": 4, "component": 3, "product": 3, "other": 0}
_SAME = ["same", "different"]
# pin of a type vote: a GLiNER confidence < a regex or code-structure match < a caller-given or frontmatter type
PIN_VOTE, PIN_REGEX, PIN_EXPLICIT = 0, 1, 2


def judge(store, question: str, text: str, labels: list[str], tenant=None) -> dict[str, float]:
    """GLiNER choice probabilities, cached as a Judgment node keyed by the content hash (pg-jev idea)."""
    jid = content_hash("\x1f".join([question, text, *labels]))
    rows = store.query("MATCH (j:Judgment {id:$i}) RETURN j.result", {"i": jid}, tenant)
    if rows:
        return json.loads(rows[0][0])
    from .extract import _softmax_labels
    res = {k: round(v, 4) for k, v in _softmax_labels(f"{question} {text}".strip(), "judge", labels).items()}
    store.query("MERGE (j:Judgment {id:$i}) SET j.question=$q, j.result=$r, j.created_ms=$t",
                {"i": jid, "q": question, "r": json.dumps(res), "t": now_ms()}, tenant)
    return res


_SIZE = re.compile(r"[\W_]+(?:base|large|small|tiny|medium|hf)$")  # "GLiNER2.5 base", "gliner-2.5-hf"
_VER = re.compile(r"[\W_]+v[01]$")                                 # "gliner2.5-base-v1"; "api v2" is a different version, kept apart


# code identifiers: snake_case, a call, a dotted attribute (not a version such as 2.5), camelCase
_CODE = re.compile(r"_|\(|[A-Za-z]\.[A-Za-z]|^[a-z]+[A-Z]")


def is_code(name: str) -> bool:
    """A code identifier ("_sentences", "parse_tree()", "os.path", "parseTree"). It merges only on the exact key or an alias:
    "_sentences" is not "_sentence", and "_hard_split" is not "_split"."""
    return bool(_CODE.search(name.strip()))


def variant_key(key: str) -> str:
    """Spelling variant of a normalised key: spacing, case and punctuation dropped, letters and digits as separate tokens
    ("GLiNER 2.5" = "gliner2.5" = "gliner-2.5"), and a trailing size or version word dropped ("base", "large", "hf", "v1").
    Different products stay apart: "gliner 2 5" is not "gliner 2" nor "gliner 25" nor "gliner 2 5 decide"."""
    s = key
    while True:  # shortcut: only trailing size/version words are dropped; "auth-gateway" keeps its tail
        t = _SIZE.sub("", s) if _SIZE.search(s) else _VER.sub("", s)
        if t == s:
            break
        s = t
    return " ".join(re.findall(r"[^\W\d_]+|\d+", s))


def _stem(key: str) -> list[str]:
    """Words with a plural "s" dropped; not after a digit ("bm25s", "k8s" are names, not plurals)."""
    return [t[:-1] if len(t) > 3 and t.endswith("s") and not t[-2].isdigit() else t for t in key.split()]


def _guard(a: str, b: str, ta: str, tb: str) -> bool:
    """Lexical preconditions for a fuzzy merge of keys a and b: same words up to plurals, or a short name that is the
    tail ("gateway" / "api gateway") or, for orgs and services, the head ("tidewater" / "tidewater credit union")."""
    if "person" in (ta, tb) and ta != tb and "other" not in (ta, tb):
        return False
    if re.findall(r"\d+", a) != re.findall(r"\d+", b):
        return False
    sa, sb = _stem(a), _stem(b)
    if sa == sb:
        return True
    if "person" in (ta, tb):  # Noor Haddad / Samir Haddad stay apart
        return False
    s, l = (sa, sb) if len(sa) < len(sb) else (sb, sa)
    if len(l) > 4 or s == l:
        return False
    if l[-len(s):] == s:
        return True
    return l[:len(s)] == s and (bool({ta, tb} & {"customer", "team"}) or l[len(s):] == ["service"])


def _winner(votes: dict) -> str:
    """Highest pin, then largest summed confidence, then _RANK. "other" counts only when no other type has a vote."""
    real = {t: v for t, v in votes.items() if t != "other"} or votes
    return max(real, key=lambda t: (real[t][1], real[t][0], _RANK.get(t, 0)))


def _vote(store, eid, typ, weight, pin, tenant):
    """Add one typed vote to an entity and reset its type to the winner. `type_votes` is JSON {type: [weight, pin]};
    an entity written before votes existed counts its stored type as one vote of weight 1."""
    old_type, old_votes = store.query("MATCH (e:Entity {id:$i}) RETURN e.type, e.type_votes", {"i": eid}, tenant)[0]
    votes = json.loads(old_votes) if old_votes else {old_type: [1.0, PIN_VOTE]}
    w, p = votes.get(typ, [0.0, PIN_VOTE])
    votes[typ] = [round(w + weight, 4), max(p, pin)]
    store.query("MATCH (e:Entity {id:$i}) SET e.type=$t, e.type_votes=$v",
                {"i": eid, "t": _winner(votes), "v": json.dumps(votes)}, tenant)


def _add_alias(store, eid, key, tenant):
    store.query("MATCH (e:Entity {id:$i}) WHERE e.key <> $k AND NOT $k IN e.aliases SET e.aliases = e.aliases + [$k]",
                {"i": eid, "k": key}, tenant)


def resolve_entity(store, name: str, type: str, emb=None, tenant=None, weight=1.0, pin=PIN_VOTE) -> str | None:
    """Return the id of the Entity for `name`, creating it when nothing matches (None for an ambiguous lone surname
    or a name with no letters or digits). `emb` skips re-embedding; `weight` and `pin` are this mention's type vote."""
    key = normalize_key(name)
    if not key:
        return None
    q = lambda c, p: store.query(c, p, tenant)  # noqa: E731
    r = q("MATCH (e:Entity {key:$k}) RETURN e.id", {"k": key})
    if not r:
        r = q("MATCH (e:Entity) WHERE $k IN e.aliases RETURN e.id", {"k": key})
    if r:
        _vote(store, r[0][0], type, weight, pin, tenant)
        return r[0][0]
    code = is_code(name)
    fuzzy = not code and pin != PIN_EXPLICIT  # caller-given names (remember entities/relations, relate) merge by exact key or alias only
    if " " not in key and type in ("person", "team", "other") and not code:  # a lone first or last name: the unique matching person
        r = q("MATCH (e:Entity {type:'person'}) WHERE e.key STARTS WITH $p OR e.key ENDS WITH $s RETURN e.id",
              {"p": key + " ", "s": " " + key})
        if len(r) == 1 and fuzzy:
            _add_alias(store, r[0][0], key, tenant)
            return r[0][0]
        if len(r) > 1 and type == "person":  # "Haddad" with two Haddads: ambiguous, so no entity at all
            return None
    vk = variant_key(key)
    if vk and vk[0].isalpha() and fuzzy:  # spelling variant of an existing entity: same letters-first prefix, same variant key
        for cid, ckey in q("MATCH (e:Entity) WHERE e.key STARTS WITH $p RETURN e.id, e.key", {"p": vk.split()[0]}):
            if variant_key(ckey) == vk:
                _add_alias(store, cid, key, tenant)
                _vote(store, cid, type, weight, pin, tenant)
                return cid
    if emb is None:
        emb = embed_docs([name])[0]
    cand = [] if not fuzzy else q("CALL db.idx.vector.queryNodes('Entity','emb',4,vecf32($e)) YIELD node, score "
                             "RETURN node.id, node.key, node.type, 1 - score ORDER BY score", {"e": np.asarray(emb).tolist()})
    for cid, ckey, ctype, sim in cand:
        if sim < SOFT or not _guard(key, ckey, type, ctype):
            continue
        if sim >= HARD or judge(store, "", f"{name} = {ckey} ?", _SAME, tenant).get("same", 0) >= JUDGE_NO:
            _add_alias(store, cid, key, tenant)
            _vote(store, cid, type, weight, pin, tenant)
            return cid
    eid, t = new_id("ent"), now_ms()
    q("CREATE (:Entity {id:$i, key:$k, name:$n, type:$t, type_votes:$v, aliases:[], emb:vecf32($e), first_seen_ms:$ts, "
      "last_seen_ms:$ts, mentions:0})", {"i": eid, "k": key, "n": name, "t": type, "v": json.dumps({type: [weight, pin]}),
                                         "e": np.asarray(emb).tolist(), "ts": t})
    return eid


def resolve_many(store, items: list[tuple], tenant=None) -> list[str | None]:
    """Resolve (name, type) or (name, type, weight, pin) items; names with no exact-key hit are embedded in one batch."""
    items = [(*it, 1.0, PIN_VOTE)[:4] for it in items]  # a (name, type) item is one GLiNER-style vote of weight 1
    keys = list({normalize_key(n) for n, *_ in items})
    known = {r[0] for r in store.query("MATCH (e:Entity) WHERE e.key IN $ks RETURN e.key", {"ks": keys}, tenant)}
    todo = list({normalize_key(n): n for n, *_ in items if normalize_key(n) not in known}.items())
    embs = dict(zip([k for k, _ in todo], embed_docs([n for _, n in todo]))) if todo else {}
    return [resolve_entity(store, n, t, embs.get(normalize_key(n)), tenant, w, p) for n, t, w, p in items]
