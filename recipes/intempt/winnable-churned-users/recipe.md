---
id: winnable-churned-users
title: Winnable churned users
slash_command: /winnable-churned-users
group: Segments
owner: intempt
summary: People who cancelled in the last two months but used the product heavily before they left, the
  best odds for a win-back.
description: >-
  Recently churned users who showed engagement before churn: best win-back candidates.
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
    title: Build the win-back list
    summary: >-
      Users with a subscription cancellation in the last 60 days, lifetime value above zero, and 50 or
      more events on record.
    builds: segment
    description: |-
      Create a segment called "Winnable Churned Users".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: subscription_cancelled occurred >= 1 time in last 60 days
      - AND Attribute: lifetime_value > 0
      - AND Attribute: total_events >= 50
      Description: Recently churned users with prior engagement (positive lifetime value, meaningful event volume during their active period). Best candidates for a win-back offer.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Winnable churned users

People who cancelled in the last two months but used the product heavily before they left, the best odds for a win-back.

## Steps

1. **Build the win-back list** (builds segment)

   Users with a subscription cancellation in the last 60 days, lifetime value above zero, and 50 or more events on record.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
