---
id: second-purchase-window
title: First-time buyers in the repeat window
slash_command: /second-purchase-window
group: Segments
owner: intempt
curator: harish
summary: Customers who bought for the first time in the last month, the period when most second purchases
  happen.
description: >-
  First-time buyers in the critical 1-30 day window after their first order. 50% of all repeat purchases
  happen here.
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
touches:
  reads:
    - The order_created event in your project
  writes:
    - A new segment, from step 1 "Build the second-purchase list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the second-purchase list
    summary: >-
      Users with exactly 1 order all time, placed within the last 30 days.
    builds: segment
    description: |-
      Build a segment of users named "Second-Purchase Window".
      A user is in the segment only when all of these are true:
      - they did the order_created event exactly 1 time, at any time
      - that order_created event happened in the last 30 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# First-time buyers in the repeat window

Customers who bought for the first time in the last month, the period when most second purchases happen.

## Steps

1. **Build the second-purchase list** (builds segment)

   Users with exactly 1 order all time, placed within the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project

Writes:

- A new segment, from step 1 "Build the second-purchase list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
