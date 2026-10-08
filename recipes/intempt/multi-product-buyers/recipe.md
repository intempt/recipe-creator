---
id: multi-product-buyers
title: Multi-product buyers
slash_command: /multi-product-buyers
group: Segments
owner: intempt
curator: harish
summary: Customers who have bought more than once and spent a meaningful amount, so cross-sell offers
  reach people with broad interest.
description: >-
  Customers who have purchased across multiple distinct products: cross-sell-ready cohort.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - ecommerce
  industry:
    - ecommerce
  vertical: []
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
    - A new segment, from step 1 "Build the repeat-spend list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the repeat-spend list
    summary: >-
      Users with 2 or more orders in the last 180 days and lifetime value of 200 or more.
    builds: segment
    description: |-
      Build a segment of users named "Multi-Product Buyers".
      A user is in the segment only when all of these are true:
      - they did the order_created event 2 or more times in the last 180 days
      - their lifetime_value attribute is 200 or more
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Multi-product buyers

Customers who have bought more than once and spent a meaningful amount, so cross-sell offers reach people with broad interest.

## Steps

1. **Build the repeat-spend list** (builds segment)

   Users with 2 or more orders in the last 180 days and lifetime value of 200 or more.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project
- The lifetime_value attribute on users

Writes:

- A new segment, from step 1 "Build the repeat-spend list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
