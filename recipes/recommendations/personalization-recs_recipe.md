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
  title: "Product recommendations across channels"
  shortDescription: "Puts product recommendations on your product pages, cart, post-purchase screens and emails, tuned to how the shopper behaves, and measures what they earn."
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
      title: "Build the recommendation model"
      command: create_recommendation
      produces: recommendation
      bindsAs: recommendation
      description: "Recommendations drawn from your product catalog using shopper-similarity and item-similarity models."
      prompt: "Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity models."
    - step: 2
      title: "Place them on each surface"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn: [recommendation]
      description: "Rules for what shows on product pages, in the cart, after purchase, and in email."
      prompt: "Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces."
    - step: 3
      title: "Split shoppers into cohorts"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [recommendation, personalization]
      description: "New visitor, browsing, returning and lapsed cohorts, each getting a differently tuned set of picks."
      prompt: "Segment users into recommendation cohorts (new visitor, browsing, returning, lapsed) for tuned strategies."
    - step: 4
      title: "Test against the alternatives"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [recommendation, personalization, segment]
      description: "A/B variants comparing personalized picks against trending products and an editor's pick."
      prompt: "Add A/B variants comparing personalized recs vs trending products vs editor's-pick."
    - step: 5
      title: "Build the email modules"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [recommendation, personalization, segment, experiment]
      description: "Recommendation blocks that drop into campaign and journey emails."
      prompt: "Generate email modules that surface recommendations within campaign and journey emails."
    - step: 6
      title: "Follow up with high-intent browsers"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [recommendation, personalization, segment, experiment, asset]
      description: "A journey that sends personalized product picks to shoppers showing strong buying intent."
      prompt: "Build a journey delivering personalized product picks to high-intent browsers."
    - step: 7
      title: "Track what recommendations earn"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [recommendation, personalization, segment, experiment, asset, journey]
      description: "Click-through rate, revenue attributed to recommendations, and how each surface performs."
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
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product recommendations across channels

Puts product recommendations on your product pages, cart, post-purchase screens and emails, tuned to how the shopper behaves, and measures what they earn.

## What it does

1. **Build the recommendation model** (`create_recommendation`)

   Recommendations drawn from your product catalog using shopper-similarity and item-similarity models.

2. **Place them on each surface** (`create_personalization`)

   Rules for what shows on product pages, in the cart, after purchase, and in email.

3. **Split shoppers into cohorts** (`create_segment`)

   New visitor, browsing, returning and lapsed cohorts, each getting a differently tuned set of picks.

4. **Test against the alternatives** (`create_experiment`)

   A/B variants comparing personalized picks against trending products and an editor's pick.

5. **Build the email modules** (`create_email_content`)

   Recommendation blocks that drop into campaign and journey emails.

6. **Follow up with high-intent browsers** (`create_journey`)

   A journey that sends personalized product picks to shoppers showing strong buying intent.

7. **Track what recommendations earn** (`create_dashboard`)

   Click-through rate, revenue attributed to recommendations, and how each surface performs.

## What you end up with

- **recommendation** (recommendation): Recommendation produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
