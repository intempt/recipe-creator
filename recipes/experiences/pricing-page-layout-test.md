---
name: Pricing Page Layout Test
description: Test which pricing page layout maximizes plan selection and checkout starts. Client experiment with three variants.
intempt:
  id: pricing-page-layout-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test which pricing page layout maximizes plan selection and checkout starts. Client experiment with three
    variants.
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

# Pricing Page Layout Test

Test which pricing page layout maximizes plan selection and checkout starts. Client experiment with three variants.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
