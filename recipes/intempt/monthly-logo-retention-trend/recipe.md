---
id: monthly-logo-retention-trend
title: Monthly logo retention
slash_command: /monthly-logo-retention-trend
group: Reports
owner: intempt
curator: aman
summary: >-
  Shows a single trailing logo-retention rate: the share of customers still subscribed at the end of the
  current period. Uses subscription status data for the current period.
description: >-
  Single trailing logo-retention rate for the current period. It reports the share of customers still
  subscribed at period end, without historical monthly reconstruction or a rolling average.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Track monthly customer retention"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track monthly customer retention
    summary: >-
      For each of the last 12 months: customers with an active subscription at the start, how many were
      still active at the end, and the resulting rate plus a 3 month rolling average, split by plan. Benchmarks
      at 95% for good and 97% for best in class.
    builds: report
    description: |-
      Create an Insights report called "Monthly Logo Retention Trend".
      Series A: For each calendar month M, count the unique customers who had an active subscription at the START of month M (no subscription_cancelled or subscription_expired before M-start)
      Series B: For the same cohort, count those who STILL have an active subscription at the END of month M (no subscription_cancelled or subscription_expired during M)
      Series C: Computed: Series B / Series A × 100, unit: %, label: "Monthly Logo Retention Rate"
      Series D: Trailing 3-month rolling average of Series C (smoother trend), label: "Logo Retention (3-mo rolling)"
      Time granularity: Monthly
      Time range: Last 12 months
      Breakdown: By plan_name (resolved from each user's subscription_created.plan_name at the START of month M)
      Compare: Year-over-year (same month previous year, dotted overlay)
      Chart type: Line chart with Series C and Series D as primary lines, plus a small-multiple of Series C per plan tier
      Annotations:
      - Add benchmarks: 95% monthly logo retention is industry-good for self-serve SaaS; 97%+ is best-in-class; <90% indicates retention issues that compound rapidly (90% monthly = 28% annual retention).
      - Flag any month where Series C dropped >2 percentage points vs. trailing-3-month average (acute churn spike).
      - Flag if Series D (rolling) has been declining for 3+ consecutive months (durable retention erosion).
      - Highlight the plan tier with the highest retention AND the one with the lowest: the gap between them is often the strongest pricing/positioning signal.
      - Surface the implied annualized retention rate (Series C compounded over 12 months) as a single callout for board reporting.
      Use case: the trend version of paid-user-retention's headline number. Where paid-user-retention shows the cohort table (deep dive), this recipe shows the single-line trend (headline metric for monthly review). Both are useful; this one is the dashboard-friendly version.
      Taxonomy notes:
      - subscription_created marks active subscription start (with plan_name, amount, trial_end). Filter for trial_end null to scope to paid (not trial) subscriptions.
      - subscription_cancelled and subscription_expired mark subscription end. subscription_paused is NOT counted as churn (paused subscriptions can resume).
      - "Active at start of month" computed by Lovable: subscription_created exists prior to month-start, with no terminal event before month-start.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Monthly logo retention

Shows a single trailing logo-retention rate: the share of customers still subscribed at the end of the current period. Uses subscription status data for the current period.

## Steps

1. **Track monthly customer retention** (builds report)

   For each of the last 12 months: customers with an active subscription at the start, how many were still active at the end, and the resulting rate plus a 3 month rolling average, split by plan. Benchmarks at 95% for good and 97% for best in class.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Track monthly customer retention"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
