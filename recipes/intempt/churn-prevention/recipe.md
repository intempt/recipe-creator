---
frontmatter_id: churn-prevention
slash_command: /churn-prevention
description: Scores churn risk, reaches medium-risk users with a win-back email while it is still cheap to fix, emails a CSM
  alert for high-risk users, and emails a weekly churn digest by risk tier.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores churn risk, emails medium-risk users a win-back message, alerts CSMs by email about high-risk users, and
    emails a weekly churn-by-tier digest.
  parameters:
  - name: high_risk_threshold
    type: number
    label: High-risk score threshold (0-1)
    default: 0.8
    required: false
  - name: medium_risk_threshold
    type: number
    label: Medium-risk score threshold (0-1)
    default: 0.5
    required: false
  - name: scoring_window
    type: duration
    label: Engagement decline lookback window
    default: 30 d
    required: false
  - name: win_back_tone
    type: enum
    label: Tone of win-back emails
    default: friendly
    required: false
    options:
    - friendly
    - professional
    - casual
  - name: alert_recipients
    type: string
    label: Email addresses of the CSMs who get high-risk alerts
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  - slot: feature_used
    kind: event
    meaning: A user used a product feature
    properties:
    - name: feature_name
      type: string
      meaning: Name of the feature used
      optional: false
  - slot: support_ticket
    kind: event
    meaning: A customer opened a support ticket
    optional: true
  - slot: subscription_canceled
    kind: event
    meaning: A customer canceled their subscription
  steps:
  - id: s1
    builds: attribute
    uses:
    - session_start
    - feature_used
    - support_ticket
    - scoring_window
    instruction: Build a computed attribute on users named "churn_risk_score", a number from 0 to 1. It rises with the drop
      in their {session_start} count in the last {scoring_window} against the {scoring_window} before, with the drop in distinct
      {feature_used.feature_name} values over the same windows, and with {support_ticket} events in the last {scoring_window}.
      Users with no {session_start} at any time get no value.
  - id: s2
    builds: segment
    uses:
    - s1
    - medium_risk_threshold
    - subscription_canceled
    dependsOn:
    - s1
    instruction: 'Build a new segment of users named "Churn risk: medium and high". A user is in it when the attribute from
      "Score churn risk" is {medium_risk_threshold} or more and they did not do {subscription_canceled} at any time.'
  - id: s3
    builds: email
    uses:
    - win_back_tone
    instruction: Write a re-engagement email in a {win_back_tone} tone for customers whose product use has dropped. It reminds
      them of the value they got, shows one feature they have not tried with one line on what it does, includes a short customer
      success story, and has one button back into the product. No discount.
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - medium_risk_threshold
    - high_risk_threshold
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s3
    instruction: 'Build an automation that runs every day at 09:00 on the segment from "Find medium and high risk". For each
      user it reads the attribute from "Score churn risk": below {high_risk_threshold} it sends the email from "Write the
      win back email", at most once every 30 days; at {high_risk_threshold} or more, the first time a user reaches it in 30
      days, it emails an alert to {alert_recipients} with the user''s name, email, score and last session date.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s4
    - subscription_canceled
    - medium_risk_threshold
    - high_risk_threshold
    - digest_recipients
    dependsOn:
    - s1
    - s2
    - s4
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users with the attribute
      from "Score churn risk" and writes these figures: user counts below {medium_risk_threshold}, medium and at {high_risk_threshold}
      or more, now and 7 days ago; the share in each tier who did {subscription_canceled} in the last 30 days; the share of
      users sent the email by "Reach them by risk tier" in the last 30 days who are now below {medium_risk_threshold}. Then
      it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Churn prevention

Slash command: /churn-prevention

## Step 1: Score churn risk

Build a computed attribute on users named "churn_risk_score", a number from 0 to 1. It rises with the drop in their session start count in the last 30 d against the 30 d before, with the drop in distinct feature name values over the same windows, and with support ticket events in the last 30 d. Users with no session start at any time get no value.

## Step 2: Find medium and high risk

Build a new segment of users named "Churn risk: medium and high". A user is in it when the attribute from "Score churn risk" is 0.5 or more and they did not do subscription canceled at any time.

## Step 3: Write the win back email

Write a re-engagement email in a friendly tone for customers whose product use has dropped. It reminds them of the value they got, shows one feature they have not tried with one line on what it does, includes a short customer success story, and has one button back into the product. No discount.

## Step 4: Reach them by risk tier

Build an automation that runs every day at 09:00 on the segment from "Find medium and high risk". For each user it reads the attribute from "Score churn risk": below 0.8 it sends the email from "Write the win back email", at most once every 30 days; at 0.8 or more, the first time a user reaches it in 30 days, it emails an alert to the email addresses of the CSMs who get high-risk alerts with the user's name, email, score and last session date.

## Step 5: Email the weekly churn digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users with the attribute from "Score churn risk" and writes these figures: user counts below 0.5, medium and at 0.8 or more, now and 7 days ago; the share in each tier who did subscription canceled in the last 30 days; the share of users sent the email by "Reach them by risk tier" in the last 30 days who are now below 0.5. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
