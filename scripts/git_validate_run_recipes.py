#!/usr/bin/env python3
"""
Run the real Validate of every recipe job 1 passed, in the CI project, and fail
when any run does not validate.

Job 1 (git_validate_recipes.py --out DIR) leaves one `<f_id>.json` per passing
recipe: the step check's answer, i.e. the recipe object. Each one is sent as-is
to llm-wrapper's `POST /v1/recipes/git_validate_run` — never re-read from the
markdown — and `GET /v1/recipes/git_validate_run/{f_id}/{chain_id}` is polled
until the run finishes. The steps really run, so the entities they create stay
in that project.

A run takes minutes (every step executes), so the recipes are started together
and polled together.

Usage:
  git_validate_run_recipes.py DIR [--url URL]
Config: .github/recipe-git-validate.json (git_validate_config.py) — job 1's
     url (`_run` is appended unless RECIPE_GIT_VALIDATE_RUN_URL is set) and the
     run's org_id, project_id, person_id. Env: RECIPE_GIT_VALIDATE_SECRET.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import git_validate_config

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


def refused(name: str, status: int, body: dict) -> None:
    if status == 404:
        print(f"FAIL  {name}  404 — wrong URL, or the secret is unset/wrong on either side")
        return
    detail = body.get("detail", body)
    if isinstance(detail, dict) and detail.get("code"):
        print(f"FAIL  {name}  {status} {detail['code']}: {detail.get('message')}")
    else:
        print(f"FAIL  {name}  {status}: {detail}")


def report(name: str, s: dict) -> bool:
    if s.get("validated"):
        print(f"PASS  {name}  ({len(s.get('verdicts') or [])} steps ran)")
        return True
    print(f"FAIL  {name}  failed at {s.get('failed_step_id')}: {s.get('message')}")
    for c in s.get("checks") or []:
        for issue in c.get("issues") or []:
            msg = issue.get("message") if isinstance(issue, dict) else issue
            print(f"        - {c.get('step_id')} check: {msg}")
    for v in s.get("verdicts") or []:
        if not v.get("passed"):
            print(f"        - {v.get('step_id')} run {v.get('run_id')}: {v.get('reason')}")
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="job 1's --out directory")
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

    ok, running = True, {}
    for path in files:
        with open(path, encoding="utf-8") as fh:
            recipe = json.load(fh)
        name = recipe.get("f_id") or os.path.basename(path)
        status, body = call("POST", args.url, secret, {"recipe": recipe, **where})
        if status == 200 and body.get("chain_id"):
            print(f"START {name}  {body['chain_id']}")
            running[name] = body["chain_id"]
        else:
            refused(name, status, body)
            ok = False

    query = urllib.parse.urlencode(where)
    deadline = time.monotonic() + DEADLINE_S
    while running and time.monotonic() < deadline:
        time.sleep(POLL_S)
        for name, chain_id in list(running.items()):
            url = f"{args.url}/{urllib.parse.quote(name, safe='')}/{chain_id}?{query}"
            status, s = call("GET", url, secret)
            if status == 200 and s.get("finished"):
                ok = report(name, s) and ok
                del running[name]
            elif status not in (0, 200, 502, 503, 504):
                refused(name, status, s)
                ok = False
                del running[name]
    for name, chain_id in running.items():
        print(f"FAIL  {name}  {chain_id} did not finish in {DEADLINE_S // 60} min")
        ok = False

    print(f"\n{len(files)} recipe(s) run.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
