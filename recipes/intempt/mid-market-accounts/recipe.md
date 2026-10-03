---
id: mid-market-accounts
title: Mid-market accounts
slash_command: /mid-market-accounts
group: Segments
owner: intempt
summary: Companies with 100 to 1,000 employees, so your inside sales team works from one list.
description: >-
  Mid-sized companies (100-1000 employees): inside-sales / scaled-AE routing.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - b2b
    - saas
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
steps:
  - id: s1
    title: Build the mid-market list
    summary: >-
      Accounts with 100 or more employees and fewer than 1,000.
    builds: segment
    description: |-
      Create a segment called "Mid-Market Accounts".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: employees >= 100
      - AND Attribute: employees < 1000
      Description: Companies with 100-1000 employees. Foundation for inside-sales / scaled-AE routing: these accounts get standardized playbooks, semi-personalized campaigns, and shorter sales cycles than enterprise. Universal B2B routing pattern.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Mid-market accounts

Companies with 100 to 1,000 employees, so your inside sales team works from one list.

## Steps

1. **Build the mid-market list** (builds segment)

   Accounts with 100 or more employees and fewer than 1,000.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
