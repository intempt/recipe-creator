---
frontmatter_id: onboarding-stalled-users
slash_command: /onboarding-stalled-users
description: Trial users logging in often enough to be ready to buy, offered a personal demo by email while sales still has the window to close them.
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
  summary: Trial users who log in often are sent a personal demo offer by email, and the sales team is alerted in Slack so
    they can follow up while the trial is open.
  parameters:
  - name: session_threshold
    type: number
    label: Minimum session starts in the window
    default: 5
    required: false
  - name: window
    type: duration
    label: Activity window
    default: 14 d
    required: false
  - name: plan_value
    type: string
    label: Plan attribute value that marks a trial user
    default: trial
    required: false
  - name: demo_tone
    type: string
    label: Tone of the demo email
    default: warm and helpful
    required: false
  - name: sales_channel
    type: string
    label: Sales Slack channel
    default: sales
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
    properties:
    - name: user_email
      type: string
      meaning: Email address of the user
      optional: false
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a user is on
  - slot: sales_slack
    kind: integration
    meaning: A Slack workspace connection for posting alerts to the sales channel
    channel: slack
  - slot: demo_booking_page
    kind: destination
    meaning: A web page where users can book a personal product demo
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - plan_attribute
    - session_threshold
    - window
    - plan_value
    instruction: 'Build a new segment named "Engaged Trial Users" containing users who are still on their trial and not yet
      paying (never people who already converted): their {plan_attribute} is {plan_value} and who did {session_start_event}
      at least {session_threshold} times in the last {window}.'
  - id: s2
    builds: email
    uses:
    - demo_booking_page
    - demo_tone
    - s1
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in the "Engaged Trial Users" segment offering a personal
      walkthrough of a feature they have not tried yet. Write three sentences in a {demo_tone} tone with no discount language.
      Include one button linking to {demo_booking_page}. If the brand kit has no logo, use the brand name as a plain text
      header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
  - id: s3
    builds: slack
    uses:
    - sales_slack
    - sales_channel
    - s1
    dependsOn:
    - s1
    instruction: Generate a Slack message to the {sales_channel} channel that lists the email address of each user in the
      "Engaged Trial Users" segment, so reps can reach out while the trial window is still open. It is for {sales_slack}.
---

# Engaged trial users

Slash command: /onboarding-stalled-users

## Step 1: Build the engaged-trial list

Build a new segment named "Engaged Trial Users" containing users who are still on their trial and not yet paying (never people who already converted): their plan attribute is trial and who did session start event at least 5 times in the last 14 d.

## Step 2: Offer a personal demo

Generate a designed marketing email for the users in the "Engaged Trial Users" segment offering a personal walkthrough of a feature they have not tried yet. Write three sentences in a warm and helpful tone with no discount language. Include one button linking to demo booking page. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Alert sales

Generate a Slack message to the sales channel that lists the email address of each user in the "Engaged Trial Users" segment, so reps can reach out while the trial window is still open. It is for sales slack.
