#!/usr/bin/env python3
"""
A git-format recipe is two files CI writes together (the draft/ flow, R-RG4-6):
recipes/<owner>/<frontmatter_id>/recipe.md and recipe.json. The deploy sends the json
and people read the md, so they must say the same thing:

  - both exist (an md without its json, or a json without its md, is half a recipe)
  - same frontmatter_id, slash_command, description and author
  - the folder is recipes/<author.org_name>/<frontmatter_id>/

Contract recipes (front matter `id:`, no recipe.json) are not this format and are
left to the contract checks. Used by the write-back (job 3) on what it wrote, and by
recipe-prerequisites.yml on the whole tree.

Usage:
  check_recipe_consistency.py            # every git-format recipe under recipes/
  check_recipe_consistency.py DIR ...    # these recipe folders
Exit 0 consistent, 1 not.
"""
from __future__ import annotations

import glob
import json
import os
import sys

from recipe_contract import git_front

FIELDS = ("frontmatter_id", "slash_command", "description", "author")


def check(folder: str) -> list[str]:
    """Problems with one recipes/<owner>/<key>/ folder; [] when it is consistent
    or is not a git-format recipe."""
    md = os.path.join(folder, "recipe.md")
    js = os.path.join(folder, "recipe.json")
    front = git_front(md) if os.path.exists(md) else None
    if front is None:
        if os.path.exists(js):
            return [f"{js}: has no git-format recipe.md beside it"]
        return []
    if not os.path.exists(js):
        return [f"{md}: has no recipe.json beside it"]
    try:
        with open(js, encoding="utf-8") as fh:
            record = json.load(fh)
    except ValueError as e:
        return [f"{js}: not JSON ({e})"]
    if not isinstance(record, dict):
        return [f"{js}: not a JSON object"]
    problems = []
    for field in FIELDS:
        a, b = front.get(field), record.get(field)
        if field != "author":
            a = None if a is None else str(a)
            b = None if b is None else str(b)
        if a != b:
            problems.append(f"{folder}: {field} differs — recipe.md {a!r}, recipe.json {b!r}")
    author = front.get("author") if isinstance(front.get("author"), dict) else {}
    owner = str(author.get("org_name") or "")
    want = os.path.join("recipes", owner, str(front.get("frontmatter_id") or ""))
    if os.path.normpath(os.path.abspath(folder)).split(os.sep)[-3:] != want.split(os.sep):
        problems.append(f"{folder}: should be {want}/ (recipes/<author.org_name>/<frontmatter_id>/)")
    return problems


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    folders = args or sorted(p.rstrip("/\\") for p in glob.glob(os.path.join("recipes", "*", "*", "")))
    problems, checked = [], 0
    for folder in folders:
        found = check(folder)
        problems += found
        checked += os.path.exists(os.path.join(folder, "recipe.json")) or bool(found)
    if problems:
        print(f"{len(problems)} recipe.md / recipe.json problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1
    print(f"{checked} git-format recipe(s): recipe.md and recipe.json agree, folders match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
