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
    instruction: Build a new segment named "At-Risk VIP Customers" of users whose {lifetime_value} is more than {ltv_threshold}
      and who did not do {session_start_event} in the last {inactivity_window}.
  - id: s2
    builds: email_plain
    uses:
    - s1
    - checkin_sentence_count
    - checkin_tone
    dependsOn:
    - s1
    instruction: 'Write a plain-text email for the users in the segment from "Build the at-risk VIP list" as a personal note
      from their account manager. It asks how things are going and offers a quick call. Use exactly {checkin_sentence_count}
      sentences in a {checkin_tone} tone. Do not pitch the product and do not use discount language. Use the segment built
      in "Build the at-risk VIP list". The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe
      line.'
  - id: s3
    builds: slack
    uses:
    - retention_team_slack
    - customer_email
    - lifetime_value
    - s1
    dependsOn:
    - s1
    instruction: Write a Slack message to the retention team channel {retention_team_slack}. For each user in the segment
      from "Build the at-risk VIP list", list their {customer_email} and their {lifetime_value}, sorted so the highest-value
      accounts come first for outreach prioritization. Use the segment built in "Build the at-risk VIP list". Take names and
      addresses from the member list in the result of the step that built the list (at most 20, then how many more); never
      write a placeholder or ask the reader to paste anything in.
---

# At-risk VIP customers

Slash command: /at-risk-vips

## Step 1: Build the at-risk VIP list

Build a new segment named "At-Risk VIP Customers" of users whose lifetime value is more than 1000 and who did not do session start event in the last 30 d.

## Step 2: Draft a personal check-in

Write a plain-text email for the users in the segment from "Build the at-risk VIP list" as a personal note from their account manager. It asks how things are going and offers a quick call. Use exactly 3 sentences in a warm and personal tone. Do not pitch the product and do not use discount language. Use the segment built in "Build the at-risk VIP list". The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.

## Step 3: Alert the retention team

Write a Slack message to the retention team channel retention team slack. For each user in the segment from "Build the at-risk VIP list", list their customer email and their lifetime value, sorted so the highest-value accounts come first for outreach prioritization. Use the segment built in "Build the at-risk VIP list". Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.
