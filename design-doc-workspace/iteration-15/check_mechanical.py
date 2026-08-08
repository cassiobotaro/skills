#!/usr/bin/env python3
"""Mechanical checks for the design-doc iteration-15 regression (skill 1.3.4).

Decides only what is reducible to bytes. Prose judgement — "nothing invented",
whether a trade-off is really stated, whether a question is a good question —
stays with the grader.

The exclusivity sweep is the point of this run: 1.3.4 generalized contract 2's
superlative list away from its Portuguese-only wording, so the failure mode it
guards against (writing an unstated absence down as fact) has to stay closed.
Hits are NOT failures by themselves; each one gets adjudicated by hand. The
script's job is to make sure none is missed.

Usage: python check_mechanical.py [iteration_dir]
"""

import json
import pathlib
import re
import sys

ITER = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

# Exclusivity / universality claims, PT + EN. Contract 2 calls these "the shape
# an unstated absence takes when you write it down as fact".
EXCLUSIVITY = re.compile(
    r"\b(únic[ao]s?|apenas|somente|sempre|nunca|nenhum[ao]?s?|todo|toda|todos|todas"
    r"|the only|the sole|the single|always|never|no other)\b",
    re.IGNORECASE,
)

# A validation disclaimer is banned (eval 6): manual review is assumed.
DISCLAIMER = re.compile(
    r"(não\s+(foi\s+)?validad|nao\s+validad|not\s+machine-validated|ilustraç[ãa]o\s+do\s+texto"
    r"|meramente\s+ilustrativ|not\s+validated)",
    re.IGNORECASE,
)

PT_MARKERS = re.compile(r"\b(de|para|que|não|com|uma|dos|pelo|será|serviço)\b", re.IGNORECASE)


def docs_of(eval_dir: pathlib.Path):
    """Markdown the run produced, excluding its saved chat reply."""
    out = eval_dir / "with_skill" / "outputs"
    repo = eval_dir / "repo"
    found = []
    for base in (out, repo):
        if base.is_dir():
            found += [p for p in base.rglob("*.md") if p.name != "response.md"]
    return sorted(set(found))


def check(eval_dir: pathlib.Path) -> dict:
    name = eval_dir.name
    docs = docs_of(eval_dir)
    reply = eval_dir / "with_skill" / "outputs" / "response.md"
    reply_text = reply.read_text(encoding="utf-8") if reply.exists() else ""
    body = "\n".join(p.read_text(encoding="utf-8") for p in docs)

    r = {
        "eval": name,
        "documents": [str(p.relative_to(ITER)) for p in docs],
        "reply_saved": reply.exists(),
        "doc_chars": len(body),
    }

    # Language: the conversation is Portuguese in every eval of this set.
    r["doc_is_portuguese"] = bool(PT_MARKERS.search(body)) if body else None
    r["reply_is_portuguese"] = bool(PT_MARKERS.search(reply_text))

    # Exclusivity claims — adjudicate each hit by hand.
    hits = []
    for src, text in (("doc", body), ("reply", reply_text)):
        for m in EXCLUSIVITY.finditer(text):
            a, b = max(0, m.start() - 90), min(len(text), m.end() + 90)
            hits.append({"where": src, "term": m.group(0),
                         "context": " ".join(text[a:b].split())})
    r["exclusivity_hits"] = hits
    r["exclusivity_count"] = len(hits)

    # Banned validation disclaimer.
    r["validation_disclaimer"] = [m.group(0) for m in DISCLAIMER.finditer(body)]

    # Diagram accounting: every diagram must be followed by prose, and the C4
    # view is Structurizr DSL folded under an image reference, never Mermaid.
    r["mermaid_blocks"] = len(re.findall(r"```mermaid", body))
    r["details_blocks"] = len(re.findall(r"<details>", body))
    r["image_refs"] = len(re.findall(r"!\[[^\]]*\]\([^)]*\)", body))
    r["dsl_workspace_blocks"] = len(re.findall(r"\bworkspace\s*\{", body))

    # Orphan-diagram heuristic: text between a fence's close and the next
    # heading. Reported for the grader to confirm, not scored here.
    orphans = []
    for m in re.finditer(r"```mermaid.*?```|</details>", body, re.S):
        after = body[m.end():m.end() + 400].strip()
        first = after.split("\n", 1)[0].strip()
        if not after or first.startswith("#") or first.startswith("!["):
            orphans.append(body[max(0, m.start() - 60):m.start()].split("\n")[-1][:60])
    r["possible_orphan_diagrams"] = orphans

    return r


def main():
    evals = sorted(p for p in ITER.iterdir() if p.is_dir() and p.name.startswith("eval-"))
    results = [check(e) for e in evals]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print("\n=== summary ===", file=sys.stderr)
    for r in results:
        print(
            f"{r['eval']:52} docs={len(r['documents'])} "
            f"excl={r['exclusivity_count']:3} disclaimer={len(r['validation_disclaimer'])} "
            f"mermaid={r['mermaid_blocks']} details={r['details_blocks']} "
            f"orphans={len(r['possible_orphan_diagrams'])}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
