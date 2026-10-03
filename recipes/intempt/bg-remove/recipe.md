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
steps:
  - id: s1
    title: Cut out the product
    summary: >-
      Replaces the backdrop and shadow with a transparent alpha channel. The product stays in the same
      position and is not re-rendered.
    builds: image
    description: |-
      Remove the background from a product image.
      Keep the SAME product in the SAME position. Replace the backdrop and shadow with transparency (alpha channel). Do not re-render or modify the product.
      Pipeline: flux-pro/kontext (background isolation)
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

## Availability

Install now: every step builds something the engine supports today.
