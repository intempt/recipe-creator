---
id: engaged-non-buyers
title: Engaged visitors who never bought
slash_command: /engaged-non-buyers
group: Segments
owner: intempt
summary: People who use your site a lot but have never placed an order, so you can aim a first-purchase
  offer at them.
description: >-
  Highly engaged visitors who have never made a purchase: first-purchase targeting cohort.
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
    title: Build the non-buyer list
    summary: >-
      Known users with 10 or more events, zero orders all time, activity in the last 7 days, and an email
      on file.
    builds: segment
    description: |-
      Create a segment called "Engaged Non-Buyers".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: total_events >= 10
      - AND Event: order_created occurred 0 times (all time)
      - AND Attribute: days_since_last_activity <= 7
      - AND Attribute: email is not empty
      Description: Identified users who engage frequently but have never purchased. First-purchase incentive cohort: typically responds well to a first-order discount or product-discovery campaign.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Engaged visitors who never bought

People who use your site a lot but have never placed an order, so you can aim a first-purchase offer at them.

## Steps

1. **Build the non-buyer list** (builds segment)

   Known users with 10 or more events, zero orders all time, activity in the last 7 days, and an email on file.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
