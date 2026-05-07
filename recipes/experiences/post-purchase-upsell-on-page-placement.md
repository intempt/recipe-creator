---
name: Post Purchase Upsell On Page Placement
description: Test where to show the post-purchase upsell on the order confirmation page (above order details, below order
  details, or as inline modal). Website-only — email and push variants are out of scope.
intempt:
  id: post-purchase-upsell-on-page-placement
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test where to show the post-purchase upsell on the order confirmation page (above order details, below
    order details, or as inline modal). Website-only — email and push variants are out of scope.
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

# Post Purchase Upsell On Page Placement

Test where to show the post-purchase upsell on the order confirmation page (above order details, below order details, or as inline modal). Website-only — email and push variants are out of scope.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
