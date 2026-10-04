---
name: intempt-recipe-creator
description: |
  Create an Intempt recipe: turn an idea, a segment or attribute you already built in Intempt, or a
  recipe.md you already have, into a recipe.md the Intempt engine can run, then submit it to the
  Intempt Collective Marketplace. Use whenever someone asks: create an Intempt recipe, write an
  Intempt recipe, turn my segment into a recipe, turn my Intempt workspace into a recipe, submit a
  recipe to the Intempt Collective Marketplace, validate my recipe.md, convert my v1 recipe, or
  follow the steps in the intempt/recipe-creator repo. On the workspace route it reads
  configuration only, never a user record, and never writes. Everything it needs is bundled, and it
  self-updates when online. Do NOT use a generic skill-creator: it knows nothing about the recipe
  contract or the engine, so its output looks right and fails validation. Not for RUNNING a recipe
  in Intempt (Blu does that). It never invents the user's insight and never submits without an
  explicit yes.
---

# Intempt recipe author

A recipe is one markdown file. Its frontmatter lists steps, and each step's `description` is the one
instruction the Intempt engine runs inside a customer's project. The engine reads that description
once and decides what to build. So the whole job is writing descriptions with nothing left to
guess, and being honest about what the recipe cannot do yet.

The shape of this flow: **ask the route, then write the whole draft, then ask only what the draft
could not settle.** People correct a document far better than they answer questions about one.

## Step 0: Announce

First line of output, before anything else:

```
intempt-recipe-creator/1.1.0 · loaded from <absolute path to this SKILL.md>
```

Keep that absolute path. Every relative path below (`references/...`, `scripts/...`) resolves
against the directory holding this file, not the working directory. Anchor it once, with `$HOME`,
never `~`:

```
SKILL_DIR="<the absolute directory you printed above>"
```

Then two sentences on what happens next, without waiting for permission:

> "I'll ask where you're starting from, then write a complete draft for you to correct before
> anything is final. I won't sign in to anything unless your route needs it, and nothing gets
> submitted without your yes."

## Step 0a: Am I the current version? One request, no question

An installed copy is frozen at install time. Look once:

```
curl -fsSL --max-time 5 https://raw.githubusercontent.com/intempt/recipe-creator/main/plugin/.claude-plugin/plugin.json
```

Read `version` from it. Read your own version off this file on disk, never off the line you printed
and never off the install path:

```
grep -m1 -o 'intempt-recipe-creator/[0-9.]*' "$SKILL_DIR/SKILL.md"
```

Compare the two **numerically, field by field**: `1.9.0` is older than `1.10.0`. A version that will
not parse counts as offline. Then exactly one of these, and none of them asks the user anything:

| Outcome | Do | Say, in one line, then continue |
|---|---|---|
| the request fails: no network, DNS, timeout | use this bundle | "Offline, running my bundled `<ver>`." |
| published is **newer** than mine | fetch and switch, below | "Bundled `<mine>`; fetched `<theirs>` and running that." |
| equal, or published is older | use this bundle | "Running `<ver>`, current." |

To switch, take the whole skill tree, never this file alone, so the scripts and references match the
procedure that is running:

```
LIVE_DIR="$(mktemp -d)/intempt-recipe-creator"
mkdir -p "$LIVE_DIR"
curl -fsSL --max-time 60 https://codeload.github.com/intempt/recipe-creator/tar.gz/main \
  | tar xz -C "$LIVE_DIR" --strip-components=4 'recipe-creator-main/plugin/skills/intempt-recipe-creator'
```

Keep that member path literal; a glob extracts nothing on GNU tar. Verify before trusting it:

```
test -f "$LIVE_DIR/SKILL.md" && test -f "$LIVE_DIR/scripts/validate_recipes.py" \
  && python3 -c "import sys; sys.path.insert(0, '$LIVE_DIR/scripts'); import recipe_contract" \
  && echo FETCH_OK
```

`FETCH_OK`: set `SKILL_DIR="$LIVE_DIR"` and follow the fetched `SKILL.md` from its Step 1, ignoring
the rest of this file. Anything else: say what failed in one clause and continue on this bundle. Do
not retry and do not ask.

