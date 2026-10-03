---
id: high-cart-value-abandoners
title: High-value cart abandoners
slash_command: /high-cart-value-abandoners
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the big-cart list
    summary: >-
      Users who abandoned a cart worth 200 or more in the last 7 days and have placed no order in those
      7 days.
    builds: segment
    description: |-
      Create a segment called "High-Cart-Value Abandoners".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: cart_abandoned where total_amount >= 200 occurred >= 1 time in last 7 days
      - AND Event: order_created occurred 0 times in last 7 days
      Description: Cart abandoners whose abandoned cart value is high: priority recovery cohort. Worth more attention (and a potentially higher-effort intervention like a personal email or SMS) than low-cart-value abandoners. Distinct from repeat-cart-abandoners (which targets by frequency, not value).
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

## Availability

Install now: every step builds something the engine supports today.
