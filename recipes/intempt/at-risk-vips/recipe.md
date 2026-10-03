---
id: at-risk-vips
title: At-risk VIP customers
slash_command: /at-risk-vips
group: Segments
owner: intempt
summary: Your biggest spenders who have gone quiet for about six weeks, so you can reach out personally
  before they drift away for good.
description: >-
  High-lifetime-value customers showing recency decay: Klaviyo's Needs Attention cohort. Distinct from
  generic churn risk.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - ecommerce
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
steps:
  - id: s1
    title: Build the at-risk VIP list
    summary: >-
      Customers with lifetime value of 1,000 or more and 2 or more orders, whose last activity was 45
      to 90 days ago and who have not ordered in 45 days.
    builds: segment
    description: |-
      Create a segment called "At-Risk VIPs".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: lifetime_value >= 1000
      - AND Attribute: days_since_last_activity is between 45 and 90
      - AND Event: order_created occurred >= 2 times (all time)
      - AND Event: order_created occurred 0 times in last 45 days
      Description: High-LTV customers who are going quiet: the Klaviyo "Needs Attention" RFM cohort. Most expensive cohort to lose; strongest ROI for personalized win-back outreach (CSM-style email from a real person, not a discount blast).
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# At-risk VIP customers

Your biggest spenders who have gone quiet for about six weeks, so you can reach out personally before they drift away for good.

## Steps

1. **Build the at-risk VIP list** (builds segment)

   Customers with lifetime value of 1,000 or more and 2 or more orders, whose last activity was 45 to 90 days ago and who have not ordered in 45 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
