---
name: product-in-motion
description: |
  Use when a user mentions "product in motion", "turntable", "360 spin", "product rotation", or asks for a product spinning/rotating video. Packshot → turntable spin.
arguments: []
intempt:
  id: product-in-motion
  version: 1.0.0
  slashCommand: /product-in-motion
  group: Creative
  shortDescription: 'Packshot to turntable spin.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, product, turntable, 360]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Generate turntable spin"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Take a product packshot and generate a slow elegant turntable rotation video."
      prompt: |
        Generate a product turntable spin video.

        Camera fixed. Slow elegant turntable rotation of the product, same backdrop. Luxury e-commerce 360° spin. No text, no logo.

        Pipeline: image→video (camera-fixed, turntable)
  outputs:
    - { name: video, type: video, cardinality: single, description: "Product turntable video." }
---

# Product in Motion

## Procedure

1. **Generate turntable spin** [`generate_video`] — Packshot → 360° turntable rotation. → produces: video

## Notes

- Pipeline: fal.ai image→video (camera-fixed).
- Luxury e-commerce style — slow, elegant rotation.
