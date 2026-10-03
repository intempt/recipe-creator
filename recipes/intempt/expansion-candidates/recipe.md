---
id: expansion-candidates
title: Users close to their plan limit
slash_command: /expansion-candidates
group: Segments
owner: intempt
summary: Users who have used up most of their plan allowance, so you can start the upgrade conversation
  before they hit the ceiling.
description: >-
  Users approaching their plan limit who are ready for an upgrade conversation.
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
    title: Build the near-limit list
    summary: >-
      Users on any plan other than enterprise whose usage is at 80 percent or more of their limit.
    builds: segment
    description: |-
      Create a segment called "Expansion Candidates".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: plan_name is not "enterprise"
      - AND Attribute: usage_pct >= 80
      Description: Users approaching plan limits: prime upgrade candidates. Trigger in-app upgrade prompt or AE outreach.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Users close to their plan limit

Users who have used up most of their plan allowance, so you can start the upgrade conversation before they hit the ceiling.

## Steps

1. **Build the near-limit list** (builds segment)

   Users on any plan other than enterprise whose usage is at 80 percent or more of their limit.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
