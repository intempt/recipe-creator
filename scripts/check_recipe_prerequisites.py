#!/usr/bin/env python3
"""
Fail when a recipe names an integration it does not declare as a prerequisite.

Why this exists
---------------
The Blu Chat spec requires two things of every recipe (BC-RCP-010, BC-RCP-012):
Blu must check prerequisite status before offering Run, disable Run with a
"Connect X" affordance when something is missing, and explain *why* it is
needed. Both read `prerequisites.integrations`.

287 of 292 recipes declared nothing. Recipes named Salesforce, Shopify, HubSpot
and Stripe in their descriptions and prompts, so a customer could open one, see
Run enabled, and get a workflow that fails at the connector — the requirement
was written and nothing enforced it, so the catalogue drifted away from it
silently and completely.

This is the enforcement. It is deliberately dumb: if the text says Shopify, the
prerequisites must say shopify. A false positive is a recipe that mentions a
vendor in passing, and the fix for that is to declare it anyway — over-declaring
costs a customer one connect prompt, under-declaring costs them a failed run
they cannot diagnose.

Usage:  python3 scripts/check_recipe_prerequisites.py [--fix-list]
"""
from __future__ import annotations

import glob
import re
import sys

# Vendor as it appears in prose -> the value a recipe must declare.
VENDORS: dict[str, str] = {
    "hubspot": "hubspot",
    "salesforce": "salesforce",
    "stripe": "stripe",
    "shopify": "shopify",
    "slack": "slack",
    "gmail": "gmail",
    "google sheets": "google_sheets",
    "sendgrid": "sendgrid",
    "twilio": "twilio",
    "kafka": "kafka",
}

# A connector the recipe reads from is blocking; one it only delivers through is
# recommended. The distinction is what makes the Run button honest rather than
# merely cautious — a recipe that only posts a Slack summary still works with
# Slack disconnected, minus the summary.
DELIVERY_ONLY = {"slack", "gmail", "sendgrid", "twilio"}


def declared(text: str) -> set[str]:
    block = re.search(r"^\s*integrations:\s*\n((?:\s*-\s*\{[^}]*\}\s*\n)+)", text, re.M)
    if not block:
        return set()
    return {v.lower() for v in re.findall(r"value:\s*([A-Za-z0-9_\-]+)", block.group(1))}


def main() -> int:
    failures: list[tuple[str, list[str]]] = []
    files = sorted(glob.glob("recipes/**/*.md", recursive=True))

    for path in files:
        text = open(path, errors="ignore").read()
        lowered = text.lower()
        have = declared(text)
        missing = [
            value
            for prose, value in VENDORS.items()
            if prose in lowered and value not in have
        ]
        if missing:
            failures.append((path, sorted(set(missing))))

    if not failures:
        print(f"recipe prerequisites: pass ({len(files)} recipes checked).")
        return 0

    print(f"recipe prerequisites: {len(failures)} recipe(s) name an integration they do not declare.\n")
    for path, missing in failures:
        print(f"  {path}")
        for value in missing:
            severity = "recommended" if value in DELIVERY_ONLY else "blocking"
            print(f"      - {{ value: {value}, severity: {severity} }}")
    print(
        "\nAdd the rows above under `prerequisites.integrations`.\n"
        "Blu cannot disable Run for a prerequisite a recipe never declares "
        "(BC-RCP-010), and cannot explain why it is needed (BC-RCP-012)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
