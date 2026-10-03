---
id: trial-expiring-soon
title: Trials expiring this week
slash_command: /trial-expiring-soon
group: Segments
owner: intempt
summary: Trial users whose trial runs out within a week and who have not paid yet, your last chance to
  convert them.
description: >-
  Trial users approaching expiry who haven't converted to paid.
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
    title: Build the expiring-trial list
    summary: >-
      Users on the trial plan whose end date falls within the next 7 days and who have not created a subscription
      in the last 14 days.
    builds: segment
    description: |-
      Create a segment called "Trial Expiring Soon".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: plan_name = "trial"
      - AND Attribute: end_date is within next 7 days
      - AND Event: subscription_created has not occurred in last 14 days
      Description: Trial users approaching expiry without paid conversion. Trigger a final-push email or in-app upgrade prompt.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Trials expiring this week

Trial users whose trial runs out within a week and who have not paid yet, your last chance to convert them.

## Steps

1. **Build the expiring-trial list** (builds segment)

   Users on the trial plan whose end date falls within the next 7 days and who have not created a subscription in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
