---
name: ad-builder
description: |
  Use when a user mentions "ad builder", "build an ad", "create ad", "branded ad", or asks for on-brand ad creation from product and concept. One-click on-brand ad from product + concept.
arguments: []
intempt:
  id: ad-builder
  version: 1.0.0
  slashCommand: /ad-builder
  group: Creative
  shortDescription: "Generate a finished on-brand ad image from a product SKU, headline concept, and Brand Kit ad recipe."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, ad, brand]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Build branded ad"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Combine a product, a headline concept, and a Brand Kit Ad Recipe to produce a finished ad."
      prompt: |
        Build a branded ad image.

        Inputs:
        - concept: headline or creative concept (rich text)
        - productId: catalog product
        - adRecipeId: Brand Kit Ad Recipe for colors, fonts, layout

        Pipeline: restyle → nano-banana-pro/edit with Brand Kit Ad Recipe composition

        Brand colours, fonts and layout flow from the design system. Produce a finished ad ready for deployment.
  outputs:
    - { name: image, type: image, cardinality: single, description: "Finished ad image." }
---

# Ad Builder

## Procedure

1. **Build branded ad** [`generate_image`] — Combine a product, a headline concept, and a Brand Kit Ad Recipe to produce a finished ad. → produces: image

   ```text
   Inputs: concept (headline), productId (SKU), adRecipeId (Brand Kit layout)
   Pipeline: restyle → nano-banana-pro/edit
   ```

## Notes

- fal.ai pipeline: restyle → nano-banana-pro/edit with Brand Kit Ad Recipe composition.
- Brand colours, fonts, and layout sourced from the project's design system.
