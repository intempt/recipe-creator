---
name: vip-loyalty
description: |
  Use when a user mentions "vip & loyalty program", or asks for related help. Identify VIPs, exclusive experiences, retention experiments, and program performance dashboards.
arguments: []
intempt:
  id: vip-loyalty
  version: 1.0.0
  slashCommand: /vip-loyalty
  group: Journeys
  shortDescription: "Build a VIP loyalty playbook that computes customer_value_tier, creates silver/gold/platinum segments, and launches a VIP journey."
  availability: coming-soon
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
      title: "Compute Customer Value"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency."
      prompt: "Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency."
    - step: 2
      title: "Segment Vips"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Segment VIPs into tiers (silver, gold, platinum) by value tier with thresholds."
      prompt: "Segment VIPs into tiers (silver, gold, platinum) by value tier with thresholds."
    - step: 3
      title: "Build Exclusive Personalization"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn: [attribute, segment]
      description: "Configure VIP-only personalizations: early access, exclusive products, free shipping."
      prompt: "Configure VIP-only personalizations: early access, exclusive products, free shipping."
    - step: 4
      title: "Build Vip Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, personalization]
      description: "Build a VIP-specific journey with appreciation touches and tier-up encouragement."
      prompt: "Build a VIP-specific journey with appreciation touches and tier-up encouragement."
    - step: 5
      title: "Build Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [attribute, segment, personalization, journey]
      description: "Add experiments comparing reward types (discount vs experience vs status)."
      prompt: "Add experiments comparing reward types (discount vs experience vs status)."
    - step: 6
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, segment, personalization, journey, experiment]
      description: "Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate."
      prompt: "Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: personalization, type: personalization, cardinality: single, description: "Personalization produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# VIP & Loyalty Program

## Procedure

1. **Compute Customer Value** [`create_ai_attribute`] — Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency. → produces: attribute
2. **Segment Vips** [`create_segment`] — Segment VIPs into tiers (silver, gold, platinum) by value tier with thresholds. → produces: segment
3. **Build Exclusive Personalization** [`create_personalization`] — Configure VIP-only personalizations: early access, exclusive products, free shipping. → produces: personalization
4. **Build Vip Journey** [`create_journey`] — Build a VIP-specific journey with appreciation touches and tier-up encouragement. → produces: journey
5. **Build Experiment** [`create_experiment`] — Add experiments comparing reward types (discount vs experience vs status). → produces: experiment
6. **Build Dashboard** [`create_dashboard`] — Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate. → produces: dashboard
