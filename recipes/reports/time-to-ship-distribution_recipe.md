---
name: time-to-ship-distribution
description: |
  Use when a user mentions "time-to-ship distribution", or asks for related help. Histogram of fulfillment time per order with median/p75/p95 callouts and bucket-level operational benchmarks.
arguments: []
intempt:
  id: time-to-ship-distribution
  version: 1.0.0
  slashCommand: /time-to-ship-distribution
  group: Reports
  title: "Time to ship"
  shortDescription: "Shows how long orders take to ship, bucketed from same day out past two weeks, with median, 75th and 95th percentile callouts."
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
      title: "Measure how fast orders ship"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "A distribution of the time between an order being created and fulfilled, across the last 30 days of fulfilments, bucketed from under 24 hours to over 14 days and split by fulfilment source or country. Benchmarks 24 hours as top quartile."
      prompt: |
        Create an Insights report called "Time-to-Ship Distribution".

        Series A: Distribution histogram of fulfillment time per order: computed by Lovable as the time between when an order was placed and when it was fulfilled, for each fulfilled order, matched on the order

        Buckets for Series A: 0 (24h / 24) 48h / 48 (72h / 3) 5 days / 5 (7 days / 7) 14 days / 14+ days
        Series B: Cumulative percentage: what % of orders ship within X time

        Time range: Last 30 days of Order fulfilled events (use the fulfillment date for cohorting, since orders fulfilled in the period may have been created before)
        Breakdown: By the fulfillment source (warehouse, fulfillment center, or 3PL: varies by integration) OR by the user's country for geographic distribution analysis
        Compare: Previous period (prior 30 days)
        Chart type: Histogram chart with Series A as the bar distribution, Series B as a cumulative line overlay; secondary callouts for median, p75, p95 fulfillment times

        Annotations:
        - Add benchmarks: top-quartile DTC ships within 24h (Amazon-trained customer expectations); 24: 48h is industry median; >72h to first ship is competitively weak.
        - Flag if the share shipping within 24h dropped >10 percentage points vs. previous period (operational regression).
        - Flag the long tail: what % of orders take >7 days to ship? Anything above 5% is a fulfillment-process problem and a customer-experience issue (these customers are likely to complain or refund).
        - Highlight the median and p75 times as headline numbers: the median is the typical experience, p75 is the experience customers complain about, p95 is the experience that drives bad reviews.
        - Surface any source/warehouse with materially worse times than others: single facility issues are easier to fix than systemic ones.

        Use case: post-purchase customer experience is increasingly a competitive lever. Brands that ship fast retain better. This recipe makes the actual time-to-ship distribution visible (most ops dashboards only show "average ship time" which obscures the long tail).

        This report excludes orders that have not been fulfilled yet (no Order fulfilled event). For an in-flight backlog view, pair this recipe with order-status-flow.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Time to ship

Shows how long orders take to ship, bucketed from same day out past two weeks, with median, 75th and 95th percentile callouts.

## What it does

1. **Measure how fast orders ship** (`build_insights_report`)

   A distribution of the time between an order being created and fulfilled, across the last 30 days of fulfilments, bucketed from under 24 hours to over 14 days and split by fulfilment source or country. Benchmarks 24 hours as top quartile.

## What you end up with

- **report** (report): Report produced by this recipe.
