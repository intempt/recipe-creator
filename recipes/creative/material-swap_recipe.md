---
name: material-swap
description: |
  Use when a user mentions "material swap", "re-cover", "re-finish", "change material", "change color", or asks to change the material or finish of a product. Re-cover, re-finish, re-colour.
arguments: []
intempt:
  id: material-swap
  version: 1.0.0
  slashCommand: /material-swap
  group: Creative
  shortDescription: "Generate a single material-swapped product image that changes the product's surface material or finish while preserving its original form."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, material, swap]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Swap material or finish"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Change the material, finish, or colour of a product while keeping form, pose, camera angle, and shadow identical."
      prompt: |
        Swap the material/finish on a product.

        Keep the frame, pose, camera angle, and shadow identical. Only change the surface material (e.g., linen → bouclé, oak → walnut, matte → gloss).

        Pipeline: flux-pro/kontext (material-targeted edit)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Material-swapped product image." }
---

# Material Swap

## Procedure

1. **Swap material or finish** [`generate_image`] — Change surface material while preserving form. → produces: image

## Notes

- Pipeline: flux-pro/kontext.
- Supports fabric, wood, metal, paint, and texture swaps.
