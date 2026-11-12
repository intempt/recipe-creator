---
frontmatter_id: usage-based-upgrade-trigger
slash_command: /usage-based-upgrade-trigger
description: Catches an account nearing its plan limits, shows the decision maker an upgrade inside the app, and calls an AE in on the bigger ones.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Alerts paying accounts nearing plan limits with an in-app upgrade prompt, calls in an AE on high-value accounts,
    and tracks which upgrade motion converts better.
  parameters:
  - name: approaching_threshold
    type: number
    label: Approaching threshold (share of plan limit used)
    default: 0.8
    required: false
  - name: near_limit_threshold
    type: number
    label: Near-limit threshold (share of plan limit used)
    default: 0.95
    required: false
  - name: lookback_window
    type: duration
    label: Window to exclude accounts with a recent upgrade conversation
    default: 30 d
    required: false
  - name: throttle_window
    type: duration
    label: Minimum gap before re-firing for the same account
    default: 14 d
    required: false
  - name: high_value_mrr
    type: number
    label: MRR above which an AE expansion task is created (USD per month)
    default: 500
    required: false
  requirements:
  - slot: paying_account
    kind: segment
    meaning: Paying accounts that are not on the highest plan, with usage tracking enabled
  - slot: plan_decision_maker
    kind: segment
    meaning: Users whose role lets them approve plan upgrades
  - slot: upgrade_conversation
    kind: event
    meaning: A customer had an upgrade conversation with sales or success
  - slot: account_mrr
    kind: attribute
    meaning: Monthly recurring revenue of the account in USD
  - slot: billing_contact
    kind: attribute
    meaning: Email address of the account's billing contact
  - slot: in_app_channel
    kind: destination
    meaning: In-app messaging surface where upgrade prompts can be shown to users
    channel: push
  - slot: ae_task_destination
    kind: integration
    meaning: CRM where expansion tasks for account executives are created
    channel: hubspot
  - slot: billing_email
    kind: destination
    meaning: Email channel used to notify billing contacts about overage
    channel: email
  - slot: upgrade_signal
    kind: event
    meaning: An analytics event recording an upgrade-related signal for an account
    optional: true
  - slot: upgrade_completed
    kind: event
    meaning: A customer completed a plan upgrade
  steps:
  - id: s1
    builds: attribute
    uses:
    - paying_account
    - approaching_threshold
    - near_limit_threshold
    instruction: Create an AI-derived account attribute named usage_capacity_used. For each metered usage dimension on the
      account's current plan (API calls, contacts, events, seats, storage, sends), compute current usage divided by plan limit
      as a fraction. Output the maximum across all dimensions as the bottleneck value, along with the name of the dimension
      at threshold. Flag values at {approaching_threshold} as approaching, {near_limit_threshold} as near-limit, and 1.0 or
      above as over-limit (overage charges or service throttling).
  - id: s2
    builds: segment
    uses:
    - s1
    - paying_account
    - upgrade_conversation
    - lookback_window
    - approaching_threshold
    instruction: 'Build a segment named Upgrade-ready accounts containing paying accounts where usage_capacity_used is at
      least {approaching_threshold}, the account is not on the highest plan, and no {upgrade_conversation} occurred in the
      last {lookback_window}. Split the segment into three tiers: approaching (from {approaching_threshold} up to {near_limit_threshold})
      for the in-app prompt, near-limit (from {near_limit_threshold} up to 1.0) for the in-app prompt plus an AE task, and
      over-limit (1.0 or above) for an urgent AE task plus a customer notification.'
  - id: s3
    builds: page
    uses:
    - s2
    - plan_decision_maker
    - in_app_channel
    instruction: 'Write in-app upgrade prompt content for the Upgrade-ready accounts segment, personalized to the dimension
      at threshold. Example copy: ''You''ve used 84% of your monthly events on the Starter plan. Upgrade to Pro for 10x capacity
      plus advanced reporting.'' Include the current usage stat, a plan comparison, and a one-click upgrade call to action.
      Use a helpful tone that says we noticed your usage, not a pushy one. Suppress display for users who are not in {plan_decision_maker},
      so end users who cannot approve upgrades are not prompted.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - account_mrr
    - high_value_mrr
    - billing_contact
    - billing_email
    - ae_task_destination
    - in_app_channel
    - upgrade_signal
    - throttle_window
    - approaching_threshold
    instruction: 'Create a workflow that fires when usage_capacity_used crosses {approaching_threshold} and again on each
      later threshold crossing. Steps in order: (1) show the ''Write in-app upgrade prompt'' page through {in_app_channel}
      to users in {plan_decision_maker} on the account; (2) if {account_mrr} is greater than {high_value_mrr} per month, create
      an AE expansion task in {ae_task_destination} immediately, without waiting for the prompt to be clicked; (3) for over-limit
      accounts only, send an overage notification email through {billing_email} to {billing_contact}; (4) record an upgrade_signal
      event in {upgrade_signal}. Do not re-fire for the same account within {throttle_window}, even while it stays over a
      threshold.'
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - upgrade_completed
    - account_mrr
    - high_value_mrr
    instruction: 'Build an upgrade conversion dashboard showing: weekly volume of accounts crossing the {approaching_threshold}
      threshold; in-app prompt to upgrade conversion rate; AE task to upgrade conversion rate for accounts with MRR above
      {high_value_mrr}; ARR uplift from usage-based expansion this quarter; and median time from threshold crossing to {upgrade_completed}.
      Add a comparison of upgrades attributed to the in-app prompt versus upgrades attributed to AE outreach as a signal of
      which motion is more effective.'
