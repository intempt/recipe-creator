#!/usr/bin/env python3
"""
Job 3 of recipe-git-validate.yml, after job 1 checked each changed
draft (the draft/ flow, R-RG4-6). For every draft it writes, for the PR head branch
to commit in ONE bot commit:

  recipes/<owner>/<frontmatter_id>/recipe.md    front matter `frontmatter_id`,
                                                `slash_command`, `description`,
                                                `author` (with `org_name`), then the
                                                draft's prose, byte for byte
  recipes/<owner>/<frontmatter_id>/recipe.json  job 1's answer — the object job 1
                                                got back — with the real key, the real
                                                slash_command and `author.org_name`
                                                put back (LM drops unknown author keys)
  draft/<…>.md                                  deleted

  owner           the draft's `author.org_name`, else `intempt` (D1)
  frontmatter_id  new draft: LM's slash_command without `/`, made unique across ALL
                  recipes (`-2`, `-3`…), and slash_command = `/<frontmatter_id>` (D2).
                  Draft naming `frontmatter_id:` = an edit of that recipe: key, folder
                  and slash_command are kept (D3); the owner must be the same.
  description     the answer's — LM keeps the one the author wrote, else generates
                  one (RG2 §6: an author's description is never overwritten)

Which draft an answer belongs to is the path job 1 recorded (<key>.path), never
re-derived. Each draft stands on its own: one that cannot be planned is listed and left
in draft/, and one whose written result fails check_recipe_consistency is put back (its
files restored, its draft returned). The others are written. The job fails only when no
draft could be written (git_validate_summary).

Usage:
  git_validate_writeback.py DIR [--root .]     # DIR = job 1's --out directory
Prints each path it wrote or deleted; exit 0 when at least one draft was written (or
there was nothing to write), 1 when drafts were given and none could be written back.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

import yaml

import check_recipe_consistency
import git_validate_summary
import recipe_draft
from recipe_contract import git_front


def _md(front: dict, body: str) -> str:
    head = yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000)
    return "---\n" + head + "---\n" + (body if body.startswith("\n") else "\n" + body)


def _edit_target(meta: dict, answer: dict, owner: str, root: str) -> tuple[str, str]:
    """D3: (folder, slash_command) of the recipe the draft edits. Raises DraftError."""
    key = str(meta.get("frontmatter_id")).strip()
    folder = recipe_draft.find_recipe(key, root)
    if folder is None:
        raise recipe_draft.DraftError(f"frontmatter_id {key!r} names no recipe to edit — "
                                      "leave frontmatter_id out for a new recipe")
    if git_front(os.path.join(root, folder, "recipe.md")) is None:
        raise recipe_draft.DraftError(f"{folder} is a contract recipe, not one the draft flow wrote")
    held_by = folder.split(os.sep)[1]
    if held_by != owner:
        raise recipe_draft.DraftError(f"{folder} belongs to {held_by!r}, the draft says org_name "
                                      f"{owner!r} — set author.org_name to the recipe's owner")
    if str(answer.get("frontmatter_id") or "") != key:
        raise recipe_draft.DraftError(f"the answer is for {answer.get('frontmatter_id')!r}, not {key!r}")
    try:
        with open(os.path.join(root, folder, "recipe.json"), encoding="utf-8") as fh:
            slash = str(json.load(fh).get("slash_command") or "")
    except (OSError, ValueError):
        slash = ""
    return folder, slash or "/" + key


def plan(pairs: list[tuple[dict, str]], root: str = ".") -> tuple[list[dict], list[str]]:
    """Each (answer, draft path) → {draft, folder, md, json}. Returns (plans, problems)."""
    used = set(recipe_draft.taken(root))
    plans, problems = [], []
    for answer, draft in pairs:
        try:
            with open(os.path.join(root, draft), encoding="utf-8") as fh:
                meta, body = recipe_draft.split(fh.read())
            owner = recipe_draft.owner_of(meta)
            description = " ".join(str(answer.get("description") or "").split())
            if not description:
                raise recipe_draft.DraftError("the answer has no description")
            author = answer.get("author")
            if not isinstance(author, dict) or not author.get("name") or not author.get("last_name"):
                raise recipe_draft.DraftError("the answer has no author name and last_name")
            if str(meta.get("frontmatter_id") or "").strip():
                folder, slash = _edit_target(meta, answer, owner, root)
                key = os.path.basename(folder)
            else:
                stem = os.path.splitext(os.path.basename(draft))[0]
                base = (recipe_draft.slugify(answer.get("slash_command"))
                        or recipe_draft.slugify(answer.get("title")) or recipe_draft.slugify(stem))
                if not base:
                    raise recipe_draft.DraftError("no slash_command, title or file name to make a key from")
                key = recipe_draft.new_key(base, used)
                used.add(key)
                folder, slash = os.path.join("recipes", owner, key), "/" + key
        except OSError as e:
            problems.append(f"{draft}: cannot read the draft ({e.strerror})")
            continue
        except recipe_draft.DraftError as e:
            problems.append(f"{draft}: {e}")
            continue

        author = {**{k: v for k, v in author.items() if k != "org_name"}, "org_name": owner}
        record = {**answer, "frontmatter_id": key, "slash_command": slash,
                  "description": description, "author": author}
        front = {"frontmatter_id": key, "slash_command": slash,
                 "description": description, "author": author}
        plans.append({"draft": draft, "folder": folder, "md": _md(front, body), "json": record})
    return plans, problems


def apply(plans: list[dict], root: str = ".") -> list[str]:
    """Write each plan's two files and delete its draft. Returns the lines to print."""
    lines = []
    for p in plans:
        lines += _write(p, root)
    return lines


