---
id: accessory-try-on
title: Accessory on a model
slash_command: /accessory-try-on
group: Creative
owner: intempt
summary: Takes a packshot of eyewear, jewelry or a watch and shows it worn by an AI model, with the accessory
  itself unchanged.
description: >-
  Eyewear, jewelry, watches on model.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  complexity: quick
  executionMode: oneshot
  tags:
    - image
    - accessory
    - try-on
steps:
  - id: s1
    title: Put the accessory on a model
    summary: >-
      Places the same accessory on an AI model, shoulders up, in soft window light against a neutral backdrop.
      The accessory itself is not redrawn.
    builds: image
    description: |-
      Place the accessory on an AI model.
      Take the exact same accessory and place it on the face/wrist/body of an AI model, shoulders-up, candid, real skin. Soft window light, neutral backdrop. Accessory identity preserved exactly.
      Pipeline: flux-pro/kontext (accessory placement with identity lock)
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Accessory try-on image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accessory on a model

Takes a packshot of eyewear, jewelry or a watch and shows it worn by an AI model, with the accessory itself unchanged.

## Steps

1. **Put the accessory on a model** (builds image)

   Places the same accessory on an AI model, shoulders up, in soft window light against a neutral backdrop. The accessory itself is not redrawn.

## What you end up with

- **image** (image): Accessory try-on image.

## Availability

Install now: every step builds something the engine supports today.
