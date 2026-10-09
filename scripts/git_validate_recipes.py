#!/usr/bin/env python3
"""
Send every draft a pull request added or changed (`draft/**/*.md`, the draft/ flow,
R-RG4-6) to llm-wrapper's `POST /v1/recipes/git_validate`. Each draft stands on its
own: the ones that pass go on to job 3, the ones that fail are listed with their reason
and stay in draft/. The job fails only when every draft failed (git_validate_summary).

The route turns the markdown into steps and runs the per-step check with no
tenant: each step must read earlier outputs correctly and must not be vague.
It is start-then-poll (R34-5): `POST <url>/start {markdown}` → 202 `{job_id}`, then
`GET <url>/<job_id>` every --poll-interval seconds until the job is
  done     → the record. A record whose steps failed is STILL a pass (R34-2/R34-3): each
             failed step keeps its `errors`, `failed_steps` lists them, the record is saved
             and written back like any other (deployed; the catalog shows it "Coming soon"),
             and its failed steps are reported here and in the job summary.
  refused  → a recipe problem (the old 422s: frontmatter_id, author, industry, unreadable,
             empty/too large) — the draft fails and stays in draft/.
  failed   → the model failed (the old 503) — the job is started again, --retries times.
A 404 on a poll (job unknown or expired) restarts the job once; a transport error counts
as a failed job. Each draft gets --timeout seconds in all (env RECIPE_GIT_VALIDATE_TIMEOUT_S,
default 900).

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
  --poll-interval S, --retries N, --timeout S   the poll loop (defaults 5, 1, 900)
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
REQUEST_TIMEOUT_S = 60      # one start or poll call; the job itself runs on LM
DEFAULT_TIMEOUT_S = float(os.environ.get("RECIPE_GIT_VALIDATE_TIMEOUT_S") or 900)
DEFAULT_INTERVAL_S = 5.0
DEFAULT_RETRIES = 1         # a failed job is started once more, as the 503 used to be


def changed_drafts(base: str) -> list[str]:
    out = subprocess.run(
        # --no-renames: a draft renamed or copied from another reads as R/C, which
        # --diff-filter=AM would drop — and that draft would never be validated.
        ["git", "diff", "--name-only", "--no-renames", "--diff-filter=AM", f"{base}...HEAD", "--",
         recipe_draft.DRAFT_DIR + "/"],
        check=True, capture_output=True, text=True).stdout
    return sorted(p for p in out.splitlines() if recipe_draft.is_draft(p))


def _call(method: str, url: str, secret: str, payload: dict | None = None) -> tuple[int, dict]:
    """One HTTP call → (status, JSON body). A transport error raises OSError."""
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        method=method, headers={"Content-Type": "application/json", HEADER: secret})
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as err:
        body = err.read()
        try:
            return err.code, json.loads(body or b"{}")
        except ValueError:
            return err.code, {"raw": body.decode("utf-8", "replace")[:500]}


def _detail(code: str, message: str) -> dict:
    return {"detail": {"code": code, "message": message}}


def validate(url: str, secret: str, markdown: str, *, timeout_s: float = DEFAULT_TIMEOUT_S,
             interval_s: float = DEFAULT_INTERVAL_S, retries: int = DEFAULT_RETRIES) -> tuple[int, dict]:
    """Start a git_validate job and poll it to the end. Returns what the sync route used to:
    (200, record) — failed steps included —, (422, {detail}) refused, (503, {detail}) the
    check failed past `retries` (or LM was unreachable), (404, body) wrong URL/secret, and
    (504, {detail: timeout}) when `timeout_s` ran out."""
    deadline = time.monotonic() + timeout_s
    failures, restarted = 0, False
    last = (503, _detail("check_failed", "The check could not be made."))
    while True:
        if failures > retries:
            return last
        if time.monotonic() >= deadline:
            return 504, _detail("timeout", f"no answer within {timeout_s:g}s")
        try:
            status, body = _call("POST", url.rstrip("/") + "/start", secret, {"markdown": markdown})
        except OSError as e:
            failures, last = failures + 1, (503, _detail("unreachable", f"start: {e}"))
            time.sleep(interval_s)
            continue
        if status in (500, 502, 503, 504):
            failures, last = failures + 1, (503, body if isinstance(body.get("detail"), dict)
                                            else _detail("check_failed", f"start answered {status}"))
            time.sleep(interval_s)
            continue
        if status != 202 or not body.get("job_id"):
            return status, body   # 404 wrong URL/secret, 422 a body LM cannot read, …
        poll = url.rstrip("/") + "/" + str(body["job_id"])
        while True:
            if time.monotonic() >= deadline:
                return 504, _detail("timeout", f"no answer within {timeout_s:g}s")
            time.sleep(interval_s)
            try:
                status, body = _call("GET", poll, secret)
            except OSError as e:
                failures, last = failures + 1, (503, _detail("unreachable", f"poll: {e}"))
                break
            state = body.get("state") if status == 200 else None
            if status == 404:
                if restarted:
                    return 404, _detail("job_lost", "the job was lost twice (unknown or expired)")
                restarted = True
                break
            if state == "running":
                continue
            if state == "done":
                return 200, body.get("result") or {}
            if state == "refused":
                return 422, {"detail": body.get("detail")}
            if state == "failed" or status >= 500:
                detail = body.get("detail")
                failures, last = failures + 1, (503, {"detail": detail} if isinstance(detail, dict)
                                                else _detail("check_failed", f"poll answered {status}"))
                break
            if status == 200:   # a 200 this client cannot read is never a pass
                return 502, _detail("bad_answer", f"poll answered state {state!r}")
            return status, body


def report(path: str, status: int, body: dict) -> str | None:
    """Print the verdict for one draft. Returns None when it passed, else the one-line reason.
    A record with failed steps passed (R34-3); its failed steps are printed under it."""
    if status == 200:
        failed_steps = body.get("failed_steps") or []
        extra = f", {len(failed_steps)} failed step(s)" if failed_steps else ""
        print(f"PASS  {path}  ({body.get('frontmatter_id')}, {len(body.get('steps') or [])} steps{extra})")
        for line in failed_step_lines(failed_steps):
            print(f"        {line}")
        return None
    detail = body.get("detail", body)
    if status == 404 and not (isinstance(detail, dict) and detail.get("code")):
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
    return why


def failed_step_lines(failed_steps: list) -> list[str]:
    """`- <title>: [<kind>] <message>` per error of each failed step."""
    lines = []
    for step in failed_steps:
        title = step.get("title") or step.get("id") or "step"
        for e in step.get("errors") or []:
            msg = e.get("message") if isinstance(e, dict) else e
            kind = e.get("kind") if isinstance(e, dict) else ""
            lines.append(f"- {title}: [{kind}] {msg}")
    return lines


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
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_S,
                    help="seconds per draft, start to answer (env RECIPE_GIT_VALIDATE_TIMEOUT_S)")
    ap.add_argument("--poll-interval", type=float, default=DEFAULT_INTERVAL_S)
    ap.add_argument("--retries", type=int, default=DEFAULT_RETRIES,
                    help="times a failed job (the model failing) is started again")
    args = ap.parse_args()

    files = args.files or (changed_drafts(args.base) if args.base else [])
    if not files:
        print("No draft changed — nothing to validate.")
        return 0
    secret = os.environ.get("RECIPE_GIT_VALIDATE_SECRET", "")
    if not args.url or not secret:
        print("url (.github/recipe-git-validate.json) / RECIPE_GIT_VALIDATE_SECRET not set.", file=sys.stderr)
        return 2

    passed, failed, flagged = [], [], []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        try:
            markdown = recipe_draft.with_key(text, recipe_draft.temp_key(path))
        except recipe_draft.DraftError as e:
            print(f"FAIL  {path}  {e}")
            failed.append((path, str(e)))
            continue
        status, body = validate(args.url, secret, markdown, timeout_s=args.timeout,
                                interval_s=args.poll_interval, retries=args.retries)
        why = report(path, status, body)
        if why is not None:
            failed.append((path, why))
            continue
        passed.append(path)
        if body.get("failed_steps"):
            flagged.append((path, "; ".join(failed_step_lines(body["failed_steps"]))))
        if args.out:
            save(args.out, body, path)
    return git_validate_summary.finish("git-validate (step check)", passed, failed, flagged)

if __name__ == "__main__":
    sys.exit(main())
