---
name: lifestyle-scene
description: |
  Use when a user mentions "lifestyle scene", "product in context", "real-world setting", "environmental shot", or asks to place a product in a real-world scene. Product in a real-world setting.
arguments: []
intempt:
  id: lifestyle-scene
  version: 1.0.0
  slashCommand: /lifestyle-scene
  group: Creative
  shortDescription: "Generate one lifestyle scene image that places the provided product packshot into a real-world environment while preserving product identity."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, lifestyle, product]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Place product in lifestyle scene"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Take a studio packshot and place the product in a real-world environment with natural lighting and depth of field."
      prompt: |
        Place a product in a lifestyle scene.

        Take the studio packshot and re-render the product in a real-world environment (kitchen, office, outdoors, etc.). Product identity must remain unchanged. Apply natural ambient lighting and realistic depth of field.

        Pipeline: flux-pro/kontext (scene replacement with product identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Lifestyle scene image." }
---

# Lifestyle Scene

## Procedure

1. **Place product in lifestyle scene** [`generate_image`] — Packshot → real-world environment. → produces: image

## Notes

- Pipeline: flux-pro/kontext with identity-locked product placement.
- Product identity preserved; only environment changes.
