---
name: monthly-logo-retention-trend
description: |
  Use when a user mentions "monthly logo retention trend", or asks for related help. Single trailing logo-retention rate over time: the headline number that pairs with NRR but answers a simpler question.
arguments: []
intempt:
  id: monthly-logo-retention-trend
  version: 1.0.0
  slashCommand: /monthly-logo-retention-trend
  group: Reports
  title: "Monthly logo retention"
  shortDescription: "Shows what share of your customers were still subscribed at the end of each month, as a monthly rate and a smoother 3 month average."
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
      title: "Track monthly customer retention"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "For each of the last 12 months: customers with an active subscription at the start, how many were still active at the end, and the resulting rate plus a 3 month rolling average, split by plan. Benchmarks at 95% for good and 97% for best in class."
      prompt: |
        Create an Insights report called "Monthly Logo Retention Trend".

        Series A: For each calendar month M, count the unique customers who had an active subscription at the START of month M (no Subscription canceled or Subscription expired before M-start)
        Series B: For the same cohort, count those who STILL have an active subscription at the END of month M (no Subscription canceled or Subscription expired during M)
        Series C: Computed: Series B / Series A × 100, unit: %, label: "Monthly Logo Retention Rate"
        Series D: Trailing 3-month rolling average of Series C (smoother trend), label: "Logo Retention (3-mo rolling)"

        Time granularity: Monthly
        Time range: Last 12 months
        Breakdown: By Plan (resolved from each user's active subscription at the START of month M)
        Compare: Year-over-year (same month previous year, dotted overlay)
        Chart type: Line chart with Series C and Series D as primary lines, plus a small-multiple of Series C per plan tier

        Annotations:
        - Add benchmarks: 95% monthly logo retention is industry-good for self-serve SaaS; 97%+ is best-in-class; <90% indicates retention issues that compound rapidly (90% monthly = 28% annual retention).
        - Flag any month where Series C dropped >2 percentage points vs. trailing-3-month average (acute churn spike).
        - Flag if Series D (rolling) has been declining for 3+ consecutive months (durable retention erosion).
        - Highlight the plan tier with the highest retention AND the one with the lowest: the gap between them is often the strongest pricing/positioning signal.
        - Surface the implied annualized retention rate (Series C compounded over 12 months) as a single callout for board reporting.

        Use case: the trend version of paid-user-retention's headline number. Where paid-user-retention shows the cohort table (deep dive), this recipe shows the single-line trend (headline metric for monthly review). Both are useful; this one is the dashboard-friendly version.

        Scope rules:
        - Count a subscription as active only when it is a paid (non-trial) subscription.
        - A paused subscription is NOT counted as churn, because paused subscriptions can resume.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Monthly logo retention

Shows what share of your customers were still subscribed at the end of each month, as a monthly rate and a smoother 3 month average.

## What it does

1. **Track monthly customer retention** (`build_insights_report`)

   For each of the last 12 months: customers with an active subscription at the start, how many were still active at the end, and the resulting rate plus a 3 month rolling average, split by plan. Benchmarks at 95% for good and 97% for best in class.

## What you end up with

- **report** (report): Report produced by this recipe.
