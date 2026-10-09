---
name: expansion-revenue-trend
description: |
  Use when a user mentions "expansion revenue trend", or asks for related help. Expansion revenue derived from subscription updates with quality-of-MRR-growth surfacing.
arguments: []
intempt:
  id: expansion-revenue-trend
  version: 1.0.0
  slashCommand: /expansion-revenue-trend
  group: Reports
  title: "Expansion revenue trend"
  shortDescription: "Shows how much new revenue comes from existing customers upgrading or adding seats each month, and how that compares with revenue from new customers."
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
      title: "Split upgrades from seat growth"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Monthly expansion revenue over 12 months, separated into plan upgrades and seat or quantity increases, each taken from the amount change on a subscription update. Shown as a share of new monthly revenue, split by plan and compared year over year."
      prompt: |
        Create an Insights report called "Expansion Revenue Trend".

        Series A: Event "Subscription updated" where the change indicates a plan upgrade (the updated plan is higher-priced than the prior one), aggregation: Sum of the resulting subscription amount delta
          Computation: for each Subscription updated event, compare the new amount against the prior amount on the same subscription. Positive delta with a plan change = upgrade. Sum positive deltas, unit: $, label: "Upgrade Revenue".
        Series B: Event "Subscription updated" where the change indicates a seat or quantity increase (the number of seats went up), aggregation: Sum of positive amount delta, unit: $, label: "Seat / Quantity Expansion Revenue"
        Series C: Computed: (A + B) / new MRR in the period × 100, unit: %, label: "Expansion as % of New MRR"
          where new MRR = sum of the amount from each Subscription started in the period
        Time granularity: Monthly
        Breakdown: By plan: show which starting plan tiers produce the most expansion
        Time range: Last 12 months
        Compare: Year-over-year
        Chart type: Stacked bar for A and B with Series C as a line on a secondary axis

        Annotations:
        - Add benchmarks: expansion as % of new MRR ≥ 30% is healthy; ≥ 50% is best-in-class.
        - Flag any month where total expansion revenue declined MoM by more than 15% (expansion engine stalling).
        - Highlight whether upgrade-driven expansion or seat-driven expansion dominates, and whether the mix is shifting.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Expansion revenue trend

Shows how much new revenue comes from existing customers upgrading or adding seats each month, and how that compares with revenue from new customers.

## What it does

1. **Split upgrades from seat growth** (`build_insights_report`)

   Monthly expansion revenue over 12 months, separated into plan upgrades and seat or quantity increases, each taken from the amount change on a subscription update. Shown as a share of new monthly revenue, split by plan and compared year over year.

## What you end up with

- **report** (report): Report produced by this recipe.
