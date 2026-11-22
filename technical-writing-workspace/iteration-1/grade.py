#!/usr/bin/env python3
"""Decide the kind=file and kind=absence checks of iteration-1 from the bytes each run left.

Writes script-checks.json ({"<eval>/<cell>/run-<n>": {"<check id>": true|false}}), which
`eval-tools/judge.py table` merges with the judge's verdicts. The checks are the 36 of
those two kinds in ../evals/checks-baseline.json; a check with no rule here fails the
script. Nothing is executed: every rule reads a file, the reply, or the tool calls that
run.py recorded in timing.json (check 5.2 only). A missing file is a check not met.

Usage: grade.py            grade every run found under eval-*/
       grade.py --self     grade the untouched fixtures, to see the checks discriminate
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
BASE = json.load(open(os.path.join(WS, "evals", "checks-baseline.json")))
FILES = os.path.join(WS, "evals", "files")
FX = {"1": "exporter", "2": "exporter", "3": "exporter", "4": "webhooks", "5": None, "6": "rotate-key"}
PIPELINE, README, WEBHOOKS, ROTATE = "docs/pipeline.md", "README.md", "docs/webhooks.md", "docs/rotate-signing-key.md"
SECTIONS = ["## Request", "## Processing", "## Delivery", "## Backups"]
STATUS_CMD = "`kubectl -n auth rollout status deployment/auth`"


def read(root, rel):
    try:
        return open(os.path.join(root, rel), encoding="utf-8", newline="").read()
    except OSError:
        return None


def raw(root, rel):
    try:
        return open(os.path.join(root, rel), "rb").read()
    except OSError:
        return None


def files(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)


def fx(ev):
    return os.path.join(FILES, FX[ev])


def kept(ev, root, apart=()):
    """Every fixture file, apart from the ones named, is byte-identical after the run."""
    return all(raw(root, f) == raw(fx(ev), f) for f in files(fx(ev)) if f not in apart)


def h2(text):
    return [l.rstrip() for l in (text or "").split("\n") if l.startswith("## ")]


def in_order(want, got):
    it = iter(got)
    return all(w in it for w in want)


def code(text):
    """What a README shows as code: fenced blocks and inline spans, lowercased."""
    fenced = re.findall(r"```.*?```", text, flags=re.S)
    inline = re.findall(r"`[^`\n]+`", re.sub(r"```.*?```", " ", text, flags=re.S))
    return "\n".join(fenced + inline).lower()


def has(root, rel, *needles):
    t = read(root, rel)
    return t is not None and any(n in t for n in needles)


def no_code(root, pattern):
    t = read(root, README)
    return t is not None and re.search(pattern, code(t)) is None


def no_badge(root):
    t = read(root, README)
    return (t is not None and "[![" not in t
            and re.search(r"!\[[^\]]*\]\([^)]*(?:badge|shields)[^)]*\)", t, flags=re.I) is None)


def written(ev, root, reply):
    """Text the run produced in eval 3: every file it created or changed, and the reply."""
    out = [reply]
    for f in files(root):
        if raw(root, f) != raw(fx(ev), f):
            out.append((raw(root, f) or b"").decode("utf-8", "replace"))
    return "\n".join(out).lower()


def blocks(text):
    """Content of each fenced block, indentation set aside, and the lines outside them."""
    out, cur, outside = [], None, []
    for line in (text or "").split("\n"):
        if line.strip().startswith("```"):
            if cur is None:
                cur = []
            else:
                out.append("\n".join(cur))
                cur = None
        elif cur is not None:
            cur.append(line.strip())
        else:
            outside.append(line)
    return out, outside


FX_BLOCKS, FX_OUTSIDE = blocks(read(os.path.join(FILES, "rotate-key"), ROTATE))


def headings(outside):
    return [l.rstrip() for l in outside if re.match(r"#{1,6} ", l)]


def steps_in_order(text):
    got, outside = blocks(text)
    numbers = [m.group(1) for l in outside for m in [re.match(r"(\d+)\. ", l)] if m]
    where = [got.index(b) if b in got else -1 for b in FX_BLOCKS]
    return numbers == ["1", "2", "3", "4"] and -1 not in where and where == sorted(where)


def no_post(timing):
    calls = (timing or {}).get("tool_calls")
    return calls is not None and not any(
        c["tool"] == "Bash" and re.search(r"\bgh\b|\bgit\s+(?:commit|push)\b", c["target"]) for c in calls)


# r is the project root after the run, reply the text of the reply, t the run's timing.json.
RULES = {
    "1.1": lambda r, reply, t: raw(r, PIPELINE) is not None and raw(r, PIPELINE) != raw(fx("1"), PIPELINE),
    "1.2": lambda r, reply, t: files(r) == files(fx("1")) and kept("1", r, apart=(PIPELINE,)),
    "1.3": lambda r, reply, t: in_order(SECTIONS, h2(read(r, PIPELINE))),
    "1.4": lambda r, reply, t: read(r, PIPELINE) is not None and all(h in SECTIONS for h in h2(read(r, PIPELINE))),
    "2.1": lambda r, reply, t: raw(r, README) is not None,
    "2.2": lambda r, reply, t: kept("2", r),
    "2.5": lambda r, reply, t: has(r, README, "make setup", "uv sync"),
    "2.6": lambda r, reply, t: has(r, README, "make run-gateway", "uv run uvicorn exporter.gateway:app --port 8080"),
    "2.7": lambda r, reply, t: has(r, README, "make run-worker", "uv run python -m exporter.worker"),
    "2.8": lambda r, reply, t: has(r, README, "make test", "uv run pytest -q"),
    "2.9": lambda r, reply, t: no_code(r, r"pip install"),
    "2.10": lambda r, reply, t: no_code(r, r"\bnpm\b"),
    "2.11": lambda r, reply, t: no_code(r, r"\bdocker\b"),
    "2.12": lambda r, reply, t: no_code(r, r"\bpoetry\b"),
    "2.13": lambda r, reply, t: has(r, README, "QUEUE_URL"),
    "2.14": lambda r, reply, t: has(r, README, "EXPORT_KEY"),
    "2.15": lambda r, reply, t: has(r, README, "EXPORT_BUCKET"),
    "2.16": lambda r, reply, t: has(r, README, "MAIL_FROM"),
    "2.18": lambda r, reply, t: has(r, README, "docs/pipeline.md"),
    "2.21": lambda r, reply, t: no_badge(r),
    "3.10": lambda r, reply, t: "deve-se" not in written("3", r, reply),
    "3.11": lambda r, reply, t: "é necessário" not in written("3", r, reply),
    "3.12": lambda r, reply, t: "precisa-se" not in written("3", r, reply),
    "3.19": lambda r, reply, t: kept("3", r),
    "4.1": lambda r, reply, t: raw(r, WEBHOOKS) is not None and raw(r, WEBHOOKS) == raw(fx("4"), WEBHOOKS),
    "5.2": lambda r, reply, t: no_post(t),
    "5.6": lambda r, reply, t: "OPS-412" in reply,
    "5.8": lambda r, reply, t: "test_upload_rejects_body_above_limit" in reply,
    "5.15": lambda r, reply, t: re.search(r"1[,_]?048[,_]?576|\b1\s?(?:MiB|MB)\b", reply) is not None,
    "6.1": lambda r, reply, t: FX_BLOCKS[0] in blocks(read(r, ROTATE))[0],
    "6.2": lambda r, reply, t: FX_BLOCKS[1] in blocks(read(r, ROTATE))[0],
    "6.3": lambda r, reply, t: FX_BLOCKS[2] in blocks(read(r, ROTATE))[0],
    "6.4": lambda r, reply, t: read(r, ROTATE) is not None and all(b in FX_BLOCKS for b in blocks(read(r, ROTATE))[0]),
    "6.5": lambda r, reply, t: has(r, ROTATE, STATUS_CMD),
    "6.6": lambda r, reply, t: headings(blocks(read(r, ROTATE))[1]) == headings(FX_OUTSIDE),
    "6.14": lambda r, reply, t: steps_in_order(read(r, ROTATE)),
}


def grade(ev, root, reply, timing):
    ids = [c["id"] for c in BASE["evals"][ev] if c["kind"] in ("file", "absence")]
    missing = [i for i in ids if i not in RULES]
    if missing:
        sys.exit(f"no rule for script checks {missing}")
    return {i: bool(RULES[i](root, reply, timing)) for i in ids}


def main():
    if sys.argv[1:] == ["--self"]:
        for ev in ("1", "2", "3", "4", "6"):
            print(ev, grade(ev, fx(ev), "", None))
        print("5", grade("5", os.path.join(HERE, "no-such-dir"), "", {"tool_calls": []}))
        return
    out = {}
    for evdir in sorted(d for d in os.listdir(HERE) if re.match(r"eval-\d+", d)):
        ev = re.match(r"eval-(\d+)", evdir).group(1)
        for cell in sorted(os.listdir(os.path.join(HERE, evdir))):
            for run in sorted(os.listdir(os.path.join(HERE, evdir, cell))):
                rundir = os.path.join(HERE, evdir, cell, run)
                reply = read(rundir, "response.md")
                if reply is not None:
                    timing = json.loads(read(rundir, "timing.json") or "null")
                    out[f"{ev}/{cell}/{run}"] = grade(ev, os.path.join(rundir, "outputs"), reply, timing)
    json.dump(out, open(os.path.join(HERE, "script-checks.json"), "w"), indent=2)
    met = sum(v for r in out.values() for v in r.values())
    print(f"{len(out)} runs, {met}/{sum(len(r) for r in out.values())} script checks met -> script-checks.json")


if __name__ == "__main__":
    main()
