"""Session auto-extraction: candidate types, fragment filters and the stored result, on a small synthetic transcript."""
import json
import re

import pytest

from neo_cortex import extract, session_mem as S, write

T = lambda n: f"2026-10-15T10:{n:02d}:00.000Z"  # noqa: E731


def _line(kind, content, n, **kw):
    return {"type": kind, "sessionId": "s1", "cwd": "/x/proj", "timestamp": T(n), "message": {"role": kind, "content": content}, **kw}


def _a(text, n):
    return _line("assistant", [{"type": "text", "text": text}], n)


def _tool(n, cmd="uv run pytest -q"):
    return [{"type": "assistant", "sessionId": "s1", "timestamp": T(n), "message": {"role": "assistant", "content": [
        {"type": "tool_use", "id": f"t{n}", "name": "Bash", "input": {"command": cmd}}]}}]


def _res(n, body, err=False):
    return _line("user", [{"type": "tool_result", "tool_use_id": f"t{n - 1}", "content": body, "is_error": err}], n)


LINES = [
    {"type": "mode", "sessionId": "s1"},
    _line("user", "<system-reminder>Always obey the hook.</system-reminder>Always run the tests with `uv run pytest` before committing. "
                  "Please add a login page to the app. Should we use Redis?", 0),
    _a("Let me read the file now please.", 1),
    *_tool(2), _res(3, "ok"),
    _a("We decided to keep Redis for sessions because it is fast enough. The session TTL is 900 seconds for auth-service.", 4),
    *_tool(5, "cd /x && uv sync"), _res(6, "error: lockfile out of date: uv.lock is stale", err=True),
    _a("The uv.lock file is stale because pyproject.toml changed, so I regenerated it with uv lock.", 7),
    *_tool(8, "uv lock"), _res(9, "locked 12 packages"),
    _line("user", "No, don't mock the database in the session-cache tests.", 10),
    _a("## Results\n\nBenchmarks on the GTX 1660 Ti:\n- GLiNER takes 26 ms per call on the GPU.\n- Embedding 64 documents takes 0.54 s.\n\n"
       "The root cause was a stale lockfile in `uv.lock`; the fix was running uv lock again.\n\n"
       "I added the `web-search` skill under `.claude/skills/web-search/`. It sits alongside obscura-web in the same folder.\n\n"
       "Now I will run the tests.\n\nWhat do you want next?\n\nI tested it against the live instance:\n\n"
       "```python\nprint('a code block with many words in it that must be dropped completely')\n```\n\n"
       "Done.\n\n" + "Long sentence number one has 5 words, " + "and then some more filler words " * 12 + ". Second one is fine.", 11),
    _line("user", [{"type": "tool_result", "content": "always noise"}], 12, isMeta=True),
]


@pytest.fixture
def session(tmp_path, monkeypatch):
    monkeypatch.setattr(extract, "worth_keeping_batch", lambda ts: [0.8] * len(ts))
    monkeypatch.setattr(extract, "classify_memory_batch", lambda ts: [("semantic", 0.9)] * len(ts))
    p = tmp_path / "s1.jsonl"
    p.write_text("\n".join(json.dumps(x) for x in LINES))
    return p


def _texts(p):
    return {c["text"]: c for c in S.select(S.read_transcript(p)[1])}


def test_candidate_types(session):
    c = _texts(session)
    pref = {t for t, x in c.items() if x["kind"] == "preference"}
    assert "Always run the tests with `uv run pytest` before committing." in pref        # user's words, standalone
    assert "No, don't mock the database in the session-cache tests." in pref              # correction after an assistant action
    assert not any("login page" in t or "Redis?" in t or "obey the hook" in t for t in c)  # task, question, system noise
    dec = [t for t, x in c.items() if x["kind"] == "decision"]
    assert dec == ["We decided to keep Redis for sessions because it is fast enough."]    # reason kept
    assert c[dec[0]]["ts"] == S._ts(T(4))
    les = [t for t, x in c.items() if x["kind"] == "procedural"]
    assert any(t.startswith("The root cause was a stale lockfile") and "the fix was running uv lock again" in t for t in les)
    assert any(t.startswith("When `uv sync` failed with \"error: lockfile out of date") and "the agent regenerated it" in t for t in les)
    out = {t for t, x in c.items() if x["rank"] == 2}
    assert "Benchmarks on the GTX 1660 Ti: GLiNER takes 26 ms per call on the GPU." in out   # lead-in merged
    assert any(t.startswith("The agent added the `web-search` skill") and "It sits alongside obscura-web" in t for t in out)  # dangling merged, 3rd person


