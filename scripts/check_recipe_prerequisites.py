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
prerequisites must say shopify.

**The original version of this docstring got the trade-off wrong**, and an
adversarial review found six recipes where the mistake had already landed. It
said "over-declaring costs a customer one connect prompt". That is true of
`recommended` and false of `blocking`: a blocking prerequisite **disables Run
entirely**. Four segment and personalization recipes that need no connector at
all had Run disabled, because a vendor name appeared in a customer logo
(`<img src="/customers/stripe-logo.svg">`), an industry citation ("Demandbase,
Gartner, Salesforce all use this benchmark"), a PLG example ("the canonical
Slack/Dropbox/Figma pattern"), or a domain-classification example ("generic
email domains (gmail, outlook)").

So over-declaring is not the safe direction. Both directions are wrong, in
different ways, and the guard cannot tell a logo from a data source. Where a
mention is genuinely not usage, it goes in EXEMPT below with the reason — an
explicit, reviewable list, rather than a fake prerequisite that breaks the
recipe.

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


# Mentions that are provably not integration usage. Each entry is (path, vendor)
# with the reason, so removing one is a decision someone has to argue for rather
# than a silent edit. Added 2026-08-10 after a review found the guard forcing
# these six declarations, four of them blocking.
EXEMPT: dict[tuple[str, str], str] = {
    ("recipes/personalizations/abm-account-personalization_recipe.md", "stripe"):
        "customer logo in a social-proof hero variant, not a data source",
    ("recipes/personalizations/intent-data-content-personalization_recipe.md", "salesforce"):
        "logo in an 'integrations we support' marketing mockup",
    ("recipes/personalizations/intent-data-content-personalization_recipe.md", "slack"):
        "logo in the same marketing mockup",
    ("recipes/segments/pql-multi-user-account_recipe.md", "slack"):
        "cited as a PLG company ('the canonical Slack/Dropbox/Figma pattern'), not the app",
    ("recipes/segments/enterprise-accounts_recipe.md", "salesforce"):
        "industry citation for the 1000-employee threshold",
    ("recipes/segments/multi-stakeholder-engaged-accounts_recipe.md", "salesforce"):
        "cited as the source of the 11-stakeholder statistic",
    ("recipes/workflows/enterprise-domain-signup-to-ae-task_recipe.md", "gmail"):
        "an example of a generic email domain being classified, not a mailbox",
}


def frontmatter(text: str) -> str:
    """Only the YAML frontmatter counts as a declaration.

    A `- { value: shopify }` line in the markdown body — a documentation example,
    say — used to satisfy the guard, so a genuinely undeclared recipe could pass.
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    return m.group(1) if m else ""


def declared(text: str) -> set[str]:
    """Values declared under `prerequisites.integrations`, in any YAML shape.

    The first version matched only inline flow-maps with unquoted values and was
    case-sensitive, so `- value: stripe` on its own line, `value: "stripe"`, and
    `Integrations:` all read as *undeclared* — a correctly-written recipe would
    have failed the guard. None of the 302 recipes used those shapes, so it never
    fired; that is luck, not correctness.
    """
    fm = frontmatter(text)
    lines = fm.splitlines()
    start = None
    key_indent = 0
    for n, line in enumerate(lines):
        m = re.match(r"^(\s*)integrations:\s*$", line, re.I)
        if m:
            start, key_indent = n + 1, len(m.group(1))
            break
    if start is None:
        return set()

    # Everything indented deeper than the key belongs to the block. Bounding it
    # by indentation rather than by a lookahead for the next key is the whole
    # point: a lookahead has to predict the shape of whatever follows, and the
    # first attempt at one silently matched nothing when the next line was
    # `scope: global` — a value on the same line as its key, which is ordinary.
    body = []
    for line in lines[start:]:
        if line.strip() and len(line) - len(line.lstrip()) <= key_indent:
            break
        body.append(line)

    return {
        v.lower()
        for v in re.findall(r"value:\s*[\"']?([A-Za-z0-9_\-]+)", "\n".join(body))
    }


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
            if prose in lowered
            and value not in have
            and (path, value) not in EXEMPT
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
