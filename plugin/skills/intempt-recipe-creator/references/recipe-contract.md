# The recipe.md contract (v2)

A recipe is one file, `recipes/<partner>/<id>/recipe.md`: YAML frontmatter, then a body
generated from it. The frontmatter is exactly what the Intempt engine reads, so a recipe
that passes `scripts/validate_recipes.py` is a recipe the engine can load.

Where each rule comes from, so nobody has to take this file's word for it:

| Rule | Source |
|---|---|
| A step is `id`, `title`, `description`, `dependsOn`; everything else is derived | `llm-wrapper` `src/blu_chat/sevices/recipes/md_import.py`, engine team rulings 2026-09-30 |
| `description` is the one instruction a step runs on | `llm-wrapper` `orchestrator.py` `step_text()` |
| command, entity, kind, arguments and `modelConfig` come from the step check | `llm-wrapper` `step_check.py` |
| A description must point to things that exist, or the step is marked vague | `step_check.py` R36 |
| Ids are `s1`, `s2`, ... and a step may only use earlier steps | `md_import.py` RULES, `step_check.py` `needs_earlier_step` |
| No placeholders, variables or curly braces | `md_import.py` RULES |
| Outputs are `{key, producedByStep}` | `llm-wrapper` `validate.py:260` |
| `slash_command` is `/kebab-case` | `llm-wrapper` `validate.py:51` |
| Which entities the engine can build | `md_import.py` `ALLOWED_ENTITIES`, see [entities.md](entities.md) |

## Frontmatter

```yaml
id: vip-thank-you                # kebab-case, equals the folder name
title: Thank your best customers # a real name, never the id
slash_command: /vip-thank-you    # unique across the repo
group: Segments                  # one of the Marketplace groups
owner: intempt                   # equals the partner folder: recipes/<owner>/
curator: somya                   # optional, kebab-case: who on the owner's team stands behind it
summary: >-                      # PUBLIC. One sentence, under 200 characters
  Finds the customers who spent the most this quarter and sends them a thank-you email.
description: >-                  # what the whole recipe is for, read by Blu when matching
  ...
version: 2.0.0
visibility: published            # optional; draft keeps it out of the public catalog
classification: {product: [segments], mode: [ecommerce], complexity: quick, tags: [vip]}
prerequisites:                   # optional, gates Run in the console
  events: [{value: order_completed, severity: blocking}]
  integrations: [{value: shopify, severity: blocking}]
inputs:                          # optional: what the installer supplies
  - input: Spend threshold
    what_the_installer_supplies: The order total that counts as a top spender
    if_missing: 500 is used.
does_not_claim:                  # optional: what the recipe does not prove
  - The 500 threshold is the author's choice, not measured against your orders.
touches:                         # REQUIRED: reads, writes and never, each a non-empty list
  reads:
    - The order_completed event in your project
  writes:
    - A new segment, from step 1 "Find your top spenders"
    - A new designed email, from step 2 "Thank them by email"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find your top spenders        # under 40 characters, an action
    summary: >-                          # PUBLIC. The concrete rule, for the Marketplace
      Customers whose orders in the last 90 days add up to more than 500.
    builds: segment                      # what this step makes; drives Install now
    description: >-                      # THE INSTRUCTION. Never published
      Build a segment of users whose total order_completed amount in the last 90 days
      is more than 500. Refresh it daily.
  - id: s2
    title: Thank them by email
    summary: A short thank-you email in your brand voice.
    builds: email_html
    description: >-
      Write a designed thank-you email for the users in Find your top spenders. Two
      sentences, no discount, signed by the founder.
    dependsOn: [s1]
outputs:
  - {key: top_spenders, producedByStep: s1, type: segment}
  - {key: thank_you_email, producedByStep: s2, type: email_html}
```

## owner and curator

`owner` is the company that submitted the recipe and equals its folder. `curator` is optional: the
person on that company's team who stands behind it, in kebab-case. For `owner: intempt` the curator
must be one of `INTEMPT_CURATORS` in `scripts/recipe_contract.py`, which also maps each Marketplace
group to the curator who looks after it. The public catalog publishes `curator`, so the website can
read the person from the repository instead of deriving one from the group.

## touches, inputs and does_not_claim

These three are for the person deciding whether to install the recipe, and for the reviewer. The
engine ignores them: `llm-wrapper` drops unknown top-level keys and `single-metadata` keeps them in
`extra`, so they never reach a step.

| Field | Required | Shape | Rendered as |
|---|---|---|---|
| `touches` | yes | `{reads: [], writes: [], never: []}`, each a non-empty list of plain sentences | What this recipe touches |
| `inputs` | no | rows of `{input, what_the_installer_supplies, if_missing}` | Declared inputs |
| `does_not_claim` | no | a list of plain sentences | What this recipe does not claim |

- **reads**: the events, attributes, connections and supplied files the steps rely on.
- **writes**: one line per step, naming what it creates in plain words. A step builds something new;
  say so.
- **never**: what the recipe will not do. Every recipe can say "Nothing runs until you approve the
  plan in Blu.", because Blu shows the plan with one approval before executing anything.
- **inputs**: anything that only exists in the installer's project or that they choose per run: a
  journey, a form, an attached image, a channel. `if_missing` says what happens without it.
- **does_not_claim**: where a value came from when nothing measured it, and what is decided at run
  time rather than written down.

No em-dashes or en-dashes in any of them; the validator refuses both.

Fields the file must never carry: `command`, `entity`, `kind`, `arguments`, `modelConfig`,
`prompt`, `bindsAs`. The engine derives them from the description when the recipe is added,
and a value written here would be ignored or contradicted.

## Writing a description the engine can run

The description is what a person would type into the canvas's Add step panel. The step
check reads it once and decides what to build. Write it so that check has nothing to guess.

1. **One thing per step.** "Build a segment and email it" is two steps.
2. **Say who it is about**: users or accounts. A segment without it is vague.
3. **Name what exists, exactly**: the event `order_completed`, the attribute `plan`, the
   value `enterprise`. A description that points at nothing real is marked vague and waits
   for a person to clarify it.
4. **Write every value out**: the threshold, the window, the schedule, the tone.
5. **Name an earlier step by its title** when you use its result, and list it in
   `dependsOn`. Never write `{{...}}`.
6. **Instruction only.** No rationale ("the differentiator is..."), no other vendors' names,
   no bracket placeholders like `[Product]`. `validate_recipes.py --lint` reports all three.

## Availability: Install now or Coming soon

Every step declares `builds`. A recipe is **Install now** when every step builds an entity
the engine can build today, and **Coming soon** otherwise, waiting on the builders it names.
The catalog publishes `availability` and `waitingOn`; the website and console read them.
When the engine gains a builder, move it into `BUILDABLE_ENTITIES` in
`scripts/recipe_contract.py` and every recipe that was waiting only on it flips.

## Public and private

The public catalog (`scripts/build_artifacts.py`) carries `summary`, step `title` and step
`summary`. It never carries a step `description`: that is the instruction Blu runs, and the
build fails if one leaks.
