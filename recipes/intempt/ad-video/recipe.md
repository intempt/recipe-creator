---
id: ad-video
title: Cinematic ad spot
slash_command: /ad-video
group: Creative
owner: intempt
summary: Turns one product still into a 5 second cinematic spot with slow camera drift and soft particles,
  no text or logo.
description: >-
  Product still to cinematic spot.
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
    - video
    - ad
    - cinematic
steps:
  - id: s1
    title: Animate the product still
    summary: >-
      Uses the product still as the seed and produces a 5 second spot with smooth camera drift, soft dust
      particles and the same backdrop. No text or logo overlay is added.
    builds: video
    description: |-
      Generate a cinematic ad video from a product still.
      Seed on the product still. Produce a cinematic 5s product spot with smooth subtle camera drift, soft dust particles, same backdrop. No text, no logo overlay.
      Pipeline: image to video (kling/seedance)
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Cinematic ad video.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Cinematic ad spot

Turns one product still into a 5 second cinematic spot with slow camera drift and soft particles, no text or logo.

## Steps

1. **Animate the product still** (builds video)

   Uses the product still as the seed and produces a 5 second spot with smooth camera drift, soft dust particles and the same backdrop. No text or logo overlay is added.

## What you end up with

- **video** (video): Cinematic ad video.

## Availability

Coming soon: waiting on the engine to build video.
