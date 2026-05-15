---
name: browse-abandonment
description: |
  Use when a user mentions "browse abandonment", or asks for related help. Re-engage users who browsed products without adding to cart — earlier-funnel than cart abandonment.
arguments: []
intempt:
  id: browse-abandonment
  version: 1.0.0
  slashCommand: /browse-abandonment
  group: Journeys
  shortDescription: "Re-engage users who browsed products without adding to cart \u2014 earlier-funnel than cart abandonment."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [browse-abandonment]
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
    - build_funnel_report
  procedure:
    - step: 1
      title: "Identify Browsers"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Identify users with product_viewed events in last 7 days who did NOT trigger cart_added."
      prompt: "Identify users with product_viewed events in last 7 days who did NOT trigger cart_added."
    - step: 2
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Generate browse-recovery email content highlighting the viewed products and similar items."
      prompt: "Generate browse-recovery email content highlighting the viewed products and similar items."
    - step: 3
      title: "Build Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse."
      prompt: "Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse."
    - step: 4
      title: "Build Recommendations"
      command: create_recommendation
      produces: recommendation
      bindsAs: recommendation
      dependsOn: [segment, asset, journey]
      description: "Generate product recommendations for each browser based on their viewed items and purchase history."
      prompt: "Generate product recommendations for each browser based on their viewed items and purchase history."
    - step: 5
      title: "Build Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey, recommendation]
      description: "Add A/B variants comparing personalized recommendations vs trending products."
      prompt: "Add A/B variants comparing personalized recommendations vs trending products."
    - step: 6
      title: "Build Funnel Report"
      command: build_funnel_report
      produces: report
      bindsAs: report
      dependsOn: [segment, asset, journey, recommendation, experiment]
      description: "Compose a funnel report tracking browse → email-open → email-click → cart-add → purchase."
      prompt: "Compose a funnel report tracking browse → email-open → email-click → cart-add → purchase."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Browse Abandonment

## Procedure

1. **Identify Browsers** [`create_segment`] — Identify users with product_viewed events in last 7 days who did NOT trigger cart_added. → produces: segment
2. **Build Content** [`create_email_content`] — Generate browse-recovery email content highlighting the viewed products and similar items. → produces: asset
3. **Build Journey** [`create_journey`] — Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse. → produces: journey
4. **Build Recommendations** [`create_recommendation`] — Generate product recommendations for each browser based on their viewed items and purchase history. → produces: recommendation
5. **Build Experiment** [`create_experiment`] — Add A/B variants comparing personalized recommendations vs trending products. → produces: experiment
6. **Build Funnel Report** [`build_funnel_report`] — Compose a funnel report tracking browse → email-open → email-click → cart-add → purchase. → produces: report
