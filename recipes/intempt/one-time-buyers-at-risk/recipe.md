---
id: one-time-buyers-at-risk
title: One-time buyers going cold
slash_command: /one-time-buyers-at-risk
group: Segments
owner: intempt
summary: Customers who bought once, have not been back in two months, and are not trending well, so you
  can give them a reason to return.
description: >-
  Customers who made one purchase but have not returned in 60+ days.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - ecommerce
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
steps:
  - id: s1
    title: Build the one-time-buyer list
    summary: >-
      Users with exactly 1 order all time, no activity for 60 days or more, and a lifecycle score other
      than Regulars or Promising.
    builds: segment
    description: |-
      Create a segment called "One-Time Buyers At Risk".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: order_created occurred = 1 time (all time)
      - AND Attribute: days_since_last_activity >= 60
      - AND Attribute: lifecycle_score is not in ["Regulars", "Promising"]
      Description: Single-purchase customers who haven't returned in over 60 days and aren't on a healthy lifecycle trajectory. Re-engagement opportunity: second-purchase incentive recommended.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# One-time buyers going cold

Customers who bought once, have not been back in two months, and are not trending well, so you can give them a reason to return.

## Steps

1. **Build the one-time-buyer list** (builds segment)

   Users with exactly 1 order all time, no activity for 60 days or more, and a lifecycle score other than Regulars or Promising.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
