---
name: personalization-recs
description: |
  Use when a user mentions "personalization & recommendations", or asks for related help. Catalog-aware recommendations across web, email, and app surfaces.
arguments: []
intempt:
  id: personalization-recs
  version: 1.0.0
  slashCommand: /personalization-recs
  group: Recommendations
  shortDescription: "Catalog-aware recommendations across web, email, and app surfaces."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing, sales]
    agent: experience-optimizer
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [personalization-recs]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_recommendation
    - create_personalization
    - create_segment
    - create_experiment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Build Recommendation"
      command: create_recommendation
      produces: recommendation
      bindsAs: recommendation
      description: "Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity models."
      prompt: "Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity models."
    - step: 2
      title: "Build Personalization"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn: [recommendation]
      description: "Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces."
      prompt: "Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces."
    - step: 3
      title: "Segment Cohorts"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [recommendation, personalization]
      description: "Segment users into recommendation cohorts (new visitor, browsing, returning, lapsed) for tuned strategies."
      prompt: "Segment users into recommendation cohorts (new visitor, browsing, returning, lapsed) for tuned strategies."
    - step: 4
      title: "Build Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [recommendation, personalization, segment]
      description: "Add A/B variants comparing personalized recs vs trending products vs editor's-pick."
      prompt: "Add A/B variants comparing personalized recs vs trending products vs editor's-pick."
    - step: 5
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [recommendation, personalization, segment, experiment]
      description: "Generate email modules that surface recommendations within campaign and journey emails."
      prompt: "Generate email modules that surface recommendations within campaign and journey emails."
    - step: 6
      title: "Build Recs Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [recommendation, personalization, segment, experiment, asset]
      description: "Build a journey delivering personalized product picks to high-intent browsers."
      prompt: "Build a journey delivering personalized product picks to high-intent browsers."
    - step: 7
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [recommendation, personalization, segment, experiment, asset, journey]
      description: "Compose a dashboard tracking recommendation CTR, attributed revenue, and per-surface performance."
      prompt: "Compose a dashboard tracking recommendation CTR, attributed revenue, and per-surface performance."
  outputs:
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation produced by this recipe." }
    - { name: personalization, type: personalization, cardinality: single, description: "Personalization produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Personalization & Recommendations

## Procedure

1. **Build Recommendation** [`create_recommendation`] — Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity models. → produces: recommendation
2. **Build Personalization** [`create_personalization`] — Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces. → produces: personalization
3. **Segment Cohorts** [`create_segment`] — Segment users into recommendation cohorts (new visitor, browsing, returning, lapsed) for tuned strategies. → produces: segment
4. **Build Experiment** [`create_experiment`] — Add A/B variants comparing personalized recs vs trending products vs editor's-pick. → produces: experiment
5. **Build Content** [`create_email_content`] — Generate email modules that surface recommendations within campaign and journey emails. → produces: asset
6. **Build Recs Journey** [`create_journey`] — Build a journey delivering personalized product picks to high-intent browsers. → produces: journey
7. **Build Dashboard** [`create_dashboard`] — Compose a dashboard tracking recommendation CTR, attributed revenue, and per-surface performance. → produces: dashboard
