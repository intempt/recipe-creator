---
id: newly-activated-users
title: Newly activated users
slash_command: /newly-activated-users
group: Segments
owner: intempt
curator: harish
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
inputs:
  - input: Activation journey
    what_the_installer_supplies: The journey whose goal marks a user as activated
    if_missing: The step is marked vague and waits until one is chosen.
touches:
  reads:
    - The goal_completed_in_journey event in your project
    - The plan_name attribute on users
    - The activation journey you supply when you run it
  writes:
    - A new segment, from step 1 "Build the newly-activated list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the newly-activated list
    summary: >-
      Users on a paid plan who completed the activation journey goal at least once in the last 7 days.
    builds: segment
    description: |-
      Build a segment of users named "Newly Activated Users".
      A user is in the segment only when all of these are true:
      - they did the goal_completed_in_journey event at least once in the last 7 days, with a journey_id equal to the activation journey chosen for this run
      - their plan_name attribute is not "free"
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

## What this recipe touches

Reads:

- The goal_completed_in_journey event in your project
- The plan_name attribute on users
- The activation journey you supply when you run it

Writes:

- A new segment, from step 1 "Build the newly-activated list"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Activation journey | The journey whose goal marks a user as activated | The step is marked vague and waits until one is chosen. |

## Availability

Install now: every step builds something the engine supports today.
