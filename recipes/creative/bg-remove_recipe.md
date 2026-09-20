---
name: bg-remove
description: |
  Use when a user mentions "background remove", "remove background", "cut out", "alpha channel", "transparent background", or asks to isolate a product from its background. Clean alpha, ready to drop in.
arguments: []
intempt:
  id: bg-remove
  version: 1.0.0
  slashCommand: /bg-remove
  group: Creative
  title: 'Background removal'
  shortDescription: 'Strips the backdrop and shadow from a product image and returns a transparent cutout you can drop anywhere.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, background, remove]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Cut out the product'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Replaces the backdrop and shadow with a transparent alpha channel. The product stays in the same position and is not re-rendered.'
      prompt: |
        Remove the background from a product image.

        Keep the SAME product in the SAME position. Replace the backdrop and shadow with transparency (alpha channel). Do not re-render or modify the product.

        Pipeline: flux-pro/kontext (background isolation)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Product on transparent background." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Background removal

Strips the backdrop and shadow from a product image and returns a transparent cutout you can drop anywhere.

## What it does

1. **Cut out the product** (`generate_image`)

   Replaces the backdrop and shadow with a transparent alpha channel. The product stays in the same position and is not re-rendered.

## What you end up with

- **image** (image): Product on transparent background.
