---
name: vip-loyalty
description: |
  Use when a user mentions "vip & loyalty program", or asks for related help. Identify VIPs, exclusive experiences, retention experiments, and program performance dashboards.
arguments: []
intempt:
  id: vip-loyalty
  title: "VIP loyalty programme"
  version: 1.0.0
  slashCommand: /vip-loyalty
  group: Journeys
  shortDescription: "Ranks your best customers into tiers, gives each tier something worth having, and tests which rewards actually keep them."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: experience-optimizer
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [vip-loyalty]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_personalization
    - create_journey
    - create_experiment
    - create_dashboard
  procedure:
    - step: 1
      title: "Rank customers by value"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "A value tier from lifetime spend, how often they buy and how recently."
      prompt: "Define an AI-derived Customer value tier attribute using LTV, frequency, and recency."
    - step: 2
      title: "Set the silver and gold lines"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Thresholds on that tier, splitting VIPs into silver, gold and platinum."
      prompt: "Segment VIPs into tiers (silver, gold, platinum) by value tier with thresholds."
    - step: 3
      title: "Give each tier something"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn: [attribute, segment]
      description: "VIP only treatment: early access, exclusive products and free shipping."
      prompt: "Configure VIP-only personalizations: early access, exclusive products, free shipping."
    - step: 4
      title: "Thank them, show the next tier"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, personalization]
      description: "Appreciation touches plus nudges towards the tier above."
      prompt: "Build a VIP-specific journey with appreciation touches and tier-up encouragement."
    - step: 5
      title: "Test which reward works"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [attribute, segment, personalization, journey]
      description: "Experiments comparing a discount, an experience and pure status."
      prompt: "Add experiments comparing reward types (discount vs experience vs status)."
    - step: 6
      title: "Track retention by tier"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, segment, personalization, journey, experiment]
      description: "VIP retention, average revenue in each tier, and how often people move up."
      prompt: "Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: personalization, type: personalization, cardinality: single, description: "Personalization produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# VIP loyalty programme

Ranks your best customers into tiers, gives each tier something worth having, and tests which rewards actually keep them.

## What it does

1. **Rank customers by value** (`create_ai_attribute`)

   A value tier from lifetime spend, how often they buy and how recently.

2. **Set the silver and gold lines** (`create_segment`)

   Thresholds on that tier, splitting VIPs into silver, gold and platinum.

3. **Give each tier something** (`create_personalization`)

   VIP only treatment: early access, exclusive products and free shipping.

4. **Thank them, show the next tier** (`create_journey`)

   Appreciation touches plus nudges towards the tier above.

5. **Test which reward works** (`create_experiment`)

   Experiments comparing a discount, an experience and pure status.

6. **Track retention by tier** (`create_dashboard`)

   VIP retention, average revenue in each tier, and how often people move up.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
