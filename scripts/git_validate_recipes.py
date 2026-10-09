#!/usr/bin/env python3
"""
Send every draft a pull request added or changed (`draft/**/*.md`, the draft/ flow,
R-RG4-6) to llm-wrapper's `POST /v1/recipes/git_validate`. Each draft stands on its
own: the ones that pass go on to job 3, the ones that fail are listed with their reason
and stay in draft/. The job fails only when every draft failed (git_validate_summary).

The route turns the markdown into steps and runs the per-step check with no
tenant: each step must read earlier outputs correctly and must not be vague.
A 422 is a recipe problem (errors printed per step); a 503 is the model
failing, retried once before it counts as a failure.

A new draft has no `frontmatter_id` yet and LM refuses one without it, so it is sent
with a TEMPORARY key (recipe_draft.temp_key, `draft-<file name>`); the real key is
chosen by the write-back (job 3). A draft that names one (an edit, D3) is sent as is.

Only changed drafts are sent — each one costs one model call to read and one
per step — and a pull request that touches no draft exits 0 in about a second,
because this runs as a check with no `paths:` filter (see
recipe-prerequisites.yml for why).

Usage:
  git_validate_recipes.py --base <ref> [--url URL]       # drafts changed since merge-base
  git_validate_recipes.py draft/x.md ...                 # explicit files
  --out DIR   writes each passing answer to DIR/<frontmatter_id>.json — the recipe object
              job 3 (git_validate_writeback.py) writes back, so it is never re-read —
              and the draft it came from to DIR/<frontmatter_id>.path (job 3's key).
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
import git_validate_summary
import recipe_draft

HEADER = "x-recipe-validate-secret"
TIMEOUT_S = 300


def changed_drafts(base: str) -> list[str]:
    out = subprocess.run(
        # --no-renames: a draft renamed or copied from another reads as R/C, which
        # --diff-filter=AM would drop — and that draft would never be validated.
        ["git", "diff", "--name-only", "--no-renames", "--diff-filter=AM", f"{base}...HEAD", "--",
         recipe_draft.DRAFT_DIR + "/"],
        check=True, capture_output=True, text=True).stdout
    return sorted(p for p in out.splitlines() if recipe_draft.is_draft(p))


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


def report(path: str, status: int, body: dict) -> str | None:
    """Print the verdict for one draft. Returns None when it passed, else the one-line reason."""
    if status == 200:
        print(f"PASS  {path}  ({body.get('frontmatter_id')}, {len(body.get('steps') or [])} steps)")
        return None
    detail = body.get("detail", body)
    if status == 404:
        why = "404 — wrong URL, or the secret is unset/wrong on either side"
        print(f"FAIL  {path}  {why}")
        return why
    if not isinstance(detail, dict):
        why = f"{status}: {detail}"
        print(f"FAIL  {path}  {why}")
        return why
    why = f"{status} {detail.get('code')}: {detail.get('message')}"
    print(f"FAIL  {path}  {why}")
    for key in ("missing",):
        if detail.get(key):
            print(f"        {key}: {', '.join(detail[key])}")
    titles = []
    for step in detail.get("steps") or []:
        title = step.get("title") or step.get("id") or f"step {step.get('position')}"
        titles.append(str(title))
        for e in step.get("errors") or []:
            msg = e.get("message") if isinstance(e, dict) else e
            code = e.get("kind") if isinstance(e, dict) else ""
            print(f"        - {title}: [{code}] {msg}")
    return why + (f" ({', '.join(titles)})" if titles else "")


def save(out_dir: str, body: dict, path: str) -> None:
    """DIR/<frontmatter_id>.json is the answer, verbatim; DIR/<frontmatter_id>.path names the
    recipe.md it came from, so the write-back never has to re-read the md."""
    os.makedirs(out_dir, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._-]", "_", str(body.get("frontmatter_id") or "recipe"))
    with open(os.path.join(out_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
        json.dump(body, fh, ensure_ascii=False)
    with open(os.path.join(out_dir, f"{name}.path"), "w", encoding="utf-8") as fh:
        fh.write(path + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--base", help="git ref to diff against (merge-base)")
    ap.add_argument("--url", default=git_validate_config.load()["url"])
    ap.add_argument("--out", help="directory for each passing answer, <frontmatter_id>.json")
    args = ap.parse_args()

    files = args.files or (changed_drafts(args.base) if args.base else [])
    if not files:
        print("No draft changed — nothing to validate.")
        return 0
    secret = os.environ.get("RECIPE_GIT_VALIDATE_SECRET", "")
    if not args.url or not secret:
        print("url (.github/recipe-git-validate.json) / RECIPE_GIT_VALIDATE_SECRET not set.", file=sys.stderr)
        return 2

    passed, failed = [], []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        try:
            markdown = recipe_draft.with_key(text, recipe_draft.temp_key(path))
        except recipe_draft.DraftError as e:
            print(f"FAIL  {path}  {e}")
            failed.append((path, str(e)))
            continue
        status, body = post(args.url, secret, markdown)
        if status == 503:
            time.sleep(5)
            status, body = post(args.url, secret, markdown)
        why = report(path, status, body)
        if why is not None:
            failed.append((path, why))
            continue
        passed.append(path)
        if args.out:
            save(args.out, body, path)
    return git_validate_summary.finish("git-validate (step check)", passed, failed)

if __name__ == "__main__":
    sys.exit(main())
