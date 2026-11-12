---
frontmatter_id: win-back
slash_command: /win-back
description: Sorts lapsed customers by how long they have been gone and escalates the offer with the gap, from a gentle nudge to an exclusive deal.
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
  summary: Wins back lapsed customers by tiering them on days inactive and escalating from a gentle nudge to an exclusive
    deal, then measures and tests what brings them back.
  parameters:
  - name: tier1_min_days
    type: number
    label: 'Early-lapsed tier: minimum days inactive'
    default: 30
    required: false
  - name: tier1_max_days
    type: number
    label: 'Early-lapsed tier: maximum days inactive'
    default: 60
    required: false
  - name: tier2_max_days
    type: number
    label: 'Mid-lapsed tier: maximum days inactive'
    default: 120
    required: false
  - name: measurement_window
    type: duration
    label: Re-engagement measurement window after the journey
    default: 90 d
    required: false
  requirements:
  - slot: lapsed_users
    kind: segment
    meaning: Users who have been inactive for at least 30 days
  - slot: customer_last_activity
    kind: attribute
    meaning: The date of a customer's most recent activity or purchase
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
    builds: segment
    instruction: 'Split {lapsed_users} into three tiers by days since {customer_last_activity}: early-lapsed from {tier1_min_days}
      to {tier1_max_days} days inactive, mid-lapsed from {tier1_max_days} to {tier2_max_days} days inactive, and deep-lapsed
      beyond {tier2_max_days} days inactive.'
  - id: s2
    builds: email
    uses:
    - s1
    - brand_voice
    instruction: 'Write a designed HTML win-back email for each tier from "Sort lapsed users by the gap": a gentle nudge for
      early-lapsed users, a value reminder for mid-lapsed users, and an exclusive offer for deep-lapsed users. Keep the content
      aligned with {brand_voice}.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    instruction: Build a multi-branch journey that routes each tier from "Sort lapsed users by the gap" through its own sequence
      of touches using the emails from "Write content per tier", with incentives escalating by tier. Send through {email_channel}.
  - id: s4
    builds: report
    uses:
    - s1
    - s2
    - s3
    instruction: Create a retention report showing re-engagement rate for each tier from "Sort lapsed users by the gap" over
      {measurement_window} after the journey from "Escalate the offer by tier" starts, using the content from "Write content
      per tier".
  - id: s5
    builds: experiment
    uses:
    - s1
    - s2
    - s3
    - s4
    instruction: 'Add A/B variants to the journey from "Escalate the offer by tier" testing incentive type: discount versus
      free gift versus value-only messaging, measured against the results in "Measure who comes back" for each tier from "Sort
      lapsed users by the gap".'
---

# Lapsed customer win back

Slash command: /win-back

## Step 1: Sort lapsed users by the gap

Segment lapsed users into tiers: 30-60 days inactive, 60-120 days inactive, 120+ days inactive.

## Step 2: Write content per tier

This step builds a designed marketing email (HTML).
Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed. Use the result of "Sort lapsed users by the gap".

## Step 3: Escalate the offer by tier

Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. Use the result of "Sort lapsed users by the gap", "Write content per tier".

## Step 4: Measure who comes back

Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. Use the result of "Sort lapsed users by the gap", "Write content per tier", "Escalate the offer by tier".

## Step 5: Test what brings them back

Add A/B variants on incentive type (discount vs free gift vs value-only). Use the result of "Sort lapsed users by the gap", "Write content per tier", "Escalate the offer by tier", "Measure who comes back".
