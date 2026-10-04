---
id: high-intent-icp-prospects
title: ICP accounts showing intent
slash_command: /high-intent-icp-prospects
group: Segments
owner: intempt
curator: harish
summary: Accounts that fit your ideal profile and read both your pricing and your docs this week, with
  no deal open yet.
description: >-
  ICP-matching accounts with active intent signals (pricing + docs visited recently).
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
    - The employees, industry and has_open_deal attributes on accounts
  writes:
    - A new segment, from step 1 "Build the hot ICP list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the hot ICP list
    summary: >-
      Accounts with 50 to 1,000 employees in SaaS, Technology, Fintech, or Financial Services, where users
      viewed both a /pricing page and a /docs page in the last 7 days, and no deal is open.
    builds: segment
    description: |-
      Build a segment of accounts named "High-Intent ICP Prospects".
      An account is in the segment only when all of these are true:
      - its employees attribute is between 50 and 1000
      - its industry attribute is one of "SaaS", "Technology", "Fintech" or "Financial Services"
      - the users in the account together did the page_viewed event with a page_url that contains "/pricing" at least once in the last 7 days
      - the users in the account together did the page_viewed event with a page_url that contains "/docs" at least once in the last 7 days
      - its has_open_deal attribute is false
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# ICP accounts showing intent

Accounts that fit your ideal profile and read both your pricing and your docs this week, with no deal open yet.

## Steps

1. **Build the hot ICP list** (builds segment)

   Accounts with 50 to 1,000 employees in SaaS, Technology, Fintech, or Financial Services, where users viewed both a /pricing page and a /docs page in the last 7 days, and no deal is open.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The page_viewed event in your project
- The page_url property on those events
- The employees, industry and has_open_deal attributes on accounts

Writes:

- A new segment, from step 1 "Build the hot ICP list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
