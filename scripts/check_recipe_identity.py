#!/usr/bin/env python3
"""Identity guard: an id is unique, matches its folder, and owns its slash command.

Three failures this catches, all of which exist in the corpus today or have:

  id != filename      the catalog is keyed by id, the repo is browsed by filename,
                      and a mismatch makes a recipe impossible to find from either.

  duplicate id        the catalog is a map. A duplicate silently drops one recipe.

  duplicate slash     single-metadata enforces slash-command uniqueness per project.
                      302 recipes currently share 227 slash commands, so copying a
                      second recipe that wants /segment-recipe fails for the customer
                      with duplicate_slash_command and no way to resolve it.
"""

import collections
import glob
import pathlib
import re
import sys

import yaml

from recipe_contract import git_front

AUTHOR_REQUIRED = ("name", "last_name")  # llm-wrapper git_validate.AUTHOR_REQUIRED

FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.S)


def main():
    problems = []
    ids = collections.defaultdict(list)
    slashes = collections.defaultdict(list)
    # The deploy key: `frontmatter_id`, else `id` (llm-wrapper git_validate reads it the same
    # way). SM keeps it UNIQUE, so two recipes sharing one could never both deploy.
    deploy_keys = collections.defaultdict(list)

    for path in sorted(glob.glob("recipes/*/*/recipe.md")):
        git = git_front(path)
        if git is not None:
            # Git-validated format: folder = frontmatter_id, an author, and a deploy key
            # no other recipe uses. The rest is llm-wrapper's git_validate check.
            key = str(git["frontmatter_id"])
            folder = pathlib.Path(path).parent.name
            if folder != key:
                problems.append(f"{path}: frontmatter_id '{key}' does not match its folder '{folder}'")
            author = git.get("author")
            missing = [k for k in AUTHOR_REQUIRED if not (isinstance(author, dict) and str(author.get(k) or "").strip())]
            if missing:
                problems.append(f"{path}: author is missing {', '.join(missing)}")
            # The draft/ flow writes recipes/<author.org_name>/<frontmatter_id>/ (R-RG4-7/9).
            owner = str(author.get("org_name") or "").strip() if isinstance(author, dict) else ""
            held_by = pathlib.Path(path).parent.parent.name
            if owner != held_by:
                problems.append(f"{path}: author.org_name '{owner}' does not match its owner folder '{held_by}'")
            deploy_keys[key].append(path)
            slash = git.get("slash_command")
            if slash:
                slashes[slash].append(key)
            continue
        text = pathlib.Path(path).read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            problems.append(f"{path}: no YAML frontmatter")
            continue
        try:
            front = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            problems.append(f"{path}: unparseable frontmatter: {exc}")
            continue

        rid = front.get("id")
        if not rid:
            problems.append(f"{path}: id is missing")
            continue

        folder = pathlib.Path(path).parent.name
        if folder != rid:
            problems.append(f"{path}: id '{rid}' does not match its folder '{folder}'")

        ids[rid].append(path)
        deploy_keys[front.get("frontmatter_id") or rid].append(path)
        slash = front.get("slash_command")
        if slash:
            slashes[slash].append(rid)

    for rid, paths in sorted(ids.items()):
        if len(paths) > 1:
            problems.append(f"duplicate id '{rid}': {', '.join(paths)}")

    for key, paths in sorted(deploy_keys.items()):
        if len(paths) > 1:
            problems.append(f"duplicate deploy key (frontmatter_id, else id) '{key}': {', '.join(paths)}")

    for slash, owners in sorted(slashes.items()):
        if len(owners) > 1:
            problems.append(
                f"duplicate slash_command '{slash}' on {len(owners)} recipes: "
                + ", ".join(sorted(owners)[:5])
                + (" ..." if len(owners) > 5 else "")
            )

    if problems:
        print(f"{len(problems)} identity problem(s):", file=sys.stderr)
        for line in problems[:40]:
            print(f"  {line}", file=sys.stderr)
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more", file=sys.stderr)
        return 1

    print(f"{len(ids)} recipes: ids unique, folders match, deploy keys unique, slash commands unique")
    return 0


if __name__ == "__main__":
    sys.exit(main())
