---
frontmatter_id: monthly-logo-retention-trend
slash_command: /monthly-logo-retention-trend
description: Emails a monthly digest of the share of paying customers kept each month, its 3-month rolling trend by plan,
  benchmarks, churn-spike flags and an annualized retention figure.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a monthly digest of logo retention for paying customers, its rolling trend by plan, the annualized rate,
    and flags for churn spikes and steady declines.
  parameters:
  - name: trend_window_months
    type: number
    label: Months of history in the digest
    default: 12
    required: false
  - name: rolling_window_months
    type: number
    label: Months in the rolling average
    default: 3
    required: false
  - name: spike_threshold_points
    type: number
    label: Drop below the rolling average that counts as a churn spike (points)
    default: 2
    required: false
  - name: decline_months
    type: number
    label: Months of decline in a row that get flagged
    default: 3
    required: false
  - name: benchmark_good_pct
    type: number
    label: Good monthly retention benchmark (%)
    default: 95
    required: false
  - name: benchmark_best_pct
    type: number
    label: Best-in-class monthly retention benchmark (%)
    default: 97
    required: false
  - name: benchmark_risk_pct
    type: number
    label: At-risk monthly retention benchmark (%)
    default: 90
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
  steps:
  - id: s1
    builds: automation
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
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes paying
      customers, those whose {subscription_started} has {subscription_started.trial_end} empty, and for each of the last {trend_window_months}
      months writes: customers active at the month''s start (no {subscription_canceled} or {subscription_expired} before it)
      and the share of them with neither event during the month, the monthly logo retention rate; the {rolling_window_months}-month
      rolling average; the last month''s rate by {subscription_started.Plan} and for the same month a year ago; the annualized
      rate, last month''s rate to the power of 12; where last month sits against {benchmark_risk_pct}%, {benchmark_good_pct}%
      and {benchmark_best_pct}%. When last month is more than {spike_threshold_points} points below the rolling average, or
      the rate fell {decline_months} months in a row, the email''s first line says so. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Monthly logo retention

Slash command: /monthly-logo-retention-trend

## Step 1: Email the monthly logo retention digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes paying customers, those whose subscription started has trial end empty, and for each of the last 12 months writes: customers active at the month's start (no subscription canceled or subscription expired before it) and the share of them with neither event during the month, the monthly logo retention rate; the 3-month rolling average; the last month's rate by Plan and for the same month a year ago; the annualized rate, last month's rate to the power of 12; where last month sits against 90%, 95% and 97%. When last month is more than 2 points below the rolling average, or the rate fell 3 months in a row, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
