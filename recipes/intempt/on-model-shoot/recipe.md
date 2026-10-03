---
id: on-model-shoot
title: On-model product shot
slash_command: /on-model
group: Creative
owner: intempt
summary: Puts your identity-locked avatar in a scene wearing or holding a catalog product, for lifestyle
  product photography.
description: >-
  Avatar wearing or holding your product in a scene.
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
    - avatar
    - on-model
steps:
  - id: s1
    title: Compose the on-model shot
    summary: >-
      Combines a catalog product, an avatar, a scene and optional pose references. The avatar keeps the
      same identity across every generation.
    builds: image
    description: |-
      Generate an on-model lifestyle product photo.
      Inputs:
      - productId: catalog SKU
      - modelId: identity-locked Avatar
      - sceneId: background + lighting
      - poseIds (optional): pose references
      Pipeline: nano-banana-pro/edit with Avatar references
      Runner: on-model (custom)
      Produce a lifestyle shot with the identity-locked Avatar wearing or holding the product in the chosen scene. The Avatar's identity must remain consistent across generations.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: On-model lifestyle shot.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# On-model product shot

Puts your identity-locked avatar in a scene wearing or holding a catalog product, for lifestyle product photography.

## Steps

1. **Compose the on-model shot** (builds image)

   Combines a catalog product, an avatar, a scene and optional pose references. The avatar keeps the same identity across every generation.

## What you end up with

- **image** (image): On-model lifestyle shot.

## Availability

Install now: every step builds something the engine supports today.
