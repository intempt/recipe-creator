---
name: feature-discovery-adoption
description: |
  Use when a user mentions "feature discovery to adoption", or asks for related help. 4-step funnel from first feature exposure to repeated use.
arguments: []
intempt:
  id: feature-discovery-adoption
  version: 1.0.0
  slashCommand: /feature-discovery-adoption
  group: Reports
  title: "Feature discovery to adoption"
  shortDescription: "Shows how many people who find a feature go on to try it, use it repeatedly, and make it a habit."
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
      title: "Follow a feature from first look"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A four step funnel over 21 days from first exposure to a feature, to first use, to three or more uses, to use on three separate days in the last five. Flags features found by more than 1000 people that fewer than 5% stick with."
      prompt: |
        Create a Funnel report called "Feature Discovery to Adoption".

        Steps:
        1. Event "View page" where the page URL contains the feature path: "Discovered Feature" (first exposure)
           (alternative: Click on where the clicked element matches a feature-tour or tooltip)
        2. Event "Click on" where the clicked element matches the feature's interaction control: "Tried Feature" (first use)
        3. Event "Click on" on the same feature control as Step 2, count >= 3 by the same user within 21 days: "Used 3+ Times"
        4. Event "Click on" on the same feature control, frequency: at least 3 distinct days of use in the last 5 days: "Habitual User"

        Conversion window: 21 days
        Breakdown: By feature
        Compare: Previous period (prior 21 days)

        For each feature, also surface:
        - Discovery to Habitual conversion rate (Step 4 / Step 1)
        - Median time-to-habitual (days from discovery to habitual)

        Annotations:
        - Flag features with discovery > 1000 users AND habitual conversion < 5%: high-discovery, low-stickiness; investigate UX.
        - Flag features where discovery to trial conversion < 20%: discovery moment isn't compelling.
        - Highlight features with discovery to habitual conversion > 25%: surface candidates for promotion.

        Surface the top 3 features by absolute habitual-user count and the top 3 by habitual-conversion rate.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Feature discovery to adoption

Shows how many people who find a feature go on to try it, use it repeatedly, and make it a habit.

## What it does

1. **Follow a feature from first look** (`build_funnel_report`)

   A four step funnel over 21 days from first exposure to a feature, to first use, to three or more uses, to use on three separate days in the last five. Flags features found by more than 1000 people that fewer than 5% stick with.

## What you end up with

- **report** (report): Report produced by this recipe.