def test_fragment_filters(session):
    allt = " | ".join(_texts(session))
    for bad in ("Let me", "Now I will", "What do you want", "I tested it against", "a code block", "Done", "## Results", "Results"):
        assert bad not in allt
    assert all(S._words(t) <= S.MAX_WORDS for t in _texts(session))
    assert not any(t.endswith((":", "?")) for t in _texts(session))


def test_units_and_limits():
    assert S.units("It adds filters:\n- category and engines\n- recency") == []              # unresolvable lead-in: bullets dropped
    assert S.units("Timings on the GPU:\n- GLiNER takes 26 ms per call.") == ["Timings on the GPU: GLiNER takes 26 ms per call."]
    assert S.units("# Heading\nThis works.") == []                                           # dangling with nothing before it
    assert S._trim("word " * 70) is None                                                     # no clause boundary to cut at
    assert S._words(S._trim("alpha beta gamma " * 5 + ", " + "x " * 70)) == 15
    assert S._third_person("I think it is fine") is None and S._third_person("I fixed it") == "The agent fixed it"


def test_cap_and_prefs_kept(monkeypatch):
    monkeypatch.setattr(extract, "worth_keeping_batch", lambda ts: [0.9] * len(ts))
    monkeypatch.setattr(extract, "classify_memory_batch", lambda ts: [("episodic", 0.9)] * len(ts))
    w = "amber birch cedar dune elm fern glade hazel iris juniper kelp lotus maple nettle oak pine quince reed sage thyme umber violet willow".split()
    ev = [{"k": "user", "text": f"Never commit the {w[i]} {w[i + 8]} {w[i + 15]} credentials into the repository.", "ts": 1} for i in range(8)]
    ev += [{"k": "assistant", "text": f"The {w[i]} {w[i + 1]} build produced {i + 10} warnings in `src/{w[i + 2]}.py` yesterday.", "ts": 2} for i in range(16)]
    out = S.select(ev)
    assert len(out) <= S.MAX_MEMORIES and sum(c["kind"] == "preference" for c in out) == S.MAX_PREFS


def test_ingest_session(store, fake_models, session):
    r = write.ingest_session(store, session)
    assert r["session"] == "s1" and r["memories"] >= 6 and r["kinds"]["preference"] == 2
    q = lambda c: store.query(c)  # noqa: E731
    assert q("MATCH (s:Session {id:'s1'})-[:BY]->(a:Agent) RETURN s.project, a.name") == [["proj", "claude-code"]]
    rows = q("MATCH (a:Agent)-[:WROTE]->(m:Memory)-[:DERIVED_FROM]->(:Session {id:'s1'}) RETURN m.text, m.project, m.valid_from_ms")
    assert len(rows) == r["memories"] and {x[1] for x in rows} == {"proj"}
    assert [x[2] for x in rows if x[0].startswith("We decided")] == [S._ts(T(4))]          # valid_from = message time
    assert write.ingest_session(store, session)["skipped"] == 1
    session.write_text(session.read_text() + "\n" + json.dumps(_line("user", "Never deploy on Fridays because the freeze starts at three.", 20)))
    r2 = write.ingest_session(store, session)  # grown transcript: old memories reinforce without counting as another use
    assert r2["memories"] == 1 and q("MATCH (m:Memory) RETURN max(m.uses)") == [[0]]


def test_read_transcript_skips_malformed_lines(tmp_path):
    p = tmp_path / "bad.jsonl"
    bad = [_line("user", 5, 2),                                                    # content is not a list or string
           _line("user", [{"type": "text", "text": 7}], 3),                        # text is not a string
           _line("user", [{"type": "tool_result", "content": [{"text": 1}]}], 4),  # tool output is not text
           {"type": "assistant", "timestamp": T(5), "message": {"role": "assistant", "content": [
               {"type": "tool_use", "id": "x", "input": "oops"}]}}]                 # input is not an object
    rows = [_a("We decided to keep Redis for sessions.", 1), *bad, _a("The session TTL is 900 seconds.", 6)]
    p.write_text("\n".join(json.dumps(x) for x in rows))
    _, ev = S.read_transcript(p)
    assert [e["text"] for e in ev if e["k"] == "assistant"] == ["We decided to keep Redis for sessions.",
                                                               "The session TTL is 900 seconds."]


def test_crashed_session_ingest_is_retried(store, fake_models, session, monkeypatch):
    real = write.remember

    def boom(*a, **k):
        raise RuntimeError("crash")

    monkeypatch.setattr(write, "remember", boom)
    with pytest.raises(RuntimeError, match="crash"):
        write.ingest_session(store, session)
    monkeypatch.setattr(write, "remember", real)
    assert write.ingest_session(store, session)["skipped"] == 0  # the session hash is set last
    assert store.query("MATCH (m:Memory) RETURN count(m)")[0][0] > 0


