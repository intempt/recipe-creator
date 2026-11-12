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
  - slot: engaged_trial_users
    kind: segment
    meaning: Trial users who started sessions frequently in the recent window
    creatable: true
    definition: users whose {plan_attribute} is {plan_value} and who did {session_start_event} at least {session_threshold}
      times in the last {window}
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
    instruction: Build a segment named "Engaged Trial Users" containing users whose {plan_attribute} is {plan_value} and who
      did {session_start_event} at least {session_threshold} times in the last {window}.
  - id: s2
    builds: email
    uses:
    - engaged_trial_users
    - demo_booking_page
    - demo_tone
    - s1
    instruction: Generate a designed marketing email for the users in the "Engaged Trial Users" segment offering a personal
      walkthrough of a feature they have not tried yet. Write three sentences in a {demo_tone} tone with no discount language.
      Include one button linking to {demo_booking_page}.
  - id: s3
    builds: slack
    uses:
    - sales_slack
    - engaged_trial_users
    - sales_channel
    - s1
    instruction: Generate a Slack message to the {sales_channel} channel that lists the email address of each user in the
      "Engaged Trial Users" segment, so reps can reach out while the trial window is still open. Use {sales_slack} to post
      it.
---

# Engaged trial users

Slash command: /onboarding-stalled-users

## Step 1: Build the engaged-trial list

Build a segment of users named "Engaged Trial Users".
A user is in the segment only when all of these are true:
- their Plan attribute is "trial"
- they did the Session start event 5 or more times in the last 14 days

## Step 2: Offer a personal demo

Generate a designed marketing email for the users in "Engaged Trial Users" offering a personal walkthrough of a feature they have not tried yet. Three sentences, warm and helpful tone, no discount language, one button linking to the demo booking page. Use the result of "Build the engaged-trial list".

## Step 3: Alert sales

Generate a Slack message to the sales channel For each user in "Engaged Trial Users", name their email address, so reps can reach out while the trial window is still open. Use the result of "Build the engaged-trial list".
