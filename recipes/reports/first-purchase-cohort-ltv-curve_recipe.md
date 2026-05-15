---
name: first-purchase-cohort-ltv-curve
description: |
  Use when a user mentions "first-purchase cohort ltv curve", or asks for related help. Cumulative revenue per cohort member by cohort age — the textbook DTC LTV view.
arguments: []
intempt:
  id: first-purchase-cohort-ltv-curve
  version: 1.0.0
  slashCommand: /first-purchase-cohort-ltv-curve
  group: Reports
  shortDescription: "Cumulative revenue per cohort member by cohort age — the textbook DTC LTV view."
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
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "First-Purchase Cohort LTV Curve".

        Series A: Event "order_created", aggregation: Sum of "total_price", scoped per user, cumulative from each user's first order_created
        Series B: Computed — Series A / cohort size, unit: $, label: "Cumulative Revenue per Cohort Member"
        Cohort: Monthly cohort defined by month of first order_created (each user's first order_created event determines their cohort)
        Time range: Last 12 months of cohorts (allow some cohorts to have shorter LTV tails — surface "incomplete cohort" labels for the most recent ones)
        Breakdown: By Users.utm_source (the user's first-touch acquisition channel, from the Users object)
        Chart type: Multi-line chart — each line is a cohort, X axis is cohort age in months (0, 1, 2, ..., 12), Y axis is cumulative revenue per cohort member

        Annotations:
        - Highlight the highest-LTV cohort and lowest-LTV cohort at month 6 and month 12.
        - Flag any cohort where LTV growth flattens prematurely (LTV-curve "going horizontal" by month 3-6 indicates a one-time-buyer cohort).
        - Highlight channels where cohort LTV is increasing across recent cohorts (acquisition quality improving).

        Taxonomy notes:
        - "First purchase" is determined per-user by the earliest order_created event for that customer_id.
        - Users.utm_source is a real first-touch attribution attribute on the Users object.
        - LTV is cumulative sum of order_created.total_price per user from first purchase onward.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# First-Purchase Cohort LTV Curve

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "First-Purchase Cohort LTV Curve".

   Series A: Event "order_created", aggregation: Sum of "total_price", scoped per user, cumulative from each user's first order_created
   Series B: Computed — Series A / cohort size, unit: $, label: "Cumulative Revenue per Cohort Member"
   Cohort: Monthly cohort defined by month of first order_created (each user's first order_created event determines their cohort)
   Time range: Last 12 months of cohorts (allow some cohorts to have shorter LTV tails — surface "incomplete cohort" labels for the most recent ones)
   Breakdown: By Users.utm_source (the user's first-touch acquisition channel, from the Users object)
   Chart type: Multi-line chart — each line is a cohort, X axis is cohort age in months (0, 1, 2, ..., 12), Y axis is cumulative revenue per cohort member

   Annotations:
   - Highlight the highest-LTV cohort and lowest-LTV cohort at month 6 and month 12.
   - Flag any cohort where LTV growth flattens prematurely (LTV-curve "going horizontal" by month 3-6 indicates a one-time-buyer cohort).
   - Highlight channels where cohort LTV is increasing across recent cohorts (acquisition quality improving).

   Taxonomy notes:
   - "First purchase" is determined per-user by the earliest order_created event for that customer_id.
   - Users.utm_source is a real first-touch attribution attribute on the Users object.
   - LTV is cumulative sum of order_created.total_price per user from first purchase onward.
   ```
