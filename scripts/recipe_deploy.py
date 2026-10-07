#!/usr/bin/env python3
"""
Deploy one recipe to SM from a tag pushed on `main` (RG1 §50):

  create/<person_id>/<f_id>   POST   <deploy_url>          {person_id, recipe}
  update/<f_id>               PUT    <deploy_url>          {recipe}   (recipe.f_id names it)
  delete/<f_id>               DELETE <deploy_url>          {f_id}

`recipe` is the `recipes/*/*/recipe.json` whose `f_id` is the tag's — the
object the PR's git Validate checked and ran, committed back by
git_validate_writeback.py. It is sent as-is. A delete needs no file, so a
recipe whose folder is already gone from `main` can still be deleted.

The one gate is that the tagged commit is on `main` (an ancestor of
origin/main). Nothing else is checked here (RG1 §17); SM refuses what it
refuses (409 duplicate f_id, 404 unknown f_id, 404 wrong secret).

The workflow deletes the tag afterwards, so the same tag can be pushed again.

Usage:
  recipe_deploy.py <tag> [--main origin/main] [--url URL]
Config: `deploy_url` in .github/recipe-git-validate.json (git_validate_config.py,
env RECIPE_DEPLOY_URL overrides). Env: RECIPE_GIT_VALIDATE_SECRET.
Exit 0 deployed; 1 refused (tag, not on main, no recipe.json, SM said no);
2 config/secret unset.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

import git_validate_config

HEADER = "x-recipe-validate-secret"
TIMEOUT_S = 60
EXPECTED = {"create": (200, 201), "update": (200,), "delete": (200, 204)}


class Refused(Exception):
    pass


def parse_tag(tag: str) -> dict:
    """`create/<person_id>/<f_id>` | `update/<f_id>` | `delete/<f_id>` →
    {action, f_id, person_id (create only, int)}. Anything else → Refused."""
    tag = tag.removeprefix("refs/tags/")
    parts = tag.split("/")
    action = parts[0]
    if action == "create" and len(parts) == 3 and parts[1].isdigit() and parts[2]:
        return {"action": action, "person_id": int(parts[1]), "f_id": parts[2]}
    if action in ("update", "delete") and len(parts) == 2 and parts[1]:
        return {"action": action, "f_id": parts[1]}
    raise Refused(f"tag {tag!r} is not create/<person_id>/<f_id>, update/<f_id> or delete/<f_id>")


def find_recipe_json(root: str, f_id: str) -> tuple[str, dict]:
    """The one recipes/*/*/recipe.json whose `f_id` is f_id → (path, record)."""
    hits = []
    for path in sorted(glob.glob(os.path.join(root, "recipes", "*", "*", "recipe.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                record = json.load(fh)
        except (OSError, ValueError):
            continue
        if isinstance(record, dict) and str(record.get("f_id") or "") == f_id:
            hits.append((path, record))
    if not hits:
        raise Refused(f"no recipes/*/*/recipe.json has f_id {f_id!r}")
    if len(hits) > 1:
        raise Refused(f"f_id {f_id!r} is in {len(hits)} recipe.json files: "
                      + ", ".join(os.path.relpath(p, root) for p, _ in hits))
    return hits[0]


def on_main(ref: str, main: str, cwd: str | None = None) -> bool:
    """True when the commit `ref` points at is an ancestor of `main` (or is it)."""
    sha = subprocess.run(["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], cwd=cwd,
                         capture_output=True, text=True)
    if sha.returncode != 0:
        return False
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha.stdout.strip(), main],
                          cwd=cwd, capture_output=True).returncode == 0


def request(tag: dict, base_url: str, record: dict | None) -> tuple[str, str, dict | None]:
    """(method, url, body) for the parsed tag. All three hit the one route; the f_id rides
    in the body (RG1 §60)."""
    if tag["action"] == "create":
        return "POST", base_url, {"person_id": tag["person_id"], "recipe": record}
    if tag["action"] == "update":
        return "PUT", base_url, {"recipe": record}
    return "DELETE", base_url, {"f_id": tag["f_id"]}


def call(method: str, url: str, secret: str, body: dict | None) -> tuple[int, str]:
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None,
        headers={"Content-Type": "application/json", HEADER: secret})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")[:500]
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode("utf-8", "replace")[:500]
    except (urllib.error.URLError, TimeoutError) as err:
        return 0, str(err)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tag", help="the pushed tag name, e.g. update/<f_id>")
    ap.add_argument("--main", default="origin/main", help="the branch the tagged commit must be on")
    ap.add_argument("--url", default=git_validate_config.load()["deploy_url"])
    ap.add_argument("--root", default=".", help="repo root holding recipes/")
    args = ap.parse_args()

    secret = os.environ.get("RECIPE_GIT_VALIDATE_SECRET", "")
    if not args.url or not secret:
        print("deploy_url (.github/recipe-git-validate.json) / RECIPE_GIT_VALIDATE_SECRET not set.",
              file=sys.stderr)
        return 2
    try:
        tag = parse_tag(args.tag)
        if not on_main(f"refs/tags/{args.tag.removeprefix('refs/tags/')}", args.main, args.root):
            raise Refused(f"tag {args.tag!r} is not on {args.main} — only commits on main deploy")
        record = None
        if tag["action"] != "delete":
            path, record = find_recipe_json(args.root, tag["f_id"])
            print(f"recipe {os.path.relpath(path, args.root)}")
    except Refused as err:
        print(f"REFUSED  {err}")
        return 1

    method, url, body = request(tag, args.url, record)
    status, text = call(method, url, secret, body)
    if status in EXPECTED[tag["action"]]:
        print(f"DEPLOYED  {tag['action']} {tag['f_id']}  ({method} {url} → {status})")
        return 0
    hint = " — wrong URL, unknown f_id, or the secret is unset/wrong on either side" if status == 404 else ""
    print(f"FAIL  {tag['action']} {tag['f_id']}  {method} {url} → {status}{hint}\n        {text}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
