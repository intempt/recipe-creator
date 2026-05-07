---
name: Product Recommendation Algorithm
description: 'Test which recommendation engine drives more cross-sell revenue: collaborative filtering vs. session-based vs.
  popularity. Server experiment with JSON payload.'
intempt:
  id: product-recommendation-algorithm
  version: 1.0.1
  slashCommand: /experiment-recipe
  shortDescription: 'Test which recommendation engine drives more cross-sell revenue: collaborative filtering vs. session-based
    vs. popularity. Server experiment with JSON payload.'
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

# Product Recommendation Algorithm

Test which recommendation engine drives more cross-sell revenue: collaborative filtering vs. session-based vs. popularity. Server experiment with JSON payload.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
