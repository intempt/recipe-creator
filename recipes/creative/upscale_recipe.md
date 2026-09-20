---
name: upscale
description: |
  Use when a user mentions "upscale", "enhance resolution", "sharpen", "super resolution", "increase resolution", or asks to improve the resolution of an image. Soft input → razor-sharp output.
arguments: []
intempt:
  id: upscale
  version: 1.0.0
  slashCommand: /upscale
  group: Creative
  shortDescription: 'Soft input to razor-sharp output.'
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
      title: "Upscale image"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Upscale a low-resolution image to 4× with pure detail enhancement — no re-rendering or identity changes."
      prompt: |
        Upscale the image to 4× resolution.

        Pure detail enhancement only. Same composition, same colors, same subject. Do not re-render or change the subject.

        Pipeline: fal-ai/clarity-upscaler, scale: 4
  outputs:
    - { name: image, type: image, cardinality: single, description: "Upscaled image." }
---

# Upscale

## Procedure

1. **Upscale image** [`generate_image`] — 4× resolution enhancement, no re-rendering. → produces: image

## Notes

- Pipeline: fal-ai/clarity-upscaler at 4× scale.
- Pure enhancement — no content or identity changes.
