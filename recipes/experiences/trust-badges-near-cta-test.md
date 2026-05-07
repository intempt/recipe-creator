---
name: Trust Badges Near Cta Test
description: Test placement and selection of trust badges (security, money-back guarantee, payment methods, accreditations)
  near the primary CTA. Cited 102% lift when integrated correctly.
intempt:
  id: trust-badges-near-cta-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test placement and selection of trust badges (security, money-back guarantee, payment methods, accreditations)
    near the primary CTA. Cited 102% lift when integrated correctly.
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

# Trust Badges Near Cta Test

Test placement and selection of trust badges (security, money-back guarantee, payment methods, accreditations) near the primary CTA. Cited 102% lift when integrated correctly.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
