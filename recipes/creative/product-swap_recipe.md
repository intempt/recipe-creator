---
name: product-swap
description: |
  Use when a user mentions "product swap", "swap product", "replace product in scene", or asks to swap one product for another in an existing image. Same scene, new product.
arguments: []
intempt:
  id: product-swap
  version: 1.0.0
  slashCommand: /product-swap
  group: Creative
  title: 'Product swap in a scene'
  shortDescription: 'Replaces the product in a shot you already have with a different one, keeping the scene, lighting and shadow the same.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, product, swap]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Swap in the new product'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Replaces only the product with the new SKU at identical size and position. Scene, lighting, shadow and backdrop are unchanged.'
      prompt: |
        Swap the product in an existing image.

        Keep the scene, lighting, shadow, and backdrop unchanged. Replace only the product with the new SKU, maintaining identical size and position.

        Pipeline: flux-pro/kontext (identity-locked swap)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Product-swapped image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product swap in a scene

Replaces the product in a shot you already have with a different one, keeping the scene, lighting and shadow the same.

## What it does

1. **Swap in the new product** (`generate_image`)

   Replaces only the product with the new SKU at identical size and position. Scene, lighting, shadow and backdrop are unchanged.

## What you end up with

- **image** (image): Product-swapped image.
