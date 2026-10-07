#!/usr/bin/env python3
"""
After a pull request's git Validate passes (job 1 checked, job 2 ran), write
what it produced back beside each recipe, for the PR head branch to commit:

  recipes/<category>/<slug>/recipe.json   job 1's answer, verbatim — the object
                                           job 2 ran and the deploy tags send
                                           to SM (recipe_deploy.py)
  recipes/<category>/<slug>/recipe.md      ONLY when its frontmatter has no
                                           `description:` — one line
                                           `description: "<generated>"` is
                                           inserted after the `title:` entry

The md edit is a line insert, never a YAML re-dump: key order, comments,
folded `>-` blocks and the body stay byte-for-byte as they were. A
`description:` the author set — any value, even empty — is never touched.
`classification.industry` is returned by validation only; it is not written
into the md (RG1 §57).

Which recipe.md an answer belongs to is read from the same frontmatter key LM's
git_validate reads (`f_id`, else `id`), among the recipes the PR changed — the
same list job 1 sent.

Usage:
  git_validate_writeback.py DIR --base <ref>     # DIR = job 1's --out directory
  git_validate_writeback.py DIR recipe.md ...    # explicit files
Prints each file it wrote; exit 0 done (also when nothing to write), 1 an
answer matched no changed recipe or more than one.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

import yaml

FENCE = re.compile(r"^---\s*$")
TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*)\s*:")


def _frontmatter_span(lines: list[str]) -> tuple[int, int] | None:
    """(index of the opening `---`, index of the closing one), or None."""
    if not lines or not FENCE.match(lines[0]):
        return None
    for i in range(1, len(lines)):
        if FENCE.match(lines[i]):
            return 0, i
    return None


def has_description(text: str) -> bool:
    """True when the frontmatter has a top-level `description:` key, whatever its value."""
    lines = text.splitlines(keepends=True)
    span = _frontmatter_span(lines)
    if span is None:
        return False
    return any((m := TOP_KEY.match(ln)) and m.group(1) == "description"
               for ln in lines[span[0] + 1:span[1]])


def insert_description(text: str, description: str) -> str:
    """`text` with `description: "<description>"` inserted after the frontmatter's
    `title:` entry (its line and any indented continuation). Unchanged — the
    same string — when a description is already there, when there is no
    frontmatter, or when the description is empty. No `title:` → inserted
    just before the closing `---`."""
    description = " ".join(str(description or "").split())
    if not description or has_description(text):
        return text
    lines = text.splitlines(keepends=True)
    span = _frontmatter_span(lines)
    if span is None:
        return text
    start, end = span
    at = end
    for i in range(start + 1, end):
        m = TOP_KEY.match(lines[i])
        if m and m.group(1) == "title":
            at = i + 1
            while at < end and lines[at][:1] in (" ", "\t"):
                at += 1
            break
    newline = "\r\n" if lines[0].endswith("\r\n") else "\n"
    entry = "description: " + json.dumps(description, ensure_ascii=False) + newline
    return "".join(lines[:at]) + entry + "".join(lines[at:])


def f_id_of(text: str) -> str:
    """Frontmatter `f_id`, else `id` — LM git_validate.f_id_of. '' when neither."""
    lines = text.splitlines(keepends=True)
    span = _frontmatter_span(lines)
    if span is None:
        return ""
    try:
        meta = yaml.safe_load("".join(lines[span[0] + 1:span[1]]))
    except yaml.YAMLError:
        return ""
    if not isinstance(meta, dict):
        return ""
    for key in ("f_id", "id"):
        v = meta.get(key)
        if isinstance(v, (str, int)) and not isinstance(v, bool) and str(v).strip():
            return str(v).strip()
    return ""


def write_back(answers: list[dict], md_paths: list[str]) -> tuple[list[str], list[str]]:
    """Write recipe.json (+ the md description when absent) for each answer.
    Returns (files written, problems)."""
    by_f_id: dict[str, list[str]] = {}
    for path in md_paths:
        with open(path, encoding="utf-8", newline="") as fh:
            by_f_id.setdefault(f_id_of(fh.read()), []).append(path)
    written, problems = [], []
    for answer in answers:
        f_id = str(answer.get("f_id") or "")
        paths = by_f_id.get(f_id, []) if f_id else []
        if len(paths) != 1:
            problems.append(f"{f_id or '(no f_id)'}: matches {len(paths)} changed recipe.md "
                            f"{'(' + ', '.join(paths) + ')' if paths else ''}".rstrip())
            continue
        md = paths[0]
        out = os.path.join(os.path.dirname(md), "recipe.json")
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(answer, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        written.append(out)
        with open(md, encoding="utf-8", newline="") as fh:
            text = fh.read()
        new = insert_description(text, answer.get("description") or "")
        if new != text:
            with open(md, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
            written.append(md)
    return written, problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="job 1's --out directory (one <f_id>.json per passing recipe)")
    ap.add_argument("files", nargs="*", help="recipe.md files (default: changed since --base)")
    ap.add_argument("--base", help="git ref to diff against (merge-base), as job 1")
    args = ap.parse_args()

    answers = []
    for path in sorted(glob.glob(os.path.join(args.dir, "*.json"))):
        with open(path, encoding="utf-8") as fh:
            answers.append(json.load(fh))
    if not answers:
        print("No validated recipe — nothing to write back.")
        return 0
    if args.files:
        md_paths = args.files
    elif args.base:
        import git_validate_recipes  # only for changed_recipes; keeps tests free of git
        md_paths = git_validate_recipes.changed_recipes(args.base)
    else:
        md_paths = []

    written, problems = write_back(answers, md_paths)
    for path in written:
        print(f"WROTE {path}")
    for p in problems:
        print(f"FAIL  {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
