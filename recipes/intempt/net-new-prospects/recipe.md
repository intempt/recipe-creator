---
id: net-new-prospects
title: Net-new prospect accounts
slash_command: /net-new-prospects
group: Segments
owner: intempt
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
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
steps:
  - id: s1
    title: Build the net-new account list
    summary: >-
      Accounts created in the last 7 days, with 5 or fewer events, lifecycle set to prospect, and no open
      deal. Updates as new accounts arrive.
    builds: segment
    description: |-
      Create a segment called "Net-New Prospects".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: created_at is within last 7 days
      - AND Attribute: total_events <= 5
      - AND Attribute: account_lifecycle = "prospect"
      - AND Attribute: has_open_deal = false
      Description: Accounts identified in the last 7 days with minimal engagement so far. Foundation for SDR first-touch sequences: these are the freshest entries to your TAL or your inbound feed, deserving immediate qualification within ICP-fit and intent-strength frameworks.
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

## Availability

Install now: every step builds something the engine supports today.
