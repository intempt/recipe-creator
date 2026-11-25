---
frontmatter_id: net-revenue-retention-by-cohort
slash_command: /net-revenue-retention-by-cohort
description: Emails a monthly digest of net revenue retention for each monthly cohort of new paying customers, by starting
  plan, with benchmarks and an early erosion flag.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a monthly digest of net revenue retention per monthly customer cohort and starting plan, with a headline
    12-month NRR and erosion flags.
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
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
  steps:
  - id: s1
    builds: automation
    uses:
    - subscription_started_event
    - subscription_updated_event
    - subscription_canceled_event
    - subscription_resumed_event
    - time_range_cohort_months
    - max_months_after_cohort
    - early_warning_month
    - erosion_nrr_threshold
    - benchmark_low
    - benchmark_mid
    - benchmark_high
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it groups paying
      customers by the month of their first {subscription_started_event} with {subscription_started_event.trial_end} empty,
      for cohorts in the last {time_range_cohort_months}, split by that event''s {subscription_started_event.plan}. For each
      cohort and each month since it started, up to {max_months_after_cohort}, it writes NRR %: (starting {subscription_started_event.amount}
      + positive changes in {subscription_updated_event.amount} per {subscription_updated_event.subscription_id} + {subscription_resumed_event.amount}
      - negative changes - {subscription_canceled_event.amount}) / starting amount x 100. It also writes the blended NRR over
      the last 12 months, the cohort with the highest NRR at month {max_months_after_cohort}, and whether NRR is rising across
      newer cohorts. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. The email
      compares NRR with {benchmark_low}%, {benchmark_mid}% and {benchmark_high}%, and flags cohorts under {erosion_nrr_threshold}%
      at month {early_warning_month}. Nothing else is sent.'
---

# Net revenue retention by cohort

Slash command: /net-revenue-retention-by-cohort

## Step 1: Email the monthly cohort NRR digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it groups paying customers by the month of their first subscription started event with trial end empty, for cohorts in the last 12 mo, split by that event's plan. For each cohort and each month since it started, up to 12, it writes NRR %: (starting amount + positive changes in amount per subscription id + amount - negative changes - amount) / starting amount x 100. It also writes the blended NRR over the last 12 months, the cohort with the highest NRR at month 12, and whether NRR is rising across newer cohorts. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email compares NRR with 100%, 110% and 120%, and flags cohorts under 90% at month 6. Nothing else is sent.
