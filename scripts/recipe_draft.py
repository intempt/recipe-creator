"""
The draft/ flow (R-RG4-6): an author's pull request adds or changes only a free-prose
`draft/<any-name>.md`; CI validates it and writes `recipes/<owner>/<frontmatter_id>/recipe.md`
+ `recipe.json` in a bot commit that also deletes the draft. What every step of that
flow shares lives here, so job 1, job 3, the PR gate and the checks read one definition.

  owner           the draft's `author.org_name`, else `intempt` (D1)
  frontmatter_id  a new recipe: LM's slash_command without `/`; on a clash with ANY
                  recipe in the repo (all owners) `-2`, `-3`… and the slash_command
                  takes the same suffix (D2). An edit: the draft carries
                  `frontmatter_id: <existing key>`, which keeps key, folder and
                  slash_command (D3).
"""
from __future__ import annotations

import glob
import json
import os
import re

import yaml

DRAFT_DIR = "draft"
DRAFT_README = "draft/README.md"
DEFAULT_OWNER = "intempt"
# The write-back job commits as this identity; the PR gate lets only it touch recipes/.
BOT_NAME = "github-actions[bot]"
BOT_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"

# The front matter as llm-wrapper's git_validate._FRONTMATTER finds it: an optional BOM
# and blank lines may come before the opening `---`.
FRONT = re.compile(r"\A﻿?(?:[ \t]*\r?\n)*---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class DraftError(Exception):
    pass


def is_draft(path: str) -> bool:
    """A draft is any .md under draft/ except its README."""
    return path.startswith(DRAFT_DIR + "/") and path.endswith(".md") and path != DRAFT_README


def split(text: str) -> tuple[dict, str]:
    """(front matter dict, body after it). No front matter → ({}, the whole text).
    A front matter that is not a mapping is an error: LM would not read it either."""
    m = FRONT.match(text or "")
    if not m:
        return {}, text or ""
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise DraftError(f"front matter is not valid YAML ({e.__class__.__name__})") from e
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        raise DraftError("front matter is not a mapping")
    return meta, text[m.end():]


def slugify(value: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", str(value or "").lower())).strip("-")


def temp_key(path: str) -> str:
    """The key job 1 sends LM for a new draft, which has none yet (LM 422s
    `frontmatter_id_missing` without one, and LM is not changed — R-RG4-10).
    Unique per draft path; never written to recipes/."""
    rel = path[len(DRAFT_DIR) + 1:] if path.startswith(DRAFT_DIR + "/") else path
    return "draft-" + (slugify(rel[:-3] if rel.endswith(".md") else rel) or "recipe")


def with_key(text: str, key: str) -> str:
    """The draft as job 1 sends it: unchanged when it already names a frontmatter_id,
    else with `frontmatter_id: <key>` as the front matter's first line (a front matter
    is added when there is none, so LM reports the real problem — a missing author)."""
    meta, _ = split(text)
    if str(meta.get("frontmatter_id") or "").strip():
        return text
    line = "frontmatter_id: " + json.dumps(key)
    m = FRONT.match(text or "")
    if not m:
        return f"---\n{line}\n---\n" + (text or "")
    at = m.start(1)
    newline = "\r\n" if "\r\n" in text[:at] else "\n"
    return text[:at] + line + newline + text[at:]


def owner_of(meta: dict) -> str:
    """D1: `author.org_name`, else `intempt`. It names a folder, so it must be a slug."""
    author = meta.get("author")
    raw = author.get("org_name") if isinstance(author, dict) else None
    owner = str(raw).strip() if raw is not None else ""
    if not owner:
        return DEFAULT_OWNER
    if not SLUG.match(owner):
        raise DraftError(f"author.org_name {owner!r} is not a folder name "
                         "(lowercase letters, digits and single hyphens)")
    return owner


def taken(root: str = ".") -> dict[str, str]:
    """Every key in use across recipes/*/*/ (all owners) → the folder that holds it:
    folder names, each recipe.md's frontmatter_id / id, each recipe.json's
    frontmatter_id, and each contract slash_command without `/` (a new key must
    not collide with any of them, so its slash_command cannot either)."""
    keys: dict[str, str] = {}
    for folder in sorted(glob.glob(os.path.join(root, "recipes", "*", "*", ""))):
        folder = folder.rstrip("/\\")
        rel = os.path.relpath(folder, root)
        keys.setdefault(os.path.basename(folder), rel)
        md = os.path.join(folder, "recipe.md")
        if os.path.exists(md):
            try:
                with open(md, encoding="utf-8") as fh:
                    meta, _ = split(fh.read())
            except DraftError:
                meta = {}
            for k in ("frontmatter_id", "id"):
                if str(meta.get(k) or "").strip():
                    keys.setdefault(str(meta[k]).strip(), rel)
            slash = str(meta.get("slash_command") or "").strip().lstrip("/")
            if slash:
                keys.setdefault(slash, rel)
        js = os.path.join(folder, "recipe.json")
        if os.path.exists(js):
            try:
                with open(js, encoding="utf-8") as fh:
                    record = json.load(fh)
            except ValueError:
                record = {}
            if isinstance(record, dict) and str(record.get("frontmatter_id") or "").strip():
                keys.setdefault(str(record["frontmatter_id"]).strip(), rel)
    return keys


def new_key(base: str, used) -> str:
    """D2: `base`, else `base-2`, `base-3`… — the first one not in `used`."""
    if base not in used:
        return base
    n = 2
    while f"{base}-{n}" in used:
        n += 1
    return f"{base}-{n}"


def find_recipe(key: str, root: str = ".") -> str | None:
    """The recipes/<owner>/<key>/ folder for an edit, or None. Two owners holding the
    same key is a broken repo (R-RG4-8), reported rather than guessed."""
    hits = sorted(p.rstrip("/\\") for p in glob.glob(os.path.join(root, "recipes", "*", key, "")))
    if len(hits) > 1:
        raise DraftError(f"frontmatter_id {key!r} is held by {len(hits)} folders: "
                         + ", ".join(os.path.relpath(h, root) for h in hits))
    return os.path.relpath(hits[0], root) if hits else None
