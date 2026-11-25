---
frontmatter_id: milestone-driven-advocacy-asks
slash_command: /milestone-driven-advocacy-asks
description: Asks for a review, a referral or a case study by email just after a customer wins something, never asks the same
  person twice inside 90 days, and emails a weekly digest of asks and yeses.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a review, referral or case-study ask right after a customer win, never asking the same person twice within
    90 days, with a weekly digest of asks and yeses.
  parameters:
  - name: lookback_window
    type: duration
    label: How recent the win must be
    default: 7 d
    required: false
  - name: cooldown_window
    type: duration
    label: Minimum gap between two asks to the same person
    default: 90 d
    required: false
  - name: follow_up_delay
    type: duration
    label: Wait before the follow-up
    default: 7 d
    required: false
  - name: sentiment_threshold
    type: number
    label: Sentiment score that counts as positive feedback
    default: 8
    required: false
  - name: sender_role
    type: enum
    label: Who the asks come from
    default: csm
    required: false
    options:
    - csm
    - account_manager
    - founder
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: first_value_event
    kind: event
    meaning: A customer reached its first-value or key activation milestone
  - slot: expansion_event
    kind: event
    meaning: A customer upgraded or expanded its plan
  - slot: renewal_event
    kind: event
    meaning: A customer renewed for another term
  - slot: positive_sentiment_event
    kind: event
    meaning: A customer gave feedback to support with a sentiment score
    properties:
    - name: sentiment_score
      type: number
      meaning: Sentiment score from 0 to 10
      optional: false
  - slot: friction_signal
    kind: event
    meaning: A customer raised a complaint or an open friction issue
  - slot: advocacy_action_event
    kind: event
    meaning: A customer completed an advocacy action such as a review, a referral or agreeing to a case study
    properties:
    - name: action_type
      type: string
      meaning: review, referral or case_study
      optional: false
  - slot: sending_identity
    kind: integration
    meaning: An email sending connection that can send from a named person
    channel: email
  - slot: review_platform_links
    kind: knowledge
    meaning: Approved review site links
    optional: true
  - slot: referral_program
    kind: knowledge
    meaning: Referral program terms and rewards
    optional: true
  - slot: product_brand
    kind: brand
    meaning: The product name and tone for customer-facing messages
  steps:
  - id: s1
    builds: attribute
    uses:
    - first_value_event
    - expansion_event
    - renewal_event
    - positive_sentiment_event
    - friction_signal
    - lookback_window
    - sentiment_threshold
    instruction: 'Create a computed user attribute named "advocacy_ask", refreshed daily. It is empty when the user did {friction_signal}
      in the last 30 days. Otherwise the first rule that matches sets it: "case_study" when they did {renewal_event} in the
      last {lookback_window}; "referral" when they did {expansion_event} in the last {lookback_window}; "review" when they
      did {first_value_event} in the last {lookback_window}, or {positive_sentiment_event} with {positive_sentiment_event.sentiment_score}
      of {sentiment_threshold} or more in the last {lookback_window}. Empty otherwise.'
  - id: s2
    builds: segment
    uses:
    - s1
    dependsOn:
    - s1
    instruction: Build a new segment of users named "Ready for an Advocacy Ask". A user is in it when their advocacy_ask attribute
      from "Spot the goodwill moments" has a value.
  - id: s3
    builds: email
    uses:
    - s2
    - sender_role
    - review_platform_links
    - referral_program
    - product_brand
    dependsOn:
    - s2
    instruction: 'Write four emails for users in the segment from "Find who is ready to be asked", sent from a named {sender_role},
      peer-respectful and never transactional, in the voice of {product_brand}. review: congratulate them on the milestone
      and ask for a 3-minute public review, with one button to the review site from {review_platform_links}. referral: thank
      them for growing with {product_brand} and ask whether they know someone who would benefit, with the reward from {referral_program}.
      case_study: thank them for renewing, name what they achieved and ask whether they would share it as a case study, saying
      the team does all the writing. follow-up: one short line repeating the ask with its single next step. If the brand kit
      has no logo, use the brand name as a plain text header.'
  - id: s4
    builds: automation
    uses:
    - s2
    - s3
    - sending_identity
    - advocacy_action_event
    - cooldown_window
    - follow_up_delay
    dependsOn:
    - s2
    - s3
    instruction: Build an automation triggered when a user enters the segment from "Find who is ready to be asked". It skips
      users who got any ask from it in the last {cooldown_window}. It sends the email from "Write one ask per moment" matching
      the user's advocacy_ask attribute through {sending_identity}. After {follow_up_delay}, if the user opened it and did
      not do {advocacy_action_event}, it sends the follow-up email from the same step. Nothing else is sent.
  - id: s5
    builds: automation
    uses:
    - s4
    - advocacy_action_event
    - digest_recipients
    dependsOn:
    - s4
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the asks sent by
      "Ask once, follow up once" and writes these figures for the last 7 days and the last 90 days: asks sent by advocacy_ask
      type; open and click rate per type; the share of asked users who did {advocacy_action_event} within 14 days, by {advocacy_action_event.action_type};
      the users with 3 or more {advocacy_action_event} at any time, by name. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Advocacy asks at the right moment

Slash command: /milestone-driven-advocacy-asks

## Step 1: Spot the goodwill moments

Create a computed user attribute named "advocacy_ask", refreshed daily. It is empty when the user did friction signal in the last 30 days. Otherwise the first rule that matches sets it: "case_study" when they did renewal event in the last 7 d; "referral" when they did expansion event in the last 7 d; "review" when they did first value event in the last 7 d, or positive sentiment event with sentiment score of 8 or more in the last 7 d. Empty otherwise.

## Step 2: Find who is ready to be asked

Build a new segment of users named "Ready for an Advocacy Ask". A user is in it when their advocacy_ask attribute from "Spot the goodwill moments" has a value.

## Step 3: Write one ask per moment

Write four emails for users in the segment from "Find who is ready to be asked", sent from a named csm, peer-respectful and never transactional, in the voice of product brand. review: congratulate them on the milestone and ask for a 3-minute public review, with one button to the review site from review platform links. referral: thank them for growing with product brand and ask whether they know someone who would benefit, with the reward from referral program. case_study: thank them for renewing, name what they achieved and ask whether they would share it as a case study, saying the team does all the writing. follow-up: one short line repeating the ask with its single next step. If the brand kit has no logo, use the brand name as a plain text header.

## Step 4: Ask once, follow up once

Build an automation triggered when a user enters the segment from "Find who is ready to be asked". It skips users who got any ask from it in the last 90 d. It sends the email from "Write one ask per moment" matching the user's advocacy_ask attribute through sending identity. After 7 d, if the user opened it and did not do advocacy action event, it sends the follow-up email from the same step. Nothing else is sent.

## Step 5: See which asks get a yes

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the asks sent by "Ask once, follow up once" and writes these figures for the last 7 days and the last 90 days: asks sent by advocacy_ask type; open and click rate per type; the share of asked users who did advocacy action event within 14 days, by action type; the users with 3 or more advocacy action event at any time, by name. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
