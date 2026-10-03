---
id: repeat-cart-abandoners
title: Repeat cart abandoners
slash_command: /repeat-cart-abandoners
group: Segments
owner: intempt
summary: People who have walked away from checkout twice or more this month without buying, usually a
  sign of friction or price resistance.
description: >-
  Users who have abandoned checkout 2+ times in the last 30 days without purchasing.
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
    title: Build the repeat-abandoner list
    summary: >-
      Users who abandoned checkout 2 or more times in the last 30 days and placed no order in that period.
    builds: segment
    description: |-
      Create a segment called "Repeat Cart Abandoners".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: abandoned_checkout occurred >= 2 times in last 30 days
      - AND Event: order_created occurred 0 times in last 30 days
      Description: Users who repeatedly abandon checkout: likely friction or price sensitivity. Trigger differentiated recovery offers (different from first-time abandoners).
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Repeat cart abandoners

People who have walked away from checkout twice or more this month without buying, usually a sign of friction or price resistance.

## Steps

1. **Build the repeat-abandoner list** (builds segment)

   Users who abandoned checkout 2 or more times in the last 30 days and placed no order in that period.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
