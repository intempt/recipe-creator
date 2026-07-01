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
  shortDescription: "Clean alpha, ready to drop in."
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
      title: "Remove background"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Remove the background from a product image, producing a clean alpha-channel cutout."
      prompt: |
        Remove the background from a product image.

        Keep the SAME product in the SAME position. Replace the backdrop and shadow with transparency (alpha channel). Do not re-render or modify the product.

        Pipeline: flux-pro/kontext (background isolation)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Product on transparent background." }
---

# Background Remove

## Procedure

1. **Remove background** [`generate_image`] — Isolate product with clean alpha cutout. → produces: image

## Notes

- Pipeline: flux-pro/kontext for background isolation.
- Product identity and position preserved exactly.