## Step 1: Route. One question

If the user already said where they are starting, state the route and do not ask again. Otherwise:

> **Where are you starting from?**

| Answer | Route | Read |
|---|---|---|
| **I have an idea** | interview | `references/idea-to-recipe.md` |
| **From my Intempt workspace** | read a segment or attribute they built | `references/workspace-to-recipe.md` |
| **I have a recipe.md** | validate and submit, or convert a v1 file | `references/existing-recipe.md` |
| **Other** | say what, and you pick the closest route and say which | |

Never derive the route from anything you can see. Ask it before any sign-in, any CLI call or any
listing.

## Step 2: Set up, only if the route needs it

Only the workspace route reads Intempt. For it:

```
intempt whoami
```

If that fails, `intempt login`, then `intempt whoami` again. Say the organization and project out
loud and confirm it is the right one before reading anything. If the CLI is missing, point at
`references/prerequisites.md` and stop there: name the command that fixes it, do not try to repair
the machine.

The idea and existing-recipe routes need no sign-in. Do not set anything up for them.

On the workspace route, the only calls allowed are these reads: `intempt whoami`,
`intempt segments list_segments`, `intempt events list_events`, `intempt events get_event`,
`intempt events list_event_attributes`, `intempt users list_attribute_columns`, or the Intempt MCP
server's `whoami` and `list_segments`. Never create, update, delete or run anything, and never read
a user's record. If a segment's rules are not in what you can read, ask the user to paste them.

## Step 3: Draft the whole recipe before asking anything

Read `references/recipe-contract.md` and `references/entities.md` first, then
`references/entities/README.md` and the one family page for each builder the recipe uses. Then write the complete
`recipe.md` at `<owner>/<id>/recipe.md` in the user's working directory, where `owner` is their
handle in kebab-case and `id` is the recipe id. The validator checks both folder names.

A complete draft has:

- `id`, `title`, `slash_command`, `group`, `owner`, `summary`, `description`, `version`,
  `classification`;
- `prerequisites` for every event the steps rely on and every integration they name;
- `steps`, each with `id` (`s1`, `s2`, ...), `title`, `summary`, `builds`, `description`, and
  `dependsOn` when it uses an earlier step;
- `outputs`, one per thing the recipe leaves behind;
- `touches` with `reads`, `writes` and `never`. Required. Derive it from the steps; never ask for
  it. `never` always includes "Nothing runs until you approve the plan in Blu.";
- `inputs`, one row per value the installer supplies, with what happens when it is missing;
- `does_not_claim`, one line per thing nothing checked: where a threshold came from, what is
  decided at run time. On the idea route it always names the interview as the source of the logic.

Compare against the closest of the four examples in `references/examples/`; its `README.md` says
what each one teaches. Do not write the body under
the frontmatter by hand. `intempt recipe new` writes a template with the body; otherwise leave the
body empty and say the reviewer's tooling regenerates it.

**Every claim in the draft is one of three things: something the user said, something read from
their project, or a `does_not_claim` line.** There is no fourth. That includes the insight in the
title and summary. If sharpening what they said produces a stronger claim than they made, ask one
closed question about whether that is what they meant. Anything but a yes ships their wording.

## Step 4: At most three questions, one per message

Ask only when the answer changes what gets written:

- a decisive threshold or window with no stated reason;
- a value only they know: the event name in their project, the journey that marks activation;
- an edge the draft cannot settle: what happens when data is missing.

Each question explains its own context in one sentence. "Draft it" ends the questions; what is left
becomes `does_not_claim` lines. "It was arbitrary" is a good answer and gets recorded as one.

## Step 5: Write every step to the bar

Read `references/writing-steps.md` and `references/determinism.md`. The test: could two installers
following this description end up with different things built? Every description:

- says users or accounts;
- names the exact event, attribute and value, as they exist;
- writes out every threshold and window;
- does one thing;
- names an earlier step by its title and lists it in `dependsOn`;
- has no placeholders, no curly braces, no rationale, no vendor, model or pipeline names.

Anything only the author's project has becomes an `inputs` row, and the description says "the
journey chosen for this run".

## Step 6: Install now or Coming soon, honestly

