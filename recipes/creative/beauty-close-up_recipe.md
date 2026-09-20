---
name: beauty-close-up
description: |
  Use when a user mentions "beauty close-up", "beauty shot", "skincare shot", "cosmetics close-up", or asks for a tight beauty photo with product branding. Plain bottle to branded bottle close-up.
arguments: []
intempt:
  id: beauty-close-up
  version: 1.0.0
  slashCommand: /beauty-close-up
  group: Creative
  title: 'Branded beauty close-up'
  shortDescription: 'Puts your brand wordmark and cap styling onto the product in a beauty close-up, leaving the model, hands and framing untouched.'
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
      title: 'Brand the product in frame'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Keeps the same model, skin, hand position, bottle and composition. The only change is the brand wordmark and cap styling on the product.'
      prompt: |
        Generate a beauty close-up with branded product.

        Keep the same model, skin, hand position, and bottle. Only change: apply the brand wordmark and cap styling to the product. Composition unchanged.

        Pipeline: flux-pro/kontext (identity-locked branding)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Branded beauty close-up." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Branded beauty close-up

Puts your brand wordmark and cap styling onto the product in a beauty close-up, leaving the model, hands and framing untouched.

## What it does

1. **Brand the product in frame** (`generate_image`)

   Keeps the same model, skin, hand position, bottle and composition. The only change is the brand wordmark and cap styling on the product.

## What you end up with

- **image** (image): Branded beauty close-up.
