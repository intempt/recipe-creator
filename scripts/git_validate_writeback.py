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

The description ends up in BOTH files (Beso 2026-10-07): an answer with no
description, or an md whose frontmatter cannot take one, is a failure, and
neither file is written for that recipe.

The md edit is a line insert, never a YAML re-dump: key order, comments,
folded `>-` blocks and the body stay byte-for-byte as they were. A
`description:` the author set — any value, even empty — is never touched.
`classification.industry` is returned by validation only; it is not written
into the md (RG1 §57).

Which recipe.md an answer belongs to is NOT read from the md: job 1 writes
DIR/<f_id>.path, the file it sent. The frontmatter is located the way LM's
git_validate._FRONTMATTER locates it — an optional BOM and blank lines may
come before the opening `---` — so a file LM accepted is a file this edits.

Usage:
  git_validate_writeback.py DIR      # DIR = job 1's --out directory
Prints each file it wrote; exit 0 done (also when nothing to write), 1 when
any recipe could not be written back.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

FENCE = re.compile(r"^---\s*$")
TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*)\s*:")


def _frontmatter_span(lines: list[str]) -> tuple[int, int] | None:
    """(index of the opening `---`, index of the closing one), or None.
    A BOM and blank lines before the opening fence are skipped, as LM's
    git_validate._FRONTMATTER skips them."""
    lines = [lines[0].lstrip("\ufeff")] + lines[1:] if lines else lines
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i == len(lines) or not FENCE.match(lines[i]):
        return None
    for j in range(i + 1, len(lines)):
        if FENCE.match(lines[j]):
            return i, j
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
    newline = "\r\n" if lines[start].endswith("\r\n") else "\n"
    entry = "description: " + json.dumps(description, ensure_ascii=False) + newline
    return "".join(lines[:at]) + entry + "".join(lines[at:])


def write_back(pairs: list[tuple[dict, str]]) -> tuple[list[str], list[str]]:
    """Write recipe.json (+ the md description when absent) for each
    (answer, recipe.md path). Returns (files written, problems)."""
    written, problems = [], []
    for answer, md in pairs:
        f_id = str(answer.get("f_id") or "(no f_id)")
        description = " ".join(str(answer.get("description") or "").split())
        if not description:
            problems.append(f"{f_id}: the answer has no description ({md})")
            continue
        try:
            with open(md, encoding="utf-8", newline="") as fh:
                text = fh.read()
        except OSError as e:
            problems.append(f"{f_id}: cannot read {md} ({e.strerror})")
            continue
        new = insert_description(text, description)
        if new == text and not has_description(text):
            problems.append(f"{f_id}: no frontmatter in {md} to put the description in")
            continue
        out = os.path.join(os.path.dirname(md), "recipe.json")
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(answer, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        written.append(out)
        if new != text:
            with open(md, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
            written.append(md)
    return written, problems


def load(out_dir: str) -> tuple[list[tuple[dict, str]], list[str]]:
    """Job 1's DIR: each <f_id>.json with the md path in its <f_id>.path."""
    pairs, problems = [], []
    for path in sorted(glob.glob(os.path.join(out_dir, "*.json"))):
        with open(path, encoding="utf-8") as fh:
            answer = json.load(fh)
        side = path[:-len(".json")] + ".path"
        try:
            with open(side, encoding="utf-8") as fh:
                md = fh.read().strip()
        except FileNotFoundError:
            md = ""
        if not md:
            problems.append(f"{os.path.basename(path)}: job 1 recorded no recipe.md path")
            continue
        pairs.append((answer, md))
    return pairs, problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="job 1's --out directory (<f_id>.json + <f_id>.path per passing recipe)")
    args = ap.parse_args()

    pairs, problems = load(args.dir)
    if not pairs and not problems:
        print("No validated recipe — nothing to write back.")
        return 0
    written, more = write_back(pairs)
    problems += more
    for path in written:
        print(f"WROTE {path}")
    for p in problems:
        print(f"FAIL  {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
