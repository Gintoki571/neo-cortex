#!/usr/bin/env python3
"""Fetch public FalkorDB GitHub data into data/public/falkordb/ as markdown + YAML frontmatter.

Needs `gh` logged in. Stdlib only. Re-run: python3 scripts/fetch_public.py
Overwrites data/public/falkordb/ and data/public/README.md on every run.
"""
import base64, collections, datetime, json, pathlib, re, shutil, subprocess, time
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "data" / "public"
OUT = PUBLIC / "falkordb"
REPOS = ["FalkorDB/FalkorDB", "FalkorDB/falkordb-py", "FalkorDB/GraphRAG-SDK"]
DOCS = "FalkorDB/docs"
DOC_PREFER = ["cypher/", "algorithms/", "indexing", "getting-started/"]
ISSUE_CAP, PR_CAP, COMMENT_CAP, FILE_CAP, DOC_CAP, PEOPLE_CAP = 80, 40, 30, 30, 60, 15
BODY_CAP = 20_000  # bytes; longer bodies are cut with a marker
SLEEP = 0.2
REQUIRED = ["id", "kind", "title", "date", "author", "participants", "status", "labels", "uri"]
failures, written = [], []


def gh(path):
    time.sleep(SLEEP)
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:200])
    return json.loads(r.stdout)


def listing(path, want, keep=lambda x: True):
    out, page = [], 1
    while len(out) < want:
        batch = gh(f"{path}&per_page=100&page={page}")
        if not batch:
            break
        out += [x for x in batch if keep(x)]
        page += 1
    return out[:want]


def login(user):
    return (user or {}).get("login", "ghost")


def clip(text):
    if len(text.encode()) <= BODY_CAP:
        return text
    return text.encode()[:BODY_CAP].decode("utf-8", "ignore") + "\n\n[truncated: body over 20 KB]"


def write(meta, body):
    d = OUT / meta["kind"]
    d.mkdir(parents=True, exist_ok=True)
    head = "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items())
    (d / f"{meta['id']}.md").write_text(f"---\n{head}\n---\n\n{body.strip()}\n", encoding="utf-8")
    written.append(meta)


def attempt(label, fn, *args):
    try:
        fn(*args)
    except Exception as e:  # keep going, report at the end
        failures.append(f"{label}: {e}")


def ticket(repo, item, is_pr):
    n = item["number"]
    comments = gh(f"repos/{repo}/issues/{n}/comments?per_page={COMMENT_CAP}")
    status = ("merged" if item.get("merged_at") else item["state"]) if is_pr else item["state"]
    body = [f"# {item['title']}", clip(item["body"] or ""), "## Comments"]
    body += [f"**{login(c['user'])} ({c['created_at'][:10]}):** {clip(c['body'] or '')}" for c in comments]
    if is_pr:
        files = gh(f"repos/{repo}/pulls/{n}/files?per_page={FILE_CAP}")
        body += ["## Files", "\n".join(f"- {f['filename']}" for f in files)]
    write({
        "id": f"gh-{repo.replace('/', '-')}-{'pr' if is_pr else 'issue'}-{n}", "kind": "ticket",
        "title": item["title"], "date": item["created_at"], "author": login(item["user"]),
        "participants": list(dict.fromkeys(login(c["user"]) for c in comments)),
        "status": status, "labels": [l["name"] for l in item["labels"]], "uri": item["html_url"],
    }, "\n\n".join(body))


def last_commit(repo, path):
    c = gh(f"repos/{repo}/commits?path={quote(path)}&per_page=1")[0]
    return c["commit"]["committer"]["date"], login(c["author"])


def split_frontmatter(text):
    if text.startswith("---\n") and (end := text.find("\n---", 3)) != -1:
        return text[4:end], text[end + 4:]
    return "", text


def fetch_doc(path):
    f = gh(f"repos/{DOCS}/contents/{quote(path)}")
    text = base64.b64decode(f["content"]).decode("utf-8")
    src_meta, body = split_frontmatter(text)
    m = re.search(r"^title:\s*(.+?)\s*$", src_meta, re.M) or re.search(r"^# (.+)$", body, re.M)
    date, author = last_commit(DOCS, path)
    write({
        "id": "gh-docs-" + re.sub(r"\.mdx?$", "", path).replace("/", "-"), "kind": "doc",
        "title": m.group(1).strip("\"' ") if m else path, "date": date, "author": author,
        "participants": [], "status": "", "labels": [], "uri": f["html_url"],
    }, clip(body))


