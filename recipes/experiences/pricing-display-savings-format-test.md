---
name: Pricing Display Savings Format Test
description: 'Test how savings are displayed on pricing pages: dollar amount ($24 off) vs. percentage (20% off) vs. compare-at
  framing ($120 → $96). Universally cited as one of the highest-impact pricing tests.'
intempt:
  id: pricing-display-savings-format-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: 'Test how savings are displayed on pricing pages: dollar amount ($24 off) vs. percentage (20% off) vs.
    compare-at framing ($120 → $96). Universally cited as one of the highest-impact pricing tests.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - saas
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

# Pricing Display Savings Format Test

Test how savings are displayed on pricing pages: dollar amount ($24 off) vs. percentage (20% off) vs. compare-at framing ($120 → $96). Universally cited as one of the highest-impact pricing tests.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
