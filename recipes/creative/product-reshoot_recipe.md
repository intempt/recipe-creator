---
name: product-reshoot
description: |
  Use when a user mentions "reshoot", "re-light", "product lighting", "studio lighting", or asks to re-photograph a product with different lighting. Re-light any product without booking a studio.
arguments: []
intempt:
  id: product-reshoot
  version: 1.0.0
  slashCommand: /product-reshoot
  group: Creative
  shortDescription: "Generate a single re-lit product image by applying specified studio lighting, setting, and angle while preserving product identity."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, product, lighting]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Re-light product"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Pick setting, lighting, and angle chips then re-shoot the product with controlled studio light."
      prompt: |
        Re-shoot a product image with new lighting.

        Inputs:
        - productImage: uploaded product photo
        - setting: environment preset
        - lighting: lighting direction/style
        - angle: camera angle

        Pipeline: iclight-v2 relight → optional nano-banana-pro/edit

        Re-light the product with physically-accurate light falloff. The product identity must remain unchanged.
  outputs:
    - { name: image, type: image, cardinality: single, description: "Re-lit product image." }
---

# Product Reshoot

## Procedure

1. **Re-light product** [`generate_image`] — Pick setting, lighting, and angle chips then re-shoot the product with controlled studio light. → produces: image

   ```text
   Inputs: productImage, setting, lighting, angle
   Pipeline: iclight-v2 relight
   ```

## Notes

- fal.ai pipeline: iclight-v2 for physically-accurate relighting.
- Product identity preserved — only lighting, angle, and environment change.
