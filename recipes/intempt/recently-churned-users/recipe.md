---
id: recently-churned-users
title: Recently cancelled customers
slash_command: /recently-churned-users
group: Segments
owner: intempt
summary: Customers who cancelled in the last month, while the reason is fresh and a win-back still has
  a chance.
description: >-
  Users who cancelled their subscription in the last 30 days: fast win-back cohort.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
steps:
  - id: s1
    title: Build the recent-cancel list
    summary: >-
      Users with a subscription cancellation in the last 30 days and lifetime value above zero.
    builds: segment
    description: |-
      Create a segment called "Recently Churned Users".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: subscription_cancelled occurred >= 1 time in last 30 days
      - AND Attribute: lifetime_value > 0
      Description: Users who cancelled in the last 30 days with prior paid history. Fast win-back cohort: easier to recover than older churned users while feedback is still fresh.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Recently cancelled customers

Customers who cancelled in the last month, while the reason is fresh and a win-back still has a chance.

## Steps

1. **Build the recent-cancel list** (builds segment)

   Users with a subscription cancellation in the last 30 days and lifetime value above zero.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
