---
frontmatter_id: predictive-churn-tiered-intervention
slash_command: /predictive-churn-tiered-intervention
description: 'Scores churn risk daily for paying users and treats each band differently: a helpful tips email at medium risk,
  a personal offer of help at high and critical risk, and an alert to the team for critical risk.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores paying users' churn risk 0-100, builds the at-risk segment, and runs a weekly automation that emails each
    risk band its own message and alerts the team on critical risk.
  parameters:
  - name: risk_threshold
    type: number
    label: Minimum churn risk score to enter intervention
    default: 30
    required: false
  - name: new_user_grace_period
    type: duration
    label: Grace period for newly signed-up users
    default: 14 d
    required: false
  - name: critical_response_window
    type: duration
    label: Time the team has to start critical-tier outreach
    default: 4 h
    required: false
  - name: medium_tone
    type: enum
    label: Tone for medium-tier emails
    default: helpful
    required: false
    options:
    - helpful
    - neutral
    - encouraging
  - name: walkthrough_length
    type: duration
    label: Length of offered walkthrough call
    default: 15 min
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses that get the critical-risk alerts
    required: true
  requirements:
  - slot: paying_user_status
    kind: attribute
    meaning: A user's plan; a value that is not free or trial means a paying customer
  - slot: signup_date
    kind: attribute
    meaning: The date a user first signed up
  - slot: session_event
    kind: event
    meaning: A customer started a session in the product
  - slot: feature_usage_event
    kind: event
    meaning: A customer used a product feature
    properties:
    - name: feature_name
      type: string
      meaning: Name of the feature used
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled their subscription
  - slot: unsubscribe_event
    kind: event
    meaning: A customer unsubscribed from marketing email
  - slot: support_ticket
    kind: event
    meaning: A customer opened a support ticket
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - paying_user_status
    - session_event
    - feature_usage_event
    - support_ticket
    instruction: 'Build a computed attribute on users named "churn_risk_score", a number from 0 to 100, for users whose {paying_user_status}
      has a value that is not free or trial. It rises when their {session_event} count in the last 7 days is lower than their
      weekly average over the last 30 days, when the number of distinct {feature_usage_event.feature_name} values they used
      in the last 14 days is lower than in the 14 days before, and when they did {support_ticket} in the last 14 days. Bands:
      low 0-29, medium 30-59, high 60-79, critical 80-100.'
  - id: s2
    builds: segment
    uses:
    - s1
    - paying_user_status
    - signup_date
    - risk_threshold
    - new_user_grace_period
    - subscription_canceled_event
    - unsubscribe_event
    dependsOn:
    - s1
    instruction: 'Build a new segment of users named "Churn risk: intervene". A user is in it when their {paying_user_status}
      has a value that is not free or trial, the attribute from "Score churn risk daily" is {risk_threshold} or more, their
      {signup_date} is more than {new_user_grace_period} ago, and they did not do {subscription_canceled_event} or {unsubscribe_event}
      in the last 30 days.'
  - id: s3
    builds: email
    uses:
    - medium_tone
    instruction: Write an email for paying users whose product use is slipping. In a {medium_tone} tone it shows two or three
      features that customers who stay use most, each with one line on what it does for them, and a 'pick up where you left
      off' button that opens the product. Sent from the customer success team. No discount, no urgency.
  - id: s4
    builds: email
    uses:
    - walkthrough_length
    instruction: Write a short personal email for paying users at high churn risk, from their customer success manager. It
      says we noticed they have not used the product much lately, asks what would help, and offers a {walkthrough_length}
      walkthrough call with a button to book it. Plain, personal, no marketing images, no discount.
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - critical_response_window
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: 'Build an automation that runs every Monday at 09:00 on the segment from "Take everyone above the threshold".
      For each user it reads the attribute from "Score churn risk daily": from 30 to 59 it sends the email from "Write the
      medium-risk tips email"; 60 or more it sends the email from "Write the personal help email". For users at 80 or more
      it also emails an alert to {alert_recipients} naming the user, their score and their plan, asking for founder or CSM
      outreach within {critical_response_window}. A user gets at most one email from this automation every 14 days.'
---

# Tiered churn intervention

Slash command: /predictive-churn-tiered-intervention

## Step 1: Score churn risk daily

Build a computed attribute on users named "churn_risk_score", a number from 0 to 100, for users whose paying user status has a value that is not free or trial. It rises when their session event count in the last 7 days is lower than their weekly average over the last 30 days, when the number of distinct feature name values they used in the last 14 days is lower than in the 14 days before, and when they did support ticket in the last 14 days. Bands: low 0-29, medium 30-59, high 60-79, critical 80-100.

## Step 2: Take everyone above the threshold

Build a new segment of users named "Churn risk: intervene". A user is in it when their paying user status has a value that is not free or trial, the attribute from "Score churn risk daily" is 30 or more, their signup date is more than 14 d ago, and they did not do subscription canceled event or unsubscribe event in the last 30 days.

## Step 3: Write the medium-risk tips email

Write an email for paying users whose product use is slipping. In a helpful tone it shows two or three features that customers who stay use most, each with one line on what it does for them, and a 'pick up where you left off' button that opens the product. Sent from the customer success team. No discount, no urgency.

## Step 4: Write the personal help email

Write a short personal email for paying users at high churn risk, from their customer success manager. It says we noticed they have not used the product much lately, asks what would help, and offers a 15 min walkthrough call with a button to book it. Plain, personal, no marketing images, no discount.

## Step 5: Treat each band differently

Build an automation that runs every Monday at 09:00 on the segment from "Take everyone above the threshold". For each user it reads the attribute from "Score churn risk daily": from 30 to 59 it sends the email from "Write the medium-risk tips email"; 60 or more it sends the email from "Write the personal help email". For users at 80 or more it also emails an alert to the email addresses that get the critical-risk alerts naming the user, their score and their plan, asking for founder or CSM outreach within 4 h. A user gets at most one email from this automation every 14 days.
