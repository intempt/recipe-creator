---
id: newly-activated-users
title: Newly activated users
slash_command: /newly-activated-users
group: Segments
owner: intempt
summary: Paying users who hit their activation milestone in the last week, while they are warm enough
  to say yes to more.
description: >-
  Users who completed activation in the last 7 days: warm and ready to expand.
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
steps:
  - id: s1
    title: Build the newly-activated list
    summary: >-
      Users on a paid plan who completed the activation journey goal at least once in the last 7 days.
    builds: segment
    description: |-
      Create a segment called "Newly Activated Users".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: goal_completed_in_journey where journey_id = <activation journey id> occurred >= 1 time in last 7 days
      - AND Attribute: plan_name is not "free"
      Description: Users who hit the activation milestone in the last 7 days. Warm cohort for expansion outreach, feature-discovery campaigns, and upgrade prompts.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Newly activated users

Paying users who hit their activation milestone in the last week, while they are warm enough to say yes to more.

## Steps

1. **Build the newly-activated list** (builds segment)

   Users on a paid plan who completed the activation journey goal at least once in the last 7 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
