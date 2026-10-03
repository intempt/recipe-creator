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
steps:
  - id: s1
    title: Brand the product in frame
    summary: >-
      Keeps the same model, skin, hand position, bottle and composition. The only change is the brand
      wordmark and cap styling on the product.
    builds: image
    description: |-
      Generate a beauty close-up with branded product.
      Keep the same model, skin, hand position, and bottle. Only change: apply the brand wordmark and cap styling to the product. Composition unchanged.
      Pipeline: flux-pro/kontext (identity-locked branding)
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

## Availability

Install now: every step builds something the engine supports today.
