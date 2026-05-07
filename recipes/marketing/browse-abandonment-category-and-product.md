---
name: Browse Abandonment Category And Product
description: Unified browse-abandonment journey triggered when users view products, collections, categories, or search results
  without adding to cart. Branches by interest type (product-level vs...
intempt:
  id: browse-abandonment-category-and-product
  version: 1.0.0
  slashCommand: /browse-abandonment-category-and-product
  shortDescription: Unified browse-abandonment journey triggered when users view products, collections, categories, or search
    results without adding to cart. Branches by interest type (product-level vs...
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
    - browse-and-interest-recovery
    - browse
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
    describe: 'Generate browse-recovery email content highlighting the viewed products and similar items. (Tailored for: Browse
      abandonment — category and product.)'
    produces: content
  - id: build-journey
    describe: 'Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse. (Tailored for: Browse
      abandonment — category and product.)'
    produces: journey
  - id: build-recommendations
    describe: 'Generate product recommendations for each browser based on their viewed items and purchase history. (Tailored
      for: Browse abandonment — category and product.)'
    produces: recommendation
  - id: build-experiment
    describe: 'Add A/B variants comparing personalized recommendations vs trending products. (Tailored for: Browse abandonment
      — category and product.)'
    produces: experiment
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking browse → email-open → email-click → cart-add → purchase. (Tailored for: Browse
      abandonment — category and product.)'
    produces: report
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Browse Abandonment Category And Product

Unified browse-abandonment journey triggered when users view products, collections, categories, or search results without adding to cart. Branches by interest type (product-level vs...

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Generate browse-recovery email content highlighting the viewed products and similar items. (Tailored for: Browse abandonment — category and product.)
2. Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse. (Tailored for: Browse abandonment — category and product.)
3. Generate product recommendations for each browser based on their viewed items and purchase history. (Tailored for: Browse abandonment — category and product.)
4. Add A/B variants comparing personalized recommendations vs trending products. (Tailored for: Browse abandonment — category and product.)
5. Compose a funnel report tracking browse → email-open → email-click → cart-add → purchase. (Tailored for: Browse abandonment — category and product.)

## Prerequisites

- Integration: **shopify** (blocking)
