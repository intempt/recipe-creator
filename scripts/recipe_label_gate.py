#!/usr/bin/env python3
"""
The PR gate of the draft/ flow (R-RG4-6), run on every pull request to staging.
An author's PR adds or changes only `draft/*.md`; CI writes recipes/ for them. So:

  1. A commit in the PR that touches recipes/ must be the write-back bot's
     (recipe_draft.BOT_EMAIL as author AND committer). A person's commit there fails:
     recipes/ is generated, and a hand edit would skip the step check and the run.
  2. A draft in the tree fails. Without the `validate-recipes` label the message says
     a reviewer adds it; with the label the git Validate jobs are running, and their
     write-back deletes the draft and posts this check green on its own commit.

Merge commits are not counted (a merge of staging brings staging's own recipes/).

Usage:
  recipe_label_gate.py --base origin/staging --labels '["a","b"]'
Exit 0 = pass; 1 = a person touched recipes/, or a draft is waiting.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

import recipe_draft

LABEL = "validate-recipes"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def person_commits(base: str) -> list[str]:
    """`<sha> <author email>` of each non-merge commit in base..HEAD that touches
    recipes/ and was not made by the write-back bot."""
    out = _git("log", "--no-merges", "--format=%H%x00%ae%x00%ce", f"{base}..HEAD", "--", "recipes/")
    found = []
    for line in out.splitlines():
        sha, author, committer = (line.split("\0") + ["", ""])[:3]
        if author != recipe_draft.BOT_EMAIL or committer != recipe_draft.BOT_EMAIL:
            found.append(f"{sha[:10]} {author}")
    return found


def drafts_in_tree() -> list[str]:
    return sorted(p for p in _git("ls-files", "--", recipe_draft.DRAFT_DIR + "/").splitlines()
                  if recipe_draft.is_draft(p))


def verdict(people: list[str], drafts: list[str], labels: list[str]) -> tuple[int, str]:
    problems = []
    if people:
        problems.append(
            f"{len(people)} commit(s) by a person change recipes/, which CI writes from draft/. "
            "Put the recipe in draft/<name>.md instead (draft/README.md):\n  " + "\n  ".join(people))
    if drafts and LABEL not in labels:
        problems.append(
            f"{len(drafts)} draft(s) wait for git Validate. A reviewer adds the {LABEL!r} label "
            "to run it:\n  " + "\n  ".join(drafts))
    elif drafts:
        problems.append(
            f"{len(drafts)} draft(s) are being validated. The write-back commit deletes them, "
            "writes recipes/, and reports this check green on its own commit:\n  " + "\n  ".join(drafts))
    if problems:
        return 1, "\n".join(problems)
    return 0, "No draft waiting, and only the write-back bot changed recipes/."


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--labels", default="[]", help="JSON list of the PR's label names")
    args = ap.parse_args(argv)
    code, message = verdict(person_commits(args.base), drafts_in_tree(), json.loads(args.labels or "[]"))
    print(message, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main())
