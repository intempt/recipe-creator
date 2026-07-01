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
  shortDescription: "Full-body model, on location."
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
      title: "Generate editorial lookbook shot"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Generate a full-body editorial fashion photo with an AI model on location, with lighting variation."
      prompt: |
        Generate an editorial lookbook shot.

        Full-body AI model in the outfit, on location. Keep the same model identity, outfit, pose, and street. Change only the lighting (e.g., golden hour with long raking shadows). Identical framing.

        Pipeline: flux-pro/kontext (lighting variation with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Editorial lookbook image." }
---

# Editorial Lookbook

## Procedure

1. **Generate editorial lookbook shot** [`generate_image`] — Full-body model on location with lighting variation. → produces: image

## Notes

- Pipeline: flux-pro/kontext.
- Model identity, outfit, and pose locked; lighting and mood vary.
