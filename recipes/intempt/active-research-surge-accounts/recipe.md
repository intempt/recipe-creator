---
id: active-research-surge-accounts
title: Accounts researching pricing now
slash_command: /active-research-surge-accounts
group: Segments
owner: intempt
curator: harish
summary: >-
  Users who viewed your pricing page 3 or more times in the past 7 days, so an AE can reach out while they are
  still looking.
description: >-
  A user segment based on per-user event conditions: 3+ pricing page views in the last 7 days.
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
    - The page_viewed event in your project
    - The page_url property on those events
    - The has_open_deal attribute on accounts
  writes:
    - A new segment, from step 1 "Build the pricing-surge list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the pricing-surge list
    summary: >-
      Accounts where users viewed a page whose URL contains /pricing 3 or more times in the last 7 days,
      and no deal is currently open.
    builds: segment
    description: |-
      Build a segment of accounts named "Active Research Surge Accounts".
      An account is in the segment only when all of these are true:
      - the users in the account together did the page_viewed event with a page_url that contains "/pricing" 3 or more times in the last 7 days
      - its has_open_deal attribute is false
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accounts researching pricing now

Users who viewed your pricing page 3 or more times in the past 7 days, so an AE can reach out while they are still looking.

## Steps

1. **Build the pricing-surge list** (builds segment)

   Accounts where users viewed a page whose URL contains /pricing 3 or more times in the last 7 days, and no deal is currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The page_viewed event in your project
- The page_url property on those events
- The has_open_deal attribute on accounts

Writes:

- A new segment, from step 1 "Build the pricing-surge list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
