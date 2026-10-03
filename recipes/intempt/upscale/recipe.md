---
id: upscale
title: Image upscale
slash_command: /upscale
group: Creative
owner: intempt
summary: Enlarges a soft or low-resolution image to four times the size with sharper detail and nothing
  re-rendered.
description: >-
  Soft input to razor-sharp output.
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
    - upscale
    - enhance
steps:
  - id: s1
    title: Upscale to 4x
    summary: >-
      Enhances detail only, at four times the resolution. Composition, colours and subject are unchanged
      and the subject is not re-rendered.
    builds: image
    description: |-
      Upscale the image to 4× resolution.
      Pure detail enhancement only. Same composition, same colors, same subject. Do not re-render or change the subject.
      Pipeline: fal-ai/clarity-upscaler, scale: 4
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Upscaled image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Image upscale

Enlarges a soft or low-resolution image to four times the size with sharper detail and nothing re-rendered.

## Steps

1. **Upscale to 4x** (builds image)

   Enhances detail only, at four times the resolution. Composition, colours and subject are unchanged and the subject is not re-rendered.

## What you end up with

- **image** (image): Upscaled image.

## Availability

Install now: every step builds something the engine supports today.
