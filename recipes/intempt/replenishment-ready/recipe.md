---
id: replenishment-ready
title: Customers due to re-order
slash_command: /replenishment-ready
group: Segments
owner: intempt
summary: Customers whose last order was one to two months ago and who are about due for another, the moment
  a running-low reminder lands best.
description: >-
  Customers approaching their typical re-order cycle. 8-15% conversion on replenishment reminders vs 1-3%
  on general promos.
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
    title: Build the replenishment list
    summary: >-
      Users who have ordered at least once, last ordered 30 to 60 days ago, and have not ordered in the
      last 30 days.
    builds: segment
    description: |-
      Create a segment called "Replenishment-Ready".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: order_created occurred >= 1 time (all time)
      - AND Event: order_created occurred 0 times in last 30 days
      - AND Event: order_created occurred >= 1 time between 30 and 60 days ago
      Description: Customers whose last purchase was 30-60 days ago and who are due for re-purchase based on typical consumption cycles. Trigger replenishment reminder ("Running low?") timed to product depletion. Replenishment messaging consistently outperforms generic promotion by 5-10x.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Customers due to re-order

Customers whose last order was one to two months ago and who are about due for another, the moment a running-low reminder lands best.

## Steps

1. **Build the replenishment list** (builds segment)

   Users who have ordered at least once, last ordered 30 to 60 days ago, and have not ordered in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
