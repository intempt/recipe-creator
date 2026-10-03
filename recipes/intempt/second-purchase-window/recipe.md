---
id: second-purchase-window
title: First-time buyers in the repeat window
slash_command: /second-purchase-window
group: Segments
owner: intempt
summary: Customers who bought for the first time in the last month, the period when most second purchases
  happen.
description: >-
  First-time buyers in the critical 1-30 day window after their first order. 50% of all repeat purchases
  happen here.
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
    title: Build the second-purchase list
    summary: >-
      Users with exactly 1 order all time, placed within the last 30 days.
    builds: segment
    description: |-
      Create a segment called "Second-Purchase Window".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: order_created occurred = 1 time (all time)
      - AND Event: order_created occurred >= 1 time in last 30 days
      Description: Customers who just bought for the first time and are in the highest-conversion repurchase window. 50.3% of all repeat purchases happen in the first 30 days post-purchase, yet most brands suppress recent buyers from campaigns. This segment fixes that by giving you a clean cohort to target with personalized cross-sells, "complete-the-set" offers, and second-purchase nudges (not discount blasts: handwritten-style notes outperform).
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# First-time buyers in the repeat window

Customers who bought for the first time in the last month, the period when most second purchases happen.

## Steps

1. **Build the second-purchase list** (builds segment)

   Users with exactly 1 order all time, placed within the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
