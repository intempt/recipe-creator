---
id: trial-users-high-engagement
title: Trials most likely to convert
slash_command: /trial-users-high-engagement
group: Segments
owner: intempt
summary: Trial users who are using the product heavily with two weeks left to run, the ones worth a sales
  call.
description: >-
  Trial users with strong usage signals who are likely to convert. Engagement bucketed enum.
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
    title: Build the strong-trial list
    summary: >-
      Users on the trial plan with a High engagement score, an end date within the next 14 days, and 3
      or more journey goals completed in the last 14 days.
    builds: segment
    description: |-
      Create a segment called "Trial Users: High Engagement".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: plan_name = "trial"
      - AND Attribute: end_date is within next 14 days
      - AND Attribute: engagement_score = "High"
      - AND Event: goal_completed_in_journey occurred >= 3 times in last 14 days
      Description: Trial users with strong usage signals: most likely to convert. Trigger high-touch sales outreach or premium-feature unlock.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Trials most likely to convert

Trial users who are using the product heavily with two weeks left to run, the ones worth a sales call.

## Steps

1. **Build the strong-trial list** (builds segment)

   Users on the trial plan with a High engagement score, an end date within the next 14 days, and 3 or more journey goals completed in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
