---
name: Checkout Flow Length Test
description: Test whether single-page or multi-step checkout reduces abandonment. Client experiment.
intempt:
  id: checkout-flow-length-test
  version: 1.0.1
  slashCommand: /experiment-recipe
  shortDescription: Test whether single-page or multi-step checkout reduces abandonment. Client experiment.
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

# Checkout Flow Length Test

Test whether single-page or multi-step checkout reduces abandonment. Client experiment.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
