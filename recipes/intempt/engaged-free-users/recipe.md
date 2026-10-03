---
id: engaged-free-users
title: Engaged free users
slash_command: /engaged-free-users
group: Segments
owner: intempt
summary: Free-plan users who are in the product often and recently, so upgrade prompts reach the people
  already getting value.
description: >-
  Free-plan users with high engagement: prime upgrade-targeting cohort.
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
    title: Build the engaged free list
    summary: >-
      Users on the free plan with a High engagement score, active in the last 7 days, and 5 or more sessions
      in the last 14 days.
    builds: segment
    description: |-
      Create a segment called "Engaged Free Users".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: plan_name = "free"
      - AND Attribute: engagement_score = "High"
      - AND Attribute: days_since_last_activity <= 7
      - AND Event: session_start occurred >= 5 times in last 14 days
      Description: Free users showing strong engagement and recent activity. Prime cohort for upgrade prompts, premium-feature trials, and account-expansion outreach.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Engaged free users

Free-plan users who are in the product often and recently, so upgrade prompts reach the people already getting value.

## Steps

1. **Build the engaged free list** (builds segment)

   Users on the free plan with a High engagement score, active in the last 7 days, and 5 or more sessions in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
