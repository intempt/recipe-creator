---
frontmatter_id: enterprise-domain-signup-to-ae-task
slash_command: /enterprise-domain-signup-to-ae-task
description: Spots when a self serve signup comes from a large company, enriches it, and puts it in front of an AE instead of leaving it in the free funnel.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Routes self-serve signups from large companies to an AE with a high-priority task and Slack alert, pulls them out
    of the self-serve nurture, and tracks response time and conversion.
  parameters:
  - name: enterprise_employee_threshold
    type: number
    label: Employee count at or above which an account is tiered enterprise
    default: 1000
    required: false
  - name: mid_market_employee_threshold
    type: number
    label: Employee count at or above which an account is tiered mid-market
    default: 100
    required: false
  - name: lookback_window
    type: duration
    label: Window for enterprise signups to include
    default: 30 d
    required: false
  - name: response_time_target
    type: duration
    label: Target AE response time to a new enterprise signup
    default: 2 h
    required: false
  - name: alert_channel
    type: text
    label: Slack channel for enterprise alerts
    default: '#enterprise-alerts'
    required: false
  requirements:
  - slot: signup_event
    kind: event
    meaning: A user signed up for the self-serve product
    properties:
    - name: email_domain
      type: string
      meaning: Domain part of the signup email address
      optional: false
  - slot: account_employee_count
    kind: attribute
    meaning: Employee count of the account from firmographic enrichment
    optional: true
  - slot: target_account_list
    kind: segment
    meaning: Accounts on the company's named target-account list
    optional: true
  - slot: ae_assignment
    kind: attribute
    meaning: The AE (account executive) currently assigned to an account
    optional: true
  - slot: account_tier
    kind: attribute
    meaning: Account tier (enterprise, mid-market, smb, consumer) computed for each account
  - slot: enterprise_signups_segment
    kind: segment
    meaning: Enterprise accounts created recently with no AE assigned
    creatable: true
    definition: accounts where {account_tier} = enterprise AND account created within {lookback_window} AND no {ae_assignment}
      is set
  - slot: enrichment_provider
    kind: integration
    meaning: Firmographic and decision-maker enrichment data source
    optional: true
    channel: email
  - slot: ae_task_destination
    kind: destination
    meaning: CRM where AE tasks are created and account owners are stored
    channel: salesforce
  - slot: sales_alert_destination
    kind: destination
    meaning: Slack workspace channel that receives enterprise alerts
    channel: slack
  steps:
  - id: s1
    builds: attribute
    uses:
    - signup_event
    - account_employee_count
    - target_account_list
    - enterprise_employee_threshold
    - mid_market_employee_threshold
    instruction: 'Create an AI-derived attribute ''account_tier'' on the Account object, computed at signup from {signup_event.email_domain}.
      Output one of: enterprise, mid-market, smb, consumer. Cross-reference (a) {target_account_list}, (b) {account_employee_count}
      where 1000 or more ({enterprise_employee_threshold}) is enterprise and 100 to under 1000 ({mid_market_employee_threshold})
      is mid-market, (c) public-company indicator, (d) ideal customer profile industry match. Generic email domains such as
      gmail and outlook are tiered consumer, since they are unlikely to buy.'
  - id: s2
    builds: segment
    uses:
    - s1
    - enterprise_signups_segment
    - lookback_window
    instruction: Build segment 'Enterprise signups - last {lookback_window}' containing accounts where {account_tier} is enterprise,
      the account was created within {lookback_window}, and no {ae_assignment} is set. Use the result of "Work out the account
      tier". This segment serves both the workflow audit and post-hoc analysis of enterprise-lead conversion.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - enrichment_provider
    - ae_task_destination
    - sales_alert_destination
    - alert_channel
    instruction: 'Create a workflow triggered by a user signup event. Steps in order: (1) compute {account_tier} from the
      email domain; (2) if tier is enterprise or mid-market, immediately enrich the account with firmographics, decision-makers
      and tech stack from {enrichment_provider}; (3) check whether the account already exists in {ae_task_destination} or
      is on {target_account_list}; (4) create a task in {ae_task_destination} for the enterprise-tier AE with priority HIGH,
      assigned by territory and named-account rules, preserving any pre-assigned account owner; (5) post a high-visibility
      alert to {alert_channel} in {sales_alert_destination} containing account context, decision-maker contacts and current
      product activity; (6) exclude this user from the standard self-serve nurture journey, since enterprise follows a sales-led
      motion. Use the result of "Work out the account tier" and "Find enterprise signups with no AE".'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - response_time_target
    - ae_task_destination
    instruction: 'Build an enterprise-lead dashboard showing: weekly enterprise signup volume; AE response time against the
      target of {response_time_target} during business hours; enterprise-signup-to-meeting conversion; enterprise-signup-to-deal
      conversion (typically 60 or more days); enterprise pipeline value sourced this way, reported separately from outbound;
      and the {account_tier} mix (enterprise, mid-market, smb, consumer) across all signups to track ICP attraction trends.
      Use the results of "Work out the account tier", "Find enterprise signups with no AE" and "Hand it to the right AE".'
---

# Enterprise signup to AE task

Slash command: /enterprise-domain-signup-to-ae-task

## Step 1: Work out the account tier

Create an AI-derived attribute 'account_tier' on the Account object. Computed at signup from email domain. Output: enterprise / mid-market / smb / consumer (generic email). Logic: cross-reference against (a) target-account list, (b) employee-count enrichment if available (1000+ = enterprise, 100-1000 = mid-market), (c) public-company indicator, (d) ICP industry match. Generic email domains (gmail, outlook) to tier: consumer (likely not a buyer).

## Step 2: Find enterprise signups with no AE

Build a segment 'Enterprise signups - last 30 days' capturing accounts where account_tier = enterprise AND the account was created in last 30 days AND no AE has been assigned. Used for both the workflow audit and post-hoc analysis of enterprise-lead conversion. Use the result of "Work out the account tier".

## Step 3: Hand it to the right AE

Create a workflow firing on user_signed_up. Step sequence: (1) compute account_tier from the email domain; (2) if tier = enterprise or mid-market: immediately enrich (firmographics, decision-makers, tech stack); (3) check whether the account is already in the CRM or part of target-account list; (4) create an enterprise-tier AE task with priority HIGH, assigned by territory + named-account rules (preserving any pre-assigned account owner); (5) post a high-visibility Slack alert to #enterprise-alerts with account context, decision-maker contacts, and current product activity; (6) suppress this user from the standard self-serve nurture journey (different motion for enterprise: sales-led, not marketing-led). Use the result of "Work out the account tier", "Find enterprise signups with no AE".

## Step 4: Watch the response time

Compose an enterprise-lead dashboard: enterprise signup volume per week, AE response time (target: <2hr business hours), enterprise-signup-to-meeting conversion, enterprise-signup-to-deal conversion (typically takes 60+ days), enterprise pipeline value sourced this way (separate from outbound), and account-tier mix (enterprise / mid-market / smb / consumer) of all signups so leadership can see ICP attraction trends. Use the result of "Work out the account tier", "Find enterprise signups with no AE", "Hand it to the right AE".
