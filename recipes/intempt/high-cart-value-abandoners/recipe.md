---
id: high-cart-value-abandoners
title: High-value cart abandoners
slash_command: /high-cart-value-abandoners
group: Segments
owner: intempt
curator: harish
summary: People who walked away from an expensive cart in the last week and have not bought since, so
  you chase the baskets worth chasing.
description: >-
  Cart abandoners with high cart value: priority recovery cohort distinct from frequency-based abandoners.
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
    - The cart_abandoned and order_created events in your project
    - The total_amount property on those events
  writes:
    - A new segment, from step 1 "Build the big-cart list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the big-cart list
    summary: >-
      Users who abandoned a cart worth 200 or more in the last 7 days and have placed no order in those
      7 days.
    builds: segment
    description: |-
      Build a segment of users named "High-Cart-Value Abandoners".
      A user is in the segment only when all of these are true:
      - they did the cart_abandoned event with a total_amount of 200 or more at least once in the last 7 days
      - they did not do the order_created event in the last 7 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# High-value cart abandoners

People who walked away from an expensive cart in the last week and have not bought since, so you chase the baskets worth chasing.

## Steps

1. **Build the big-cart list** (builds segment)

   Users who abandoned a cart worth 200 or more in the last 7 days and have placed no order in those 7 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The cart_abandoned and order_created events in your project
- The total_amount property on those events

Writes:

- A new segment, from step 1 "Build the big-cart list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
