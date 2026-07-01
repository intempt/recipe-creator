---
name: talking-avatar
description: |
  Use when a user mentions "talking avatar", "spokesperson video", "talking head", "avatar clip", or asks for a portrait that speaks. Portrait still → spokesperson clip.
arguments: []
intempt:
  id: talking-avatar
  version: 1.0.0
  slashCommand: /talking-avatar
  group: Creative
  shortDescription: "Portrait still → spokesperson clip."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, avatar, talking-head]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Animate portrait as spokesperson"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Take a portrait still and generate a 5s natural talking-head loop with subtle lip movement and eye contact."
      prompt: |
        Generate a talking avatar video from a portrait still.

        Camera fixed. 5s natural talking-head loop: subtle lip movement, gentle eye contact, single blink. Identity preserved exactly.

        Pipeline: image→video (camera-fixed, talking-head)
  outputs:
    - { name: video, type: video, cardinality: single, description: "Talking avatar clip." }
---

# Talking Avatar

## Procedure

1. **Animate portrait as spokesperson** [`generate_video`] — Portrait → 5s talking-head loop. → produces: video

## Notes

- Pipeline: fal.ai image→video (camera-fixed).
- Identity preserved; subtle lip movement and eye contact.
