---
frontmatter_id: vip-loyalty
slash_command: /vip-loyalty
description: Ranks your best customers into tiers, gives each tier something worth having, and tests which rewards actually keep them.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
  - travel-hospitality
portable:
  summary: Ranks best customers into silver, gold and platinum tiers, gives each tier VIP rewards, sends appreciation and
    tier-up messages, tests which rewards keep them, and tracks retention by tier.
  parameters:
  - name: silver_threshold
    type: number
    label: Silver tier threshold (value tier score)
    default: 2
    required: false
  - name: gold_threshold
    type: number
    label: Gold tier threshold (value tier score)
    default: 3
    required: false
  - name: platinum_threshold
    type: number
    label: Platinum tier threshold (value tier score)
    default: 4
    required: false
  - name: recency_window
    type: duration
    label: Recency window for value scoring
    default: 90 d
    required: false
  requirements:
  - slot: customer_ltv
    kind: attribute
    meaning: A customer's lifetime value in revenue
  - slot: purchase_event
    kind: event
    meaning: A customer completed an order
    properties:
    - name: order_value
      type: number
      meaning: Value of the order
      optional: false
    - name: order_date
      type: date
      meaning: Date the order was placed
      optional: false
  - slot: vip_segment
    kind: segment
    meaning: Customers eligible for the VIP programme
    creatable: true
    definition: users who did {purchase_event} in the last {recency_window} with a value tier at or above {silver_threshold}
  - slot: email_channel
    kind: destination
    meaning: An email channel to send VIP messages
    channel: email
  steps:
  - id: s1
    builds: attribute
    uses:
    - customer_ltv
    - purchase_event
    - recency_window
    instruction: Define an AI-derived customer value tier attribute that scores each customer using {customer_ltv}, purchase
      frequency from {purchase_event}, and recency within {recency_window}.
  - id: s2
    builds: segment
    uses:
    - s1
    - silver_threshold
    - gold_threshold
    - platinum_threshold
    instruction: Segment VIP customers into silver, gold and platinum tiers based on customer value tier using thresholds
      {silver_threshold}, {gold_threshold} and {platinum_threshold}.
  - id: s3
    builds: personalization
    uses:
    - s1
    - s2
    - vip_segment
    instruction: 'Configure VIP-only personalizations for each tier: early access, exclusive products and free shipping, applied
      to members of {vip_segment} by tier from "Set the silver and gold lines".'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - vip_segment
    - email_channel
    instruction: Build a VIP-specific journey through {email_channel} with appreciation touches and tier-up encouragement
      for members of {vip_segment}, using the tiers from "Set the silver and gold lines" and the offers from "Give each tier
      something".
  - id: s5
    builds: experiment
    uses:
    - s1
    - s2
    - s3
    - s4
    - vip_segment
    instruction: Add experiments comparing reward types (discount vs experience vs status) across the tiers from "Set the
      silver and gold lines" for members of {vip_segment}, using the journey from "Thank them, show the next tier".
  - id: s6
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - vip_segment
    instruction: Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate for {vip_segment},
      broken out by tier from "Set the silver and gold lines" and including results from "Test which reward works".
---

# VIP loyalty programme

Slash command: /vip-loyalty

## Step 1: Rank customers by value

Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency.

## Step 2: Set the silver and gold lines

Segment VIPs into tiers (silver, gold, platinum) by value tier with thresholds. Use the result of "Rank customers by value".

## Step 3: Give each tier something

Configure VIP-only personalizations: early access, exclusive products, free shipping. Use the result of "Rank customers by value", "Set the silver and gold lines".

## Step 4: Thank them, show the next tier

Build a VIP-specific journey with appreciation touches and tier-up encouragement. Use the result of "Rank customers by value", "Set the silver and gold lines", "Give each tier something".

## Step 5: Test which reward works

Add experiments comparing reward types (discount vs experience vs status). Use the result of "Rank customers by value", "Set the silver and gold lines", "Give each tier something", "Thank them, show the next tier".

## Step 6: Track retention by tier

Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate. Use the result of "Rank customers by value", "Set the silver and gold lines", "Give each tier something", "Thank them, show the next tier", "Test which reward works".