---

# Upgrade prompt when limits approach

Slash command: /usage-based-upgrade-trigger

## Step 1: Find the bottleneck limit

Create an AI-derived attribute 'usage_capacity_used' on the Account object. For each metered usage dimension on the account's current plan (API calls / contacts / events / seats / storage / sends), compute current_usage / plan_limit as a fraction. Output: the maximum across all dimensions (the bottleneck), with which dimension is at threshold. Flag thresholds: 0.8 = approaching, 0.95 = near-limit, 1.0+ = over-limit (overage charges or service throttling).

## Step 2: Find accounts near a limit

Build a segment 'Upgrade-ready accounts' capturing paying accounts where usage_capacity_used >= 0.8 AND the account isn't already on the highest plan AND no upgrade conversation occurred in last 30 days. Splits implicitly: (a) approaching (0.8-0.94) to in-app prompt, (b) near-limit (0.95-1.0) to in-app prompt + AE task, (c) over-limit to urgent AE task + customer notification. Use the result of "Find the bottleneck limit".

## Step 3: Write the in app prompt

This step builds a page.
Generate in-app upgrade prompt content. Personalized to which dimension is approaching limit: 'You've used 84% of your monthly events on the Starter plan. Upgrade to Pro for 10x capacity + advanced reporting.' Include current usage stat, plan comparison, and a one-click upgrade CTA. Tone: helpful (we noticed) not pushy (we're charging you). Suppress display for users not in plan-decision-maker role (avoid spamming end users about upgrades they can't approve). Use the result of "Find accounts near a limit".

## Step 4: Prompt, then call in an AE

Create a workflow firing when usage_capacity_used crosses 0.8 (and on each subsequent threshold). Step sequence: (1) trigger in-app upgrade prompt for plan-decision-makers on the account; (2) for accounts with MRR > $500/month, create AE expansion task immediately (don't wait for prompt-clickthrough: these are high-value, deserve human outreach); (3) for over-limit cases, additionally send an email notification to billing-contact about overage; (4) emit upgrade_signal event for analytics tracking. Throttle: don't re-fire for the same account within 14 days even if it's still over threshold (avoid prompt fatigue). Use the result of "Find the bottleneck limit", "Find accounts near a limit", "Write the in app prompt".

## Step 5: Compare prompt against AE

Compose an upgrade conversion dashboard: usage-trigger volume per week (accounts crossing 0.8 threshold), in-app-prompt-to-upgrade conversion rate, AE-task-to-upgrade conversion rate (for high-MRR cohort), ARR uplift from usage-based expansion this quarter, and median time from threshold-cross to upgrade-completed. Compare upgrade-via-prompt vs. upgrade-via-AE-outreach as motion-effectiveness signal. Use the result of "Find the bottleneck limit", "Find accounts near a limit", "Write the in app prompt", "Prompt, then call in an AE".
