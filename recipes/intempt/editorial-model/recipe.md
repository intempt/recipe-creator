---
id: editorial-model
title: Editorial lookbook shot
slash_command: /editorial-model
group: Creative
owner: intempt
summary: Produces a full-body editorial fashion photo of an AI model on location, then varies the lighting
  while holding pose and framing.
description: >-
  Full-body model, on location.
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
    - editorial
    - fashion
    - model
steps:
  - id: s1
    title: Relight the lookbook shot
    summary: >-
      Keeps the same model, outfit, pose, street and framing, and changes only the lighting, for example
      golden hour with long raking shadows.
    builds: image
    description: |-
      Generate an editorial lookbook shot.
      Full-body AI model in the outfit, on location. Keep the same model identity, outfit, pose, and street. Change only the lighting (e.g., golden hour with long raking shadows). Identical framing.
      Pipeline: flux-pro/kontext (lighting variation with identity lock)
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Editorial lookbook image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Editorial lookbook shot

Produces a full-body editorial fashion photo of an AI model on location, then varies the lighting while holding pose and framing.

## Steps

1. **Relight the lookbook shot** (builds image)

   Keeps the same model, outfit, pose, street and framing, and changes only the lighting, for example golden hour with long raking shadows.

## What you end up with

- **image** (image): Editorial lookbook image.

## Availability

Install now: every step builds something the engine supports today.
