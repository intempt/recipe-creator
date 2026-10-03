import pathlib
import re

import yaml

ENGINE_REF = "intempt/llm-wrapper@16c2a7a2 src/blu_chat/sevices/recipes/md_import.py ALLOWED_ENTITIES"

BUILDABLE_ENTITIES = {
    "email_html": "a designed marketing email (HTML)",
    "email_plain": "a plain-text email",
    "image": "an image",
    "sms": "an SMS text message",
    "push": "a push notification",
    "slack": "a Slack message",
    "json": "a JSON content asset",
    "avatar": "a brand avatar",
    "pose": "a brand pose",
    "scene": "a brand scene",
    "design_system": "a brand design system",
    "segment": "a segment of users or accounts",
    "event": "an event definition",
    "attribute": "an attribute on users or accounts",
}

COMING_SOON_ENTITIES = {
    "dashboard": "a dashboard",
    "report": "an insights, funnel, retention or paths report",
    "journey": "a journey (turned off in the engine on 2026-09-21)",
    "workflow": "a workflow and its steps",
    "experiment": "an A/B experiment",
    "personalization": "a website personalization",
    "recommendation": "a product recommendation",
    "video": "a video",
    "page": "a landing page",
    "content": "a generic content asset",
    "snippet": "a reusable content snippet",
    "agent": "a custom agent",
    "meeting": "a meeting action",
    "meeting_type": "a meeting type",
    "account": "an account update",
    "task": "a task",
}

COMMAND_TO_BUILDS = {
    "create_segment": "segment",
    "create_ai_attribute": "attribute",
    "create_attribute": "attribute",
    "generate_image": "image",
    "create_email_content": "email_html",
    "create_sms_content": "sms",
    "create_slack_content": "slack",
    "create_dashboard": "dashboard",
    "create_report": "report",
    "build_insights_report": "report",
    "build_funnel_report": "report",
    "build_retention_report": "report",
    "build_paths_report": "report",
    "create_journey": "journey",
    "create_workflow": "workflow",
    "publish_workflow": "workflow",
    "create_experiment": "experiment",
    "create_personalization": "personalization",
    "create_recommendation": "recommendation",
    "generate_video": "video",
    "create_page_content": "page",
    "create_content": "content",
    "create_snippet": "snippet",
    "create_agent": "agent",
    "update_account": "account",
    "create_task": "task",
    "analyze_talk_listen_ratio": "meeting",
}


def builds_for_command(command):
    if command in COMMAND_TO_BUILDS:
        return COMMAND_TO_BUILDS[command]
    if command.startswith("configure_") and command.endswith("_step"):
        return "workflow"
    if "meeting_type" in command:
        return "meeting_type"
    if "meeting" in command or command in ("get_booking_link", "book_meeting", "configure_notetaker_autojoin"):
        return "meeting"
    return command.split("_", 1)[-1]


ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SLASH_PATTERN = re.compile(r"^/[a-z0-9]+(-[a-z0-9]+)*$")
STEP_ID_PATTERN = re.compile(r"^s[1-9][0-9]*$")
OWNER_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BRACES = re.compile(r"\{\{|\}\}")

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)

REQUIRED_TOP = ("id", "title", "slash_command", "group", "owner", "summary", "steps")
REQUIRED_STEP = ("id", "title", "summary", "builds", "description")

SUMMARY_MAX = 200
STEP_TITLE_MAX = 60


class RecipeError(Exception):
    pass


def recipe_paths(recipes_dir):
    return sorted(pathlib.Path(recipes_dir).glob("*/*/recipe.md"))


