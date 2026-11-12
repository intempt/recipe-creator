---
frontmatter_id: at-risk-vips
slash_command: /at-risk-vips
description: High lifetime value customers who have stopped logging in, checked on personally by their account manager and flagged to the retention team before they churn.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Finds high-value customers who have stopped logging in, sends each a personal check-in email from their account
    manager, and alerts the retention team on Slack.
  parameters:
  - name: ltv_threshold
    type: number
    label: Lifetime value above which a customer counts as VIP
    default: 1000
    required: false
  - name: inactivity_window
    type: duration
    label: Period without a session start before a customer counts as at risk
    default: 30 d
    required: false
  - name: checkin_sentence_count
    type: number
    label: Number of sentences in the check-in email
    default: 3
    required: false
  - name: checkin_tone
    type: enum
    label: Tone of the check-in email
    default: warm and personal
    required: false
    options:
    - warm and personal
    - formal
    - casual
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A customer started a session by logging in to the product
  - slot: lifetime_value
    kind: attribute
    meaning: The total lifetime value a customer has generated
  - slot: customer_email
    kind: attribute
    meaning: The email address of a customer
  - slot: at_risk_vip_customers
    kind: segment
    meaning: High lifetime value customers who have not started a session recently
    creatable: true
    definition: users whose {lifetime_value} is more than {ltv_threshold} and who did not do {session_start_event} in the
      last {inactivity_window}
  - slot: retention_team_slack
    kind: integration
    meaning: A Slack workspace connection with a channel for the retention team
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - lifetime_value
    - session_start_event
    - ltv_threshold
    - inactivity_window
    instruction: Build a segment named "At-Risk VIP Customers" of users whose {lifetime_value} is more than {ltv_threshold}
      and who did not do {session_start_event} in the last {inactivity_window}.
  - id: s2
    builds: email_plain
    uses:
    - at_risk_vip_customers
    - s1
    - checkin_sentence_count
    - checkin_tone
    instruction: Write a plain-text email for the users in {at_risk_vip_customers} as a personal note from their account manager.
      It asks how things are going and offers a quick call. Use exactly {checkin_sentence_count} sentences in a {checkin_tone}
      tone. Do not pitch the product and do not use discount language. Use the segment built in "Build the at-risk VIP list".
  - id: s3
    builds: slack
    uses:
    - retention_team_slack
    - at_risk_vip_customers
    - customer_email
    - lifetime_value
    - s1
    instruction: Write a Slack message to the retention team channel {retention_team_slack}. For each user in {at_risk_vip_customers},
      list their {customer_email} and their {lifetime_value}, sorted so the highest-value accounts come first for outreach
      prioritization. Use the segment built in "Build the at-risk VIP list".
---

# At-risk VIP customers

Slash command: /at-risk-vips

## Step 1: Build the at-risk VIP list

Build a segment of users named "At-Risk VIP Customers".
A user is in the segment only when all of these are true:
- their Lifetime value attribute is more than 1000
- they did not do the Session start event in the last 30 days

## Step 2: Draft a personal check-in

Generate a plain-text email for the users in "At-Risk VIP Customers" written as a personal note from their account manager, asking how things are going and offering a quick call. Three sentences, warm and personal tone, no product pitch, no discount language. Use the result of "Build the at-risk VIP list".

## Step 3: Alert the retention team

Generate a Slack message to the retention team channel For each user in "At-Risk VIP Customers", name their email address and their Lifetime value, so the team can prioritize outreach to the highest-value accounts first. Use the result of "Build the at-risk VIP list".
