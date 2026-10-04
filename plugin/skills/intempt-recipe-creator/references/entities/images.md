# Images

| `builds` | What it makes | Install now |
|---|---|---|
| `image` | an image | yes |

## What the builder makes

A generated or edited image saved in the installer's project. The engine picks the model; the
description never names one. An image an earlier step made can be used by a later step that names
that step by its title; the step check records what the later step needs from it (an email that uses
an image as its hero needs `image`) and refuses an earlier step that makes the wrong kind of thing
(`wrong_earlier_step`).

## A good description names

- whether it generates a new image or edits "the image attached to this run";
- how many images;
- exactly what changes and what must stay the same: composition, colours, subject, position;
- the size or aspect ratio, when it matters;
- nothing about a model, a pipeline or a vendor.

## Good, from `recipes/intempt/`

`bg-remove` (Install now):

```
Edit the product image attached to this run.
Remove the backdrop and the shadow and replace them with a transparent background.
Keep the product in exactly the same position, and do not re-render or alter it.
```

`ad-variants` (Install now) is in [../../examples/intempt/ad-variants/recipe.md](../examples/intempt/ad-variants/recipe.md):
six images, each changing exactly one named thing.

## Bad, from `recipes/intempt/`

`bg-remove` before the rewrite in this repository's history:

```
Remove the background from a product image.
Keep the SAME product in the SAME position. Replace the backdrop and shadow with transparency
(alpha channel). Do not re-render or modify the product.
Pipeline: flux-pro/kontext (background isolation)
```

"A product image" does not say which one, and the pipeline line names a model the engine takes no
instruction about. The rewrite says "the product image attached to this run" and drops the pipeline.

## What belongs in `inputs`

- every image the step edits or uses as a reference: "The step is marked vague and waits until one
  is attached" is the honest `if_missing`;
- a choice the installer makes per run, such as which dimensions to vary, with the default written
  into the step.

What the generated image will contain, when the step leaves it to run time (a new headline, a new
palette), goes under `does_not_claim`.

## Common lint failures

| Lint | Seen as | Fix |
|---|---|---|
| not linted: the vendor lint knows a fixed list of marketing tools, not models | `Pipeline: flux-pro/kontext` | delete it; the engine picks the model |
| bracket placeholder | `[Product photo]` | "the product image attached to this run", plus an `inputs` row |
