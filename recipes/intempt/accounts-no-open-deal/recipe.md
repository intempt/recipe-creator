---
id: accounts-no-open-deal
title: Healthy accounts with no open deal
slash_command: /accounts-no-open-deal
group: Segments
owner: intempt
summary: Healthy customer accounts nobody is currently selling into, so AEs can see where the expansion
  room is.
description: >-
  Healthy customer accounts with no current open deal: whitespace expansion opportunity.
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
    title: Build the whitespace list
    summary: >-
      Accounts marked healthy, with no open deal, 3 or more users, and 5 or more sessions across those
      users in the last 30 days.
    builds: segment
    description: |-
      Create a segment called "Accounts With No Open Deal".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: has_open_deal = false
      - AND Attribute: account_health = "healthy"
      - AND Attribute: users_count >= 3
      - AND Event: session_start (across users in account) occurred >= 5 times in last 30 days
      Description: Healthy active accounts with no open deal: ready for expansion conversation. Trigger AE whitespace task or executive outreach.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Healthy accounts with no open deal

Healthy customer accounts nobody is currently selling into, so AEs can see where the expansion room is.

## Steps

1. **Build the whitespace list** (builds segment)

   Accounts marked healthy, with no open deal, 3 or more users, and 5 or more sessions across those users in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
