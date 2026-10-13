#!/usr/bin/env python3
"""
Writes recipe.json beside every git-format recipes/<owner>/<id>/recipe.md that has none —
the recipes that never went through recipe-git-validate. Each one is deployed as a
Coming soon recipe (Beso 2026-10-13):

  frontmatter_id, slash_command,   the front matter's, as written (check_recipe_consistency
  description, author,             compares them with recipe.md)
  classification
  title                            the body's `# ` heading
  markdown                         `# title`, `## Description`, then each `## Step N: …`
                                   section as `### Step N: …` under `## Steps` — the layout
                                   recipe-git-validate writes — prose kept byte for byte
  steps                            []: nothing is runnable until the recipe is validated
  availability                     "coming_soon": llm-wrapper serves a stored availability
                                   as-is, instead of reading a step-less recipe as install_now
  permissions                      []

An existing recipe.json is never touched. Run from the repo root:
  python3 scripts/build_coming_soon_json.py [recipes/intempt]   (prints one line per file)
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recipe_contract import git_front  # noqa: E402

STEP = re.compile(r"^## (Step \d+:.*)$", re.M)


def body_of(md_text: str) -> str:
    return md_text.split("\n---\n", 1)[1] if md_text.startswith("---\n") else md_text


def build(front: dict, md_text: str) -> dict:
    body = body_of(md_text)
    title = re.search(r"^# (.+)$", body, re.M).group(1).strip()
    heads = list(STEP.finditer(body))
    sections = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        sections.append(f"### {m.group(1).strip()}\n\n{body[m.end():end].strip()}\n")
    markdown = f"# {title}\n\n## Description\n\n{front['description']}\n"
    if sections:
        markdown += "\n## Steps\n\n" + "\n".join(sections)
    record = {
        "frontmatter_id": front["frontmatter_id"],
        "title": title,
        "slash_command": front["slash_command"],
        "description": front["description"],
        "markdown": markdown,
    }
    if front.get("classification") is not None:
        record["classification"] = front["classification"]
    record.update({"author": front["author"], "permissions": [], "steps": [],
                   "availability": "coming_soon"})
    return record


def main(argv=None) -> int:
    roots = (argv if argv is not None else sys.argv[1:]) or ["recipes"]
    written = 0
    for root in roots:
        for md in sorted(glob.glob(os.path.join(root, "**", "recipe.md"), recursive=True)):
            js = os.path.join(os.path.dirname(md), "recipe.json")
            front = git_front(md)
            if front is None or os.path.exists(js):
                continue
            with open(md, encoding="utf-8") as fh:
                record = build(front, fh.read())
            with open(js, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(record, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
            print(f"WROTE   {js}")
            written += 1
    print(f"{written} recipe.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
