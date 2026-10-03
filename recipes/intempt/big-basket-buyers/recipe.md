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
steps:
  - id: s1
    title: Build the big-basket list
    summary: >-
      Customers with an average order value of 150 or more, 2 or more orders all time, and lifetime value
      of 300 or more.
    builds: segment
    description: |-
      Create a segment called "Big-Basket Buyers".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: avg_order_value >= 150
      - AND Event: order_created occurred >= 2 times (all time)
      - AND Attribute: lifetime_value >= 300
      Description: Customers who buy at higher AOV per order. Distinct from VIPs (which is by lifetime spend). Big-basket buyers may have fewer orders but consistently spend big on each: the right cohort for premium product launches, bundle offers, and "spend more, save more" tier promotions.
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

## Availability

Install now: every step builds something the engine supports today.
