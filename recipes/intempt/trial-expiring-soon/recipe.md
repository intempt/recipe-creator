---
id: trial-expiring-soon
title: Trials expiring this week
slash_command: /trial-expiring-soon
group: Segments
owner: intempt
summary: Trial users whose trial runs out within a week and who have not paid yet, your last chance to
  convert them.
description: >-
  Trial users approaching expiry who haven't converted to paid.
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
    - The subscription_created event in your project
    - The plan_name and end_date attributes on users
  writes:
    - A new segment, from step 1 "Build the expiring-trial list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the expiring-trial list
    summary: >-
      Users on the trial plan whose end date falls within the next 7 days and who have not created a subscription
      in the last 14 days.
    builds: segment
    description: |-
      Build a segment of users named "Trial Expiring Soon".
      A user is in the segment only when all of these are true:
      - their plan_name attribute is "trial"
      - their end_date attribute is within the next 7 days
      - they did not do the subscription_created event in the last 14 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Trials expiring this week

Trial users whose trial runs out within a week and who have not paid yet, your last chance to convert them.

## Steps

1. **Build the expiring-trial list** (builds segment)

   Users on the trial plan whose end date falls within the next 7 days and who have not created a subscription in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The subscription_created event in your project
- The plan_name and end_date attributes on users

Writes:

- A new segment, from step 1 "Build the expiring-trial list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
