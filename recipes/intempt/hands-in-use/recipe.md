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
inputs:
  - input: Hands-in-use image
    what_the_installer_supplies: A photo of hands holding or using the product
    if_missing: The step is marked vague and waits until one is attached.
touches:
  reads:
    - The hands-in-use image you supply when you run it
  writes:
    - A new image, from step 1 "Shoot hands with the product"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Shoot hands with the product
    summary: >-
      Keeps the same hands, product and surface, and adds small props such as a napkin, sprig or utensil.
      Lighting and angle are unchanged and no face is visible.
    builds: image
    description: |-
      Edit the hands-in-use product image attached to this run.
      Add three small props around the product: a napkin, a sprig and a utensil.
      Keep the same hands, product and surface, and keep the lighting and the camera angle identical.
      No face may be visible: only hands interacting with the product.
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

## What this recipe touches

Reads:

- The hands-in-use image you supply when you run it

Writes:

- A new image, from step 1 "Shoot hands with the product"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Hands-in-use image | A photo of hands holding or using the product | The step is marked vague and waits until one is attached. |

## Availability

Install now: every step builds something the engine supports today.
