---
name: Customer Birthday Celebration
description: Annual birthday touchpoint with birthday-specific incentive. Works as relationship-builder for active customers
  and light re-engagement for dormant ones.
intempt:
  id: customer-birthday-celebration
  version: 1.0.0
  slashCommand: /customer-birthday-celebration
  shortDescription: Annual birthday touchpoint with birthday-specific incentive. Works as relationship-builder for active
    customers and light re-engagement for dormant ones.
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
    - customer
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
      (Tailored for: Customer birthday celebration.)'
    produces: content
  - id: build-journey
    describe: 'Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell),
      30day (loyalty intro). (Tailored for: Customer birthday celebration.)'
    produces: journey
  - id: build-recommendations
    describe: 'Generate cross-sell recommendations based on the purchased items and the customer''s profile. (Tailored for:
      Customer birthday celebration.)'
    produces: recommendation
  - id: build-experiment
    describe: 'Add A/B variants on review-request timing (3day vs 7day vs 14day). (Tailored for: Customer birthday celebration.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell.
      (Tailored for: Customer birthday celebration.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Customer Birthday Celebration

Annual birthday touchpoint with birthday-specific incentive. Works as relationship-builder for active customers and light re-engagement for dormant ones.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions. (Tailored for: Customer birthday celebration.)
2. Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro). (Tailored for: Customer birthday celebration.)
3. Generate cross-sell recommendations based on the purchased items and the customer's profile. (Tailored for: Customer birthday celebration.)
4. Add A/B variants on review-request timing (3day vs 7day vs 14day). (Tailored for: Customer birthday celebration.)
5. Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell. (Tailored for: Customer birthday celebration.)

## Prerequisites

- Integration: **shopify** (blocking)
