---
name: trial-activation
description: |
  Use when a user mentions "trial-to-paid activation", "trial conversion", "trial activation", or asks for related help. Drive trial users to paid conversion via scoring, segmentation, onboarding journey, and funnel measurement.
arguments: []
intempt:
  id: trial-activation
  version: 1.0.0
  slashCommand: /trial-activation
  group: Journeys
  shortDescription: "Create a trial_health_score attribute, risk-tier trial segment, tier-specific onboarding emails, and a conversion journey with funnel reporting."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [trial-activation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_journey
    - build_funnel_report
  procedure:
    - step: 1
      title: "Compute Trial Health"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded)."
      prompt: "Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded)."
    - step: 2
      title: "Segment By Risk"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Segment trial users into risk tiers (high-engagement, moderate, at-risk) based on trial_health_score."
      prompt: "Segment trial users into risk tiers (high-engagement, moderate, at-risk) based on trial_health_score."
    - step: 3
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute, segment]
      description: "Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier."
      prompt: "Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier."
    - step: 4
      title: "Build Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, asset]
      description: "Build a tiered onboarding journey routing each tier through appropriate education and conversion touches."
      prompt: "Build a tiered onboarding journey routing each tier through appropriate education and conversion touches."
    - step: 5
      title: "Build Funnel Report"
      command: build_funnel_report
      produces: report
      bindsAs: report
      dependsOn: [attribute, segment, asset, journey]
      description: "Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay."
      prompt: "Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Trial-to-Paid Activation

## Procedure

1. **Compute Trial Health** [`create_ai_attribute`] — Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). → produces: attribute
2. **Segment By Risk** [`create_segment`] — Segment trial users into risk tiers (high-engagement, moderate, at-risk) based on trial_health_score. → produces: segment
3. **Build Content** [`create_email_content`] — Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. → produces: asset
4. **Build Journey** [`create_journey`] — Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. → produces: journey
5. **Build Funnel Report** [`build_funnel_report`] — Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. → produces: report
