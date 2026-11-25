---
frontmatter_id: pre-cancellation-save
slash_command: /pre-cancellation-save
description: Catches paying customers who open the cancel flow but have not finished it, and answers the reason they gave
  with a discount, a pause or a call, alerting the team on high-value accounts.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: 'Catches paying customers who start but do not finish cancelling and sends one save email matched to their reason:
    a discount, a pause, or a call.'
  parameters:
  - name: cancel_window
    type: duration
    label: Lookback window for cancel-flow activity
    default: 14 d
    required: false
  - name: save_cooldown
    type: duration
    label: Cooldown since last save offer
    default: 90 d
    required: false
  - name: retention_discount_percent
    type: number
    label: Retention discount percent (price reason)
    default: 20
    required: false
  - name: retention_discount_months
    type: number
    label: Retention discount duration in months
    default: 3
    required: false
  - name: max_pause_days
    type: number
    label: Maximum pause length in days
    default: 90
    required: false
  - name: high_value_arr
    type: number
    label: Annual revenue at or above which the team is alerted
    default: 10000
    required: false
  - name: brand_tone
    type: enum
    label: Email tone
    default: warm
    required: false
    options:
    - warm
    - direct
    - formal
  - name: alert_recipients
    type: string
    label: Email addresses of the customer success team who get high-value alerts
    required: true
  requirements:
  - slot: cancel_flow_visit
    kind: event
    meaning: A customer visited the cancel or downgrade page
  - slot: cancel_reason_submitted
    kind: event
    meaning: A customer submitted a cancel reason in the cancel flow without confirming cancellation
    properties:
    - name: reason
      type: string
      meaning: 'Stated reason: price, unused, competitor, feature-gap, pause-needed or other'
      optional: false
  - slot: subscription_canceled
    kind: event
    meaning: A customer's subscription was canceled
  - slot: save_offer_accepted
    kind: event
    meaning: A customer accepted a cancel-save offer
  - slot: plan
    kind: attribute
    meaning: The user's plan; a value that is not free or trial means a paying customer
  - slot: arr_value
    kind: attribute
    meaning: Annual recurring revenue of the customer
  steps:
  - id: s1
    builds: segment
    uses:
    - cancel_flow_visit
    - cancel_reason_submitted
    - subscription_canceled
    - plan
    - cancel_window
    instruction: Build a new segment of users named "Cancel intent, not cancelled". A user is in it when their {plan} has
      a value that is not free or trial, they did {cancel_flow_visit} or {cancel_reason_submitted} in the last {cancel_window},
      and they did not do {subscription_canceled} in the last {cancel_window}.
  - id: s2
    builds: email
    uses:
    - retention_discount_percent
    - retention_discount_months
    - brand_tone
    instruction: Write a save email in a {brand_tone} tone for paying customers who said price is why they want to cancel.
      It offers {retention_discount_percent}% off for {retention_discount_months} months, or a move to a lighter plan, each
      with its own button. Sent from the customer success team.
  - id: s3
    builds: email
    uses:
    - max_pause_days
    - brand_tone
    instruction: Write a save email in a {brand_tone} tone for paying customers who said they are not using the product or
      need a break. It offers a one-click pause of up to {max_pause_days} days that keeps all their data, and a free 1:1 onboarding
      call, each with its own button. Sent from the customer success team.
  - id: s4
    builds: email
    uses:
    - brand_tone
    instruction: Write a save email in a {brand_tone} tone for paying customers who are cancelling for a competitor, a missing
      feature or another reason. It asks what would have made them stay and offers a 1:1 call with the product team about
      what is missing, with one button to book it. Sent from the customer success team.
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - cancel_reason_submitted
    - subscription_canceled
    - save_offer_accepted
    - arr_value
    - high_value_arr
    - save_cooldown
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: 'Build an automation triggered when a user enters the segment from "Find who is halfway out", at most once
      per {save_cooldown}. Within 1 hour it sends one email by their latest {cancel_reason_submitted.reason}: price gets the
      email from "Write the price offer"; unused or pause-needed gets the email from "Write the pause offer"; any other reason
      or none gets the email from "Write the talk-to-us offer". When their {arr_value} is {high_value_arr} or more, it also
      emails an alert to {alert_recipients} with the user, their reason and {arr_value}. It stops on {save_offer_accepted}
      or {subscription_canceled}.'
---

# Save them before they cancel

Slash command: /pre-cancellation-save

## Step 1: Find who is halfway out

Build a new segment of users named "Cancel intent, not cancelled". A user is in it when their plan has a value that is not free or trial, they did cancel flow visit or cancel reason submitted in the last 14 d, and they did not do subscription canceled in the last 14 d.

## Step 2: Write the price offer

Write a save email in a warm tone for paying customers who said price is why they want to cancel. It offers 20% off for 3 months, or a move to a lighter plan, each with its own button. Sent from the customer success team.

## Step 3: Write the pause offer

Write a save email in a warm tone for paying customers who said they are not using the product or need a break. It offers a one-click pause of up to 90 days that keeps all their data, and a free 1:1 onboarding call, each with its own button. Sent from the customer success team.

## Step 4: Write the talk-to-us offer

Write a save email in a warm tone for paying customers who are cancelling for a competitor, a missing feature or another reason. It asks what would have made them stay and offers a 1:1 call with the product team about what is missing, with one button to book it. Sent from the customer success team.

## Step 5: Make one matched offer

Build an automation triggered when a user enters the segment from "Find who is halfway out", at most once per 90 d. Within 1 hour it sends one email by their latest reason: price gets the email from "Write the price offer"; unused or pause-needed gets the email from "Write the pause offer"; any other reason or none gets the email from "Write the talk-to-us offer". When their arr value is 10000 or more, it also emails an alert to the email addresses of the customer success team who get high-value alerts with the user, their reason and arr value. It stops on save offer accepted or subscription canceled.
