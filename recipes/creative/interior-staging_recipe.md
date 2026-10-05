---
name: interior-staging
description: |
  Use when a user mentions "interior staging", "room staging", "virtual staging", "furniture placement", or asks to stage an empty room with furniture. Empty room, finished room.
arguments: []
intempt:
  id: interior-staging
  version: 1.0.0
  slashCommand: /interior-staging
  group: Creative
  shortDescription: "Generate a single virtual staging image that adds furniture and decor to an empty room while preserving its geometry and lighting."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, interior, staging]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Stage interior"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Take an empty room photo and add furniture, decor, and styling while preserving the room geometry and daylight."
      prompt: |
        Stage an empty room with furniture and decor.

        Keep the room geometry, walls, flooring, windows, and daylight unchanged. Add furniture, a coffee table, vase, floor lamp, and other staging elements appropriate to the space.

        Pipeline: flux-pro/kontext (scene augmentation)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Staged interior image." }
---

# Interior Staging

## Procedure

1. **Stage interior** [`generate_image`] — Add furniture and decor to an empty room. → produces: image

## Notes

- Pipeline: flux-pro/kontext for scene augmentation.
- Room geometry and lighting preserved; only furnishings added.
