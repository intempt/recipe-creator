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
  shortDescription: "Generate a single top-down styled flatlay product image with complementary props around a fixed product."
  availability: available
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
      title: "Generate flatlay composition"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Take a product and arrange it in a styled top-down flatlay with complementary props."
      prompt: |
        Generate a top-down flatlay composition.

        Keep the same product in the same position. Add complementary props arranged around it. Maintain top-down angle and lighting throughout.

        Pipeline: flux-pro/kontext (prop addition with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Flatlay composition." }
---

# Flatlay

## Procedure

1. **Generate flatlay composition** [`generate_image`] — Styled top-down arrangement with props. → produces: image

## Notes

- Pipeline: flux-pro/kontext.
- Product position fixed; complementary props added around it.
