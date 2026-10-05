---
name: cinemagraph
description: |
  Use when a user mentions "cinemagraph", "living photo", "subtle motion", "one element moves", or asks for a photo where only one element is animated. Still photo, one element moves.
arguments: []
intempt:
  id: cinemagraph
  version: 1.0.0
  slashCommand: /cinemagraph
  group: Creative
  shortDescription: "Generates a seamless-loop cinemagraph video where one element of a still photo animates while the rest stays frozen."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, cinemagraph, loop]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Generate cinemagraph"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Take a still image and animate only one element (steam, leaf, liquid) while everything else stays frozen."
      prompt: |
        Generate a cinemagraph from a still image.

        Camera stays fixed. Everything stays frozen except one element (gentle steam, single leaf in breeze, liquid pour). Subtle hypnotic seamless loop.

        Pipeline: image→video (camera-fixed, loop)
  outputs:
    - { name: video, type: video, cardinality: single, description: "Cinemagraph loop." }
---

# Cinemagraph

## Procedure

1. **Generate cinemagraph** [`generate_video`] — Animate one element in a still photo. → produces: video

## Notes

- Pipeline: fal.ai image→video (camera-fixed).
- Seamless loop — one element animates while the rest stays frozen.
