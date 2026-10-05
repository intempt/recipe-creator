---
name: post-purchase-second-order-velocity
description: |
  Use when a user mentions "post-purchase second-order velocity", or asks for related help. Histogram of days from 1st to 2nd order_created — informs the right delay for replenishment journey triggers.
arguments: []
intempt:
  id: post-purchase-second-order-velocity
  version: 1.0.0
  slashCommand: /post-purchase-second-order-velocity
  group: Reports
  shortDescription: "Insights report showing histogram and cumulative percentage of days between first and second order_created for repeat buyers."
  availability: coming-soon
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
        Create an Insights report called "Time from 1st to 2nd Purchase".

        Series A: Distribution histogram of days between each user's 1st order_created and 2nd order_created (only users who have at least 2 orders)
        Series B: Cumulative percentage — what % of repeat-buyers make their 2nd purchase within X days

        Buckets for Series A: 0-3 days / 4-7 days / 8-14 days / 15-30 days / 31-60 days / 61-90 days / 91-180 days / 181-365 days / 365+ days

        Time range: Users whose 1st order was 6+ months ago (so we have a full follow-up window for measuring 2nd-purchase timing)
        Breakdown: By first-order product category (derived from first order_created.items → Products.category) — top 6 categories
        Compare: Previous period (cohorts whose 1st order was 12-18 months ago — answers: is repeat-velocity getting faster or slower?)
        Chart type: Histogram chart with the cumulative % overlay as a secondary line

        Annotations:
        - Highlight the median time-to-second-purchase per category — this is the right delay to set on replenishment journey triggers.
        - Flag any category where median time-to-second-purchase is <14 days (high-velocity replenishment — candidate for subscribe-and-save offering).
        - Flag any category where median time-to-second-purchase is >180 days (long-cycle category — replenishment journeys should fire at 6-9 months, not 30 days).
        - Highlight the share of repeat-buyers who returned within 30 days (the "early loyalty" group). This share growing over time = improving retention; shrinking = deteriorating.

        Use case: distinct from the existing purchase-retention recipe (which is cohort %). This is the histogram that tells you the actual time distribution — critical for journey-trigger timing. Most brands use a generic 30-day or 60-day replenishment delay; this recipe surfaces the right delay per category.

        Taxonomy notes:
        - "First order" and "second order" per user are derived from the temporal order of order_created events for the same customer_id.
        - order_created.items contains product_id which resolves to category via the Products record-object.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Post-Purchase Second-Order Velocity

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Time from 1st to 2nd Purchase".

   Series A: Distribution histogram of days between each user's 1st order_created and 2nd order_created (only users who have at least 2 orders)
   Series B: Cumulative percentage — what % of repeat-buyers make their 2nd purchase within X days

   Buckets for Series A: 0-3 days / 4-7 days / 8-14 days / 15-30 days / 31-60 days / 61-90 days / 91-180 days / 181-365 days / 365+ days

   Time range: Users whose 1st order was 6+ months ago (so we have a full follow-up window for measuring 2nd-purchase timing)
   Breakdown: By first-order product category (derived from first order_created.items → Products.category) — top 6 categories
   Compare: Previous period (cohorts whose 1st order was 12-18 months ago — answers: is repeat-velocity getting faster or slower?)
   Chart type: Histogram chart with the cumulative % overlay as a secondary line

   Annotations:
   - Highlight the median time-to-second-purchase per category — this is the right delay to set on replenishment journey triggers.
   - Flag any category where median time-to-second-purchase is <14 days (high-velocity replenishment — candidate for subscribe-and-save offering).
   - Flag any category where median time-to-second-purchase is >180 days (long-cycle category — replenishment journeys should fire at 6-9 months, not 30 days).
   - Highlight the share of repeat-buyers who returned within 30 days (the "early loyalty" group). This share growing over time = improving retention; shrinking = deteriorating.

   Use case: distinct from the existing purchase-retention recipe (which is cohort %). This is the histogram that tells you the actual time distribution — critical for journey-trigger timing. Most brands use a generic 30-day or 60-day replenishment delay; this recipe surfaces the right delay per category.

   Taxonomy notes:
   - "First order" and "second order" per user are derived from the temporal order of order_created events for the same customer_id.
   - order_created.items contains product_id which resolves to category via the Products record-object.
   ```
