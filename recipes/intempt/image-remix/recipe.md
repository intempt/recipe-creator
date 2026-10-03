---
id: image-remix
title: Reference-anchored remix
slash_command: /image-remix
group: Creative
owner: intempt
summary: Pin up to four reference images with a weight on each, and get back variations anchored to them
  (four by default).
description: >-
  Reference-anchored variations from your pinboard.
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
    - remix
    - reference
steps:
  - id: s1
    title: Pin references and fan out
    summary: >-
      You pin one to four references (a canvas snapshot, scene, avatar or upload) and set each to Light,
      Medium or Strong. The weight decides how strongly that reference pulls the output.
    builds: image
    description: |-
      Generate image variations from reference pins.
      Inputs:
      - references: 1: 4 reference images (canvas snapshot, scene, avatar, or upload) each with weight (Light/Medium/Strong)
      - fanout: number of variations to generate (default: 4)
      Pipeline: nano-banana-pro with reference_images[] and per-weight prompt directives
      Runner: image-remix (custom)
      Fan out on-brand variations anchored to the reference images. Each reference's weight controls how strongly it influences the output.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Remixed image variations.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Reference-anchored remix

Pin up to four reference images with a weight on each, and get back variations anchored to them (four by default).

## Steps

1. **Pin references and fan out** (builds image)

   You pin one to four references (a canvas snapshot, scene, avatar or upload) and set each to Light, Medium or Strong. The weight decides how strongly that reference pulls the output.

## What you end up with

- **image** (image): Remixed image variations.

## Availability

Install now: every step builds something the engine supports today.
