#!/usr/bin/env python3
"""Convert consolev2-loveable TypeScript recipe files to .md with YAML frontmatter.

Reads all .ts recipe files from consolev2-loveable/src/data/recipes/v2/global/,
parses the JSON-like objects, and writes .md files in the format expected by
single-metadata's RecipeMdParser.
"""
import json
import os
import re
import sys
import yaml


SOURCE_DIR = os.path.expanduser(
    "~/Intempt/consolev2-loveable/src/data/recipes/v2/global"
)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "recipes")


def extract_json_from_ts(ts_content: str) -> dict:
    content = re.sub(r"^import\s+.*;\s*\n", "", ts_content, flags=re.MULTILINE)
    content = re.sub(r"^export\s+const\s+\w+:\s*Recipe\s*=\s*", "", content, flags=re.MULTILINE)
    content = re.sub(r"\s*as\s+const;\s*$", "", content.rstrip())
    content = content.rstrip().rstrip(";")
    content = re.sub(r",(\s*[}\]])", r"\1", content)
    return json.loads(content)


def recipe_to_md(recipe: dict) -> str:
    fm = {}
    fm["name"] = recipe.get("name", "")
    fm["description"] = recipe.get("shortDescription", "")

    intempt = {}
    intempt["id"] = recipe.get("id", "")
    intempt["version"] = recipe.get("version", "1.0.0")
    intempt["slashCommand"] = recipe.get("slashCommand", f"/{recipe.get('id', '')}")
    intempt["shortDescription"] = recipe.get("shortDescription", "")

    if recipe.get("author"):
        intempt["author"] = recipe["author"]

    if recipe.get("classification"):
        cls = recipe["classification"]
        intempt["classification"] = {}
        for key in ["product", "agent", "mode", "complexity", "executionMode", "tags", "object"]:
            if key in cls and cls[key] is not None:
                intempt["classification"][key] = cls[key]

    intempt["scope"] = recipe.get("scope", "global")
    intempt["visibility"] = recipe.get("visibility", "published")
    intempt["accessTier"] = recipe.get("accessTier", "free")
    intempt["aiPassRequired"] = recipe.get("aiPassRequired", True)

    if recipe.get("outputs"):
        intempt["outputs"] = recipe["outputs"]
    if recipe.get("steps"):
        intempt["steps"] = recipe["steps"]
    if recipe.get("inputs"):
        intempt["inputs"] = recipe["inputs"]
    if recipe.get("prerequisites"):
        intempt["prerequisites"] = recipe["prerequisites"]
    if recipe.get("chainable"):
        intempt["chainable"] = recipe["chainable"]
    if recipe.get("replaces"):
        intempt["replaces"] = recipe["replaces"]

    fm["intempt"] = intempt

    yaml_str = yaml.dump(fm, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

    name = recipe.get("name", "Recipe")
    desc = recipe.get("shortDescription", "")

    body_parts = [f"# {name}", ""]
    if desc:
        body_parts.append(desc)
        body_parts.append("")

    if recipe.get("outputs"):
        body_parts.append("## Outputs")
        body_parts.append("")
        for out in recipe["outputs"]:
            body_parts.append(f"- **{out.get('name', 'output')}** ({out.get('type', 'unknown')}): {out.get('description', '')}")
        body_parts.append("")

    if recipe.get("steps"):
        body_parts.append("## Steps")
        body_parts.append("")
        for i, step in enumerate(recipe["steps"], 1):
            step_desc = step.get("describe", step.get("description", ""))
            body_parts.append(f"{i}. {step_desc}")
        body_parts.append("")

    if recipe.get("prerequisites"):
        prereqs = recipe["prerequisites"]
        if prereqs.get("integrations"):
            body_parts.append("## Prerequisites")
            body_parts.append("")
            for integ in prereqs["integrations"]:
                if isinstance(integ, str):
                    body_parts.append(f"- Integration: **{integ}**")
                else:
                    body_parts.append(f"- Integration: **{integ['value']}** ({integ.get('severity', 'blocking')})")
            body_parts.append("")

    body = "\n".join(body_parts)
    return f"---\n{yaml_str}---\n\n{body}"


def convert_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ts_files = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.endswith(".ts") and f not in ("index.ts", "types.ts"):
                ts_files.append(os.path.join(root, f))

    success = 0
    errors = []

    for ts_path in sorted(ts_files):
        rel = os.path.relpath(ts_path, SOURCE_DIR)
        category = os.path.dirname(rel)
        slug = os.path.splitext(os.path.basename(rel))[0]

        try:
            with open(ts_path, "r") as fh:
                ts_content = fh.read()
            recipe = extract_json_from_ts(ts_content)
            md_content = recipe_to_md(recipe)

            out_dir = os.path.join(OUTPUT_DIR, category)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, f"{slug}.md")

            with open(out_path, "w") as fh:
                fh.write(md_content)

            success += 1
        except Exception as e:
            errors.append((rel, str(e)))

    print(f"Converted {success}/{len(ts_files)} recipes")
    if errors:
        print(f"\n{len(errors)} errors:")
        for path, err in errors[:10]:
            print(f"  {path}: {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

    return success, errors


if __name__ == "__main__":
    success, errors = convert_all()
    sys.exit(0 if not errors else 1)
