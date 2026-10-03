---
id: material-swap
title: Material and finish swap
slash_command: /material-swap
group: Creative
owner: intempt
summary: Changes the material, finish or colour of a product while the shape, pose, camera angle and shadow
  stay exactly as shot.
description: >-
  Re-cover, re-finish, re-colour.
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
    - material
    - swap
steps:
  - id: s1
    title: Swap the material
    summary: >-
      Changes only the surface material, for example linen to boucle, oak to walnut, or matte to gloss.
      Frame, pose, camera angle and shadow are identical.
    builds: image
    description: |-
      Swap the material/finish on a product.
      Keep the frame, pose, camera angle, and shadow identical. Only change the surface material (e.g., linen to bouclé, oak to walnut, matte to gloss).
      Pipeline: flux-pro/kontext (material-targeted edit)
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Material-swapped product image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Material and finish swap

Changes the material, finish or colour of a product while the shape, pose, camera angle and shadow stay exactly as shot.

## Steps

1. **Swap the material** (builds image)

   Changes only the surface material, for example linen to boucle, oak to walnut, or matte to gloss. Frame, pose, camera angle and shadow are identical.

## What you end up with

- **image** (image): Material-swapped product image.

## Availability

Install now: every step builds something the engine supports today.
