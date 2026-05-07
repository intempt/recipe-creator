---
name: Hero Static Vs Screenshot Test
description: 'Test landing page hero image: abstract illustration vs. real product screenshot vs. customer/team photo. Distinct
  from product-page-layout (ecom) and onboarding-flow (post-signup).'
intempt:
  id: hero-static-vs-screenshot-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: 'Test landing page hero image: abstract illustration vs. real product screenshot vs. customer/team photo.
    Distinct from product-page-layout (ecom) and onboarding-flow (post-signup).'
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

# Hero Static Vs Screenshot Test

Test landing page hero image: abstract illustration vs. real product screenshot vs. customer/team photo. Distinct from product-page-layout (ecom) and onboarding-flow (post-signup).

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
