---
id: recently-signed-up-users
title: Recent signups
slash_command: /recently-signed-up-users
group: Segments
owner: intempt
curator: harish
summary: Everyone who created an account in the last month, the audience for your welcome and first-week
  activation emails.
description: >-
  Users who created an account in the last 30 days: onboarding cohort.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
    - ecommerce
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
touches:
  reads:
    - The first_seen_at attribute on users
  writes:
    - A new segment, from step 1 "Build the new signup list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the new signup list
    summary: >-
      Users first seen in the last 30 days.
    builds: segment
    description: |-
      Build a segment of users named "Recently Signed-Up Users".
      A user is in the segment only when all of these are true:
      - their first_seen_at attribute is within the last 30 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Recent signups

Everyone who created an account in the last month, the audience for your welcome and first-week activation emails.

## Steps

1. **Build the new signup list** (builds segment)

   Users first seen in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The first_seen_at attribute on users

Writes:

- A new segment, from step 1 "Build the new signup list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
