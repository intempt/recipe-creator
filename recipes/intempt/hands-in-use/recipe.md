---
id: hands-in-use
title: Hands using the product
slash_command: /hands-in-use
group: Creative
owner: intempt
summary: Shows hands pouring, applying or holding your product, with no face in frame and small props
  added around it.
description: >-
  Pouring, applying, holding: no face.
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
    - hands
    - in-use
steps:
  - id: s1
    title: Shoot hands with the product
    summary: >-
      Keeps the same hands, product and surface, and adds small props such as a napkin, sprig or utensil.
      Lighting and angle are unchanged and no face is visible.
    builds: image
    description: |-
      Generate a hands-in-use product shot.
      Same hands, product, and surface. Add small complementary props (napkin, sprig, utensil). Identical lighting and angle. No face visible: only hands interacting with the product.
      Pipeline: flux-pro/kontext (prop addition with identity lock)
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Hands-in-use product image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Hands using the product

Shows hands pouring, applying or holding your product, with no face in frame and small props added around it.

## Steps

1. **Shoot hands with the product** (builds image)

   Keeps the same hands, product and surface, and adds small props such as a napkin, sprig or utensil. Lighting and angle are unchanged and no face is visible.

## What you end up with

- **image** (image): Hands-in-use product image.

## Availability

Install now: every step builds something the engine supports today.
