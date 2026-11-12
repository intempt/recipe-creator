---
frontmatter_id: monthly-logo-retention-trend
slash_command: /monthly-logo-retention-trend
description: 'Shows a single trailing logo-retention rate: the share of customers still subscribed at the end of the current period. Uses subscription status data for the current period.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows the monthly logo retention rate and its 3-month rolling trend by plan, with benchmarks, churn-spike flags,
    and an annualized retention callout for board reporting.
  parameters:
  - name: trend_window_months
    type: number
    label: Time range (months)
    default: 12
    required: false
  - name: rolling_window_months
    type: number
    label: Rolling average window (months)
    default: 3
    required: false
  - name: spike_threshold_points
    type: number
    label: Churn spike threshold (percentage points below trailing average)
    default: 2
    required: false
  - name: decline_months
    type: number
    label: Consecutive declining months that trigger an erosion flag
    default: 3
    required: false
  - name: benchmark_good_pct
    type: number
    label: Industry-good monthly logo retention (%)
    default: 95
    required: false
  - name: benchmark_best_pct
    type: number
    label: Best-in-class monthly logo retention (%)
    default: 97
    required: false
  - name: benchmark_risk_pct
    type: number
    label: Retention issue threshold (%)
    default: 90
    required: false
  requirements:
  - slot: subscription_started
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: Plan
      type: string
      meaning: Subscription plan tier
      optional: false
    - name: trial_end
      type: date
      meaning: Trial end date; empty for paid subscriptions
      optional: true
  - slot: subscription_canceled
    kind: event
    meaning: A customer canceled a subscription
  - slot: subscription_expired
    kind: event
    meaning: A customer subscription expired
  - slot: subscription_paused
    kind: event
    meaning: A customer paused a subscription (not counted as churn)
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - subscription_started
    - subscription_canceled
    - subscription_expired
    - trend_window_months
    - rolling_window_months
    - spike_threshold_points
    - decline_months
    - benchmark_good_pct
    - benchmark_best_pct
    - benchmark_risk_pct
    instruction: Create an Insights report titled "Monthly Logo Retention Trend" with monthly granularity over the last {trend_window_months}
      months. Scope to paid subscriptions by filtering {subscription_started.trial_end} to empty. For each calendar month
      M, define the cohort as unique customers with a {subscription_started} event before the start of M and no {subscription_canceled}
      or {subscription_expired} event before the start of M. Series A is the cohort count. Series B is the number of cohort
      members with no {subscription_canceled} or {subscription_expired} event during M. Series C is Series B divided by Series
      A times 100, in %, labeled "Monthly Logo Retention Rate". Series D is the trailing {rolling_window_months}-month rolling
      average of Series C, labeled "Logo Retention ({rolling_window_months}-mo rolling)". Break down by {subscription_started.Plan}
      as resolved at the start of month M. Compare year over year using a dotted overlay of the same month in the prior year.
      Chart as a line chart with Series C and Series D as primary lines, plus a small multiple of Series C per plan tier.
      Pause events from {subscription_paused} are not churn and must be excluded from the churn counts.
---

# Monthly logo retention

Slash command: /monthly-logo-retention-trend

## Step 1: Track monthly customer retention

Create an Insights report called "Monthly Logo Retention Trend".
Series A: For each calendar month M, count the unique customers who had an active subscription at the START of month M (no Subscription canceled or subscription_expired before M-start)
Series B: For the same cohort, count those who STILL have an active subscription at the END of month M (no Subscription canceled or subscription_expired during M)
Series C: Computed: Series B / Series A × 100, unit: %, label: "Monthly Logo Retention Rate"
Series D: Trailing 3-month rolling average of Series C (smoother trend), label: "Logo Retention (3-mo rolling)"
Time granularity: Monthly
Time range: Last 12 months
Breakdown: By Plan (resolved from each user's Subscription started.Plan at the START of month M)
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
- Subscription started marks active subscription start (with Plan, amount, trial_end). Filter for trial_end null to scope to paid (not trial) subscriptions.
- Subscription canceled and subscription_expired mark subscription end. subscription_paused is NOT counted as churn (paused subscriptions can resume).
- "Active at start of month" computed by Lovable: Subscription started exists prior to month-start, with no terminal event before month-start.
