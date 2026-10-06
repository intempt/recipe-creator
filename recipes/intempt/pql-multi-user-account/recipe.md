---
id: pql-multi-user-account
title: Free accounts with a team trying it
slash_command: /pql-multi-user-account
group: Segments
owner: intempt
curator: harish
summary: >-
  Identify product-qualified leads by segmenting free and trial users who log multiple sessions and complete
  key activation goals.
description: >-
  Segment individual free or trial users meeting session and goal-completion activity thresholds to flag
  qualified leads for outreach.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
    - ecommerce
  vertical:
    - plg
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
touches:
  reads:
    - The session_start and goal_completed_in_journey events in your project
    - The users_count attribute on accounts
  writes:
    - A new segment, from step 1 "Build the team-trial list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the team-trial list
    summary: >-
      Accounts with 2 or more users, where those users started 3 or more sessions and completed at least
      one journey goal in the last 14 days.
    builds: segment
    description: |-
      Build a segment of accounts named "PQL: Multi-User Account".
      An account is in the segment only when all of these are true:
      - its users_count attribute is 2 or more
      - the users in the account together did the session_start event 3 or more times in the last 14 days
      - the users in the account together did the goal_completed_in_journey event at least once in the last 14 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Free accounts with a team trying it

Identify product-qualified leads by segmenting free and trial users who log multiple sessions and complete key activation goals.

## Steps

1. **Build the team-trial list** (builds segment)

   Accounts with 2 or more users, where those users started 3 or more sessions and completed at least one journey goal in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The session_start and goal_completed_in_journey events in your project
- The users_count attribute on accounts

Writes:

- A new segment, from step 1 "Build the team-trial list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
