---
frontmatter_id: free-to-paid-csm-kickoff
slash_command: /free-to-paid-csm-kickoff
description: Every upgrade from free to paid creates a CSM kickoff task carrying the customer's whole free period history, due inside five working days.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Each free-to-paid upgrade creates a CSM kickoff task with the customer's free-period history attached, due within
    five business days, plus a Slack hand-off and a dashboard tracking results.
  parameters:
  - name: conversion_window
    type: duration
    label: Window for recent upgrades
    default: 7 d
    required: false
  - name: min_mrr
    type: number
    label: Minimum MRR for CSM motion (USD)
    default: 50
    required: false
  - name: kickoff_due_days
    type: number
    label: Business days to complete kickoff task
    default: 5
    required: false
  - name: completion_target
    type: number
    label: Target kickoff completion rate (%)
    default: 95
    required: false
  - name: retention_window
    type: duration
    label: Retention measurement window
    default: 90 d
    required: false
  - name: celebration_channel
    type: string
    label: Slack channel for celebration message
    default: '#wins'
    required: false
  requirements:
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: mrr
      type: number
      meaning: Monthly recurring revenue of the subscription
      optional: false
    - name: plan_tier
      type: string
      meaning: Plan tier of the subscription (enterprise, SMB, etc.)
      optional: false
  - slot: subscription_status_attribute
    kind: attribute
    meaning: The user's subscription status (free, trialing, paid)
  - slot: account_lifecycle_attribute
    kind: attribute
    meaning: The account lifecycle stage of the customer account
  - slot: preconversion_history_attribute
    kind: attribute
    meaning: A user attribute holding the pre-conversion history brief for the CSM
    optional: true
  - slot: free_converters_segment
    kind: segment
    meaning: Users who recently converted from free or trial to paid
    creatable: true
    definition: users who did {subscription_started_event} in the last {conversion_window} AND whose previous subscription_status
      was free or trialing AND whose subscription MRR is at least {min_mrr}
  - slot: csm_territory_rules
    kind: knowledge
    meaning: Territory and plan-tier rules that map accounts to named or pooled CSMs
  - slot: csm_kickoff_task_destination
    kind: integration
    meaning: A task system where CSM kickoff tasks can be created
    channel: hubspot
  - slot: csm_slack_channel
    kind: destination
    meaning: A Slack destination for notifying assigned CSMs and posting wins
    channel: slack
  - slot: plg_handoff_dashboard_data
    kind: event
    meaning: Event data for free-to-paid conversions and CSM task completions
    properties:
    - name: kickoff_completed_at
      type: date
      meaning: When the CSM kickoff task was completed
      optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - subscription_started_event
    - subscription_status_attribute
    - free_converters_segment
    - conversion_window
    - min_mrr
    instruction: Build the segment '{free_converters_segment}' of users who did {subscription_started_event} in the last {conversion_window}
      and whose prior {subscription_status_attribute} was free or trialing (genuine upgrades, excluding direct paid signups).
      Exclude users whose subscription MRR is below {min_mrr}.
  - id: s2
    builds: attribute
    uses:
    - subscription_started_event
    - preconversion_history_attribute
    instruction: 'Create an AI-derived user attribute ''{preconversion_history_attribute}'' computed at the time of {subscription_started_event}.
      It captures: (a) days from signup to paid conversion; (b) features most used during the free period; (c) features never
      used, as later expansion drivers; (d) team signal: how many users from the same account are on free and on paid; (e)
      acquisition source (organic, paid, referral, or outbound). This is the CSM''s pre-call brief.'
  - id: s3
    builds: automation
    uses:
    - subscription_started_event
    - free_converters_segment
    - preconversion_history_attribute
    - csm_territory_rules
    - csm_kickoff_task_destination
    - kickoff_due_days
    - account_lifecycle_attribute
    - csm_slack_channel
    - celebration_channel
    - s1
    - s2
    instruction: 'Create a workflow that fires on {subscription_started_event} for users in ''{free_converters_segment}''.
      Steps in order: (1) compute {preconversion_history_attribute}; (2) assign a CSM using {csm_territory_rules}: enterprise
      plan tier gets a named CSM, SMB plan tier gets a pooled CSM; (3) create a CSM kickoff task in {csm_kickoff_task_destination}
      with the pre-call brief attached, due within {kickoff_due_days} business days; (4) trigger structured onboarding journey
      for the user; (5) set {account_lifecycle_attribute} to new-customer; (6) post a Slack notification to the assigned CSM
      in {csm_slack_channel} and a celebration message to {celebration_channel}.'
  - id: s4
    builds: dashboard
    uses:
    - plg_handoff_dashboard_data
    - free_converters_segment
    - kickoff_due_days
    - completion_target
    - retention_window
    - s1
    - s2
    - s3
    instruction: 'Build a PLG-to-CS handoff quality dashboard showing: free-to-paid conversion volume per week from ''{free_converters_segment}'';
      the share of CSM kickoff tasks completed within {kickoff_due_days} business days against the {completion_target}% target;
      median days from signup to conversion; and {retention_window} retention of free-to-paid converters split into ''CSM
      kickoff completed within {kickoff_due_days} days'' and ''CSM kickoff missed''. Typical gap between these groups is 15
      to 25 percentage points.'
---

# Free to paid CSM kickoff

Slash command: /free-to-paid-csm-kickoff

## Step 1: Find genuine upgrades

Build a segment 'Free-to-paid converters - last 7 days' capturing users where Subscription started fired in the last 7 days AND the user previously had subscription_status = free OR trialing (true conversion, not net-new direct-paid signup, those go through a different flow). Excludes users where the subscription is < $50 MRR (consumer-tier; doesn't get CSM motion).

## Step 2: Write the pre call brief

Create an AI-derived attribute 'preconversion_history' on the User object, computed at Subscription started time. Capture: (a) days from signup to paid conversion; (b) features most-used in free period; (c) features NEVER touched (potential expansion drivers later); (d) team-member signal: how many users from the same account are also on free / paid; (e) source: how they got to signup (organic / paid / referral / outbound). This becomes the CSM's pre-call brief.

## Step 3: Assign a CSM and kick off

Create a workflow firing on Subscription started for free-to-paid converters. Step sequence: (1) compute preconversion_history attribute; (2) assign CSM via territory + plan-tier rules (enterprise tier gets named CSM, SMB tier gets pooled CSM); (3) create CSM kickoff task with the preconversion history pre-attached, due within 5 business days; (4) trigger the structured onboarding journey (separate recipe) for the user; (5) update account lifecycle to 'new-customer'; (6) post Slack notification to the assigned CSM and a celebration message to #wins. Use the result of "Find genuine upgrades", "Write the pre call brief".

## Step 4: Prove the handoff matters

Compose a PLG-to-CS handoff quality dashboard: free-to-paid conversion volume per week, CSM-task completion rate within 5 business days (target: 95%+), median days from signup-to-conversion (PLG funnel speed), and 90-day retention of free-to-paid converters split by 'CSM kickoff completed within 5 days' vs. 'CSM kickoff missed': typically the gap is 15-25 percentage points (the proof-of-value for human CSM motion). Use the result of "Find genuine upgrades", "Write the pre call brief", "Assign a CSM and kick off".
