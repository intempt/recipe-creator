---
id: churn-risk-users
title: Paid users going quiet
slash_command: /churn-risk-users
group: Segments
owner: intempt
summary: Paying users who used to log in regularly and have not shown up for a month, so you can reach
  them before they cancel.
description: >-
  Previously active paid users who have gone silent in the last month.
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
    title: Build the silent paid-user list
    summary: >-
      Users on a paid plan who started 5 or more sessions between 60 and 90 days ago and have started
      none in the last 30 days.
    builds: segment
    description: |-
      Create a segment called "Churn Risk Users".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: session_start occurred >= 5 times between 60 and 90 days ago
      - AND Event: session_start occurred 0 times in last 30 days
      - AND Attribute: plan_name is not "free"
      Description: Previously active paid users who have gone silent. Trigger CSM outreach or save-offer journey before they churn.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Paid users going quiet

Paying users who used to log in regularly and have not shown up for a month, so you can reach them before they cancel.

## Steps

1. **Build the silent paid-user list** (builds segment)

   Users on a paid plan who started 5 or more sessions between 60 and 90 days ago and have started none in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
