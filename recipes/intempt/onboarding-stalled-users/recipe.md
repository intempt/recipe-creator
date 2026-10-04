---
id: onboarding-stalled-users
title: Users stuck in onboarding
slash_command: /onboarding-stalled-users
group: Segments
owner: intempt
curator: harish
summary: People who signed up a few weeks ago and still drop in now and then, but have never finished
  setup, so you can help them over the line.
description: >-
  Recently signed up but no activation milestone in last 14 days: activation-rescue cohort.
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
    - The goal_completed_in_journey event in your project
    - The first_seen_at and days_since_last_activity attributes on users
  writes:
    - A new segment, from step 1 "Build the stalled-onboarding list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the stalled-onboarding list
    summary: >-
      Users first seen 7 to 30 days ago who have completed no journey goal since signing up and were last
      active within the past 14 days.
    builds: segment
    description: |-
      Build a segment of users named "Onboarding-Stalled Users".
      A user is in the segment only when all of these are true:
      - their first_seen_at attribute is between 7 and 30 days ago
      - they have not done the goal_completed_in_journey event since their first_seen_at date
      - their days_since_last_activity attribute is 14 or less
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Users stuck in onboarding

People who signed up a few weeks ago and still drop in now and then, but have never finished setup, so you can help them over the line.

## Steps

1. **Build the stalled-onboarding list** (builds segment)

   Users first seen 7 to 30 days ago who have completed no journey goal since signing up and were last active within the past 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The goal_completed_in_journey event in your project
- The first_seen_at and days_since_last_activity attributes on users

Writes:

- A new segment, from step 1 "Build the stalled-onboarding list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
