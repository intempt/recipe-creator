---
id: paid-users-low-engagement
title: Paid users losing interest
slash_command: /paid-users-low-engagement
group: Segments
owner: intempt
curator: harish
summary: Paying customers whose usage has dropped off in the last couple of weeks, early enough to fix
  before it turns into churn.
description: >-
  Paying customers showing early disengagement signals. Engagement bucketed enum.
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
    - The plan_name, days_since_last_activity and engagement_score attributes on users
  writes:
    - A new segment, from step 1 "Build the low-engagement list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the low-engagement list
    summary: >-
      Users on a paid plan (not free or trial) with a Low engagement score whose last activity was 7 to
      21 days ago.
    builds: segment
    description: |-
      Build a segment of users named "Paid Users: Low Engagement".
      A user is in the segment only when all of these are true:
      - their plan_name attribute is neither "free" nor "trial"
      - their days_since_last_activity attribute is between 7 and 21
      - their engagement_score attribute is "Low"
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Paid users losing interest

Paying customers whose usage has dropped off in the last couple of weeks, early enough to fix before it turns into churn.

## Steps

1. **Build the low-engagement list** (builds segment)

   Users on a paid plan (not free or trial) with a Low engagement score whose last activity was 7 to 21 days ago.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The plan_name, days_since_last_activity and engagement_score attributes on users

Writes:

- A new segment, from step 1 "Build the low-engagement list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
