---
id: beauty-close-up
title: Branded beauty close-up
slash_command: /beauty-close-up
group: Creative
owner: intempt
summary: Puts your brand wordmark and cap styling onto the product in a beauty close-up, leaving the model,
  hands and framing untouched.
description: >-
  Plain bottle to branded bottle close-up.
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
    - beauty
    - skincare
inputs:
  - input: Beauty close-up
    what_the_installer_supplies: A close-up photo of a model with the product
    if_missing: The step is marked vague and waits until one is attached.
touches:
  reads:
    - The beauty close-up you supply when you run it
  writes:
    - A new image, from step 1 "Brand the product in frame"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Brand the product in frame
    summary: >-
      Keeps the same model, skin, hand position, bottle and composition. The only change is the brand
      wordmark and cap styling on the product.
    builds: image
    description: |-
      Edit the beauty close-up image attached to this run.
      Apply your brand wordmark and cap styling to the product in the shot.
      Keep the model, skin, hand position, bottle shape and composition exactly as they are.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Branded beauty close-up.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Branded beauty close-up

Puts your brand wordmark and cap styling onto the product in a beauty close-up, leaving the model, hands and framing untouched.

## Steps

1. **Brand the product in frame** (builds image)

   Keeps the same model, skin, hand position, bottle and composition. The only change is the brand wordmark and cap styling on the product.

## What you end up with

- **image** (image): Branded beauty close-up.

## What this recipe touches

Reads:

- The beauty close-up you supply when you run it

Writes:

- A new image, from step 1 "Brand the product in frame"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Beauty close-up | A close-up photo of a model with the product | The step is marked vague and waits until one is attached. |

## Availability

Install now: every step builds something the engine supports today.
