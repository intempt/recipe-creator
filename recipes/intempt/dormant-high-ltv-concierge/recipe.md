---
frontmatter_id: dormant-high-ltv-concierge
slash_command: /dormant-high-ltv-concierge
description: When one of your most valuable accounts stops showing up for a month, it emails the CSM team a briefing and asks
  them to call. Nothing is sent to the customer.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: When a top-value account goes quiet for a month, the CSM team gets an emailed briefing to call, plus a weekly digest
    of dormant value and re-engagement. Nothing goes to customers.
  parameters:
  - name: dormancy_threshold
    type: duration
    label: Days without session activity before an account counts as dormant
    default: 30 d
    required: false
  - name: ltv_top_percent
    type: number
    label: Top percentile by LTV that counts as high-LTV
    default: 10
    required: false
  - name: csm_contact_window
    type: duration
    label: Window in which a recent CSM contact rules out dormancy
    default: 30 d
    required: false
  - name: response_target
    type: duration
    label: Target CSM response time on dormancy alerts
    default: 48 h
    required: false
  - name: re_engagement_window
    type: duration
    label: Window after CSM outreach to count re-engagement
    default: 14 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the CSMs and managers who get the briefings
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: account_session_event
    kind: event
    meaning: A user started a session on a customer account
    properties:
    - name: account_id
      type: string
      meaning: Account the session belongs to
      optional: false
  - slot: account_revenue_attributes
    kind: attribute
    meaning: 'Account revenue fields: cumulative paid revenue and current monthly recurring revenue'
  - slot: csm_contact_record
    kind: event
    meaning: A CSM logged a contact or meeting with a customer account
    properties:
    - name: contact_date
      type: date
      meaning: Date of the CSM contact
      optional: false
  - slot: pause_status_attribute
    kind: attribute
    meaning: Account flag marking a known temporary pause such as legal review or annual leave
    optional: true
  - slot: support_ticket_data
    kind: knowledge
    meaning: Recent support tickets and last meeting summaries for customer accounts
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_revenue_attributes
    instruction: 'Build a computed attribute on accounts named "account_ltv", a number refreshed daily: the account''s cumulative
      paid revenue plus its current monthly recurring revenue times 24, both from {account_revenue_attributes}.'
  - id: s2
    builds: segment
    uses:
    - s1
    - account_session_event
    - csm_contact_record
    - pause_status_attribute
    - ltv_top_percent
    - dormancy_threshold
    - csm_contact_window
    dependsOn:
    - s1
    instruction: 'Build a new segment of accounts named "High-LTV Dormant Accounts". An account is in it when all of these
      are true: its account_ltv from "Track account value" is in the top {ltv_top_percent}% of all accounts; none of its users
      did {account_session_event} in the last {dormancy_threshold}; it has no {csm_contact_record} in the last {csm_contact_window};
      its {pause_status_attribute} is not set.'
  - id: s3
    builds: automation
    uses:
    - s2
    - account_session_event
    - support_ticket_data
    - alert_recipients
    dependsOn:
    - s2
    instruction: 'Build an automation triggered when an account enters the segment from "Find the valuable ones gone quiet".
      An analysis step writes: days since the last {account_session_event} on the account; whether its sessions were falling
      in the 60 days before that; its recent support topics from {support_ticket_data}; one suggested outreach angle (check-in,
      re-onboarding offer, or executive sponsor introduction). Then it emails {alert_recipients} the account name, its account_ltv
      and this briefing, asking the CSM to call. It sends nothing to the customer.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - csm_contact_record
    - account_session_event
    - response_target
    - re_engagement_window
    - digest_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the segment from
      "Find the valuable ones gone quiet" and writes these figures: the number of accounts in it now and 7 days ago; the sum
      of their account_ltv; of the accounts that entered it in the last 30 days, the share with a {csm_contact_record} within
      {response_target} of entering; the share whose users did {account_session_event} again within {re_engagement_window}
      of that contact. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing
      else is sent.'
---

# Concierge for dormant big accounts

Slash command: /dormant-high-ltv-concierge

## Step 1: Track account value

Build a computed attribute on accounts named "account_ltv", a number refreshed daily: the account's cumulative paid revenue plus its current monthly recurring revenue times 24, both from account revenue attributes.

## Step 2: Find the valuable ones gone quiet

Build a new segment of accounts named "High-LTV Dormant Accounts". An account is in it when all of these are true: its account_ltv from "Track account value" is in the top 10% of all accounts; none of its users did account session event in the last 30 d; it has no csm contact record in the last 30 d; its pause status attribute is not set.

## Step 3: Brief the CSM team

Build an automation triggered when an account enters the segment from "Find the valuable ones gone quiet". An analysis step writes: days since the last account session event on the account; whether its sessions were falling in the 60 days before that; its recent support topics from support ticket data; one suggested outreach angle (check-in, re-onboarding offer, or executive sponsor introduction). Then it emails the email addresses of the CSMs and managers who get the briefings the account name, its account_ltv and this briefing, asking the CSM to call. It sends nothing to the customer.

## Step 4: Email the weekly dormant-value digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the segment from "Find the valuable ones gone quiet" and writes these figures: the number of accounts in it now and 7 days ago; the sum of their account_ltv; of the accounts that entered it in the last 30 days, the share with a csm contact record within 48 h of entering; the share whose users did account session event again within 14 d of that contact. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
