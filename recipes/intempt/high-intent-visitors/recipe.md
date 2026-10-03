---
id: high-intent-visitors
title: High-intent visitors
slash_command: /high-intent-visitors
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the high-intent list
    summary: >-
      Users with no plan or the free plan who viewed both a /pricing page and a /docs page in the last
      14 days.
    builds: segment
    description: |-
      Create a segment called "High-Intent Visitors".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: page_viewed where page_url contains "/pricing" occurred >= 1 time in last 14 days
      - AND Event: page_viewed where page_url contains "/docs" occurred >= 1 time in last 14 days
      - AND Attribute: plan_name is empty OR plan_name = "free"
      Description: Non-customers (or free-plan users) showing strong buying signals across pricing and docs. Prioritize for sales outreach or in-app upgrade prompt.
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

## Availability

Install now: every step builds something the engine supports today.