def read(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise RecipeError(f"{path}: no YAML frontmatter")
    try:
        front = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise RecipeError(f"{path}: {exc}") from exc
    return front, match.group(2)


def availability(front):
    waiting = sorted({s.get("builds") for s in front.get("steps") or []} - set(BUILDABLE_ENTITIES) - {None})
    return ("install_now" if not waiting else "coming_soon"), waiting


def validate(path, front):
    problems = []
    p = pathlib.Path(path)
    for key in REQUIRED_TOP:
        if not front.get(key):
            problems.append(f"{key} is required")
    rid = front.get("id") or ""
    if rid and not ID_PATTERN.match(rid):
        problems.append(f"id {rid!r} must be kebab-case")
    if rid and p.parent.name != rid:
        problems.append(f"folder {p.parent.name!r} must equal id {rid!r}")
    owner = front.get("owner") or ""
    if owner and p.parent.parent.name != owner:
        problems.append(f"owner {owner!r} must equal the partner folder {p.parent.parent.name!r}")
    if owner and not OWNER_PATTERN.match(owner):
        problems.append(f"owner {owner!r} must be kebab-case")
    slash = front.get("slash_command") or ""
    if slash and not SLASH_PATTERN.match(slash):
        problems.append(f"slash_command {slash!r} must match /kebab-case (validate.py:51)")
    summary = (front.get("summary") or "").strip()
    if len(summary) > SUMMARY_MAX:
        problems.append(f"summary is {len(summary)} chars, max {SUMMARY_MAX}")

    steps = front.get("steps") or []
    seen = []
    for i, step in enumerate(steps, start=1):
        where = f"step {i}"
        if not isinstance(step, dict):
            problems.append(f"{where} is not a mapping")
            continue
        for key in REQUIRED_STEP:
            if not str(step.get(key) or "").strip():
                problems.append(f"{where}: {key} is required")
        sid = step.get("id")
        if sid != f"s{i}":
            problems.append(f"{where}: id must be s{i}, steps are numbered in order (md_import.py RULES)")
        if len(str(step.get("title") or "")) > STEP_TITLE_MAX:
            problems.append(f"{where}: title over {STEP_TITLE_MAX} chars")
        builds = step.get("builds")
        if builds and builds not in BUILDABLE_ENTITIES and builds not in COMING_SOON_ENTITIES:
            problems.append(f"{where}: builds {builds!r} is not a known entity, see references/entities.md")
        desc = str(step.get("description") or "")
        if BRACES.search(desc):
            problems.append(f"{where}: description has curly braces; name the earlier step by its title instead (md_import.py RULES)")
        for dep in step.get("dependsOn") or []:
            if dep not in seen:
                problems.append(f"{where}: dependsOn {dep!r} is not an earlier step (step_check.py needs_earlier_step)")
        for unknown in set(step) - {"id", "title", "summary", "builds", "description", "dependsOn"}:
            problems.append(f"{where}: unknown field {unknown!r}; command, entity, kind and arguments come from the step check, not the file")
        seen.append(sid)

    keys = set()
    for o in front.get("outputs") or []:
        key = o.get("key")
        if not key:
            problems.append("an output has no key")
        elif key in keys:
            problems.append(f"output key {key!r} is declared twice")
        keys.add(key)
        if o.get("producedByStep") not in seen:
            problems.append(f"output {key!r}: producedByStep must name a step id (validate.py:260)")
    return problems


BODY_MARKER = "<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->"


def render_body(front):
    status, waiting = availability(front)
    lines = ["", BODY_MARKER, "", f"# {front.get('title') or front.get('id')}", "", " ".join(str(front.get("summary") or "").split()), "", "## Steps", ""]
    for n, step in enumerate(front.get("steps") or [], start=1):
        lines += [f"{n}. **{step.get('title')}** (builds {step.get('builds')})", "", "   " + " ".join(str(step.get("summary") or "").split()), ""]
    outputs = front.get("outputs") or []
    if outputs:
        lines += ["## What you end up with", ""]
        for o in outputs:
            lines.append(f"- **{o.get('key')}** ({o.get('type')}): " + " ".join(str(o.get("description") or "").split()))
        lines.append("")
    lines += ["## Availability", ""]
    if status == "install_now":
        lines.append("Install now: every step builds something the engine supports today.")
    else:
        lines.append("Coming soon: waiting on the engine to build " + ", ".join(waiting) + ".")
    return "\n".join(lines).rstrip() + "\n"
