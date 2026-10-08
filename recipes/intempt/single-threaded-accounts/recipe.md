---
id: single-threaded-accounts
title: Single-threaded open deals
slash_command: /single-threaded-accounts
group: Segments
owner: intempt
curator: harish
summary: Open deals at larger companies where only one person is engaged, so an AE can bring more stakeholders
  in before it stalls.
description: >-
  Multi-user companies where only 1 user is engaged: multi-threading risk for enterprise SaaS.
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
    - The employees, users_count and has_open_deal attributes on accounts
  writes:
    - A new segment, from step 1 "Build the single-threaded list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the single-threaded list
    summary: >-
      Accounts with more than 50 employees, exactly 1 engaged user, and a deal currently open.
    builds: segment
    description: |-
      Build a segment of accounts named "Single-Threaded Accounts".
      An account is in the segment only when all of these are true:
      - its employees attribute is more than 50
      - its users_count attribute is exactly 1
      - its has_open_deal attribute is true
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Single-threaded open deals

Open deals at larger companies where only one person is engaged, so an AE can bring more stakeholders in before it stalls.

## Steps

1. **Build the single-threaded list** (builds segment)

   Accounts with more than 50 employees, exactly 1 engaged user, and a deal currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The employees, users_count and has_open_deal attributes on accounts

Writes:

- A new segment, from step 1 "Build the single-threaded list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
