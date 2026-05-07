---
name: Product Review Request
description: Post-delivery review solicitation sequence timed to arrive when the buyer has actually used the product. Branches
  on review submission to route feedback (positive → request public review, negative...
intempt:
  id: product-review-request
  version: 1.0.0
  slashCommand: /product-review-request
  shortDescription: Post-delivery review solicitation sequence timed to arrive when the buyer has actually used the product.
    Branches on review submission to route feedback (positive → request public review, negative...
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
    - post-purchase-and-retention
    - product
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
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-content
    describe: 'Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions.
      (Tailored for: Product review request.)'
    produces: content
  - id: build-journey
    describe: 'Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell),
      30day (loyalty intro). (Tailored for: Product review request.)'
    produces: journey
  - id: build-recommendations
    describe: 'Generate cross-sell recommendations based on the purchased items and the customer''s profile. (Tailored for:
      Product review request.)'
    produces: recommendation
  - id: build-experiment
    describe: 'Add A/B variants on review-request timing (3day vs 7day vs 14day). (Tailored for: Product review request.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell.
      (Tailored for: Product review request.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Product Review Request

Post-delivery review solicitation sequence timed to arrive when the buyer has actually used the product. Branches on review submission to route feedback (positive → request public review, negative...

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions. (Tailored for: Product review request.)
2. Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro). (Tailored for: Product review request.)
3. Generate cross-sell recommendations based on the purchased items and the customer's profile. (Tailored for: Product review request.)
4. Add A/B variants on review-request timing (3day vs 7day vs 14day). (Tailored for: Product review request.)
5. Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell. (Tailored for: Product review request.)

## Prerequisites

- Integration: **shopify** (blocking)
