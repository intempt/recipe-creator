---
frontmatter_id: recently-churned-users
slash_command: /recently-churned-users
description: Customers who cancelled in the last month, sent a win-back email and flagged to the retention team while the reason is still fresh.
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
  summary: Wins back customers who cancelled within the last month with a warm email and alerts the retention team in Slack
    with their lifetime value.
  parameters:
  - name: lookback_window
    type: duration
    label: Cancellation lookback window
    default: 30 d
    required: false
  - name: min_lifetime_value
    type: number
    label: Minimum lifetime value (exclusive)
    default: 0
    required: false
  - name: email_tone
    type: string
    label: Email tone
    default: warm and non-defensive
    required: false
  - name: email_sentence_count
    type: number
    label: Number of sentences in the email
    default: 3
    required: false
  requirements:
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled their subscription
  - slot: lifetime_value
    kind: attribute
    meaning: The total lifetime value a customer has generated
  - slot: retention_slack
    kind: integration
    meaning: Slack workspace used to message the retention team
    channel: slack
  - slot: restart_subscription_page
    kind: destination
    meaning: Page where a customer can restart their subscription
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - subscription_canceled_event
    - lifetime_value
    - lookback_window
    - min_lifetime_value
    instruction: Build a new segment named "Recently Churned Users" containing users who did {subscription_canceled_event}
      at least once in the last {lookback_window} and whose {lifetime_value} is more than {min_lifetime_value}.
  - id: s2
    builds: email
    uses:
    - s1
    - restart_subscription_page
    - email_tone
    - email_sentence_count
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in the "Recently Churned Users" segment inviting them back.
      Write {email_sentence_count} sentences in a {email_tone} tone that ask what did not work and offer to help. Do not use
      discount language. Include one button linking to {restart_subscription_page} for restarting the subscription. If the
      brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or
      named in this step; never leave a button without a link.
  - id: s3
    builds: slack
    uses:
    - s1
    - retention_slack
    dependsOn:
    - s1
    instruction: Generate a Slack message to the retention team in {retention_slack}. For each user in the "Recently Churned
      Users" segment, include their email address and their {lifetime_value} so the team can track cancellation volume and
      follow up personally with the highest-value customers. Take names and addresses from the member list in the result of
      the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste
      anything in.
---

# Recently cancelled customers

Slash command: /recently-churned-users

## Step 1: Build the recent-cancel list

Build a new segment named "Recently Churned Users" containing users who did subscription canceled event at least once in the last 30 d and whose lifetime value is more than 0.

## Step 2: Draft a win-back email

Generate a designed marketing email for the users in the "Recently Churned Users" segment inviting them back. Write 3 sentences in a warm and non-defensive tone that ask what did not work and offer to help. Do not use discount language. Include one button linking to restart subscription page for restarting the subscription. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Notify the retention team

Generate a Slack message to the retention team in retention slack. For each user in the "Recently Churned Users" segment, include their email address and their lifetime value so the team can track cancellation volume and follow up personally with the highest-value customers. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.
