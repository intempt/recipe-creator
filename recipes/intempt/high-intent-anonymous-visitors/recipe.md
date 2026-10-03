---
id: high-intent-anonymous-visitors
title: High-intent anonymous visitors
slash_command: /high-intent-anonymous-visitors
group: Segments
owner: intempt
curator: harish
summary: Visitors you cannot email yet who keep coming back, so you can retarget them with ads or try
  to capture an address.
description: >-
  Unidentified visitors with strong engagement signals: ad retargeting cohort.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
    - b2b
    - ecommerce
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
touches:
  reads:
    - The page_viewed and session_start events in your project
    - The total_events and email attributes on users
  writes:
    - A new segment, from step 1 "Build the anonymous visitor list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the anonymous visitor list
    summary: >-
      Visitors with no email on file, 5 or more events in total, and 3 or more page views across 2 or
      more sessions in the last 7 days.
    builds: segment
    description: |-
      Build a segment of users named "High-Intent Anonymous Visitors".
      A user is in the segment only when all of these are true:
      - their total_events attribute is 5 or more
      - their email attribute is empty
      - they did the page_viewed event 3 or more times in the last 7 days
      - they did the session_start event 2 or more times in the last 7 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# High-intent anonymous visitors

Visitors you cannot email yet who keep coming back, so you can retarget them with ads or try to capture an address.

## Steps

1. **Build the anonymous visitor list** (builds segment)

   Visitors with no email on file, 5 or more events in total, and 3 or more page views across 2 or more sessions in the last 7 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The page_viewed and session_start events in your project
- The total_events and email attributes on users

Writes:

- A new segment, from step 1 "Build the anonymous visitor list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
