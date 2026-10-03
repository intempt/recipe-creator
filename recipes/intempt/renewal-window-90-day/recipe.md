---
id: renewal-window-90-day
title: Renewals due in 90 days
slash_command: /renewal-window-90-day
group: Segments
owner: intempt
summary: Paid subscriptions that end within the next three months, so renewal conversations start early
  instead of the week before.
description: >-
  Subscriptions ending in next 90 days) foundation for renewal-flow journeys and NRR plays.
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
    - The end_date and plan_name attributes on users
  writes:
    - A new segment, from step 1 "Build the renewal list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the renewal list
    summary: >-
      Users on a paid plan whose subscription end date falls within the next 90 days and is still in the
      future.
    builds: segment
    description: |-
      Build a segment of users named "Renewal Window: 90 Days".
      A user is in the segment only when all of these are true:
      - their end_date attribute is in the future and within the next 90 days
      - their plan_name attribute is not "free"
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Renewals due in 90 days

Paid subscriptions that end within the next three months, so renewal conversations start early instead of the week before.

## Steps

1. **Build the renewal list** (builds segment)

   Users on a paid plan whose subscription end date falls within the next 90 days and is still in the future.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The end_date and plan_name attributes on users

Writes:

- A new segment, from step 1 "Build the renewal list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
