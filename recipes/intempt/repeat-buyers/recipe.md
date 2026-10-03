---
id: repeat-buyers
title: Repeat buyers
slash_command: /repeat-buyers
group: Segments
owner: intempt
summary: Customers who have ordered three or more times this quarter and spent real money, the right list
  for loyalty perks and review requests.
description: >-
  Customers who have made 3+ purchases in the last 90 days with meaningful spend.
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
    - The lifetime_value attribute on users
  writes:
    - A new segment, from step 1 "Build the repeat-buyer list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the repeat-buyer list
    summary: >-
      Users with 3 or more orders in the last 90 days and lifetime value of 100 or more.
    builds: segment
    description: |-
      Build a segment of users named "Repeat Buyers".
      A user is in the segment only when all of these are true:
      - they did the order_created event 3 or more times in the last 90 days
      - their lifetime_value attribute is 100 or more
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Repeat buyers

Customers who have ordered three or more times this quarter and spent real money, the right list for loyalty perks and review requests.

## Steps

1. **Build the repeat-buyer list** (builds segment)

   Users with 3 or more orders in the last 90 days and lifetime value of 100 or more.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project
- The lifetime_value attribute on users

Writes:

- A new segment, from step 1 "Build the repeat-buyer list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
