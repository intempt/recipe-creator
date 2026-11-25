---
frontmatter_id: customer-progress-business-case
slash_command: /customer-progress-business-case
description: Totals up each paying account's quarter of product use and emails the account admin a progress summary they can
  hand to their own boss, with the same snapshot shown in the app.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends each paying account's admin a quarterly email summary of the value they got from the product, shows the same
    snapshot in the app, and follows up with a review offer.
  parameters:
  - name: quarter_lookback_days
    type: duration
    label: Length of the quarter summarized
    default: 90 d
    required: false
  - name: min_usage_events
    type: number
    label: Usage events in the quarter an account needs to get the summary
    default: 50
    required: false
  - name: churn_risk_threshold
    type: number
    label: Churn risk score at or above which an account is left out
    default: 60
    required: false
  - name: followup_delay
    type: duration
    label: Wait before the follow-up email
    default: 14 d
    required: false
  - name: sender_name
    type: string
    label: Name the emails are sent from
    required: true
  requirements:
  - slot: plan_attribute
    kind: attribute
    meaning: The account's current plan name
  - slot: account_age_days
    kind: attribute
    meaning: Number of days since the account was created
  - slot: churn_risk_score
    kind: attribute
    meaning: Account churn risk score from 0 to 100
  - slot: account_admin_contact
    kind: attribute
    meaning: The email address of the account's admin or champion, who receives account-level emails
  - slot: product_usage_event
    kind: event
    meaning: A customer used the product (any tracked usage action)
    properties:
    - name: feature_name
      type: string
      meaning: The feature used
      optional: false
  - slot: email_channel
    kind: integration
    meaning: An email sending integration used to deliver account emails
    channel: email
  - slot: product_brand
    kind: brand
    meaning: The product name and voice used in the emails
  steps:
  - id: s1
    builds: attribute
    uses:
    - product_usage_event
    - quarter_lookback_days
    instruction: 'Create a computed account attribute named "quarterly_progress_snapshot", refreshed on the first day of each
      quarter. Its value is a short text built from the account''s own data: the number of {product_usage_event} events by
      its users in the last {quarter_lookback_days} and the change against the {quarter_lookback_days} before; the number
      of active users in both windows; the number of different {product_usage_event.feature_name} values used and any feature
      used for the first time; the number of users who did their first {product_usage_event} in the last {quarter_lookback_days}.
      Each figure has its change against the prior quarter in percent.'
  - id: s2
    builds: segment
    uses:
    - plan_attribute
    - account_age_days
    - churn_risk_score
    - product_usage_event
    - quarter_lookback_days
    - min_usage_events
    - churn_risk_threshold
    instruction: 'Build a new segment of accounts named "Quarterly Progress Recipients". An account is in it when all of these
      are true: its {plan_attribute} attribute has a value and is not "free" or "trial"; its {account_age_days} attribute
      is 90 or more; the users in the account together did {product_usage_event} {min_usage_events} or more times in the last
      {quarter_lookback_days}; its {churn_risk_score} attribute is below {churn_risk_threshold}.'
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - sender_name
    - product_brand
    dependsOn:
    - s1
    - s2
    instruction: 'Write two emails for the admins of accounts in the segment from "Pick who should get it", sent from {sender_name},
      in the voice of {product_brand}. Email 1, the progress summary: subject "Your quarter with" and the product name; the
      body shows the account''s quarterly_progress_snapshot attribute from "Total up the quarter" with the largest gain as
      the headline and the other figures as three or four lines with their change; it closes by saying the email can be forwarded
      to their manager as is. Celebratory but factual, no marketing language, no figure that is not in the snapshot. Email
      2, the follow-up: offers a 30-minute review of the quarter with their account manager, with one reply call to action.
      If the brand kit has no logo, use the brand name as a plain text header.'
  - id: s4
    builds: personalization
    uses:
    - s1
    - s2
    dependsOn:
    - s1
    - s2
    instruction: Create an in-app personalization named "Your quarter snapshot" on the admin home page for admin users of
      accounts in the segment from "Pick who should get it". It shows the account's quarterly_progress_snapshot attribute
      from "Total up the quarter" as a card with the headline figure and the supporting lines. Show it for 30 days after the
      first day of each quarter; devices any; display frequency always.
  - id: s5
    builds: automation
    uses:
    - s2
    - s3
    - account_admin_contact
    - email_channel
    - followup_delay
    dependsOn:
    - s2
    - s3
    instruction: Build an automation that runs on the 4th day of each quarter at 09:00 on a schedule. For each account in
      the segment from "Pick who should get it" it sends email 1 from "Write the quarter in numbers" through {email_channel}
      to the address in the account's {account_admin_contact} attribute. After {followup_delay}, if that email was opened,
      it sends email 2 from the same step to the same address. Each account gets each email at most once per quarter.
---

# Quarterly customer progress report

Slash command: /customer-progress-business-case

## Step 1: Total up the quarter

Create a computed account attribute named "quarterly_progress_snapshot", refreshed on the first day of each quarter. Its value is a short text built from the account's own data: the number of product usage event events by its users in the last 90 d and the change against the 90 d before; the number of active users in both windows; the number of different feature name values used and any feature used for the first time; the number of users who did their first product usage event in the last 90 d. Each figure has its change against the prior quarter in percent.

## Step 2: Pick who should get it

Build a new segment of accounts named "Quarterly Progress Recipients". An account is in it when all of these are true: its plan attribute attribute has a value and is not "free" or "trial"; its account age days attribute is 90 or more; the users in the account together did product usage event 50 or more times in the last 90 d; its churn risk score attribute is below 60.

## Step 3: Write the quarter in numbers

Write two emails for the admins of accounts in the segment from "Pick who should get it", sent from the name the emails are sent from, in the voice of product brand. Email 1, the progress summary: subject "Your quarter with" and the product name; the body shows the account's quarterly_progress_snapshot attribute from "Total up the quarter" with the largest gain as the headline and the other figures as three or four lines with their change; it closes by saying the email can be forwarded to their manager as is. Celebratory but factual, no marketing language, no figure that is not in the snapshot. Email 2, the follow-up: offers a 30-minute review of the quarter with their account manager, with one reply call to action. If the brand kit has no logo, use the brand name as a plain text header.

## Step 4: Show it in the app too

Create an in-app personalization named "Your quarter snapshot" on the admin home page for admin users of accounts in the segment from "Pick who should get it". It shows the account's quarterly_progress_snapshot attribute from "Total up the quarter" as a card with the headline figure and the supporting lines. Show it for 30 days after the first day of each quarter; devices any; display frequency always.

## Step 5: Send three days after close

Build an automation that runs on the 4th day of each quarter at 09:00 on a schedule. For each account in the segment from "Pick who should get it" it sends email 1 from "Write the quarter in numbers" through email channel to the address in the account's account admin contact attribute. After 14 d, if that email was opened, it sends email 2 from the same step to the same address. Each account gets each email at most once per quarter.
