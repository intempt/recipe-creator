---
name: editorial-model
description: |
  Use when a user mentions "editorial lookbook", "fashion editorial", "lookbook", "model on location", or asks for full-body editorial fashion photography. Full-body model, on location.
arguments: []
intempt:
  id: editorial-model
  version: 1.0.0
  slashCommand: /editorial-model
  group: Creative
  title: 'Editorial lookbook shot'
  shortDescription: 'Produces a full-body editorial fashion photo of an AI model on location, then varies the lighting while holding pose and framing.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, editorial, fashion, model]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Relight the lookbook shot'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Keeps the same model, outfit, pose, street and framing, and changes only the lighting, for example golden hour with long raking shadows.'
      prompt: |
        Generate an editorial lookbook shot.

        Full-body AI model in the outfit, on location. Keep the same model identity, outfit, pose, and street. Change only the lighting (e.g., golden hour with long raking shadows). Identical framing.

        Pipeline: flux-pro/kontext (lighting variation with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Editorial lookbook image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Editorial lookbook shot

Produces a full-body editorial fashion photo of an AI model on location, then varies the lighting while holding pose and framing.

## What it does

1. **Relight the lookbook shot** (`generate_image`)

   Keeps the same model, outfit, pose, street and framing, and changes only the lighting, for example golden hour with long raking shadows.

## What you end up with

- **image** (image): Editorial lookbook image.
