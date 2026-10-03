# Events and attributes

| `builds` | What it makes | Install now |
|---|---|---|
| `event` | an event definition | yes |
| `attribute` | an attribute on users or accounts | yes |

## What the builders make

- **`event`**: a new event definition in the installer's project. It defines the event; it does
  not send or backfill any.
- **`attribute`**: a new attribute on users or on accounts. An AI attribute can hold a derived value
  such as a score or a tier ([../../NO-ENTITY-EXISTS.md](../../NO-ENTITY-EXISTS.md): there is no
  separate scoring builder).

Both are ordinary builders to the step check (`step_check.py` step 6d): every field the builder asks
for is either stated in the description and stored in `modelConfig`, filled from the builder's
default, or left as a gap the installer fills before the step runs.

## A good description names

For an **attribute**:

- whether it is on **users** or on **accounts**;
- its name in snake_case, in quotes;
- what goes into it, by exact attribute and event name, with every window;
- how each output value is reached: the bands, the tiers, the thresholds, written out;
- when it refreshes.

For an **event**:

- its name in snake_case, in quotes;
- what it means, in one sentence: when it should be recorded;
- the properties it carries, each by name.

## Good, from `recipes/intempt/`

No recipe in this repository is Install now with an `attribute` step yet; they all sit in recipes
that also need a Coming soon builder. This step is lint-clean and close to the bar.
`auto-enrich-new-accounts` step 1 (Coming soon):

```
Create an AI-derived attribute 'icp_fit_score' on the Account object. Inputs after enrichment:
industry (match against ICP target industries), employee count band, annual revenue band, tech stack
signals (does the account use complementary tools that signal fit?), geographic match. Output: 0-100
score with tier (ideal 80+, viable 50-79, marginal 20-49, poor <20). Refreshed when enrichment data
updates.
```

It names the object, the attribute and every tier boundary. What it still leaves open: "ICP target
industries" and "complementary tools" exist only in the author's head. Name them, or make each an
`inputs` row.

No recipe in this repository has an `event` step. Write one to the list above.

## Bad, from `recipes/intempt/`

`account-engagement-score-orchestration` step 1 (Coming soon) ends with:

```
... The account-as-unit aggregation is the differentiator: most CDPs score users, this scores the
buying entity.
```

The lint reports "rationale, not instruction". The step check reads that sentence as something to
do, and there is nothing in it to do.

## What belongs in `inputs`

- a list the author keeps somewhere else: target industries, competitor tools, a territory map;
- a weight or tier boundary the installer is expected to tune, with the default written into the
  step and the `if_missing` saying the default is used.

## Common lint failures

| Lint | Seen as | Fix |
|---|---|---|
| rationale, not instruction | "the differentiator", "best practice" | delete the sentence |
| names another vendor | "the Klaviyo RFM cohort" | describe the rule itself |
| over 1200 chars | an attribute that also builds the segment that reads it | two steps, the segment `dependsOn` the attribute |

An attribute that a later step uses: the later step names it by its step title and lists it in
`dependsOn`, the same as any other earlier result.
