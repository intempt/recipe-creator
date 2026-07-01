---
name: product-shot-video
description: |
  Use when a user mentions "product video", "product clip", "SKU video", "product animation", or asks for a video from a static product image. Every SKU becomes a thumb-stopping clip.
arguments: []
intempt:
  id: product-shot-video
  version: 1.0.0
  slashCommand: /product-shot-video
  group: Creative
  shortDescription: "Every SKU becomes a thumb-stopping clip."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, product, i2v]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Animate product still"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Take a static product image and produce a 5-second clip with optional music bed."
      prompt: |
        Generate a product shot video from a static image.

        Inputs:
        - productId: catalog product
        - scene: motion style (360° rotation, dolly-in, floating reveal)
        - script (optional): additional direction
        - music: enable music bed (default: true)

        Pipeline: kling i2v + mmaudio-v2

        Produce a 5-second clip — 360° rotation, dolly-in, or floating reveal — with optional music bed.
  outputs:
    - { name: video, type: video, cardinality: single, description: "Product shot video." }
---

# Product Shot Video

## Procedure

1. **Animate product still** [`generate_video`] — Take a static product image and produce a 5-second clip. → produces: video

   ```text
   Inputs: productId, scene (motion style), script, music
   Pipeline: kling i2v + mmaudio-v2
   ```

## Notes

- fal.ai pipeline: kling i2v for image-to-video + mmaudio-v2 for music bed.
- Motion styles: 360° rotation, dolly-in, floating reveal.
