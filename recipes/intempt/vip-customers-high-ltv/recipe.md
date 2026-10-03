---
id: vip-customers-high-ltv
title: VIP customers
slash_command: /vip-customers-high-ltv
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the VIP list
    summary: >-
      Users with lifetime value of 1,000 or more and 2 or more orders.
    builds: segment
    description: |-
      Create a segment called "VIP Customers".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: lifetime_value >= 1000
      - AND Event: order_created occurred >= 2 times
      Description: High lifetime-value customers with repeat purchase history. Foundation segment for VIP rewards, exclusive product access, and concierge support.
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

## Availability

Install now: every step builds something the engine supports today.
