---
name: ad-variants
description: |
  Use when a user mentions "ad variants", "ad variations", "swap headline", "swap palette", "A/B ad creative", or asks for multiple versions of an existing ad. One ad in, six tested variants out.
arguments: []
intempt:
  id: ad-variants
  version: 1.0.0
  slashCommand: /ad-variants
  group: Creative
  title: 'Six variants of one ad'
  shortDescription: 'Takes an ad you already have and returns six variants, one for each dimension you choose to vary.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, ad, variants]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Fan out the variants'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'You upload an existing ad and pick which dimensions to vary. Returns six variants covering headline, palette, background, model, CTA and aspect ratio, with one focused change each.'
      prompt: |
        Generate ad variants from an existing ad.

        Inputs:
        - adImage: existing ad image (file upload)
        - swaps: dimensions to vary (headline, palette, background, model, CTA, aspect)

        Pipeline: restyle × N (one per swap dimension)

        Fan out one focused variation per swap dimension. Six variants total covering headline, palette, background, model, CTA, and aspect ratio.
  outputs:
    - { name: image, type: image, cardinality: list, description: "6 ad variants." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Six variants of one ad

Takes an ad you already have and returns six variants, one for each dimension you choose to vary.

## What it does

1. **Fan out the variants** (`generate_image`)

   You upload an existing ad and pick which dimensions to vary. Returns six variants covering headline, palette, background, model, CTA and aspect ratio, with one focused change each.

## What you end up with

- **image** (image): 6 ad variants.
