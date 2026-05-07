---
name: Saas Exit Intent Offer Test
description: Test what to OFFER on exit-intent for SaaS visitors (discount vs. comparison guide vs. content download vs. survey).
  5x conversion vs. time-based popup cited.
intempt:
  id: saas-exit-intent-offer-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test what to OFFER on exit-intent for SaaS visitors (discount vs. comparison guide vs. content download
    vs. survey). 5x conversion vs. time-based popup cited.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - saas
    - b2b
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

# Saas Exit Intent Offer Test

Test what to OFFER on exit-intent for SaaS visitors (discount vs. comparison guide vs. content download vs. survey). 5x conversion vs. time-based popup cited.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
