---
name: Pricing Toggle Default Test
description: Default to annual vs. monthly billing on the pricing toggle. Direct revenue impact (annual default → higher LTV).
  Distinct from pricing-page-layout-test.
intempt:
  id: pricing-toggle-default-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Default to annual vs. monthly billing on the pricing toggle. Direct revenue impact (annual default → higher
    LTV). Distinct from pricing-page-layout-test.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - saas
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

# Pricing Toggle Default Test

Default to annual vs. monthly billing on the pricing toggle. Direct revenue impact (annual default → higher LTV). Distinct from pricing-page-layout-test.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
