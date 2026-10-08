#!/usr/bin/env python3
"""
Run the real Validate of every recipe job 1 passed, in the CI project. Each recipe
stands on its own: the ones that validate are copied to OUT (answer + draft path) for
job 3 to write back; the ones that do not are listed with their reason. The job fails
only when every run failed (git_validate_summary).

Job 1 (git_validate_recipes.py --out DIR) leaves one `<frontmatter_id>.json` per passing
recipe: the step check's answer, i.e. the recipe object. Each one is sent as-is
to llm-wrapper's `POST /v1/recipes/git_validate_run` — never re-read from the
markdown — and `GET /v1/recipes/git_validate_run/{frontmatter_id}/{chain_id}` is polled
until the run finishes. The steps really run, so the entities they create stay
in that project.

A run takes minutes (every step executes), so the recipes are started together
and polled together.

Usage:
  git_validate_run_recipes.py DIR [--out OUT] [--url URL]
Config: .github/recipe-git-validate.json (git_validate_config.py) — job 1's
     url (`_run` is appended unless RECIPE_GIT_VALIDATE_RUN_URL is set) and the
     run's org_id, project_id, person_id. Env: RECIPE_GIT_VALIDATE_SECRET.
"""
from __future__ import annotations

import argparse
import glob
import shutil
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import git_validate_config
import git_validate_summary

HEADER = "x-recipe-validate-secret"
TIMEOUT_S = 60
POLL_S = 10
DEADLINE_S = 30 * 60


def call(method: str, url: str, secret: str, body: dict | None = None) -> tuple[int, dict]:
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers={"Content-Type": "application/json", HEADER: secret})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as err:
        raw = err.read()
        try:
            return err.code, json.loads(raw or b"{}")
        except ValueError:
            return err.code, {"raw": raw.decode("utf-8", "replace")[:500]}
    except (urllib.error.URLError, TimeoutError) as err:
        return 0, {"raw": str(err)}


def refused(name: str, status: int, body: dict) -> str:
    """Print why the run could not start or be read. Returns the one-line reason."""
    if status == 404:
        why = "404 — wrong URL, or the secret is unset/wrong on either side"
    else:
        detail = body.get("detail", body)
        if isinstance(detail, dict) and detail.get("code"):
            why = f"{status} {detail['code']}: {detail.get('message')}"
        else:
            why = f"{status}: {detail}"
    print(f"FAIL  {name}  {why}")
    return why


def report(name: str, s: dict) -> str | None:
    """Print a finished run's verdict. Returns None when it validated, else the reason."""
    if s.get("validated"):
        print(f"PASS  {name}  ({len(s.get('verdicts') or [])} steps ran)")
        return None
    why = f"failed at {s.get('failed_step_id')}: {s.get('message')}"
    print(f"FAIL  {name}  {why}")
    for c in s.get("checks") or []:
        for issue in c.get("issues") or []:
            msg = issue.get("message") if isinstance(issue, dict) else issue
            print(f"        - {c.get('step_id')} check: {msg}")
    for v in s.get("verdicts") or []:
        if not v.get("passed"):
            print(f"        - {v.get('step_id')} run {v.get('run_id')}: {v.get('reason')}")
    return why


def keep(path: str, out: str) -> None:
    """Copy a validated recipe's answer and its draft path (job 1's pair) into OUT."""
    os.makedirs(out, exist_ok=True)
    side = path[:-len(".json")] + ".path"
    for p in (path, side):
        if os.path.exists(p):
            shutil.copy(p, out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="job 1's --out directory")
    ap.add_argument("--out", help="directory for each recipe that validated (job 3's input)")
    cfg = git_validate_config.load()
    ap.add_argument("--url", default=os.environ.get("RECIPE_GIT_VALIDATE_RUN_URL")
                    or (cfg["url"] + "_run" if cfg["url"] else ""))
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.dir, "*.json")))
    if not files:
        print("No recipe passed job 1's check — nothing to run.")
        return 0
    secret = os.environ.get("RECIPE_GIT_VALIDATE_SECRET", "")
    where = {k: cfg[k] for k in ("org_id", "project_id", "person_id")}
    if not args.url or not secret or not all(where.values()):
        print("url / org_id / project_id / person_id (.github/recipe-git-validate.json) / "
              "RECIPE_GIT_VALIDATE_SECRET not set.", file=sys.stderr)
        return 2

    passed, failed, running, paths = [], [], {}, {}
    for path in files:
        with open(path, encoding="utf-8") as fh:
            recipe = json.load(fh)
        name = recipe.get("frontmatter_id") or os.path.basename(path)
        paths[name] = path
        status, body = call("POST", args.url, secret, {"recipe": recipe, **where})
        if status == 200 and body.get("chain_id"):
            print(f"START {name}  {body['chain_id']}")
            running[name] = body["chain_id"]
        else:
            failed.append((name, refused(name, status, body)))

    query = urllib.parse.urlencode(where)
    deadline = time.monotonic() + DEADLINE_S
    while running and time.monotonic() < deadline:
        time.sleep(POLL_S)
        for name, chain_id in list(running.items()):
            url = f"{args.url}/{urllib.parse.quote(name, safe='')}/{chain_id}?{query}"
            status, s = call("GET", url, secret)
            if status == 200 and s.get("finished"):
                why = report(name, s)
                if why is None:
                    passed.append(name)
                    if args.out:
                        keep(paths[name], args.out)
                else:
                    failed.append((name, why))
                del running[name]
            elif status not in (0, 200, 502, 503, 504):
                failed.append((name, refused(name, status, s)))
                del running[name]
    for name, chain_id in running.items():
        why = f"{chain_id} did not finish in {DEADLINE_S // 60} min"
        print(f"FAIL  {name}  {why}")
        failed.append((name, why))

    return git_validate_summary.finish("git-validate-run (real Validate)", passed, failed)

if __name__ == "__main__":
    sys.exit(main())
