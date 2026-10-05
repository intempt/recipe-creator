---
name: ugc-selfie-video
description: |
  Use when a user mentions "UGC video", "selfie video", "candid video clip", "handheld video", or asks for an authentic selfie-style video. Handheld selfie still → candid clip.
arguments: []
intempt:
  id: ugc-selfie-video
  version: 1.0.0
  slashCommand: /ugc-selfie-video
  group: Creative
  shortDescription: "Generate a 5-second handheld selfie-style UGC video from a user-provided still image."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, ugc, selfie, candid]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Generate UGC selfie video"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Take a handheld selfie still and generate a 5s candid video clip with subtle head turn and natural smile."
      prompt: |
        Generate a UGC selfie video from a still.

        Seed on the selfie still. 5s candid handheld selfie clip: subtle head turn, natural smile, real kitchen light, slight handheld drift. Authentic, not glamour.

        Pipeline: image→video (candid motion)
  outputs:
    - { name: video, type: video, cardinality: single, description: "UGC selfie video clip." }
---

# UGC Selfie Video

## Procedure

1. **Generate UGC selfie video** [`generate_video`] — Selfie still → candid 5s clip. → produces: video

## Notes

- Pipeline: fal.ai image→video.
- Authentic handheld feel — natural motion, not polished.
