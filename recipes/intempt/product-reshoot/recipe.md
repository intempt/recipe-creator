---
id: product-reshoot
title: Product relight
slash_command: /product-reshoot
group: Creative
owner: intempt
summary: Re-lights a product photo you already have, using a setting, lighting direction and camera angle
  that you choose.
description: >-
  Re-light any product without booking a studio.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  complexity: standard
  executionMode: oneshot
  tags:
    - image
    - product
    - lighting
inputs:
  - input: Product photo
    what_the_installer_supplies: The product photo to relight
    if_missing: The step is marked vague and waits until one is attached.
  - input: Setting, lighting and angle
    what_the_installer_supplies: The environment, the lighting direction and the camera angle
    if_missing: The step is marked vague and waits until one is chosen.
touches:
  reads:
    - The product photo you supply when you run it
    - The setting, lighting and angle you supply when you run it
  writes:
    - A new image, from step 1 "Relight the product"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Relight the product
    summary: >-
      You upload a product photo and pick the setting, lighting and angle. The shot is relit with physically
      accurate light falloff and the product itself is unchanged.
    builds: image
    description: |-
      Edit the product photo attached to this run.
      Relight it with physically accurate light falloff, using the setting, lighting direction and camera angle chosen for this run.
      Do not change the product itself.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Re-lit product image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product relight

Re-lights a product photo you already have, using a setting, lighting direction and camera angle that you choose.

## Steps

1. **Relight the product** (builds image)

   You upload a product photo and pick the setting, lighting and angle. The shot is relit with physically accurate light falloff and the product itself is unchanged.

## What you end up with

- **image** (image): Re-lit product image.

## What this recipe touches

Reads:

- The product photo you supply when you run it
- The setting, lighting and angle you supply when you run it

Writes:

- A new image, from step 1 "Relight the product"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Product photo | The product photo to relight | The step is marked vague and waits until one is attached. |
| Setting, lighting and angle | The environment, the lighting direction and the camera angle | The step is marked vague and waits until one is chosen. |

## Availability

Install now: every step builds something the engine supports today.
