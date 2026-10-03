---
id: high-intent-anonymous-visitors
title: High-intent anonymous visitors
slash_command: /high-intent-anonymous-visitors
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the anonymous visitor list
    summary: >-
      Visitors with no email on file, 5 or more events in total, and 3 or more page views across 2 or
      more sessions in the last 7 days.
    builds: segment
    description: |-
      Create a segment called "High-Intent Anonymous Visitors".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: total_events >= 5
      - AND Attribute: email is empty
      - AND Event: page_viewed occurred >= 3 times in last 7 days
      - AND Event: session_start occurred >= 2 times in last 7 days
      Description: Unidentified visitors with multiple sessions and substantial activity. Ad-retargeting cohort: also a candidate for an email-capture popup or content offer.
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

## Availability

Install now: every step builds something the engine supports today.
