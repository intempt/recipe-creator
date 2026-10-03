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
inputs:
  - input: Ad image
    what_the_installer_supplies: The existing ad to vary
    if_missing: The step is marked vague and waits until one is attached.
  - input: Dimensions to vary
    what_the_installer_supplies: Any of headline, palette, background, model, call to action and aspect
      ratio
    if_missing: All six are varied, one image each.
does_not_claim:
  - The new headline, palette, background, model, call to action and aspect ratio in each variant are
    chosen when the step runs.
touches:
  reads:
    - The ad image you supply when you run it
    - The dimensions to vary you supply when you run it
  writes:
    - A new image, from step 1 "Fan out the variants"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Fan out the variants
    summary: >-
      You upload an existing ad and pick which dimensions to vary. Returns six variants covering headline,
      palette, background, model, CTA and aspect ratio, with one focused change each.
    builds: image
    description: |-
      Generate six images from the ad image attached to this run.
      Each image changes exactly one thing and keeps everything else from the original ad:
      - one with a new headline
      - one with a new colour palette
      - one with a new background
      - one with a different model
      - one with a new call to action
      - one at a different aspect ratio
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

## What this recipe touches

Reads:

- The ad image you supply when you run it
- The dimensions to vary you supply when you run it

Writes:

- A new image, from step 1 "Fan out the variants"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Ad image | The existing ad to vary | The step is marked vague and waits until one is attached. |
| Dimensions to vary | Any of headline, palette, background, model, call to action and aspect ratio | All six are varied, one image each. |

## What this recipe does not claim

- The new headline, palette, background, model, call to action and aspect ratio in each variant are chosen when the step runs.

## Availability

Install now: every step builds something the engine supports today.
