---
frontmatter_id: aha-moment-activation
slash_command: /aha-moment-activation
description: Follows up right after someone hits the action that predicts retention with three emails, so the first win turns
  into a habit, and emails a weekly activation and retention digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends a three-touch email sequence after users reach their aha moment to turn a first win into a habit, plus a
    weekly digest of activation and retention.
  parameters:
  - name: aha_lookback
    type: duration
    label: How recent the aha moment must be
    default: 14 d
    required: false
  - name: touch_1_delay
    type: duration
    label: Wait before email 1
    default: 1 d
    required: false
  - name: touch_2_delay
    type: duration
    label: Wait before email 2
    default: 5 d
    required: false
  - name: touch_3_delay
    type: duration
    label: Wait before email 3
    default: 10 d
    required: false
  - name: email_tone
    type: enum
    label: Email tone
    default: warm_motivating
    required: false
    options:
    - warm_motivating
    - neutral
    - playful
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: aha_moment_event
    kind: event
    meaning: A user completed the product's aha-moment action that predicts retention (for example first message sent)
  - slot: signup_event
    kind: event
    meaning: A user signed up
  - slot: subscription_started_event
    kind: event
    meaning: A user started a paid subscription
  - slot: next_step_feature_event
    kind: event
    meaning: A user used the feature that naturally follows the aha action
  - slot: product_session_event
    kind: event
    meaning: A user started a session in the product
  - slot: email_sender
    kind: destination
    meaning: An email channel that can deliver the reinforcement emails
    channel: email
  - slot: product_deep_link_base
    kind: knowledge
    meaning: Product knowledge describing the next-step feature, its how-to and its in-app link
  steps:
  - id: s1
    builds: segment
    uses:
    - aha_moment_event
    - subscription_started_event
    - aha_lookback
    instruction: Build a new segment of users named "Recent Aha-Moment Achievers". A user is in it when they did {aha_moment_event}
      for the first time in the last {aha_lookback} and did not do {subscription_started_event} at any time.
  - id: s2
    builds: email
    uses:
    - s1
    - product_deep_link_base
    - email_tone
    dependsOn:
    - s1
    instruction: 'Write three emails for users in the segment from "Find people who just got value" in a {email_tone} tone.
      Email 1: celebrate the milestone as a meaningful first step and share one short story of a user who reached the same
      moment. Email 2: point to the next feature that complements the aha action, with a three-step how-to and one button
      to it, from {product_deep_link_base}; never a plan upsell. Email 3: "now that you have done this, here is how power
      users go further", with one habit to build. If the brand kit has no logo, use the brand name as a plain text header.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - next_step_feature_event
    - subscription_started_event
    - email_sender
    - touch_1_delay
    - touch_2_delay
    - touch_3_delay
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation triggered when a user enters the segment from "Find people who just got value". It sends
      the three emails from "Write three follow up emails" through {email_sender}: email 1 after {touch_1_delay}, email 2
      after {touch_2_delay}, email 3 after {touch_3_delay}. If the user already did {next_step_feature_event} when email 2
      is due, it skips email 2. It stops for a user who does {subscription_started_event}. Each user goes through it once.'
  - id: s4
    builds: automation
    uses:
    - s3
    - signup_event
    - aha_moment_event
    - product_session_event
    - digest_recipients
    dependsOn:
    - s3
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users and writes
      these figures: the share of users who did {signup_event} between 14 and 21 days ago who did {aha_moment_event} within
      14 days of signing up, against the week before; the median days from {signup_event} to the first {aha_moment_event};
      the open and click rate of each email sent by "Send on days 1, 5 and 10" in the last 7 days; the share of users who
      did {aha_moment_event} between 30 and 37 days ago who did {product_session_event} in the last 7 days, split by whether
      they got the emails, against users who did {signup_event} then and never did {aha_moment_event}. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Aha moment reinforcement

Slash command: /aha-moment-activation

## Step 1: Find people who just got value

Build a new segment of users named "Recent Aha-Moment Achievers". A user is in it when they did aha moment event for the first time in the last 14 d and did not do subscription started event at any time.

## Step 2: Write three follow up emails

Write three emails for users in the segment from "Find people who just got value" in a warm_motivating tone. Email 1: celebrate the milestone as a meaningful first step and share one short story of a user who reached the same moment. Email 2: point to the next feature that complements the aha action, with a three-step how-to and one button to it, from product deep link base; never a plan upsell. Email 3: "now that you have done this, here is how power users go further", with one habit to build. If the brand kit has no logo, use the brand name as a plain text header.

## Step 3: Send on days 1, 5 and 10

Build an automation triggered when a user enters the segment from "Find people who just got value". It sends the three emails from "Write three follow up emails" through email sender: email 1 after 1 d, email 2 after 5 d, email 3 after 10 d. If the user already did next step feature event when email 2 is due, it skips email 2. It stops for a user who does subscription started event. Each user goes through it once.

## Step 4: Track activation and retention

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users and writes these figures: the share of users who did signup event between 14 and 21 days ago who did aha moment event within 14 days of signing up, against the week before; the median days from signup event to the first aha moment event; the open and click rate of each email sent by "Send on days 1, 5 and 10" in the last 7 days; the share of users who did aha moment event between 30 and 37 days ago who did product session event in the last 7 days, split by whether they got the emails, against users who did signup event then and never did aha moment event. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
