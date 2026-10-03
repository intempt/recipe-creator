---
id: big-basket-buyers
title: Big basket buyers
slash_command: /big-basket-buyers
group: Segments
owner: intempt
summary: Customers who spend heavily on every single order, so premium bundles and higher tiers go to
  people who already buy big.
description: >-
  Customers with high average order value: premium-bundle and upsell-targeting cohort.
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
    - The avg_order_value and lifetime_value attributes on users
  writes:
    - A new segment, from step 1 "Build the big-basket list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the big-basket list
    summary: >-
      Customers with an average order value of 150 or more, 2 or more orders all time, and lifetime value
      of 300 or more.
    builds: segment
    description: |-
      Build a segment of users named "Big-Basket Buyers".
      A user is in the segment only when all of these are true:
      - their avg_order_value attribute is 150 or more
      - they did the order_created event 2 or more times, at any time
      - their lifetime_value attribute is 300 or more
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Big basket buyers

Customers who spend heavily on every single order, so premium bundles and higher tiers go to people who already buy big.

## Steps

1. **Build the big-basket list** (builds segment)

   Customers with an average order value of 150 or more, 2 or more orders all time, and lifetime value of 300 or more.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project
- The avg_order_value and lifetime_value attributes on users

Writes:

- A new segment, from step 1 "Build the big-basket list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
