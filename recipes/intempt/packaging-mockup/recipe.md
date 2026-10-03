---
id: packaging-mockup
title: Label wrapped on a package
slash_command: /packaging-mockup
group: Creative
owner: intempt
summary: Wraps your flat label artwork photorealistically around a 3D can, bottle or box, with the label
  content unchanged.
description: >-
  Flat label to wrapped on 3D pack.
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
    - packaging
    - mockup
    - label
steps:
  - id: s1
    title: Wrap the label
    summary: >-
      Takes the same label artwork, wordmark and layout and wraps it around a 3D package on the same backdrop.
      Nothing on the label is redrawn.
    builds: image
    description: |-
      Wrap flat label artwork onto a 3D package.
      Take the SAME label artwork (identical wordmark, identical layout) and wrap it photorealistically around a 3D package on the same backdrop. Label content preserved exactly.
      Pipeline: flux-pro/kontext (label wrapping with identity lock)
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Packaging mockup image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Label wrapped on a package

Wraps your flat label artwork photorealistically around a 3D can, bottle or box, with the label content unchanged.

## Steps

1. **Wrap the label** (builds image)

   Takes the same label artwork, wordmark and layout and wraps it around a 3D package on the same backdrop. Nothing on the label is redrawn.

## What you end up with

- **image** (image): Packaging mockup image.

## Availability

Install now: every step builds something the engine supports today.
