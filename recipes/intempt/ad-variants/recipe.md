---
id: ad-variants
title: Six variants of one ad
slash_command: /ad-variants
group: Creative
owner: intempt
summary: Takes an ad you already have and returns six variants, one for each dimension you choose to vary.
description: >-
  One ad in, six tested variants out.
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
    - variants
steps:
  - id: s1
    title: Fan out the variants
    summary: >-
      You upload an existing ad and pick which dimensions to vary. Returns six variants covering headline,
      palette, background, model, CTA and aspect ratio, with one focused change each.
    builds: image
    description: |-
      Generate ad variants from an existing ad.
      Inputs:
      - adImage: existing ad image (file upload)
      - swaps: dimensions to vary (headline, palette, background, model, CTA, aspect)
      Pipeline: restyle × N (one per swap dimension)
      Fan out one focused variation per swap dimension. Six variants total covering headline, palette, background, model, CTA, and aspect ratio.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: 6 ad variants.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Six variants of one ad

Takes an ad you already have and returns six variants, one for each dimension you choose to vary.

## Steps

1. **Fan out the variants** (builds image)

   You upload an existing ad and pick which dimensions to vary. Returns six variants covering headline, palette, background, model, CTA and aspect ratio, with one focused change each.

## What you end up with

- **image** (image): 6 ad variants.

## Availability

Install now: every step builds something the engine supports today.
