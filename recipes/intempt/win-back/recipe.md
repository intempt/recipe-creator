---
frontmatter_id: win-back
slash_command: /win-back
description: Sorts lapsed customers by how long they have been gone, emails each tier from a gentle nudge to an exclusive
  offer, emails a weekly digest of who comes back and tests which incentive works.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
  - saas-b2b-tech
portable:
  summary: Wins back lapsed customers with emails that escalate from a gentle nudge to an exclusive offer by days inactive,
    a weekly comeback digest and an incentive test.
  parameters:
  - name: tier1_min_days
    type: number
    label: Days inactive where early-lapsed starts
    default: 30
    required: false
  - name: tier1_max_days
    type: number
    label: Days inactive where mid-lapsed starts
    default: 60
    required: false
  - name: tier2_max_days
    type: number
    label: Days inactive where deep-lapsed starts
    default: 120
    required: false
  - name: offer_percent
    type: number
    label: Discount in the deep-lapsed offer (%)
    default: 15
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: customer_last_activity
    kind: attribute
    meaning: The date of a customer's most recent activity or purchase
  - slot: purchase_event
    kind: event
    meaning: A customer completed an order
  - slot: email_channel
    kind: destination
    meaning: An email destination for sending win-back messages
    channel: email
  - slot: brand_voice
    kind: brand
    meaning: The brand's tone and identity guidelines for customer messages
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - customer_last_activity
    - tier1_min_days
    - tier1_max_days
    - tier2_max_days
    instruction: Create a computed user attribute named "lapse_tier", refreshed daily, from the days since the user's {customer_last_activity}
      date. The value is "early" from {tier1_min_days} up to {tier1_max_days} days, "mid" from {tier1_max_days} up to {tier2_max_days}
      days, "deep" at {tier2_max_days} days or more, and empty under {tier1_min_days} days.
  - id: s2
    builds: email
    uses:
    - s1
    - brand_voice
    - offer_percent
    dependsOn:
    - s1
    instruction: 'Write three win-back emails for users by their lapse_tier attribute from "Sort lapsed users by the gap",
      in the voice of {brand_voice}. early: a gentle "we miss you" with what is new since their last visit. mid: a value reminder
      of why customers come back, with best sellers. deep: an exclusive offer of {offer_percent}% off their next order. Each
      has one call to action to the store. If the brand kit has no logo, use the brand name as a plain text header.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - purchase_event
    - email_channel
    dependsOn:
    - s1
    - s2
    instruction: Build an automation triggered when a user's lapse_tier attribute from "Sort lapsed users by the gap" changes
      to early, mid or deep. It sends the matching email from "Write content per tier" through {email_channel} at once. It
      skips users who did {purchase_event} in the last 7 days. Each user gets each tier's email at most once in 180 days.
  - id: s4
    builds: automation
    uses:
    - s1
    - s3
    - purchase_event
    - digest_recipients
    dependsOn:
    - s1
    - s3
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users emailed
      by "Escalate the offer by tier" and writes these figures by lapse_tier from "Sort lapsed users by the gap": users emailed
      in the last 7 days; open and click rate of those emails; the share of users emailed in the last 30 days who did {purchase_event}
      within 30 days of the email; the same share for the 30 days before. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
  - id: s5
    builds: experiment
    uses:
    - s1
    - s3
    - purchase_event
    - offer_percent
    dependsOn:
    - s1
    - s3
    instruction: 'Create an experiment on the deep-tier email sent by "Escalate the offer by tier" for users whose lapse_tier
      from "Sort lapsed users by the gap" is deep. Variant A: {offer_percent}% off the next order. Variant B: a free gift
      with the next order. Variant C: value-only message with no incentive. Split users evenly at random. Primary metric:
      share who do {purchase_event} within 30 days of the email. Run for 60 days.'
---

# Lapsed customer win back

Slash command: /win-back

## Step 1: Sort lapsed users by the gap

Create a computed user attribute named "lapse_tier", refreshed daily, from the days since the user's customer last activity date. The value is "early" from 30 up to 60 days, "mid" from 60 up to 120 days, "deep" at 120 days or more, and empty under 30 days.

## Step 2: Write content per tier

Write three win-back emails for users by their lapse_tier attribute from "Sort lapsed users by the gap", in the voice of brand voice. early: a gentle "we miss you" with what is new since their last visit. mid: a value reminder of why customers come back, with best sellers. deep: an exclusive offer of 15% off their next order. Each has one call to action to the store. If the brand kit has no logo, use the brand name as a plain text header.

## Step 3: Escalate the offer by tier

Build an automation triggered when a user's lapse_tier attribute from "Sort lapsed users by the gap" changes to early, mid or deep. It sends the matching email from "Write content per tier" through email channel at once. It skips users who did purchase event in the last 7 days. Each user gets each tier's email at most once in 180 days.

## Step 4: Measure who comes back

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users emailed by "Escalate the offer by tier" and writes these figures by lapse_tier from "Sort lapsed users by the gap": users emailed in the last 7 days; open and click rate of those emails; the share of users emailed in the last 30 days who did purchase event within 30 days of the email; the same share for the 30 days before. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.

## Step 5: Test what brings them back

Create an experiment on the deep-tier email sent by "Escalate the offer by tier" for users whose lapse_tier from "Sort lapsed users by the gap" is deep. Variant A: 15% off the next order. Variant B: a free gift with the next order. Variant C: value-only message with no incentive. Split users evenly at random. Primary metric: share who do purchase event within 30 days of the email. Run for 60 days.
