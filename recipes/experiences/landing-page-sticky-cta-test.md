---
name: Landing Page Sticky Cta Test
description: 'Test sticky CTA bar on SaaS marketing pages: always-visible vs. fade-in-on-scroll vs. no sticky. 8-15% lift
  cited; distinct from mobile-sticky-add-to-cart (ecom PDP).'
intempt:
  id: landing-page-sticky-cta-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: 'Test sticky CTA bar on SaaS marketing pages: always-visible vs. fade-in-on-scroll vs. no sticky. 8-15%
    lift cited; distinct from mobile-sticky-add-to-cart (ecom PDP).'
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

# Landing Page Sticky Cta Test

Test sticky CTA bar on SaaS marketing pages: always-visible vs. fade-in-on-scroll vs. no sticky. 8-15% lift cited; distinct from mobile-sticky-add-to-cart (ecom PDP).

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
