---
name: monthly-logo-retention-trend
description: |
  Use when a user mentions "monthly logo retention trend", or asks for related help. Single trailing logo-retention rate over time — the headline number that pairs with NRR but answers a simpler question.
arguments: []
intempt:
  id: monthly-logo-retention-trend
  version: 1.0.0
  slashCommand: /monthly-logo-retention-trend
  group: Reports
  shortDescription: "Single trailing logo-retention rate over time — the headline number that pairs with NRR but answers a simpler question."
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
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Monthly Logo Retention Trend".

        Series A: For each calendar month M, count the unique customers who had an active subscription at the START of month M (no subscription_cancelled or subscription_expired before M-start)
        Series B: For the same cohort, count those who STILL have an active subscription at the END of month M (no subscription_cancelled or subscription_expired during M)
        Series C: Computed — Series B / Series A × 100, unit: %, label: "Monthly Logo Retention Rate"
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
        - Highlight the plan tier with the highest retention AND the one with the lowest — the gap between them is often the strongest pricing/positioning signal.
        - Surface the implied annualized retention rate (Series C compounded over 12 months) as a single callout for board reporting.

        Use case: the trend version of paid-user-retention's headline number. Where paid-user-retention shows the cohort table (deep dive), this recipe shows the single-line trend (headline metric for monthly review). Both are useful; this one is the dashboard-friendly version.

        Taxonomy notes:
        - subscription_created marks active subscription start (with plan_name, amount, trial_end). Filter for trial_end null to scope to paid (not trial) subscriptions.
        - subscription_cancelled and subscription_expired mark subscription end. subscription_paused is NOT counted as churn (paused subscriptions can resume).
        - "Active at start of month" computed by Lovable: subscription_created exists prior to month-start, with no terminal event before month-start.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Monthly Logo Retention Trend

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Monthly Logo Retention Trend".

   Series A: For each calendar month M, count the unique customers who had an active subscription at the START of month M (no subscription_cancelled or subscription_expired before M-start)
   Series B: For the same cohort, count those who STILL have an active subscription at the END of month M (no subscription_cancelled or subscription_expired during M)
   Series C: Computed — Series B / Series A × 100, unit: %, label: "Monthly Logo Retention Rate"
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
   - Highlight the plan tier with the highest retention AND the one with the lowest — the gap between them is often the strongest pricing/positioning signal.
   - Surface the implied annualized retention rate (Series C compounded over 12 months) as a single callout for board reporting.

   Use case: the trend version of paid-user-retention's headline number. Where paid-user-retention shows the cohort table (deep dive), this recipe shows the single-line trend (headline metric for monthly review). Both are useful; this one is the dashboard-friendly version.

   Taxonomy notes:
   - subscription_created marks active subscription start (with plan_name, amount, trial_end). Filter for trial_end null to scope to paid (not trial) subscriptions.
   - subscription_cancelled and subscription_expired mark subscription end. subscription_paused is NOT counted as churn (paused subscriptions can resume).
   - "Active at start of month" computed by Lovable: subscription_created exists prior to month-start, with no terminal event before month-start.
   ```
