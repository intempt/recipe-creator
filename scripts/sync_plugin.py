#!/usr/bin/env python3
import argparse
import json
import pathlib
import posixpath
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = pathlib.Path("plugin/skills/intempt-recipe-author")

MIRRORS = {
    "references/recipe-contract.md": "references/recipe-contract.md",
    "references/entities.md": "references/entities.md",
    "WRITING-STEPS.md": "references/writing-steps.md",
    "NO-ENTITY-EXISTS.md": "references/no-entity-exists.md",
    "SUBMITTING.md": "references/submitting.md",
    "VALIDATION.md": "references/validation.md",
    "PREREQUISITES.md": "references/prerequisites.md",
    "RECIPE-TEMPLATE.md": "references/recipe-template.md",
    "workflows/idea-to-recipe.md": "references/idea-to-recipe.md",
    "workflows/workspace-to-recipe.md": "references/workspace-to-recipe.md",
    "workflows/existing-recipe.md": "references/existing-recipe.md",
    "examples/intempt/trial-expiring-nudge/recipe.md": "references/examples/intempt/trial-expiring-nudge/recipe.md",
    "scripts/recipe_contract.py": "scripts/recipe_contract.py",
    "scripts/validate_recipes.py": "scripts/validate_recipes.py",
}

MANIFESTS = (
    "plugin/.claude-plugin/plugin.json",
    "plugin/.codex-plugin/plugin.json",
    "plugin/.cursor-plugin/plugin.json",
)

LINK = re.compile(r"\]\(([^)#\s]+)(#[^)]*)?\)")
REPO_URL = "https://github.com/intempt/recipe-creator/blob/main/"


def relink(text, source, destination):
    source_dir = posixpath.dirname(source)
    destination_dir = posixpath.dirname(destination)

    def swap(match):
        target, anchor = match.group(1), match.group(2) or ""
        if "://" in target or target.startswith("mailto:"):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(source_dir, target))
        if resolved in MIRRORS:
            new = posixpath.relpath(MIRRORS[resolved], destination_dir or ".")
        else:
            new = REPO_URL + resolved
        return f"]({new}{anchor})"

    return LINK.sub(swap, text)


def wanted(source, destination):
    text = (ROOT / source).read_text(encoding="utf-8")
    if source.endswith(".md") and not source.endswith("/recipe.md"):
        text = relink(text, source, destination)
    return text


def version_problems():
    problems = []
    versions = {}
    for manifest in MANIFESTS:
        versions[manifest] = json.loads((ROOT / manifest).read_text(encoding="utf-8")).get("version")
    if len(set(versions.values())) != 1:
        problems.append("plugin manifests disagree on version: " + ", ".join(f"{k} {v}" for k, v in versions.items()))
    skill = (ROOT / SKILL / "SKILL.md").read_text(encoding="utf-8")
    announced = re.search(r"intempt-recipe-author/([0-9.]+)", skill)
    declared = next(iter(versions.values()))
    if not announced or announced.group(1) != declared:
        problems.append(f"SKILL.md announces {announced.group(1) if announced else 'no version'}, manifests declare {declared}")
    return problems


def main():
    parser = argparse.ArgumentParser(description="Copy the root references and validator into the plugin.")
    parser.add_argument("--check", action="store_true", help="Fail if any copy differs instead of writing.")
    args = parser.parse_args()

    stale = []
    for source, destination in MIRRORS.items():
        target = ROOT / SKILL / destination
        text = wanted(source, destination)
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current == text:
            continue
        if args.check:
            stale.append(str(SKILL / destination))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            stale.append(str(SKILL / destination))

    problems = version_problems()
    for problem in problems:
        print(problem, file=sys.stderr)

    if args.check:
        if stale:
            print(f"{len(stale)} plugin cop(ies) differ from the root:", file=sys.stderr)
            for path in stale:
                print(f"  {path}", file=sys.stderr)
            print("Run scripts/sync_plugin.py and commit the result.", file=sys.stderr)
        if stale or problems:
            return 1
        print(f"{len(MIRRORS)} plugin copies match the root; manifests and SKILL.md agree on the version")
        return 0
    print(f"{len(stale)} plugin cop(ies) written")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
