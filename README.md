# Intempt recipe creator

Write a recipe for the [Intempt](https://intempt.com) platform and submit it to the Intempt
Collective Marketplace.

A recipe is one markdown file, `recipe.md`. Its frontmatter lists steps; each step's `description`
is the instruction Blu, Intempt's agent, runs inside a customer's project with that person's own
access: build a segment, write an email, generate an image. A recipe that only works in your project
is not a recipe, it is a note to yourself, so everything the installer supplies is declared as an
input.

## Four ways in

| | Start from | Use when |
|---|---|---|
| **I have an idea** | a conversation | nothing is built yet |
| **From my Intempt workspace** | a segment or attribute you already built | it works in your project and you want others to install it. Read only |
| **I have a recipe.md** | a file you already have | it is written; you want it validated and submitted, or converted from the v1 format |
| **Something else** | tell the agent | it picks the closest route and says which |

All of them end the same way: a `recipe.md` you review, then you choose how it goes. Upload it at
[intempt.com/recipes/submit](https://intempt.com/recipes/submit), or have the agent send it with
`intempt recipe submit`, which previews first and cannot send without your explicit yes.

## Start here

**[START-HERE.md](./START-HERE.md)**: install, then create the recipe. If you are pasting a link to
someone, paste that one.

The rest is reference, in the order you will want it:

1. [PREREQUISITES.md](./PREREQUISITES.md): the Intempt CLI, signing in, the plugin.
2. Your route: [workflows/idea-to-recipe.md](./workflows/idea-to-recipe.md),
   [workflows/workspace-to-recipe.md](./workflows/workspace-to-recipe.md) or
   [workflows/existing-recipe.md](./workflows/existing-recipe.md).
3. [WRITING-STEPS.md](./WRITING-STEPS.md): read this before writing any step. The test, the vague
   rule, and before and after examples from this repository. [DETERMINISM.md](./DETERMINISM.md) is
   the reasoning behind it: what the engine derives from a step, and the seven rules that pin it.
4. [NO-ENTITY-EXISTS.md](./NO-ENTITY-EXISTS.md): read this while you are still talking. The jobs the
   engine cannot build yet, and how they become Coming soon instead of being faked.
5. [references/recipe-contract.md](./references/recipe-contract.md): what the file must contain.
6. [references/entities.md](./references/entities.md): what a step can build, generated from the recipes,
   and [references/entities/](./references/entities/README.md): one page per builder, with good and bad
   steps.
7. [RECIPE-TEMPLATE.md](./RECIPE-TEMPLATE.md) and [PACKAGE-LAYOUT.md](./PACKAGE-LAYOUT.md).
8. [VALIDATION.md](./VALIDATION.md), then [SUBMITTING.md](./SUBMITTING.md).

**This repository is an installable plugin.** In Claude Code:

```
/plugin marketplace add intempt/recipe-creator
/plugin install intempt-recipe-creator@intempt-recipe-creator
```

The skill lives at [plugin/skills/intempt-recipe-creator/](./plugin/skills/intempt-recipe-creator/):
the whole flow, its own validator and the worked example, so it runs with no network.

## Install now and Coming soon

Every step declares what it `builds`. A recipe whose steps all build something the engine supports
today is **Install now**; the rest are **Coming soon**, and the catalog says which builder each is
waiting on. The counts are in [references/entities.md](./references/entities.md), generated from
the recipes.

## Where finished recipes live

- **[examples/](./examples/README.md)** is a curated set to copy from, chosen because it meets the
  bar. Its README says what each one teaches.
- **`recipes/<author>/<recipe-id>/recipe.md`** holds published recipes. A folder there is written
  only when a submission is approved. `recipes/intempt/` holds the recipes the Intempt team
  publishes.

When a customer installs a recipe, Intempt makes a copy in their project. That copy is theirs to
edit and never changes underneath them.

## If your agent cannot read this repository

Some sandboxes cannot fetch a GitHub page. Tell the agent to fetch the raw file instead:

```
curl -fsSL https://raw.githubusercontent.com/intempt/recipe-creator/main/START-HERE.md
```

If that also returns nothing, the sandbox has no network at all. Install the plugin instead: it
carries this procedure, the validator and the example, and loads from disk.

**The tell that your agent gave up and improvised:** it names no files from this repository. Ask
which files it read.

## Three things that will save you a rejected submission

**Your project's names do not travel.** A journey id, a form, a list, a value only your project
holds: each becomes an `inputs` row the installer supplies, with what happens when it is missing.

**Every step says who, what and when.** Users or accounts, the exact event or attribute, every
threshold and window written out. A step the engine finds vague does not run; it waits for someone
to clarify it. [WRITING-STEPS.md](./WRITING-STEPS.md) is the bar.

**Say what you did not check.** If a threshold is your judgment rather than something measured, put
it under `does_not_claim`. A recipe that declares nothing cannot be trusted or corrected.

## Licence

MIT. See [LICENSE](./LICENSE). You keep the copyright in a recipe you submit; accepted recipes are
published under MIT with your attribution preserved.
