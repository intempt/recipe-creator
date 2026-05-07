---
name: Loyalty Program Entry Offer Test
description: Test the best entry offer to drive loyalty programme sign-ups at checkout. Client experiment with random split.
intempt:
  id: loyalty-program-entry-offer-test
  version: 1.0.1
  slashCommand: /experiment-recipe
  shortDescription: Test the best entry offer to drive loyalty programme sign-ups at checkout. Client experiment with random
    split.
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

# Loyalty Program Entry Offer Test

Test the best entry offer to drive loyalty programme sign-ups at checkout. Client experiment with random split.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
