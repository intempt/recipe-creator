---
id: at-risk-vips
title: At-risk VIP customers
slash_command: /at-risk-vips
group: Segments
owner: intempt
curator: harish
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
touches:
  reads:
    - The order_created event in your project
    - The lifetime_value and days_since_last_activity attributes on users
  writes:
    - A new segment, from step 1 "Build the at-risk VIP list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the at-risk VIP list
    summary: >-
      Customers with lifetime value of 1,000 or more and 2 or more orders, whose last activity was 45
      to 90 days ago and who have not ordered in 45 days.
    builds: segment
    description: |-
      Build a segment of users named "At-Risk VIPs".
      A user is in the segment only when all of these are true:
      - their lifetime_value attribute is 1000 or more
      - their days_since_last_activity attribute is between 45 and 90
      - they did the order_created event 2 or more times, at any time
      - they did not do the order_created event in the last 45 days
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

## What this recipe touches

Reads:

- The order_created event in your project
- The lifetime_value and days_since_last_activity attributes on users

Writes:

- A new segment, from step 1 "Build the at-risk VIP list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
