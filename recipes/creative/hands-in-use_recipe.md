---
name: hands-in-use
description: |
  Use when a user mentions "hands in use", "product in use", "pouring", "applying", "holding product", or asks for a product being used by hands without showing a face. Pouring, applying, holding: no face.
arguments: []
intempt:
  id: hands-in-use
  version: 1.0.0
  slashCommand: /hands-in-use
  group: Creative
  title: 'Hands using the product'
  shortDescription: 'Shows hands pouring, applying or holding your product, with no face in frame and small props added around it.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, hands, in-use]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Shoot hands with the product'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Keeps the same hands, product and surface, and adds small props such as a napkin, sprig or utensil. Lighting and angle are unchanged and no face is visible.'
      prompt: |
        Generate a hands-in-use product shot.

        Same hands, product, and surface. Add small complementary props (napkin, sprig, utensil). Identical lighting and angle. No face visible: only hands interacting with the product.

        Pipeline: flux-pro/kontext (prop addition with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Hands-in-use product image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Hands using the product

Shows hands pouring, applying or holding your product, with no face in frame and small props added around it.

## What it does

1. **Shoot hands with the product** (`generate_image`)

   Keeps the same hands, product and surface, and adds small props such as a napkin, sprig or utensil. Lighting and angle are unchanged and no face is visible.

## What you end up with

- **image** (image): Hands-in-use product image.
