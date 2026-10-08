---
id: churn-risk-users
title: Paid users going quiet
slash_command: /churn-risk-users
group: Segments
owner: intempt
curator: harish
summary: Paying users who used to log in regularly and have not shown up for a month, so you can reach
  them before they cancel.
description: >-
  Previously active paid users who have gone silent in the last month.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
    - media
  vertical: []
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
touches:
  reads:
    - The session_start event in your project
    - The plan_name attribute on users
  writes:
    - A new segment, from step 1 "Build the silent paid-user list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the silent paid-user list
    summary: >-
      Users on a paid plan who started 5 or more sessions between 60 and 90 days ago and have started
      none in the last 30 days.
    builds: segment
    description: |-
      Build a segment of users named "Churn Risk Users".
      A user is in the segment only when all of these are true:
      - they did the session_start event 5 or more times between 60 and 90 days ago
      - they did not do the session_start event in the last 30 days
      - their plan_name attribute is not "free"
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Paid users going quiet

Paying users who used to log in regularly and have not shown up for a month, so you can reach them before they cancel.

## Steps

1. **Build the silent paid-user list** (builds segment)

   Users on a paid plan who started 5 or more sessions between 60 and 90 days ago and have started none in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The session_start event in your project
- The plan_name attribute on users

Writes:

- A new segment, from step 1 "Build the silent paid-user list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
