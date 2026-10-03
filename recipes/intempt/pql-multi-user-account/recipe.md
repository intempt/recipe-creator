---
id: pql-multi-user-account
title: Free accounts with a team trying it
slash_command: /pql-multi-user-account
group: Segments
owner: intempt
summary: Free and trial accounts where two or more colleagues are both active, which converts better than
  one person trying it alone.
description: >-
  Free/trial accounts with 2+ engaged users from same company) enterprise PQL signal.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
steps:
  - id: s1
    title: Build the team-trial list
    summary: >-
      Accounts with 2 or more users, where those users started 3 or more sessions and completed at least
      one journey goal in the last 14 days.
    builds: segment
    description: |-
      Create a segment called "PQL: Multi-User Account".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: users_count >= 2
      - AND Event (across users in account): session_start occurred >= 3 times in last 14 days
      - AND Event (across users in account): goal_completed_in_journey occurred >= 1 time in last 14 days
      Description: Accounts where 2+ users from the same company are actively engaged in trial or free plan. The enterprise PQL signal: distinguishes team-buying behavior from individual-trial signups. Highest-converting PQL cohort: when multiple stakeholders test the product, they convert at 2-3x the rate of individual-trial PQLs.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Free accounts with a team trying it

Free and trial accounts where two or more colleagues are both active, which converts better than one person trying it alone.

## Steps

1. **Build the team-trial list** (builds segment)

   Accounts with 2 or more users, where those users started 3 or more sessions and completed at least one journey goal in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
