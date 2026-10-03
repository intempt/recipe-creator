---
id: high-frequency-buyers
title: High-frequency buyers
slash_command: /high-frequency-buyers
group: Segments
owner: intempt
summary: Customers who order at least four times a quarter, so loyalty perks and early access go to the
  people who buy most often.
description: >-
  Customers who purchase 4+ times per quarter: most loyal cohort.
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
    - A new segment, from step 1 "Build the frequent-buyer list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the frequent-buyer list
    summary: >-
      Users with 4 or more orders in the last 90 days.
    builds: segment
    description: |-
      Build a segment of users named "High-Frequency Buyers".
      A user is in the segment only when all of these are true:
      - they did the order_created event 4 or more times in the last 90 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# High-frequency buyers

Customers who order at least four times a quarter, so loyalty perks and early access go to the people who buy most often.

## Steps

1. **Build the frequent-buyer list** (builds segment)

   Users with 4 or more orders in the last 90 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project

Writes:

- A new segment, from step 1 "Build the frequent-buyer list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
