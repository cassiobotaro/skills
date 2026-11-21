#!/usr/bin/env python3
"""Check the repository's own rules, the ones `claude plugin validate` does not.

    scripts/validate.py                 before committing: the working tree against HEAD
    scripts/validate.py --base <rev>    in CI: HEAD against the commit the push started from

What it checks, per plugin listed in `.claude-plugin/marketplace.json`:

- the marketplace entry carries no `version`, its `source` holds a `plugin.json` with the
  same `name` and the same `description`, and no plugin directory is left out of the list;
- each `skills/<name>/SKILL.md` has frontmatter whose `name` is the directory name and whose
  `description` is present and within the 1024 characters the Agent Skills spec allows;
- every `references/` file a skill names exists, and every file under `references/` is named
  in its `SKILL.md` (a file the body never points at is never loaded);
- no file under `skills/` names a `*-workspace/` path;
- a plugin whose `skills/` changed since `--base` has a higher `version` in `plugin.json`.

Standard library only, so it runs the same on a laptop and on a bare CI runner. The
frontmatter reader handles the YAML these files use (`key: value`, and `key: >` or `key: |`
blocks) and reports anything else instead of guessing.

The last line counts what was checked. A pass that checked nothing reads the same as a pass
that checked everything, unless the counts are printed.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DESCRIPTION_LIMIT = 1024  # https://agentskills.io/specification
NAME_LIMIT = 64
NAME_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
REFERENCE_MENTION = re.compile(r"references/[A-Za-z0-9._-]*[A-Za-z0-9]")
# `adr-workspace/...`, not Structurizr's `-workspace workspace.dsl` flag or "multi-workspace".
WORKSPACE_PATH = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*-workspace/")
KEY_LINE = re.compile(r"([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]+(.*))?$")
NULL_SHA = re.compile(r"0{40,}")


class FrontmatterError(Exception):
    pass


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def fold(lines: list[str]) -> str:
    """A `>` block: lines join with a space, a blank line is a line break."""
    paragraphs, current = [], []
    for line in lines:
        if line.strip():
            current.append(line.strip())
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n".join(paragraphs)


def read_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("no frontmatter: the file does not start with ---")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        raise FrontmatterError("frontmatter is never closed with ---") from None

    fields: dict[str, str] = {}
    body = lines[1:end]
    i = 0
    while i < len(body):
        line = body[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        match = KEY_LINE.match(line)
        if not match:
            raise FrontmatterError(f"cannot read frontmatter line {i + 2}: {line!r}")
        key, value = match.group(1), (match.group(2) or "").strip()
        i += 1
        block = []
        while i < len(body) and (not body[i].strip() or body[i][0] in " \t"):
            block.append(body[i])
            i += 1
        if key in fields:
            raise FrontmatterError(f"frontmatter key {key!r} appears twice")
        if value[:1] in (">", "|"):
            if value.rstrip("+-0123456789") not in (">", "|"):
                raise FrontmatterError(f"cannot read the block header of {key!r}: {value!r}")
            fields[key] = fold(block) if value[0] == ">" else "\n".join(b.strip() for b in block).strip()
        elif value:
            # A plain scalar may continue on indented lines.
            fields[key] = unquote(" ".join([value, *(b.strip() for b in block if b.strip())]))
        else:
            fields[key] = "\n".join(block)  # a nested mapping or list: kept raw, not interpreted
    return fields


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def version_key(version: str) -> tuple[int, ...] | None:
    if not re.fullmatch(r"\d+(\.\d+)*", version):
        return None
    return tuple(int(part) for part in version.split("."))


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")


def load_json(path: Path, report: Report, root: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(str(path.relative_to(root)), "file not found")
    except json.JSONDecodeError as exc:
        report.error(str(path.relative_to(root)), f"not valid JSON ({exc})")
    return None


def check_marketplace(root: Path, report: Report) -> dict[str, Path]:
    """Returns the plugin directories by plugin name."""
    where = ".claude-plugin/marketplace.json"
    marketplace = load_json(root / where, report, root)
    if marketplace is None:
        return {}
    plugins: dict[str, Path] = {}
    for entry in marketplace.get("plugins", []):
        name = entry.get("name", "<unnamed>")
        if "version" in entry:
            report.error(where, f"plugin {name!r} has a version; it lives only in plugin.json")
        source = entry.get("source")
        if not isinstance(source, str):
            report.error(where, f"plugin {name!r} has no local source directory")
            continue
        directory = (root / source).resolve()
        manifest_path = directory / ".claude-plugin/plugin.json"
        manifest = load_json(manifest_path, report, root) if directory.is_dir() else None
        if not directory.is_dir():
            report.error(where, f"plugin {name!r} points at {source}, which is not a directory")
        if manifest is None:
            continue
        manifest_where = str(manifest_path.relative_to(root))
        if manifest.get("name") != name:
            report.error(manifest_where, f"name {manifest.get('name')!r} differs from the marketplace entry {name!r}")
        if manifest.get("description") != entry.get("description"):
            report.error(manifest_where, "description differs from the marketplace entry (the two showcase texts must match)")
        if version_key(str(manifest.get("version", ""))) is None:
            report.error(manifest_where, f"version {manifest.get('version')!r} is missing or not dotted numbers")
        plugins[name] = directory

    listed = {path.resolve() for path in plugins.values()}
    for manifest_path in sorted(root.glob("*/.claude-plugin/plugin.json")):
        if manifest_path.parent.parent.resolve() not in listed:
            report.error(str(manifest_path.relative_to(root)), "plugin is not listed in .claude-plugin/marketplace.json")
    return plugins


def check_skill(root: Path, skill_dir: Path, report: Report) -> int:
    """Returns the number of reference files checked."""
    skill_md = skill_dir / "SKILL.md"
    where = str(skill_md.relative_to(root))
    text = skill_md.read_text(encoding="utf-8")
    try:
        fields = read_frontmatter(text)
    except FrontmatterError as exc:
        report.error(where, str(exc))
        fields = {}
    else:
        name = fields.get("name", "")
        if name != skill_dir.name:
            report.error(where, f"frontmatter name {name!r} does not match the directory {skill_dir.name!r}")
        elif len(name) > NAME_LIMIT or not NAME_PATTERN.fullmatch(name):
            report.error(where, f"name {name!r} is not lowercase letters, digits and single hyphens, at most {NAME_LIMIT}")
        description = fields.get("description", "").strip()
        if not description:
            report.error(where, "frontmatter has no description")
        elif len(description) > DESCRIPTION_LIMIT:
            report.error(
                where,
                f"description is {len(description)} characters; the Agent Skills spec allows {DESCRIPTION_LIMIT} "
                f"({len(description) - DESCRIPTION_LIMIT} over)",
            )

    references = sorted(p for p in (skill_dir / "references").glob("**/*") if p.is_file())
    named_in_skill = set(REFERENCE_MENTION.findall(text))
    for path in references:
        relative = path.relative_to(skill_dir).as_posix()
        if relative not in named_in_skill:
            report.error(where, f"{relative} exists but SKILL.md never names it, so nothing says when to read it")

    for path in sorted(p for p in skill_dir.glob("**/*") if p.is_file()):
        file_where = str(path.relative_to(root))
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix == ".md":
            for mention in sorted(set(REFERENCE_MENTION.findall(content))):
                if not (skill_dir / mention).is_file():
                    report.error(file_where, f"names {mention}, which does not exist in the skill")
        for number, line in enumerate(content.splitlines(), 1):
            found = WORKSPACE_PATH.search(line)
            if found:
                report.error(f"{file_where}:{number}", f"names a workspace path ({found.group(0)}); workspaces are not installed with the skill")
    return len(references)


def check_versions(root: Path, plugins: dict[str, Path], base: str, report: Report) -> str:
    """Returns a description of what the version check compared."""
    if NULL_SHA.fullmatch(base):
        report.notes.append("version check skipped: the push has no earlier commit (a new branch)")
        return "skipped"
    if git(root, "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}").returncode != 0:
        report.notes.append(f"version check skipped: {base} is not a commit in this clone (a force push, or a shallow clone)")
        return "skipped"
    merge_base = git(root, "merge-base", base, "HEAD")
    start = merge_base.stdout.strip() if merge_base.returncode == 0 and merge_base.stdout.strip() else base

    changed_plugins = 0
    for name, directory in sorted(plugins.items()):
        relative = directory.relative_to(root).as_posix()
        # Against the working tree, so that an uncommitted edit counts before the commit is made.
        tracked = git(root, "diff", "--name-only", start, "--", f"{relative}/skills").stdout.split()
        untracked = git(root, "ls-files", "--others", "--exclude-standard", "--", f"{relative}/skills").stdout.split()
        changed = tracked + untracked
        if not changed:
            continue
        changed_plugins += 1
        manifest_where = f"{relative}/.claude-plugin/plugin.json"
        before = git(root, "show", f"{start}:{manifest_where}")
        if before.returncode != 0:
            continue  # the plugin did not exist at the base: any version is its first
        try:
            old = str(json.loads(before.stdout).get("version", ""))
            new = str(json.loads((root / manifest_where).read_text(encoding="utf-8")).get("version", ""))
        except json.JSONDecodeError:
            continue  # reported by check_marketplace
        old_key, new_key = version_key(old), version_key(new)
        if old_key is None or new_key is None or new_key <= old_key:
            report.error(
                manifest_where,
                f"version is {new} and was {old} at {start[:9]}, but {len(changed)} file(s) under "
                f"{relative}/skills changed (first: {changed[0]}); bump it",
            )
    return f"{changed_plugins} plugin(s) changed since {start[:9]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="HEAD", help="Commit to compare versions against (default: HEAD, i.e. the uncommitted changes)")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help="Repository root (default: this script's)")
    args = parser.parse_args()
    root = args.root.resolve()

    report = Report()
    plugins = check_marketplace(root, report)
    skills = references = 0
    for name, directory in sorted(plugins.items()):
        skill_dirs = sorted(p.parent for p in directory.glob("skills/*/SKILL.md"))
        if not skill_dirs:
            report.error(directory.relative_to(root).as_posix(), "plugin has no skills/<name>/SKILL.md")
        for skill_dir in skill_dirs:
            skills += 1
            references += check_skill(root, skill_dir, report)
    versions = check_versions(root, plugins, args.base, report) if plugins else "skipped"

    for note in report.notes:
        print(f"note: {note}")
    for error in report.errors:
        print(f"ERROR {error}")
    print(
        f"{'FAILED' if report.errors else 'ok'}: {len(report.errors)} error(s); checked {len(plugins)} plugin(s), "
        f"{skills} skill(s), {references} reference file(s); versions: {versions}"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
