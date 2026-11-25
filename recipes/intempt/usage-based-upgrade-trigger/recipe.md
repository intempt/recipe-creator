---
frontmatter_id: usage-based-upgrade-trigger
slash_command: /usage-based-upgrade-trigger
description: Catches an account nearing its plan limit, shows the decision maker an upgrade inside the app, emails the billing
  contact when it goes over, and alerts an AE about the bigger accounts.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Flags accounts near their plan limit, prompts decision makers to upgrade in the app, emails over-limit accounts
    and alerts AEs about high-value ones.
  parameters:
  - name: approaching_threshold
    type: number
    label: Share of the plan limit used that counts as approaching (0 to 1)
    default: 0.8
    required: false
  - name: lookback_window
    type: duration
    label: Skip accounts with an upgrade conversation in this window
    default: 30 d
    required: false
  - name: high_value_mrr
    type: number
    label: Monthly revenue above which an AE is alerted
    default: 500
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the AE team alerted about high-value accounts
    required: true
  requirements:
  - slot: plan_usage
    kind: attribute
    meaning: Account attribute with this period's usage of the main metered plan dimension (events, contacts, seats or sends)
  - slot: plan_limit
    kind: attribute
    meaning: Account attribute with the plan limit for that same dimension
  - slot: plan
    kind: attribute
    meaning: Account attribute with the current plan name
  - slot: plan_role
    kind: attribute
    meaning: User attribute that is admin or owner for people who can approve a plan upgrade
  - slot: upgrade_conversation
    kind: event
    meaning: A customer had an upgrade conversation with sales or success
  - slot: account_mrr
    kind: attribute
    meaning: Account attribute with monthly recurring revenue in USD
  steps:
  - id: s1
    builds: attribute
    uses:
    - plan_usage
    - plan_limit
    instruction: 'Build a computed attribute on accounts named "usage_capacity_used": the account''s {plan_usage} attribute
      divided by its {plan_limit} attribute, as a number rounded to two decimals. Accounts with no {plan_limit} value have
      no value.'
  - id: s2
    builds: segment
    uses:
    - s1
    - plan
    - upgrade_conversation
    - approaching_threshold
    - lookback_window
    dependsOn:
    - s1
    instruction: Build a new segment of accounts named "Upgrade-ready accounts". An account is in it when its usage_capacity_used
      attribute from "Find the bottleneck limit" is {approaching_threshold} or more, its {plan} attribute is not enterprise,
      and none of its users did {upgrade_conversation} in the last {lookback_window}.
  - id: s3
    builds: page
    uses:
    - s1
    - s2
    - plan_role
    dependsOn:
    - s1
    - s2
    instruction: 'Build an in-app upgrade prompt shown to users whose {plan_role} attribute is admin or owner at accounts
      in the segment from "Find accounts near a limit". It shows how much of the plan limit the account has used (usage_capacity_used
      from "Find the bottleneck limit" as a percentage), one line on what the next plan adds, and one upgrade button. Helpful
      tone: we noticed your usage, not a hard sell.'
  - id: s4
    builds: email
    uses:
    - s1
    - s2
    - plan_role
    dependsOn:
    - s1
    - s2
    instruction: Write a short designed HTML email for users whose {plan_role} attribute is admin or owner at accounts in
      the segment from "Find accounts near a limit" that are at or over 100% of their plan limit. Say plainly that the account
      has reached its plan limit, what that means for their usage, and offer one button to review plans. Calm, factual, no
      prices.
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s4
    - plan_role
    - account_mrr
    - high_value_mrr
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s4
    instruction: Build an automation that starts when an account enters the segment from "Find accounts near a limit". If
      the account's usage_capacity_used from "Find the bottleneck limit" is 1 or more, it sends the email from "Write the
      over-limit notice" to the account's users whose {plan_role} attribute is admin or owner. If the account's {account_mrr}
      attribute is above {high_value_mrr}, it emails {alert_recipients} the account name, {account_mrr} and usage_capacity_used
      so an AE can reach out.
---

# Upgrade prompt when limits approach

Slash command: /usage-based-upgrade-trigger

## Step 1: Find the bottleneck limit

Build a computed attribute on accounts named "usage_capacity_used": the account's plan usage attribute divided by its plan limit attribute, as a number rounded to two decimals. Accounts with no plan limit value have no value.

## Step 2: Find accounts near a limit

Build a new segment of accounts named "Upgrade-ready accounts". An account is in it when its usage_capacity_used attribute from "Find the bottleneck limit" is 0.8 or more, its plan attribute is not enterprise, and none of its users did upgrade conversation in the last 30 d.

## Step 3: Write the in app prompt

Build an in-app upgrade prompt shown to users whose plan role attribute is admin or owner at accounts in the segment from "Find accounts near a limit". It shows how much of the plan limit the account has used (usage_capacity_used from "Find the bottleneck limit" as a percentage), one line on what the next plan adds, and one upgrade button. Helpful tone: we noticed your usage, not a hard sell.

## Step 4: Write the over-limit notice

Write a short designed HTML email for users whose plan role attribute is admin or owner at accounts in the segment from "Find accounts near a limit" that are at or over 100% of their plan limit. Say plainly that the account has reached its plan limit, what that means for their usage, and offer one button to review plans. Calm, factual, no prices.

## Step 5: Notify and call in an AE

Build an automation that starts when an account enters the segment from "Find accounts near a limit". If the account's usage_capacity_used from "Find the bottleneck limit" is 1 or more, it sends the email from "Write the over-limit notice" to the account's users whose plan role attribute is admin or owner. If the account's account mrr attribute is above 500, it emails the email addresses of the AE team alerted about high-value accounts the account name, account mrr and usage_capacity_used so an AE can reach out.
