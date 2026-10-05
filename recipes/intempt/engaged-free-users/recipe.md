---
id: engaged-free-users
title: Engaged free users
slash_command: /engaged-free-users
group: Segments
owner: intempt
curator: harish
summary: >-
  Identify free-plan users using their computed engagement_score to help prioritize upgrade outreach. The
  score is a number, not a High-tier match.
description: >-
  Free-plan users evaluated using their computed engagement_score for upgrade targeting.
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
    - The session_start event in your project
    - The plan_name, engagement_score and days_since_last_activity attributes on users
  writes:
    - A new segment, from step 1 "Build the engaged free list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the engaged free list
    summary: >-
      Users on the free plan with a High engagement score, active in the last 7 days, and 5 or more sessions
      in the last 14 days.
    builds: segment
    description: |-
      Build a segment of users named "Engaged Free Users".
      A user is in the segment only when all of these are true:
      - their plan_name attribute is "free"
      - their engagement_score attribute is "High"
      - their days_since_last_activity attribute is 7 or less
      - they did the session_start event 5 or more times in the last 14 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Engaged free users

Identify free-plan users using their computed engagement_score to help prioritize upgrade outreach. The score is a number, not a High-tier match.

## Steps

1. **Build the engaged free list** (builds segment)

   Users on the free plan with a High engagement score, active in the last 7 days, and 5 or more sessions in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The session_start event in your project
- The plan_name, engagement_score and days_since_last_activity attributes on users

Writes:

- A new segment, from step 1 "Build the engaged free list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
