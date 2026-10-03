---
id: interior-staging
title: Virtual interior staging
slash_command: /interior-staging
group: Creative
owner: intempt
summary: Furnishes a photo of an empty room, leaving the walls, floor, windows and daylight exactly as
  they were shot.
description: >-
  Empty room, finished room.
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
    - interior
    - staging
steps:
  - id: s1
    title: Furnish the empty room
    summary: >-
      Adds furniture, a coffee table, a vase, a floor lamp and other staging suited to the space. Room
      geometry, walls, flooring, windows and daylight stay unchanged.
    builds: image
    description: |-
      Stage an empty room with furniture and decor.
      Keep the room geometry, walls, flooring, windows, and daylight unchanged. Add furniture, a coffee table, vase, floor lamp, and other staging elements appropriate to the space.
      Pipeline: flux-pro/kontext (scene augmentation)
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Staged interior image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Virtual interior staging

Furnishes a photo of an empty room, leaving the walls, floor, windows and daylight exactly as they were shot.

## Steps

1. **Furnish the empty room** (builds image)

   Adds furniture, a coffee table, a vase, a floor lamp and other staging suited to the space. Room geometry, walls, flooring, windows and daylight stay unchanged.

## What you end up with

- **image** (image): Staged interior image.

## Availability

Install now: every step builds something the engine supports today.
