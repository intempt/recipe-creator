---
id: bg-remove
title: Background removal
slash_command: /bg-remove
group: Creative
owner: intempt
summary: Strips the backdrop and shadow from a product image and returns a transparent cutout you can
  drop anywhere.
description: >-
  Clean alpha, ready to drop in.
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
    - background
    - remove
inputs:
  - input: Product image
    what_the_installer_supplies: The product photo to cut out
    if_missing: The step is marked vague and waits until one is attached.
touches:
  reads:
    - The product image you supply when you run it
  writes:
    - A new image, from step 1 "Cut out the product"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Cut out the product
    summary: >-
      Replaces the backdrop and shadow with a transparent alpha channel. The product stays in the same
      position and is not re-rendered.
    builds: image
    description: |-
      Edit the product image attached to this run.
      Remove the backdrop and the shadow and replace them with a transparent background.
      Keep the product in exactly the same position, and do not re-render or alter it.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Product on transparent background.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Background removal

Strips the backdrop and shadow from a product image and returns a transparent cutout you can drop anywhere.

## Steps

1. **Cut out the product** (builds image)

   Replaces the backdrop and shadow with a transparent alpha channel. The product stays in the same position and is not re-rendered.

## What you end up with

- **image** (image): Product on transparent background.

## What this recipe touches

Reads:

- The product image you supply when you run it

Writes:

- A new image, from step 1 "Cut out the product"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Product image | The product photo to cut out | The step is marked vague and waits until one is attached. |

## Availability

Install now: every step builds something the engine supports today.
