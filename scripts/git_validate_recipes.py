#!/usr/bin/env python3
"""
Send every recipe.md a pull request changed to llm-wrapper's
`POST /v1/recipes/git_validate`, and fail when any of them does not pass.

The route turns the markdown into steps and runs the per-step check with no
tenant: each step must read earlier outputs correctly and must not be vague.
A 422 is a recipe problem (CI red, errors printed per step); a 503 is the model
failing, retried once before it counts as a failure.

Only changed recipes are sent — each one costs one model call to read and one
per step — and a pull request that touches no recipe exits 0 in about a second,
because this runs as a check with no `paths:` filter (see
recipe-prerequisites.yml for why).

Usage:
  git_validate_recipes.py --base <ref> [--url URL]       # changed since merge-base
  git_validate_recipes.py path/to/recipe.md ...          # explicit files
  --out DIR   writes each passing answer to DIR/<f_id>.json — the recipe object
              job 2 (git_validate_run_recipes.py) runs, so it is never re-read —
              and the recipe.md it came from to DIR/<f_id>.path (job 3's key).
URL: .github/recipe-git-validate.json (git_validate_config.py). Env: RECIPE_GIT_VALIDATE_SECRET.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

import git_validate_config

HEADER = "x-recipe-validate-secret"
TIMEOUT_S = 300


def changed_recipes(base: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD", "--", "recipes/"],
        check=True, capture_output=True, text=True).stdout
    return sorted(p for p in out.splitlines() if p.endswith("/recipe.md"))


def post(url: str, secret: str, markdown: str) -> tuple[int, dict]:
    req = urllib.request.Request(
        url, data=json.dumps({"markdown": markdown}).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", HEADER: secret})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as err:
        body = err.read()
        try:
            return err.code, json.loads(body or b"{}")
        except ValueError:
            return err.code, {"raw": body.decode("utf-8", "replace")[:500]}


def report(path: str, status: int, body: dict) -> bool:
    if status == 200:
        print(f"PASS  {path}  ({body.get('f_id')}, {len(body.get('steps') or [])} steps)")
        return True
    detail = body.get("detail", body)
    if status == 404:
        print(f"FAIL  {path}  404 — wrong URL, or the secret is unset/wrong on either side")
        return False
    if not isinstance(detail, dict):
        print(f"FAIL  {path}  {status}: {detail}")
        return False
    print(f"FAIL  {path}  {status} {detail.get('code')}: {detail.get('message')}")
    for key in ("missing",):
        if detail.get(key):
            print(f"        {key}: {', '.join(detail[key])}")
    for step in detail.get("steps") or []:
        title = step.get("title") or step.get("id") or f"step {step.get('position')}"
        for e in step.get("errors") or []:
            msg = e.get("message") if isinstance(e, dict) else e
            code = e.get("kind") if isinstance(e, dict) else ""
            print(f"        - {title}: [{code}] {msg}")
    return False


def save(out_dir: str, body: dict, path: str) -> None:
    """DIR/<f_id>.json is the answer, verbatim; DIR/<f_id>.path names the
    recipe.md it came from, so the write-back never has to re-read the md."""
    os.makedirs(out_dir, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._-]", "_", str(body.get("f_id") or "recipe"))
    with open(os.path.join(out_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
        json.dump(body, fh, ensure_ascii=False)
    with open(os.path.join(out_dir, f"{name}.path"), "w", encoding="utf-8") as fh:
        fh.write(path + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--base", help="git ref to diff against (merge-base)")
    ap.add_argument("--url", default=git_validate_config.load()["url"])
    ap.add_argument("--out", help="directory for each passing answer, <f_id>.json")
    args = ap.parse_args()

    files = args.files or (changed_recipes(args.base) if args.base else [])
    if not files:
        print("No recipe.md changed — nothing to validate.")
        return 0
    secret = os.environ.get("RECIPE_GIT_VALIDATE_SECRET", "")
    if not args.url or not secret:
        print("url (.github/recipe-git-validate.json) / RECIPE_GIT_VALIDATE_SECRET not set.", file=sys.stderr)
        return 2

    ok = True
    for path in files:
        with open(path, encoding="utf-8") as fh:
            markdown = fh.read()
        status, body = post(args.url, secret, markdown)
        if status == 503:
            time.sleep(5)
            status, body = post(args.url, secret, markdown)
        passed = report(path, status, body)
        if passed and args.out:
            save(args.out, body, path)
        ok = passed and ok
    print(f"\n{len(files)} recipe(s) checked.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
