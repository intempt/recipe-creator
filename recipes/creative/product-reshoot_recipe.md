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
  title: 'Product relight'
  shortDescription: 'Re-lights a product photo you already have, using a setting, lighting direction and camera angle that you choose.'
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
      title: 'Relight the product'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'You upload a product photo and pick the setting, lighting and angle. The shot is relit with physically accurate light falloff and the product itself is unchanged.'
      prompt: |
        Re-shoot a product image with new lighting.

        Inputs:
        - productImage: uploaded product photo
        - setting: environment preset
        - lighting: lighting direction/style
        - angle: camera angle

        Pipeline: iclight-v2 relight to optional nano-banana-pro/edit

        Re-light the product with physically-accurate light falloff. The product identity must remain unchanged.
  outputs:
    - { name: image, type: image, cardinality: single, description: "Re-lit product image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product relight

Re-lights a product photo you already have, using a setting, lighting direction and camera angle that you choose.

## What it does

1. **Relight the product** (`generate_image`)

   You upload a product photo and pick the setting, lighting and angle. The shot is relit with physically accurate light falloff and the product itself is unchanged.

## What you end up with

- **image** (image): Re-lit product image.
