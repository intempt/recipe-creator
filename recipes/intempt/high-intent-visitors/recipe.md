---
id: high-intent-visitors
title: High-intent visitors
slash_command: /high-intent-visitors
group: Segments
owner: intempt
curator: harish
summary: Free and unregistered users who read both your pricing and your docs in the last two weeks, the
  clearest sign somebody is close to buying.
description: >-
  Non-customers who viewed both pricing and documentation in the last 14 days: strong buying signals.
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
    - The page_viewed event in your project
    - The page_url property on those events
    - The plan_name attribute on users
  writes:
    - A new segment, from step 1 "Build the high-intent list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the high-intent list
    summary: >-
      Users with no plan or the free plan who viewed both a /pricing page and a /docs page in the last
      14 days.
    builds: segment
    description: |-
      Build a segment of users named "High-Intent Visitors".
      A user is in the segment only when all of these are true:
      - they did the page_viewed event with a page_url that contains "/pricing" at least once in the last 14 days
      - they did the page_viewed event with a page_url that contains "/docs" at least once in the last 14 days
      - their plan_name attribute is empty or is "free"
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# High-intent visitors

Free and unregistered users who read both your pricing and your docs in the last two weeks, the clearest sign somebody is close to buying.

## Steps

1. **Build the high-intent list** (builds segment)

   Users with no plan or the free plan who viewed both a /pricing page and a /docs page in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The page_viewed event in your project
- The page_url property on those events
- The plan_name attribute on users

Writes:

- A new segment, from step 1 "Build the high-intent list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
