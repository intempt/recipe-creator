---
id: pack-shot
title: Studio product shots
slash_command: /pack-shot
group: Creative
owner: intempt
summary: Generates clean studio stills of one catalog product, in a background and lighting you pick.
description: >-
  Studio-clean product stills from one SKU.
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
    - product
    - pack-shot
steps:
  - id: s1
    title: Render the product
    summary: >-
      You pick a catalog product and a scene that sets background and lighting. Returns a kit of clean
      studio shots: front, three-quarter, detail and lifestyle inserts.
    builds: image
    description: |-
      Generate studio pack-shot images for the selected product.
      Inputs:
      - productId: catalog SKU to photograph
      - sceneId: background + lighting preset
      Pipeline: nano-banana-pro/edit
      Runner: pack-shot (custom)
      Produce a kit of clean studio shots (front, three-quarter, detail, lifestyle inserts) from the single catalog product using the chosen scene for background and lighting.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Generated pack-shot image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Studio product shots

Generates clean studio stills of one catalog product, in a background and lighting you pick.

## Steps

1. **Render the product** (builds image)

   You pick a catalog product and a scene that sets background and lighting. Returns a kit of clean studio shots: front, three-quarter, detail and lifestyle inserts.

## What you end up with

- **image** (image): Generated pack-shot image.

## Availability

Install now: every step builds something the engine supports today.
