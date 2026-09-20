---
name: trial-activation
description: |
  Use when a user mentions "trial-to-paid activation", "trial conversion", "trial activation", or asks for related help. Drive trial users to paid conversion via scoring, segmentation, onboarding journey, and funnel measurement.
arguments: []
intempt:
  id: trial-activation
  title: "Trial to paid activation"
  version: 1.0.0
  slashCommand: /trial-activation
  group: Journeys
  shortDescription: "Scores how well each trial is going and sends different onboarding to the ones racing ahead, the ones drifting, and the ones at risk."
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
      title: "Score how the trial is going"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "A trial health score from logins, use of the key features, team invites and data uploaded."
      prompt: "Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded)."
    - step: 2
      title: "Split trials into three tiers"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Highly engaged, moderate and at risk, off that score."
      prompt: "Segment trial users into risk tiers (high-engagement, moderate, at-risk) based on trial_health_score."
    - step: 3
      title: "Write onboarding per tier"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute, segment]
      description: "Content for each tier, leading with the features most likely to get that tier to its first real win."
      prompt: "Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier."
    - step: 4
      title: "Route each tier differently"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, asset]
      description: "One journey with a branch per tier, each running the education and conversion touches that tier needs."
      prompt: "Build a tiered onboarding journey routing each tier through appropriate education and conversion touches."
    - step: 5
      title: "Track trial to paid"
      command: build_funnel_report
      produces: report
      bindsAs: report
      dependsOn: [attribute, segment, asset, journey]
      description: "A funnel from signup to the first key event, then the second, then paid conversion, with retention laid over it."
      prompt: "Compose a funnel report tracking trial-signup to key-event-1 to key-event-2 to paid-conversion with retention overlay."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Trial to paid activation

Scores how well each trial is going and sends different onboarding to the ones racing ahead, the ones drifting, and the ones at risk.

## What it does

1. **Score how the trial is going** (`create_ai_attribute`)

   A trial health score from logins, use of the key features, team invites and data uploaded.

2. **Split trials into three tiers** (`create_segment`)

   Highly engaged, moderate and at risk, off that score.

3. **Write onboarding per tier** (`create_email_content`)

   Content for each tier, leading with the features most likely to get that tier to its first real win.

4. **Route each tier differently** (`create_journey`)

   One journey with a branch per tier, each running the education and conversion touches that tier needs.

5. **Track trial to paid** (`build_funnel_report`)

   A funnel from signup to the first key event, then the second, then paid conversion, with retention laid over it.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
