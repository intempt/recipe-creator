---
name: upscale
description: |
  Use when a user mentions "upscale", "enhance resolution", "sharpen", "super resolution", "increase resolution", or asks to improve the resolution of an image. Soft input to razor-sharp output.
arguments: []
intempt:
  id: upscale
  version: 1.0.0
  slashCommand: /upscale
  group: Creative
  title: 'Image upscale'
  shortDescription: 'Enlarges a soft or low-resolution image to four times the size with sharper detail and nothing re-rendered.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, upscale, enhance]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Upscale to 4x'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Enhances detail only, at four times the resolution. Composition, colours and subject are unchanged and the subject is not re-rendered.'
      prompt: |
        Upscale the image to 4× resolution.

        Pure detail enhancement only. Same composition, same colors, same subject. Do not re-render or change the subject.

        Pipeline: fal-ai/clarity-upscaler, scale: 4
  outputs:
    - { name: image, type: image, cardinality: single, description: "Upscaled image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Image upscale

Enlarges a soft or low-resolution image to four times the size with sharper detail and nothing re-rendered.

## What it does

1. **Upscale to 4x** (`generate_image`)

   Enhances detail only, at four times the resolution. Composition, colours and subject are unchanged and the subject is not re-rendered.

## What you end up with

- **image** (image): Upscaled image.
