---
name: win-back
description: |
  Use when a user mentions "win-back & re-engagement", "re-engagement", "lapsed", or asks for related help. Tiered re-engagement for lapsed users: segment by recency, content per tier, journey, retention measurement.
arguments: []
intempt:
  id: win-back
  title: "Lapsed customer win back"
  version: 1.0.0
  slashCommand: /win-back
  group: Journeys
  shortDescription: "Sorts lapsed customers by how long they have been gone and escalates the offer with the gap, from a gentle nudge to an exclusive deal."
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
      title: "Sort lapsed users by the gap"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Three tiers: inactive 30 to 60 days, 60 to 120 days, and 120 days or more."
      prompt: "Segment lapsed users into tiers: 30-60 days inactive, 60-120 days inactive, 120+ days inactive."
    - step: 2
      title: "Write content per tier"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Gentle for the recently lapsed, a reminder of the value for the middle tier, and an exclusive offer for the long gone."
      prompt: "Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed."
    - step: 3
      title: "Escalate the offer by tier"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "One journey with an arm per tier, each with its own touches and a bigger incentive the longer they have been away."
      prompt: "Build a multi-arm journey routing each tier through appropriate touches with escalating incentives."
    - step: 4
      title: "Measure who comes back"
      command: build_retention_report
      produces: report
      bindsAs: report
      dependsOn: [segment, asset, journey]
      description: "Re-engagement rate per tier over the 90 days after the journey."
      prompt: "Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey."
    - step: 5
      title: "Test what brings them back"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey, report]
      description: "A/B variants on the incentive: a discount, a free gift, or no incentive at all."
      prompt: "Add A/B variants on incentive type (discount vs free gift vs value-only)."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Lapsed customer win back

Sorts lapsed customers by how long they have been gone and escalates the offer with the gap, from a gentle nudge to an exclusive deal.

## What it does

1. **Sort lapsed users by the gap** (`create_segment`)

   Three tiers: inactive 30 to 60 days, 60 to 120 days, and 120 days or more.

2. **Write content per tier** (`create_email_content`)

   Gentle for the recently lapsed, a reminder of the value for the middle tier, and an exclusive offer for the long gone.

3. **Escalate the offer by tier** (`create_journey`)

   One journey with an arm per tier, each with its own touches and a bigger incentive the longer they have been away.

4. **Measure who comes back** (`build_retention_report`)

   Re-engagement rate per tier over the 90 days after the journey.

5. **Test what brings them back** (`create_experiment`)

   A/B variants on the incentive: a discount, a free gift, or no incentive at all.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
