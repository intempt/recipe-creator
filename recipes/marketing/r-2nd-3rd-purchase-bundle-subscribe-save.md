---
name: R 2Nd 3Rd Purchase Bundle Subscribe Save
description: Moves 2-time buyers to the VIP 3rd-purchase milestone with bundle offers and subscribe-and-save incentives. Third
  purchase is the strongest predictor of long-term LTV.
intempt:
  id: r-2nd-3rd-purchase-bundle-subscribe-save
  version: 1.0.0
  slashCommand: /r-2nd-3rd-purchase-bundle-subscribe-save
  shortDescription: Moves 2-time buyers to the VIP 3rd-purchase milestone with bundle offers and subscribe-and-save incentives.
    Third purchase is the strongest predictor of long-term LTV.
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
    - r
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
      (Tailored for: 2nd → 3rd purchase bundle / subscribe-save.)'
    produces: content
  - id: build-journey
    describe: 'Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell),
      30day (loyalty intro). (Tailored for: 2nd → 3rd purchase bundle / subscribe-save.)'
    produces: journey
  - id: build-recommendations
    describe: 'Generate cross-sell recommendations based on the purchased items and the customer''s profile. (Tailored for:
      2nd → 3rd purchase bundle / subscribe-save.)'
    produces: recommendation
  - id: build-experiment
    describe: 'Add A/B variants on review-request timing (3day vs 7day vs 14day). (Tailored for: 2nd → 3rd purchase bundle
      / subscribe-save.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell.
      (Tailored for: 2nd → 3rd purchase bundle / subscribe-save.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# R 2Nd 3Rd Purchase Bundle Subscribe Save

Moves 2-time buyers to the VIP 3rd-purchase milestone with bundle offers and subscribe-and-save incentives. Third purchase is the strongest predictor of long-term LTV.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions. (Tailored for: 2nd → 3rd purchase bundle / subscribe-save.)
2. Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro). (Tailored for: 2nd → 3rd purchase bundle / subscribe-save.)
3. Generate cross-sell recommendations based on the purchased items and the customer's profile. (Tailored for: 2nd → 3rd purchase bundle / subscribe-save.)
4. Add A/B variants on review-request timing (3day vs 7day vs 14day). (Tailored for: 2nd → 3rd purchase bundle / subscribe-save.)
5. Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell. (Tailored for: 2nd → 3rd purchase bundle / subscribe-save.)

## Prerequisites

- Integration: **shopify** (blocking)
