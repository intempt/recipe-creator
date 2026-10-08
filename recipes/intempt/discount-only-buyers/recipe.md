---
id: discount-only-buyers
title: Discount-only buyers
slash_command: /discount-only-buyers
group: Segments
owner: intempt
curator: harish
summary: Customers who have never bought anything without a discount code, so you can keep them out of
  full-price campaigns and protect your margin.
description: >-
  Customers who only purchase when a discount is applied: suppression cohort for full-price campaigns.
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
prerequisites:
  integrations:
    - value: stripe
      severity: blocking
touches:
  reads:
    - Your Stripe connection
    - The order_created event in your project
    - The discount_codes property on those events
  writes:
    - A new segment, from step 1 "Build the discount-only list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the discount-only list
    summary: >-
      Customers with 2 or more orders that all carried a discount code, and zero orders without one.
    builds: segment
    description: |-
      Build a segment of users named "Discount-Only Buyers".
      A user is in the segment only when all of these are true:
      - they did the order_created event with a discount_codes value that is not empty 2 or more times, at any time
      - they never did the order_created event with an empty discount_codes value
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Discount-only buyers

Customers who have never bought anything without a discount code, so you can keep them out of full-price campaigns and protect your margin.

## Steps

1. **Build the discount-only list** (builds segment)

   Customers with 2 or more orders that all carried a discount code, and zero orders without one.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- Your Stripe connection
- The order_created event in your project
- The discount_codes property on those events

Writes:

- A new segment, from step 1 "Build the discount-only list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
