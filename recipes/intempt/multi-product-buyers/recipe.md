---
id: multi-product-buyers
title: Multi-product buyers
slash_command: /multi-product-buyers
group: Segments
owner: intempt
summary: Customers who have bought more than once and spent a meaningful amount, so cross-sell offers
  reach people with broad interest.
description: >-
  Customers who have purchased across multiple distinct products: cross-sell-ready cohort.
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
    title: Build the repeat-spend list
    summary: >-
      Users with 2 or more orders in the last 180 days and lifetime value of 200 or more.
    builds: segment
    description: |-
      Create a segment called "Multi-Product Buyers".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: order_created occurred >= 2 times in last 180 days
      - AND Attribute: lifetime_value >= 200
      Description: Customers with multiple orders and meaningful spend. Cross-sell-ready cohort: broader product affinity than single-category buyers.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Multi-product buyers

Customers who have bought more than once and spent a meaningful amount, so cross-sell offers reach people with broad interest.

## Steps

1. **Build the repeat-spend list** (builds segment)

   Users with 2 or more orders in the last 180 days and lifetime value of 200 or more.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
