---
id: replenishment-ready
title: Customers due to re-order
slash_command: /replenishment-ready
group: Segments
owner: intempt
curator: harish
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
  industry:
    - ecommerce
  vertical:
    - subscription
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
touches:
  reads:
    - The order_created event in your project
  writes:
    - A new segment, from step 1 "Build the replenishment list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the replenishment list
    summary: >-
      Users who have ordered at least once, last ordered 30 to 60 days ago, and have not ordered in the
      last 30 days.
    builds: segment
    description: |-
      Build a segment of users named "Replenishment-Ready".
      A user is in the segment only when all of these are true:
      - they did the order_created event at least once between 30 and 60 days ago
      - they did not do the order_created event in the last 30 days
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

## What this recipe touches

Reads:

- The order_created event in your project

Writes:

- A new segment, from step 1 "Build the replenishment list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
