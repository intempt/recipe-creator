---
id: product-shot-video
title: Product clip from a still
slash_command: /product-shot-video
group: Creative
owner: intempt
curator: aurobind
summary: >-
  Turn a static product image into a 5-second video clip with a 360 spin, dolly-in, or floating reveal.
description: >-
  Create a short product video from a static image.
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
  complexity: standard
  executionMode: oneshot
  tags:
    - video
    - product
    - i2v
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new video, from step 1 "Animate the product"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Animate the product
    summary: >-
      You pick a catalog product and a motion style: 360 rotation, dolly-in or floating reveal. Returns
      a 5 second clip, with the music bed on by default.
    builds: video
    description: |-
      Generate a product shot video from a static image.
      Inputs:
      - productId: catalog product
      - scene: motion style (360° rotation, dolly-in, floating reveal)
      - script (optional): additional direction
      - music: enable music bed (default: true)
      Pipeline: kling i2v + mmaudio-v2
      Produce a 5-second clip (360° rotation, dolly-in, or floating reveal) with optional music bed.
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Product shot video.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product clip from a still

Turn a static product image into a 5-second video clip with a 360 spin, dolly-in, or floating reveal.

## Steps

1. **Animate the product** (builds video)

   You pick a catalog product and a motion style: 360 rotation, dolly-in or floating reveal. Returns a 5 second clip, with the music bed on by default.

## What you end up with

- **video** (video): Product shot video.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new video, from step 1 "Animate the product"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build video.
