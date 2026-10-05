---
id: accounts-no-open-deal
title: Healthy accounts with no open deal
slash_command: /accounts-no-open-deal
group: Segments
owner: intempt
curator: harish
summary: >-
  Customer accounts with no open deal and account-level health attributes, plus per-user recent session
  activity, so AEs can review expansion whitespace.
description: >-
  Accounts filtered by account attributes such as customer status, health, and no open deal, with per-user
  event conditions for recent session_start. No cross-user event rollup.
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
touches:
  reads:
    - The session_start event in your project
    - The has_open_deal, account_health and users_count attributes on accounts
  writes:
    - A new segment, from step 1 "Build the whitespace list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the whitespace list
    summary: >-
      Accounts marked healthy, with no open deal, 3 or more users, and 5 or more sessions across those
      users in the last 30 days.
    builds: segment
    description: |-
      Build a segment of accounts named "Accounts With No Open Deal".
      An account is in the segment only when all of these are true:
      - its has_open_deal attribute is false
      - its account_health attribute is "healthy"
      - its users_count attribute is 3 or more
      - the users in the account together did the session_start event 5 or more times in the last 30 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Healthy accounts with no open deal

Customer accounts with no open deal and account-level health attributes, plus per-user recent session activity, so AEs can review expansion whitespace.

## Steps

1. **Build the whitespace list** (builds segment)

   Accounts marked healthy, with no open deal, 3 or more users, and 5 or more sessions across those users in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The session_start event in your project
- The has_open_deal, account_health and users_count attributes on accounts

Writes:

- A new segment, from step 1 "Build the whitespace list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
