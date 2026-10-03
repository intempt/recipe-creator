#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from recipe_contract import read


def find_sources(recipes_dir):
    sources = {}
    for path in sorted(pathlib.Path(recipes_dir).glob("*/*/recipe.md")):
        sources[path.parent.name] = path
    return sources


def build_payload(catalog_path, recipes_dir):
    catalog = json.loads(pathlib.Path(catalog_path).read_text())
    recipes = catalog["recipes"]
    problems = []
    seen = set()
    for recipe in recipes:
        slug = recipe.get("slug")
        if not slug:
            problems.append("a catalog recipe has no slug")
            continue
        if slug in seen:
            problems.append(f"slug {slug} appears twice in the catalog")
        seen.add(slug)
    available = find_sources(recipes_dir)
    missing = sorted(seen - set(available))
    problems += [f"{slug}: no recipes/<owner>/{slug}/recipe.md source" for slug in missing]
    for recipe in recipes:
        source = available.get(recipe.get("slug"))
        if not source:
            continue
        instructions = {(s.get("description") or "").strip() for s in (read(source)[0].get("steps") or [])} - {""}
        for step in recipe.get("procedure") or []:
            if (step.get("description") or "").strip() in instructions:
                problems.append(f"{recipe['slug']}: public step {step.get('step')} repeats its engine instruction")
    if problems:
        return None, problems
    sources = {slug: available[slug].read_text() for slug in sorted(seen)}
    return {"version": catalog["version"], "recipes": recipes, "sources": sources}, []


def send(url, payload, token):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        method="PUT",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.status


def main():
    parser = argparse.ArgumentParser(description="Send the Marketplace catalog and recipe sources to single-metadata.")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--recipes", default="recipes")
    parser.add_argument("--out")
    parser.add_argument("--url")
    args = parser.parse_args()

    payload, problems = build_payload(args.catalog, args.recipes)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(payload))
    print(f"{len(payload['recipes'])} recipes at {payload['version']}")
    if not args.url:
        return 0
    token = os.environ.get("MARKETPLACE_SYNC_TOKEN")
    if not token:
        print("MARKETPLACE_SYNC_TOKEN is not set", file=sys.stderr)
        return 2
    try:
        status = send(args.url, payload, token)
    except urllib.error.HTTPError as err:
        print(f"single-metadata refused the sync: {err.code} {err.read().decode(errors='replace')[:500]}", file=sys.stderr)
        return 1
    print(f"synced, {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
