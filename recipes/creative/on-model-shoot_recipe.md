---
name: on-model-shoot
description: |
  Use when a user mentions "on-model", "model photoshoot", "avatar wearing product", "try-on", or asks for lifestyle product photography with an AI model. Avatar wearing or holding your product in a scene.
arguments: []
intempt:
  id: on-model-shoot
  version: 1.0.0
  slashCommand: /on-model
  group: Creative
  title: 'On-model product shot'
  shortDescription: 'Puts your identity-locked avatar in a scene wearing or holding a catalog product, for lifestyle product photography.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, product, avatar, on-model]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Compose the on-model shot'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Combines a catalog product, an avatar, a scene and optional pose references. The avatar keeps the same identity across every generation.'
      prompt: |
        Generate an on-model lifestyle product photo.

        Inputs:
        - productId: catalog SKU
        - modelId: identity-locked Avatar
        - sceneId: background + lighting
        - poseIds (optional): pose references

        Pipeline: nano-banana-pro/edit with Avatar references
        Runner: on-model (custom)

        Produce a lifestyle shot with the identity-locked Avatar wearing or holding the product in the chosen scene. The Avatar's identity must remain consistent across generations.
  outputs:
    - { name: image, type: image, cardinality: single, description: "On-model lifestyle shot." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# On-model product shot

Puts your identity-locked avatar in a scene wearing or holding a catalog product, for lifestyle product photography.

## What it does

1. **Compose the on-model shot** (`generate_image`)

   Combines a catalog product, an avatar, a scene and optional pose references. The avatar keeps the same identity across every generation.

## What you end up with

- **image** (image): On-model lifestyle shot.
