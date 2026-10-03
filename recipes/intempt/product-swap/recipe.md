---
id: product-swap
title: Product swap in a scene
slash_command: /product-swap
group: Creative
owner: intempt
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
steps:
  - id: s1
    title: Swap in the new product
    summary: >-
      Replaces only the product with the new SKU at identical size and position. Scene, lighting, shadow
      and backdrop are unchanged.
    builds: image
    description: |-
      Swap the product in an existing image.
      Keep the scene, lighting, shadow, and backdrop unchanged. Replace only the product with the new SKU, maintaining identical size and position.
      Pipeline: flux-pro/kontext (identity-locked swap)
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

## Availability

Install now: every step builds something the engine supports today.
