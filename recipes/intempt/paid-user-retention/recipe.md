---
frontmatter_id: paid-user-retention
slash_command: /paid-user-retention
description: Builds a segment of paying users who stopped logging in, and emails a monthly digest of whether paying customers
  keep logging in and keep paying month by month, by plan.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds the paying users gone quiet segment and emails a monthly digest of logo and revenue retention for paid cohorts
    by plan, with benchmark flags.
  parameters:
  - name: quiet_window
    type: duration
    label: Days without a session that count as gone quiet
    default: 30 d
    required: false
  - name: time_range
    type: duration
    label: Paid signup cohorts covered
    default: 6 mo
    required: false
  - name: compare_window
    type: duration
    label: Earlier cohorts they are compared with
    default: 6 mo
    required: false
  - name: logo_benchmark_good
    type: number
    label: Good month-1 logo retention (%)
    default: 95
    required: false
  - name: logo_benchmark_below_par
    type: number
    label: Below-par month-1 logo retention (%)
    default: 85
    required: false
  - name: m3_logo_flag_threshold
    type: number
    label: Month-3 logo retention below which a cohort is flagged (%)
    default: 80
    required: false
  - name: expansion_gap_threshold
    type: number
    label: Revenue retention above logo retention that marks expansion (points)
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: paid_subscription_started
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: trial_end
      type: text
      meaning: Trial end date; empty means the start was a paid signup, not a trial
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
  steps:
  - id: s1
    builds: segment
    uses:
    - paid_subscription_started
    - session_start
    - revenue_completed
    - quiet_window
    instruction: 'Build a new segment of users named "Paying Users Gone Quiet": users who did {paid_subscription_started}
      with {paid_subscription_started.trial_end} empty, did {revenue_completed} in the last 45 days, and did not do {session_start}
      in the last {quiet_window}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - paid_subscription_started
    - session_start
    - revenue_completed
    - time_range
    - compare_window
    - logo_benchmark_good
    - logo_benchmark_below_par
    - m3_logo_flag_threshold
    - expansion_gap_threshold
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes monthly
      cohorts of users whose {paid_subscription_started} with {paid_subscription_started.trial_end} empty happened in the
      last {time_range}, and writes for each cohort and each {paid_subscription_started.plan}: logo retention at months 1
      to 6, the share who did {session_start} in that month; revenue retention at months 1 to 6, that month''s sum of {revenue_completed.amount}
      against month 0; the same averages for cohorts in the {compare_window} before; where month-1 logo retention sits against
      {logo_benchmark_below_par}% and {logo_benchmark_good}%; the number of users in the segment from "Find paying users gone
      quiet". When a cohort''s month-3 logo retention is below {m3_logo_flag_threshold}%, or revenue retention is more than
      {expansion_gap_threshold} points above logo retention, the email''s first line says so. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Paid user retention

Slash command: /paid-user-retention

## Step 1: Find paying users gone quiet

Build a new segment of users named "Paying Users Gone Quiet": users who did paid subscription started with trial end empty, did revenue completed in the last 45 days, and did not do session start in the last 30 d.

## Step 2: Email the monthly paid retention digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes monthly cohorts of users whose paid subscription started with trial end empty happened in the last 6 mo, and writes for each cohort and each plan: logo retention at months 1 to 6, the share who did session start in that month; revenue retention at months 1 to 6, that month's sum of amount against month 0; the same averages for cohorts in the 6 mo before; where month-1 logo retention sits against 85% and 95%; the number of users in the segment from "Find paying users gone quiet". When a cohort's month-3 logo retention is below 80%, or revenue retention is more than 10 points above logo retention, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
