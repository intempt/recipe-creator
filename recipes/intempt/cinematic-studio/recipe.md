---
id: cinematic-studio
title: Cinematic look board
slash_command: /cinematic-studio
group: Creative
owner: intempt
summary: Returns a board of nine cinematic looks from one image, so you can pick the grade you want.
description: >-
  Nine cinematic looks from one frame.
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
    - cinematic
steps:
  - id: s1
    title: Render nine cinematic looks
    summary: >-
      Renders nine looks from your image in parallel, each in the style of a different cinematographer.
      You promote the one you want to the canvas.
    builds: image
    description: |-
      Generate a 3×3 board of cinematic looks from one input image.
      Inputs:
      - image: source image (file upload)
      Pipeline: restyle × 9 (parallel)
      Produce 9 cinematic looks (Wes Anderson, Roger Deakins, Lubezki, Christopher Doyle, Bradford Young, etc.). The user picks one to promote to the canvas.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: 9 cinematic looks.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Cinematic look board

Returns a board of nine cinematic looks from one image, so you can pick the grade you want.

## Steps

1. **Render nine cinematic looks** (builds image)

   Renders nine looks from your image in parallel, each in the style of a different cinematographer. You promote the one you want to the canvas.

## What you end up with

- **image** (image): 9 cinematic looks.

## Availability

Install now: every step builds something the engine supports today.
