"""
Where the git Validate CI sends recipes and runs them:
`.github/recipe-git-validate.json`.

None of it is secret, so it is committed config, not repo secrets; the one
secret is still RECIPE_GIT_VALIDATE_SECRET. An env var of the same name as a
key below overrides the file, for a local run (e.g. against localhost:8211):
RECIPE_GIT_VALIDATE_URL, RECIPE_GIT_RUN_ORG_ID, RECIPE_GIT_RUN_PROJECT_ID,
RECIPE_GIT_RUN_PERSON_ID.
"""
from __future__ import annotations

import json
import os

CONFIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      ".github", "recipe-git-validate.json")


def load(path: str = CONFIG) -> dict:
    with open(path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    run = cfg.get("run", {})
    out = {"url": os.environ.get("RECIPE_GIT_VALIDATE_URL") or cfg.get("url", "")}
    for k in ("org_id", "project_id", "person_id"):
        v = run.get(k)
        out[k] = os.environ.get(f"RECIPE_GIT_RUN_{k.upper()}") or ("" if v is None else str(v))
    return out