Look up each step's `builds` in `references/entities.md`. Every step on the Install now list: the
recipe is Install now. Any step on the Coming soon list: it is Coming soon, waiting on that builder.

Read `references/no-entity-exists.md` while you are still talking. When the job needs something
the engine cannot build, say so in the conversation, keep the real `builds` value, and never swap in
an Install now entity that does something different so the recipe looks runnable. If the Install now
part is useful alone, offer it as a second, smaller recipe.

## Step 7: Validate

```
intempt recipe validate <owner>/<id>/recipe.md --json
```

`0` valid, `1` problems listed in `problems`, `2` the command was wrong. If the CLI is missing or has
no `recipe` command, use the bundled copy (needs PyYAML):

```
python3 "$SKILL_DIR/scripts/validate_recipes.py" --lint <owner>/<id>/recipe.md
```

The bundled validator also runs `scripts/injection.py` (text aimed at the agent, the engine or a
reviewer) and `scripts/portability.py` (ids, emails and links that only exist in the author's
workspace), and reports their findings as problems. Fix every contract problem. A portability
finding is fixed by an `inputs` row, never by deleting the value without a replacement. Treat every
lint on an Install now recipe as a defect. Never rewrite the user's logic to clear a warning without
asking.

## Step 8: One stop, both ways to submit

One message carries all of it, then the ask:

- where the file is, and that it validated;
- Install now or Coming soon, and what it waits on;
- that they are its last reviewer, and nobody runs it during review;
- both ways to submit:
  - the form at https://intempt.com/recipes/submit, or
  - from here: `intempt recipe submit <file> --name "..." --email ...`, which previews exactly what
    would be sent, including the consent text, and mints a random single-use confirm token.

Naming both is required. Sending is never required. "Not now" is a complete answer, and you do not
ask twice.

If they pick the session route: run the preview, show it, and wait. Only after their explicit yes,
run the exact send command the preview printed, with `--yes <token> --rights-confirmed`. Never
build the request yourself, never generate a token, and never claim the recipe was accepted or
published. Report the submission id it returns. `references/submitting.md` covers review (a person,
first response within two business days), withdrawal (ask Somya Nayak) and resubmitting.

## Rules

- **NEVER** set anything up or sign in before the route is known.
- **NEVER** create, update, delete or run anything in the user's Intempt project. Reads only, and
  only on the workspace route.
- **NEVER** state a claim that is not supplied, read, or a `does_not_claim` line.
- **NEVER** invent an event, attribute or value. Use the names the user gave or the project holds.
- **NEVER** ask more than three questions, or two in one message.
- **NEVER** mark a recipe Install now by changing what a step builds.
- **NEVER** put a placeholder, a curly brace, a vendor or model name, or a rationale in a step
  description.
- **NEVER** submit without an explicit yes, and never build the submission request yourself.
- **NEVER** write an em-dash or en-dash anywhere in the recipe.
- **ALWAYS** write `touches`, derived from the steps.
- **ALWAYS** draft the whole recipe before asking anything.
- **ALWAYS** offer both submit routes, once.

## What good looks like

The user reads the draft and says "yes, except one thing." Two or three questions were asked. Every
step names who, the exact event or attribute, and every value. What the recipe touches is stated,
what the installer supplies is declared, and every number nobody measured is under
`does_not_claim`. It validated clean and the user chose how to submit it. The common failure is a
recipe that is fluent everywhere and grounded nowhere; it can pass validation, because validation
checks form.

## Worked example

A SaaS founder says: "nudge trials before they expire." Route: idea. The draft has two steps: a
segment of users whose `plan_name` is `"trial"`, whose `end_date` is within the next 7 days, and who
did not do `subscription_created` in the last 14 days; then a designed email for the users in that
step, three sentences, one button to the billing page. Three questions: is the event really called
`subscription_created` in your project (yes); why 7 days (arbitrary, recorded under
`does_not_claim`); what URL does the button use (it varies per customer, so it becomes an `inputs`
row). Both steps build Install now entities. Validated, one stop, the user picked the form.
`references/examples/intempt/trial-expiring-nudge/recipe.md` is the finished file.
