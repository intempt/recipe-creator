#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from recipe_contract import FRONTMATTER, builds_for_command, render_body

ROUTING_PREFIX = re.compile(r"^Use when a user mentions .*?(?:, or asks for related help\.\s*|\.\s+)", re.S)
PLACEHOLDER = re.compile(r"\{\{\s*([^}]*?)\s*\}\}")


class Literal(str):
    pass


class Block(str):
    pass


def literal_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=">")


def block_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|" if "\n" in data else ">")


class Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


Dumper.add_representer(Literal, literal_representer)
Dumper.add_representer(Block, block_representer)


def plain_placeholder(match):
    owner, _, field = match.group(1).partition(".")
    return f"the {owner}'s {field.replace('_', ' ')}" if field else match.group(1).replace("_", " ")


def clean_instruction(text):
    lines = [re.sub(r"[ \t]+", " ", line).rstrip() for line in PLACEHOLDER.sub(plain_placeholder, text).strip().splitlines()]
    return "\n".join(line for line in lines if line.strip())


def convert(front, path, owner="intempt"):
    i = front["intempt"]
    steps_v1 = i.get("procedure") or []
    sid_by_bind = {}
    title_by_sid = {}
    steps = []
    for n, s in enumerate(steps_v1, start=1):
        sid = f"s{n}"
        deps = [sid_by_bind[d] for d in (s.get("dependsOn") or []) if d in sid_by_bind]
        upstream = {sid_by_bind[d]: title_by_sid[sid_by_bind[d]] for d in (s.get("dependsOn") or []) if d in sid_by_bind}
        instruction = clean_instruction(s.get("prompt") or s.get("description") or "")
        missing = [t for t in upstream.values() if t.lower() not in instruction.lower()]
        if missing:
            instruction += " Use the result of " + ", ".join(f'"{t}"' for t in missing) + "."
        step = {
            "id": sid,
            "title": s["title"],
            "summary": Literal(re.sub(r"\s+", " ", s.get("description") or "").strip()),
            "builds": builds_for_command(s["command"]),
            "description": Block(instruction),
        }
        if deps:
            step["dependsOn"] = deps
        steps.append(step)
        if s.get("bindsAs"):
            sid_by_bind[s["bindsAs"]] = sid
        title_by_sid[sid] = s["title"]

    outputs = []
    binds = {s.get("bindsAs"): f"s{n}" for n, s in enumerate(steps_v1, start=1) if s.get("bindsAs")}
    produces = {}
    for n, s in enumerate(steps_v1, start=1):
        produces[s.get("produces")] = f"s{n}"
    used = set()
    for o in i.get("outputs") or []:
        sid = binds.get(o["name"]) or produces.get(o.get("type"))
        key = o["name"]
        while key in used:
            key += "_2"
        used.add(key)
        out = {"key": key, "producedByStep": sid, "type": o.get("type")}
        if o.get("description"):
            out["description"] = o["description"]
        outputs.append(out)

    routing = (front.get("description") or "").strip()
    intent = ROUTING_PREFIX.sub("", routing).strip() or i.get("shortDescription", "")

    v2 = {
        "id": i["id"],
        "title": i["title"],
        "slash_command": i["slashCommand"],
        "group": i["group"],
        "owner": owner,
        "summary": i["shortDescription"],
        "description": Literal(re.sub(r"\s+", " ", intent)),
        "version": "2.0.0",
        "classification": i.get("classification") or {},
    }
    if i.get("prerequisites"):
        v2["prerequisites"] = i["prerequisites"]
    v2["steps"] = steps
    v2["outputs"] = outputs
    return v2


def dump(v2):
    text = yaml.dump(v2, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=100)
    return f"---\n{text}---\n{render_body(v2)}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default="recipes", type=pathlib.Path)
    parser.add_argument("--dst", default="recipes", type=pathlib.Path)
    parser.add_argument("--file", type=pathlib.Path, help="Convert one v1 file instead of every file under --src.")
    parser.add_argument("--owner", default="intempt", help="Partner folder the converted recipe belongs to.")
    args = parser.parse_args()
    old = [args.file] if args.file else sorted(args.src.glob("*/*_recipe.md"))
    for path in old:
        match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
        if not match or "intempt" not in (yaml.safe_load(match.group(1)) or {}):
            print(f"error: {path} is not a v1 recipe with an intempt: block", file=sys.stderr)
            return 2
        front = yaml.safe_load(match.group(1))
        v2 = convert(front, path, args.owner)
        out = args.dst / args.owner / v2["id"] / "recipe.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(dump(v2), encoding="utf-8")
    print(f"converted {len(old)} recipe(s) into {args.dst}/{args.owner}/; add touches before validating")


if __name__ == "__main__":
    sys.exit(main())
