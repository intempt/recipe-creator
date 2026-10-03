---
id: onboarding-stalled-users
title: Users stuck in onboarding
slash_command: /onboarding-stalled-users
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the stalled-onboarding list
    summary: >-
      Users first seen 7 to 30 days ago who have completed no journey goal since signing up and were last
      active within the past 14 days.
    builds: segment
    description: |-
      Create a segment called "Onboarding-Stalled Users".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: first_seen_at is between 7 and 30 days ago
      - AND Event: goal_completed_in_journey occurred 0 times since first_seen_at
      - AND Attribute: days_since_last_activity <= 14
      Description: Users who signed up 7-30 days ago, are still occasionally active, but have not completed any activation milestone. The activation-rescue cohort. Trigger guided onboarding outreach (in-app checklist, founder-style email, CSM check-in for high-value accounts).
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

## Availability

Install now: every step builds something the engine supports today.
