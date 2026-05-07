---
name: Free Shipping Progress Bar Test
description: Test cart-page free-shipping progress bar (e.g., "$12 away from free shipping") vs. no progress bar. Top-cited
  AOV-lifting test in 2026 CRO content.
intempt:
  id: free-shipping-progress-bar-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test cart-page free-shipping progress bar (e.g., "$12 away from free shipping") vs. no progress bar. Top-cited
    AOV-lifting test in 2026 CRO content.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - experiment
    - client
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: experience
    type: experience
    description: Website experiment created on /experiences.
  steps:
  - id: configure-website-experiment
    describe: 'Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content
      (Path 2).'
    produces: experience
---

# Free Shipping Progress Bar Test

Test cart-page free-shipping progress bar (e.g., "$12 away from free shipping") vs. no progress bar. Top-cited AOV-lifting test in 2026 CRO content.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
