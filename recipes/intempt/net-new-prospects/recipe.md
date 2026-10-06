---
id: net-new-prospects
title: Net-new prospect accounts
slash_command: /net-new-prospects
group: Segments
owner: intempt
curator: harish
summary: Accounts created in the last week that have barely done anything yet, so SDRs know who to contact
  first.
description: >-
  Recently identified accounts with minimal engagement: SDR first-touch foundation.
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
    - media
  vertical:
    - sales-led
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
touches:
  reads:
    - The created_at, total_events, account_lifecycle and has_open_deal attributes on accounts
  writes:
    - A new segment, from step 1 "Build the net-new account list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the net-new account list
    summary: >-
      Accounts created in the last 7 days, with 5 or fewer events, lifecycle set to prospect, and no open
      deal. Updates as new accounts arrive.
    builds: segment
    description: |-
      Build a segment of accounts named "Net-New Prospects".
      An account is in the segment only when all of these are true:
      - its created_at attribute is within the last 7 days
      - its total_events attribute is 5 or less
      - its account_lifecycle attribute is "prospect"
      - its has_open_deal attribute is false
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Net-new prospect accounts

Accounts created in the last week that have barely done anything yet, so SDRs know who to contact first.

## Steps

1. **Build the net-new account list** (builds segment)

   Accounts created in the last 7 days, with 5 or fewer events, lifecycle set to prospect, and no open deal. Updates as new accounts arrive.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The created_at, total_events, account_lifecycle and has_open_deal attributes on accounts

Writes:

- A new segment, from step 1 "Build the net-new account list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
