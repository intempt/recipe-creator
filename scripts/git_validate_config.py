"""
Where the git Validate CI sends recipes, and where the main-tag deploy calls:
`.github/recipe-git-validate.json`.

None of it is secret, so it is committed config, not repo secrets; the one
secret is still RECIPE_GIT_VALIDATE_SECRET. An env var of the same name as a
key below overrides the file, for a local run (e.g. against localhost:8211):
RECIPE_GIT_VALIDATE_URL for `url`, and RECIPE_DEPLOY_URL for `deploy_url` — SM's global
recipe routes the main-tag deploy calls (recipe_deploy.py).
"""
from __future__ import annotations

import json
import os

CONFIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      ".github", "recipe-git-validate.json")


def load(path: str = CONFIG) -> dict:
    with open(path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    return {"url": os.environ.get("RECIPE_GIT_VALIDATE_URL") or cfg.get("url", ""),
            "deploy_url": os.environ.get("RECIPE_DEPLOY_URL") or cfg.get("deploy_url", "")}
