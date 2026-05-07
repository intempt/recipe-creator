---
name: Express Checkout Placement Test
description: Test express-checkout button placement on PDP, cart, and checkout. "Highest-impact payment additions" eliminating
  card-entry friction; major mobile conversion factor.
intempt:
  id: express-checkout-placement-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test express-checkout button placement on PDP, cart, and checkout. "Highest-impact payment additions"
    eliminating card-entry friction; major mobile conversion factor.
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

# Express Checkout Placement Test

Test express-checkout button placement on PDP, cart, and checkout. "Highest-impact payment additions" eliminating card-entry friction; major mobile conversion factor.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
