---
id: mid-market-accounts
title: Mid-market accounts
slash_command: /mid-market-accounts
group: Segments
owner: intempt
curator: harish
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
  industry:
    - ai
    - b2b-saas
  vertical:
    - sales-led
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
touches:
  reads:
    - The employees attribute on accounts
  writes:
    - A new segment, from step 1 "Build the mid-market list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the mid-market list
    summary: >-
      Accounts with 100 or more employees and fewer than 1,000.
    builds: segment
    description: |-
      Build a segment of accounts named "Mid-Market Accounts".
      An account is in the segment only when all of these are true:
      - its employees attribute is 100 or more
      - its employees attribute is less than 1000
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

## What this recipe touches

Reads:

- The employees attribute on accounts

Writes:

- A new segment, from step 1 "Build the mid-market list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
