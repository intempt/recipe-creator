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
  - slot: trial_high_engagement_segment
    kind: segment
    meaning: Trial users who log in frequently within their first week
    creatable: true
    definition: users whose {trial_plan_attribute} is {trialPlanValue} and who did {subscription_started_event} at least once
      between 0 and {signupWindow} ago and did {session_start_event} at least {sessionThreshold} times in the last {sessionWindow}
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
    instruction: 'Build a segment named "Trial Users: High Engagement" of users whose {trial_plan_attribute} is {trialPlanValue},
      who did {subscription_started_event} at least once between 0 and {signupWindow} ago, and who did {session_start_event}
      {sessionThreshold} or more times in the last {sessionWindow}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_slack
    - salesChannel
    - trial_high_engagement_segment
    instruction: Send a Slack message to the {salesChannel} channel for each user in {trial_high_engagement_segment} listing
      their email address {subscription_started_event.email} so reps can reach out while interest is at its peak. Use the
      result of "Build the fast-starter list".
  - id: s3
    builds: email
    uses:
    - s1
    - trial_high_engagement_segment
    - tone
    - callBookingUrl
    - brand
    instruction: Create a designed marketing email for users in {trial_high_engagement_segment} congratulating them on their
      fast start and offering a personal onboarding session. Write exactly three sentences in a {tone} tone with no discount
      language. Include one button linking to {callBookingUrl}. Use the result of "Build the fast-starter list".
---

# Fast-starter trials

Slash command: /trial-users-high-engagement

## Step 1: Build the fast-starter list

Build a segment of users named "Trial Users: High Engagement".
A user is in the segment only when all of these are true:
- their Plan attribute is "trial"
- they did the Subscription started event at least once between 0 and 7 days ago
- they did the Session start event 5 or more times in the last 7 days

## Step 2: Fast-track to sales

Generate a Slack message to the sales channel For each user in "Trial Users: High Engagement", name their email address, so reps can reach out while interest is at its peak. Use the result of "Build the fast-starter list".

## Step 3: Offer a personal onboarding session

Generate a designed marketing email for the users in "Trial Users: High Engagement" congratulating them on their fast start and offering a personal onboarding session. Three sentences, warm and encouraging tone, no discount language, one button linking to a call-booking page. Use the result of "Build the fast-starter list".
