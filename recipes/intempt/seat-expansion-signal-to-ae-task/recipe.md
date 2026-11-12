---
frontmatter_id: seat-expansion-signal-to-ae-task
slash_command: /seat-expansion-signal-to-ae-task
description: Tells the AE when a customer is running out of seats or people from their domain keep signing up, which is the clearest upsell signal there is.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Alerts the account executive when a paying customer nears its seat or usage limit, or when new sign-ups from its
    domain spike, so an expansion task and Slack ping are created.
  parameters:
  - name: seat_warning_threshold
    type: number
    label: Seat capacity warning threshold (fraction of plan limit)
    default: 0.8
    required: false
  - name: usage_cap_threshold
    type: number
    label: Usage cap utilization threshold (fraction)
    default: 0.9
    required: false
  - name: domain_signup_count
    type: number
    label: New domain sign-ups that count as a spike
    default: 3
    required: false
  - name: domain_signup_window
    type: duration
    label: Window for counting new domain sign-ups
    default: 14 d
    required: false
  - name: engagement_lookback
    type: duration
    label: Window to check for recent AE engagement
    default: 30 d
    required: false
  - name: net_growth_window
    type: duration
    label: Window for net seat growth
    default: 30 d
    required: false
  requirements:
  - slot: account_seat_usage
    kind: attribute
    meaning: An account's active seats compared with its plan seat limit, with usage cap utilization
  - slot: paying_account
    kind: segment
    meaning: Accounts that are existing paying customers
  - slot: user_signed_up
    kind: event
    meaning: A new user signed up for the product
    properties:
    - name: email_domain
      type: string
      meaning: Domain of the user's email address
      optional: false
  - slot: ae_engagement
    kind: event
    meaning: An account executive logged an engagement activity on an account
  - slot: ae_owner
    kind: attribute
    meaning: The account executive assigned to an account
    optional: true
  - slot: expansion_candidates
    kind: segment
    meaning: Paying accounts nearing a seat or usage limit or with a domain sign-up spike, excluding accounts in active expansion
      deals
    creatable: true
    definition: paying accounts where seat_capacity_used >= {seat_warning_threshold}, OR at least {domain_signup_count} new
      users from the account's domain signed up in the last {domain_signup_window} and are not provisioned, OR any usage cap
      utilization >= {usage_cap_threshold}; excluding accounts in active expansion deal conversations
  - slot: expansion_task_crm
    kind: integration
    meaning: A connected CRM where expansion tasks can be created for account executives
    channel: salesforce
  - slot: ae_slack
    kind: integration
    meaning: A connected Slack workspace for direct messages to account executives
    channel: slack
  - slot: revops_queue
    kind: destination
    meaning: The RevOps queue that receives expansion signals for accounts without an assigned AE
    optional: true
    channel: email
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_seat_usage
    - seat_warning_threshold
    - usage_cap_threshold
    - domain_signup_count
    - domain_signup_window
    - net_growth_window
    - user_signed_up
    instruction: 'Create an AI-derived account attribute ''seat_capacity_used'' computed as active seats divided by plan seat
      limit, as a fraction. Flag the account when the value is at or above {seat_warning_threshold} (approaching limit) or
      above 1.0 (over limit, billed as overage). Also surface on the account: (a) net seat growth over the last {net_growth_window};
      (b) count of new sign-ups from the account''s domain in the last {domain_signup_window} that are not yet provisioned,
      using {user_signed_up.email_domain}; (c) proximity of any usage cap (API calls, contacts, and similar) to its limit.'
  - id: s2
    builds: segment
    uses:
    - s1
    - paying_account
    - expansion_candidates
    - seat_warning_threshold
    - usage_cap_threshold
    - domain_signup_count
    - domain_signup_window
    - ae_engagement
    instruction: Build the segment 'Seat-expansion candidates' from existing paying accounts where seat_capacity_used is at
      or above {seat_warning_threshold}, OR at least {domain_signup_count} new users from the account's domain signed up in
      the last {domain_signup_window} and are not provisioned, OR any usage cap is at or above {usage_cap_threshold} utilized.
      Exclude accounts already in active expansion deal conversations handled by an account executive. Use the result of "Measure
      how full the plan is".
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - user_signed_up
    - ae_engagement
    - ae_owner
    - expansion_task_crm
    - ae_slack
    - revops_queue
    - seat_warning_threshold
    - domain_signup_count
    - domain_signup_window
    - engagement_lookback
    - usage_cap_threshold
    instruction: 'Create a workflow that fires when seat_capacity_used crosses {seat_warning_threshold}, or when a {user_signed_up}
      event arrives from an existing customer domain. Steps in order: (1) refresh account context; (2) check whether an account
      executive already engaged the account in the last {engagement_lookback} and if so stop, since they are already working
      it; (3) create an expansion task in {expansion_task_crm} including the trigger context (seat-capacity threshold, domain-signup
      spike, or usage cap at {usage_cap_threshold}), current ARR, plan tier, and expected upsell size; (4) send a Slack direct
      message to the owner in {ae_owner} through {ae_slack}. If the account has no assigned AE, route the signal to {revops_queue}.
      Use the results of "Measure how full the plan is" and "Find accounts near a limit".'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - expansion_task_crm
    - ae_engagement
    instruction: 'Compose an expansion pipeline dashboard showing: weekly count of expansion signals by trigger type (seat-cap,
      domain-signup, usage-cap); AE response time; conversion from expansion task to deal created; expansion deal cycle time;
      expansion deal win rate; and ARR uplift from expansion signals year to date versus target. Use the results of "Measure
      how full the plan is", "Find accounts near a limit", and "Raise the expansion task".'
---

# Seat expansion signal to AE

Slash command: /seat-expansion-signal-to-ae-task

## Step 1: Measure how full the plan is

Create an AI-derived attribute 'seat_capacity_used' on the Account object. Compute: (active_seats / plan_seat_limit) as a fraction. Flag when >= 0.8 (approaching limit) or > 1.0 (over limit, billed as overage). Also surface: (a) net seat growth in last 30 days, (b) count of new sign-ups from the account's domain in last 14 days not yet provisioned, (c) any usage cap proximity (API calls, contacts, etc.).

## Step 2: Find accounts near a limit

Build a segment 'Seat-expansion candidates' capturing existing paying accounts where (a) seat_capacity_used >= 0.8, OR (b) 3+ new users from the domain signed up in the last 14 days not yet provisioned, OR (c) any usage cap is >= 0.9 utilized. Excludes accounts already in active expansion deal conversations (handled by AE). Use the result of "Measure how full the plan is".

## Step 3: Raise the expansion task

Create a workflow firing when seat_capacity_used crosses 0.8, or when a new user_signed_up event comes from an existing customer domain. Step sequence: (1) refresh account context; (2) check whether AE already engaged this account in last 30 days (if so, skip: they're on it); (3) create an AE expansion task with the trigger context (seat-capacity threshold vs. domain-signup spike vs. usage-cap), current ARR, plan tier, expected upsell size; (4) post Slack DM to the AE owner. If the account has no assigned AE, route to RevOps queue. Use the result of "Measure how full the plan is", "Find accounts near a limit".

## Step 4: Track the expansion pipeline

Compose an expansion pipeline dashboard: count of expansion signals per week (by trigger type: seat-cap / domain-signup / usage-cap), AE response time, expansion-task-to-deal-created conversion, expansion deal cycle time (typically 2-3x faster than new-logo deals), and expansion-deal win rate. ARR uplift from expansion signals YTD vs. target. Use the result of "Measure how full the plan is", "Find accounts near a limit", "Raise the expansion task".
