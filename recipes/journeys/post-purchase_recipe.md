---
name: post-purchase
description: |
  Use when a user mentions "post-purchase nurture", or asks for related help. Thank-you, review request, brand education, and cross-sell for first-time buyers.
arguments: []
intempt:
  id: post-purchase
  version: 1.0.0
  slashCommand: /post-purchase
  group: Journeys
  shortDescription: "Thank-you, review request, brand education, and cross-sell for first-time buyers."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [post-purchase]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_recommendation
    - create_experiment
    - create_dashboard
  procedure:
    - step: 1
      title: "Identify Recent Buyers"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Identify users with order_placed event in last 14 days, segmented by first-time vs repeat buyer."
      prompt: "Identify users with order_placed event in last 14 days, segmented by first-time vs repeat buyer."
    - step: 2
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions."
      prompt: "Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions."
    - step: 3
      title: "Build Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro)."
      prompt: "Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro)."
    - step: 4
      title: "Build Recommendations"
      command: create_recommendation
      produces: recommendation
      bindsAs: recommendation
      dependsOn: [segment, asset, journey]
      description: "Generate cross-sell recommendations based on the purchased items and the customer's profile."
      prompt: "Generate cross-sell recommendations based on the purchased items and the customer's profile."
    - step: 5
      title: "Build Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey, recommendation]
      description: "Add A/B variants on review-request timing (3day vs 7day vs 14day)."
      prompt: "Add A/B variants on review-request timing (3day vs 7day vs 14day)."
    - step: 6
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, recommendation, experiment]
      description: "Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell."
      prompt: "Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Post-Purchase Nurture

## Procedure

1. **Identify Recent Buyers** [`create_segment`] — Identify users with order_placed event in last 14 days, segmented by first-time vs repeat buyer. → produces: segment
2. **Build Content** [`create_email_content`] — Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions. → produces: asset
3. **Build Journey** [`create_journey`] — Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro). → produces: journey
4. **Build Recommendations** [`create_recommendation`] — Generate cross-sell recommendations based on the purchased items and the customer's profile. → produces: recommendation
5. **Build Experiment** [`create_experiment`] — Add A/B variants on review-request timing (3day vs 7day vs 14day). → produces: experiment
6. **Build Dashboard** [`create_dashboard`] — Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell. → produces: dashboard
