---
id: vip-loyalty
title: VIP loyalty programme
slash_command: /vip-loyalty
group: Journeys
owner: intempt
summary: Ranks your best customers into tiers, gives each tier something worth having, and tests which
  rewards actually keep them.
description: >-
  Identify VIPs, exclusive experiences, retention experiments, and program performance dashboards.
version: 2.0.0
classification:
  product:
    - marketing
  agent: experience-optimizer
  mode:
    - ecommerce
  complexity: advanced
  executionMode: live
  tags:
    - vip-loyalty
steps:
  - id: s1
    title: Rank customers by value
    summary: >-
      A value tier from lifetime spend, how often they buy and how recently.
    builds: attribute
    description: >-
      Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency.
  - id: s2
    title: Set the silver and gold lines
    summary: >-
      Thresholds on that tier, splitting VIPs into silver, gold and platinum.
    builds: segment
    description: >-
      Segment VIPs into tiers (silver, gold, platinum) by value tier with thresholds. Use the result of
      "Rank customers by value".
    dependsOn:
      - s1
  - id: s3
    title: Give each tier something
    summary: >-
      VIP only treatment: early access, exclusive products and free shipping.
    builds: personalization
    description: >-
      Configure VIP-only personalizations: early access, exclusive products, free shipping. Use the result
      of "Rank customers by value", "Set the silver and gold lines".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Thank them, show the next tier
    summary: >-
      Appreciation touches plus nudges towards the tier above.
    builds: journey
    description: >-
      Build a VIP-specific journey with appreciation touches and tier-up encouragement. Use the result
      of "Rank customers by value", "Set the silver and gold lines", "Give each tier something".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Test which reward works
    summary: >-
      Experiments comparing a discount, an experience and pure status.
    builds: experiment
    description: >-
      Add experiments comparing reward types (discount vs experience vs status). Use the result of "Rank
      customers by value", "Set the silver and gold lines", "Give each tier something", "Thank them, show
      the next tier".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: Track retention by tier
    summary: >-
      VIP retention, average revenue in each tier, and how often people move up.
    builds: dashboard
    description: >-
      Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate. Use
      the result of "Rank customers by value", "Set the silver and gold lines", "Give each tier something",
      "Thank them, show the next tier", "Test which reward works".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: personalization
    producedByStep: s3
    type: personalization
    description: Personalization produced by this recipe.
  - key: journey
    producedByStep: s4
    type: journey
    description: Journey produced by this recipe.
  - key: experiment
    producedByStep: s5
    type: experiment
    description: Experiment produced by this recipe.
  - key: dashboard
    producedByStep: s6
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# VIP loyalty programme

Ranks your best customers into tiers, gives each tier something worth having, and tests which rewards actually keep them.

## Steps

1. **Rank customers by value** (builds attribute)

   A value tier from lifetime spend, how often they buy and how recently.

2. **Set the silver and gold lines** (builds segment)

   Thresholds on that tier, splitting VIPs into silver, gold and platinum.

3. **Give each tier something** (builds personalization)

   VIP only treatment: early access, exclusive products and free shipping.

4. **Thank them, show the next tier** (builds journey)

   Appreciation touches plus nudges towards the tier above.

5. **Test which reward works** (builds experiment)

   Experiments comparing a discount, an experience and pure status.

6. **Track retention by tier** (builds dashboard)

   VIP retention, average revenue in each tier, and how often people move up.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, experiment, journey, personalization.
