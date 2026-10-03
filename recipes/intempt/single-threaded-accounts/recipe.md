---
id: single-threaded-accounts
title: Single-threaded open deals
slash_command: /single-threaded-accounts
group: Segments
owner: intempt
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
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
steps:
  - id: s1
    title: Build the single-threaded list
    summary: >-
      Accounts with more than 50 employees, exactly 1 engaged user, and a deal currently open.
    builds: segment
    description: |-
      Create a segment called "Single-Threaded Accounts".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: employees > 50
      - AND Attribute: users_count = 1
      - AND Attribute: has_open_deal = true
      Description: Multi-user-sized companies (50+ employees) where only one user is engaged with our product, AND there's an active deal. Critical multi-threading risk: single-threaded enterprise deals lose at 2-3x the rate of multi-threaded deals. Trigger AE plays to identify and engage 2-3 additional stakeholders before deal close.
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

## Availability

Install now: every step builds something the engine supports today.
