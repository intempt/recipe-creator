---
name: stickiness-ratios-dau-wau-mau
description: |
  Use when a user mentions "dau/wau/mau stickiness ratios", or asks for related help. DAU, WAU, MAU with stickiness ratios (DAU/WAU and DAU/MAU): the standard PLG engagement metric.
arguments: []
intempt:
  id: stickiness-ratios-dau-wau-mau
  version: 1.0.0
  slashCommand: /stickiness-ratios-dau-wau-mau
  group: Reports
  title: "Daily, weekly and monthly stickiness"
  shortDescription: "Shows daily, weekly and monthly active users together with the ratios between them, the standard read on how habitual your product is."
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
      title: "Track daily against monthly use"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Daily active users, a rolling 7 day figure and a rolling 28 day figure over 90 days, with daily over weekly and daily over monthly as smoothed percentages split by plan. Benchmarks daily over monthly at 20% for good and 50% for best in class."
      prompt: |
        Create an Insights report called "DAU / WAU / MAU Stickiness".

        Series A: Event "session_start", aggregation: Count Unique Users, time granularity: Daily, label: "DAU"
        Series B: Event "session_start", aggregation: Count Unique Users, rolling 7-day window, label: "WAU"
        Series C: Event "session_start", aggregation: Count Unique Users, rolling 28-day window, label: "MAU"
        Series D: Computed: Series A / Series B × 100, unit: %, label: "DAU/WAU Stickiness"
        Series E: Computed: Series A / Series C × 100, unit: %, label: "DAU/MAU Stickiness"
        Time granularity: Daily (smooth Series D and E with 7-day rolling average to reduce noise)
        Time range: Last 90 days
        Breakdown: By plan_name: resolved from the user's most-recent active subscription
        Compare: Year-over-year (same 90-day window prior year)
        Chart type: Dual-axis: left axis user counts (A/B/C as lines), right axis stickiness % (D and E as lines)

        Annotations:
        - Add benchmarks: DAU/MAU ≥ 20% is "good" for B2B SaaS; ≥ 50% is best-in-class.
        - Add benchmarks: DAU/WAU ≥ 50% indicates strong daily-habit usage.
        - Flag any plan where DAU/MAU stickiness dropped >3 percentage points vs. previous period (engagement erosion: leading indicator of churn).
        - Flag any plan where MAU is growing but DAU is flat (acquiring users who aren't engaging).

        Stickiness leads retention by 1-2 quarters; it's the canary in the coal mine.

        Taxonomy notes:
        - session_start is the canonical "user is active" event. Alternative: identify, but session_start is more frequent and reliable.
        - plan_tier as a User property does not exist; plan_name comes from the user's subscription_created.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Daily, weekly and monthly stickiness

Shows daily, weekly and monthly active users together with the ratios between them, the standard read on how habitual your product is.

## What it does

1. **Track daily against monthly use** (`build_insights_report`)

   Daily active users, a rolling 7 day figure and a rolling 28 day figure over 90 days, with daily over weekly and daily over monthly as smoothed percentages split by plan. Benchmarks daily over monthly at 20% for good and 50% for best in class.

## What you end up with

- **report** (report): Report produced by this recipe.
