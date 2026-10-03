---
id: customer-lifecycle-distribution
title: Customer lifecycle distribution
slash_command: /customer-lifecycle-distribution
group: Reports
owner: intempt
summary: Shows how your customers are spread across the six lifecycle stages today, how much revenue sits
  in each, and who moved between stages in the last month.
description: >-
  Distribution of customers across the canonical lifecycle stages (At risk, Needs attention, New customers,
  Promising, Regulars, Champions) with month-over-month migration tracking.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: quick
  executionMode: live
  tags:
    - insights
steps:
  - id: s1
    title: Map customers to lifecycle stages
    summary: >-
      A snapshot count of customers in each of the six stages (At risk, Needs attention, New customers,
      Promising, Regulars, Champions) with lifetime value, recency and average order value per stage,
      compared against 30 and 90 days ago, plus a view of who moved where.
    builds: report
    description: |-
      Create an Insights report called "Customer Lifecycle Distribution".
      Series A: Count Unique Users grouped by Users.lifecycle_score: the canonical lifecycle enum with exactly six values:
       - At risk
       - Needs attention
       - New customers
       - Promising
       - Regulars
       - Champions
      Series B: Sum of Users.lifetime_value per lifecycle stage (revenue concentration view)
      Series C: Computed: Series B / total LTV × 100, unit: %, label: "Share of Total LTV"
      Series D: Average of Users.days_since_last_activity per lifecycle stage (recency context)
      Series E: Average of Users.avg_order_value per lifecycle stage (basket-size context)
      Time range: Current snapshot
      Compare: Same snapshot 30 days ago AND 90 days ago (lifecycle migration over 1 month and 1 quarter)
      Chart type: Stacked bar chart with each bar = a lifecycle stage, plus side panels showing:
       - Series C (% of LTV per stage)
       - Series D (recency average per stage)
       - Series E (AOV per stage)
      Migration view (secondary):
      - For each pair of stages, surface the count of users who moved from stage X to stage Y over the last 30 days
      - Render as a Sankey-style flow diagram or a simple migration table with the 6×6 transitions
      - Highlight the dominant migrations: which lifecycle transitions are happening most?
      Annotations:
      - Highlight the top 2 stages by share of customers (volume) AND the top 2 by share of LTV (value). In healthy distributions, "Champions" + "Regulars" hold a small share of customers but a disproportionate share of LTV: this is the desired pattern.
      - Flag if "At risk" + "Needs attention" stages together hold >25% of total LTV: high-value customers are slipping; immediate retention action required.
      - Flag if "Champions" stage shrunk >10% in customer count vs. snapshot 30 days ago: your best customers are decaying; investigate which migrations they're moving INTO ("Regulars" is healthy aging; "At risk" is alarming).
      - Flag if "New customers" stage grew but "Promising" stage didn't grow proportionally a month later: the new-customer-to-promising progression is broken; first-purchase users aren't being properly nurtured.
      - Surface the largest single migration over the period (e.g. "147 users moved from Regulars to At risk this month"): this is the at-risk cohort that warrants targeted re-engagement.
      - Add benchmarks for healthy share-of-customers distribution: Champions 5-10%, Regulars 15-25%, Promising 15-20%, New customers 10-20%, Needs attention 15-25%, At risk 10-20%. Distributions skewed toward "At risk" + "Needs attention" indicate retention erosion; distributions skewed toward "New customers" without "Regulars" growing indicate weak repeat-purchase mechanics.
      Use case: the canonical CRM segmentation view. Every direct-to-consumer brand needs lifecycle visibility; this recipe materializes it directly from the platform's pre-computed Users.lifecycle_score attribute (which is maintained automatically based on RFM scoring). The migration view is the high-leverage piece: the single number "Champions: 8%" is less actionable than "147 Regulars moved to At risk this month."
      Taxonomy notes:
      - Users.lifecycle_score is the canonical platform-maintained lifecycle enum with exactly the six values listed above. Do NOT invent additional segments (no "Loyal," no "Hibernating," no "Lost," no "Can't Lose Them"): these are common in textbook RFM frameworks but are not part of Intempt's canonical lifecycle taxonomy.
      - Users.recency_score, frequency_score, monetary_score are separate enum attributes (the inputs that feed lifecycle_score) but should NOT be used as cross-tab dimensions in this recipe: they're the components, not the segmentation. If R/F/M-cube cross-tab analysis is needed, that's a different recipe.
      - Users.lifetime_value, days_since_last_activity, avg_order_value are real computed numeric attributes on the Users object.
      - Migration analysis is computed by Lovable from snapshots of lifecycle_score taken at different points in time. The platform should retain or version lifecycle_score history to enable this.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Customer lifecycle distribution

Shows how your customers are spread across the six lifecycle stages today, how much revenue sits in each, and who moved between stages in the last month.

## Steps

1. **Map customers to lifecycle stages** (builds report)

   A snapshot count of customers in each of the six stages (At risk, Needs attention, New customers, Promising, Regulars, Champions) with lifetime value, recency and average order value per stage, compared against 30 and 90 days ago, plus a view of who moved where.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
