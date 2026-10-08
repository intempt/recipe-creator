#!/usr/bin/env python3
"""
Migrate contract-format (v2) recipes to the git-validate format: each recipe.md keeps
ONLY what llm-wrapper's git_validate reads to build the global recipe record
(recipe.json). Deterministic and re-runnable: a file already in the target format is
left byte-for-byte alone, so a second run writes nothing.

Reference: recipes/intempt-internal-use-only/recent-page-viewers-segment/recipe.md,
written by scripts/git_validate_writeback.py (same YAML dump settings are used here).

What git_validate reads today (llm-wrapper src/blu_chat/sevices/recipes/git_validate.py):
  frontmatter  frontmatter_id (else id), author{name,last_name + optional email,
               company, byline, linkedin_url, avatar_url}, classification.industry,
               description. NOTHING else.
  body         everything after the frontmatter; the model reads it into
               {title, slash_command, steps} (md_import INTRO/STEP_SHAPE/RULES), then
               every step is checked on its own (step_check) and refused as `vague`
               when it does not say what it builds.

TARGET FRONTMATTER, in this order (NO frontmatter_id, NO id, NO slash_command — Beso
ruling 2026-10-08: the validate flow makes the key. recipe-git-validate.yml job 1 sends
LM a temporary key (recipe_draft.temp_key/with_key) and job 3, git_validate_writeback.py,
sets key = LM's slash_command without "/", deduped -2, -3...):
  description      <- summary, whitespace-collapsed to one line. `summary` is the
                      customer prose; the old `description` was an internal one-liner
                      (e.g. "Eyewear, jewelry, watches on model.") and is dropped.
                      git_validate keeps a frontmatter description verbatim.
  author           <- curator handle, mapped from website/app/recipes/curators.ts,
                      exactly (Beso ruling 2026-10-08):
                        first_name   required  (replaces `name`)
                        last_name    required
                        job_title    optional  (replaces `byline`; byline is NOT emitted)
                        avatar       optional  (replaces `avatar_url`; only where
                                               curators.ts has a photo)
                        company      Intempt
                        org_name     <owner folder> (= intempt)
                      LM's git_validate is being changed in parallel to accept these keys.
                      An unknown curator is refused and NOTHING is written. A file this
                      script already migrated with the earlier name/byline/avatar_url
                      spelling is re-emitted in this shape (body untouched).
  classification   <- classification.industry only, when present and non-empty.

DROPPED: id, slash_command and title (the last two move to the body), group, owner, curator, summary
(renamed), the old description, version, every other classification key, touches,
steps (moved to the body), outputs, prerequisites, inputs, does_not_claim, and the
generated body (rebuild_bodies.py output).

Not folded into the body, on evidence (see MIGRATION.md):
  inputs         every one of the 24 recipes' inputs is already written into its step
                 ("attached to this run", "chosen for this run", defaults spelled out).
  prerequisites  project facts (events / integrations that must exist), not step
                 content; adding a section risks the model turning it into a step
                 (md_import RULES: "Never drop a part of the file ... it is still a step").
  dependsOn      every dependency's title is already named in the step description,
                 which is what md_import RULES ask for.

TARGET BODY:
  (blank line)
  # <title>
  (blank line)
  Slash command: /<slash_command>   the v2 slash_command, exactly as it was
  (blank line)
  ## Step N: <step title>          one per step, in order
  (blank line)
  <the FULL steps[].description, trailing whitespace stripped>
  (blank line between steps; file ends with one newline)

Minimal rewrite: when a step description never names what it builds (no word for its
`builds` entity, see SYNONYMS), one line "This step builds <entity>." is put first.
Nothing else in a description is changed.

Usage (from the recipe-creator repo root):
  python3 scripts/migrate_to_git_format.py recipes/intempt            # all folders
  python3 scripts/migrate_to_git_format.py recipes/intempt/<id> ...   # some folders
Exit 0 done, 1 refused (nothing written).
"""
from __future__ import annotations

import os
import re
import sys

import yaml

