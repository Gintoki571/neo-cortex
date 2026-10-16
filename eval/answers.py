"""Answer-level eval: graph tools vs a text baseline over eval/answers_gold.jsonl (30 questions, 3 categories).

    NEO_DEVICE=cuda uv run --no-sync python eval/answers.py [--home DIR] [--port N] [--device cuda|cpu]

Tool: tools.who / impact / timeline (current_owner / impact / changes), max_chars 4000.
Baseline: top-8 vector chunks (recall channels=["vector"]), each expanded with tools.read, concatenated, capped at 4000 chars.
Scores: fraction of keys present and all keys present (norm: case, punctuation and hyphens ignored); current_owner also gets
"correct current": tool = first listed person is the gold owner; baseline = gold owner occurs before any forbidden name.
Writes eval/answers_results.json (one entry per --label run, kept across runs) and replaces the "## Graph-native answers"
section at the end of eval/results.md: the "new extraction" run in full, other runs in one line.
Note: run_eval.py rewrites results.md from scratch, so re-run this script after it.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics as M  # noqa: E402

TENANT = "eval"  # the tenant run_eval.py ingests into
BUDGET = 4000
NOW_MS = int(datetime(2026, 10, 16, tzinfo=timezone.utc).timestamp() * 1000)  # same clock as run_eval.py
CATS = ["current_owner", "impact", "changes"]
TOOL_FOR = {"current_owner": "who", "impact": "impact", "changes": "timeline"}


def load_gold(path):
    qs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    for q in qs:
        assert q["category"] in CATS and q["keys"], q["id"]
        if q["category"] == "current_owner":  # keys[0] is the gold owner, so the list holds exactly one name
            assert len(q["keys"]) == 1, f"{q['id']}: current_owner keys must be the single gold owner"
    return qs


def tool_text(store, q):
    from neo_cortex import tools
    fn = getattr(tools, TOOL_FOR[q["category"]])
    return fn(store, q["entity"], max_chars=BUDGET, tenant=TENANT)


def baseline_text(store, q):
    from neo_cortex import tools
    from neo_cortex.retrieve import recall
    items = recall(store, q["question"], k=8, channels=["vector"], tenant=TENANT, now_ms=NOW_MS)
    return "\n\n".join(tools.read(store, it["id"], tenant=TENANT) for it in items)[:BUDGET]


def first_person(out):
    m = re.search(r"^\d+\. \[[^\]]+\] (.+?) score", out, re.M)
    return M.norm(m.group(1)) if m else None


def score(text, q, is_tool):
    tn = f" {M.norm(text)} "
    found = [f" {M.norm(k)} " in tn for k in q["keys"]]
    s = {"keys": sum(found) / len(found), "all": float(all(found)),
         "missing": [k for k, f in zip(q["keys"], found) if not f],
         "forbidden_present": float(any(f" {M.norm(x)} " in tn for x in q["forbidden"]))}
    if q["category"] == "current_owner":
        gold = M.norm(q["keys"][0])
        if is_tool:
            s["correct"] = float(first_person(text) == gold)
        else:
            p = tn.find(f" {gold} ")
            fp = [i for i in (tn.find(f" {M.norm(x)} ") for x in q["forbidden"]) if i >= 0]
            s["correct"] = float(p >= 0 and (not fp or p < min(fp)))
    return s


def run(store, gold):
    rows = []
    for q in gold:
        t, b = tool_text(store, q), baseline_text(store, q)
        rows.append({"id": q["id"], "category": q["category"],
                     "tool": score(t, q, True) | {"chars": len(t)}, "baseline": score(b, q, False) | {"chars": len(b)}})
    return rows


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def summarise(rows):
    out = {}
    for name in ["overall"] + CATS:
        rs = [r for r in rows if name == "overall" or r["category"] == name]
        out[name] = {"n": len(rs)}
        for side in ("tool", "baseline"):
            out[name][side] = {f: mean([r[side][f] for r in rs]) for f in ("keys", "all")}
            cc = [r[side]["correct"] for r in rs if "correct" in r[side]]
            if cc:
                out[name][side]["correct"] = mean(cc)
    return out


def bootstraps(rows):
    res = {}

    def pair(rs, field, label):
        res[label] = M.paired_bootstrap([r["tool"][field] for r in rs], [r["baseline"][field] for r in rs])

    pair(rows, "all", "all keys, overall")
    for c in CATS:
        pair([r for r in rows if r["category"] == c], "all", f"all keys, {c}")
    pair([r for r in rows if r["category"] == "current_owner"], "correct", "correct current, current_owner")
    return res


def db_note(home):
    stamp = home / "eval_ingest.json"  # written at ingest; neo.rdb is re-saved by every server start, so it is no build clock
    if not stamp.exists():
        return f"no eval_ingest.json under {home}; build time unknown"
    built = stamp.stat().st_mtime
    newer = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "src" / "neo_cortex").glob("*.py") if p.stat().st_mtime > built)
    when = datetime.fromtimestamp(built).strftime("%Y-%m-%d %H:%M")
    if newer:
        return (f"DB ingested {when}, before later source edits ({', '.join(newer)}). Its extraction predates those fixes; "
                "re-ingest (run_eval.py --reingest) for current numbers.")
    return f"DB ingested {when}, newer than every src/neo_cortex/*.py file."


def fmt(x):
    return "-" if x is None else f"{x:.2f}"


def render(r):
    summary, boots, rows, note, home, port = r["summary"], r["bootstrap"], r["questions"], r["db_note"], r["home"], r["port"]
    L = [f"Run `{r['label']}`. DB: `{home}` (port {port}, tenant `{TENANT}`). {note}",
         f"Tool: `tools.who`/`impact`/`timeline`, max_chars {BUDGET}. Baseline: top-8 vector chunks via `tools.read`, capped at {BUDGET} chars.",
         "", "| category | n | keys, tool | keys, baseline | all keys, tool | all keys, baseline | correct current, tool | correct current, baseline |",
         "|---|---|---|---|---|---|---|---|"]
    for name in ["overall"] + CATS:
        s = summary[name]
        t, b = s["tool"], s["baseline"]
        L.append(f"| {name} | {s['n']} | {fmt(t['keys'])} | {fmt(b['keys'])} | {fmt(t['all'])} | {fmt(b['all'])} | "
                 f"{fmt(t.get('correct'))} | {fmt(b.get('correct'))} |")
    L += ["", "Paired bootstrap (1000 resamples, seed 0, 95% CI of mean delta, tool minus baseline):"]
    for label, b in boots.items():
        L.append(f"- {label}: {b['delta']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}] (n={b['n']}, {'significant' if b['significant'] else 'inside noise'})")
    fails = [r for r in rows if not r["tool"]["all"] or not r["baseline"]["all"]]
    L += ["", "Questions where a side misses a key (tool / baseline missing):"]
    for r in fails:
        t, b = r["tool"], r["baseline"]
        L.append(f"- {r['id']}: tool {'ok' if t['all'] else 'missing ' + json.dumps(t['missing'])}; "
                 f"baseline {'ok' if b['all'] else 'missing ' + json.dumps(b['missing'])}")
    return "\n".join(L) + "\n"


def write_md(runs):
    primary = runs.get("new extraction") or next(reversed(list(runs.values())))
    text = render(primary)
    for r in runs.values():
        if r is primary:
            continue
        s = r["summary"]
        text += (f"\nOther run, `{r['label']}` ({r['home']}): overall all keys tool {s['overall']['tool']['all']:.2f} vs baseline "
                 f"{s['overall']['baseline']['all']:.2f}; impact {s['impact']['tool']['all']:.2f} vs {s['impact']['baseline']['all']:.2f}; "
                 f"changes {s['changes']['tool']['all']:.2f} vs {s['changes']['baseline']['all']:.2f}.\n")
    p = ROOT / "eval" / "results.md"
    head = p.read_text(encoding="utf-8").split("\n## Graph-native answers", 1)[0].rstrip("\n") + "\n"
    p.write_text(head + "\n## Graph-native answers\n\n" + text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", default=os.environ.get("NEO_HOME", str(ROOT / ".neo" / "eval-new")))
    ap.add_argument("--port", type=int, default=int(os.environ.get("NEO_PORT", "6367")))
    ap.add_argument("--device", default=os.environ.get("NEO_DEVICE"), help="cuda or cpu (cpu on GPU OOM)")
    ap.add_argument("--label", default=None, help="run name, e.g. 'old extraction' or 'new extraction' (default: DB folder name)")
    a = ap.parse_args()
    home = Path(a.home).expanduser().resolve()
    os.environ["NEO_HOME"], os.environ["NEO_PORT"] = str(home), str(a.port)
    if a.device:
        os.environ["NEO_DEVICE"] = a.device
    from neo_cortex.store import Store
    gold = load_gold(ROOT / "eval" / "answers_gold.jsonl")
    with Store() as store:
        rows = run(store, gold)
    summary, boots, note = summarise(rows), bootstraps(rows), db_note(home)
    result = {"label": a.label or home.name, "home": str(home), "port": a.port, "tenant": TENANT, "budget_chars": BUDGET,
              "db_note": note, "summary": summary, "bootstrap": boots, "questions": rows}
    out = ROOT / "eval" / "answers_results.json"
    runs = json.loads(out.read_text(encoding="utf-8")).get("runs", {}) if out.exists() else {}
    runs[result["label"]] = result
    out.write_text(json.dumps({"runs": runs}, indent=1), encoding="utf-8")
    write_md(runs)
    print(render(result))


if __name__ == "__main__":
    main()
