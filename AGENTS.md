# Working in this repository

This tree is the kit for writing an Intempt recipe and submitting it to the Intempt Collective
Marketplace. **`START-HERE.md` is the entry point.** This file only carries what an agent cannot
infer from the tree, and points at the pages that say the rest.

## If the `intempt-recipe-author` skill is loaded, follow it and stop reading here

That skill is this kit's procedure. When it is available, installed as a plugin or invoked by name,
it is the authority on what happens next. Re-deriving the steps from these files produces a slower
and worse version of the same thing. Everything below is for the case where it is not loaded.

One exception, about which copy is newer. An installed copy is frozen at install time. Its Step 0a
fetches the published version and switches to it, so normally this resolves itself. If you are
reading this tree and the skill is loaded and it announces an older version than
`plugin/.claude-plugin/plugin.json` here declares, say both numbers and follow the tree. If a clone
of this repo is already on disk from an earlier run, `git pull` it before reading.

## If it is not loaded, read the raw files in this order

Read them raw, never through a tool that hands back a summary. A summary keeps the headline rules
and drops the exceptions.

```
curl -fsSL https://raw.githubusercontent.com/intempt/recipe-creator/main/<NAME>
```

1. `START-HERE.md`: the order of work, the route question, the stops.
2. `references/recipe-contract.md`: what a recipe file must contain.
3. `references/entities.md`: what a step can build today, and what is coming.
4. `WRITING-STEPS.md`: how to write a step the engine can run.
5. `NO-ENTITY-EXISTS.md`: the jobs the engine cannot build yet.
6. The workflow for the route: `workflows/idea-to-recipe.md`, `workflows/workspace-to-recipe.md`
   or `workflows/existing-recipe.md`.
7. `VALIDATION.md`, then `SUBMITTING.md`.

## Three things worth knowing before writing a recipe

- **The step `description` is the instruction the engine runs.** It is never published and it is
  not marketing copy. `WRITING-STEPS.md` is the bar.
- **A recipe runs in someone else's project.** No ids, names or values that only exist in yours.
  Anything the installer supplies goes in `inputs`, with what happens when it is missing.
- **Nothing is submitted without an explicit yes.** `intempt recipe submit` previews first and
  refuses to send without the random token the preview mints.

## Do not edit this tree

The recipe you write is its own file in your own working directory. Nothing you build belongs in
these files. `recipes/` holds published recipes, written only when a submission is approved.
`examples/` holds recipes chosen to copy from.
