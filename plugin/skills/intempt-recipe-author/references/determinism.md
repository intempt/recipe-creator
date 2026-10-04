# Writing a deterministic recipe

**The test, and it fits in one sentence: could two installers following this step description end up
with different things built?** If yes, the step describes what you meant rather than instructing
anyone.

"Find your best customers" fails that test. One reader builds a segment on lifetime value, another
on order count, a third on accounts instead of users. Each is a reasonable reading, and each is a
different recipe.

It does **not** mean the same output. The installer's project decides who is in a segment today, a
generated email is worded differently each run, and that is correct. It means **the same description
makes the engine derive the same command, the same entity and the same conditions every time.**
Determinism lives in the mechanism, never in the data.

## Why this is the whole job

A step's `description` is the one instruction the engine runs (`llm-wrapper` `orchestrator.py`
`step_text()`). When a recipe is added to a project, the step check (`step_check.py`) reads each
description once and derives everything else:

| The engine derives | From |
|---|---|
| the command it runs | the description, matched against the commands the project can run |
| the entity it builds, and its kind | the description, picked from the entities list in [references/entities.md](entities.md) |
| the arguments | every value the step needs that the description does **not** state: the gaps |
| `modelConfig` | every value the description **does** state, stored so the run never asks for it |
| `dependsOn` wiring | an earlier step the description names by its title |

So the file never carries `command`, `entity`, `kind`, `arguments`, `modelConfig`, `prompt` or
`bindsAs`. A value written there would be ignored or contradicted, and the validator refuses a step
that has one. The only lever you have is the description, which is why it has to leave nothing to
pick.

Three outcomes are possible for every value a builder needs:

| The description | The step check | The installer sees |
|---|---|---|
| states it | stores it in `modelConfig` | nothing to fill: the step runs as written |
| leaves out a value the builder requires | uses the builder's default, or leaves an argument | a value nobody chose, or a red field to fill before Run |
| points at something that does not exist | marks the step vague (R36) | a question, and a step that waits |

Only the first is deterministic. The other two are the recipe handing its author's decision to
whoever installs it.

## The seven rules

### 1. One thing per step

The engine's import rule is "one step per thing built or read. A sentence that asks for two things
is two steps" (`md_import.py` RULES). "Build a segment of trial users and email them" is a segment
step and an email step, and the email step depends on the segment. A description over 1200
characters is usually two steps; `validate_recipes.py --lint` reports it.

### 2. Users or accounts, said out loud

A segment's first decision is who it is about, and the step check stores it only when the
description says it (`step_check.py` 6c). "A segment of users" or "a segment of accounts", in the
first sentence. For accounts built from what their users do, say how it rolls up: "the users in the
account together did the session_start event 5 or more times". An attribute is on users or on
accounts; say which. The lint reports a segment that never says.

### 3. Exact names, as they exist

`order_completed`, not "a purchase". `plan_name`, not "their plan". `"trial"`, not "on a trial".
For a segment, every attribute, event, segment or consent the description names is looked up in the
installer's project: exactly one match is used, none or several make the step vague (R36). A
paraphrase is a lookup that fails. If the name differs between projects, declare it under
`prerequisites` so Run is gated on it, and spell it the way most projects do.

### 4. Every value written out

The threshold, the window, the count, the schedule, the tone, the length, the button label. "In the
last 30 days", never "recently". "5 or more times", never "often". "Refresh daily", never "keep it
fresh". An unstated value is a default nobody chose or a field the installer has to fill, and
either way two installs differ. Where the value came from is a separate question: if nothing
measured it, it goes under `does_not_claim`.

### 5. Earlier steps by title, and in `dependsOn`

When a step uses an earlier step's result, it names that step by its **title** ("the users in 'Find
trials ending this week'") and lists its id in `dependsOn`. The step check wires the dependency
from the wording, refuses one that is not above it (`needs_earlier_step`) and one that makes the
wrong kind of thing (`wrong_earlier_step`). Never `{{steps.s1}}`, never "that segment", never "the
list above": the engine's rules forbid placeholders and anything in curly braces, and "that" points
at nothing.

### 6. What only the installer has goes in `inputs`

A journey, a form, a Slack channel, a billing link, an attached image, a brand colour. The
description says "the demo request form chosen for this run" and an `inputs` row says what the
installer supplies and what happens without it. A value the installer may change gets a default
written into the step and an `if_missing` saying the default is used. Never an id:
`scripts/portability.py` blocks UUIDs, long numeric ids, opaque ids, email addresses, links into
one workspace and hardcoded segment or journey ids.

### 7. Instruction only

The step check reads every sentence as something to do. Rationale ("the highest-ROI cohort"),
another product's vocabulary ("the Klaviyo RFM cohort"), a model or pipeline name, a statistic
nobody in the recipe measured: each is either an instruction the engine cannot follow or noise that
changes what it derives. Delete them. The reason a recipe exists goes in its `description` at the
top, which no step runs.

## Six ways a reasonable description is read two ways

Each one is in this repository's history.

- **"A demo-request form"** reads as "any form". The step needs the one form the installer picks,
  so it is an input, and the step says "the demo request form chosen for this run".
- **`utm_source = "<source>"`** is a placeholder, so the step check has nothing to resolve. The
  rewrite names `"google"` and `"cpc"` and makes the pair an input with that default.
- **"Description: ... Trigger AE whitespace task or executive outreach."** closed a segment step in
  `accounts-no-open-deal`. The step check reads it as a second job, and a task is not something the
  engine builds. The rewrite stops at the last condition.
- **"Generate nurture content per segment: hot, warm, cold"** is three emails in one step, with no
  length, subject or call to action for any.
- **`[Product] vs [Competitor]`** points at nothing. The lint reports bracket placeholders; a
  lowercase `[link]` is just as vague and is not caught.
- **"Pipeline: flux-pro/kontext"** names a model. The engine picks the model and takes no
  instruction about it.

[WRITING-STEPS.md](writing-steps.md) has full before and after versions. Per builder, the good and
bad steps are in [references/entities/](entities/README.md).

## What validation does and does not prove

`validate_recipes.py --lint` catches the shapes above that a pattern can see: placeholders,
rationale words, a fixed list of vendor names, segments that never say who, descriptions over 1200
characters, ids that only exist in one workspace and text aimed at the agent. It cannot see whether
`order_completed` exists in anyone's project, whether 30 days is the right window, or whether two
people would read your sentence the same way. That last one is this file's question, and only
reading the step out loud answers it.

## Provenance, and how this file goes wrong

The engine behaviour here is read from `intempt/llm-wrapper` at the commit `scripts/recipe_contract.py`
names in `ENGINE_REF`: `md_import.py` for the import rules and the entity list, `step_check.py` for
the derivation, the vague rule (R36) and the earlier-step checks. If the engine disagrees with this
file, **the engine wins and this file is wrong**.

## Before you keep a step, ask it out loud

> Could two installers following this description end up with different things built?

If yes, the step is not finished. The fix is never longer prose. It is naming who, the exact event
or attribute, every value, and the earlier step by its title.
