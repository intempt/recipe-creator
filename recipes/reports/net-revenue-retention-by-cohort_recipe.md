---
name: net-revenue-retention-by-cohort
description: |
  Use when a user mentions "net revenue retention by cohort", or asks for related help. Proper NRR per cohort: starting MRR + expansion + reactivation − contraction − churn. Requires computing the amount change on each subscription update.
arguments: []
intempt:
  id: net-revenue-retention-by-cohort
  version: 1.0.0
  slashCommand: /net-revenue-retention-by-cohort
  group: Reports
  title: "Net revenue retention by cohort"
  shortDescription: "Tracks what each monthly cohort of paying customers is worth over time once upgrades, downgrades, churn and reactivations are all counted."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
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
      title: "Track cohort revenue month by month"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "For each of the last 12 monthly cohorts of first paid subscriptions: starting revenue plus expansion and reactivation, minus contraction and churn, expressed as a percentage of that cohort's original revenue at every month after signup."
      prompt: |
        Create a Retention report called "Net Revenue Retention by Cohort".

        Cohort: Monthly cohort defined by the month of each user's first paid subscription (a Subscription started with no trial end, or a follow-on Subscription started after a trial).

        For each cohort and each month-after-cohort N (M, M+1, M+2, ... M+12), compute the dollar values for users in the cohort:

        - Starting MRR (cohort's recurring revenue in month N-1) = Sum of the recurring Revenue completed amount, for cohort users
        - Expansion MRR = Sum of positive amount-deltas from Subscription updated events in month N for cohort users (where the post-event amount exceeds the prior amount on the same subscription)
        - Reactivation MRR = Sum of the Subscription resumed amount in month N for cohort users who had a prior Subscription canceled
        - Contraction MRR = Sum of negative amount-deltas from Subscription updated events (subtracted)
        - Churned MRR = Sum of the prior subscription amount for each Subscription canceled in month N (subtracted)
        - Ending MRR = Starting + Expansion + Reactivation − Contraction − Churn
        - NRR for cohort at month N = Ending MRR / Original cohort revenue at month M × 100, unit: %

        Time range: Last 12 cohort-months
        Breakdown: By initial Plan (the Plan on the cohort-defining Subscription started event)
        Chart type: Multi-line chart: X axis is months-since-cohort, Y axis is NRR %; each cohort is a line. Plus a stacked bar showing the per-component decomposition for the most recent cohort.

        Annotations:
        - Add benchmarks: NRR ≥ 100% (cohort growing in revenue despite churn); ≥ 110% (top-quartile); ≥ 120% (best-in-class).
        - Flag any cohort whose NRR at M+6 is below 90% (revenue erosion).
        - Highlight the cohort with the highest M+12 NRR.
        - Flag whether NRR is improving across cohorts over time (cohort-quality trend).

        Surface the trailing 12-month blended NRR (a single headline number) and whether the cohort-level trend is improving.

        Deriving the movement split:
        - Expansion and Contraction are computed by comparing the new amount to the prior amount on each subscription update: positive deltas are expansion, negative deltas are contraction.
        - Reactivation is a resumed (or reactivated) subscription where the same customer had a recent cancellation.
        - This recipe depends on subscription updates firing reliably with enough detail for the delta computation. If subscription updates are sparse, the report degrades to logo-retention only.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Net revenue retention by cohort

Tracks what each monthly cohort of paying customers is worth over time once upgrades, downgrades, churn and reactivations are all counted.

## What it does

1. **Track cohort revenue month by month** (`build_retention_report`)

   For each of the last 12 monthly cohorts of first paid subscriptions: starting revenue plus expansion and reactivation, minus contraction and churn, expressed as a percentage of that cohort's original revenue at every month after signup.

## What you end up with

- **report** (report): Report produced by this recipe.
