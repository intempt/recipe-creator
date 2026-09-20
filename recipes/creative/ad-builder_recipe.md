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
  title: 'Branded ad from a product'
  shortDescription: 'Turns a catalog product and a headline into a finished ad laid out in your Brand Kit colours, fonts and layout.'
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
      title: 'Build the ad'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Combines the product, your headline concept and a Brand Kit ad recipe, so colours, fonts and layout come from your design system. The output is a finished ad ready to run.'
      prompt: |
        Build a branded ad image.

        Inputs:
        - concept: headline or creative concept (rich text)
        - productId: catalog product
        - adRecipeId: Brand Kit Ad Recipe for colors, fonts, layout

        Pipeline: restyle to nano-banana-pro/edit with Brand Kit Ad Recipe composition

        Brand colours, fonts and layout flow from the design system. Produce a finished ad ready for deployment.
  outputs:
    - { name: image, type: image, cardinality: single, description: "Finished ad image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Branded ad from a product

Turns a catalog product and a headline into a finished ad laid out in your Brand Kit colours, fonts and layout.

## What it does

1. **Build the ad** (`generate_image`)

   Combines the product, your headline concept and a Brand Kit ad recipe, so colours, fonts and layout come from your design system. The output is a finished ad ready to run.

## What you end up with

- **image** (image): Finished ad image.
