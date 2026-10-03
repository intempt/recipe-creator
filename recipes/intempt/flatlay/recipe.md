---
id: flatlay
title: Styled flatlay
slash_command: /flatlay
group: Creative
owner: intempt
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
  complexity: quick
  executionMode: oneshot
  tags:
    - image
    - flatlay
    - top-down
steps:
  - id: s1
    title: Style the flatlay
    summary: >-
      Keeps the product in the same position and adds complementary props around it, holding the top-down
      angle and the lighting throughout.
    builds: image
    description: |-
      Generate a top-down flatlay composition.
      Keep the same product in the same position. Add complementary props arranged around it. Maintain top-down angle and lighting throughout.
      Pipeline: flux-pro/kontext (prop addition with identity lock)
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

## Availability

Install now: every step builds something the engine supports today.
