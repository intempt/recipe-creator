#!/usr/bin/env python3
"""Build the public recipe catalog from the recipe .md sources.

This repo is the source of truth. CI publishes the catalog to cdn.intempt.com
and the website and console both read it from there, so neither holds a copy
and the two lists cannot describe the same recipe differently.

The catalog is PUBLIC. It carries only scope: global, visibility: published
recipes, and it never carries step prompts: those are the instructions Blu
executes, not customer copy.
"""

import argparse
import json
import pathlib
import sys


sys.path.insert(0, str(pathlib.Path(__file__).parent))
from recipe_contract import RecipeError, availability, read, recipe_paths, validate


def read_recipes(recipes_dir):
    recipes = []
    for path in recipe_paths(recipes_dir):
        front, _ = read(path)
        if not front.get("id"):
            raise RecipeError(f"{path}: id is required")
        recipes.append((path, front, front))
    return recipes


SHORT_DESCRIPTION_MAX = 200
STEP_TITLE_MAX = 40


def is_public(front):
    return (front.get("visibility") or "published") == "published"


def public_step(n, step):
    entry = {"step": n, "title": step.get("title") or "", "description": step.get("summary") or "", "produces": step.get("builds")}
    if step.get("dependsOn"):
        entry["dependsOn"] = step["dependsOn"]
    return entry


def catalog_entry(front, _):
    outputs = [
        {"name": o.get("key"), "type": o.get("type"), **({"description": o["description"]} if o.get("description") else {})}
        for o in front.get("outputs") or []
    ]
    status, waiting = availability(front)
    entry = {
        "slug": front["id"],
        "name": front["id"],
        "title": front.get("title") or "",
        "group": front.get("group") or "",
        "owner": front.get("owner") or "",
        "shortDescription": front.get("summary") or "",
        "classification": front.get("classification") or {},
        "availability": status,
        "waitingOn": waiting,
        "slashCommand": front.get("slash_command") or "",
        "procedure": [public_step(n, s) for n, s in enumerate(front.get("steps") or [], start=1)],
        "outputs": outputs,
        "outputCount": len(outputs),
    }
    if front.get("curator"):
        entry["curator"] = front["curator"]
    if front.get("prerequisites"):
        entry["prerequisites"] = front["prerequisites"]
    return entry


def dumps(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build the public recipe catalog.")
    parser.add_argument("--recipes", default="recipes", type=pathlib.Path)
    parser.add_argument("--out", type=pathlib.Path, required=True,
                        help="Directory to write the catalog into.")
    parser.add_argument("--version", default="",
                        help="Catalog version stamped into the payload, normally the commit sha.")
    parser.add_argument("--check", action="store_true",
                        help="Validate only. Writes nothing and fails on any problem.")
    args = parser.parse_args()

    try:
        recipes = read_recipes(args.recipes)
    except RecipeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    problems = []
    warnings = []

    ids = [i["id"] for _, _, i in recipes]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"duplicate recipe id: {dup}")

    for path, front, _ in recipes:
        for problem in validate(path, front):
            problems.append(f"{path}: {problem}")

    public = []
    for path, front, intempt in recipes:
        if not is_public(intempt):
            continue
        entry = catalog_entry(front, intempt)
        title = (intempt.get("title") or "").strip()
        if not title:
            problems.append(f"{path}: title is missing. It renders as the id to customers")
        elif title == intempt["id"]:
            problems.append(f"{path}: title is the id. Give it a real name")

        for step in entry["procedure"]:
            n = step.get("step")
            st = (step.get("title") or "").strip()
            sd = (step.get("description") or "").strip()
            if not st:
                problems.append(f"{path}: step {n} has no title")
            elif len(st) > STEP_TITLE_MAX:
                warnings.append(f"{path}: step {n} title is {len(st)} chars, over {STEP_TITLE_MAX}")
            if not sd:
                problems.append(f"{path}: step {n} has no description")
            for glyph, label in (("\u2014", "em-dash"), ("\u2013", "en-dash"), ("\u2192", "arrow")):
                if glyph in st or glyph in sd:
                    problems.append(f"{path}: step {n} contains a {label}")

        short = entry["shortDescription"].strip()
        if not short:
            problems.append(f"{path}: shortDescription is empty")
        elif short[0] in "\"'" and short[-1] in "\"'":
            problems.append(f"{path}: shortDescription is quote-wrapped, so the quote renders")
        elif len(short) > SHORT_DESCRIPTION_MAX:
            warnings.append(f"{path}: shortDescription is {len(short)} chars, over {SHORT_DESCRIPTION_MAX}")
        for glyph, label in (("\u2014", "em-dash"), ("\u2013", "en-dash"), ("\u2192", "arrow")):
            if glyph in short:
                problems.append(f"{path}: shortDescription contains a {label}")
        if not entry["group"].strip():
            problems.append(f"{path}: group is empty")
        public.append(entry)

    instructions = {front["id"]: {s.get("description") for s in front.get("steps") or []} for _, front, _ in recipes}
    leaked = [e["slug"] for e in public
              if any(step["description"] in instructions[e["slug"]] and step["description"] for step in e["procedure"])]
    for slug in leaked:
        problems.append(f"{slug}: a step instruction reached the public catalog")

    if problems:
        print(f"{len(problems)} problem(s) in the recipe sources:", file=sys.stderr)
        for line in problems[:25]:
            print(f"  {line}", file=sys.stderr)
        if len(problems) > 25:
            print(f"  ... and {len(problems) - 25} more", file=sys.stderr)
        return 1

    if warnings:
        print(f"{len(warnings)} warning(s):", file=sys.stderr)
        for line in warnings[:10]:
            print(f"  {line}", file=sys.stderr)
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more", file=sys.stderr)

    skipped = len(recipes) - len(public)
    if args.check:
        print(f"{len(public)} public recipes valid ({skipped} not published)")
        return 0

    catalog = {
        "version": args.version,
        "count": len(public),
        "recipes": sorted(public, key=lambda e: e["slug"]),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "recipes.json").write_text(dumps(catalog), encoding="utf-8")

    groups = sorted({e["group"] for e in public})
    (args.out / "groups.json").write_text(
        dumps({"version": args.version, "groups": groups}), encoding="utf-8")

    print(f"{len(public)} public recipes written to {args.out} ({skipped} not published)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
