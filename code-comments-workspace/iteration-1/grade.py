#!/usr/bin/env python3
"""Decide the kind=file checks of iteration-1 from the files each run left on disk.

Writes script-checks.json ({"<eval>/<cell>/run-<n>": {"<check id>": true|false}}), which
`eval-tools/judge.py table` merges with the judge's verdicts. The checks are the 14 of
kind `file` in ../evals/checks-baseline.json; a check with no rule here fails the script.

Behavior checks import the file the run wrote, in a separate isolated interpreter with a
10 s limit, and call the function with fixed inputs. Anything that goes wrong (missing
file, syntax error, exception, timeout) is a check not met.

Usage: grade.py            grade every run found under eval-*/
       grade.py --self     grade the untouched fixtures, to see the checks discriminate
"""
import ast, io, json, os, re, subprocess, sys, tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
BASE = json.load(open(os.path.join(WS, "evals", "checks-baseline.json")))
FILES = os.path.join(WS, "evals", "files")

RUNNER = r'''
import importlib.util, json, sys
from datetime import date
spec = importlib.util.spec_from_file_location("m", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
out = []
for expr in json.loads(sys.argv[2]):
    try:
        out.append(bool(eval(expr, {"m": m, "date": date})))
    except Exception:
        out.append(False)
print("\n__RESULT__" + json.dumps(out))
'''


def calls(root, rel, exprs):
    """True when every expression holds on the module at root/rel."""
    try:
        p = subprocess.run([sys.executable, "-I", "-B", "-c", RUNNER, rel, json.dumps(exprs)], cwd=root,
                           capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
        got = json.loads(p.stdout.rsplit("__RESULT__", 1)[1])
        return len(got) == len(exprs) and all(got)
    except Exception:
        return False


def text(root, rel):
    try:
        return open(os.path.join(root, rel), encoding="utf-8", newline="").read()
    except OSError:
        return None


def fixture_lines(rel, start=None):
    lines = open(os.path.join(FILES, rel), encoding="utf-8", newline="").read().rstrip("\n").split("\n")
    if start:
        lines = lines[next(i for i, l in enumerate(lines) if l.startswith(start)):]
    return lines


def has_block(root, rel, start=None):
    """The fixture's lines (from the one starting with `start`) are one contiguous block of the file."""
    t = text(root, rel)
    return t is not None and "\n" + "\n".join(fixture_lines(rel, start)) + "\n" in "\n" + t.rstrip("\n") + "\n"


def tree_without_docstrings(src):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) \
                    and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return ast.dump(tree)


def same_code(root, rel):
    t = text(root, rel)
    try:
        return t is not None and tree_without_docstrings(t) == tree_without_docstrings(text(FILES, rel))
    except SyntaxError:
        return False


def has_comment_or_docstring(root, rel):
    t = text(root, rel)
    if t is None:
        return False
    try:
        if any(tok.type == tokenize.COMMENT for tok in tokenize.generate_tokens(io.StringIO(t).readline)):
            return True
        return tree_without_docstrings(t) != ast.dump(ast.parse(t))
    except (SyntaxError, tokenize.TokenError):
        return False


def assigns_d(root, rel):
    t = text(root, rel)
    try:
        fn = next(n for n in ast.walk(ast.parse(t)) if isinstance(n, ast.FunctionDef) and n.name == "summarize")
    except (StopIteration, SyntaxError, TypeError):
        return False
    return any(isinstance(n, ast.Name) and n.id == "d" and isinstance(n.ctx, ast.Store) for n in ast.walk(fn))


SLUG, INV, POLL, USAGE, TTL = "slugs/slugify.py", "billing/invoice.py", "worker/poller.py", "reports/usage.py", "cache/ttl.py"
ROWS = ("[{'account': 'a', 'bytes': 10}, {'account': 'a', 'bytes': -4}, {'account': 'b', 'bytes': 7}, "
        "{'account': 'b', 'bytes': 5}, {'account': 'a', 'bytes': 1}]")
RULES = {
    "1.1": lambda r: calls(r, SLUG, ["m.unique_slug('Olá, Mundo!', set()) == 'ola-mundo'"]),
    "1.2": lambda r: calls(r, SLUG, ["m.unique_slug('Olá, Mundo!', {'ola-mundo'}) == 'ola-mundo-2'",
                                     "m.unique_slug('Olá, Mundo!', {'ola-mundo', 'ola-mundo-2'}) == 'ola-mundo-3'"]),
    "1.7": lambda r: has_block(r, SLUG),
    "2.1": lambda r: calls(r, INV, ["m.due_date(date(2026, 1, 1), 30) == date(2026, 2, 2)",
                                    "m.due_date(date(2026, 1, 2), 30) == date(2026, 2, 2)"]),
    "2.2": lambda r: calls(r, INV, ["m.due_date(date(2026, 1, 5), 30) == date(2026, 2, 4)"]),
    "2.3": lambda r: (text(r, INV) is not None
                      and "Due terms_days calendar days after issue, weekends included." not in text(r, INV)),
    "2.8": lambda r: has_block(r, INV, "def late_fee"),
    "4.1": lambda r: calls(r, POLL, ["m.POLL_INTERVAL_S == 45"]),
    "4.2": lambda r: has_block(r, POLL, "def run("),
    "5.1": lambda r: calls(r, USAGE, [f"m.summarize({ROWS}) == {{'a': 11, 'b': 12}}"]),
    "5.2": lambda r: assigns_d(r, USAGE),
    "5.7": lambda r: has_block(r, USAGE, "def top_accounts"),
    "6.1": lambda r: same_code(r, TTL),
    "6.2": lambda r: has_comment_or_docstring(r, TTL),
}


def grade(ev, root):
    ids = [c["id"] for c in BASE["evals"][ev] if c["kind"] == "file"]
    missing = [i for i in ids if i not in RULES]
    if missing:
        sys.exit(f"no rule for file checks {missing}")
    return {i: bool(RULES[i](root)) for i in ids}


def main():
    if sys.argv[1:] == ["--self"]:
        for ev in BASE["evals"]:
            print(ev, grade(ev, FILES))
        return
    out = {}
    for evdir in sorted(d for d in os.listdir(HERE) if re.match(r"eval-\d+", d)):
        ev = re.match(r"eval-(\d+)", evdir).group(1)
        for cell in sorted(os.listdir(os.path.join(HERE, evdir))):
            for run in sorted(os.listdir(os.path.join(HERE, evdir, cell))):
                root = os.path.join(HERE, evdir, cell, run, "outputs")
                if os.path.isdir(root):
                    out[f"{ev}/{cell}/{run}"] = grade(ev, root)
    json.dump(out, open(os.path.join(HERE, "script-checks.json"), "w"), indent=2)
    met = sum(v for r in out.values() for v in r.values())
    print(f"{len(out)} runs, {met}/{sum(len(r) for r in out.values())} file checks met -> script-checks.json")


if __name__ == "__main__":
    main()
