"""
The portable recipe (blu-on-jp P9 recipes; the engine's design: llm-wrapper / single-metadata
"PHASE9_RECIPES_DESIGN"): what single-metadata's catalog publish route reads, built from a
recipe.md and checked here with the SAME rules the route applies, so a release tag never
fails at SM for a reason CI could have seen.

A recipe.md keeps its front matter and its body. The portable fields live in ONE front-matter
block, `portable:`, so nothing an older reader looks at changes:

  portable:
    summary: What the customer gets, one sentence, at most 200 characters.
    tags: [ecommerce, email]
    pattern: abandoned_cart          # optional build hint (an automation template)
    eval_case_id: rcp-...             # optional, set by the engine team
    parameters:                       # values a person may change (were `inputs`)
      - {name: discount, type: enum, label: Discount, default: "10%", options: ["0%", "10%"]}
    requirements:                     # what the project must have, by type (were `touches` / `prerequisites`)
      - {slot: purchase, kind: event, meaning: A customer completed an order,
         properties: [{name: order_value, type: number, meaning: the order total}]}
      - {slot: email_sender, kind: integration, channel: email, meaning: The email sender}
    steps:                            # one per body "## Step N", by id s1, s2 ...
      - {id: s1, builds: email, uses: [purchase, discount],
         instruction: "Write a thank-you email for people who did {purchase} ..."}

A step's instruction names `{slot}`, `{slot.<property>}` and `{parameter}`, never a real event,
attribute or id: the engine binds each slot to the project's own object when the recipe runs.
Without `instruction` the body's prose is the step's text.
"""
from __future__ import annotations

import glob
import os
import re

import recipe_draft

MAX_STEP_CHARS = 1200
MAX_SUMMARY_CHARS = 200
MAX_DESCRIPTION_CHARS = 300
PARAMETER_TYPES = {"string", "number", "boolean", "enum", "duration", "date", "text", "attachment"}
REQUIREMENT_KINDS = {"event", "attribute", "segment", "product_feed", "integration", "destination", "brand",
                     "knowledge"}
CHANNEL_KINDS = {"integration", "destination"}
# What a step builds (the engine's builder words; anything else makes the recipe Coming soon there).
BUILDS = {"email", "email_html", "email_plain", "sms", "push", "slack", "image", "segment", "attribute", "event",
          "automation", "report", "dashboard", "journey", "workflow", "experiment", "personalization",
          "recommendation", "video", "page", "content", "snippet", "agent", "meeting", "meeting_type", "account",
          "task", "avatar", "pose", "scene", "design_system", "json", "knowledge", "webhook"}

NAME = re.compile(r"^[a-z][A-Za-z0-9_]{0,63}$")
BRACKET_PLACEHOLDER = re.compile(r"\[[A-Z][A-Za-z ]{1,30}]")
LIQUID_PLACEHOLDER = re.compile(r"\{\{.*?}}|\{%.*?%}", re.S)
REFERENCE = re.compile(r"(?<!\{)\{([A-Za-z][A-Za-z0-9_]*)(?:\.[A-Za-z_]+)?}")
INJECTION = [re.compile(pattern, re.I) for pattern in (
    r"ignore (all |any )?(the )?(previous|prior|above) (instructions|rules|messages)",
    r"disregard (all |the )?(previous|prior|above|system)",
    r"\bsystem prompt\b",
    r"</?(system|assistant|user)>",
    r"\byou are now\b",
    r"\b(reveal|print|show) (your|the) (instructions|prompt|secrets?)\b")]
OTHER_VENDORS = ("klaviyo", "braze", "iterable", "customer.io", "mailchimp", "lovable", "attentive", "omnisend",
                 "bloomreach", "moengage", "clevertap", "insider.com")
INTEGRATION_WORDS = {"slack": "slack", "sms": "sms", "twilio": "sms", "sendgrid": "email", "gmail": "email",
                     "hubspot": "hubspot", "salesforce": "salesforce", "shopify": "shopify",
                     "google sheets": "google_sheets"}

TITLE = re.compile(r"^#[ \t]+(.+?)\s*$", re.M)
STEP = re.compile(r"^##[ \t]+Step[ \t]+(\d+)[ \t]*:[ \t]*(.+?)\s*$", re.M)
USES_RESULT = re.compile(r'Use the result of "([^"]+)"')


