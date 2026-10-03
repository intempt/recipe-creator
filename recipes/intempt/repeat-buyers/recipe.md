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
steps:
  - id: s1
    title: Build the repeat-buyer list
    summary: >-
      Users with 3 or more orders in the last 90 days and lifetime value of 100 or more.
    builds: segment
    description: |-
      Create a segment called "Repeat Buyers".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: order_created occurred >= 3 times in last 90 days
      - AND Attribute: lifetime_value >= 100
      Description: Repeat customers with meaningful spend. Priority for loyalty rewards, replenishment campaigns, and review requests.
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

## Availability

Install now: every step builds something the engine supports today.
