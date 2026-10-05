---
name: win-back
description: |
  Use when a user mentions "win-back & re-engagement", "re-engagement", "lapsed", or asks for related help. Tiered re-engagement for lapsed users — segment by recency, content per tier, journey, retention measurement.
arguments: []
intempt:
  id: win-back
  version: 1.0.0
  slashCommand: /win-back
  group: Journeys
  shortDescription: "Build tiered win-back email segments and a multi-step re-engagement journey with retention tracking."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [all]
    complexity: advanced
    executionMode: live
    tags: [win-back]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - build_retention_report
    - create_experiment
  procedure:
    - step: 1
      title: "Segment Lapsed"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Segment lapsed users into tiers: 30-60 days inactive, 60-120 days inactive, 120+ days inactive."
      prompt: "Segment lapsed users into tiers: 30-60 days inactive, 60-120 days inactive, 120+ days inactive."
    - step: 2
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed."
      prompt: "Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed."
    - step: 3
      title: "Build Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Build a multi-arm journey routing each tier through appropriate touches with escalating incentives."
      prompt: "Build a multi-arm journey routing each tier through appropriate touches with escalating incentives."
    - step: 4
      title: "Build Retention Report"
      command: build_retention_report
      produces: report
      bindsAs: report
      dependsOn: [segment, asset, journey]
      description: "Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey."
      prompt: "Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey."
    - step: 5
      title: "Build Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey, report]
      description: "Add A/B variants on incentive type (discount vs free gift vs value-only)."
      prompt: "Add A/B variants on incentive type (discount vs free gift vs value-only)."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
---

# Win-Back & Re-Engagement

## Procedure

1. **Segment Lapsed** [`create_segment`] — Segment lapsed users into tiers: 30-60 days inactive, 60-120 days inactive, 120+ days inactive. → produces: segment
2. **Build Content** [`create_email_content`] — Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed. → produces: asset
3. **Build Journey** [`create_journey`] — Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. → produces: journey
4. **Build Retention Report** [`build_retention_report`] — Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. → produces: report
5. **Build Experiment** [`create_experiment`] — Add A/B variants on incentive type (discount vs free gift vs value-only). → produces: experiment
