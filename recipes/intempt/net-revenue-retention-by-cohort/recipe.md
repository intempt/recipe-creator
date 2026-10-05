---
id: net-revenue-retention-by-cohort
title: Net revenue retention by cohort
slash_command: /net-revenue-retention-by-cohort
group: Reports
owner: intempt
curator: aman
summary: >-
  Tracks monthly cohort retention rates over time to measure ongoing customer and user engagement.
description: >-
  Build a cohort retention report tracking unique customer retention rates over successive months.
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
    - retention
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Track cohort revenue month by month"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track cohort revenue month by month
    summary: >-
      For each of the last 12 monthly cohorts of first paid subscriptions: starting revenue plus expansion
      and reactivation, minus contraction and churn, expressed as a percentage of that cohort's original
      revenue at every month after signup.
    builds: report
    description: |-
      Create a Retention report called "Net Revenue Retention by Cohort".
      Cohort: Monthly cohort defined by month of first paid subscription_created (trial_end is null OR a follow-on after-trial subscription_created) per user.
      For each cohort and each month-after-cohort N (M, M+1, M+2, ... M+12), compute the dollar values for users in the cohort:
      - Starting MRR (cohort's recurring revenue in month N-1) = Sum of revenue_completed.amount filtered to recurring type, for cohort users
      - Expansion MRR = Sum of positive amount-deltas from subscription_updated events in month N for cohort users (where the post-event amount exceeds the prior amount on the same subscription_id)
      - Reactivation MRR = Sum of subscription_resumed.amount in month N for cohort users who had a prior subscription_cancelled
      - Contraction MRR = Sum of negative amount-deltas from subscription_updated events (subtracted)
      - Churned MRR = Sum of the prior subscription amount for each subscription_cancelled in month N (subtracted)
      - Ending MRR = Starting + Expansion + Reactivation − Contraction − Churn
      - NRR for cohort at month N = Ending MRR / Original cohort revenue at month M × 100, unit: %
      Time range: Last 12 cohort-months
      Breakdown: By initial plan_name (the plan_name on the cohort-defining subscription_created)
      Chart type: Multi-line chart: X axis is months-since-cohort, Y axis is NRR %; each cohort is a line. Plus a stacked bar showing the per-component decomposition for the most recent cohort.
      Annotations:
      - Add benchmarks: NRR ≥ 100% (cohort growing in revenue despite churn); ≥ 110% (top-quartile); ≥ 120% (best-in-class).
      - Flag any cohort whose NRR at M+6 is below 90% (revenue erosion).
      - Highlight the cohort with the highest M+12 NRR.
      - Flag whether NRR is improving across cohorts over time (cohort-quality trend).
      Surface the trailing 12-month blended NRR (a single headline number) and whether the cohort-level trend is improving.
      Taxonomy notes:
      - The canonical taxonomy does not have separate subscription_upgraded/_downgraded/_reactivated events. Expansion and Contraction are computed by Lovable from subscription_updated by comparing pre/post amount on the same subscription_id. Reactivation is computed as subscription_resumed (or subscription_activated) where the same customer_id had a recent subscription_cancelled.
      - This recipe depends on subscription_updated firing reliably with sufficient detail (changed_fields, plan_items) for the delta computation. If the integration emits sparse subscription_updated, the report degrades to logo-retention only.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Net revenue retention by cohort

Tracks monthly cohort retention rates over time to measure ongoing customer and user engagement.

## Steps

1. **Track cohort revenue month by month** (builds report)

   For each of the last 12 monthly cohorts of first paid subscriptions: starting revenue plus expansion and reactivation, minus contraction and churn, expressed as a percentage of that cohort's original revenue at every month after signup.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Track cohort revenue month by month"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
