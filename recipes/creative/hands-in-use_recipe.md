---
name: hands-in-use
description: |
  Use when a user mentions "hands in use", "product in use", "pouring", "applying", "holding product", or asks for a product being used by hands without showing a face. Pouring, applying, holding — no face.
arguments: []
intempt:
  id: hands-in-use
  version: 1.0.0
  slashCommand: /hands-in-use
  group: Creative
  shortDescription: "Pouring, applying, holding — no face."
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
      title: "Generate hands-in-use shot"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Show hands interacting with the product (pouring, applying, holding) — no face visible. Add complementary props."
      prompt: |
        Generate a hands-in-use product shot.

        Same hands, product, and surface. Add small complementary props (napkin, sprig, utensil). Identical lighting and angle. No face visible — only hands interacting with the product.

        Pipeline: flux-pro/kontext (prop addition with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Hands-in-use product image." }
---

# Hands in Use

## Procedure

1. **Generate hands-in-use shot** [`generate_image`] — Product being used by hands, no face. → produces: image

## Notes

- Pipeline: flux-pro/kontext.
- No face visible — emphasizes product interaction.
