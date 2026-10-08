---
id: engaged-non-buyers
title: Engaged visitors who never bought
slash_command: /engaged-non-buyers
group: Segments
owner: intempt
curator: harish
summary: People who use your site a lot but have never placed an order, so you can aim a first-purchase
  offer at them.
description: >-
  Highly engaged visitors who have never made a purchase: first-purchase targeting cohort.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - ecommerce
  industry:
    - ecommerce
  vertical: []
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
touches:
  reads:
    - The order_created event in your project
    - The total_events, days_since_last_activity and email attributes on users
  writes:
    - A new segment, from step 1 "Build the non-buyer list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the non-buyer list
    summary: >-
      Known users with 10 or more events, zero orders all time, activity in the last 7 days, and an email
      on file.
    builds: segment
    description: |-
      Build a segment of users named "Engaged Non-Buyers".
      A user is in the segment only when all of these are true:
      - their total_events attribute is 10 or more
      - they have never done the order_created event
      - their days_since_last_activity attribute is 7 or less
      - their email attribute is not empty
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Engaged visitors who never bought

People who use your site a lot but have never placed an order, so you can aim a first-purchase offer at them.

## Steps

1. **Build the non-buyer list** (builds segment)

   Known users with 10 or more events, zero orders all time, activity in the last 7 days, and an email on file.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project
- The total_events, days_since_last_activity and email attributes on users

Writes:

- A new segment, from step 1 "Build the non-buyer list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
