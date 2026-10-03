---
id: expansion-candidates
title: Users close to their plan limit
slash_command: /expansion-candidates
group: Segments
owner: intempt
curator: harish
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
touches:
  reads:
    - The plan_name and usage_pct attributes on users
  writes:
    - A new segment, from step 1 "Build the near-limit list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the near-limit list
    summary: >-
      Users on any plan other than enterprise whose usage is at 80 percent or more of their limit.
    builds: segment
    description: |-
      Build a segment of users named "Expansion Candidates".
      A user is in the segment only when all of these are true:
      - their plan_name attribute is not "enterprise"
      - their usage_pct attribute is 80 or more
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

## What this recipe touches

Reads:

- The plan_name and usage_pct attributes on users

Writes:

- A new segment, from step 1 "Build the near-limit list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
