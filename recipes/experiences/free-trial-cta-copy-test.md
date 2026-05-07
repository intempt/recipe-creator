---
name: Free Trial Cta Copy Test
description: Test which CTA button copy drives more trial signups on a landing page. Client experiment with random traffic
  split.
intempt:
  id: free-trial-cta-copy-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test which CTA button copy drives more trial signups on a landing page. Client experiment with random
    traffic split.
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

# Free Trial Cta Copy Test

Test which CTA button copy drives more trial signups on a landing page. Client experiment with random traffic split.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
