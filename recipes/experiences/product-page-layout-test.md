---
name: Product Page Layout Test
description: Test which PDP layout drives the highest add-to-cart rate. Client experiment with three layouts.
intempt:
  id: product-page-layout-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test which PDP layout drives the highest add-to-cart rate. Client experiment with three layouts.
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

# Product Page Layout Test

Test which PDP layout drives the highest add-to-cart rate. Client experiment with three layouts.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
