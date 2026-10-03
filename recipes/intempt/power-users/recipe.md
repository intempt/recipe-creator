---
id: power-users
title: Power users
slash_command: /power-users
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the power-user list
    summary: >-
      Users with 10 or more sessions and 20 or more clicks in the last 30 days, a High engagement score,
      and activity in the last 7 days.
    builds: segment
    description: |-
      Create a segment called "Power Users".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: session_start occurred >= 10 times in last 30 days
      - AND Event: click_on occurred >= 20 times in last 30 days
      - AND Attribute: engagement_score = "High"
      - AND Attribute: last_seen_at is within last 7 days
      Description: Highly engaged users: frequent sessions, high engagement, recent activity. Priority cohort for advocacy programs, beta access, and case-study outreach.
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

## Availability

Install now: every step builds something the engine supports today.
