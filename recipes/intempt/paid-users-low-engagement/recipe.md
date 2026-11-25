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
    instruction: 'Build a new segment named "Paid Users: Low Engagement" containing users whose {plan_attribute} has a value
      and is not any of {excluded_plans}, and who did not do {session_start} in the last {inactivity_window}.'
  - id: s2
    builds: email
    uses:
    - s1
    - reminder_tone
    - reminder_sentence_count
    dependsOn:
    - s1
    instruction: 'Generate a designed marketing email for the users in the "Paid Users: Low Engagement" segment from step
      "Build the low-engagement list". The email reminds each user of one feature that drew them to sign up in the first place.
      Write {reminder_sentence_count} sentences in a {reminder_tone} tone. Include no discount language. Include one button
      that links back into the product. If the brand kit has no logo, use the brand name as a plain text header. Every button
      links to a URL given for this run or named in this step; never leave a button without a link.'
  - id: s3
    builds: email_plain
    uses:
    - s1
    - customer_success_list
    dependsOn:
    - s1
    instruction: 'Generate a plain-text email to {customer_success_list}. For each user in the "Paid Users: Low Engagement"
      segment from step "Build the low-engagement list", list their email address so the team can check in before they become
      a real churn risk. Take names and addresses from the member list in the result of the step that built the list (at most
      20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain
      text only: no HTML tags, no markup and no unsubscribe line.'
---

# Paying users going quiet early

Slash command: /paid-users-low-engagement

## Step 1: Build the low-engagement list

Build a new segment named "Paid Users: Low Engagement" containing users whose plan attribute has a value and is not any of free, trial, and who did not do session start in the last 14 d.

## Step 2: Send a feature reminder

Generate a designed marketing email for the users in the "Paid Users: Low Engagement" segment from step "Build the low-engagement list". The email reminds each user of one feature that drew them to sign up in the first place. Write 3 sentences in a friendly and low-pressure tone. Include no discount language. Include one button that links back into the product. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Flag to customer success

Generate a plain-text email to customer success list. For each user in the "Paid Users: Low Engagement" segment from step "Build the low-engagement list", list their email address so the team can check in before they become a real churn risk. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.
