# Segments

| `builds` | What it makes | Install now |
|---|---|---|
| `segment` | a segment of users or accounts | yes |

## What the builder makes

A saved segment in the installer's project: a named group of users, or of accounts, defined by
conditions on attributes, events, other segments or consent. The engine's own catalog describes it
as "a segment of users or accounts; read: who is in a segment" (`md_import.py` `ALLOWED_ENTITIES`).

## What the step check does with it

This is the one builder whose description is resolved against the installer's project before
anything runs (`step_check.py` steps 6b and 6c):

1. **Who.** The check reads whether the segment is about users or accounts. That answer is stored
   in `modelConfig` only when the description says it.
2. **The condition.** Every attribute, event, segment or consent the description names is looked
   up in the project. Exactly one match: the condition is known and stored. No match: the step is
   marked vague with "Say which attribute, event, segment or consent this segment is based on."
   More than one match: "Say its exact name."
3. **The value.** An event, segment or consent condition needs no value (did it at least once, is
   in it, has consented). An **attribute** condition needs the value written out, or it stays a gap.

## A good description names

- **users** or **accounts**, in the first sentence;
- the segment's name, in quotes;
- each condition with the exact event or attribute name as it exists in a project, its operator and
  its value;
- the window on every event: "in the last 30 days", "between 60 and 90 days ago", "at any time";
- for accounts built from user behaviour, how it rolls up: "the users in the account together did".

## Good, from `recipes/intempt/`

`churn-risk-users` (Install now):

```
Build a segment of users named "Churn Risk Users".
A user is in the segment only when all of these are true:
- they did the session_start event 5 or more times between 60 and 90 days ago
- they did not do the session_start event in the last 30 days
- their plan_name attribute is not "free"
```

`accounts-no-open-deal` (Install now), for accounts:

```
Build a segment of accounts named "Accounts With No Open Deal".
An account is in the segment only when all of these are true:
- its has_open_deal attribute is false
- its account_health attribute is "healthy"
- its users_count attribute is 3 or more
- the users in the account together did the session_start event 5 or more times in the last 30 days
```

## Bad, from `recipes/intempt/`

`cold-outbound` step 1 (Coming soon), as it stands today. The lint reports "segment never says who
it is about":

```
Build target prospect list from ICP criteria (firmographic + intent signals).
```

Nothing in it exists in a project: no attribute, no event, no value. The step check can only ask.

`demo-requested-accounts` before the rewrite in this repository's history (now Install now):

```
Create a segment called "Demo-Requested Accounts".
Object: Accounts
Rules (all conditions joined by AND):
- Event (across users in account): submit_on a demo-request form occurred >= 1 time in last 30 days
- AND Attribute: has_open_deal = false
Description: ... Highest SDR-routing priority: research consistently shows 53% conversion rate for
1-hour response vs 17% after 24 hours. SLA: SDR contact within 1 hour, AE follow-up within 24 hours.
```

"A demo-request form" points at a form only the author has, and the last line is rationale with
numbers nobody in the recipe measured. The step check reads every sentence as something to do. The
published version is [../../examples/intempt/demo-requested-accounts/recipe.md](../examples/intempt/demo-requested-accounts/recipe.md).

## What belongs in `inputs`

- a form, a list, a journey or another segment that only the installer's project has: the step says
  "the demo request form chosen for this run";
- a value the installer should choose, with the default written into the step and the `if_missing`
  saying it is used: see `acquisition-channel-cohort`, where `"google"` and `"cpc"` are the default.

A threshold you picked is not an input. Write it into the step and put where it came from under
`does_not_claim`.

## Common lint failures

| Lint | Seen as | Fix |
|---|---|---|
| segment never says who it is about | "Create a segment over the imported records" | start with "a segment of users" or "of accounts" |
| rationale, not instruction | "Highest SDR-routing priority" | delete it; it is not something to do |
| bracket placeholder | `[segment name]` | write the name, or make it an `inputs` row |
| over 1200 chars | a segment plus what to do with it | split the second job into its own step |

Portability (`scripts/portability.py`) also blocks a segment id, a journey id or a form id written as
a value: `segment id 4821`. Name the thing, or make it an input.
