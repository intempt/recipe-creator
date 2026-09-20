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
  title: 'Material and finish swap'
  shortDescription: 'Changes the material, finish or colour of a product while the shape, pose, camera angle and shadow stay exactly as shot.'
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
      title: 'Swap the material'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Changes only the surface material, for example linen to boucle, oak to walnut, or matte to gloss. Frame, pose, camera angle and shadow are identical.'
      prompt: |
        Swap the material/finish on a product.

        Keep the frame, pose, camera angle, and shadow identical. Only change the surface material (e.g., linen to bouclé, oak to walnut, matte to gloss).

        Pipeline: flux-pro/kontext (material-targeted edit)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Material-swapped product image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Material and finish swap

Changes the material, finish or colour of a product while the shape, pose, camera angle and shadow stay exactly as shot.

## What it does

1. **Swap the material** (`generate_image`)

   Changes only the surface material, for example linen to boucle, oak to walnut, or matte to gloss. Frame, pose, camera angle and shadow are identical.

## What you end up with

- **image** (image): Material-swapped product image.
