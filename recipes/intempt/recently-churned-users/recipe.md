---
id: recently-churned-users
title: Recently cancelled customers
slash_command: /recently-churned-users
group: Segments
owner: intempt
curator: harish
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
touches:
  reads:
    - The subscription_cancelled event in your project
    - The lifetime_value attribute on users
  writes:
    - A new segment, from step 1 "Build the recent-cancel list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the recent-cancel list
    summary: >-
      Users with a subscription cancellation in the last 30 days and lifetime value above zero.
    builds: segment
    description: |-
      Build a segment of users named "Recently Churned Users".
      A user is in the segment only when all of these are true:
      - they did the subscription_cancelled event at least once in the last 30 days
      - their lifetime_value attribute is more than 0
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

## What this recipe touches

Reads:

- The subscription_cancelled event in your project
- The lifetime_value attribute on users

Writes:

- A new segment, from step 1 "Build the recent-cancel list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
