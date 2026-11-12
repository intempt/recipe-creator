---
frontmatter_id: paid-users-low-engagement
slash_command: /paid-users-low-engagement
description: Paying customers who have stopped logging in recently, nudged with a feature reminder and flagged to customer success before they slide into real churn risk.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Nudges paying customers who have gone quiet with a friendly feature reminder email and flags them to customer success
    before they become real churn risks.
  parameters:
  - name: inactivity_window
    type: duration
    label: Inactivity window (no session start within this period)
    default: 14 d
    required: false
  - name: excluded_plans
    type: text
    label: Plan values excluded from the segment
    default: free, trial
    required: false
  - name: reminder_tone
    type: string
    label: Tone of the feature reminder email
    default: friendly and low-pressure
    required: false
  - name: reminder_sentence_count
    type: number
    label: Number of sentences in the feature reminder email
    default: 3
    required: false
  requirements:
  - slot: low_engagement_paid_segment
    kind: segment
    meaning: Paying customers who have not started a session recently
    creatable: true
    definition: users whose Plan attribute is not {excluded_plans} and who did not do {session_start} in the last {inactivity_window}
  - slot: session_start
    kind: event
    meaning: A customer started a session in the product
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a user is on (e.g. free, trial, paid)
  - slot: customer_success_list
    kind: destination
    meaning: The customer success team's distribution list for email
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start
    - plan_attribute
    - inactivity_window
    - excluded_plans
    - low_engagement_paid_segment
    instruction: 'Build a segment named "Paid Users: Low Engagement" containing users whose {plan_attribute} is not any of
      {excluded_plans}, and who did not do {session_start} in the last {inactivity_window}.'
  - id: s2
    builds: email
    uses:
    - s1
    - reminder_tone
    - reminder_sentence_count
    instruction: 'Generate a designed marketing email for the users in the "Paid Users: Low Engagement" segment from step
      "Build the low-engagement list". The email reminds each user of one feature that drew them to sign up in the first place.
      Write {reminder_sentence_count} sentences in a {reminder_tone} tone. Include no discount language. Include one button
      that links back into the product.'
  - id: s3
    builds: email_plain
    uses:
    - s1
    - customer_success_list
    instruction: 'Generate a plain-text email to {customer_success_list}. For each user in the "Paid Users: Low Engagement"
      segment from step "Build the low-engagement list", list their email address so the team can check in before they become
      a real churn risk.'
---

# Paying users going quiet early

Slash command: /paid-users-low-engagement

## Step 1: Build the low-engagement list

Build a segment of users named "Paid Users: Low Engagement".
A user is in the segment only when all of these are true:
- their Plan attribute is not "free"
- their Plan attribute is not "trial"
- they did not do the Session start event in the last 14 days

## Step 2: Send a feature reminder

Generate a designed marketing email for the users in "Paid Users: Low Engagement" reminding them of one feature that made them sign up in the first place. Three sentences, friendly and low-pressure tone, no discount language, one button linking back into the product. Use the result of "Build the low-engagement list".

## Step 3: Flag to customer success

Generate a plain-text email to the customer success distribution list For each user in "Paid Users: Low Engagement", name their email address, so the team can check in before this turns into real churn risk. Use the result of "Build the low-engagement list".
