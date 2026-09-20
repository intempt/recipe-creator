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
  title: 'Virtual interior staging'
  shortDescription: 'Furnishes a photo of an empty room, leaving the walls, floor, windows and daylight exactly as they were shot.'
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
      title: 'Furnish the empty room'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Adds furniture, a coffee table, a vase, a floor lamp and other staging suited to the space. Room geometry, walls, flooring, windows and daylight stay unchanged.'
      prompt: |
        Stage an empty room with furniture and decor.

        Keep the room geometry, walls, flooring, windows, and daylight unchanged. Add furniture, a coffee table, vase, floor lamp, and other staging elements appropriate to the space.

        Pipeline: flux-pro/kontext (scene augmentation)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Staged interior image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Virtual interior staging

Furnishes a photo of an empty room, leaving the walls, floor, windows and daylight exactly as they were shot.

## What it does

1. **Furnish the empty room** (`generate_image`)

   Adds furniture, a coffee table, a vase, a floor lamp and other staging suited to the space. Room geometry, walls, flooring, windows and daylight stay unchanged.

## What you end up with

- **image** (image): Staged interior image.
