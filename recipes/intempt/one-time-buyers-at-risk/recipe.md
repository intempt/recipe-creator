---
id: one-time-buyers-at-risk
title: One-time buyers going cold
slash_command: /one-time-buyers-at-risk
group: Segments
owner: intempt
curator: harish
summary: Customers who bought once, have not been back in two months, and are not trending well, so you
  can give them a reason to return.
description: >-
  Customers who made one purchase but have not returned in 60+ days.
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
    - The days_since_last_activity and lifecycle_score attributes on users
  writes:
    - A new segment, from step 1 "Build the one-time-buyer list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the one-time-buyer list
    summary: >-
      Users with exactly 1 order all time, no activity for 60 days or more, and a lifecycle score other
      than Regulars or Promising.
    builds: segment
    description: |-
      Build a segment of users named "One-Time Buyers At Risk".
      A user is in the segment only when all of these are true:
      - they did the order_created event exactly 1 time, at any time
      - their days_since_last_activity attribute is 60 or more
      - their lifecycle_score attribute is neither "Regulars" nor "Promising"
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# One-time buyers going cold

Customers who bought once, have not been back in two months, and are not trending well, so you can give them a reason to return.

## Steps

1. **Build the one-time-buyer list** (builds segment)

   Users with exactly 1 order all time, no activity for 60 days or more, and a lifecycle score other than Regulars or Promising.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project
- The days_since_last_activity and lifecycle_score attributes on users

Writes:

- A new segment, from step 1 "Build the one-time-buyer list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
