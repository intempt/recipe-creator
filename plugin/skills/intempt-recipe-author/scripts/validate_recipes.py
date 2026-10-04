#!/usr/bin/env python3
import argparse
import collections
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from recipe_contract import RecipeError, availability, read, recipe_paths, validate
import injection
import portability

BRACKET = re.compile(r"\[[A-Z][A-Za-z ]+\]")
RATIONALE = re.compile(r"\b(the differentiator|most CDPs|best practice|industry standard|pattern|-style)\b", re.I)
COMPETITORS = re.compile(r"\b(Adobe|Braze|Klaviyo|Iterable|Amplitude|Mixpanel|Segment\.io|HubSpot-style|Salesforce-style)\b")
WHO = re.compile(r"\b(user|users|account|accounts|people|person|customers?|visitors?|shoppers?|members?|leads?|contacts?)\b", re.I)
LONG = 1200


def lint(front):
    warnings = []
    for step in front.get("steps") or []:
        where = step.get("id")
        text = str(step.get("description") or "")
        if BRACKET.search(text):
            warnings.append((where, "bracket placeholder", BRACKET.search(text).group(0)))
        if RATIONALE.search(text):
            warnings.append((where, "rationale, not instruction", RATIONALE.search(text).group(0)))
        if COMPETITORS.search(text):
            warnings.append((where, "names another vendor", COMPETITORS.search(text).group(0)))
        if step.get("builds") == "segment" and not WHO.search(text):
            warnings.append((where, "segment never says who it is about", ""))
        if len(text) > LONG:
            warnings.append((where, f"over {LONG} chars, likely more than one thing", str(len(text))))
    return warnings


def main():
    parser = argparse.ArgumentParser(description="Validate recipe.md files against the v2 contract.")
    parser.add_argument("paths", nargs="*", type=pathlib.Path)
    parser.add_argument("--recipes", default="recipes", type=pathlib.Path)
    parser.add_argument("--lint", action="store_true", help="Also report description quality warnings.")
    args = parser.parse_args()

    paths = args.paths or recipe_paths(args.recipes)
    try:
        _, patterns = injection.load_patterns()
    except injection.PatternsTampered as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    problems = []
    statuses = collections.Counter()
    waiting = collections.Counter()
    lints = collections.Counter()
    linted_install_now = set()
    for path in paths:
        try:
            front, _ = read(path)
        except RecipeError as exc:
            problems.append(str(exc))
            continue
        problems += [f"{path}: {p}" for p in validate(path, front)]
        text = pathlib.Path(path).read_text(encoding="utf-8")
        problems += [f"{path}: injection {f['pattern_id']} at {f['where']}: {f['evidence']}"
                     for f in injection.scan_text(text, patterns) if f["severity"] == "block"]
        problems += [f"{path}: portability {f['kind']} at {f['where']}: {f['evidence']}; move it into inputs"
                     for f in portability.scan_text(text)]
        status, wait = availability(front)
        statuses[status] += 1
        waiting.update(wait)
        if args.lint:
            found = lint(front)
            for where, kind, sample in found:
                lints[kind] += 1
                if len(paths) <= 5:
                    print(f"  lint {path} {where}: {kind} {sample}".rstrip())
            if found and status == "install_now":
                linted_install_now.add(front.get("id"))

    for line in problems[:40]:
        print(f"  {line}", file=sys.stderr)
    print(f"{len(paths)} recipe(s): {statuses['install_now']} install now, {statuses['coming_soon']} coming soon")
    if waiting:
        print("coming soon is waiting on: " + ", ".join(f"{k} {v}" for k, v in waiting.most_common()))
    if args.lint:
        print("lint: " + (", ".join(f"{k} {v}" for k, v in lints.most_common()) or "clean"))
        print(f"lint: {len(linted_install_now)} install-now recipe(s) have at least one warning")
    if problems:
        print(f"{len(problems)} contract problem(s)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
