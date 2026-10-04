---
id: vip-customers-high-ltv
title: VIP customers
slash_command: /vip-customers-high-ltv
group: Segments
owner: intempt
curator: harish
summary: Customers who have spent 1,000 or more across repeat orders, the base list for rewards, early
  access, and concierge support.
description: >-
  Highest-value customers by lifetime spend. Concrete numeric threshold (no percentile placeholder).
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
    - A new segment, from step 1 "Build the VIP list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the VIP list
    summary: >-
      Users with lifetime value of 1,000 or more and 2 or more orders.
    builds: segment
    description: |-
      Build a segment of users named "VIP Customers".
      A user is in the segment only when all of these are true:
      - their lifetime_value attribute is 1000 or more
      - they did the order_created event 2 or more times, at any time
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# VIP customers

Customers who have spent 1,000 or more across repeat orders, the base list for rewards, early access, and concierge support.

## Steps

1. **Build the VIP list** (builds segment)

   Users with lifetime value of 1,000 or more and 2 or more orders.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project
- The lifetime_value attribute on users

Writes:

- A new segment, from step 1 "Build the VIP list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
