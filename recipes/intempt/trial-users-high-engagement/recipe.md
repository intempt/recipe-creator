---
frontmatter_id: trial-users-high-engagement
slash_command: /trial-users-high-engagement
description: Trial users logging in constantly within their first week, the clearest early signal of a trial about to convert, fast-tracked to sales and offered a personal onboarding session.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Flags trial users who log in often in their first week and fast-tracks them to sales with a Slack alert and a personal
    onboarding session offer by email.
  parameters:
  - name: trialPlanValue
    type: string
    label: Plan attribute value that marks a trial user
    default: trial
  - name: signupWindow
    type: duration
    label: Window after subscription start in which the user qualifies
    default: 7 d
  - name: sessionThreshold
    type: number
    label: Minimum session starts required
    default: 5
  - name: sessionWindow
    type: duration
    label: Window for counting session starts
    default: 7 d
  - name: salesChannel
    type: string
    label: Slack channel name for sales alerts
    default: sales
  - name: tone
    type: enum
    label: Tone of the onboarding email
    default: warm and encouraging
    options:
    - warm and encouraging
    - professional
    - playful
  - name: callBookingUrl
    type: text
    label: Call-booking page link for the email button
    required: true
  requirements:
  - slot: trial_plan_attribute
    kind: attribute
    meaning: The user's plan attribute indicating their account plan, such as trial
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: email
      type: text
      meaning: The user's email address
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A user started a session by logging in to the product
  - slot: sales_slack
    kind: integration
    meaning: A Slack workspace connection with a sales channel for posting rep alerts
    channel: slack
  - slot: brand
    kind: brand
    meaning: The brand voice and identity used in customer emails
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - trial_plan_attribute
    - subscription_started_event
    - session_start_event
    - trialPlanValue
    - signupWindow
    - sessionThreshold
    - sessionWindow
    instruction: 'Build a new segment named "Trial Users: High Engagement" of users who are still on their trial and not yet
      paying (never people who already converted): their {trial_plan_attribute} is {trialPlanValue}, who did {subscription_started_event}
      at least once between 0 and {signupWindow} ago, and who did {session_start_event} {sessionThreshold} or more times in
      the last {sessionWindow}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_slack
    - salesChannel
    dependsOn:
    - s1
    instruction: Write a Slack message for the {salesChannel} channel for each user in the segment from "Build the fast-starter
      list" listing their email address {subscription_started_event.email} so reps can reach out while interest is at its
      peak. Use the result of "Build the fast-starter list". Take names and addresses from the member list in the result of
      the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste
      anything in.
  - id: s3
    builds: email
    uses:
    - s1
    - tone
    - callBookingUrl
    - brand
    dependsOn:
    - s1
    instruction: Create a designed marketing email for users in the segment from "Build the fast-starter list" congratulating
      them on their fast start and offering a personal onboarding session. Write exactly three sentences in a {tone} tone
      with no discount language. Include one button linking to {callBookingUrl}. Use the result of "Build the fast-starter
      list". If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for
      this run or named in this step; never leave a button without a link.
---

# Fast-starter trials

Slash command: /trial-users-high-engagement

## Step 1: Build the fast-starter list

Build a new segment named "Trial Users: High Engagement" of users who are still on their trial and not yet paying (never people who already converted): their trial plan attribute is trial, who did subscription started event at least once between 0 and 7 d ago, and who did session start event 5 or more times in the last 7 d.

## Step 2: Fast-track to sales

Write a Slack message for the sales channel for each user in the segment from "Build the fast-starter list" listing their email address email so reps can reach out while interest is at its peak. Use the result of "Build the fast-starter list". Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.

## Step 3: Offer a personal onboarding session

Create a designed marketing email for users in the segment from "Build the fast-starter list" congratulating them on their fast start and offering a personal onboarding session. Write exactly three sentences in a warm and encouraging tone with no discount language. Include one button linking to the call-booking page link for the email button. Use the result of "Build the fast-starter list". If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