def _write(p: dict, root: str) -> list[str]:
    folder = os.path.join(root, p["folder"])
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "recipe.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(p["md"])
    with open(os.path.join(folder, "recipe.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(p["json"], fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    os.remove(os.path.join(root, p["draft"]))
    return [f"WROTE   {p['folder']}/recipe.md", f"WROTE   {p['folder']}/recipe.json",
            f"DELETED {p['draft']}"]


def _snapshot(p: dict, root: str) -> dict:
    """The bytes _write is about to replace or delete, so one recipe can be put back."""
    paths = [os.path.join(root, p["folder"], n) for n in ("recipe.md", "recipe.json")]
    paths.append(os.path.join(root, p["draft"]))
    snap = {}
    for path in paths:
        try:
            with open(path, "rb") as fh:
                snap[path] = fh.read()
        except FileNotFoundError:
            snap[path] = None
    return snap


def _restore(snap: dict, folder: str) -> None:
    for path, data in snap.items():
        if data is None:
            if os.path.exists(path):
                os.remove(path)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(data)
    if os.path.isdir(folder) and not os.listdir(folder):
        os.rmdir(folder)


def apply_each(plans: list[dict], root: str = ".") -> tuple[list[str], list[tuple[str, str]]]:
    """Write each plan on its own and check it (check_recipe_consistency). A plan whose
    result is inconsistent is put back — its files restored, its draft returned — so it
    fails alone. Returns (the drafts written, [(draft, reason)] for the ones put back)."""
    written, failed = [], []
    for p in plans:
        snap = _snapshot(p, root)
        lines = _write(p, root)
        folder = os.path.join(root, p["folder"])
        bad = check_recipe_consistency.check(folder)
        if bad:
            _restore(snap, folder)
            print(f"FAIL  {p['draft']}  written, then put back:")
            for m in bad:
                print(f"        - {m}")
            failed.append((p["draft"], "; ".join(bad)))
            continue
        for line in lines:
            print(line)
        written.append(p["draft"])
    return written, failed


def load(out_dir: str) -> tuple[list[tuple[dict, str]], list[str]]:
    """Job 1's DIR: each <key>.json with the draft path in its <key>.path."""
    pairs, problems = [], []
    for path in sorted(glob.glob(os.path.join(out_dir, "*.json"))):
        with open(path, encoding="utf-8") as fh:
            answer = json.load(fh)
        side = path[:-len(".json")] + ".path"
        try:
            with open(side, encoding="utf-8") as fh:
                draft = fh.read().strip()
        except FileNotFoundError:
            draft = ""
        if not draft:
            problems.append(f"{os.path.basename(path)}: job 1 recorded no draft path")
            continue
        if not recipe_draft.is_draft(draft):
            problems.append(f"{os.path.basename(path)}: {draft} is not a draft/*.md")
            continue
        pairs.append((answer, draft))
    return pairs, problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="job 1's --out directory (<key>.json + <key>.path per passing draft)")
    ap.add_argument("--root", default=".", help="the repo checkout (default: the current directory)")
    args = ap.parse_args(argv)

    pairs, problems = load(args.dir)
    if not pairs and not problems:
        print("No validated draft — nothing to write back.")
        return 0
    plans, more = plan(pairs, args.root)
    problems += more
    failed = []
    for p in problems:
        print(f"FAIL  {p}")
        name, _, why = p.partition(": ")
        failed.append((name, why or p))
    written, put_back = apply_each(plans, args.root)
    return git_validate_summary.finish("git-validate-writeback", written, failed + put_back)

if __name__ == "__main__":
    sys.exit(main())
