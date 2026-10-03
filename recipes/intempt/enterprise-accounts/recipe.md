---
id: enterprise-accounts
title: Enterprise accounts
slash_command: /enterprise-accounts
group: Segments
owner: intempt
summary: Companies with 1,000 or more employees, so your enterprise sellers work from one list.
description: >-
  Large companies (1000+ employees): AE white-glove sales-motion routing.
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
    title: Build the enterprise list
    summary: >-
      Accounts with 1,000 or more employees. Updates as company size data changes.
    builds: segment
    description: |-
      Create a segment called "Enterprise Accounts".
      Object: Accounts
      Rules:
      - Attribute: employees >= 1000
      Description: Companies with 1000+ employees. Foundation for enterprise sales-motion routing: these accounts get AE white-glove engagement: dedicated account plans, executive-sponsor outreach, and quarterly business reviews. Universal B2B routing pattern.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Enterprise accounts

Companies with 1,000 or more employees, so your enterprise sellers work from one list.

## Steps

1. **Build the enterprise list** (builds segment)

   Accounts with 1,000 or more employees. Updates as company size data changes.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
