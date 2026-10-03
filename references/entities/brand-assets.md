# Brand assets: avatar, pose, scene and design system

| `builds` | What it makes | Install now |
|---|---|---|
| `avatar` | a brand avatar | yes |
| `pose` | a brand pose | yes |
| `scene` | a brand scene | yes |
| `design_system` | a brand design system | yes |

## What the builders make

The engine's catalog lists four brand builders: a brand avatar, a brand pose, a brand scene and a
brand design system (`md_import.py` `ALLOWED_ENTITIES`). Each saves one asset in the installer's
project. To the step check they are ordinary builders (`step_check.py` step 6d): a field the
description states is stored in `modelConfig`, and an unstated required field takes the builder's
default or stays a gap the installer fills before the step runs.

## A good description names

- which asset, and one per step;
- what it depicts or defines, concretely enough that two people would picture the same thing;
- an earlier asset it builds on, by that step's title, with `dependsOn`;
- every value as a value: a hex code, a font name, a count, never "on-brand".

## Good and bad, from `recipes/intempt/`

No recipe in this repository builds a brand asset yet, so there is no real step to quote. Do not
copy one from another product's catalog; write to the list above and run
`python3 scripts/validate_recipes.py --lint` on it.

## What belongs in `inputs`

- the installer's own brand: a logo, a reference image, existing colours or fonts. A recipe that
  writes one brand's hex codes into the step builds that brand for every installer;
- an asset the step builds on that no earlier step of the same recipe builds.

## Common lint failures

| Lint | Seen as | Fix |
|---|---|---|
| bracket placeholder | `[Brand colour]` | an `inputs` row for the brand, or the value written out |
| not linted: the vendor lint knows a fixed list of marketing tools | a design tool or a model name | describe the asset, not the tool |
