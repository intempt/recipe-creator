---
name: Browse Abandonment
description: Re-engage users who browsed products without adding to cart — earlier-funnel than cart abandonment.
intempt:
  id: browse-abandonment
  version: 1.0.0
  slashCommand: /browse-abandonment
  shortDescription: Re-engage users who browsed products without adding to cart — earlier-funnel than cart abandonment.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - ecommerce
    complexity: advanced
    executionMode: live
    tags:
    - browse-abandonment
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: recommendation
    type: recommendation
    description: Recommendation produced by this recipe.
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-content
    describe: Generate browse-recovery email content highlighting the viewed products and similar items.
    produces: content
  - id: build-journey
    describe: Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse.
    produces: journey
  - id: build-recommendations
    describe: Generate product recommendations for each browser based on their viewed items and purchase history.
    produces: recommendation
  - id: build-experiment
    describe: Add A/B variants comparing personalized recommendations vs trending products.
    produces: experiment
  - id: build-funnel-report
    describe: Compose a funnel report tracking browse → email-open → email-click → cart-add → purchase.
    produces: report
---

# Browse Abandonment

Re-engage users who browsed products without adding to cart — earlier-funnel than cart abandonment.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Generate browse-recovery email content highlighting the viewed products and similar items.
2. Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse.
3. Generate product recommendations for each browser based on their viewed items and purchase history.
4. Add A/B variants comparing personalized recommendations vs trending products.
5. Compose a funnel report tracking browse → email-open → email-click → cart-add → purchase.
