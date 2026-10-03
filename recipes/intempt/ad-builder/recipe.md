---
id: ad-builder
title: Branded ad from a product
slash_command: /ad-builder
group: Creative
owner: intempt
summary: Turns a catalog product and a headline into a finished ad laid out in your Brand Kit colours,
  fonts and layout.
description: >-
  One-click on-brand ad from product + concept.
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
    - ad
    - brand
steps:
  - id: s1
    title: Build the ad
    summary: >-
      Combines the product, your headline concept and a Brand Kit ad recipe, so colours, fonts and layout
      come from your design system. The output is a finished ad ready to run.
    builds: image
    description: |-
      Build a branded ad image.
      Inputs:
      - concept: headline or creative concept (rich text)
      - productId: catalog product
      - adRecipeId: Brand Kit Ad Recipe for colors, fonts, layout
      Pipeline: restyle to nano-banana-pro/edit with Brand Kit Ad Recipe composition
      Brand colours, fonts and layout flow from the design system. Produce a finished ad ready for deployment.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Finished ad image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Branded ad from a product

Turns a catalog product and a headline into a finished ad laid out in your Brand Kit colours, fonts and layout.

## Steps

1. **Build the ad** (builds image)

   Combines the product, your headline concept and a Brand Kit ad recipe, so colours, fonts and layout come from your design system. The output is a finished ad ready to run.

## What you end up with

- **image** (image): Finished ad image.

## Availability

Install now: every step builds something the engine supports today.
