---
name: ad-video
description: |
  Use when a user mentions "ad video", "video ad", "product spot", "cinematic ad", or asks for a video ad from a product still. Product still → cinematic spot.
arguments: []
intempt:
  id: ad-video
  version: 1.0.0
  slashCommand: /ad-video
  group: Creative
  shortDescription: "Product still → cinematic spot."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, ad, cinematic]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Generate ad video"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Take a product still and generate a cinematic 5-second ad spot with camera drift and ambient particles."
      prompt: |
        Generate a cinematic ad video from a product still.

        Seed on the product still. Produce a cinematic 5s product spot with smooth subtle camera drift, soft dust particles, same backdrop. No text, no logo overlay.

        Pipeline: image→video (kling/seedance)
  outputs:
    - { name: video, type: video, cardinality: single, description: "Cinematic ad video." }
---

# Ad Video

## Procedure

1. **Generate ad video** [`generate_video`] — Product still → cinematic 5s spot. → produces: video

## Notes

- Pipeline: fal.ai image→video (kling/seedance).
- Subtle camera drift and ambient particles for cinematic feel.
