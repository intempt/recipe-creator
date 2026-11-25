---
frontmatter_id: post-cancel-winback
slash_command: /post-cancel-winback
description: Goes back to people who cancelled at 30, 60 and 90 days with what has changed, a discount, and a free month, then stops.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Wins back cancelled customers with three emails at 30, 60 and 90 days after cancelling: what is new, a discount,
    and a free reactivation month.'
  parameters:
  - name: discount_percent
    type: number
    label: Winback discount percent
    default: 50
    required: false
  - name: discount_months
    type: number
    label: Number of months the discount applies
    default: 3
    required: false
  - name: free_trial_days
    type: number
    label: Free reactivation trial length (days)
    default: 30
    required: false
  - name: lookback_window
    type: duration
    label: Cancellation lookback window
    default: 120 d
    required: false
  - name: min_days_since_cancel
    type: duration
    label: Earliest days after cancel to start outreach
    default: 30 d
    required: false
  requirements:
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer's subscription was canceled
    properties:
    - name: cancel_reason
      type: string
      meaning: Reason given for cancelling, such as price, unused, wrong-fit or company-shutdown
      optional: false
    - name: plan
      type: string
      meaning: Plan they cancelled
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A customer started or restarted a subscription
  - slot: email_replied_event
    kind: event
    meaning: A customer replied to an email
  - slot: unsubscribed_event
    kind: event
    meaning: A customer unsubscribed from marketing emails
  - slot: no_marketing_request
    kind: attribute
    meaning: True when the customer asked for no marketing messages in the cancellation form
  - slot: prior_use_case
    kind: attribute
    meaning: The customer's prior use case, if known
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - subscription_canceled_event
    - subscription_started_event
    - no_marketing_request
    - unsubscribed_event
    - min_days_since_cancel
    - lookback_window
    instruction: Build a new segment of users named "Recently cancelled, recoverable". A user is in it when they did {subscription_canceled_event}
      between {min_days_since_cancel} and {lookback_window} ago with {subscription_canceled_event.cancel_reason} not equal
      to wrong-fit or company-shutdown, did not do {subscription_started_event} after it, did not do {unsubscribed_event}
      at any time, and their {no_marketing_request} is not true.
  - id: s2
    builds: email
    uses:
    - subscription_canceled_event
    instruction: 'Write a winback email for customers who cancelled about 30 days ago, subject "A lot has changed since you
      left: here''s what''s new". It leads with two or three product improvements, the first one matched to their {subscription_canceled_event.cancel_reason},
      and has one button to come back. Sent from the customer success team. No discount.'
  - id: s3
    builds: email
    uses:
    - discount_percent
    - discount_months
    - prior_use_case
    instruction: Write a winback email for customers who cancelled about 60 days ago, subject "Come back for {discount_months}
      months at {discount_percent}% off". It offers {discount_percent}% off for {discount_months} months, ties the value to
      their {prior_use_case} when it is set, and has one button to reactivate. Sent from the customer success team.
  - id: s4
    builds: email
    uses:
    - free_trial_days
    instruction: 'Write a final winback email for customers who cancelled about 90 days ago, subject "One last invitation".
      Softer and personal: it acknowledges they left for a reason and offers a free {free_trial_days}-day reactivation with
      no charge until they confirm, with one button. It says this is the last email about coming back.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - subscription_canceled_event
    - subscription_started_event
    - email_replied_event
    - unsubscribed_event
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: Build an automation triggered when a user enters the segment from "Find recent cancellations". It sends the
      email from "Write the what's-new email" 30 days after their {subscription_canceled_event}, the email from "Write the
      discount email" at 60 days, and the email from "Write the last invitation" at 90 days. It stops when the user does {subscription_started_event},
      {email_replied_event} or {unsubscribed_event}, and sends nothing after the third email.
---

# Win back after cancellation

Slash command: /post-cancel-winback

## Step 1: Find recent cancellations

Build a new segment of users named "Recently cancelled, recoverable". A user is in it when they did subscription canceled event between 30 d and 120 d ago with cancel reason not equal to wrong-fit or company-shutdown, did not do subscription started event after it, did not do unsubscribed event at any time, and their no marketing request is not true.

## Step 2: Write the what's-new email

Write a winback email for customers who cancelled about 30 days ago, subject "A lot has changed since you left: here's what's new". It leads with two or three product improvements, the first one matched to their cancel reason, and has one button to come back. Sent from the customer success team. No discount.

## Step 3: Write the discount email

Write a winback email for customers who cancelled about 60 days ago, subject "Come back for 3 months at 50% off". It offers 50% off for 3 months, ties the value to their prior use case when it is set, and has one button to reactivate. Sent from the customer success team.

## Step 4: Write the last invitation

Write a final winback email for customers who cancelled about 90 days ago, subject "One last invitation". Softer and personal: it acknowledges they left for a reason and offers a free 30-day reactivation with no charge until they confirm, with one button. It says this is the last email about coming back.

## Step 5: Send at 30, 60 and 90 days

Build an automation triggered when a user enters the segment from "Find recent cancellations". It sends the email from "Write the what's-new email" 30 days after their subscription canceled event, the email from "Write the discount email" at 60 days, and the email from "Write the last invitation" at 90 days. It stops when the user does subscription started event, email replied event or unsubscribed event, and sends nothing after the third email.