CURATORS = {  # website/app/recipes/curators.ts (CURATORS), 2026-10-08
    "aman": ("Aman", "Tiwari", "Product Manager", None),
    "trishik": ("Trishik", "Shrestha", "Growth Marketer",
                "https://cdn.intempt.com/assets/author-profile-pics/trishik.png"),
    "harish": ("Harish", "Kumar", "Growth Marketer",
               "https://cdn.intempt.com/assets/author-profile-pics/harish.jpg"),
    "aurobind": ("Aurobind", "Venu", "Creative Director", None),
    "somya": ("Somya", "Nayak", "Marketing Lead",
              "https://cdn.intempt.com/assets/author-profile-pics/somya.png"),
    "rana": ("V", "Ranadheer", "Design Engineer", None),
    "sid": ("Sid", "Chaudhary", "Founder & CEO",
            "https://cdn.intempt.com/assets/author-profile-pics/sid.png"),
}
COMPANY = "Intempt"

# builds -> (words that count as naming it, phrase used when none appears)
SYNONYMS = {
    "workflow": (("workflow",), "a workflow"),
    "segment": (("segment", "cohort"), "a segment"),
    "dashboard": (("dashboard", "dash board"), "a dashboard"),
    "report": (("report",), "a report"),
    "attribute": (("attribute",), "an attribute"),
    "email_html": (("email",), "a designed marketing email (HTML)"),
    "email_plain": (("email",), "a plain-text email"),
    "journey": (("journey",), "a journey"),
    "experiment": (("experiment", "a/b"), "an experiment"),
    "image": (("image", "photo", "packshot", "picture"), "an image"),
    "personalization": (("personaliz", "personalis"), "a personalization"),
    "video": (("video",), "a video"),
    "recommendation": (("recommend",), "a recommendation"),
    "meeting_type": (("meeting",), "a meeting type"),
    "meeting": (("meeting",), "a meeting"),
    "page": (("page",), "a page"),
    "slack": (("slack",), "a Slack message"),
    "sms": (("sms",), "an SMS text message"),
    "push": (("push",), "a push notification"),
    "agent": (("agent",), "an agent"),
    "account": (("account",), "an account"),
    "task": (("task",), "a task"),
    "content": None,  # generic: the description names the concrete channel itself
}

OLD_FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
TARGET_KEYS = {"description", "author", "classification"}
# keys an earlier run of this script wrote and the 2026-10-08 ruling removed
_EARLIER_KEYS = {"frontmatter_id", "slash_command"}
SLASH_LINE = re.compile(r"^Slash command: /[a-z0-9]+(-[a-z0-9]+)*$", re.M)


class Refused(Exception):
    pass


def dump_front(front: dict) -> str:
    # same settings as git_validate_writeback._md
    return yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000)


def make_author(first, last, title, avatar, owner) -> dict:
    """The author block, Beso ruling 2026-10-08: first_name, last_name, job_title,
    avatar (only where curators.ts has a photo), company, org_name — in this order."""
    author = {"first_name": first, "last_name": last}
    if title:
        author["job_title"] = title
    if avatar:
        author["avatar"] = avatar
    author.update({"company": COMPANY, "org_name": owner})
    return author


# earlier key spellings of this script's own output -> the ruled ones
_RENAMED = {"name": "first_name", "byline": "job_title", "avatar_url": "avatar"}
_AUTHOR_KEYS = {"first_name", "last_name", "job_title", "avatar", "company", "org_name"}


def renormalize(front: dict, body: str) -> str:
    """An already-migrated file: re-emit its frontmatter in the ruled shape (renaming the
    earlier author keys), body untouched. A file already in the ruled shape comes back
    byte-identical, which is what makes a second run a no-op."""
    raw = front.get("author")
    if not isinstance(raw, dict):
        raise Refused("migrated file has no author mapping")
    author = {_RENAMED.get(k, k): v for k, v in raw.items()}
    if set(author) - _AUTHOR_KEYS:
        raise Refused(f"unknown author keys {sorted(set(author) - _AUTHOR_KEYS)}")
    author = make_author(author.get("first_name"), author.get("last_name"),
                         author.get("job_title"), author.get("avatar"), author.get("org_name"))
    if not SLASH_LINE.search(body):
        raise Refused("migrated file has no 'Slash command: /...' line in its body")
    new = {k: front[k] for k in ("description",) if k in front}
    new["author"] = author
    if "classification" in front:
        new["classification"] = front["classification"]
    return "---\n" + dump_front(new) + "---\n" + body


