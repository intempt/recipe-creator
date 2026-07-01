---
name: beauty-close-up
description: |
  Use when a user mentions "beauty close-up", "beauty shot", "skincare shot", "cosmetics close-up", or asks for a tight beauty photo with product branding. Plain bottle → branded bottle close-up.
arguments: []
intempt:
  id: beauty-close-up
  version: 1.0.0
  slashCommand: /beauty-close-up
  group: Creative
  shortDescription: "Plain bottle → branded bottle close-up."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, beauty, skincare]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Generate beauty close-up"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Take a tight beauty close-up with product and apply brand identity (wordmark, label) while preserving the model and composition."
      prompt: |
        Generate a beauty close-up with branded product.

        Keep the same model, skin, hand position, and bottle. Only change: apply the brand wordmark and cap styling to the product. Composition unchanged.

        Pipeline: flux-pro/kontext (identity-locked branding)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Branded beauty close-up." }
---

# Beauty Close-Up

## Procedure

1. **Generate beauty close-up** [`generate_image`] — Apply brand identity to product in close-up. → produces: image

## Notes

- Pipeline: flux-pro/kontext for identity-locked branding.
- Model identity, skin, and composition preserved; only product branding changes.
