#!/usr/bin/env python3
"""
The whole catalog as portable recipes (scripts/portable.py), the body single-metadata's
`POST /v1/recipes/catalog` takes: `{ref, recipes: [...]}`.

Usage:
  build_catalog.py [--root .] [--ref REF] [--out catalog.json]   # write the body
  build_catalog.py --check [--root .]                             # SM's publish checks, locally

--check prints every refused recipe with its problems and the warnings, and exits 1 when
any recipe would be refused (the release tag would publish an incomplete catalog).
"""
from __future__ import annotations

import argparse
import json
import sys

import portable


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--ref", default="")
    parser.add_argument("--out", default="")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    found = portable.catalog(args.root)
    if args.check:
        refused = 0
        for path, recipe in found:
            problems = portable.problems(recipe)
            if problems:
                refused += 1
                print(f"REFUSED {recipe.get('frontmatter_id') or path}: " + "; ".join(problems))
            for warning in portable.warnings(recipe):
                print(f"WARNING {recipe.get('frontmatter_id') or path}: {warning}")
        print(f"{len(found)} recipes, {refused} refused")
        return 1 if refused else 0
    body = {"ref": args.ref, "recipes": [recipe for _, recipe in found]}
    text = json.dumps(body, ensure_ascii=False, indent=1)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        print(f"{len(found)} recipes written to {args.out}")
    else:
        sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
