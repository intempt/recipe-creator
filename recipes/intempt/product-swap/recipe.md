---
id: product-swap
title: Product swap in a scene
slash_command: /product-swap
group: Creative
owner: intempt
curator: aurobind
summary: Replaces the product in a shot you already have with a different one, keeping the scene, lighting
  and shadow the same.
description: >-
  Same scene, new product.
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
    - product
    - swap
inputs:
  - input: Original image
    what_the_installer_supplies: The shot that holds the product to replace
    if_missing: The step is marked vague and waits until one is attached.
  - input: New product
    what_the_installer_supplies: The product to swap in
    if_missing: The step is marked vague and waits until one is chosen.
touches:
  reads:
    - The original image you supply when you run it
    - The new product you supply when you run it
  writes:
    - A new image, from step 1 "Swap in the new product"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Swap in the new product
    summary: >-
      Replaces only the product with the new SKU at identical size and position. Scene, lighting, shadow
      and backdrop are unchanged.
    builds: image
    description: |-
      Edit the image attached to this run.
      Replace only the product with the new product chosen for this run, at identical size and position.
      Keep the scene, lighting, shadow and backdrop unchanged.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Product-swapped image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product swap in a scene

Replaces the product in a shot you already have with a different one, keeping the scene, lighting and shadow the same.

## Steps

1. **Swap in the new product** (builds image)

   Replaces only the product with the new SKU at identical size and position. Scene, lighting, shadow and backdrop are unchanged.

## What you end up with

- **image** (image): Product-swapped image.

## What this recipe touches

Reads:

- The original image you supply when you run it
- The new product you supply when you run it

Writes:

- A new image, from step 1 "Swap in the new product"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Original image | The shot that holds the product to replace | The step is marked vague and waits until one is attached. |
| New product | The product to swap in | The step is marked vague and waits until one is chosen. |

## Availability

Install now: every step builds something the engine supports today.
