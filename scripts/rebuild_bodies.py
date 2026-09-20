#!/usr/bin/env python3
"""Regenerate each recipe's markdown body from its frontmatter.

The body is the human walkthrough under the `---` fence. It restates the title,
the summary and the steps, which means it is a second copy of the same facts and
it drifts the moment the frontmatter is edited. Rewriting the customer copy across
all 302 recipes left every body quoting step titles that no longer exist.

So the body stops being written by hand. It is generated from the frontmatter,
which is the one place those facts live, and `--check` fails when a committed body
does not match what the frontmatter would produce.

The body is not published: the catalog carries the frontmatter only, and neither
the website nor the console reads it. It exists for someone reading the repo, and
that is exactly the reader a stale body misleads.
"""

import argparse
import pathlib
import re
import sys

import yaml

FRONTMATTER = re.compile(r"^(---\n.*?\n---\n)(.*)$", re.S)
MARKER = "<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->"


def body_for(intempt):
    title = intempt.get("title") or intempt.get("id")
    lines = [MARKER, "", f"# {title}", ""]

    summary = (intempt.get("shortDescription") or "").strip()
    if summary:
        lines += [summary, ""]

    prereqs = intempt.get("prerequisites") or {}
    integrations = [p.get("value") for p in (prereqs.get("integrations") or []) if p.get("value")]
    events = [p.get("value") for p in (prereqs.get("events") or []) if p.get("value")]
    if integrations or events:
        lines += ["## Before you run it", ""]
        for value in integrations:
            lines.append(f"- Connect {value}")
        for value in events:
            lines.append(f"- Send the `{value}` event")
        lines.append("")

    procedure = intempt.get("procedure") or []
    if procedure:
        lines += ["## What it does", ""]
        for step in procedure:
            step_title = (step.get("title") or "").strip()
            description = " ".join((step.get("description") or "").split())
            command = step.get("command") or ""
            lines.append(f"{step.get('step')}. **{step_title}** (`{command}`)")
            if description:
                lines += ["", f"   {description}"]
            lines.append("")

    outputs = intempt.get("outputs") or []
    if outputs:
        lines += ["## What you end up with", ""]
        for output in outputs:
            description = " ".join((output.get("description") or "").split())
            lines.append(f"- **{output.get('name')}** ({output.get('type')}): {description}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--recipes", default="recipes", type=pathlib.Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    stale = []
    written = 0

    for path in sorted(args.recipes.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            print(f"error: {path}: no frontmatter", file=sys.stderr)
            return 2
        head, current = match.group(1), match.group(2)
        try:
            front = yaml.safe_load(head.strip("-\n")) or {}
        except yaml.YAMLError as exc:
            print(f"error: {path}: {exc}", file=sys.stderr)
            return 2

        wanted = body_for(front.get("intempt") or {})
        if current == wanted:
            continue
        if args.check:
            stale.append(path)
        else:
            path.write_text(head + wanted, encoding="utf-8")
            written += 1

    if args.check:
        if stale:
            print(f"{len(stale)} body/bodies do not match their frontmatter:", file=sys.stderr)
            for path in stale[:20]:
                print(f"  {path}", file=sys.stderr)
            if len(stale) > 20:
                print(f"  ... and {len(stale) - 20} more", file=sys.stderr)
            print("\nRegenerate with scripts/rebuild_bodies.py, do not hand edit.", file=sys.stderr)
            return 1
        print("every body matches its frontmatter")
        return 0

    print(f"{written} body/bodies regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