def read(path: str) -> tuple[dict, str]:
    with open(path, encoding="utf-8") as handle:
        return recipe_draft.split(handle.read())


def body_steps(body: str) -> list[dict]:
    """The body's `## Step N: title` sections: `[{id, title, text, dependsOn}]` (dependsOn from "Use the result
    of "<title>"", the git format's way of naming an earlier step)."""
    found = list(STEP.finditer(body or ""))
    steps = []
    for index, match in enumerate(found):
        end = found[index + 1].start() if index + 1 < len(found) else len(body)
        text = body[match.end():end].strip()
        steps.append({"id": f"s{match.group(1)}", "title": match.group(2).strip(), "text": text})
    by_title = {step["title"]: step["id"] for step in steps}
    for step in steps:
        step["dependsOn"] = [by_title[title] for title in USES_RESULT.findall(step["text"])
                             if title in by_title and by_title[title] != step["id"]]
    return steps


def title_of(front: dict, body: str) -> str:
    found = TITLE.search(body or "")
    return str(front.get("title") or (found.group(1) if found else "")).strip()


def build(front: dict, body: str) -> dict:
    """The portable recipe (single-metadata's `RecipePayload`, snake_case) of one recipe.md."""
    portable = front.get("portable") if isinstance(front.get("portable"), dict) else {}
    meta = {str(item.get("id")): item for item in portable.get("steps") or [] if isinstance(item, dict)}
    steps = []
    for step in body_steps(body):
        extra = meta.get(step["id"], {})
        out = {"id": step["id"], "title": step["title"],
               "instruction": str(extra.get("instruction") or step["text"]).strip(),
               "builds": str(extra.get("builds") or "").strip()}
        uses = [str(item) for item in extra.get("uses") or []]
        if uses:
            out["uses"] = uses
        depends = [str(item) for item in extra.get("dependsOn") or step["dependsOn"]]
        if depends:
            out["dependsOn"] = depends
        steps.append(out)
    tags = portable.get("tags")
    if not tags:
        classification = front.get("classification") if isinstance(front.get("classification"), dict) else {}
        tags = sorted({str(value) for values in classification.values() if isinstance(values, list)
                       for value in values})
    recipe = {"frontmatter_id": str(front.get("frontmatter_id") or front.get("id") or ""),
              "title": title_of(front, body),
              "slash_command": str(front.get("slash_command") or ""),
              "summary": str(portable.get("summary") or front.get("summary") or "").strip(),
              "description": str(front.get("description") or "").strip(),
              "tags": list(tags or []),
              "parameters": list(portable["parameters"]) if isinstance(portable.get("parameters"), list) else None,
              "requirements": (list(portable["requirements"]) if isinstance(portable.get("requirements"), list)
                               else None),
              "steps": steps}
    for key in ("pattern", "eval_case_id"):
        if portable.get(key):
            recipe[key] = str(portable[key])
    return recipe


def _blank(value) -> bool:
    return value is None or not str(value).strip()


