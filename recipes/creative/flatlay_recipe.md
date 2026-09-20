---
name: flatlay
description: |
  Use when a user mentions "flatlay", "flat lay", "top-down composition", "overhead shot", or asks for a styled top-down product arrangement. Top-down styled composition.
arguments: []
intempt:
  id: flatlay
  version: 1.0.0
  slashCommand: /flatlay
  group: Creative
  title: 'Styled flatlay'
  shortDescription: 'Arranges your product in a top-down flatlay with complementary props styled around it.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, flatlay, top-down]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Style the flatlay'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Keeps the product in the same position and adds complementary props around it, holding the top-down angle and the lighting throughout.'
      prompt: |
        Generate a top-down flatlay composition.

        Keep the same product in the same position. Add complementary props arranged around it. Maintain top-down angle and lighting throughout.

        Pipeline: flux-pro/kontext (prop addition with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Flatlay composition." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Styled flatlay

Arranges your product in a top-down flatlay with complementary props styled around it.

## What it does

1. **Style the flatlay** (`generate_image`)

   Keeps the product in the same position and adds complementary props around it, holding the top-down angle and the lighting throughout.

## What you end up with

- **image** (image): Flatlay composition.
