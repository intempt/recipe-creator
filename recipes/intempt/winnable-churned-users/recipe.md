---
id: winnable-churned-users
title: Winnable churned users
slash_command: /winnable-churned-users
group: Segments
owner: intempt
curator: harish
summary: People who cancelled in the last two months but used the product heavily before they left, the
  best odds for a win-back.
description: >-
  Recently churned users who showed engagement before churn: best win-back candidates.
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
    - The lifetime_value and total_events attributes on users
  writes:
    - A new segment, from step 1 "Build the win-back list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the win-back list
    summary: >-
      Users with a subscription cancellation in the last 60 days, lifetime value above zero, and 50 or
      more events on record.
    builds: segment
    description: |-
      Build a segment of users named "Winnable Churned Users".
      A user is in the segment only when all of these are true:
      - they did the subscription_cancelled event at least once in the last 60 days
      - their lifetime_value attribute is more than 0
      - their total_events attribute is 50 or more
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Winnable churned users

People who cancelled in the last two months but used the product heavily before they left, the best odds for a win-back.

## Steps

1. **Build the win-back list** (builds segment)

   Users with a subscription cancellation in the last 60 days, lifetime value above zero, and 50 or more events on record.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The subscription_cancelled event in your project
- The lifetime_value and total_events attributes on users

Writes:

- A new segment, from step 1 "Build the win-back list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
