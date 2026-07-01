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
  shortDescription: "Avatar wearing or holding your product in a scene."
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
      title: "Compose on-model shot"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Combine an Avatar with a catalog product, a Scene, and optional Poses to generate lifestyle product photography."
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

# On-Model Photoshoot

## Procedure

1. **Compose on-model shot** [`generate_image`] — Combine an Avatar with a catalog product, a Scene, and optional Poses to generate lifestyle product photography. → produces: image

   ```text
   Generate an on-model lifestyle product photo.

   Inputs:
   - productId: catalog SKU
   - modelId: identity-locked Avatar
   - sceneId: background + lighting
   - poseIds (optional): pose references

   Pipeline: nano-banana-pro/edit with Avatar references
   Runner: on-model (custom)
   ```

## Notes

- Uses the `on-model` custom runner in the content builder.
- fal.ai pipeline: nano-banana-pro/edit with Avatar reference images.
- Corresponds to the `on-model` tile on the Design Home page.
