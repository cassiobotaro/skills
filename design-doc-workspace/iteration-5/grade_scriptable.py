#!/usr/bin/env python3
"""Grade the scriptable assertions for eval-6 (architecture diagram) on a design doc.

Usage: python grade_scriptable.py <path-to-design-doc.md>
Prints a JSON object: {assertion_key: {"passed": bool, "evidence": str}}.
"""
import json
import re
import sys
from pathlib import Path

DISCLAIMER_PATTERNS = [
    r"n[aã]o\s+(?:foram\s+|foi\s+)?validad", # não validado / não foram validados
    r"sem\s+valida[cç][aã]o\s+autom",          # sem validação automática
    r"validad[oa]s?\s+por\s+ferramenta",        # validado por ferramenta
    r"machine[-\s]?validat",                     # machine-validated / machine validation
    r"not\s+validated\s+by\s+a?\s*tool",
    r"n[aã]o\s+validad[oa]s?\s+por\s+ferramenta",
]


def grade(text: str) -> dict:
    results = {}

    # 1. Structurizr DSL present (C4 keywords), not a Mermaid graph for the architecture.
    has_workspace = re.search(r"\bworkspace\b", text) is not None
    has_softwaresystem = re.search(r"softwareSystem", text) is not None
    has_container_kw = re.search(r"(^|\n)\s*\w*\s*=?\s*container\s+\"", text) is not None \
        or re.search(r"\bcontainer\s+\"", text) is not None
    dsl_ok = has_workspace and has_softwaresystem and has_container_kw
    results["structurizr_dsl_present"] = {
        "passed": dsl_ok,
        "evidence": f"workspace={has_workspace}, softwareSystem={has_softwaresystem}, container-keyword={has_container_kw}",
    }

    # 2. <details> fold with <summary>.
    has_details = "<details>" in text and "</details>" in text
    has_summary = "<summary" in text
    results["details_fold_present"] = {
        "passed": has_details and has_summary,
        "evidence": f"<details>={has_details}, <summary>={has_summary}",
    }

    # 3. Markdown image reference (space for the rendered image).
    img = re.search(r"!\[[^\]]*\]\(([^)]+)\)", text)
    img_target = img.group(1) if img else ""
    points_at_image = bool(re.search(r"\.(svg|png|jpg|jpeg|webp)\b", img_target)) or "diagram" in img_target.lower()
    results["rendered_image_reference"] = {
        "passed": img is not None,
        "evidence": (f"image ref -> {img_target!r}" + (" (image-ish path)" if points_at_image else "")) if img else "no markdown image reference found",
    }

    # 4. No machine-validation disclaimer.
    hits = [p for p in DISCLAIMER_PATTERNS if re.search(p, text, re.IGNORECASE)]
    results["no_validation_disclaimer"] = {
        "passed": len(hits) == 0,
        "evidence": "no disclaimer phrasing found" if not hits else f"found disclaimer pattern(s): {hits}",
    }

    return results


def main():
    if len(sys.argv) != 2:
        print("usage: grade_scriptable.py <doc.md>", file=sys.stderr)
        sys.exit(2)
    p = Path(sys.argv[1])
    if not p.exists():
        print(json.dumps({"error": f"file not found: {p}"}))
        sys.exit(1)
    text = p.read_text(encoding="utf-8", errors="replace")
    print(json.dumps(grade(text), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
