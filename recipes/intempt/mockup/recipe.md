---
id: mockup
title: Artwork on a mockup
slash_command: /mockup
group: Creative
owner: intempt
summary: Puts your artwork onto a t-shirt, mug, billboard or package with realistic lighting, perspective
  and material.
description: >-
  Apparel, print, packaging: mockup in one click.
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
    - mockup
steps:
  - id: s1
    title: Composite the artwork
    summary: >-
      You supply the artwork and pick a mockup scene. The artwork is composited on with realistic lighting,
      perspective warping and material-appropriate rendering.
    builds: image
    description: |-
      Generate a product mockup.
      Inputs:
      - artwork: artwork file (upload)
      - mockupScene: mockup scene preset (t-shirt, mug, billboard, packaging, etc.)
      Pipeline: restyle to nano-banana-pro/edit
      Composite the artwork onto the mockup scene with realistic lighting, perspective warping, and material-appropriate rendering.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Mockup image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Artwork on a mockup

Puts your artwork onto a t-shirt, mug, billboard or package with realistic lighting, perspective and material.

## Steps

1. **Composite the artwork** (builds image)

   You supply the artwork and pick a mockup scene. The artwork is composited on with realistic lighting, perspective warping and material-appropriate rendering.

## What you end up with

- **image** (image): Mockup image.

## Availability

Install now: every step builds something the engine supports today.
