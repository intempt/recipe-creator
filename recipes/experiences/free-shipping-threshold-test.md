---
name: Free Shipping Threshold Test
description: Find the optimal free shipping threshold ($50, $75, $99, or no free shipping) that maximizes revenue per session.
  Server experiment with JSON payload.
intempt:
  id: free-shipping-threshold-test
  version: 1.0.1
  slashCommand: /experiment-recipe
  shortDescription: Find the optimal free shipping threshold ($50, $75, $99, or no free shipping) that maximizes revenue per
    session. Server experiment with JSON payload.
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
    - server
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

# Free Shipping Threshold Test

Find the optimal free shipping threshold ($50, $75, $99, or no free shipping) that maximizes revenue per session. Server experiment with JSON payload.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