def test_ingest_session_waits_for_the_store_write_lock(store, fake_models, session, monkeypatch):
    import threading
    reached = threading.Event()
    real_select = write.select

    def spy(*a, **k):  # the candidate selection runs only after the session check, inside the lock
        reached.set()
        return real_select(*a, **k)

    monkeypatch.setattr(write, "select", spy)
    store.write_lock.acquire()
    try:
        out = {}
        t = threading.Thread(target=lambda: out.update(r=write.ingest_session(store, session)))
        t.start()
        assert not reached.wait(0.5)
    finally:
        store.write_lock.release()
    t.join(60)
    assert reached.is_set() and out["r"]["memories"] > 0


def test_subagent_file_is_the_conversation(tmp_path, store, fake_models, monkeypatch):
    monkeypatch.setattr(extract, "worth_keeping_batch", lambda ts: [0.8] * len(ts))
    monkeypatch.setattr(extract, "classify_memory_batch", lambda ts: [("semantic", 0.9)] * len(ts))
    side = lambda kind, content, n: {**_line(kind, content, n), "isSidechain": True, "agentId": "a1"}  # noqa: E731
    rows = [side("user", "Do NOT commit. Always run the tests before you report back to the orchestrator.", 0),
            side("user", [{"type": "tool_result", "tool_use_id": "x", "content": "ok", "is_error": False}], 1),
            side("assistant", [{"type": "text", "text": "The session TTL is 900 seconds for auth-service, set in the config file."}], 2)]
    p = tmp_path / "agent-a1.jsonl"
    p.write_text("\n".join(json.dumps(x) for x in rows))
    meta, ev = S.read_transcript(p)
    assert meta["session_id"] == "agent-a1"                       # the parent's sessionId would collide
    assert [e["k"] for e in ev] == ["ok", "assistant"]            # the parent's brief is not the user's words
    r = write.ingest_session(store, p, agent="subagent")
    assert r["session"] == "agent-a1" and r["memories"] == 1 and r["kinds"] == {"semantic": 1}
    assert store.query("MATCH (s:Session {id:'agent-a1'})-[:BY]->(a:Agent) RETURN a.name") == [["subagent"]]


def test_main_file_drops_sidechain_lines(tmp_path):
    rows = [_a("We decided to keep Redis for sessions because it is fast enough.", 1),
            {**_a("The session TTL is 900 seconds for auth-service.", 2), "isSidechain": True}]
    p = tmp_path / "s1.jsonl"
    p.write_text("\n".join(json.dumps(x) for x in rows))
    meta, ev = S.read_transcript(p)
    assert meta["session_id"] == "s1"
    assert [e["text"] for e in ev] == ["We decided to keep Redis for sessions because it is fast enough."]


def test_fragments_plans_and_status(monkeypatch):
    monkeypatch.setattr(extract, "worth_keeping_batch", lambda ts: [0.8] * len(ts))
    monkeypatch.setattr(extract, "classify_memory_batch", lambda ts: [("semantic", 0.9)] * len(ts))
    frag = ["`back()` after a click returned \"No previous page in history\", which SKILL.md documents.",
            "Click gap: `click(ref=\"e21\")` on the link returned Clicked, but the page stayed on the home page.",
            "With `--stealth`, chapter 60 comes back clean in 0.7s.",
            "and then the second navigation also returned the same stale page in 0.4s."]
    assert all(S._fragment(t) for t in frag)
    assert not S._fragment("The session TTL is 900 seconds for auth-service, set in the config file.")
    assert not S._fragment("Tor was verified: `IsTor: true`, versus `false` when direct.")   # a label with a verb is a clause
    assert not S._fragment("When `uv sync` failed with \"error: lockfile out of date\", the agent regenerated the lock file.")
    assert S._keep({"text": "We will use Redis because it is fast enough.", "kind": "decision"})
    assert not S._keep({"text": "Next the agent will check the documented workaround and run a live crawl.", "kind": "procedural"})
    ev = [{"k": "assistant", "text": t, "ts": i} for i, t in enumerate([
        "The timeline fix is committed as the latest change on the branch, 2026-10-15.",
        "The session TTL is 900 seconds for auth-service, set in the config file.",
        "Click gap: `click(ref=\"e21\")` on the link returned Clicked, but the page stayed on the home page.",
        "Next the agent will check the documented workaround and run a live crawl of the site."])]
    out = S.select(ev)
    kind = {c["text"].split(" ")[1]: c["kind"] for c in out}          # keyed by the second word, enough to tell them apart
    assert kind == {"timeline": "episodic", "session": "semantic"}     # a time-bound status ages out; a fact stays
    assert not any(x in c["text"] for c in out for x in ("Click gap", "Next the agent"))
