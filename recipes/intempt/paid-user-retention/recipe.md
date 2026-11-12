---
frontmatter_id: paid-user-retention
slash_command: /paid-user-retention
description: See whether paying customers continue logging in, tracked month by month and compared by plan.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows whether paying customers keep logging in and keep paying month by month, broken down by plan, with flags
    for weak retention and benchmark comparisons.
  parameters:
  - name: report_name
    type: string
    label: Report name
    default: Paid User Monthly Retention
    required: false
  - name: cohort_granularity
    type: enum
    label: Cohort granularity
    default: monthly
    required: false
    options:
    - daily
    - weekly
    - monthly
  - name: time_range
    type: duration
    label: Time range
    default: 6 mo
    required: false
  - name: compare_window
    type: duration
    label: Comparison period
    default: 6 mo
    required: false
  - name: logo_benchmark_good
    type: number
    label: Good monthly logo retention benchmark (%)
    default: 95
    required: false
  - name: logo_benchmark_below_par
    type: number
    label: Below-par monthly logo retention benchmark (%)
    default: 85
    required: false
  - name: m3_logo_flag_threshold
    type: number
    label: Flag plan tiers whose M3 logo retention is below (%)
    default: 80
    required: false
  - name: expansion_gap_threshold
    type: number
    label: Flag cohorts where revenue retention exceeds logo retention by (points)
    default: 10
    required: false
  requirements:
  - slot: paid_subscription_started
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: trial_end
      type: text
      meaning: Trial end date; null means the start was a paid signup, not a trial
      optional: true
    - name: plan
      type: text
      meaning: Plan tier the customer subscribed to
      optional: false
  - slot: session_start
    kind: event
    meaning: A customer started a logged-in session
  - slot: revenue_completed
    kind: event
    meaning: A customer completed a recurring revenue payment
    properties:
    - name: amount
      type: number
      meaning: Payment amount
      optional: false
    - name: customer_id
      type: text
      meaning: Customer identifier
      optional: false
    - name: type
      type: text
      meaning: Revenue type marker identifying recurring revenue
      optional: false
  steps:
  - id: s1
    builds: report
    uses:
    - paid_subscription_started
    - session_start
    - revenue_completed
    - report_name
    - cohort_granularity
    - time_range
    - compare_window
    instruction: 'Create a retention report named "{report_name}". Anchor event: {paid_subscription_started} where trial_end
      is null (paid signup, not trial). Return events: {session_start} for logo retention and {revenue_completed} for revenue
      retention, shown as two views. Cohort granularity: {cohort_granularity}. Time range: {time_range}. Breakdown: by plan
      from {paid_subscription_started.plan}. Compare against the previous period of {compare_window} (prior cohorts). Chart
      type: retention curve plus cohort table with M1 through M6 columns.'
---

# Paid user retention

Slash command: /paid-user-retention

## Step 1: Split logo and revenue retention

Create a Retention report called "Paid User Monthly Retention".
Anchor event: Subscription started where trial_end is null (paid signup, not trial)
Return event: Session start (logo retention) AND Revenue completed (revenue retention): render as two views
Cohort granularity: Monthly
Time range: Last 6 months
Breakdown: By Plan (from Subscription started.Plan)
Compare: Previous period (prior 6 months of cohorts)
Chart type: Retention curve plus cohort table with M1 through M6 columns
Logo Retention view:
- Cell value = % of cohort users who emitted at least one Session start in month N
Revenue Retention view:
- Cell value = Sum of Revenue completed.amount in month N from cohort users / Sum of Revenue completed.amount in month 0 from cohort users × 100, unit: %
- This separates "do users stay?" from "do they pay the same or more?"
Annotations:
- Add benchmarks: 95% monthly logo retention is industry-good for self-serve SaaS; 85% is below par.
- Flag any plan tier where M3 logo retention is below 80%.
- Flag any cohort where revenue retention exceeded logo retention by 10+ percentage points (expansion offsetting churn: good).
- Highlight the highest-retaining plan tier.
Surface whether enterprise tiers retain materially better than starter tiers.
Taxonomy notes:
- Subscription started with trial_end=null marks paid (non-trial) starts.
- Revenue completed has amount, customer_id, type: the canonical recurring revenue marker.
- "any_active_event" as a return signal can be substituted with Session start (most reliable active marker).
