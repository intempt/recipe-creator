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
    - churn_window
    - min_lifetime_value
    - activity_window
    instruction: 'Build a new segment named "Winnable Churned Users". A user is in the segment only when all of these are
      true: they did {subscription_canceled_event} at least once in the last {churn_window}; their {lifetime_value_attribute}
      is more than {min_lifetime_value}; they did {session_start_event} at least once in the last {activity_window}.'
  - id: s2
    builds: sms
    uses:
    - sms_tone
    - s1
    dependsOn:
    - s1
    instruction: Generate an SMS for the users in the segment from "Build the win-back list" telling them they are welcome
      back and that it only takes a minute to reactivate. Use one or two sentences, a {sms_tone} tone, and no discount language.
      Use the segment built in "Build the win-back list".
  - id: s3
    builds: slack
    uses:
    - retention_team_slack
    - customer_email_attribute
    - s1
    dependsOn:
    - s1
    instruction: Generate a Slack message to {retention_team_slack}. For each user in the segment from "Build the win-back
      list", include their {customer_email_attribute} and note that they are still active despite cancelling, so the team
      prioritizes them first. Use the segment built in "Build the win-back list". Take names and addresses from the member
      list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask
      the reader to paste anything in.
---

# Winnable churned users

Slash command: /winnable-churned-users

## Step 1: Build the win-back list

Build a new segment named "Winnable Churned Users". A user is in the segment only when all of these are true: they did subscription canceled event at least once in the last 60 d; their lifetime value attribute is more than 0; they did session start event at least once in the last 7 d.

## Step 2: Send a quick win-back text

Generate an SMS for the users in the segment from "Build the win-back list" telling them they are welcome back and that it only takes a minute to reactivate. Use one or two sentences, a warm and direct tone, and no discount language. Use the segment built in "Build the win-back list".

## Step 3: Alert the retention team

Generate a Slack message to retention team slack. For each user in the segment from "Build the win-back list", include their customer email attribute and note that they are still active despite cancelling, so the team prioritizes them first. Use the segment built in "Build the win-back list". Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.
