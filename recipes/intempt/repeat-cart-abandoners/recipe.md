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
touches:
  reads:
    - The abandoned_checkout and order_created events in your project
  writes:
    - A new segment, from step 1 "Build the repeat-abandoner list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the repeat-abandoner list
    summary: >-
      Users who abandoned checkout 2 or more times in the last 30 days and placed no order in that period.
    builds: segment
    description: |-
      Build a segment of users named "Repeat Cart Abandoners".
      A user is in the segment only when all of these are true:
      - they did the abandoned_checkout event 2 or more times in the last 30 days
      - they did not do the order_created event in the last 30 days
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

## What this recipe touches

Reads:

- The abandoned_checkout and order_created events in your project

Writes:

- A new segment, from step 1 "Build the repeat-abandoner list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