def fetch_codeowners(repo):
    for path in ["CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"]:
        try:
            f = gh(f"repos/{repo}/contents/{path}")
        except RuntimeError:
            continue
        date, author = last_commit(repo, path)
        text = base64.b64decode(f["content"]).decode("utf-8")
        write({
            "id": f"gh-{repo.replace('/', '-')}-codeowners", "kind": "doc", "title": f"{repo} CODEOWNERS",
            "date": date, "author": author, "participants": [], "status": "", "labels": [],
            "uri": f["html_url"],
        }, f"# CODEOWNERS ({path})\n\n```\n{clip(text)}\n```")
        return


def fetch_people(repo):
    return [{"login": c["login"], "repo": repo, "contributions": c["contributions"]}
            for c in gh(f"repos/{repo}/contributors?per_page={PEOPLE_CAP}")]


def check_frontmatter(path):
    _, fm, _ = path.read_text(encoding="utf-8").split("---\n", 2)
    keys = {line.split(":", 1)[0] for line in fm.splitlines()}
    assert set(REQUIRED) <= keys, f"{path}: missing {set(REQUIRED) - keys}"


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    for repo in REPOS:
        try:
            items = [(i, False) for i in listing(f"repos/{repo}/issues?state=all&sort=created&direction=desc",
                                                ISSUE_CAP, lambda i: "pull_request" not in i)]
            items += [(p, True) for p in listing(f"repos/{repo}/pulls?state=all&sort=created&direction=desc", PR_CAP)]
        except Exception as e:
            failures.append(f"{repo} listing: {e}")
            continue
        for item, is_pr in items:
            attempt(f"{repo} #{item['number']}", ticket, repo, item, is_pr)
    try:
        tree = gh(f"repos/{DOCS}/git/trees/HEAD?recursive=1")["tree"]
        paths = [t["path"] for t in tree if t["type"] == "blob" and t["path"].endswith((".md", ".mdx"))
                 and not t["path"].startswith(".")]
        paths = sorted(paths, key=lambda p: next((i for i, k in enumerate(DOC_PREFER) if k in p), len(DOC_PREFER)))
    except Exception as e:
        failures.append(f"docs tree: {e}")
        paths = []
    for p in paths[:DOC_CAP]:
        attempt(f"doc {p}", fetch_doc, p)
    for repo in REPOS:
        attempt(f"{repo} codeowners", fetch_codeowners, repo)
    people = []
    for repo in REPOS:
        try:
            people += fetch_people(repo)
        except Exception as e:
            failures.append(f"{repo} contributors: {e}")
    (OUT / "people.jsonl").write_text("".join(json.dumps(p) + "\n" for p in people), encoding="utf-8")

    for path in OUT.rglob("*.md"):
        check_frontmatter(path)
    counts = collections.Counter((m["kind"], "/".join(m["uri"].split("/")[3:5])) for m in written)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Public data: FalkorDB", "",
        f"Fetched {now} by `scripts/fetch_public.py` via `gh api` (REST).", "",
        "Public data from public GitHub repos (FalkorDB org). No private repos, no credentials.", "",
        f"- Repos: {', '.join(REPOS)}",
        f"- Docs: {DOCS} (cap {DOC_CAP} files; prefers {', '.join(DOC_PREFER)})",
        f"- Tickets: last {ISSUE_CAP} issues and {PR_CAP} PRs per repo, first {COMMENT_CAP} comments each; PRs list first {FILE_CAP} changed files",
        f"- People: top {PEOPLE_CAP} contributors per repo in `falkordb/people.jsonl`", "",
        "## Counts", "", "| kind | repo | files |", "|---|---|---|",
        *[f"| {k} | {r} | {n} |" for (k, r), n in sorted(counts.items())],
        f"| people | all | {len(people)} rows |", "",
        f"Failures: {len(failures)}", *[f"- {f}" for f in failures], "",
        "## Re-run", "", "    python3 scripts/fetch_public.py", "",
        "Needs `gh` logged in. Takes several minutes (about 0.2 s sleep per call). Overwrites `falkordb/`.",
    ]
    (PUBLIC / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"written: {len(written)} files, people rows: {len(people)}, failures: {len(failures)}")
    for f in failures:
        print("FAIL", f)


if __name__ == "__main__":
    main()
