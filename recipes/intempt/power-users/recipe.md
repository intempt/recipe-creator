---
id: power-users
title: Power users
slash_command: /power-users
group: Segments
owner: intempt
curator: harish
summary: Your most active users over the last month, the people to ask for reviews, case studies, and
  beta feedback.
description: >-
  Highly engaged users with frequent sessions and high activity score in the last 30 days.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - all
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
touches:
  reads:
    - The session_start and click_on events in your project
    - The engagement_score and last_seen_at attributes on users
  writes:
    - A new segment, from step 1 "Build the power-user list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the power-user list
    summary: >-
      Users with 10 or more sessions and 20 or more clicks in the last 30 days, a High engagement score,
      and activity in the last 7 days.
    builds: segment
    description: |-
      Build a segment of users named "Power Users".
      A user is in the segment only when all of these are true:
      - they did the session_start event 10 or more times in the last 30 days
      - they did the click_on event 20 or more times in the last 30 days
      - their engagement_score attribute is "High"
      - their last_seen_at attribute is within the last 7 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Power users

Your most active users over the last month, the people to ask for reviews, case studies, and beta feedback.

## Steps

1. **Build the power-user list** (builds segment)

   Users with 10 or more sessions and 20 or more clicks in the last 30 days, a High engagement score, and activity in the last 7 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The session_start and click_on events in your project
- The engagement_score and last_seen_at attributes on users

Writes:

- A new segment, from step 1 "Build the power-user list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
