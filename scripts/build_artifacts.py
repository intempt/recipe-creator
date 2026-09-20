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
import re
import sys

import yaml

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


class RecipeError(Exception):
    pass


def read_recipes(recipes_dir):
    recipes = []
    for path in sorted(recipes_dir.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            raise RecipeError(f"{path}: no YAML frontmatter")
        try:
            front = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            raise RecipeError(f"{path}: {exc}") from exc
        intempt = front.get("intempt") or {}
        if not intempt.get("id"):
            raise RecipeError(f"{path}: intempt.id is required")
        recipes.append((path, front, intempt))
    return recipes


PUBLIC_STEP_FIELDS = ("step", "title", "command", "produces", "bindsAs", "dependsOn", "description")


def public_step(step):
    """bindsAs and dependsOn stay because they are the edges the recipe graph is
    drawn from. prompt is dropped: it is the instruction Blu executes, it is the
    bulk of the payload, and this file is served publicly."""
    return {k: step[k] for k in PUBLIC_STEP_FIELDS if k in step}


SHORT_DESCRIPTION_MAX = 200
STEP_TITLE_MAX = 40


def is_public(intempt):
    return (intempt.get("scope") or "") == "global" and (intempt.get("visibility") or "") == "published"


def catalog_entry(front, intempt):
    outputs = intempt.get("outputs") or []
    """description is deliberately absent. That field is Blu's intent-matching
    string ("Use when a user mentions ..."), written to route an AI, and the
    console was rendering it to customers as though it were copy. Leaving it out
    of the public catalog means no surface can make that mistake again."""
    entry = {
        "slug": intempt["id"],
        "name": front.get("name") or intempt["id"],
        "title": intempt.get("title") or "",
        "group": intempt.get("group") or "",
        "shortDescription": intempt.get("shortDescription") or "",
        "classification": intempt.get("classification") or {},
        "procedure": [public_step(s) for s in (intempt.get("procedure") or [])],
        "outputs": outputs,
        "outputCount": len(outputs),
    }
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

    leaked = [e["slug"] for e in public
              if any("prompt" in step for step in e["procedure"])]
    for slug in leaked:
        problems.append(f"{slug}: a step prompt reached the public catalog")

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
