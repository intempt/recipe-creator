# Idea to recipe

For when nothing is built yet, or what you built is not in Intempt. No sign-in, no CLI.

## What you will be asked

The order matters: purpose before mechanics, because mechanics without a purpose produce a recipe
that runs and helps nobody.

1. **The job.** What does a team want done, in their words? This becomes the `summary` customers
   read and the `description` Blu matches against.
2. **Who it is about.** Users or accounts, and which ones: paying, on trial, in the last 30 days.
3. **What exists in their project.** The exact events and attributes the recipe relies on:
   `order_created`, `plan_name`, `end_date`. A recipe that names an event nobody sends cannot run,
   so these become `prerequisites` where they are required.
4. **The steps, one thing each.** A segment, then an email that names the segment by its step
   title. Each step builds one entity from [../references/entities.md](entities.md).
5. **Every value.** Each threshold, window, tone and length, written out. "Recently" is not a value;
   "in the last 14 days" is.
6. **The honest edges.** What it should not guess at, what happens when data is missing, which values
   are your judgment rather than something measured. These become `does_not_claim` lines.
7. **The boundary.** What it is not for. Naming the adjacent jobs keeps Blu from offering it when
   somebody asks loosely.

## What comes out

A complete `recipe.md` at `<your-handle>/<recipe-id>/recipe.md` in your working directory, with
`touches`, `inputs` where the installer supplies something, and a `does_not_claim` line that names
the interview as the source of its logic:

```yaml
does_not_claim:
  - The steps and thresholds come from the author's interview, not from a project they ran in.
```

That line is not a formality. Interview logic has no ground truth: nothing has checked it against a
project that already ran it.

## Then validate and submit

The interview is not the last step. Validate it ([../VALIDATION.md](validation.md)), read it end
to end, then pick a way to submit ([../SUBMITTING.md](submitting.md)).
