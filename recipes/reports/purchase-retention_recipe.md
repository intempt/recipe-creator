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
  shortDescription: "Repeat-purchase retention with cohort-level second-purchase rates and time-to-2nd-purchase distribution."
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
      title: "Build Retention Report"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Retention report called "Purchase Retention".

        Anchor event: order_created (per user, scope: their first order_created → cohort by month of first purchase)
        Return event: order_created (any subsequent order)
        Cohort granularity: Monthly
        Time range: Last 12 months
        Breakdown: By the first-purchase product category — derived from the first order's items.product_id resolved via Products object
        Compare: Previous period (prior 12 months of cohorts)
        Chart type: Retention curve plus cohort table with M1 / M3 / M6 / M12 columns

        Also include a secondary view: "Time from 1st to 2nd purchase" distribution — histogram of days-between, bucketed into 0-7 / 8-30 / 31-90 / 91+ days.

        Annotations:
        - Add benchmarks: 27% of first-time DTC buyers make a 2nd purchase ever; brands at 45%+ are top-quartile.
        - Flag any category where M6 repeat rate is below 15% (one-time-purchase pattern).
        - Flag any cohort where M3 repeat rate dropped >5 percentage points vs. prior cohort (recent acquisition-quality drop).
        - Highlight categories with M3 repeat rate > 30% (high natural-replenishment products — candidates for subscribe-and-save).

        Surface the median time from 1st to 2nd purchase per category — this is the right delay for replenishment journeys.

        Taxonomy notes:
        - "first_order_created" as an event does not exist. "First order" is computed as the earliest order_created per customer_id.
        - "first_purchase_category" is derived from first order's items.product_id → Products.category.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Purchase Retention

## Procedure

1. **Build Retention Report** [`build_retention_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Retention report called "Purchase Retention".

   Anchor event: order_created (per user, scope: their first order_created → cohort by month of first purchase)
   Return event: order_created (any subsequent order)
   Cohort granularity: Monthly
   Time range: Last 12 months
   Breakdown: By the first-purchase product category — derived from the first order's items.product_id resolved via Products object
   Compare: Previous period (prior 12 months of cohorts)
   Chart type: Retention curve plus cohort table with M1 / M3 / M6 / M12 columns

   Also include a secondary view: "Time from 1st to 2nd purchase" distribution — histogram of days-between, bucketed into 0-7 / 8-30 / 31-90 / 91+ days.

   Annotations:
   - Add benchmarks: 27% of first-time DTC buyers make a 2nd purchase ever; brands at 45%+ are top-quartile.
   - Flag any category where M6 repeat rate is below 15% (one-time-purchase pattern).
   - Flag any cohort where M3 repeat rate dropped >5 percentage points vs. prior cohort (recent acquisition-quality drop).
   - Highlight categories with M3 repeat rate > 30% (high natural-replenishment products — candidates for subscribe-and-save).

   Surface the median time from 1st to 2nd purchase per category — this is the right delay for replenishment journeys.

   Taxonomy notes:
   - "first_order_created" as an event does not exist. "First order" is computed as the earliest order_created per customer_id.
   - "first_purchase_category" is derived from first order's items.product_id → Products.category.
   ```
