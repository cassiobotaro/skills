#!/usr/bin/env python3
"""Script pre-pass for iteration-9: decides every kind=file / kind=absence check of
evals/checks-baseline.json from the bytes on disk. Read-only over the run outputs.

Usage (repo root):  python3 adr-workspace/iteration-9/check_files.py
Writes <run>/checks-script.json next to each run's outputs/.
A met check carries `ref` (path:line or a path); an unmet one carries `search`.
"""
import datetime, glob, hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
FIXTURE = os.path.join(WS, "evals", "files", "session-service")
BASELINE = json.load(open(os.path.join(WS, "evals", "checks-baseline.json")))["evals"]
HEADINGS = ["## Status", "## Context", "## Decision", "## Consequences"]


def tree(root):
    out = []
    for d, _, fs in os.walk(root):
        for f in fs:
            out.append(os.path.relpath(os.path.join(d, f), root))
    return sorted(out)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def met(ref, note=""):
    return {"passed": True, "ref": ref, "evidence": note or ref}


def unmet(search, note):
    return {"passed": False, "search": search, "evidence": note}


def empty_tree(out):
    files = tree(out)
    if not files:
        return met("outputs/ (empty)", "project root holds no file after the run")
    return unmet("os.walk over outputs/", "files present: " + ", ".join(files))


def eval10(out):
    r = {}
    files = tree(out)
    fixture = tree(FIXTURE)
    new = [f for f in files if f not in fixture]
    adr_new = [f for f in new if f.startswith("doc/adr/")]
    walk = "os.walk over outputs/, diffed against the session-service fixture"

    ok = len(adr_new) == 1 and re.fullmatch(r"doc/adr/0004-[a-z0-9]+(-[a-z0-9]+)*\.md", adr_new[0])
    r["10.1"] = met(adr_new[0]) if ok else unmet(walk, f"new files under doc/adr/: {adr_new or 'none'}")

    path = os.path.join(out, adr_new[0]) if len(adr_new) == 1 else None
    lines = open(path, encoding="utf-8").read().split("\n") if path else []
    rel = adr_new[0] if path else None
    need = "needs the single new ADR of 10.1, which is absent"

    def ln(i):
        return f"{rel}:{i + 1}"

    # 10.2 H1 and slug
    if not path:
        r["10.2"] = unmet(walk, need)
    else:
        m = re.fullmatch(r"# 4\. (.+)", lines[0])
        base = os.path.basename(rel)[5:-3]
        if m and slugify(m.group(1)) == base:
            r["10.2"] = met(ln(0), f"H1 '{lines[0]}' -> slug '{base}'")
        else:
            want = slugify(m.group(1)) if m else "n/a"
            r["10.2"] = unmet(f"line 1 of {rel} and its filename", f"H1 '{lines[0]}', filename slug '{base}', slug from title '{want}'")

    # 10.3 date
    if not path:
        r["10.3"] = unmet(walk, need)
    else:
        written = datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
        hits = [i for i, l in enumerate(lines) if re.fullmatch(r"Date: \d{4}-\d{2}-\d{2}", l)]
        if len(hits) == 1 and lines[hits[0]] == f"Date: {written}":
            r["10.3"] = met(ln(hits[0]), f"'{lines[hits[0]]}' equals the file's write date")
        else:
            found = [lines[i] for i in hits] or "no 'Date: YYYY-MM-DD' line"
            r["10.3"] = unmet(f"regex '^Date: \\d{{4}}-\\d{{2}}-\\d{{2}}$' over {rel}; file mtime date {written}", f"found: {found}")

    # 10.4 headings
    if not path:
        r["10.4"] = unmet(walk, need)
    else:
        heads = [(i, l) for i, l in enumerate(lines) if l.startswith("#")]
        if [l for _, l in heads[1:]] == HEADINGS and heads and heads[0][0] == 0:
            r["10.4"] = met(f"{rel}:{','.join(str(i + 1) for i, _ in heads[1:])}", "four headings in order, none extra")
        else:
            r["10.4"] = unmet(f"every line starting with '#' in {rel}", f"headings found: {[l for _, l in heads]}")

    # 10.5 status word
    if not path:
        r["10.5"] = unmet(walk, need)
    else:
        try:
            a, b = lines.index("## Status"), lines.index("## Context")
            body = [(i, lines[i]) for i in range(a + 1, b) if lines[i].strip()]
        except ValueError:
            body = []
        if body and body[0][1] == "Accepted":
            r["10.5"] = met(ln(body[0][0]), "first non-blank line of Status is 'Accepted'")
        else:
            r["10.5"] = unmet(f"lines between '## Status' and '## Context' in {rel}", f"found: {[l for _, l in body] or 'nothing'}")

    # 10.6 blank-line discipline
    if not path:
        r["10.6"] = unmet(walk, need)
    else:
        bad = []
        body = lines[:-1] if lines and lines[-1] == "" else lines
        for i in range(1, len(body)):
            if body[i] == "" and body[i - 1] == "":
                bad.append(f"{ln(i)} double blank")
        for i, l in enumerate(body):
            if l.startswith("#") or l.startswith("Date: "):
                if i > 0 and body[i - 1] != "":
                    bad.append(f"{ln(i)} no blank before")
                if i + 1 < len(body) and body[i + 1] != "":
                    bad.append(f"{ln(i)} no blank after")
        if not bad:
            r["10.6"] = met(rel, "no double blank; blank line around H1, Date and every heading")
        else:
            r["10.6"] = unmet(f"line-by-line scan of {rel}", "; ".join(bad))

    # 10.10 fixtures untouched
    diffs = []
    for f in fixture:
        p = os.path.join(out, f)
        if not os.path.exists(p):
            diffs.append(f"{f} missing")
        elif sha(p) != sha(os.path.join(FIXTURE, f)):
            diffs.append(f"{f} differs")
    r["10.10"] = met("doc/adr/0001..0003", "sha256 equal to the fixture for all three") if not diffs else unmet("sha256 of each fixture file vs outputs/", "; ".join(diffs))

    # 10.11 nothing else created or edited
    other = [f for f in new if f not in adr_new]
    dsl = [f for f in files if f.endswith(".dsl")]
    if not other and not dsl:
        r["10.11"] = met("outputs/", "the only new path is the ADR; no .dsl file anywhere")
    else:
        r["10.11"] = unmet(walk, f"extra new files: {other or 'none'}; .dsl files: {dsl or 'none'}")
    return r


def main():
    for run in sorted(glob.glob(os.path.join(HERE, "eval-*", "*", "run-*"))):
        ev = re.search(r"eval-(\d+)-", run).group(1)
        out = os.path.join(run, "outputs")
        if ev == "8":
            res = {"8.4": empty_tree(out)}
        elif ev == "9":
            res = {"9.3": empty_tree(out)}
        else:
            res = eval10(out)
        text = {c["id"]: c["check"] for c in BASELINE[ev]}
        rows = [{"id": k, "text": text[k], **v} for k, v in res.items()]
        json.dump({"decided_by": "script", "files": tree(out), "checks": rows},
                  open(os.path.join(run, "checks-script.json"), "w"), ensure_ascii=False, indent=2)
        print(os.path.relpath(run, HERE), " ".join(f"{x['id']}={'Y' if x['passed'] else 'N'}" for x in rows))


if __name__ == "__main__":
    main()
