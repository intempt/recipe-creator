#!/usr/bin/env python3
"""Deleting a global recipe is two steps (Beso 2026-10-08): archive it in git, then remove it from SM.

  move <frontmatter_id>        the `delete` action of recipe-deploy.yml. Moves
                               recipes/<owner>/<slug>/ → archived/<owner>/<slug>/ on a branch
                               archive/<frontmatter_id> cut from --base, pushes it and opens a PR
                               into --base. Nothing is sent to SM.
  delete-merged <before> <after>
                               recipe-archive-delete.yml, on a push to main. Every
                               archived/*/*/recipe.json that the push ADDED is deleted from SM
                               (DELETE <deploy_url> {frontmatter_id}); prints DELETED <id> per hit.

Why a PR: main and staging are both protected (org rulesets: main restricts pushes and needs the
`prerequisites` check; staging needs a code-owner approval), so a workflow cannot commit the move
itself. The PR is the archive; merging it to main is what removes the recipe from SM, so the repo
and SM cannot drift apart.

A recipe with no deployed/<frontmatter_id> marker was never deployed by recipe-deploy: it is
archived all the same, and delete-merged reports it NOT DEPLOYED instead of calling SM.

Exit 0 done; 1 refused or SM said no; 2 config/secret unset.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

import git_validate_config
import recipe_deploy as rd

ARCHIVE_DIR = "archived"
BRANCH = "archive/{}"


def git(root: str, *args: str) -> str:
    out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if out.returncode != 0:
        raise rd.Refused(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def archive_path(root: str, recipe_json: str) -> tuple[str, str]:
    """recipes/<owner>/<slug>/recipe.json → ("recipes/<owner>/<slug>", "archived/<owner>/<slug>")."""
    src = os.path.relpath(os.path.dirname(recipe_json), root)
    parts = src.split(os.sep)
    if len(parts) != 3 or parts[0] != "recipes":
        raise rd.Refused(f"{src} is not recipes/<owner>/<slug>")
    return src, "/".join([ARCHIVE_DIR, parts[1], parts[2]])


def move(root: str, frontmatter_id: str, base: str) -> tuple[str, str, str]:
    """Commit the move on a new branch archive/<frontmatter_id> cut from `base` → (branch, src, dst).
    The working tree is left on that branch."""
    branch = BRANCH.format(frontmatter_id)
    git(root, "checkout", "-q", "-b", branch, base)
    path, _ = rd.find_recipe_json(root, frontmatter_id)
    src, dst = archive_path(root, path)
    if os.path.exists(os.path.join(root, dst)):
        raise rd.Refused(f"{dst} already exists — archive it by hand")
    os.makedirs(os.path.dirname(os.path.join(root, dst)), exist_ok=True)
    git(root, "mv", src, dst)
    git(root, "commit", "-q", "-m",
        f"archive: {frontmatter_id} ({src} → {dst})\n\n"
        "Merging this to main deletes the recipe from SM (recipe-archive-delete.yml).")
    return branch, src, dst


def archived_between(root: str, before: str, after: str) -> list[tuple[str, dict]]:
    """Every archived/*/*/recipe.json the range before..after ADDED (a move counts as an add)
    → [(path, record)], read at `after`."""
    names = git(root, "diff", "--name-only", "--no-renames", "--diff-filter=A", before, after,
                "--", f"{ARCHIVE_DIR}/*/*/recipe.json").split()
    hits = []
    for name in sorted(names):
        try:
            record = json.loads(git(root, "show", f"{after}:{name}"))
        except ValueError:
            continue
        if isinstance(record, dict) and record.get("frontmatter_id"):
            hits.append((name, record))
    return hits


def cmd_move(args) -> int:
    try:
        branch, src, dst = move(args.root, args.frontmatter_id, args.base)
    except rd.Refused as err:
        print(f"REFUSED  {err}")
        return 1
    print(f"ARCHIVED  {args.frontmatter_id}: {src} → {dst} on {branch}")
    if args.no_push:
        return 0
    try:
        git(args.root, "push", "-q", "origin", branch)
    except rd.Refused as err:
        print(f"REFUSED  {err}")
        return 1
    pr_base = args.base.removeprefix("origin/")
    body = (f"Archives `{args.frontmatter_id}`: `{src}` → `{dst}`.\n\n"
            "When this reaches **main**, `recipe-archive-delete` deletes the recipe from SM.")
    pr = subprocess.run(["gh", "pr", "create", "--base", pr_base, "--head", branch,
                         "--title", f"archive: {args.frontmatter_id}", "--body", body],
                        cwd=args.root, capture_output=True, text=True)
    if pr.returncode != 0:
        print(f"REFUSED  gh pr create: {pr.stderr.strip()}")
        return 1
    print(f"PR  {pr.stdout.strip()}")
    return 0


def cmd_delete_merged(args) -> int:
    secret = os.environ.get("RECIPE_GIT_VALIDATE_SECRET", "")
    if not args.url or not secret:
        print("deploy_url (.github/recipe-git-validate.json) / RECIPE_GIT_VALIDATE_SECRET not set.",
              file=sys.stderr)
        return 2
    before = args.before
    if not before.strip("0"):  # a new branch's push carries before=000…0
        before = f"{args.after}^"
    try:
        hits = archived_between(args.root, before, args.after)
    except rd.Refused as err:
        print(f"REFUSED  {err}")
        return 1
    if not hits:
        print("nothing archived in this push")
        return 0
    failed = 0
    for name, record in hits:
        fid = str(record["frontmatter_id"])
        if not rd.has_marker(args.root, fid):
            print(f"NOT DEPLOYED  {fid} ({name}): no {rd.MARKER.format(fid)} — nothing to delete in SM")
            continue
        method, url, body = rd.request({"action": "delete", "frontmatter_id": fid}, args.url, None)
        status, text = rd.call(method, url, secret, body)
        if status in rd.EXPECTED["delete"]:
            print(f"DELETED  {fid}  ({method} {url} → {status})")
        else:
            failed += 1
            print(f"FAIL  delete {fid}  {method} {url} → {status}\n        {text}")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root holding recipes/ and archived/")
    sub = ap.add_subparsers(dest="cmd", required=True)
    mv = sub.add_parser("move", help="archive a recipe on a branch and open its PR")
    mv.add_argument("frontmatter_id")
    mv.add_argument("--base", default="origin/staging", help="branch to cut from and open the PR into")
    mv.add_argument("--no-push", action="store_true", help="commit only; no push, no PR")
    dm = sub.add_parser("delete-merged", help="delete from SM every recipe a push archived")
    dm.add_argument("before")
    dm.add_argument("after")
    dm.add_argument("--url", default=git_validate_config.load()["deploy_url"])
    args = ap.parse_args()
    return cmd_move(args) if args.cmd == "move" else cmd_delete_merged(args)


if __name__ == "__main__":
    sys.exit(main())
