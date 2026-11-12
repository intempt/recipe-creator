---
frontmatter_id: net-revenue-retention-by-cohort
slash_command: /net-revenue-retention-by-cohort
description: Tracks monthly cohort retention rates over time to measure ongoing customer and user engagement.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows monthly cohort net revenue retention, broken down by starting plan, with benchmarks, a headline trailing
    12-month NRR, and a cohort-quality trend check.
  parameters:
  - name: time_range_cohort_months
    type: duration
    label: Cohort lookback window
    default: 12 mo
    required: false
  - name: max_months_after_cohort
    type: number
    label: Maximum months after cohort start
    default: 12
    required: false
  - name: early_warning_month
    type: number
    label: Month used for early erosion flag
    default: 6
    required: false
  - name: erosion_nrr_threshold
    type: number
    label: NRR threshold for erosion flag (%)
    default: 90
    required: false
  - name: benchmark_low
    type: number
    label: Benchmark NRR (%) - growing revenue
    default: 100
    required: false
  - name: benchmark_mid
    type: number
    label: Benchmark NRR (%) - top quartile
    default: 110
    required: false
  - name: benchmark_high
    type: number
    label: Benchmark NRR (%) - best in class
    default: 120
    required: false
  requirements:
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: plan
      type: string
      meaning: Plan on the subscription when it started
      optional: false
    - name: trial_end
      type: date
      meaning: When the trial ends, empty if no trial
      optional: true
    - name: amount
      type: number
      meaning: Recurring amount of the subscription
      optional: false
  - slot: subscription_updated_event
    kind: event
    meaning: A customer's subscription was updated, including amount changes
    properties:
    - name: subscription_id
      type: string
      meaning: Identifier of the subscription
      optional: false
    - name: amount
      type: number
      meaning: Post-update recurring amount
      optional: false
    - name: changed_fields
      type: text
      meaning: Fields changed in the update
      optional: true
    - name: plan_items
      type: text
      meaning: Plan line items after the update
      optional: true
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: subscription_id
      type: string
      meaning: Identifier of the subscription
      optional: false
    - name: amount
      type: number
      meaning: Prior recurring amount of the canceled subscription
      optional: false
  - slot: subscription_resumed_event
    kind: event
    meaning: A customer resumed a previously canceled or paused subscription
    properties:
    - name: amount
      type: number
      meaning: Recurring amount on resume
      optional: false
  - slot: revenue_completed_event
    kind: event
    meaning: A customer completed a payment
    properties:
    - name: amount
      type: number
      meaning: Payment amount
      optional: false
    - name: revenue_type
      type: string
      meaning: Whether the payment is recurring or one-time
      optional: false
  steps:
  - id: s1
    builds: report
    uses:
    - subscription_started_event
    - subscription_updated_event
    - subscription_canceled_event
    - subscription_resumed_event
    - revenue_completed_event
    - time_range_cohort_months
    - max_months_after_cohort
    - early_warning_month
    - erosion_nrr_threshold
    - benchmark_low
    - benchmark_mid
    - benchmark_high
    instruction: 'Create a Retention report named "Net Revenue Retention by Cohort". Define each cohort by the calendar month
      of the user''s first paid subscription start, where a subscription started event counts as paid when its trial_end is
      empty or it is a follow-on subscription started after a trial. Cover the last {time_range_cohort_months} of cohorts.
      For each cohort month M and each month N from M to M+{max_months_after_cohort}, compute for cohort users: Starting MRR
      as the sum of revenue_completed amount where revenue_type is recurring in month N-1; Expansion MRR as the sum of positive
      changes in amount between consecutive subscription_updated amounts on the same subscription_id in month N; Reactivation
      MRR as the sum of subscription_resumed amount in month N for users who previously had a subscription_canceled; Contraction
      MRR as the sum of negative amount changes from subscription_updated in month N, subtracted; Churned MRR as the sum of
      the prior amount of each subscription_canceled in month N, subtracted. Ending MRR equals Starting plus Expansion plus
      Reactivation minus Contraction minus Churned. NRR at month N equals Ending MRR divided by the cohort''s original revenue
      at month M, multiplied by 100, shown in percent. Break down cohorts by the plan on the cohort-defining subscription
      started event. Chart as a multi-line chart with months since cohort on the X axis and NRR percent on the Y axis, one
      line per cohort, plus a stacked bar showing the component breakdown for the most recent cohort. Add reference lines
      at {benchmark_low}%, {benchmark_mid}% and {benchmark_high}%. Flag any cohort whose NRR at month {early_warning_month}
      is below {erosion_nrr_threshold}%. Highlight the cohort with the highest NRR at month {max_months_after_cohort}. Indicate
      whether NRR is improving across successive cohorts. Show a headline trailing 12-month blended NRR number and state whether
      the cohort trend is improving. If subscription_updated events lack changed_fields or plan_items detail, note that the
      report reflects logo retention only.'
---

# Net revenue retention by cohort

Slash command: /net-revenue-retention-by-cohort

## Step 1: Track cohort revenue month by month

Create a Retention report called "Net Revenue Retention by Cohort".
Cohort: Monthly cohort defined by month of first paid Subscription started (trial_end is null OR a follow-on after-trial Subscription started) per user.
For each cohort and each month-after-cohort N (M, M+1, M+2, ... M+12), compute the dollar values for users in the cohort:
- Starting MRR (cohort's recurring revenue in month N-1) = Sum of Revenue completed.amount filtered to recurring type, for cohort users
- Expansion MRR = Sum of positive amount-deltas from Subscription updated events in month N for cohort users (where the post-event amount exceeds the prior amount on the same subscription_id)
- Reactivation MRR = Sum of subscription_resumed.amount in month N for cohort users who had a prior Subscription canceled
- Contraction MRR = Sum of negative amount-deltas from Subscription updated events (subtracted)
- Churned MRR = Sum of the prior subscription amount for each Subscription canceled in month N (subtracted)
- Ending MRR = Starting + Expansion + Reactivation − Contraction − Churn
- NRR for cohort at month N = Ending MRR / Original cohort revenue at month M × 100, unit: %
Time range: Last 12 cohort-months
Breakdown: By initial Plan (the Plan on the cohort-defining Subscription started)
Chart type: Multi-line chart: X axis is months-since-cohort, Y axis is NRR %; each cohort is a line. Plus a stacked bar showing the per-component decomposition for the most recent cohort.
Annotations:
- Add benchmarks: NRR ≥ 100% (cohort growing in revenue despite churn); ≥ 110% (top-quartile); ≥ 120% (best-in-class).
- Flag any cohort whose NRR at M+6 is below 90% (revenue erosion).
- Highlight the cohort with the highest M+12 NRR.
- Flag whether NRR is improving across cohorts over time (cohort-quality trend).
Surface the trailing 12-month blended NRR (a single headline number) and whether the cohort-level trend is improving.
Taxonomy notes:
- The canonical taxonomy does not have separate subscription_upgraded/_downgraded/_reactivated events. Expansion and Contraction are computed by Lovable from Subscription updated by comparing pre/post amount on the same subscription_id. Reactivation is computed as subscription_resumed (or subscription_activated) where the same customer_id had a recent Subscription canceled.
- This recipe depends on Subscription updated firing reliably with sufficient detail (changed_fields, plan_items) for the delta computation. If the integration emits sparse Subscription updated, the report degrades to logo-retention only.
