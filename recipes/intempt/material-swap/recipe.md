---
id: material-swap
title: Material and finish swap
slash_command: /material-swap
group: Creative
owner: intempt
curator: aurobind
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
  industry:
    - b2b-saas
    - ecommerce
    - media
    - social
  vertical: []
  complexity: quick
  executionMode: oneshot
  tags:
    - image
    - material
    - swap
inputs:
  - input: Product image
    what_the_installer_supplies: The product photo to change
    if_missing: The step is marked vague and waits until one is attached.
  - input: New material
    what_the_installer_supplies: The material, finish or colour to change to, for example walnut instead
      of oak
    if_missing: The step is marked vague and waits until one is chosen.
touches:
  reads:
    - The product image you supply when you run it
    - The new material you supply when you run it
  writes:
    - A new image, from step 1 "Swap the material"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Swap the material
    summary: >-
      Changes only the surface material, for example linen to boucle, oak to walnut, or matte to gloss.
      Frame, pose, camera angle and shadow are identical.
    builds: image
    description: |-
      Edit the product image attached to this run.
      Change only the product's surface material to the new material chosen for this run.
      Keep the frame, the pose, the camera angle and the shadow identical.
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

## What this recipe touches

Reads:

- The product image you supply when you run it
- The new material you supply when you run it

Writes:

- A new image, from step 1 "Swap the material"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Product image | The product photo to change | The step is marked vague and waits until one is attached. |
| New material | The material, finish or colour to change to, for example walnut instead of oak | The step is marked vague and waits until one is chosen. |

## Availability

Install now: every step builds something the engine supports today.
