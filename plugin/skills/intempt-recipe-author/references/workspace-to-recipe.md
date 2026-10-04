# Workspace to recipe

For when you already built the thing in Intempt: a segment that works, an attribute you rely on.
The recipe makes it installable by every other team.

## What this route reads, and what it never touches

It reads your project's **configuration only**, and only through these calls:

| Call | What it returns |
|---|---|
| `intempt whoami` | your organization and project |
| `intempt segments list_segments` | your segments |
| `intempt events list_events` | the events your project receives |
| `intempt events get_event` | one event definition |
| `intempt events list_event_attributes` | the properties an event carries |
| `intempt users list_attribute_columns` | the user and account attributes in your project |

Or the same reads through the Intempt MCP server: `whoami` and `list_segments`. Every call above is
marked read in the CLI's command registry.

If a segment's rules are not in what `list_segments` returns, ask the user to paste them from the
console or describe them. Do not reach for another command to get them.

That allowlist is the whole surface. It never creates, updates or deletes anything, never runs a
segment, never reads a user's record, and never starts a journey. If a command you would need is not
on the list, the recipe gets a `does_not_claim` line instead.

## The steps

1. `intempt whoami`, and say the organization and project out loud. If it is the wrong one, stop.
2. Ask which segment or attribute to start from. Do not list everything and pick one yourself.
3. Read that one item's rules, then check each event and attribute it names against the event and
   attribute lists, so the recipe names them exactly.
4. Turn its rules into a step `description` in plain words, following
   [../WRITING-STEPS.md](writing-steps.md). Copy event names, attribute names and values exactly
   as the rules hold them.
5. Anything that only exists in your project becomes an input: a journey id, a form, a list. A
   recipe that names your ids fails on everyone else's project.
6. Ask why each decisive threshold is what it is. "It was arbitrary" is a good answer; it becomes a
   `does_not_claim` line.
7. Write the rest of the draft, validate, and submit. See [../SUBMITTING.md](submitting.md).

## What comes out

A `recipe.md` whose rules match a segment that already ran in your project. Say so, and say what it
does not prove:

```yaml
does_not_claim:
  - The rules were copied from a segment in the author's project. They are not checked against yours.
```
