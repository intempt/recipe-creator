---
name: first-purchase-cohort-ltv-curve
description: |
  Use when a user mentions "first-purchase cohort ltv curve", or asks for related help. Cumulative revenue per cohort member by cohort age: the textbook DTC LTV view.
arguments: []
intempt:
  id: first-purchase-cohort-ltv-curve
  version: 1.0.0
  slashCommand: /first-purchase-cohort-ltv-curve
  group: Reports
  title: "First purchase LTV curve"
  shortDescription: "Shows cumulative revenue per customer for each monthly cohort as it ages, so you can see which acquisition months and channels pay back."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
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
      title: "Plot revenue per cohort by age"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Cumulative revenue per cohort member for each of the last 12 monthly cohorts, grouped by the month of a customer's first order and split by acquisition source. Marks cohorts that are still incomplete and flags any whose curve flattens by month 3 to 6."
      prompt: |
        Create an Insights report called "First-Purchase Cohort LTV Curve".

        Series A: Event "Placed order", aggregation: Sum of order total, scoped per user, cumulative from each user's first order
        Series B: Computed: Series A / cohort size, unit: $, label: "Cumulative Revenue per Cohort Member"
        Cohort: Monthly cohort defined by the month of a user's first order (each user's first order determines their cohort)
        Time range: Last 12 months of cohorts (allow some cohorts to have shorter LTV tails: surface "incomplete cohort" labels for the most recent ones)
        Breakdown: By UTM source (the user's first-touch acquisition channel)
        Chart type: Multi-line chart: each line is a cohort, X axis is cohort age in months (0, 1, 2, ..., 12), Y axis is cumulative revenue per cohort member

        Annotations:
        - Highlight the highest-LTV cohort and lowest-LTV cohort at month 6 and month 12.
        - Flag any cohort where LTV growth flattens prematurely (LTV-curve "going horizontal" by month 3-6 indicates a one-time-buyer cohort).
        - Highlight channels where cohort LTV is increasing across recent cohorts (acquisition quality improving).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# First purchase LTV curve

Shows cumulative revenue per customer for each monthly cohort as it ages, so you can see which acquisition months and channels pay back.

## What it does

1. **Plot revenue per cohort by age** (`build_insights_report`)

   Cumulative revenue per cohort member for each of the last 12 monthly cohorts, grouped by the month of a customer's first order and split by acquisition source. Marks cohorts that are still incomplete and flags any whose curve flattens by month 3 to 6.

## What you end up with

- **report** (report): Report produced by this recipe.
