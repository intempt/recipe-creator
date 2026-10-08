---
id: upscale
title: Image upscale
slash_command: /upscale
group: Creative
owner: intempt
curator: aurobind
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
  industry:
    - b2b-saas
    - ecommerce
    - media
    - social
  vertical: []
  complexity: quick
  executionMode: oneshot
  tags:
    - image
    - upscale
    - enhance
inputs:
  - input: Image
    what_the_installer_supplies: The image to enlarge
    if_missing: The step is marked vague and waits until one is attached.
touches:
  reads:
    - The image you supply when you run it
  writes:
    - A new image, from step 1 "Upscale to 4x"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Upscale to 4x
    summary: >-
      Enhances detail only, at four times the resolution. Composition, colours and subject are unchanged
      and the subject is not re-rendered.
    builds: image
    description: |-
      Upscale the image attached to this run to 4 times its width and height.
      Enhance detail only: keep the composition, colours and subject the same, and do not re-render the subject.
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

## What this recipe touches

Reads:

- The image you supply when you run it

Writes:

- A new image, from step 1 "Upscale to 4x"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Image | The image to enlarge | The step is marked vague and waits until one is attached. |

## Availability

Install now: every step builds something the engine supports today.
