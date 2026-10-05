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
  shortDescription: "Generate a single image where the specified new product replaces the original product while preserving the scene, lighting, shadow, and backdrop."
  availability: available
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
      title: "Swap product in scene"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Replace one product with another in the same scene, preserving lighting, shadow, and backdrop."
      prompt: |
        Swap the product in an existing image.

        Keep the scene, lighting, shadow, and backdrop unchanged. Replace only the product with the new SKU, maintaining identical size and position.

        Pipeline: flux-pro/kontext (identity-locked swap)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Product-swapped image." }
---

# Product Swap

## Procedure

1. **Swap product in scene** [`generate_image`] — Replace one product with another, preserving the scene. → produces: image

## Notes

- Pipeline: flux-pro/kontext for identity-locked product replacement.
- Scene, lighting, shadow, and backdrop preserved exactly.
