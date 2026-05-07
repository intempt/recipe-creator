---
name: Mobile Sticky Add To Cart Test
description: Test whether a sticky add-to-cart bar on mobile improves conversion. Client experiment, mobile-only.
intempt:
  id: mobile-sticky-add-to-cart-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test whether a sticky add-to-cart bar on mobile improves conversion. Client experiment, mobile-only.
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

# Mobile Sticky Add To Cart Test

Test whether a sticky add-to-cart bar on mobile improves conversion. Client experiment, mobile-only.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
