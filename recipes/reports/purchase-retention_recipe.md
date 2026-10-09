---
name: purchase-retention
description: |
  Use when a user mentions "purchase retention", or asks for related help. Repeat-purchase retention with cohort-level second-purchase rates and time-to-2nd-purchase distribution.
arguments: []
intempt:
  id: purchase-retention
  version: 1.0.0
  slashCommand: /purchase-retention
  group: Reports
  title: "Repeat purchase retention"
  shortDescription: "Shows what share of first time buyers come back to buy again, by month and by the category they bought first."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [retention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_retention_report
  procedure:
    - step: 1
      title: "Track buyers back for more"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Monthly cohorts by month of first order over 12 months, measuring repeat orders at months 1, 3, 6 and 12, split by first purchase category, plus a distribution of the days between the first and second order. Benchmarks the second purchase rate at 27%."
      prompt: |
        Create a Retention report called "Purchase Retention".

        Anchor event: Placed order (per user, scope: their first order to cohort by month of first purchase)
        Return event: Placed order (any subsequent order)
        Cohort granularity: Monthly
        Time range: Last 12 months
        Breakdown: By the first-purchase product category: taken from the first order's line items and resolved to the product category
        Compare: Previous period (prior 12 months of cohorts)
        Chart type: Retention curve plus cohort table with M1 / M3 / M6 / M12 columns

        Also include a secondary view: "Time from 1st to 2nd purchase" distribution: histogram of days-between, bucketed into 0-7 / 8-30 / 31-90 / 91+ days.

        Annotations:
        - Add benchmarks: 27% of first-time DTC buyers make a 2nd purchase ever; brands at 45%+ are top-quartile.
        - Flag any category where M6 repeat rate is below 15% (one-time-purchase pattern).
        - Flag any cohort where M3 repeat rate dropped >5 percentage points vs. prior cohort (recent acquisition-quality drop).
        - Highlight categories with M3 repeat rate > 30% (high natural-replenishment products: candidates for subscribe-and-save).

        Surface the median time from 1st to 2nd purchase per category: this is the right delay for replenishment journeys.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Repeat purchase retention

Shows what share of first time buyers come back to buy again, by month and by the category they bought first.

## What it does

1. **Track buyers back for more** (`build_retention_report`)

   Monthly cohorts by month of first order over 12 months, measuring repeat orders at months 1, 3, 6 and 12, split by first purchase category, plus a distribution of the days between the first and second order. Benchmarks the second purchase rate at 27%.

## What you end up with

- **report** (report): Report produced by this recipe.
