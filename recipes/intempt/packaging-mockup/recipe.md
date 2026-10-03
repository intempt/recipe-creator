---
id: packaging-mockup
title: Label wrapped on a package
slash_command: /packaging-mockup
group: Creative
owner: intempt
curator: aurobind
summary: Wraps your flat label artwork photorealistically around a 3D can, bottle or box, with the label
  content unchanged.
description: >-
  Flat label to wrapped on 3D pack.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  complexity: quick
  executionMode: oneshot
  tags:
    - image
    - packaging
    - mockup
    - label
inputs:
  - input: Label artwork
    what_the_installer_supplies: The flat label artwork
    if_missing: The step is marked vague and waits until one is attached.
  - input: Package shape
    what_the_installer_supplies: A can, a bottle or a box
    if_missing: The shape is decided when the step runs.
touches:
  reads:
    - The label artwork you supply when you run it
    - The package shape you supply when you run it
  writes:
    - A new image, from step 1 "Wrap the label"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Wrap the label
    summary: >-
      Takes the same label artwork, wordmark and layout and wraps it around a 3D package on the same backdrop.
      Nothing on the label is redrawn.
    builds: image
    description: |-
      Edit the flat label artwork attached to this run.
      Wrap it photorealistically around a 3D package on the same backdrop.
      Keep the wordmark, the layout and every element of the label exactly as they are.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Packaging mockup image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Label wrapped on a package

Wraps your flat label artwork photorealistically around a 3D can, bottle or box, with the label content unchanged.

## Steps

1. **Wrap the label** (builds image)

   Takes the same label artwork, wordmark and layout and wraps it around a 3D package on the same backdrop. Nothing on the label is redrawn.

## What you end up with

- **image** (image): Packaging mockup image.

## What this recipe touches

Reads:

- The label artwork you supply when you run it
- The package shape you supply when you run it

Writes:

- A new image, from step 1 "Wrap the label"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Label artwork | The flat label artwork | The step is marked vague and waits until one is attached. |
| Package shape | A can, a bottle or a box | The shape is decided when the step runs. |

## Availability

Install now: every step builds something the engine supports today.
