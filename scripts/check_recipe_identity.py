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

FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.S)


def main():
    problems = []
    ids = collections.defaultdict(list)
    slashes = collections.defaultdict(list)

    for path in sorted(glob.glob("recipes/*/*/recipe.md")):
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
        slash = front.get("slash_command")
        if slash:
            slashes[slash].append(rid)

    for rid, paths in sorted(ids.items()):
        if len(paths) > 1:
            problems.append(f"duplicate id '{rid}': {', '.join(paths)}")

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

    print(f"{len(ids)} recipes: ids unique, folders match, slash commands unique")
    return 0


if __name__ == "__main__":
    sys.exit(main())