def lead_line(builds: str, description: str):
    if builds not in SYNONYMS:
        raise Refused(f"unknown builds {builds!r}")
    spec = SYNONYMS[builds]
    if spec is None:
        return None
    words, phrase = spec
    low = description.lower()
    if any(w in low for w in words):
        return None
    return f"This step builds {phrase}."


def convert(folder: str, text: str) -> tuple[str, list[str]]:
    """(new recipe.md text, notes). Raises Refused."""
    m = OLD_FM.match(text)
    if not m:
        raise Refused("no frontmatter")
    front = yaml.safe_load(m.group(1))
    if not isinstance(front, dict):
        raise Refused("frontmatter is not a mapping")
    if "id" not in front:
        if "author" in front and set(front) <= TARGET_KEYS | _EARLIER_KEYS:
            return renormalize(front, m.group(2)), ["already migrated"]
        raise Refused("neither a v2 contract recipe nor a migrated one")
    key, owner = str(front["id"]), os.path.basename(os.path.dirname(os.path.abspath(folder)))
    if key != os.path.basename(os.path.abspath(folder)):
        raise Refused(f"id {key!r} does not match its folder")
    curator = front.get("curator")
    if curator not in CURATORS:
        raise Refused(f"unknown curator {curator!r}")
    name, last, byline, avatar = CURATORS[curator]
    author = make_author(name, last, byline, avatar, owner)

    summary = " ".join(str(front.get("summary") or "").split())
    if not summary:
        raise Refused("no summary to use as description")
    title = " ".join(str(front.get("title") or "").split())
    slash = str(front.get("slash_command") or "")
    steps = front.get("steps") or []
    if not title or not slash or not steps:
        raise Refused("title, slash_command or steps missing")

    new = {"description": summary, "author": author}
    industry = (front.get("classification") or {}).get("industry")
    if industry not in (None, "", []):
        new["classification"] = {"industry": industry}

    notes, parts = [], [f"# {title}", f"Slash command: {slash}"]
    for n, step in enumerate(steps, 1):
        desc = "\n".join(line.rstrip() for line in str(step.get("description") or "").strip().splitlines())
        stitle = " ".join(str(step.get("title") or "").split())
        if not desc or not stitle:
            raise Refused(f"step {n} has no title or description")
        lead = lead_line(str(step.get("builds") or ""), desc)
        if lead:
            desc = lead + "\n" + desc
            notes.append(f"s{n}: lead line added ({step.get('builds')})")
        parts.append(f"## Step {n}: {stitle}\n\n{desc}")
    body = "\n" + "\n\n".join(parts) + "\n"
    return "---\n" + dump_front(new) + "---\n" + body, notes


def folders_of(args: list[str]) -> list[str]:
    out = []
    for a in args:
        a = a.rstrip("/")
        if os.path.isfile(os.path.join(a, "recipe.md")):
            out.append(a)
        else:
            out += sorted(os.path.join(a, d) for d in os.listdir(a)
                          if os.path.isfile(os.path.join(a, d, "recipe.md")))
    return out


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(__doc__.strip().splitlines()[-4], file=sys.stderr)
        return 2
    plans, problems = [], []
    for folder in folders_of(args):
        path = os.path.join(folder, "recipe.md")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        try:
            new, notes = convert(folder, text)
        except Refused as e:
            problems.append(f"{path}: {e}")
            continue
        plans.append((path, text, new, notes))
    if problems:
        for p in problems:
            print(f"REFUSED {p}", file=sys.stderr)
        print("Nothing written.", file=sys.stderr)
        return 1
    written = 0
    for path, old, new, notes in plans:
        if new != old:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(new)
            written += 1
        for n in notes:
            if n != "already migrated":
                print(f"NOTE    {path}: {n}")
    print(f"{len(plans)} recipe(s): {written} written, {len(plans) - written} unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
