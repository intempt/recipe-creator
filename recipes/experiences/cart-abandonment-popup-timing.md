---
name: Cart Abandonment Popup Timing
description: 'Test when to show the save-your-cart popup: exit-intent vs. delay vs. no popup. Client experiment.'
intempt:
  id: cart-abandonment-popup-timing
  version: 1.0.1
  slashCommand: /experiment-recipe
  shortDescription: 'Test when to show the save-your-cart popup: exit-intent vs. delay vs. no popup. Client experiment.'
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

# Cart Abandonment Popup Timing

Test when to show the save-your-cart popup: exit-intent vs. delay vs. no popup. Client experiment.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
