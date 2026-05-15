---
name: welcome-series
description: |
  Use when a user mentions "welcome series", "onboarding", "welcome series", or asks for related help. First-touch sequence for new subscribers — segment, content, journey, A/B variants, performance dashboard.
arguments: []
intempt:
  id: welcome-series
  version: 1.0.0
  slashCommand: /welcome-series
  group: Journeys
  shortDescription: "First-touch sequence for new subscribers \u2014 segment, content, journey, A/B variants, performance dashboard."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [all]
    complexity: advanced
    executionMode: live
    tags: [welcome-series]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_experiment
    - create_dashboard
  procedure:
    - step: 1
      title: "Identify New Subscribers"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Identify users who subscribed within the last 30 days and have not received a welcome email yet."
      prompt: "Identify users who subscribed within the last 30 days and have not received a welcome email yet."
    - step: 2
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice."
      prompt: "Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice."
    - step: 3
      title: "Build Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription."
      prompt: "Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription."
    - step: 4
      title: "Build Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey]
      description: "Add A/B variants on subject lines and welcome offer presence."
      prompt: "Add A/B variants on subject lines and welcome offer presence."
    - step: 5
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, experiment]
      description: "Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey."
      prompt: "Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Welcome Series

## Procedure

1. **Identify New Subscribers** [`create_segment`] — Identify users who subscribed within the last 30 days and have not received a welcome email yet. → produces: segment
2. **Build Content** [`create_email_content`] — Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. → produces: asset
3. **Build Journey** [`create_journey`] — Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. → produces: journey
4. **Build Experiment** [`create_experiment`] — Add A/B variants on subject lines and welcome offer presence. → produces: experiment
5. **Build Dashboard** [`create_dashboard`] — Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. → produces: dashboard
