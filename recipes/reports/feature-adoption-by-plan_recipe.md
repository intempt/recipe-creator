---
name: feature-adoption-by-plan
description: |
  Use when a user mentions "feature adoption by plan", or asks for related help. Feature adoption by plan tier with adoption-rate trend and tier-specific feature affinity.
arguments: []
intempt:
  id: feature-adoption-by-plan
  version: 1.0.0
  slashCommand: /feature-adoption-by-plan
  group: Reports
  title: "Feature adoption by plan"
  shortDescription: "Shows which features each plan tier actually uses, as a share of that tier's active users, and whether adoption is rising or falling."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Map feature use to plan tier"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Unique users per feature over the last 30 days as a share of active users on the same plan, drawn as a heatmap of feature against tier, plus a 12 week trend per feature. Flags features that lower tiers ignore and any feature whose use is falling."
      prompt: |
        Create an Insights report called "Feature Adoption by Plan".

        Series A: Event "Click on" filtered by the feature a user clicked (a stable identifier for each feature surface, e.g. /feature/<feature-slug>), aggregation: Count Unique Users
        Series B: Computed: Series A / total active users in the same plan tier × 100, unit: %, label: "Adoption Rate"
        Breakdown: By feature on the X axis, secondary breakdown by plan (the user's most-recent plan) on the Y axis
        Time range: Last 30 days
        Compare: Previous period (prior 30 days)
        Chart type: Heatmap (feature on Y axis, plan tier on X axis), cell value = adoption rate %, color intensity scaled

        Also include a parallel view: per-feature adoption-rate trend over the last 12 weeks, broken down by plan tier: to show whether adoption is accelerating, flat, or declining per feature.

        Annotations:
        - Flag features with high adoption in higher tiers but low adoption in lower tiers (candidates to promote down-tier OR signs of plan-feature mismatch).
        - Flag features with declining adoption in any tier (deprecation candidate or UX issue).
        - Highlight features used by >40% of paying users: these are the load-bearing features whose performance and reliability matter most.
        - Highlight features where higher-tier users adopt at >2× the rate of lower-tier users (the best upgrade-pitch features).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Feature adoption by plan

Shows which features each plan tier actually uses, as a share of that tier's active users, and whether adoption is rising or falling.

## What it does

1. **Map feature use to plan tier** (`build_insights_report`)

   Unique users per feature over the last 30 days as a share of active users on the same plan, drawn as a heatmap of feature against tier, plus a 12 week trend per feature. Flags features that lower tiers ignore and any feature whose use is falling.

## What you end up with

- **report** (report): Report produced by this recipe.