def problems(recipe: dict) -> list[str]:
    """Every reason single-metadata's catalog publish refuses the recipe (its `RecipeCatalogChecks`); [] = publishable."""
    out = []
    rid = recipe.get("frontmatter_id")
    if _blank(rid):
        out.append("frontmatter_id is required")
    if _blank(recipe.get("title")):
        out.append("title is required")
    summary = recipe.get("summary")
    if _blank(summary):
        out.append("summary is required")
    elif len(summary) > MAX_SUMMARY_CHARS:
        out.append(f"summary is at most {MAX_SUMMARY_CHARS} characters")
    if recipe.get("description") and len(recipe["description"]) > MAX_DESCRIPTION_CHARS:
        out.append(f"description is at most {MAX_DESCRIPTION_CHARS} characters")
    if not _blank(rid) and recipe.get("slash_command") != f"/{rid}":
        out.append(f"slash_command must be /{rid} (the recipe's own)")
    names: set = set()
    channels: set = set()
    parameters = recipe.get("parameters")
    if parameters is None:
        out.append("parameters is required (an empty list when the recipe has none)")
    else:
        for parameter in parameters:
            name = parameter.get("name") if isinstance(parameter, dict) else None
            if not isinstance(name, str) or not NAME.match(name):
                out.append(f"parameter name {name} is not a plain name")
                continue
            if name in names:
                out.append(f"parameter {name} is declared twice")
            names.add(name)
            kind = parameter.get("type")
            if kind not in PARAMETER_TYPES:
                out.append(f"parameter {name} type must be one of {sorted(PARAMETER_TYPES)}")
            elif kind == "enum" and not parameter.get("options"):
                out.append(f"parameter {name} is an enum without options")
    requirements = recipe.get("requirements")
    if requirements is None:
        out.append("requirements is required (typed: slot, kind, meaning)")
    else:
        for requirement in requirements:
            slot = requirement.get("slot") if isinstance(requirement, dict) else None
            if not isinstance(slot, str) or not NAME.match(slot):
                out.append(f"requirement slot {slot} is not a plain name")
                continue
            if slot in names:
                out.append(f"slot {slot} is declared twice (or as a parameter too)")
            names.add(slot)
            kind = requirement.get("kind")
            if kind not in REQUIREMENT_KINDS:
                out.append(f"slot {slot} kind must be one of {sorted(REQUIREMENT_KINDS)}")
            if _blank(requirement.get("meaning")):
                out.append(f"slot {slot} needs a meaning")
            if kind in CHANNEL_KINDS:
                if _blank(requirement.get("channel")):
                    out.append(f"slot {slot} is an {kind} without a channel")
                else:
                    channels.add(str(requirement["channel"]).lower())
    steps = recipe.get("steps") or []
    if not steps:
        out.append("steps are required")
    step_ids = {step.get("id") for step in steps if step.get("id")}
    for index, step in enumerate(steps):
        label = f"step {index + 1}"
        text = str(step.get("instruction") or "")
        if _blank(text):
            out.append(f"{label} needs an instruction")
        if _blank(step.get("builds")):
            out.append(f"{label} needs builds (what it produces)")
        if len(text) > MAX_STEP_CHARS:
            out.append(f"{label} is longer than {MAX_STEP_CHARS} characters")
        for found in REFERENCE.finditer(text):
            if found.group(1) not in names:
                out.append(f"{label} names {{{found.group(1)}}}, which is no slot or parameter")
        lower = text.lower()
        for word, channel in INTEGRATION_WORDS.items():
            if re.search(r"\b" + re.escape(word) + r"\b", lower) and channel not in channels:
                out.append(f"{label} uses {word}, which no integration requirement declares (channel {channel})")
    for step in steps:
        for used in step.get("uses") or []:
            if used not in names and used not in step_ids:
                out.append(f"step {step.get('id')} uses {used}, which is no slot, parameter or step")
    text = "\n".join([str(recipe.get("title")), str(recipe.get("summary")), str(recipe.get("description"))]
                     + [f"{step.get('title')}\n{step.get('instruction')}" for step in steps])
    if BRACKET_PLACEHOLDER.search(text) or LIQUID_PLACEHOLDER.search(text):
        out.append("the text holds a placeholder ([Brand] or {{ }}); name the slot or parameter instead")
    for pattern in INJECTION:
        if pattern.search(text):
            out.append(f"the injection scan refuses the text ({pattern.pattern})")
    lower = text.lower()
    for vendor in OTHER_VENDORS:
        if re.search(r"\b" + re.escape(vendor) + r"\b", lower):
            out.append(f"the text names another vendor ({vendor})")
    return out


def warnings(recipe: dict) -> list[str]:
    """Reported, never refused: a title / description sharing no word (longer than 3 letters) with the steps."""
    def words(text):
        return {word for word in re.split(r"[^a-z0-9]+", str(text or "").lower()) if len(word) > 3}
    step_words = set()
    for step in recipe.get("steps") or []:
        step_words |= words(step.get("title")) | words(step.get("instruction"))
    out = []
    for field in ("title", "description"):
        own = words(recipe.get(field))
        if own and not own & step_words:
            out.append(f"{field} shares no word with the steps; check that it describes them")
    return out


def recipe_paths(root: str = ".") -> list[str]:
    return sorted(glob.glob(os.path.join(root, "recipes", "*", "*", "recipe.md")))


def catalog(root: str = ".") -> list[tuple[str, dict]]:
    """Every published recipe of the repository as `(path, portable recipe)`; drafts (`visibility: draft`) left out."""
    out = []
    for path in recipe_paths(root):
        front, body = read(path)
        if str(front.get("visibility") or "").lower() == "draft":
            continue
        out.append((path, build(front, body)))
    return out
