#!/usr/bin/env python3
"""
Publishes the WHOLE catalog to single-metadata on a release tag (recipe-catalog-publish.yml):
POST `catalog_url` (.github/recipe-git-validate.json) with the body build_catalog.py wrote and
the header `x-recipe-validate-secret` (env RECIPE_GIT_VALIDATE_SECRET, the secret the other
recipe routes check). SM upserts by frontmatter_id (unchanged skipped, changed = a new version,
missing from the body = archived) and answers
`{created, versioned, unchanged, archived, refused: [{frontmatter_id, problems}], warnings}`.

Exit 0 when SM accepted every recipe, 1 when it refused any (they stay unpublished; the
others are published), 2 when the call itself failed. The secret is never printed.

Usage: publish_catalog.py BODY.json [--config .github/recipe-git-validate.json]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

SECRET_ENV = "RECIPE_GIT_VALIDATE_SECRET"
HEADER = "x-recipe-validate-secret"
TIMEOUT_S = 300


def post(url: str, body: bytes, secret: str, opener=urllib.request.urlopen) -> dict:
    request = urllib.request.Request(url, data=body, method="POST",
                                     headers={"Content-Type": "application/json", HEADER: secret})
    with opener(request, timeout=TIMEOUT_S) as response:
        return json.loads(response.read().decode("utf-8") or "{}")


def summary(answer: dict) -> tuple[str, int]:
    counts = {key: answer.get(key) for key in ("created", "versioned", "unchanged", "archived")}
    lines = ["published: " + ", ".join(f"{key} {len(value) if isinstance(value, list) else value}"
                                       for key, value in counts.items())]
    refused = answer.get("refused") or []
    for item in refused:
        lines.append(f"REFUSED {item.get('frontmatter_id')}: " + "; ".join(item.get("problems") or []))
    for item in answer.get("warnings") or []:
        lines.append(f"WARNING {item}")
    return "\n".join(lines), 1 if refused else 0


def main(argv=None, opener=urllib.request.urlopen) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("body")
    parser.add_argument("--config", default=".github/recipe-git-validate.json")
    args = parser.parse_args(argv)
    secret = os.environ.get(SECRET_ENV, "")
    if not secret:
        print(f"::error::{SECRET_ENV} is not set")
        return 2
    with open(args.config, encoding="utf-8") as handle:
        url = json.load(handle).get("catalog_url")
    if not url:
        print(f"::error::no catalog_url in {args.config}")
        return 2
    with open(args.body, "rb") as handle:
        body = handle.read()
    if not json.loads(body).get("recipes"):
        print("::error::the body has no recipes; an empty catalog is never published")
        return 2
    try:
        answer = post(url, body, secret, opener)
    except urllib.error.HTTPError as error:
        print(f"::error::single-metadata answered {error.code} to the catalog publish")
        return 2
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        print(f"::error::the catalog publish failed: {error.__class__.__name__}")
        return 2
    text, code = summary(answer)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
