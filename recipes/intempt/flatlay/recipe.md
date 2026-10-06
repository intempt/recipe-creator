---
id: flatlay
title: Styled flatlay
slash_command: /flatlay
group: Creative
owner: intempt
curator: aurobind
summary: Arranges your product in a top-down flatlay with complementary props styled around it.
description: >-
  Top-down styled composition.
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
    - flatlay
    - top-down
inputs:
  - input: Flatlay image
    what_the_installer_supplies: A top-down photo of the product
    if_missing: The step is marked vague and waits until one is attached.
does_not_claim:
  - Which props are added is decided when the step runs.
touches:
  reads:
    - The flatlay image you supply when you run it
  writes:
    - A new image, from step 1 "Style the flatlay"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Style the flatlay
    summary: >-
      Keeps the product in the same position and adds complementary props around it, holding the top-down
      angle and the lighting throughout.
    builds: image
    description: |-
      Edit the top-down flatlay product image attached to this run.
      Add complementary props arranged around the product.
      Keep the product in the same position, and keep the top-down angle and the lighting unchanged.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Flatlay composition.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Styled flatlay

Arranges your product in a top-down flatlay with complementary props styled around it.

## Steps

1. **Style the flatlay** (builds image)

   Keeps the product in the same position and adds complementary props around it, holding the top-down angle and the lighting throughout.

## What you end up with

- **image** (image): Flatlay composition.

## What this recipe touches

Reads:

- The flatlay image you supply when you run it

Writes:

- A new image, from step 1 "Style the flatlay"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Flatlay image | A top-down photo of the product | The step is marked vague and waits until one is attached. |

## What this recipe does not claim

- Which props are added is decided when the step runs.

## Availability

Install now: every step builds something the engine supports today.
