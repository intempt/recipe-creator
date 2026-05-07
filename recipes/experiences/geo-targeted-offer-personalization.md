---
name: Geo Targeted Offer Personalization
description: Show different homepage offers based on visitor's geography (country, region) — different shipping promotions,
  currency display, and local promotions. Client personalization.
intempt:
  id: geo-targeted-offer-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  shortDescription: Show different homepage offers based on visitor's geography (country, region) — different shipping promotions,
    currency display, and local promotions. Client personalization.
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
    - personalization
    - client
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: experience
    type: experience
    description: Website personalization created on /experiences.
  steps:
  - id: configure-website-personalization
    describe: 'Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content
      (Path 2).'
    produces: experience
---

# Geo Targeted Offer Personalization

Show different homepage offers based on visitor's geography (country, region) — different shipping promotions, currency display, and local promotions. Client personalization.

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
