---
frontmatter_id: winnable-churned-users
slash_command: /winnable-churned-users
description: Customers who cancelled in the last two months but are still logging in, texted a quick way back in and flagged to the retention team as the best odds for a win-back.
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
  summary: Texts recently cancelled customers who are still logging in a quick welcome-back message, and alerts the retention
    team to prioritize them for win-back.
  parameters:
  - name: churn_window
    type: duration
    label: Lookback window for cancellation
    default: 60 d
    required: false
  - name: activity_window
    type: duration
    label: Recent login activity window
    default: 7 d
    required: false
  - name: min_lifetime_value
    type: number
    label: Minimum lifetime value (exclusive)
    default: 0
    required: false
  - name: sms_tone
    type: enum
    label: Tone of the win-back text
    default: warm and direct
    required: false
    options:
    - warm and direct
    - friendly and casual
    - formal
  requirements:
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled their subscription
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the app or website
  - slot: lifetime_value_attribute
    kind: attribute
    meaning: The total lifetime value a customer has generated
  - slot: customer_email_attribute
    kind: attribute
    meaning: The email address of a customer
  - slot: winnable_churned_users
    kind: segment
    meaning: Users who canceled recently, have lifetime value above the minimum, and were active recently
    creatable: true
    definition: users who did {subscription_canceled_event} at least once in the last {churn_window} and whose {lifetime_value_attribute}
      is more than {min_lifetime_value} and who did {session_start_event} at least once in the last {activity_window}
  - slot: retention_team_slack
    kind: destination
    meaning: The Slack channel used by the retention team
    channel: slack
  - slot: sms_connection
    kind: integration
    channel: sms
    meaning: The SMS sender the text goes out from
  steps:
  - id: s1
    builds: segment
    uses:
    - subscription_canceled_event
    - session_start_event
    - lifetime_value_attribute
    - winnable_churned_users
    - churn_window
    - min_lifetime_value
    - activity_window
    instruction: 'Build a segment named {winnable_churned_users}. A user is in the segment only when all of these are true:
      they did {subscription_canceled_event} at least once in the last {churn_window}; their {lifetime_value_attribute} is
      more than {min_lifetime_value}; they did {session_start_event} at least once in the last {activity_window}.'
  - id: s2
    builds: sms
    uses:
    - winnable_churned_users
    - sms_tone
    - s1
    instruction: Generate an SMS for the users in {winnable_churned_users} telling them they are welcome back and that it
      only takes a minute to reactivate. Use one or two sentences, a {sms_tone} tone, and no discount language. Use the segment
      built in "Build the win-back list".
  - id: s3
    builds: slack
    uses:
    - retention_team_slack
    - winnable_churned_users
    - customer_email_attribute
    - s1
    instruction: Generate a Slack message to {retention_team_slack}. For each user in {winnable_churned_users}, include their
      {customer_email_attribute} and note that they are still active despite cancelling, so the team prioritizes them first.
      Use the segment built in "Build the win-back list".
---

# Winnable churned users

Slash command: /winnable-churned-users

## Step 1: Build the win-back list

Build a segment of users named "Winnable Churned Users".
A user is in the segment only when all of these are true:
- they did the Subscription canceled event at least once in the last 60 days
- their Lifetime value attribute is more than 0
- they did the Session start event at least once in the last 7 days

## Step 2: Send a quick win-back text

Generate an SMS for the users in "Winnable Churned Users" letting them know they are welcome back and it only takes a minute to reactivate. One or two sentences, warm and direct tone, no discount language. Use the result of "Build the win-back list".

## Step 3: Alert the retention team

Generate a Slack message to the retention team channel For each user in "Winnable Churned Users", name their email address, and noting that they are still active despite cancelling, so the team prioritizes them first. Use the result of "Build the win-back list".
