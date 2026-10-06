---
id: trial-users-high-engagement
title: Trials most likely to convert
slash_command: /trial-users-high-engagement
group: Segments
owner: intempt
curator: harish
summary: >-
  Trial users with high numeric engagement scores and two weeks remaining in their trial period.
description: >-
  Segment trial users exceeding a numeric engagement score threshold with two weeks left before trial
  expiration.
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
    - The goal_completed_in_journey event in your project
    - The plan_name, end_date and engagement_score attributes on users
  writes:
    - A new segment, from step 1 "Build the strong-trial list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the strong-trial list
    summary: >-
      Users on the trial plan with a High engagement score, an end date within the next 14 days, and 3
      or more journey goals completed in the last 14 days.
    builds: segment
    description: |-
      Build a segment of users named "Trial Users: High Engagement".
      A user is in the segment only when all of these are true:
      - their plan_name attribute is "trial"
      - their end_date attribute is within the next 14 days
      - their engagement_score attribute is "High"
      - they did the goal_completed_in_journey event 3 or more times in the last 14 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Trials most likely to convert

Trial users with high numeric engagement scores and two weeks remaining in their trial period.

## Steps

1. **Build the strong-trial list** (builds segment)

   Users on the trial plan with a High engagement score, an end date within the next 14 days, and 3 or more journey goals completed in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The goal_completed_in_journey event in your project
- The plan_name, end_date and engagement_score attributes on users

Writes:

- A new segment, from step 1 "Build the strong-trial list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
