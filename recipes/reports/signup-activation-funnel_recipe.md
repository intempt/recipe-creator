---
name: signup-activation-funnel
description: |
  Use when a user mentions "signup to activation funnel", or asks for related help. Signup-to-activation funnel from user signup to the first activation goal, with per-step time-to-convert.
arguments: []
intempt:
  id: signup-activation-funnel
  version: 1.0.0
  slashCommand: /signup-activation-funnel
  group: Reports
  title: "Signup to activation"
  shortDescription: "Shows how many new signups come back, use the core feature and activate within two weeks, and which signup source produces the best ones."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Follow signups to activation"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A four step funnel over 14 days from signup to a return session within 24 hours, core feature use and activation, split by the top 6 signup sources, with median and 75th percentile timings. Benchmarks activation at 30% and flags sources under 15%."
      prompt: |
        Create a Funnel report called "Signup to Activation".

        Steps:
        1. Event "User created": "Signed Up"
        2. Event "Session start" within 24 hours of signup: "Returned After Signup" (proxy for engagement after creation)
        3. Event "Completed a journey goal" where the goal is the onboarding/activation goal: "Used Core Feature"
        4. Event "Completed a journey goal" where the goal is the activation goal AND it happened within 14 days of signup: "Activated"

        Conversion window: 14 days
        Breakdown: By signup source (first-touch UTM source): top 6 channels: organic, paid_search, paid_social, content, referral, direct
        Compare: Previous period (prior 14 days)

        For each step, also surface:
        - Median and 75th-percentile time-to-convert from previous step
        - Per-source conversion rate at each stage

        Annotations:
        - Add benchmark: activation rate (Step 4 / Step 1) of 30% is typical PLG SaaS.
        - Flag any source with activation rate <15% (poor lead quality or onboarding mismatch).
        - Flag any step where median time-to-convert exceeds 24 hours for "Returned After Signup" or 7 days for "Used Core Feature".
        - Highlight sources with activation rate >40%.

        Identify which signup source produces the highest-activating users at sufficient volume.

        There is no separate signup-complete or onboarding-start event; the activation journey records a completed goal when the user reaches the activation goal.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Signup to activation

Shows how many new signups come back, use the core feature and activate within two weeks, and which signup source produces the best ones.

## What it does

1. **Follow signups to activation** (`build_funnel_report`)

   A four step funnel over 14 days from signup to a return session within 24 hours, core feature use and activation, split by the top 6 signup sources, with median and 75th percentile timings. Benchmarks activation at 30% and flags sources under 15%.

## What you end up with

- **report** (report): Report produced by this recipe.
