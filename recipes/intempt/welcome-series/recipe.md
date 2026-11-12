---
frontmatter_id: welcome-series
slash_command: /welcome-series
description: Introduces your brand to new subscribers over their first week in four emails, and tests the subject lines and the opening offer.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Introduces your brand to new subscribers through a four-email welcome sequence over their first week, with tests
    on subject lines and the opening offer.
  parameters:
  - name: subscription_window
    type: duration
    label: Subscription window for new subscribers
    default: 30 d
    required: false
  - name: offer_test_enabled
    type: boolean
    label: Test presence of welcome offer
    default: true
    required: false
  requirements:
  - slot: new_subscriber_event
    kind: event
    meaning: A customer subscribed to the mailing list
  - slot: welcome_email_sent_event
    kind: event
    meaning: A customer received a welcome email
    optional: true
  - slot: purchase_event
    kind: event
    meaning: A customer completed an order
  - slot: email_channel
    kind: integration
    meaning: An email sending integration for delivering marketing emails
    channel: email
  - slot: brand_voice
    kind: knowledge
    meaning: Brand voice and value proposition guidelines describing the brand, product and tone
  - slot: new_subscribers
    kind: segment
    meaning: New subscribers in the last 30 days who have not received a welcome email
    creatable: true
    definition: users who subscribed within the last {subscription_window} and have not received a welcome email yet
  steps:
  - id: s1
    builds: segment
    uses:
    - new_subscriber_event
    - welcome_email_sent_event
    - subscription_window
    instruction: Identify users who subscribed within the last {subscription_window} and have not received a welcome email
      yet.
  - id: s2
    builds: email
    uses:
    - brand_voice
    - s1
    instruction: Generate a 4-email welcome sequence introducing the brand, product, and value props using {brand_voice}.
      Use the result of "Find new subscribers".
  - id: s3
    builds: automation
    uses:
    - new_subscribers
    - email_channel
    - s2
    instruction: Build a 4-touch welcome journey for {new_subscribers} sending the emails through {email_channel} at 0 hr,
      1 day, 3 days, and 7 days after subscription. Use the result of "Write the four emails".
  - id: s4
    builds: experiment
    uses:
    - new_subscribers
    - s2
    - s3
    - offer_test_enabled
    instruction: Add A/B variants on subject lines and welcome offer presence{offer_test_enabled} to the welcome journey.
      Use the result of "Find new subscribers", "Write the four emails", and "Send across the first week".
  - id: s5
    builds: dashboard
    uses:
    - purchase_event
    - new_subscribers
    - s2
    - s3
    - s4
    instruction: Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. Use the result of "Find new subscribers", "Write the four emails", "Send across the first week", and
      "Test subject lines and offer".
---

# Welcome series

Slash command: /welcome-series

## Step 1: Find new subscribers

This step builds a segment.
Identify users who subscribed within the last 30 days and have not received a welcome email yet.

## Step 2: Write the four emails

Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. Use the result of "Find new subscribers".

## Step 3: Send across the first week

Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. Use the result of "Find new subscribers", "Write the four emails".

## Step 4: Test subject lines and offer

Add A/B variants on subject lines and welcome offer presence. Use the result of "Find new subscribers", "Write the four emails", "Send across the first week".

## Step 5: Track the first purchase

Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. Use the result of "Find new subscribers", "Write the four emails", "Send across the first week", "Test subject lines and offer".
