#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recipe_contract as rc

TOP_ORDER = ("id", "title", "slash_command", "group", "owner", "curator", "summary", "description", "version",
             "visibility", "classification", "prerequisites", "inputs", "does_not_claim", "touches", "steps", "outputs")
STEP_ORDER = ("id", "title", "summary", "builds", "description", "dependsOn")

TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*)\s*:")
ITEM = re.compile(r"^(\s*)- ")


class NormaliseError(Exception):
    pass


def ranked(order, key):
    return order.index(key) if key in order else len(order)


def blocks(lines, key_pattern):
    out = []
    pending = []
    for line in lines:
        match = key_pattern.match(line)
        if match:
            out.append([match.group(1), pending + [line]])
            pending = []
        elif out:
            out[-1][1].append(line)
        else:
            pending.append(line)
    if pending:
        out.append([None, pending])
    return out


def reorder(lines, key_pattern, order):
    found = sorted(blocks(lines, key_pattern), key=lambda b: ranked(order, b[0]))
    return [line for b in found for line in b[1]]


def reorder_step(item, indent):
    child = " " * (indent + 2)
    first = child + item[0][indent + 2:]
    lines = [first] + item[1:]
    key = re.compile("^" + re.escape(child) + r"([A-Za-z_][\w-]*)\s*:")
    ordered = reorder(lines, key, STEP_ORDER)
    ordered[0] = " " * indent + "- " + ordered[0][indent + 2:]
    return ordered


def reorder_steps(block):
    head, lines = block[0], block[1:]
    items, current, indent = [], None, None
    for line in lines:
        match = ITEM.match(line)
        if match and (indent is None or len(match.group(1)) == indent):
            indent = len(match.group(1))
            current = [line]
            items.append(current)
        elif current is not None:
            current.append(line)
        else:
            return block
    if indent is None:
        return block
    return [head] + [line for item in items for line in reorder_step(item, indent)]


def normalise_head(head):
    lines = head.split("\n")
    found = sorted(blocks(lines, TOP_KEY), key=lambda b: ranked(TOP_ORDER, b[0]))
    return "\n".join(line for name, chunk in found for line in (reorder_steps(chunk) if name == "steps" else chunk))


def normalise(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    head, _ = rc.split(text)
    if head is None:
        raise NormaliseError("no YAML frontmatter")
    try:
        before = yaml.safe_load(head) or {}
        new_head = normalise_head(head)
        after = yaml.safe_load(new_head) or {}
    except yaml.YAMLError as exc:
        raise NormaliseError(str(exc)) from exc
    if before != after:
        raise NormaliseError("reordering would change a frontmatter value; fix the file by hand")
    return "---\n" + new_head + "\n---\n" + rc.render_body(after)


def main():
    parser = argparse.ArgumentParser(description="Normalise recipe.md files: LF endings, no trailing whitespace, keys in template order, body regenerated.")
    parser.add_argument("paths", nargs="+", type=pathlib.Path, help="recipe.md files, or folders to search for them")
    parser.add_argument("--check", action="store_true", help="Write nothing; exit 1 if any file is not normalised.")
    args = parser.parse_args()
    files = rc.recipe_files(args.paths)
    if not files:
        print("normalise: no recipe.md found", file=sys.stderr)
        return 2
    changed, failed = [], []
    for path in files:
        current = path.read_bytes().decode("utf-8")
        try:
            wanted = normalise(current)
        except NormaliseError as exc:
            failed.append(f"{path}: {exc}")
            continue
        if wanted == current:
            continue
        changed.append(path)
        if not args.check:
            path.write_bytes(wanted.encode("utf-8"))
    for line in failed:
        print(f"  {line}", file=sys.stderr)
    if args.check:
        for path in changed:
            print(f"  not normalised: {path}", file=sys.stderr)
        print(f"normalise: {len(files)} file(s), {len(changed)} not normalised, {len(failed)} could not be read")
        return 1 if changed or failed else 0
    print(f"normalise: {len(files)} file(s), {len(changed)} rewritten, {len(failed)} could not be read")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
