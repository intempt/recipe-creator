---
frontmatter_id: welcome-series
slash_command: /welcome-series
description: Introduces your brand to new subscribers over their first week in four emails, tests the subject lines and the
  opening offer, and emails a weekly digest of first purchases.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Welcomes new subscribers with four emails over their first week, tests subject lines and the opening offer, and
    emails a weekly first-purchase digest.
  parameters:
  - name: subscription_window
    type: duration
    label: How recently a subscriber joined
    default: 7 d
    required: false
  - name: welcome_offer_percent
    type: number
    label: Discount in the opening offer (%)
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: new_subscriber_event
    kind: event
    meaning: A customer subscribed to the mailing list
  - slot: purchase_event
    kind: event
    meaning: A customer completed an order
    properties:
    - name: order_value
      type: number
      meaning: Value of the order
      optional: false
  - slot: email_channel
    kind: integration
    meaning: An email sending integration for delivering marketing emails
    channel: email
  - slot: brand_voice
    kind: brand
    meaning: The brand's name, voice and value proposition used in the emails
  steps:
  - id: s1
    builds: segment
    uses:
    - new_subscriber_event
    - purchase_event
    - subscription_window
    instruction: Build a new segment of users named "New Subscribers". A user is in it when they did {new_subscriber_event}
      in the last {subscription_window} and did not do {purchase_event} at any time.
  - id: s2
    builds: email
    uses:
    - s1
    - brand_voice
    - welcome_offer_percent
    dependsOn:
    - s1
    instruction: 'Write a four-email welcome sequence for the users in the segment from "Find new subscribers", in the voice
      of {brand_voice}. Email 1 (on subscribe): welcome them and say who the brand is and what it stands for. Email 2 (day
      1): the products and the main value they get. Email 3 (day 3): customer stories and best sellers. Email 4 (day 7): an
      opening offer of {welcome_offer_percent}% off the first order. Each email has one call to action that links to the store.
      If the brand kit has no logo, use the brand name as a plain text header.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - new_subscriber_event
    - purchase_event
    - email_channel
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation triggered when a user does {new_subscriber_event}. It sends the four emails from "Write
      the four emails" through {email_channel}: email 1 at once, email 2 after 1 day, email 3 after 3 days and email 4 after
      7 days. Before each send it checks whether the user did {purchase_event} since subscribing; if they did, the automation
      stops for that user.'
  - id: s4
    builds: experiment
    uses:
    - s1
    - s2
    - s3
    - purchase_event
    - welcome_offer_percent
    dependsOn:
    - s1
    - s2
    - s3
    instruction: 'Create an experiment on the automation from "Send across the first week" for users in the segment from "Find
      new subscribers". Variant A sends the emails from "Write the four emails" as written. Variant B uses a question-style
      subject line on each email and leaves out the {welcome_offer_percent}% offer in email 4. Split users 50/50 at random.
      Primary metric: share of users who did {purchase_event} within 14 days of subscribing. Secondary metrics: open rate
      and click rate per email. Run for 30 days.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s3
    - new_subscriber_event
    - purchase_event
    - digest_recipients
    dependsOn:
    - s1
    - s3
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {new_subscriber_event}
      in the last 7 days and in the 7 days before that, and writes these figures: new subscribers in each window; open rate
      and click rate of each email sent by "Send across the first week" in the last 7 days; the share of new subscribers who
      did {purchase_event} within 7 days of subscribing; the median days from subscribing to the first {purchase_event}; the
      total {purchase_event.order_value} of those first orders. Then it emails these figures as plain-text lines, each with
      its window, to {digest_recipients}. Nothing else is sent.'
---

# Welcome series

Slash command: /welcome-series

## Step 1: Find new subscribers

Build a new segment of users named "New Subscribers". A user is in it when they did new subscriber event in the last 7 d and did not do purchase event at any time.

## Step 2: Write the four emails

Write a four-email welcome sequence for the users in the segment from "Find new subscribers", in the voice of brand voice. Email 1 (on subscribe): welcome them and say who the brand is and what it stands for. Email 2 (day 1): the products and the main value they get. Email 3 (day 3): customer stories and best sellers. Email 4 (day 7): an opening offer of 10% off the first order. Each email has one call to action that links to the store. If the brand kit has no logo, use the brand name as a plain text header.

## Step 3: Send across the first week

Build an automation triggered when a user does new subscriber event. It sends the four emails from "Write the four emails" through email channel: email 1 at once, email 2 after 1 day, email 3 after 3 days and email 4 after 7 days. Before each send it checks whether the user did purchase event since subscribing; if they did, the automation stops for that user.

## Step 4: Test subject lines and offer

Create an experiment on the automation from "Send across the first week" for users in the segment from "Find new subscribers". Variant A sends the emails from "Write the four emails" as written. Variant B uses a question-style subject line on each email and leaves out the 10% offer in email 4. Split users 50/50 at random. Primary metric: share of users who did purchase event within 14 days of subscribing. Secondary metrics: open rate and click rate per email. Run for 30 days.

## Step 5: Email the weekly first-purchase digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did new subscriber event in the last 7 days and in the 7 days before that, and writes these figures: new subscribers in each window; open rate and click rate of each email sent by "Send across the first week" in the last 7 days; the share of new subscribers who did purchase event within 7 days of subscribing; the median days from subscribing to the first purchase event; the total order value of those first orders. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
