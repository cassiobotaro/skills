#!/usr/bin/env python3
"""Mechanical assertion checks for the adr eval set.

Covers the assertions that are objectively decidable from the file bytes:
scaffolding language, section order, blank-line discipline, H1/filename number
agreement, slug shape, ISO date. Judgment-bound assertions (prose language,
"nothing invented", question quality) are left to the grader.
"""
import re, sys, os, glob, unicodedata

TODAY = "2026-08-07"
HEADINGS = ["## Status", "## Context", "## Decision", "## Consequences"]
STATUS_WORDS = {"Accepted", "Proposed", "Deprecated"}

def check_adr(path, is_new=True):
    """Return (list_of_failures, list_of_notes) for one ADR file.

    is_new=False marks a pre-existing fixture ADR: its structure is still
    checked, but its Date: is historical and must NOT equal today.
    """
    fails, notes = [], []
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    base = os.path.basename(path)

    # --- filename shape: NNNN-slug.md, slug lowercase alnum + single hyphens
    m = re.match(r"^(\d{4})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$", base)
    if not m:
        fails.append(f"filename does not match NNNN-slug.md with a clean slug: {base}")
        return fails, notes
    file_num = int(m.group(1))
    slug = m.group(2)

    # --- H1 with un-padded number
    if not lines or not lines[0].startswith("# "):
        fails.append("first line is not an H1")
        return fails, notes
    h1 = lines[0][2:]
    hm = re.match(r"^(\d+)\.\s+(.+)$", h1)
    if not hm:
        fails.append(f"H1 is not '# N. Title': {lines[0]!r}")
        return fails, notes
    h1_num, title = int(hm.group(1)), hm.group(2)
    if h1_num != file_num:
        fails.append(f"H1 number {h1_num} != filename number {file_num}")
    if str(h1_num) != hm.group(1):
        fails.append(f"H1 number is zero-padded ({hm.group(1)}); must be un-padded")

    # --- slug derives from the title (ASCII-folded, non-alnum runs -> single hyphen)
    folded = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    expected = re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")
    if slug != expected:
        notes.append(f"slug {slug!r} != strict derivation {expected!r} (check by hand)")

    # --- Date: literal English label, ISO 8601, today
    dm = re.search(r"^Date: (\d{4}-\d{2}-\d{2})$", text, re.M)
    if not dm:
        fails.append("no canonical 'Date: YYYY-MM-DD' line (label must stay English)")
    elif is_new and dm.group(1) != TODAY:
        fails.append(f"date {dm.group(1)} is not today ({TODAY})")
    elif not is_new and dm.group(1) == TODAY:
        fails.append(f"pre-existing fixture ADR had its historical date rewritten to {TODAY}")

    # --- exactly the four canonical headings, in order, nothing else at ##
    found = re.findall(r"^##+ .*$", text, re.M)
    if found != HEADINGS:
        fails.append(f"headings are not exactly {HEADINGS} in order; got {found}")

    # --- no YAML frontmatter
    if text.startswith("---"):
        fails.append("file starts with YAML frontmatter")

    # --- Status section content
    si = text.index("## Status") if "## Status" in text else None
    if si is not None and "## Context" in text:
        status_body = text[si + len("## Status"):text.index("## Context")].strip()
        sl = [l for l in status_body.split("\n") if l.strip()]
        words = [l for l in sl if l.strip() in STATUS_WORDS]
        links = [l for l in sl if re.match(r"^(Supersedes|Superseded by|Amends|Amended by|Clarifies|Clarified by) \[", l.strip())]
        if len(sl) != len(words) + len(links):
            fails.append(f"Status section has unrecognized lines: {sl}")
        if re.search(r"Supercede", status_body):
            fails.append("legacy spelling 'Superceded/Supercedes' written")
        if not words and not links:
            fails.append("Status section is empty")
        for l in links:
            lm = re.match(r"^\S+(?: \S+)? \[(\d+)\. .+\]\(((\d{4})-[a-z0-9-]+\.md)\)$", l.strip())
            if not lm:
                fails.append(f"link line malformed (or href not a bare basename): {l!r}")
            elif "/" in lm.group(2):
                fails.append(f"link href is not a bare basename: {l!r}")
        notes.append(f"status lines: {sl}")

    # --- blank-line discipline: no two consecutive blank lines, no trailing space
    if "\n\n\n" in text:
        fails.append("doubled blank line somewhere in the file")
    for i, l in enumerate(lines, 1):
        if l != l.rstrip():
            fails.append(f"trailing whitespace on line {i}")
            break
    # one blank line after H1 and around headings
    if len(lines) > 1 and lines[1] != "":
        fails.append("no blank line after the H1")
    for h in HEADINGS:
        idx = [i for i, l in enumerate(lines) if l == h]
        for i in idx:
            if i > 0 and lines[i-1] != "":
                fails.append(f"no blank line before {h}")
            if i + 1 < len(lines) and lines[i+1] != "":
                fails.append(f"no blank line after {h}")

    return fails, notes


# eval id -> fixture dir holding the pristine pre-existing ADRs, if any
FIXTURES = {
    "eval-3": "evals/files/session-service",
    "eval-4": "evals/files/api-platform",
    "eval-6": "evals/files/english-log",
}


def preexisting(evaldir, workspace_root):
    """Basenames of ADRs that were seeded as fixtures for this eval."""
    for prefix, fx in FIXTURES.items():
        if os.path.basename(evaldir).startswith(prefix):
            p = os.path.join(workspace_root, fx)
            return {os.path.basename(f) for f in glob.glob(os.path.join(p, "**/*.md"), recursive=True)}
    return set()


def main(root, workspace_root, config="with_skill"):
    total_fail = 0
    for d in sorted(glob.glob(os.path.join(root, "eval-*"))):
        adrs = sorted(glob.glob(os.path.join(d, config, "outputs/**/*.md"), recursive=True))
        seeded = preexisting(d, workspace_root)
        new = [a for a in adrs if os.path.basename(a) not in seeded]
        print(f"\n=== {os.path.basename(d)} — {len(new)} new ADR(s), {len(adrs)-len(new)} pre-existing")
        if not adrs:
            print("   (no ADR written — expected for the 'asks instead of writing' eval)")
            continue
        for a in adrs:
            is_new = os.path.basename(a) not in seeded
            fails, notes = check_adr(a, is_new=is_new)
            rel = os.path.relpath(a, d)
            tag = "new" if is_new else "fixture"
            print(f"  {'FAIL' if fails else 'ok  '}  [{tag}] {rel}")
            for n in notes:
                print(f"          note: {n}")
            for f in fails:
                print(f"          FAIL: {f}")
            total_fail += len(fails)
    print(f"\n{'='*60}\nmechanical failures: {total_fail}")
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ".",
                  sys.argv[2] if len(sys.argv) > 2 else ".",
                  sys.argv[3] if len(sys.argv) > 3 else "with_skill"))
