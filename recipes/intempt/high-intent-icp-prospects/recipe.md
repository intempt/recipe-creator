---
id: high-intent-icp-prospects
title: ICP accounts showing intent
slash_command: /high-intent-icp-prospects
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the hot ICP list
    summary: >-
      Accounts with 50 to 1,000 employees in SaaS, Technology, Fintech, or Financial Services, where users
      viewed both a /pricing page and a /docs page in the last 7 days, and no deal is open.
    builds: segment
    description: |-
      Create a segment called "High-Intent ICP Prospects".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: employees is between 50 and 1000
      - AND Attribute: industry is one of ["SaaS", "Technology", "Fintech", "Financial Services"]
      - AND Event (via users in account): page_viewed where page_url contains "/pricing" occurred >= 1 time in last 7 days
      - AND Event (via users in account): page_viewed where page_url contains "/docs" occurred >= 1 time in last 7 days
      - AND Attribute: has_open_deal = false
      Description: ICP-matching accounts with hot buying signals this week. Highest-priority cohort for SDR outreach: pre-qualified and actively researching.
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

## Availability

Install now: every step builds something the engine supports today.
