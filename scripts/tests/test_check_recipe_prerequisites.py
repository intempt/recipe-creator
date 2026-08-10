#!/usr/bin/env python3
"""Shape tests for the prerequisite guard's YAML parsing.

Written 2026-08-10 after a review found the first `declared()` was case-sensitive
and matched only inline flow-maps with unquoted values. `- value: stripe` on its
own line, `value: "stripe"`, and `Integrations:` all read as *undeclared*, so a
correctly-written recipe would have failed the guard. None of the 302 recipes
happened to use those shapes, so it never fired.

That is the thing worth testing. A guard that is right about the corpus it was
written against tells you nothing about the next recipe someone writes, and the
failure mode here is loud in one direction (a good recipe blocked) and silent in
the other (a bad one waved through).

Run: python3 scripts/tests/test_check_recipe_prerequisites.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "guard", ROOT / "scripts" / "check_recipe_prerequisites.py"
)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def fm(inner: str) -> str:
    """A recipe skeleton with `inner` inside `intempt.prerequisites`."""
    return (
        "---\nname: x\nintempt:\n  prerequisites:\n" + inner + "  scope: global\n---\nbody\n"
    )


CASES: list[tuple[str, str, set[str]]] = [
    ("inline unquoted", fm("    integrations:\n      - { value: stripe, severity: blocking }\n"), {"stripe"}),
    ("double-quoted", fm('    integrations:\n      - { value: "salesforce", severity: blocking }\n'), {"salesforce"}),
    ("single-quoted", fm("    integrations:\n      - { value: 'shopify', severity: blocking }\n"), {"shopify"}),
    ("block-style", fm("    integrations:\n      - value: hubspot\n        severity: blocking\n"), {"hubspot"}),
    ("capitalised key", fm("    Integrations:\n      - { value: kafka, severity: blocking }\n"), {"kafka"}),
    ("two entries", fm("    integrations:\n      - { value: stripe, severity: blocking }\n      - { value: slack, severity: recommended }\n"), {"stripe", "slack"}),
    ("events block before", fm("    events:\n      - { value: order_placed, severity: blocking }\n    integrations:\n      - { value: shopify, severity: blocking }\n"), {"shopify"}),
    ("events block after", fm("    integrations:\n      - { value: shopify, severity: blocking }\n    events:\n      - { value: order_placed, severity: blocking }\n"), {"shopify"}),
    ("no integrations key", fm("    events:\n      - { value: order_placed, severity: blocking }\n"), set()),
    # The silent direction: a block in the markdown body is documentation, not a
    # declaration. Counting it would wave through a genuinely undeclared recipe.
    ("body block does not count", "---\nname: x\nintempt:\n  scope: global\n---\nExample:\n    integrations:\n      - { value: stripe, severity: blocking }\n", set()),
]


def main() -> int:
    failed = 0
    for name, text, want in CASES:
        got = guard.declared(text)
        ok = got == want
        failed += not ok
        print(f"  {'PASS' if ok else 'FAIL'}  {name:<28} got={sorted(got)} want={sorted(want)}")
    total = len(CASES)
    print(f"\nguard shape tests: {total - failed}/{total} pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
