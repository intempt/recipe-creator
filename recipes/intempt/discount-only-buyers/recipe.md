---
id: discount-only-buyers
title: Discount-only buyers
slash_command: /discount-only-buyers
group: Segments
owner: intempt
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
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
prerequisites:
  integrations:
    - value: stripe
      severity: blocking
steps:
  - id: s1
    title: Build the discount-only list
    summary: >-
      Customers with 2 or more orders that all carried a discount code, and zero orders without one.
    builds: segment
    description: |-
      Create a segment called "Discount-Only Buyers".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: order_created where discount_codes is not empty occurred >= 2 times (all time)
      - AND Event: order_created where discount_codes is empty occurred 0 times (all time)
      Description: Customers whose every order has a discount code applied. Margin-protective suppression cohort: exclude from full-price campaigns and reserve for sale-only outreach. Pricing them at full price typically results in zero conversion; the bargain-hunting behavior is the buying signal.
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

## Availability

Install now: every step builds something the engine supports today.
