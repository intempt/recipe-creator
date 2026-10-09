---
description: 'Shows a single trailing logo-retention rate: the share of customers still subscribed at the end of the current period. Uses subscription status data for the current period.'
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
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
